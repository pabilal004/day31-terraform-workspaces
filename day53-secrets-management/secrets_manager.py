"""A small, local secrets-management demo using environment variables.

This is an educational example, not a replacement for a production secrets manager.
Never print, commit, or log real secret values.
"""
import os
from typing import Optional


def get_secret(name: str) -> Optional[str]:
    """Return a configured secret, or None when it is missing."""
    if not name or not name.replace("_", "").isalnum():
        raise ValueError("Secret name must contain only letters, numbers, and underscores.")
    value = os.getenv(name)
    if value is None or value == "":
        return None
    return value


def secret_is_configured(name: str) -> bool:
    """Check whether a secret exists without revealing its value."""
    return get_secret(name) is not None


def main() -> None:
    required_secrets = ("DATABASE_PASSWORD", "API_KEY")
    for name in required_secrets:
        if secret_is_configured(name):
            print(f"{name}: configured")
        else:
            print(f"{name}: NOT configured")


if __name__ == "__main__":
    main()
