# Day 42: Kubernetes Deployments and ReplicaSets

## Overview
Hands-on Kubernetes practice using a local kind cluster.

## What I Practiced
- Created a Kubernetes Deployment from YAML.
- Verified how a Deployment manages ReplicaSets.
- Scaled the Deployment to five replicas.
- Tested Pod self-healing by deleting a managed Pod and observing replacement.
- Performed a rolling update from `nginx:1.28` to `nginx:1.29`.
- Rolled back to `nginx:1.28`.
- Verified rollout status and Pod readiness.

## Technologies
- Kubernetes
- kubectl
- Docker
- kind
- YAML

## Files
- `deployment.yaml`: Kubernetes Deployment manifest.

## Useful Commands
```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get replicasets
kubectl get pods -l app=nginx
kubectl scale deployment nginx-deployment --replicas=5
kubectl rollout status deployment/nginx-deployment
kubectl rollout history deployment/nginx-deployment
kubectl set image deployment/nginx-deployment nginx=nginx:1.29
kubectl rollout undo deployment/nginx-deployment
```

## Final Verification
- Deployment: `nginx-deployment`
- Desired replicas: 5
- Ready replicas: 5
- Image after rollback: `nginx:1.28`
- Rollout status: successfully rolled out

## Learning Outcome
Learned how Kubernetes Deployments manage ReplicaSets, maintain the desired number of Pods, perform rolling updates, replace deleted Pods, and support rollbacks.

> This project folder is stored in the existing GitHub repository under `day42-kubernetes-deployments/` to preserve the repository and its existing Terraform work.
