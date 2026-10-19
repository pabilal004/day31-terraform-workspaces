# Day 45 — Python CI Pipeline

A beginner-friendly Continuous Integration project that tests a Python function with pytest and runs the tests automatically using GitHub Actions.

## Application

`app.py` defines `calculate_total(price, quantity)`. It multiplies price by quantity and raises `ValueError` when either input is negative.

## Run locally

Create and activate a virtual environment, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

The tests cover a normal calculation, negative price, and negative quantity.

## CI

The repository's GitHub Actions workflow installs the dependencies and runs pytest on pushes and pull requests that change this project. The workflow also retains the existing Kubernetes manifest YAML validation.

## Scope

These tests check the behavior covered by the three test cases; passing tests do not prove that every possible input or behavior is bug-free.
