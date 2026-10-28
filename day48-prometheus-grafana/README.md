# Day 48 — Prometheus Queries and Grafana Dashboard

## Goal
Practice querying Prometheus with PromQL and displaying Kubernetes monitoring results in Grafana.

## PromQL queries

| Query | Purpose |
|---|---|
| `up` | Returns one time series per scrape target: 1 means the scrape succeeded; 0 means it failed. |
| `count(up)` | Counts the `up` time series, including both healthy and unhealthy targets. |
| `sum(up)` | Counts targets currently up because healthy targets contribute 1 and failed targets contribute 0. |
| `count(up == 0)` | Counts targets whose current `up` value is 0. |
| `sum(up == 0)` | **Not suitable for counting down targets:** the comparison filters to series whose value is 0, so their sum is 0. Use `count(up == 0)` instead. |

Prometheus documents the `up` metric as a way to check whether a target scrape succeeds. See [Prometheus first steps](https://prometheus.io/docs/introduction/first_steps/) and [PromQL basics](https://prometheus.io/docs/prometheus/latest/querying/basics/).

## Grafana dashboards

### Day 48 — Kubernetes Monitoring
Dashboard panels:
1. **Prometheus Targets UP** — Stat visualization, query: `sum(up)`
2. **Prometheus Targets DOWN** — Stat visualization; use `count(up == 0)` to count down targets.

The dashboard JSON in this folder uses the corrected down-target query. If the dashboard is already imported/saved in a running Grafana instance, update that panel's query there as well; changing the repository JSON does not automatically change a dashboard already stored in Grafana.

### Day 46 — Kubernetes Monitoring Overview
The separate Day 46 dashboard was verified in Grafana and contains six panels for scrape target status, pods by namespace, container CPU and memory, and node CPU and memory.

## Observed lab status

At the time of verification, the `up` query returned 16 target series:
- **12 UP**
- **4 DOWN**

The down targets were:
- `kube-scheduler` — `172.19.0.2:10259`
- `kube-etcd` — `172.19.0.2:2381`
- `kube-proxy` — `172.19.0.2:10249`
- `kube-controller-manager` — `172.19.0.2:10257`

The errors observed for these endpoints were connection refused. In this local Kind lab, the control-plane metrics endpoints are configured to bind to localhost or have metrics binding disabled, so Prometheus cannot scrape them at the node IP. This does not by itself prove that the Kubernetes control-plane components are stopped. The remaining 12 targets, including Grafana, Prometheus, the API server, kubelet, CoreDNS, node-exporter, and kube-state-metrics, were up.

These counts are a point-in-time observation and may change as targets change. Do not change the Kind control-plane configuration solely to make every scrape target green unless you deliberately want to modify and test those settings.

## Access the local services

Run each port-forward in its own terminal and keep it open:

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9091:9090
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

- Prometheus: http://localhost:9091/
- Grafana: http://localhost:3000/

If a local port is already in use, choose another unused local port. A port-forward only works while its terminal process is running.

## Validation completed
- Prometheus health endpoint and API query succeeded.
- Grafana Prometheus data source health returned OK.
- Both the Day 46 overview and Day 48 dashboards were opened and showed data.
- The `up` query returned 16 target series, with 12 up and 4 down at the time of checking.
- Dashboard JSON is stored in this folder for version control.
