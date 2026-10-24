# Day 48 — Prometheus Queries and Grafana Dashboard

## Goal
Practice querying Prometheus with PromQL and displaying Kubernetes monitoring results in Grafana.

## PromQL queries practiced

| Query | Purpose |
|---|---|
| `up` | Shows the up/down value for each scraped target (1 = up, 0 = down). |
| `count(up)` | Counts the `up` time series returned. |
| `sum(up)` | Adds the `up` values, giving the number of targets currently up. |
| `sum(up == 0)` | Counts targets currently reporting down. |

## Grafana dashboard
Dashboard name used in the local lab: **Day 48 - Kubernetes Monitoring**

Panels created:
1. **Prometheus Targets UP** — Stat visualization, query: `sum(up)`
2. **Prometheus Targets DOWN** — Stat visualization, query: `sum(up == 0)`

## Lab notes
- The user's observed `count(up)` result was 16.
- The observed `sum(up)` result was 12.
- The observed `sum(up == 0)` result was 0.
- Prometheus showed a single result series for `up` in one query result. A result-series count is not the same as the numeric value of a metric.
- These values are a point-in-time observation and may change as targets change.

## How to access the local services
Run each port-forward in its own terminal and keep it open:

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9091:9090
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

- Prometheus: http://localhost:9091/
- Grafana: http://localhost:3000/

If a local port is already in use, choose another unused local port.

## Validation
- Prometheus queries executed in the local lab.
- Two Stat panels created and the dashboard saved in Grafana.
- This repository documentation records the manually created dashboard; it does not claim the Grafana dashboard JSON was exported or provisioned from GitHub.
