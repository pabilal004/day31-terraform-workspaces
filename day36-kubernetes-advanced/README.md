# Day 36 — Kubernetes Advanced: Namespaces, Requests, Limits & ResourceQuota

## Goal
Practice isolating workloads with a Namespace, setting Pod CPU/memory requests and limits, and enforcing a ResourceQuota.

## Prerequisites
- A working Kubernetes cluster (this lab was tested with kind).
- `kubectl` configured for the cluster.

## Files
- `namespace.yaml` — creates the `day36-dev` namespace.
- `nginx-resources.yaml` — Pod with CPU/memory requests and limits.
- `resource-quota.yaml` — quota for Pods, CPU, and memory in `day36-dev`.
- `nginx-test.yaml` — second Pod used to fill the CPU quota.
- `nginx-over-quota.yaml` — intentional negative test; it should be rejected once the quota is full.

## Run the lab
Run these commands from this directory:

```bash
kubectl apply -f namespace.yaml
kubectl apply -f nginx-resources.yaml
kubectl get pods -n day36-dev
kubectl describe pod nginx-resources -n day36-dev

kubectl apply -f resource-quota.yaml
kubectl describe resourcequota day36-quota -n day36-dev

kubectl apply -f nginx-test.yaml
kubectl get pods -n day36-dev
kubectl describe resourcequota day36-quota -n day36-dev
```

When the two normal Pods are running, try the intentional quota test:

```bash
kubectl apply -f nginx-over-quota.yaml
```

**Expected result:** Kubernetes rejects this Pod with a `Forbidden` / `exceeded quota` message because the existing Pods already consume the namespace's CPU request and CPU limit quota. This rejection is the expected outcome of the test.

## Resource settings

| Resource | Request | Limit |
|---|---:|---:|
| `nginx-resources` CPU | 100m | 500m |
| `nginx-resources` memory | 64Mi | 128Mi |
| `nginx-test` CPU | 400m | 500m |
| `nginx-test` memory | 64Mi | 128Mi |

The quota permits 500m total CPU requests, 1 CPU total CPU limits, 256Mi total memory requests, 512Mi total memory limits, and 5 Pods. The two normal Pods use 500m CPU requests, 1 CPU in limits, 128Mi memory requests, and 256Mi memory limits.

## Useful checks

```bash
kubectl get namespaces
kubectl get pods -n day36-dev
kubectl get resourcequota -n day36-dev
kubectl describe resourcequota day36-quota -n day36-dev
kubectl describe pod nginx-resources -n day36-dev
```

- `kubectl get` gives a quick status/list.
- `kubectl describe` shows detailed information, configuration, and events.
- A request is used for scheduling; a limit caps the container's resource use.
- A ResourceQuota constrains aggregate resource consumption in a namespace.

## Cleanup

```bash
kubectl delete namespace day36-dev
```

Deleting the namespace removes the lab's Pods and quota.

## Lab note
During this practice, Pods showed a small number of restarts and an event mentioning `SandboxChanged`. That event indicates the Pod sandbox was recreated; it did not establish that ResourceQuota caused the restarts. The Pods were subsequently Running and Ready.
