# Day 34 — Kubernetes ConfigMaps & Secrets

## What was practiced

- ConfigMap for non-sensitive application configuration
- Secret for sensitive values
- Using `envFrom` with ConfigMap and Secret
- Verifying environment variables inside a Pod
- Inspecting Secret data returned by the Kubernetes API
- Cleaning up Kubernetes resources after the lab

## Resources

### ConfigMap

- Name: `day34-config`
- `APP_NAME=devops-app`
- `APP_ENV=development`
- `LOG_LEVEL=info`

### Secret

- Name: `day34-secret`
- Keys: `DB_USERNAME`, `DB_PASSWORD`

The actual lab Secret was intentionally **not committed** to GitHub because it contained test credentials. Use `secret-example.yaml` and replace the placeholder values locally.

> Kubernetes Secret `data` values are Base64-encoded representations, not encryption by themselves. Production environments should use appropriate RBAC, encryption-at-rest, and secure secret-management practices.

## Pod

The `day34-app` Pod used:

```yaml
envFrom:
  - configMapRef:
      name: day34-config
  - secretRef:
      name: day34-secret
```

## Verification

The Pod reached `1/1 Running` and successfully received:

- ConfigMap values as environment variables
- Secret values as environment variables

The lab resources were then deleted after verification.
