# Day 49 Runbook — Grafana or Monitoring Pod Shows 2/3 Ready

## Known symptom

During the lab, a monitoring/Grafana Pod was reported as showing **2/3 containers ready**. This means the Pod has three regular containers reported in its status and only two are ready. It does not, by itself, identify which container is unhealthy or prove the root cause.

**Incident status:** Monitoring recovered after a Kubernetes node reboot and remained stable during the observed verification window. The node reboot explains the timing of the wider disruption; the cause of Grafana's earlier individual restarts is not fully confirmed.

## 1. Incident summary (observed 2026-10-29, Saudi Arabia time)

- Cluster context: `kind-devops-cluster`.
- Node: `devops-cluster-control-plane`.
- The node's Events reported `Rebooted`; kubelet and kube-proxy then reported starting. The node was subsequently `Ready`, with `MemoryPressure=False`, `DiskPressure=False`, and `PIDPressure=False`.
- Multiple unrelated workloads showed startup or probe errors around the same period, including Grafana, Prometheus, CoreDNS, and the Prometheus operator.
- The Grafana Pod event stream reported `SandboxChanged`.
- Docker showed the Kind node container running with `RestartCount=0` and start time `2026-10-29T06:50:29Z`. This does not indicate that Docker restarted the container; the Kubernetes node/runtime restarted internally.
- Grafana's main container had last terminated with exit code `137` and reason `Error`. Exit code 137 means it received SIGKILL; it does **not alone prove** an OOM kill.
- One Grafana memory sample showed 478 MiB against a configured 384 MiB limit. A later sample showed 287 MiB. These are point-in-time readings and do not independently establish the cause of the termination.
- Earlier Grafana readiness/liveness Events included request timeouts and connection refused; an Event recorded a liveness-probe-triggered restart.
- Prometheus logs showed startup completed and the server was ready to receive web requests.

## 2. Collect evidence first

Confirm the intended context:

```bash
kubectl config current-context
kubectl get nodes
```

Inspect monitoring Pods and Events:

```bash
kubectl get pods -n monitoring -o wide
kubectl get events -A --sort-by=.lastTimestamp | tail -40
kubectl describe node devops-cluster-control-plane
```

Run the read-only helper from this folder:

```bash
chmod +x scripts/diagnose-monitoring.sh
./scripts/diagnose-monitoring.sh
```

The script accepts an optional namespace. For example, use `./scripts/diagnose-monitoring.sh monitoring`. It only reads cluster status and does not restart, delete, or modify resources.

## 3. Identify the exact unready container

Use the actual Pod name from `kubectl get pods`:

```bash
kubectl describe pod <pod-name> -n monitoring
kubectl get pod <pod-name> -n monitoring -o jsonpath='{range .status.containerStatuses[*]}{.name}{" ready="}{.ready}{" restarts="}{.restartCount}{" waiting="}{.state.waiting.reason}{" lastTermination="}{.lastState.terminated.reason}{"\\n"}{end}'
```

Look for:
- Readiness or liveness probe failures.
- A waiting reason such as `CrashLoopBackOff` or `ImagePullBackOff`.
- Repeated restarts or a previous termination reason.
- Missing configuration, permissions, or a dependency that cannot be reached.

## 4. Read logs for the specific container

Replace the placeholders with values shown in the Pod status:

```bash
kubectl logs <pod-name> -n monitoring -c <container-name> --tail=100
```

If that container has restarted and previous logs exist:

```bash
kubectl logs <pod-name> -n monitoring -c <container-name> --previous --tail=100
```

Do not publish logs until you have checked for credentials, tokens, internal endpoints, or other sensitive details.

## 5. Evidence-based interpretation

- The node reboot and `SandboxChanged` event are strong evidence for the timing of the cluster-wide disruption.
- Grafana's failed probes show that it was not accepting or answering health requests at those moments. They do not, on their own, establish why.
- Exit code 137 is consistent with SIGKILL but is not enough to label the termination `OOMKilled`.
- The earlier memory sample above the configured limit makes memory pressure a hypothesis to revisit, not a confirmed root cause.
- The exact cause of Grafana's previous repeated restarts remains **unconfirmed**.

Do not delete the Pod or restart the whole monitoring stack as the first step. If the workload is managed by Helm or a Deployment, make corrections through the owning configuration rather than editing a generated Pod directly. Do not alter resource limits or probe settings without new supporting evidence.

## 6. Recovery verification recorded

Observed after the node recovered:

- All listed monitoring Pods/containers reported Ready.
- Grafana `/api/health` returned HTTP 200 with `"database": "ok"` and version `13.2.4`.
- Grafana main container memory was 287 MiB in the later sample, below its configured 384 MiB limit.
- Restart counts were unchanged across two consecutive checks: Grafana `14,6,6`; Prometheus operator `9`; kube-state-metrics `10`; node exporter `6`; Prometheus `6,6`.

This verifies recovery and stable restart counts during the observed window only; it does not guarantee future stability. The Grafana UI was health-checked through its API endpoint. A separate Prometheus data-source query/target verification was not recorded in this incident.

## 7. Record the incident

- Date: 2026-10-29.
- Cluster/node: `kind-devops-cluster` / `devops-cluster-control-plane`.
- Affected workloads: Grafana and other monitoring/system pods around the node reboot.
- Relevant evidence: node `Rebooted` Event; Grafana `SandboxChanged`; probe failures; Grafana exit code 137; health endpoint HTTP 200 after recovery.
- Confirmed contributing event: Kubernetes node reboot and pod sandbox recreation.
- Root cause of Grafana's earlier individual restarts: **unconfirmed**.
- Fix applied: no manual deployment/resource/probe changes; recovery followed node/runtime restart.
- Verification: all monitoring containers Ready, health API HTTP 200, restart counts unchanged across two checks.
- Git commit: see the commit history for this runbook.

If additional restarts occur, immediately capture `kubectl describe pod`, `kubectl logs --previous`, and the latest node Events before changing configuration.
