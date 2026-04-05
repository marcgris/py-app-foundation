"""Integration smoke tests for UI desktop profile skeleton."""

from starter.ui import (
    UI_DESKTOP_SMOKE_MARKER_TEXT,
    UI_DESKTOP_WINDOW_TITLE,
    get_ui_desktop_entry_file,
)


class TestUiDesktopSmoke:
    """Smoke-level validation for UI desktop profile contract behavior."""

    def test_ui_desktop_entry_contains_window_title_constant(self) -> None:
        """Test desktop entry script includes stable window title constant value."""
        source = get_ui_desktop_entry_file().read_text(encoding="utf-8")

        assert f'WINDOW_TITLE = "{UI_DESKTOP_WINDOW_TITLE}"' in source

    def test_ui_desktop_entry_contains_smoke_marker_text_constant(self) -> None:
        """Test desktop entry script includes stable smoke marker text constant value."""
        source = get_ui_desktop_entry_file().read_text(encoding="utf-8")

        assert f'SMOKE_MARKER_TEXT = "{UI_DESKTOP_SMOKE_MARKER_TEXT}"' in source
