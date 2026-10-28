#!/usr/bin/env bash
set -uo pipefail

# Read-only triage helper for the Day 49 monitoring lab.
# It does not restart, delete, or modify Kubernetes resources.

NAMESPACE="${1:-monitoring}"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "ERROR: kubectl was not found." >&2
  exit 1
fi

CONTEXT="$(kubectl config current-context 2>/dev/null)" || {
  echo "ERROR: No usable kubectl context is configured." >&2
  exit 1
}

if ! kubectl get nodes >/dev/null 2>&1; then
  echo "ERROR: Cannot reach the Kubernetes API using context: ${CONTEXT}" >&2
  echo "Check the cluster/context before continuing." >&2
  exit 1
fi

echo "=================================================="
echo "Day 49 monitoring triage (read-only)"
echo "Timestamp: $(date -Is 2>/dev/null || date)"
echo "Context:   ${CONTEXT}"
echo "Namespace: ${NAMESPACE}"
echo "=================================================="

run_check() {
  local title="$1"
  shift
  echo
  echo "---- ${title} ----"
  "$@" || echo "WARNING: command failed: $*"
}

if ! kubectl get namespace "${NAMESPACE}" >/dev/null 2>&1; then
  echo "ERROR: Namespace '${NAMESPACE}' was not found."
  echo "List namespaces with: kubectl get namespaces"
  exit 1
fi

run_check "Monitoring Pods and readiness" kubectl get pods -n "${NAMESPACE}" -o wide
run_check "Monitoring Services" kubectl get services -n "${NAMESPACE}"
run_check "Monitoring Endpoints" kubectl get endpoints -n "${NAMESPACE}"
run_check "Recent monitoring Events" kubectl get events -n "${NAMESPACE}" --sort-by=.metadata.creationTimestamp

echo
echo "---- Containers that are not ready ----"
pod_names="$(kubectl get pods -n "${NAMESPACE}" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null)" || pod_names=""
found_unready=0

while IFS= read -r pod; do
  [[ -z "${pod}" ]] && continue
  statuses="$(kubectl get pod "${pod}" -n "${NAMESPACE}" -o jsonpath='{range .status.containerStatuses[*]}{.name}{"|"}{.ready}{"|"}{.restartCount}{"|"}{.state.waiting.reason}{"|"}{.state.waiting.message}{"|"}{.lastState.terminated.reason}{"\n"}{end}' 2>/dev/null)" || statuses=""
  while IFS='|' read -r container ready restarts waiting_reason waiting_message last_reason; do
    [[ -z "${container}" ]] && continue
    if [[ "${ready}" != "true" ]]; then
      found_unready=1
      echo "Pod: ${pod} | Container: ${container} | Ready: ${ready:-unknown} | Restarts: ${restarts:-unknown}"
      [[ -n "${waiting_reason}" ]] && echo "  Waiting reason: ${waiting_reason}"
      [[ -n "${waiting_message}" ]] && echo "  Waiting message: ${waiting_message}"
      [[ -n "${last_reason}" ]] && echo "  Last termination reason: ${last_reason}"
      echo "  Next inspect: kubectl describe pod ${pod} -n ${NAMESPACE}"
      echo "  Logs:         kubectl logs ${pod} -n ${NAMESPACE} -c ${container} --tail=100"
    fi
  done <<< "${statuses}"
done <<< "${pod_names}"

if [[ "${found_unready}" -eq 0 ]]; then
  echo "No non-ready container status was found in namespace '${NAMESPACE}'."
fi

echo
echo "---- Prometheus target follow-up ----"
echo "Open the Prometheus Targets page and inspect the scrape error for any DOWN target."
echo "If Prometheus is port-forwarded locally, use the local URL already configured for this lab."
echo
echo "Triage complete. No Kubernetes resources were changed."
echo "Review output for sensitive names or internal addresses before sharing."
