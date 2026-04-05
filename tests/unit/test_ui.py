"""Tests for UI overlay helper utilities."""

from starter.ui import (
    UI_WEB_SMOKE_MARKER_ID,
    UI_WEB_SMOKE_MARKER_TEXT,
    get_ui_overlay_root,
    get_ui_shared_base_dir,
    get_ui_web_entry_file,
    get_ui_web_profile_dir,
    validate_ui_web_skeleton,
)


class TestUiOverlayPaths:
    """Test suite for UI overlay path discovery."""

    def test_ui_overlay_paths_exist(self) -> None:
        """Test that shared base and web profile paths resolve correctly."""
        assert get_ui_overlay_root().is_dir()
        assert get_ui_shared_base_dir().is_dir()
        assert get_ui_web_profile_dir().is_dir()
        assert get_ui_web_entry_file().is_file()


class TestUiOverlayValidation:
    """Test suite for UI overlay skeleton validation."""

    def test_validate_ui_web_skeleton_when_files_present_returns_true(self) -> None:
        """Test skeleton validation returns success for the baseline layout."""
        is_valid, missing = validate_ui_web_skeleton()

        assert is_valid is True
        assert missing == []

    def test_ui_smoke_marker_contract_constants_are_stable(self) -> None:
        """Test marker constants remain stable for contract and smoke tests."""
        assert UI_WEB_SMOKE_MARKER_ID == "starter-ui-smoke-marker"
        assert UI_WEB_SMOKE_MARKER_TEXT == "starter-ui-web-ready"
