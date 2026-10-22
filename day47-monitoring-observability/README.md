# Day 47 — Kubernetes Monitoring Practice

A continuation of the Day 46 monitoring lab. This project uses the existing local **kind** cluster, **Prometheus**, **Grafana**, **kube-state-metrics**, **Node Exporter**, and **Metrics Server**.

## Current lab status

The user-verified environment showed these monitoring pods Ready in namespace `monitoring`:

- Grafana: `3/3 Running`
- Prometheus: `2/2 Running`
- Prometheus Operator: `1/1 Running`
- kube-state-metrics: `1/1 Running`
- Node Exporter: `1/1 Running`

Kubernetes Metrics API was also verified to return node metrics, and `kubectl top pods -A` returned CPU and memory values.

## Simple notes

- **Metrics Server** provides recent CPU and memory measurements for commands such as `kubectl top`.
- **Prometheus** scrapes configured targets and stores time-series metrics.
- **Grafana** visualizes metrics in dashboards.
- **kube-state-metrics** exposes Kubernetes object state, such as pod readiness and restart counters.
- A Prometheus query returning labels identifies a time series; inspect the **Value** column to see the actual measurement.
- For the `up` metric, `1` means a scrape succeeded and `0` means a scrape failed.
- A pod showing `Running` now can still have a restart history. Investigate restarts rather than assuming the pod is currently unhealthy.

## 1. Check Kubernetes health

Run from WSL Ubuntu:

```bash
kubectl get nodes
kubectl get pods -n monitoring
kubectl get pods -A
kubectl top nodes
kubectl top pods -A
```

Expected: the node is Ready, monitoring pods are Ready, and `kubectl top` returns resource readings. Low-usage application containers may show `0m` CPU because the displayed value is rounded.

## 2. Open Prometheus

Run this in a terminal and leave it open:

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Open [http://localhost:9090](http://localhost:9090). In **Graph**, run each query in [queries.md](queries.md). Use the Table view to inspect numeric values. Also check **Status → Targets** for scrape health.

## 3. Open Grafana

In a second terminal:

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Open [http://localhost:3000](http://localhost:3000). Use the existing Prometheus data source and import the dashboard JSON from [Day 46](../day46-monitoring-observability/grafana-dashboard.json) if you need to restore it.

## 4. Optional alert rules

`prometheus-rules.yaml` contains example PrometheusRule resources for scrape failures, unready pods, and repeated container restarts. Review and apply it only after confirming the monitoring stack and Prometheus Operator are healthy:

```bash
kubectl apply -f day47-monitoring-observability/prometheus-rules.yaml
kubectl get prometheusrules -n monitoring
```

Check whether Prometheus loaded the rules at [http://localhost:9090/rules](http://localhost:9090/rules) while port-forwarding is active.

**Important:** The existing lab disables Alertmanager to save resources. These rules can be evaluated by Prometheus, but email/chat notifications will not be sent unless Alertmanager and a receiver are configured. The rules are examples for a local learning cluster, not production-ready alert policy.

To remove the example rules:

```bash
kubectl delete -f day47-monitoring-observability/prometheus-rules.yaml
```

## 5. Troubleshooting

### Prometheus query shows no data

1. Confirm the query spelling.
2. Try `up` and inspect the Table view and Value column.
3. Check **Status → Targets** for scrape errors.
4. Confirm the relevant pod/exporter is running.
5. For optional metrics, confirm the metric exists before adding it to a dashboard.

### Grafana does not load

1. Check `kubectl get pods -n monitoring`.
2. Confirm the port-forward terminal is still running.
3. Check `kubectl get svc monitoring-grafana -n monitoring`.

### A pod has restarts

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
```

Use `--previous` to inspect the previous container instance when available. Replace the placeholders with the actual pod name and namespace.

## 6. Completion checklist

- [ ] Monitoring pods are Ready.
- [ ] `kubectl top nodes` and `kubectl top pods -A` return measurements.
- [ ] Prometheus `up` query displays numeric values.
- [ ] Prometheus **Status → Targets** has been reviewed.
- [ ] Grafana dashboard panels display data.
- [ ] Optional alert rules have been applied and checked, if desired.
- [ ] No passwords, tokens, or Kubernetes Secrets have been committed.

## What this project demonstrates

Practical Kubernetes monitoring, metrics interpretation, PromQL basics, dashboard troubleshooting, and an introduction to Prometheus alert rules.
