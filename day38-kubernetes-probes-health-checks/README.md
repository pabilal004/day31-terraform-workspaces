# Day 38 — Kubernetes Probes & Health Checks

## Goal
Configure Kubernetes startup, liveness, and readiness probes for an Nginx Pod.

## Probe notes
- **Startup probe:** checks whether the application has finished starting. While it has not succeeded, Kubernetes does not run liveness or readiness probes for that container.
- **Liveness probe:** checks whether the application is still functioning. Repeated failures can cause Kubernetes to restart the container.
- **Readiness probe:** checks whether the application can receive traffic. When it fails, the Pod is removed from the Service's ready endpoints.

## Probe methods
- `httpGet`: makes an HTTP request.
- `tcpSocket`: checks whether a TCP port is open.
- `exec`: runs a command inside the container.

## Files
- `nginx-probes.yaml`: Pod manifest with all three HTTP probes on port 80.

## Run the lab
```bash
kubectl apply -f nginx-probes.yaml
kubectl get pod nginx-probes
kubectl describe pod nginx-probes
kubectl exec nginx-probes -- curl -I http://localhost:80/
```

Expected checks:
- Pod status is `Running`.
- Pod readiness is `1/1` after startup.
- `kubectl describe pod nginx-probes` shows Startup, Liveness, and Readiness probe settings.
- HTTP check returns `HTTP/1.1 200 OK`.

## Key settings
- `periodSeconds`: approximate interval between probe checks.
- `failureThreshold`: consecutive failures before the probe is considered failed.
- `initialDelaySeconds`: delay before the first probe check, if configured.
- `timeoutSeconds`: time allowed for a single probe, if configured.

## Cleanup
```bash
kubectl delete -f nginx-probes.yaml
```

This lab uses the public `nginx:latest` image and contains no credentials.
