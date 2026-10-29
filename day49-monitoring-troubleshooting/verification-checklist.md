# Day 49 — Verification Checklist

Use this checklist after running the Day 49 diagnostics.

## Environment
- [x] Confirmed the current context is the intended local Kind cluster (`kind-devops-cluster`).
- [x] Confirmed the node is Ready after a reported node reboot.
- [x] Collected Pod, Service/endpoint, and recent Event status.

## Troubleshooting
- [x] Identified the Grafana container and inspected its termination state.
- [x] Read Grafana and Prometheus logs and Pod Events.
- [x] Distinguished observed probe failures from a confirmed root cause.
- [x] Recorded the node reboot/sandbox recreation as the confirmed wider incident event, while leaving the cause of Grafana's earlier individual restarts unconfirmed.
- [x] Avoided unneeded deployment, resource-limit, and probe changes.

## Recovery
- [x] Verified monitoring container readiness and unchanged restart counts across two checks.
- [x] Earlier diagnostics showed the relevant monitoring Services/endpoints existed.
- [x] Verified Grafana `/api/health` returned HTTP 200 and database status `ok`.
- [ ] Separately verified a Grafana Prometheus data-source query and the relevant Prometheus targets after recovery.
- [x] Recorded the observed incident timeline and remaining uncertainty in the runbook.

## GitHub
- [x] Updated project documentation with verified findings only.
- [x] Excluded credentials, Secret contents, tokens, and unredacted logs.
- [x] Committed the documentation changes to the default branch through GitHub.
