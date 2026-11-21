# Day 57 — Production Kubernetes Deployment

## Objective
Deploy the production-capstone container as a Kubernetes workload and verify availability, health checks, networking, and scaling configuration.

## Architecture
- **Deployment:** maintains two application replicas.
- **Pod security:** non-root UID/GID 10001, RuntimeDefault seccomp, no privilege escalation, read-only root filesystem, and all Linux capabilities dropped.
- **Resources:** CPU/memory requests and limits are defined.
- **Probes:** readiness uses `/ready`; liveness uses `/health`.
- **Service:** ClusterIP exposes port 80 and forwards to the named container port (8000).
- **HPA:** targets 70% average CPU utilization, with 2–5 replicas. It requires a working Metrics API.

## Deploy to the existing Kind cluster

Run these commands from the `day55-production-capstone` directory. The commands below are instructions for the local operator; the GitHub workflow validates the manifests but does not access your workstation's Kind cluster.

### 1. Confirm cluster access

```bash
kubectl config current-context
kubectl get nodes
```

The expected context is `kind-devops-cluster` and the node should be `Ready`.

### 2. Build and load the image

```bash
docker build -t production-capstone:local .
kind load docker-image production-capstone:local --name devops-cluster
```

The image tag must match `spec.template.spec.containers[].image` in `k8s/deployment.yaml`. The manifest uses `imagePullPolicy: IfNotPresent`, so Kind can use the locally loaded image.

### 3. Create the namespace

Choose **one** namespace owner:
- Terraform: run `terraform -chdir=terraform init` then `terraform -chdir=terraform apply`.
- Kubernetes YAML: run `kubectl apply -f k8s/namespace.yaml`.

Do not use both methods against the same namespace unless you import the existing namespace into Terraform state.

### 4. Apply the workload and verify rollout

```bash
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
kubectl rollout status deployment/production-capstone -n production-capstone
kubectl get deployment,pods,service -n production-capstone
kubectl get endpoints production-capstone -n production-capstone
```

Expected steady state: Deployment shows 2/2 available replicas, two Pods are Ready, and the Service has Pod endpoints.

### 5. Test the application

In terminal 1:

```bash
kubectl port-forward -n production-capstone svc/production-capstone 8080:80
```

In terminal 2:

```bash
curl -fsS http://localhost:8080/
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8080/ready
curl -fsS http://localhost:8080/metrics
```

The health and readiness endpoints should return HTTP 200. The metrics endpoint should include Prometheus metrics such as `http_requests_total`.

### 6. Verify scaling configuration

Only after the cluster Metrics API is healthy:

```bash
kubectl top pods -n production-capstone
kubectl apply -f k8s/hpa.yaml
kubectl get hpa -n production-capstone
```

The HPA should report CPU utilization once metrics are available. A temporary `<unknown>` value indicates metrics are not yet available; check `kubectl top pods -n production-capstone` and the metrics-server before troubleshooting the HPA itself.

## Troubleshooting

| Symptom | First checks |
|---|---|
| `ImagePullBackOff` | Confirm the image tag and run `kind load docker-image production-capstone:local --name devops-cluster` |
| `CrashLoopBackOff` | `kubectl logs` and `kubectl describe pod` |
| Readiness probe failing | Check app logs and `/ready` on port 8000 |
| Service has no endpoints | Check Pod labels, readiness, and Service selector |
| HPA shows unknown metrics | Check Metrics API and `kubectl top pods` |

Useful commands:

```bash
kubectl get pods -n production-capstone
kubectl describe deployment production-capstone -n production-capstone
kubectl logs deployment/production-capstone -n production-capstone
kubectl get events -n production-capstone --sort-by=.metadata.creationTimestamp
```

## Automated manifest validation

The repository workflow `.github/workflows/day57-kubernetes-validation.yml` runs Kubeconform against the namespace, Deployment, Service, and HPA manifests whenever these files change or the workflow is manually started.

## Completion criteria

- [ ] Kind context and node are healthy.
- [ ] Image built and loaded into Kind.
- [ ] Namespace created using exactly one management method.
- [ ] Deployment reaches 2/2 available replicas.
- [ ] Service has endpoints.
- [ ] `/`, `/health`, `/ready`, and `/metrics` respond successfully.
- [ ] HPA metrics are visible (if Metrics Server is enabled).
- [ ] GitHub Actions Kubernetes manifest validation passes.

**Scope note:** CI validation proves that the YAML conforms to Kubernetes schemas. It does not prove a live deployment. The live cluster checks above must be run against the local Kind cluster.
