# Day 46 — Monitoring and Observability

A beginner-friendly local Kubernetes monitoring lab using **Prometheus, Grafana, kube-state-metrics, Node Exporter, and Metrics Server**.

## What this project does

- Prometheus collects metrics from the Kubernetes cluster.
- Grafana displays metrics as graphs and dashboards.
- kube-state-metrics reports Kubernetes object information, such as pods and namespaces.
- Node Exporter exposes node-level metrics.
- Metrics Server provides resource usage for commands such as `kubectl top`.
- Helm installs and manages the monitoring stack.

## Simple notes

- **Monitoring:** checking whether an application or system is healthy.
- **Observability:** using metrics, logs, and traces to understand why a system behaves a certain way.
- **Metrics:** numbers measured over time, such as CPU usage, memory usage, request count, and latency.
- **Logs:** records of events, warnings, and errors.
- **Traces:** follow a request as it travels between services.
- **Prometheus:** collects and stores time-series metrics.
- **Grafana:** turns metrics into graphs and dashboards.
- **Alerting:** notifies an operator when a defined condition occurs.

## Lab environment

- Kubernetes: kind cluster named `devops-cluster`
- Namespace: `monitoring`
- Installation method: Helm chart `prometheus-community/kube-prometheus-stack`
- Prometheus retention: 6 hours (keeps this local lab lighter)
- Alertmanager: disabled for this resource-limited practice lab

## Prerequisites

- Docker
- kind and kubectl
- Helm
- A running kind cluster named `devops-cluster`

Check the cluster:

```bash
kubectl get nodes
kubectl get pods -A
helm version
```

## Install / reproduce the monitoring stack

Create the namespace:

```bash
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
```

Install or update the stack using the values file in this directory:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f day46-monitoring-observability/values.yaml \
  --wait --timeout 10m
```

Check pods and services:

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

Expected main components include Grafana, Prometheus, the Prometheus Operator, kube-state-metrics, and Node Exporter. Wait until the pods are Ready before opening the web interfaces.

## Open Grafana

In one terminal, run and leave it open:

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Open [http://localhost:3000](http://localhost:3000).

The chart commonly provisions an admin account and credentials through a Kubernetes Secret. Retrieve the password locally if needed; do not commit passwords or paste them into public issues.

If localhost does not load, verify the port-forward is still running and check:

```bash
kubectl get pods -n monitoring
kubectl get svc monitoring-grafana -n monitoring
kubectl logs -n monitoring deploy/monitoring-grafana
```

## Open Prometheus

In a second terminal, run and leave it open:

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Open [http://localhost:9090](http://localhost:9090). Visit **Status → Targets** and confirm scrape targets are UP.

## Practice PromQL queries

Try these in Prometheus first, then in Grafana Explore using the Prometheus data source:

```promql
up
```

Shows whether scrape targets are up (1) or down (0).

```promql
kube_pod_info
```

Shows information about Kubernetes pods.

```promql
container_cpu_usage_seconds_total
```

Shows cumulative CPU time used by containers. Use a rate query to estimate current CPU usage:

```promql
sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{container!="", image!=""}[5m]))
```

Container resident memory:

```promql
container_memory_rss
```

Memory working set (if exposed by the cluster's cAdvisor endpoint):

```promql
container_memory_working_set_bytes
```

Node CPU usage percentage (depends on Node Exporter metrics being available):

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

See [queries.md](queries.md) for more queries and explanations.

## Metrics Server versus Prometheus

These tools have different purposes:

```bash
kubectl top nodes
kubectl top pods -A
```

- Metrics Server provides a short-term resource view for Kubernetes autoscaling and `kubectl top`.
- Prometheus stores time-series metrics and lets you query historical values and build dashboards.

## Important local-lab note

The kind lab previously needed Metrics Server's `--kubelet-insecure-tls` option because of a local kubelet certificate mismatch. That setting is only a workaround for this disposable learning cluster. **Do not copy it into production.** Production clusters should use valid kubelet certificates and secure TLS verification.

## Import the prepared Grafana dashboard

The repository includes [grafana-dashboard.json](grafana-dashboard.json), a starter dashboard with panels for target health, pods by namespace, container CPU and memory, and node CPU and memory.

1. Open Grafana at http://localhost:3000 and sign in.
2. Open **Dashboards → New → Import** (the menu wording may vary).
3. Open the JSON file from this repository, copy its full contents, and paste them into the import box. Alternatively, download the file from GitHub and upload it if your Grafana version offers that option.
4. When asked for a Prometheus data source, select the Prometheus data source installed with the monitoring stack.
5. Click **Import**.

If a panel says “No data,” first check the same PromQL query in Prometheus at http://localhost:9090. Some node panels require Node Exporter metrics to be available; the container memory panel uses `container_memory_rss`, which was confirmed present in this lab.

## Troubleshooting checklist

1. `kubectl get pods -n monitoring` — wait for pods to become Ready.
2. Confirm the port-forward terminal remains open.
3. In Prometheus, query `up`, then check **Status → Targets**.
4. If `kube_pod_info` works but a container metric does not, check whether that specific metric exists in Prometheus before changing the installation.
5. In Grafana, verify the Prometheus data source with **Connections / Data sources → Prometheus → Save & test** (menu wording can vary by Grafana version).
6. A dashboard with no data may have the wrong time range, wrong data source, or queries for metrics not exposed by this cluster. Test the query in Prometheus first.

## Cleanup

Only run this if you intentionally want to remove the monitoring stack:

```bash
helm uninstall monitoring -n monitoring
kubectl delete namespace monitoring
```

## Learning outcome

By completing this lab, you have practiced installing a monitoring stack, checking scrape targets, confirming Kubernetes and container metrics, opening Grafana and Prometheus, and troubleshooting local access.

**Verified in this lab:** monitoring pods were Running; Prometheus targets were UP; `up`, `kube_pod_info`, `container_cpu_usage_seconds_total`, and `container_memory_rss` returned results in Prometheus. Grafana was installed and opened again. A Grafana graph/dashboard with the test query still needs a final visual check.
