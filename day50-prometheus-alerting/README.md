# Day 50 – Prometheus Alerting and Alertmanager

## Overview

This project demonstrates how to define Prometheus alert rules and configure Alertmanager to group, inhibit, silence, and route alerts by severity in a Kubernetes cluster.

The lab uses the Prometheus Operator stack installed with Helm in the `monitoring` namespace.

## Lab environment

- Kubernetes: Kind cluster
- Namespace: `monitoring`
- Helm release: `monitoring`
- Chart: `prometheus-community/kube-prometheus-stack`
- Chart version: `92.11.0`
- Prometheus rule resource: `PrometheusRule`

## Project files

| File | Purpose |
|---|---|
| `prometheus-rule.yaml` | Defines the `PrometheusTargetDown` alert |
| `values-alertmanager.yaml` | Enables Alertmanager while retaining the lab's Grafana and Prometheus resource settings |
| `values-routing.yaml` | Configures default, critical, and warning routes plus inhibition rules |

Generated Helm output and local backup values are intentionally not included.

## 1. Prometheus alert rule

The `PrometheusRule` resource defines:

- Alert: `PrometheusTargetDown`
- Expression: `up == 0`
- Pending duration: `2m`
- Severity: `warning`
- Evaluation interval: `30s`

Apply it:

```bash
kubectl apply -f prometheus-rule.yaml
```

The rule uses the label `release: monitoring` so it is selected by this Helm release's Prometheus configuration.

## 2. Enable Alertmanager

The `values-alertmanager.yaml` file enables Alertmanager and preserves the lab's existing Grafana and Prometheus resource settings.

Apply the values:

```bash
helm upgrade monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --version 92.11.0 \
  -f values-alertmanager.yaml \
  --wait --timeout 10m
```

## 3. Configure severity-based routing

The `values-routing.yaml` file configures these routes:

| Matching severity | Receiver |
|---|---|
| `critical` | `critical-receiver` |
| `warning` | `warning-receiver` |
| No matching child route | `default-receiver` |

It also configures:

- Grouping by `alertname` and `namespace`
- Group wait: `30s`
- Group interval: `5m`
- Repeat interval: `12h`
- The four inhibition rules used by the lab configuration

Apply the routing configuration:

```bash
helm upgrade monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --version 92.11.0 \
  -f values-routing.yaml \
  --wait --timeout 10m
```

### Important: notification receivers

The three receivers are empty placeholders. This lab verifies route selection and configuration loading, but it does not deliver email, Slack, PagerDuty, or webhook notifications. Add a properly secured receiver integration before using this configuration for real incident notifications.

## 4. Verify the deployment

Check the pods:

```bash
kubectl get pods -n monitoring
```

Inspect the active Alertmanager configuration stored in the Kubernetes Secret:

```bash
kubectl get secret -n monitoring alertmanager-monitoring-kube-prometheus-alertmanager \
  -o jsonpath='{.data.alertmanager\\.yaml}' | base64 -d
```

If port-forwarding is active on local port 9093, inspect Alertmanager's status API:

```bash
curl -s http://localhost:9093/api/v2/status
```

The status response includes the loaded configuration and Alertmanager version.

## 5. Silence practice

A silence was created for `PrometheusTargetDown` for five minutes using the Alertmanager API.

A silence suppresses notifications for matching alerts during its validity period. It does **not** stop Prometheus from evaluating the rule or resolve the underlying target condition.

## Observations and troubleshooting

During this lab, Prometheus reported several unavailable Kubernetes control-plane scrape targets. An `up == 0` result means Prometheus could not successfully scrape that target; it does not by itself prove that the underlying Kubernetes component is unhealthy.

An initial attempt to create a silence through the UI returned a validity error. Creating it through the API with explicit UTC start and end timestamps succeeded.

Alertmanager reported clustering as disabled with no peers. That is expected for this single-instance lab and is not, by itself, a failure.

## Cleanup

Remove the custom alert rule when it is no longer needed:

```bash
kubectl delete -f prometheus-rule.yaml
```

Do not uninstall the monitoring Helm release unless you intend to remove the whole monitoring stack.

## Skills practised

- PrometheusRule resources and PromQL alert expressions
- Alert pending duration and severity labels
- Alertmanager enablement with Helm
- Alert grouping and severity-based routing
- Alert inhibition and silences
- Kubernetes Secret inspection
- Helm upgrade and deployment verification
