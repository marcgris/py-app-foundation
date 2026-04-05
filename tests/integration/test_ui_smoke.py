"""Integration smoke tests for UI shared base and web profile skeleton."""

from starter.ui import (
    UI_WEB_SMOKE_MARKER_ID,
    UI_WEB_SMOKE_MARKER_TEXT,
    get_ui_shared_base_dir,
    get_ui_web_entry_file,
)


class TestUiWebSmoke:
    """Smoke-level validation for UI web profile behavior contract."""

    def test_ui_web_entry_contains_deterministic_smoke_marker(self) -> None:
        """Test web entry HTML includes the deterministic smoke marker contract."""
        html = get_ui_web_entry_file().read_text(encoding="utf-8")

        marker_snippet = f'id="{UI_WEB_SMOKE_MARKER_ID}"'
        assert marker_snippet in html
        assert UI_WEB_SMOKE_MARKER_TEXT in html

    def test_ui_web_entry_references_shared_design_tokens(self) -> None:
        """Test web entry references shared base design tokens stylesheet."""
        html = get_ui_web_entry_file().read_text(encoding="utf-8")

        assert "../shared/design-tokens.css" in html

    def test_shared_design_tokens_file_exists(self) -> None:
        """Test shared base design token file exists for cross-profile reuse."""
        token_file = get_ui_shared_base_dir() / "design-tokens.css"

        assert token_file.is_file()
