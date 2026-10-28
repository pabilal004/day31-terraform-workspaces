# Day 49 — Monitoring and Troubleshooting

## Goal

Practice a safe, repeatable troubleshooting workflow for Kubernetes workloads and Prometheus/Grafana monitoring. This project builds on the Prometheus and Grafana work from Days 46–48.

## Troubleshooting workflow

1. **Observe** the symptom in Grafana or Prometheus.
2. **Gather evidence** from Kubernetes status, Events, logs, Services, and endpoints.
3. **Form a hypothesis** based on the evidence.
4. **Apply the smallest safe fix** only after identifying a likely cause.
5. **Verify recovery** in Kubernetes and Prometheus.
6. **Document** the cause, fix, and verification result.

Do not restart or delete resources before collecting evidence unless there is an urgent operational reason.

## Prerequisites

- A working Kubernetes context (the local Kind cluster used in this learning lab is `kind-devops-cluster`).
- `kubectl` configured for that cluster.
- Prometheus and Grafana deployed from the earlier monitoring labs.
- Optional: `jq` for formatting JSON output.

Check the context before running commands:

```bash
kubectl config current-context
kubectl get nodes
```

## Quick health checks

```bash
kubectl get pods -A
kubectl get services -A
kubectl get endpoints -A
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

For a specific Pod:

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --all-containers=true
```

If a container restarted, inspect its previous logs when available:

```bash
kubectl logs <pod-name> -n <namespace> --previous
```

Replace placeholders with the real Pod name and namespace.

## Common symptoms

| Symptom | First checks |
| --- | --- |
| `CrashLoopBackOff` | Current and previous logs, Pod description, Events, startup configuration |
| `ImagePullBackOff` | Image name/tag, registry reachability and credentials, Events |
| Pod remains `Pending` | Events, node readiness, resource requests, scheduling constraints |
| Service has no endpoints | Service selector, Pod labels, readiness, namespace |
| Prometheus target is DOWN | Target address/port, scrape configuration, network path, metrics endpoint |
| Grafana panel is empty | Selected data source, time range, PromQL query, labels and target availability |

## Prometheus query examples

See [queries.md](queries.md) for safe starting queries, including target scrape status and failed-scrape counts.

Important: `up = 0` means the Prometheus scrape failed. It does **not** prove that the application process has crashed. Also, `count(up == 0)` counts matching time series; interpret it as a target count only when the scrape configuration produces one relevant series per target.

## Read-only diagnostic helper

The script at [scripts/collect-diagnostics.sh](scripts/collect-diagnostics.sh) gathers basic Kubernetes status, Events, Services and endpoint information. It is designed to read information only; it does not delete, restart, or modify resources.

Run it with:

```bash
chmod +x scripts/collect-diagnostics.sh
./scripts/collect-diagnostics.sh
```

The script may print cluster information and resource names. Review its output before sharing it publicly and redact sensitive details if any appear.

## Focused monitoring triage

For the previously observed symptom where a monitoring/Grafana Pod showed `2/3` containers ready, use the dedicated [Grafana readiness runbook](runbooks/grafana-readiness-2-of-3.md). The symptom alone does not identify the failing container or root cause, so the live cluster must be checked before recording a fix.

Run the read-only monitoring diagnostics helper:

```bash
chmod +x scripts/diagnose-monitoring.sh
./scripts/diagnose-monitoring.sh
```

Optionally pass a namespace: `./scripts/diagnose-monitoring.sh monitoring`. It reports Pod/container readiness, restarts, waiting reasons, Services, endpoints, and recent Events. It does not modify resources.

Use the [verification checklist](verification-checklist.md) to record what was actually checked and confirmed. Keep credentials, Secret values, tokens, and unredacted logs out of GitHub.

## Verification checklist

- [ ] Confirmed the intended Kubernetes context.
- [ ] Checked node and Pod status.
- [ ] Reviewed Events and relevant application logs.
- [ ] Checked Service selectors and endpoint addresses.
- [ ] Checked Prometheus target status and the relevant query.
- [ ] Applied only an evidence-based correction, if needed.
- [ ] Verified application behavior and monitoring after the correction.
- [ ] Recorded the actual observed cause and result.

## Lab result record

Do not mark an issue as fixed until the local cluster has been checked. Record findings here after running the diagnostics:

- Date:
- Symptom:
- Evidence collected:
- Root cause (confirmed or still unknown):
- Fix applied (if any):
- Kubernetes verification:
- Prometheus/Grafana verification:

## Safety notes

- Diagnostic commands are read-only.
- Avoid publishing credentials, Secret contents, tokens, private endpoints, or unredacted logs.
- A dashboard showing a DOWN target should trigger investigation, not an automatic restart.
