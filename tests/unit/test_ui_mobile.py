"""Unit tests for UI mobile profile helper behavior."""

from starter.ui import (
    UI_MOBILE_APP_NAME,
    UI_MOBILE_SMOKE_MARKER_TEXT,
    get_ui_mobile_entry_file,
    get_ui_mobile_profile_dir,
    validate_ui_mobile_skeleton,
)


class TestUiMobilePaths:
    """Test suite for UI mobile profile path resolution."""

    def test_ui_mobile_paths_exist(self) -> None:
        """Test mobile profile directory and entry script exist."""
        assert get_ui_mobile_profile_dir().is_dir()
        assert get_ui_mobile_entry_file().is_file()


class TestUiMobileValidation:
    """Test suite for UI mobile profile skeleton validation."""

    def test_validate_ui_mobile_skeleton_when_files_present_returns_true(self) -> None:
        """Test mobile skeleton validation returns success for baseline layout."""
        is_valid, missing = validate_ui_mobile_skeleton()

        assert is_valid is True
        assert missing == []

    def test_mobile_smoke_marker_contract_constants_are_stable(self) -> None:
        """Test mobile marker constants remain stable for smoke contract tests."""
        assert UI_MOBILE_APP_NAME == "Py App Foundation Mobile Profile"
        assert UI_MOBILE_SMOKE_MARKER_TEXT == "starter-ui-mobile-ready"
