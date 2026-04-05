"""Minimal worker profile shell for overlay validation."""

from __future__ import annotations

import json

APP_NAME = "Py App Foundation Worker Profile"
JOB_NAME = "baseline-job"
JOB_STATUS = "processed"


def build_contract_descriptor() -> dict[str, str]:
    """Build deterministic worker contract metadata for smoke validation.

    Returns:
        Dictionary containing worker profile contract values.
    """
    return {
        "app_name": APP_NAME,
        "job_name": JOB_NAME,
        "job_status": JOB_STATUS,
    }


def run() -> None:
    """Run worker profile shell output."""
    print(json.dumps(build_contract_descriptor(), sort_keys=True))


if __name__ == "__main__":
    run()
