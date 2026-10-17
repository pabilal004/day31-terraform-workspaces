# Day 43 — Kubernetes Namespaces

## Goal
Practice separating workloads into `dev`, `staging`, and `production` namespaces in one Kubernetes cluster.

## Namespaces
Create the three namespaces (skip any that already exist):

```bash
kubectl create namespace dev
kubectl create namespace staging
kubectl create namespace production
```

## Deploy Nginx to each environment

Apply the manifests:

```bash
kubectl apply -f nginx-dev.yaml
kubectl apply -f nginx-staging.yaml
kubectl apply -f nginx-production.yaml
```

| Namespace | Deployment | Desired replicas |
|---|---|---:|
| `dev` | `nginx-dev` | 2 |
| `staging` | `nginx-staging` | 2 |
| `production` | `nginx-production` | 3 |

All manifests use the `nginx:1.28` image. Replica counts are for this learning lab, not production sizing guidance.

## Verify

```bash
kubectl get namespaces
kubectl get deployments -A
kubectl get pods -n dev
kubectl get pods -n staging
kubectl get pods -n production
kubectl get pods -A
```

Expected: each Deployment becomes Ready with its desired replica count, and its pods appear only in the namespace specified in its manifest.

## Useful namespace commands

```bash
kubectl get pods -n dev
kubectl get deployments -n staging
kubectl describe deployment nginx-production -n production
kubectl config set-context --current --namespace=dev
kubectl config set-context --current --namespace=default
```

Changing the current context namespace only changes the default namespace for future commands; it does not move existing resources.

## Key learnings
- Namespaces logically organize resources within one cluster.
- Use `-n <namespace>` to target a specific environment.
- Use `-A` to list resources across all namespaces.
- Namespace separation alone is not a complete security boundary. Use appropriate RBAC, NetworkPolicies, and other controls where required.
- Existing namespaces such as `day36-dev` and `day40-quota-demo` are separate practice resources and are not deleted by this lab.
