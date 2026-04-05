"""Utilities for UI overlay skeleton discovery and validation."""

from __future__ import annotations

from pathlib import Path

UI_OVERLAY_DIRNAME = "ui"
UI_SHARED_DIRNAME = "shared"
UI_WEB_DIRNAME = "web"
UI_WEB_ENTRY_FILENAME = "index.html"
UI_WEB_SMOKE_MARKER_ID = "starter-ui-smoke-marker"
UI_WEB_SMOKE_MARKER_TEXT = "starter-ui-web-ready"


def get_ui_overlay_root() -> Path:
    """Return the absolute path to the UI overlay root directory.

    Returns:
        Absolute path to the UI overlay folder.
    """
    return Path(__file__).resolve().parent / UI_OVERLAY_DIRNAME


def get_ui_shared_base_dir() -> Path:
    """Return the absolute path to shared UI base assets.

    Returns:
        Absolute path to the shared UI base directory.
    """
    return get_ui_overlay_root() / UI_SHARED_DIRNAME


def get_ui_web_profile_dir() -> Path:
    """Return the absolute path to the UI web profile directory.

    Returns:
        Absolute path to the web profile directory.
    """
    return get_ui_overlay_root() / UI_WEB_DIRNAME


def get_ui_web_entry_file() -> Path:
    """Return the absolute path to the web profile entry HTML file.

    Returns:
        Absolute path to the web entry file.
    """
    return get_ui_web_profile_dir() / UI_WEB_ENTRY_FILENAME


def validate_ui_web_skeleton() -> tuple[bool, list[str]]:
    """Validate baseline UI Shared Base and Web profile structure.

    Returns:
        Tuple of validation success flag and a list of missing path descriptions.
    """
    required_paths: list[tuple[Path, str]] = [
        (get_ui_overlay_root(), "ui overlay root"),
        (get_ui_shared_base_dir(), "ui shared base directory"),
        (get_ui_shared_base_dir() / "README.md", "ui shared base readme"),
        (get_ui_shared_base_dir() / "design-tokens.css", "ui shared base design tokens"),
        (get_ui_web_profile_dir(), "ui web profile directory"),
        (get_ui_web_profile_dir() / "README.md", "ui web profile readme"),
        (get_ui_web_profile_dir() / "styles.css", "ui web profile stylesheet"),
        (get_ui_web_profile_dir() / "app.js", "ui web profile script"),
        (get_ui_web_entry_file(), "ui web entry html"),
    ]

    missing_descriptions: list[str] = []
    for path, description in required_paths:
        if not path.exists():
            missing_descriptions.append(f"{description}: {path}")

    return len(missing_descriptions) == 0, missing_descriptions
