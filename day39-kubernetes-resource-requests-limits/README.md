# Day 39: Kubernetes Resource Requests & Limits

## Objective
Learn how to configure CPU and memory requests and limits
for a Kubernetes container.

## Concepts
- Requests define resources used for Pod scheduling.
- CPU requests and limits use units such as 100m and 500m.
- Memory requests and limits use units such as 64Mi and 128Mi.
- CPU usage above the limit is generally throttled.
- Exceeding the memory limit can cause a container to be OOMKilled.
- Burstable QoS applies when requests and limits do not meet
  the Guaranteed QoS requirements.

## Files
- resource-limits-pod.yaml: Pod configuration with resource settings.

## Validation
- Pod status: Running
- CPU request: 100m
- CPU limit: 500m
- Memory request: 64Mi
- Memory limit: 128Mi
- HTTP test: 200 OK

## Commands Practiced
- kubectl apply -f resource-limits-pod.yaml
- kubectl get pod resource-demo
- kubectl describe pod resource-demo
- kubectl exec resource-demo -- curl -I http://localhost:80/
