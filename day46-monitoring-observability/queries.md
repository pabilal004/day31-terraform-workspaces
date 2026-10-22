# Day 46 — PromQL Query Cheat Sheet

Run these in Prometheus at `http://localhost:9090`. Once they work there, try them in Grafana Explore.

## 1. Are targets working?

```promql
up
```

A value of `1` means a target is being scraped successfully; `0` means it is not.

## 2. Kubernetes pod information

```promql
kube_pod_info
```

Returns pod metadata such as namespace, pod name, and node.

## 3. Container CPU counter

```promql
container_cpu_usage_seconds_total
```

This is a cumulative counter, not a percentage. Use `rate()` to estimate CPU use per second.

```promql
sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{container!="", image!=""}[5m]))
```

## 4. Container memory

```promql
container_memory_rss
```

Resident memory used by a container, in bytes.

```promql
container_memory_working_set_bytes
```

Working-set memory, in bytes. This metric may be absent on some configurations; test availability before using it in a dashboard.

## 5. Node CPU (Node Exporter)

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

Estimates the percentage of CPU time not spent idle.

## 6. Node memory percentage (Node Exporter)

```promql
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

Shows the approximate percentage of node memory in use.

## 7. Pod count by namespace

```promql
count by (namespace) (kube_pod_info)
```

Counts pods represented by kube-state-metrics in each namespace.

## 8. Request rate (only if the application exports an HTTP request counter)

Example pattern; replace the metric name and labels with those your application actually exposes:

```promql
sum(rate(http_requests_total[5m]))
```

Not every Nginx setup exposes `http_requests_total` by default. Do not expect this query to return data unless an exporter or instrumented application provides that metric.
