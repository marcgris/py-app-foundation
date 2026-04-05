"""Utilities for worker overlay skeleton discovery and validation."""

from __future__ import annotations

from pathlib import Path

WORKER_OVERLAY_DIRNAME = "worker"
WORKER_ENTRY_FILENAME = "app.py"
WORKER_README_FILENAME = "README.md"
WORKER_APP_NAME = "Py App Foundation Worker Profile"
WORKER_JOB_NAME = "baseline-job"
WORKER_JOB_STATUS = "processed"


def get_worker_overlay_dir() -> Path:
    """Return the absolute path to the worker overlay directory.

    Returns:
        Absolute path to the worker overlay folder.
    """
    return Path(__file__).resolve().parent / WORKER_OVERLAY_DIRNAME


def get_worker_entry_file() -> Path:
    """Return the absolute path to the worker overlay entry script.

    Returns:
        Absolute path to the worker entry script.
    """
    return get_worker_overlay_dir() / WORKER_ENTRY_FILENAME


def validate_worker_skeleton() -> tuple[bool, list[str]]:
    """Validate baseline worker profile skeleton structure.

    Returns:
        Tuple of validation success flag and a list of missing path descriptions.
    """
    required_paths: list[tuple[Path, str, str]] = [
        (get_worker_overlay_dir(), "worker overlay directory", "dir"),
        (get_worker_overlay_dir() / WORKER_README_FILENAME, "worker overlay readme", "file"),
        (get_worker_entry_file(), "worker overlay entry script", "file"),
    ]

    missing_descriptions: list[str] = []
    for path, description, expected_kind in required_paths:
        is_valid = path.is_dir() if expected_kind == "dir" else path.is_file()
        if not is_valid:
            missing_descriptions.append(f"{description}: {path}")

    return len(missing_descriptions) == 0, missing_descriptions
