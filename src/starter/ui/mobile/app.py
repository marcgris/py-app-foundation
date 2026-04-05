"""Minimal mobile profile shell for UI overlay validation."""

from __future__ import annotations

APP_NAME = "Py App Foundation Mobile Profile"
SMOKE_MARKER_TEXT = "starter-ui-mobile-ready"


def build_profile_metadata() -> dict[str, str]:
    """Build deterministic metadata for mobile profile smoke validation.

    Returns:
        Dictionary containing app name and marker text values.
    """
    return {
        "app_name": APP_NAME,
        "marker": SMOKE_MARKER_TEXT,
    }


def run() -> None:
    """Run the mobile profile shell output."""
    metadata = build_profile_metadata()
    print(f"{metadata['app_name']} | {metadata['marker']}")


if __name__ == "__main__":
    run()
