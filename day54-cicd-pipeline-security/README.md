# Day 54 — CI/CD Pipeline Security

A practical, cost-free DevSecOps lab that adds automated security gates to a GitHub Actions pipeline. It uses a small Python application and a hardened Docker image; no cloud account or paid service is required.

## What the pipeline checks

| Stage | Tool | Purpose |
|---|---|---|
| Unit tests | Python unittest | Confirms expected application behavior |
| SAST | Bandit | Finds common security issues in Python source |
| Dependency audit | pip-audit | Checks Python dependencies against known advisories |
| Secret scanning | Gitleaks | Detects accidentally committed credentials |
| Filesystem and IaC scanning | Trivy | Scans files, dependencies, secrets and configuration |
| Container scanning | Trivy | Checks the built image for known vulnerabilities |

The workflow is at `.github/workflows/day54-security-pipeline.yml (at the repository root)`. It runs on pushes and pull requests that change this project, and can also be started manually from the GitHub Actions tab.

## Security design choices

- No real credentials, API keys or passwords are stored in this repository.
- The demo application uses only the Python standard library.
- The container runs as a non-root user.
- The workflow requests read-only repository contents permission.
- High and critical findings fail the relevant security job instead of silently allowing the pipeline to pass.

## Run locally

Requirements: Python 3.12+ and Docker.

Run the tests:

```bash
python -m unittest discover -v
```

Run Bandit and the dependency audit:

```bash
python -m pip install --upgrade bandit pip-audit
bandit -q -r app.py -ll
pip-audit -r requirements.txt
```

Build and run the container:

```bash
docker build -t day54-secure-demo .
docker run --rm -p 8000:8000 day54-secure-demo
```

In another terminal, check the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

Scan the local image (install Trivy first):

```bash
trivy image --severity HIGH,CRITICAL --ignore-unfixed day54-secure-demo
```

## How to review the pipeline

1. Open the repository's **Actions** tab.
2. Select **Secure CI/CD Pipeline**.
3. Open the latest run and inspect each job.
4. A failed security gate should be investigated and fixed before merging or deploying.

A clean run is not a guarantee that software is vulnerability-free. Scanners only detect issues covered by their rules and vulnerability databases; review findings and keep tools and base images updated.

## Learning outcomes

After completing this lab, you should be able to explain the difference between SAST and DAST, identify where dependency and secret scanning fit, scan a container image, and use CI/CD security gates to prevent risky changes from progressing.
