"""A small, local IAM-style policy simulator for learning.

This is an educational example, not an implementation of AWS IAM.
"""
from fnmatch import fnmatchcase
from typing import Any


POLICIES: dict[str, list[dict[str, Any]]] = {
    "developer": [
        {
            "Effect": "Allow",
            "Action": "read_logs",
            "Resource": "logs",
        }
    ],
    "admin": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*",
        },
        {
            "Effect": "Deny",
            "Action": "delete_resource",
            "Resource": "database",
        },
    ],
    "tester": [
        {
            "Effect": "Allow",
            "Action": "read_logs",
            "Resource": "logs",
        }
    ],
}


def _matches(patterns: str | list[str], value: str) -> bool:
    """Match a value against one pattern or a list of wildcard patterns."""
    if isinstance(patterns, str):
        patterns = [patterns]
    return any(fnmatchcase(value, pattern) for pattern in patterns)


def check_permission(
    user: str,
    action: str,
    resource: str,
    policies: dict[str, list[dict[str, Any]]],
) -> str:
    """Return ALLOW only when an Allow matches and no Deny matches.

    A matching explicit Deny always overrides matching Allow statements.
    If no Allow statement matches, the result is an implicit DENY.
    """
    statements = policies.get(user, [])
    allowed = False

    for statement in statements:
        action_matches = _matches(statement["Action"], action)
        resource_matches = _matches(statement["Resource"], resource)

        if action_matches and resource_matches:
            if statement["Effect"] == "Deny":
                return "DENY"
            if statement["Effect"] == "Allow":
                allowed = True

    return "ALLOW" if allowed else "DENY"


def main() -> None:
    requests = [
        ("developer", "read_logs", "logs"),
        ("developer", "delete_resource", "database"),
        ("admin", "delete_resource", "database"),
        ("admin", "create_resource", "compute"),
        ("tester", "create_resource", "compute"),
    ]

    for user, action, resource in requests:
        decision = check_permission(user, action, resource, POLICIES)
        print(f"{user} -> {action} on {resource}: {decision}")


if __name__ == "__main__":
    main()
