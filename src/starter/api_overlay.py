"""Utilities for API overlay skeleton discovery and validation."""

from __future__ import annotations

from pathlib import Path

API_OVERLAY_DIRNAME = "api"
API_ENTRY_FILENAME = "app.py"
API_README_FILENAME = "README.md"
API_APP_NAME = "Py App Foundation API Profile"
API_HEALTH_ROUTE = "/health"
API_HEALTH_RESPONSE = "ok"


def get_api_overlay_dir() -> Path:
    """Return the absolute path to the API overlay directory.

    Returns:
        Absolute path to the API overlay folder.
    """
    return Path(__file__).resolve().parent / API_OVERLAY_DIRNAME


def get_api_entry_file() -> Path:
    """Return the absolute path to the API overlay entry script.

    Returns:
        Absolute path to the API entry script.
    """
    return get_api_overlay_dir() / API_ENTRY_FILENAME


def validate_api_skeleton() -> tuple[bool, list[str]]:
    """Validate baseline API profile skeleton structure.

    Returns:
        Tuple of validation success flag and a list of missing path descriptions.
    """
    required_paths: list[tuple[Path, str, str]] = [
        (get_api_overlay_dir(), "api overlay directory", "dir"),
        (get_api_overlay_dir() / API_README_FILENAME, "api overlay readme", "file"),
        (get_api_entry_file(), "api overlay entry script", "file"),
    ]

    missing_descriptions: list[str] = []
    for path, description, expected_kind in required_paths:
        is_valid = path.is_dir() if expected_kind == "dir" else path.is_file()
        if not is_valid:
            missing_descriptions.append(f"{description}: {path}")

    return len(missing_descriptions) == 0, missing_descriptions
