"""Integration smoke tests for UI mobile profile skeleton."""

from starter.ui import (
    UI_MOBILE_APP_NAME,
    UI_MOBILE_SMOKE_MARKER_TEXT,
    get_ui_mobile_entry_file,
)


class TestUiMobileSmoke:
    """Smoke-level validation for UI mobile profile contract behavior."""

    def test_ui_mobile_entry_contains_app_name_constant(self) -> None:
        """Test mobile entry script includes stable app name constant value."""
        source = get_ui_mobile_entry_file().read_text(encoding="utf-8")

        assert f'APP_NAME = "{UI_MOBILE_APP_NAME}"' in source

    def test_ui_mobile_entry_contains_smoke_marker_text_constant(self) -> None:
        """Test mobile entry script includes stable smoke marker text constant value."""
        source = get_ui_mobile_entry_file().read_text(encoding="utf-8")

        assert f'SMOKE_MARKER_TEXT = "{UI_MOBILE_SMOKE_MARKER_TEXT}"' in source
