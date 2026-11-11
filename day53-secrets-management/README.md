# Day 53 — Secrets Management

## Objective

Learn to keep passwords, API keys, and other sensitive values out of application source code by reading them from environment variables.

## What this lab demonstrates

- Retrieve a secret with Python's `os.getenv()`
- Detect missing configuration without printing secret values
- Reject malformed environment-variable names
- Test configured and missing secrets
- Exclude real `.env` files and Python artifacts from Git

## Files

- `secrets_manager.py` — reads environment variables and reports only whether each value is configured
- `test_secrets_manager.py` — five unit tests using Python's standard library
- `.env.example` — placeholder names only; contains no real credentials
- `.gitignore` — excludes local secret files and Python artifacts

## Run locally

Python 3.10+ is recommended.

```bash
python3 -m unittest -v
```

Try the application with no secrets configured:

```bash
python3 secrets_manager.py
```

Set example values for the current shell and run again:

```bash
export DATABASE_PASSWORD='local-example-only'
export API_KEY='local-example-only'
python3 secrets_manager.py
```

The program reports whether values are configured. It never prints their contents.

## Security lessons

1. Never hardcode credentials in source code.
2. Never commit real secrets, `.env` files, private keys, or tokens.
3. Use environment variables for simple local demonstrations.
4. Use a dedicated secrets manager such as AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault for production workloads.
5. Apply least privilege and rotate credentials if they are exposed.

## Important limitation

This is a local educational demonstration, not a production-grade secrets manager. Environment variables can still be exposed through process inspection, debug output, crash reports, or misconfigured systems. Production systems should use a dedicated secrets-management service and carefully scoped access policies.

No real credentials or cloud account are required for this lab.
