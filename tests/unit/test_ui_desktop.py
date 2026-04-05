"""Unit tests for UI desktop profile helper behavior."""

from starter.ui import (
    UI_DESKTOP_SMOKE_MARKER_TEXT,
    UI_DESKTOP_WINDOW_TITLE,
    get_ui_desktop_entry_file,
    get_ui_desktop_profile_dir,
    validate_ui_desktop_skeleton,
)


class TestUiDesktopPaths:
    """Test suite for UI desktop profile path resolution."""

    def test_ui_desktop_paths_exist(self) -> None:
        """Test desktop profile directory and entry script exist."""
        assert get_ui_desktop_profile_dir().is_dir()
        assert get_ui_desktop_entry_file().is_file()


class TestUiDesktopValidation:
    """Test suite for UI desktop profile skeleton validation."""

    def test_validate_ui_desktop_skeleton_when_files_present_returns_true(self) -> None:
        """Test desktop skeleton validation returns success for baseline layout."""
        is_valid, missing = validate_ui_desktop_skeleton()

        assert is_valid is True
        assert missing == []

    def test_desktop_smoke_marker_contract_constants_are_stable(self) -> None:
        """Test desktop marker constants remain stable for smoke contract tests."""
        assert UI_DESKTOP_WINDOW_TITLE == "Py App Foundation Desktop Profile"
        assert UI_DESKTOP_SMOKE_MARKER_TEXT == "starter-ui-desktop-ready"
