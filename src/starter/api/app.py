"""Minimal API profile shell for overlay validation."""

from __future__ import annotations

import json

APP_NAME = "Py App Foundation API Profile"
HEALTH_ROUTE = "/health"
HEALTH_RESPONSE = "ok"


def build_contract_descriptor() -> dict[str, str]:
    """Build deterministic API contract metadata for smoke validation.

    Returns:
        Dictionary containing API profile contract values.
    """
    return {
        "app_name": APP_NAME,
        "health_route": HEALTH_ROUTE,
        "health_response": HEALTH_RESPONSE,
    }


def run() -> None:
    """Run API profile shell output."""
    print(json.dumps(build_contract_descriptor(), sort_keys=True))


if __name__ == "__main__":
    run()
