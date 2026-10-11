# Day 37 — Kubernetes ConfigMaps and Secrets

## Goal
Practice storing non-sensitive configuration in a ConfigMap and sensitive values in a Kubernetes Secret, then expose each to a Pod as environment variables.

## Files
- `configmap.yaml` — stores `APP_ENV` and `APP_COLOR`.
- `secret.yaml` — stores a **fake, training-only** `DB_PASSWORD` using `stringData`.
- `configmap-pod.yaml` — imports all ConfigMap entries with `envFrom` and `configMapRef`.
- `secret-pod.yaml` — imports one Secret key with `secretKeyRef` and checks that it exists without printing its value.

## Run the lab
Apply the objects:

```bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f configmap-pod.yaml
kubectl apply -f secret-pod.yaml
```

Verify resources and results:

```bash
kubectl get configmaps app-config
kubectl describe configmap app-config
kubectl get secret app-secret
kubectl describe secret app-secret
kubectl get pods
kubectl logs configmap-test
kubectl logs secret-test
```

Expected ConfigMap Pod logs include:

```text
APP_COLOR=blue
APP_ENV=development
```

Expected Secret Pod log:

```text
Secret loaded successfully
```

The Secret Pod intentionally does not print the password.

## Security notes
- ConfigMaps are for non-sensitive configuration.
- Kubernetes Secrets are intended for sensitive values, but Base64 encoding is not encryption.
- Restrict Secret access with least-privilege RBAC and configure encryption at rest for production clusters.
- Never commit real passwords, tokens, or API keys to GitHub. The value in this training example is fake and must not be reused.

## Cleanup
Run from this directory:

```bash
kubectl delete -f secret-pod.yaml --ignore-not-found
kubectl delete -f configmap-pod.yaml --ignore-not-found
kubectl delete -f secret.yaml --ignore-not-found
kubectl delete -f configmap.yaml --ignore-not-found
```
