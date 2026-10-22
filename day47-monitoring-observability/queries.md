# Day 47 — PromQL Practice Cheat Sheet

Run these queries at [http://localhost:9090](http://localhost:9090) while Prometheus port-forwarding is active. Use the Table view when you need to read exact numeric values.

## 1. Scrape health

```promql
up
```

Each returned time series has a value. **1 = scrape succeeded; 0 = scrape failed.** Labels such as `job`, `instance`, `namespace`, and `metrics_path` identify the target.

Count failed targets:

```promql
sum(up == 0)
```

If this returns no series, try `up` and inspect the results directly; PromQL comparisons can omit false series.

## 2. Count targets

```promql
count(up)
```

Count currently successful targets:

```promql
sum(up)
```

Compare the results to understand how many targets are configured and how many are currently scraped successfully.

## 3. Pod count by namespace

```promql
count by (namespace) (kube_pod_info)
```

Uses kube-state-metrics. This is a count of pod objects represented by the metric, not a count of only Ready pods.

## 4. Pods not Ready

```promql
kube_pod_status_ready{condition="true"} == 0
```

Returns pod series that report not Ready. Check namespace and pod labels before deciding whether an item is a problem.

## 5. Container restart increases

```promql
increase(kube_pod_container_status_restarts_total[10m])
```

Estimates restart-counter increases over the last 10 minutes. A restart by itself is not proof of a current failure; inspect the pod events and previous logs.

## 6. CPU usage by pod

```promql
sum by (namespace, pod) (
  rate(container_cpu_usage_seconds_total{container!="", image!=""}[5m])
)
```

Returns CPU usage in cores. For example, approximately `0.04` means four-hundredths of one CPU core. Some container series may be absent depending on the cluster and scrape configuration.

## 7. Memory working set by pod

```promql
sum by (namespace, pod) (
  container_memory_working_set_bytes{container!="", image!=""}
)
```

Returns bytes. This metric depends on cAdvisor metrics being available. If it returns no data, test `container_memory_rss` and inspect the configured targets.

## 8. Node CPU usage percentage

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

Uses Node Exporter. It estimates the percentage of CPU time not spent idle. This is not the same measurement as `kubectl top`.

## 9. Node memory usage percentage

```promql
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

Uses Node Exporter metrics to estimate memory not currently available. Metric availability depends on the scrape configuration.

## Important differences

- `kubectl top` uses Metrics Server and shows recent resource measurements.
- Prometheus queries read metrics collected by Prometheus targets.
- Grafana displays query results; it does not itself collect Kubernetes metrics.
- A label set is not the numeric value. In Prometheus Table view, read the **Value** column.
- Avoid treating sample thresholds in a learning lab as universal production alert thresholds.
