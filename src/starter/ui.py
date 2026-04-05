"""Utilities for UI overlay skeleton discovery and validation."""

from __future__ import annotations

from pathlib import Path

UI_OVERLAY_DIRNAME = "ui"
UI_SHARED_DIRNAME = "shared"
UI_WEB_DIRNAME = "web"
UI_DESKTOP_DIRNAME = "desktop"
UI_MOBILE_DIRNAME = "mobile"
UI_WEB_ENTRY_FILENAME = "index.html"
UI_DESKTOP_ENTRY_FILENAME = "app.py"
UI_MOBILE_ENTRY_FILENAME = "app.py"
UI_WEB_SMOKE_MARKER_ID = "starter-ui-smoke-marker"
UI_WEB_SMOKE_MARKER_TEXT = "starter-ui-web-ready"
UI_DESKTOP_WINDOW_TITLE = "Py App Foundation Desktop Profile"
UI_DESKTOP_SMOKE_MARKER_TEXT = "starter-ui-desktop-ready"
UI_MOBILE_APP_NAME = "Py App Foundation Mobile Profile"
UI_MOBILE_SMOKE_MARKER_TEXT = "starter-ui-mobile-ready"


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


def get_ui_desktop_profile_dir() -> Path:
    """Return the absolute path to the UI desktop profile directory.

    Returns:
        Absolute path to the desktop profile directory.
    """
    return get_ui_overlay_root() / UI_DESKTOP_DIRNAME


def get_ui_desktop_entry_file() -> Path:
    """Return the absolute path to the desktop profile entry script.

    Returns:
        Absolute path to the desktop entry script.
    """
    return get_ui_desktop_profile_dir() / UI_DESKTOP_ENTRY_FILENAME


def get_ui_mobile_profile_dir() -> Path:
    """Return the absolute path to the UI mobile profile directory.

    Returns:
        Absolute path to the mobile profile directory.
    """
    return get_ui_overlay_root() / UI_MOBILE_DIRNAME


def get_ui_mobile_entry_file() -> Path:
    """Return the absolute path to the mobile profile entry script.

    Returns:
        Absolute path to the mobile entry script.
    """
    return get_ui_mobile_profile_dir() / UI_MOBILE_ENTRY_FILENAME


def validate_ui_web_skeleton() -> tuple[bool, list[str]]:
    """Validate baseline UI Shared Base and Web profile structure.

    Returns:
        Tuple of validation success flag and a list of missing path descriptions.
    """
    required_paths: list[tuple[Path, str, str]] = [
        (get_ui_overlay_root(), "ui overlay root", "dir"),
        (get_ui_shared_base_dir(), "ui shared base directory", "dir"),
        (get_ui_shared_base_dir() / "README.md", "ui shared base readme", "file"),
        (
            get_ui_shared_base_dir() / "design-tokens.css",
            "ui shared base design tokens",
            "file",
        ),
        (get_ui_web_profile_dir(), "ui web profile directory", "dir"),
        (get_ui_web_profile_dir() / "README.md", "ui web profile readme", "file"),
        (get_ui_web_profile_dir() / "styles.css", "ui web profile stylesheet", "file"),
        (get_ui_web_profile_dir() / "app.js", "ui web profile script", "file"),
        (get_ui_web_entry_file(), "ui web entry html", "file"),
    ]

    missing_descriptions: list[str] = []
    for path, description, expected_kind in required_paths:
        is_valid = path.is_dir() if expected_kind == "dir" else path.is_file()
        if not is_valid:
            missing_descriptions.append(f"{description}: {path}")

    return len(missing_descriptions) == 0, missing_descriptions


def validate_ui_desktop_skeleton() -> tuple[bool, list[str]]:
    """Validate baseline UI Desktop profile structure.

    Returns:
        Tuple of validation success flag and a list of missing path descriptions.
    """
    required_paths: list[tuple[Path, str, str]] = [
        (get_ui_overlay_root(), "ui overlay root", "dir"),
        (get_ui_shared_base_dir(), "ui shared base directory", "dir"),
        (get_ui_shared_base_dir() / "README.md", "ui shared base readme", "file"),
        (
            get_ui_shared_base_dir() / "design-tokens.css",
            "ui shared base design tokens",
            "file",
        ),
        (get_ui_desktop_profile_dir(), "ui desktop profile directory", "dir"),
        (get_ui_desktop_profile_dir() / "README.md", "ui desktop profile readme", "file"),
        (get_ui_desktop_entry_file(), "ui desktop entry script", "file"),
    ]

    missing_descriptions: list[str] = []
    for path, description, expected_kind in required_paths:
        is_valid = path.is_dir() if expected_kind == "dir" else path.is_file()
        if not is_valid:
            missing_descriptions.append(f"{description}: {path}")

    return len(missing_descriptions) == 0, missing_descriptions


def validate_ui_mobile_skeleton() -> tuple[bool, list[str]]:
    """Validate baseline UI Mobile profile structure.

    Returns:
        Tuple of validation success flag and a list of missing path descriptions.
    """
    required_paths: list[tuple[Path, str, str]] = [
        (get_ui_overlay_root(), "ui overlay root", "dir"),
        (get_ui_shared_base_dir(), "ui shared base directory", "dir"),
        (get_ui_shared_base_dir() / "README.md", "ui shared base readme", "file"),
        (
            get_ui_shared_base_dir() / "design-tokens.css",
            "ui shared base design tokens",
            "file",
        ),
        (get_ui_mobile_profile_dir(), "ui mobile profile directory", "dir"),
        (get_ui_mobile_profile_dir() / "README.md", "ui mobile profile readme", "file"),
        (get_ui_mobile_entry_file(), "ui mobile entry script", "file"),
    ]

    missing_descriptions: list[str] = []
    for path, description, expected_kind in required_paths:
        is_valid = path.is_dir() if expected_kind == "dir" else path.is_file()
        if not is_valid:
            missing_descriptions.append(f"{description}: {path}")

    return len(missing_descriptions) == 0, missing_descriptions
