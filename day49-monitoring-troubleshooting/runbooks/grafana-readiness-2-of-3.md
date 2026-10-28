# Day 49 Runbook — Grafana or Monitoring Pod Shows 2/3 Ready

## Known symptom

During the lab, a monitoring/Grafana Pod was reported as showing **2/3 containers ready**. This means the Pod has three regular containers reported in its status and only two are ready. It does not, by itself, identify which container is unhealthy or prove the root cause.

**Status:** Diagnosis and recovery must be verified against the live Kind cluster. Do not record the issue as fixed until the failing container and recovery are confirmed.

## 1. Collect evidence first

Confirm the intended context:

```bash
kubectl config current-context
kubectl get nodes
```

Inspect monitoring Pods and Events:

```bash
kubectl get pods -n monitoring -o wide
kubectl get events -n monitoring --sort-by=.metadata.creationTimestamp
```

Run the read-only helper from this folder:

```bash
chmod +x scripts/diagnose-monitoring.sh
./scripts/diagnose-monitoring.sh
```

The script accepts an optional namespace. For example, use `./scripts/diagnose-monitoring.sh monitoring`. It only reads cluster status and does not restart, delete, or modify resources.

## 2. Identify the exact unready container

Use the actual Pod name from `kubectl get pods`:

```bash
kubectl describe pod <pod-name> -n monitoring
kubectl get pod <pod-name> -n monitoring -o jsonpath='{range .status.containerStatuses[*]}{.name}{" ready="}{.ready}{" restarts="}{.restartCount}{" waiting="}{.state.waiting.reason}{" lastTermination="}{.lastState.terminated.reason}{"\n"}{end}'
```

Look for:
- Readiness or liveness probe failures.
- A waiting reason such as `CrashLoopBackOff` or `ImagePullBackOff`.
- Repeated restarts or a previous termination reason.
- Missing configuration, permissions, or a dependency that cannot be reached.

## 3. Read logs for the specific container

Replace the placeholders with values shown in the Pod status:

```bash
kubectl logs <pod-name> -n monitoring -c <container-name> --tail=100
```

If that container has restarted and previous logs exist:

```bash
kubectl logs <pod-name> -n monitoring -c <container-name> --previous --tail=100
```

Do not publish logs until you have checked for credentials, tokens, internal endpoints, or other sensitive details.

## 4. Choose a fix based on evidence

- **Probe failure:** check the configured probe path, port, timing, and container health.
- **Configuration error:** verify the referenced ConfigMap/arguments and correct the source configuration.
- **Dependency or endpoint failure:** check the relevant Service and its endpoints.
- **Image pull failure:** verify the image name/tag and registry access.
- **Resource pressure or scheduling issue:** review Pod Events and node/resource status.

Do not delete the Pod or restart the whole monitoring stack as the first step. If the workload is managed by Helm or a Deployment, make corrections through the owning configuration rather than editing a generated Pod directly.

## 5. Verify recovery

After an evidence-based fix:

```bash
kubectl get pods -n monitoring -o wide
kubectl get events -n monitoring --sort-by=.metadata.creationTimestamp
kubectl get services,endpoints -n monitoring
```

Confirm all intended containers are ready, restart counts are stable, the Grafana UI and Prometheus data source work, and the relevant Prometheus targets/queries return expected data.

## 6. Record the incident

- Date/time:
- Pod name and namespace:
- Unready container:
- Readiness/waiting reason:
- Relevant Event or sanitized log evidence:
- Confirmed root cause:
- Fix applied:
- Pod/container readiness after fix:
- Grafana and Prometheus verification:
- Git commit containing the documented change:

If the root cause is still unknown, record it as **unconfirmed**. Never invent a successful recovery result.
