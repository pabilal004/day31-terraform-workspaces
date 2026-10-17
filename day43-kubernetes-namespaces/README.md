# Day 43 — Kubernetes Namespaces

## Objective
Organize Kubernetes resources by environment using namespaces.

## Lab environment
- Cluster: kind `devops-cluster`
- Kubernetes context: `kind-devops-cluster`
- Namespaces created: `dev`, `staging`, `production`
- Deployment: `nginx-dev`
- Namespace: `dev`
- Image: `nginx:1.28`
- Desired replicas: 2

## Apply
```bash
kubectl create namespace dev
kubectl create namespace staging
kubectl create namespace production
kubectl apply -f nginx-dev.yaml
```

If the namespaces already exist, the create commands may report that they already exist; this is expected.

## Verify
```bash
kubectl get namespaces
kubectl get deployments -n dev
kubectl get pods -n dev
kubectl get pods -n staging
kubectl get pods -n production
```

Expected: `nginx-dev` is 2/2 ready in `dev`; this exercise creates no Pods in `staging` or `production`.

## Useful commands
```bash
kubectl get pods -A
kubectl describe namespace dev
kubectl config view --minify
kubectl config set-context --current --namespace=dev
kubectl config set-context --current --namespace=default
```

## Key learnings
- Namespaces organize namespaced resources within a cluster.
- Use `-n <namespace>` to target a namespace for a command.
- Namespaces alone are not a complete security boundary; RBAC, network policies, and other controls may be needed.
- Changing the current context namespace does not move existing resources.

## Cleanup (optional)
Only run this if you intend to remove this lab workload:
```bash
kubectl delete deployment nginx-dev -n dev
``
