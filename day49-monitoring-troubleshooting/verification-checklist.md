# Day 49 — Verification Checklist

Use this checklist after running the Day 49 diagnostics.

## Environment
- [ ] Confirmed the current context is the intended local Kind cluster.
- [ ] Confirmed the node is Ready.
- [ ] Collected Pod, Service, endpoint, and recent Event status.

## Troubleshooting
- [ ] Identified the exact Pod and container showing a problem.
- [ ] Read the Pod description and relevant logs.
- [ ] Distinguished a failed Prometheus scrape from an application crash.
- [ ] Identified a root cause from evidence, or explicitly recorded it as unconfirmed.
- [ ] Applied only a small, evidence-based correction, if needed.

## Recovery
- [ ] Verified container readiness and stable restart counts.
- [ ] Verified the relevant Service has expected endpoints.
- [ ] Verified Grafana opens and its Prometheus data source works.
- [ ] Verified relevant Prometheus queries/targets after the change.
- [ ] Recorded the actual observed result in the incident runbook.

## GitHub
- [ ] Updated the project documentation with verified findings only.
- [ ] Excluded credentials, Secret contents, tokens, and unredacted logs.
- [ ] Committed and pushed the project changes.
