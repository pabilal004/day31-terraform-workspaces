# Day 49 — Prometheus Troubleshooting Queries

Use these in Prometheus or a Grafana panel with the Prometheus data source selected.

## 1. Scrape status for each target

```promql
up
```

- `1`: the latest scrape succeeded.
- `0`: the latest scrape failed.

## 2. Count failed-scrape series

```promql
count(up == 0)
```

This counts time series whose current value is zero. Treat it as a target count only if there is one matching series per target in the selected query result.

## 3. Show failed targets with identifying labels

```promql
up == 0
```

Use the result labels (often including `job` and `instance`) to identify which target needs investigation.

## 4. Show target scrape status for a selected job

Replace `<job-name>` with the actual job label value:

```promql
up{job="<job-name>"}
```

## 5. Basic CPU and memory metrics (if the relevant exporters are installed)

CPU rate example:

```promql
rate(process_cpu_seconds_total[5m])
```

Process memory example:

```promql
process_resident_memory_bytes
```

These process metrics are available only when the scraped application exposes them. They are not universal Kubernetes metrics.

## Troubleshooting an empty result

1. Set a time range that includes recent data.
2. Confirm the Prometheus data source is selected and working.
3. Check whether the metric exists in Prometheus.
4. Check labels and the selected job/instance.
5. Inspect the target status and scrape error details.
6. Verify that the relevant exporter or metrics endpoint is installed and reachable.

## Interpretation caution

A DOWN scrape indicates a monitoring collection failure. Possible causes include a stopped process, a network problem, an incorrect address or port, access restrictions, or an endpoint/configuration issue. Confirm the root cause from evidence before changing the workload.
