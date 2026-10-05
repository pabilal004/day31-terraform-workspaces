# Day 32 — Kubernetes NGINX Deployment

Hands-on Kubernetes project completed with a local kind cluster.

## What was practiced

- Kubernetes cluster and kubectl
- Pods and labels
- ClusterIP Service
- Service selectors and EndpointSlice
- Deployment and ReplicaSet
- Scaling from 2 to 3 replicas
- Self-healing after Pod deletion
- Rolling update from nginx:latest to nginx:1.27
- Rollback to the previous Deployment revision
- Service routing to multiple Pods

## Architecture

Deployment → ReplicaSet → 3 Pods → nginx-service

## Key commands practiced

```bash
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
kubectl get pods,deployments,services
kubectl get endpointslice
kubectl scale deployment nginx-deployment --replicas=3
kubectl rollout status deployment/nginx-deployment
kubectl rollout undo deployment/nginx-deployment
```

## Verification

The final cluster state had:

- nginx-deployment: 3/3 Ready
- 3 Deployment-managed NGINX Pods: Running
- nginx-service: ClusterIP on port 80

The project was tested by sending a request through the Service and receiving the NGINX welcome page.
