# Day 51 — DevSecOps: Secrets Management

## Objective
Practice identifying hardcoded credentials, reading configuration from environment variables, and preventing local secret files and generated Python files from being committed.

## Files
- `app.py` — sample Python application that reads `DATABASE_PASSWORD` from an environment.
- `.gitignore` — excludes Python cache files and local `.env` files.

## Run
```bash
export DATABASE_PASSWORD="your-local-test-value"
python3 -c "from app import connect_database; connect_database()"
```

Unset the variable to test the missing-configuration path:
```bash
unset DATABASE_PASSWORD
python3 -c "from app import connect_database; connect_database()"
```

## Security notes
- Never hardcode real passwords, API keys, or tokens in source code.
- Do not commit `.env` files.
- Review staged changes with `git diff --cached` before committing.
- Environment variables avoid hardcoding but are not a complete secrets-management system; protect their storage and access.

The password values used during this exercise are test values only and are not included in this repository.
