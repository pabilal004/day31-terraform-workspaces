# Day 55–60: Production-Style DevOps Capstone

A small Python HTTP service delivered as a hardened container and Kubernetes workload. This capstone demonstrates application testing, containerization, Kubernetes deployment, Terraform namespace provisioning, CI security checks, and Prometheus alert rules.

## Architecture

GitHub → GitHub Actions (tests, Bandit, pip-audit, image build, manifest validation) → Docker image → Kubernetes Deployment/Service → Prometheus metrics and alert rules.

## Application endpoints

| Path | Purpose |
|---|---|
| `/` | Application metadata and environment |
| `/health` | Liveness check |
| `/ready` | Readiness check |
| `/metrics` | Prometheus metrics |

## Run locally

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements-dev.txt
python -m pytest -v app/test_app.py
```

Run with Docker:

```bash
docker build -t production-capstone:local .
docker run --rm -p 8000:8000 -e APP_ENV=local production-capstone:local
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

Or use Docker Compose:

```bash
docker compose up --build
```

## Deploy to the existing Kind cluster

Build the image, load it into Kind, and apply manifests:

```bash
docker build -t production-capstone:local .
kind load docker-image production-capstone:local --name devops-cluster
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
kubectl rollout status deployment/production-capstone -n production-capstone
kubectl get pods,svc,hpa -n production-capstone
```

Test the service using port-forward:

```bash
kubectl port-forward -n production-capstone svc/production-capstone 8080:80
```

In another terminal:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/ready
curl http://localhost:8080/metrics
```

Apply HPA only after confirming the cluster Metrics API is healthy:

```bash
kubectl apply -f k8s/hpa.yaml
kubectl get hpa -n production-capstone
kubectl top pods -n production-capstone
```

## Terraform

Terraform provisions the dedicated namespace only; Kubernetes workload resources remain declarative YAML so the responsibilities stay clear.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Then return to the project root and apply the deployment and service manifests. The provider uses the existing `kind-devops-cluster` kube context.

## Prometheus alert rules

The example rule file assumes the Prometheus Operator is installed and its rule selector accepts the `release: monitoring` label:

```bash
kubectl apply -f monitoring/prometheus-rules.yaml
kubectl get prometheusrules -n monitoring
```

Confirm the Prometheus Operator's rule selectors before applying. Alert expressions depend on the app being scraped; configure a ServiceMonitor or scrape job for the service if your Prometheus installation does not discover it automatically.

## Security controls

- Non-root container user
- Read-only root filesystem in Kubernetes
- Dropped Linux capabilities and no privilege escalation
- RuntimeDefault seccomp profile
- Disabled automatic service-account token mounting
- CPU/memory requests and limits
- Liveness and readiness probes
- Bandit static analysis and pip-audit dependency scanning in CI

## Important production notes

This is a learning capstone, not a fully production-certified service. Before real production use, add TLS/Ingress, external secret management, persistent centralized logs, backup/recovery testing, image signing, SBOM generation, policy enforcement, and a managed highly available Kubernetes control plane. The sample Prometheus rules require working service discovery and alert routing.

## Cleanup

```bash
kubectl delete namespace production-capstone
```

If Terraform created the namespace, run `terraform destroy` from the terraform directory instead. Do not run both cleanup methods at the same time.
