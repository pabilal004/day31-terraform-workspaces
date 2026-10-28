#!/usr/bin/env bash
set -u

# Read-only Kubernetes diagnostic collector for the Day 49 learning lab.
# This script does not restart, delete, or modify cluster resources.

if ! command -v kubectl >/dev/null 2>&1; then
  echo "ERROR: kubectl was not found. Install/configure kubectl first." >&2
  exit 1
fi

if ! kubectl config current-context >/dev/null 2>&1; then
  echo "ERROR: No usable Kubernetes context is configured." >&2
  exit 1
fi

echo "=================================================="
echo "Kubernetes diagnostics — read-only"
echo "Timestamp: $(date -Is 2>/dev/null || date)"
echo "Context:   $(kubectl config current-context)"
echo "=================================================="

run_check() {
  local title="$1"
  shift
  echo
  echo "---- ${title} ----"
  "$@" || echo "WARNING: command failed: $*"
}

run_check "Nodes" kubectl get nodes -o wide
run_check "Pods across namespaces" kubectl get pods -A -o wide
run_check "Services across namespaces" kubectl get services -A
run_check "Endpoints across namespaces" kubectl get endpoints -A
run_check "Recent Events" kubectl get events -A --sort-by=.metadata.creationTimestamp

echo
echo "Diagnostics complete. No resources were modified."
echo "Review output for sensitive names, addresses, or log details before sharing."
