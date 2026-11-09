# Day 52 — Local IAM Policy Simulator

A beginner-friendly Python project that demonstrates identity permissions and the **principle of least privilege** without an AWS account, cloud resources, or paid services.

> This is an educational simulator. It is not AWS IAM and must not be used to secure real systems.

## What it demonstrates

- **Identity:** a user such as developer, admin, or tester.
- **Action:** an operation such as `read_logs` or `delete_resource`.
- **Resource:** the target, such as `logs`, `database`, or `compute`.
- **Allow:** a matching statement grants permission.
- **Implicit Deny:** if no Allow statement matches, access is denied.
- **Explicit Deny:** a matching Deny always overrides an Allow.
- **Wildcards:** `*` matches any action/resource; patterns such as `read_*` are also supported.

## Requirements

- Python 3.10 or newer
- No third-party packages
- No AWS account or credentials

## Run the simulator

From this directory:

```bash
python3 iam_simulator.py
```

Expected output:

```text
developer -> read_logs on logs: ALLOW
developer -> delete_resource on database: DENY
admin -> delete_resource on database: DENY
admin -> create_resource on compute: ALLOW
tester -> create_resource on compute: DENY
```

The admin has a broad Allow statement, but the explicit Deny blocks deleting the database. This demonstrates why explicit Deny takes precedence.

## Run the tests

```bash
python3 -m unittest -v
```

The tests cover allowed access, implicit denial, explicit-Deny precedence, wildcard matching, and an unknown user.

## Policy example

Each user's policy is a list of statements in `POLICIES` inside `iam_simulator.py`:

```python
{
    "Effect": "Allow",
    "Action": "read_logs",
    "Resource": "logs"
}
```

An action or resource can also be a list of patterns. For example, `"Action": ["read_*", "list_*"]`.

## Project structure

```text
day52-iam-lab/
├── .gitignore
├── README.md
├── iam_simulator.py
└── test_iam_simulator.py
```

## Security lessons

1. Give each identity only the permissions it needs.
2. Do not grant administrator access by default.
3. Treat explicit Deny as an overriding restriction.
4. Review permissions when roles or responsibilities change.
5. Never place real passwords, API keys, or cloud credentials in source code.

## Limitations

This project uses a small, simplified policy model. It does not implement AWS policy evaluation, IAM users/roles, trust policies, conditions, resource-based policies, policy variables, or cloud authentication. Its purpose is to practise the core permission concepts locally.
