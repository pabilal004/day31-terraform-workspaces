# Day 40: Kubernetes ResourceQuota and LimitRange

## Objective
Learn how to control namespace resource consumption and apply default resource requests and limits.

## Concepts
- ResourceQuota controls total resources in a namespace.
- LimitRange sets default container requests and limits.
- Requests help Kubernetes schedule Pods.
- Limits cap container CPU and memory usage.

## Files
- resource-quota.yaml: Namespace resource quota.
- limit-range.yaml: Default container resources.
- test-pod.yaml: NGINX Pod without explicit resources.

## ResourceQuota
- CPU requests: 1 core
- Memory requests: 1Gi
- CPU limits: 2 cores
- Memory limits: 2Gi
- Maximum Pods: 5

## LimitRange Defaults
- CPU request: 100m
- Memory request: 64Mi
- CPU limit: 500m
- Memory limit: 128Mi

## Validation
- Namespace: day40-quota-demo
- Pod status: Running
- QoS class: Burstable
- ResourceQuota usage verified successfully.

## Commands Practiced
- kubectl create namespace day40-quota-demo
- kubectl apply -f resource-quota.yaml
- kubectl apply -f limit-range.yaml
- kubectl apply -f test-pod.yaml
- kubectl describe pod quota-test-pod -n day40-quota-demo
- kubectl describe resourcequota day40-resource-quota -n day40-quota-demo
- kubectl describe limitrange day40-limit-range -n day40-quota-demo
