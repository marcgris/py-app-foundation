"""Unit tests for API overlay helper behavior."""

from starter.api_overlay import (
    API_APP_NAME,
    API_HEALTH_RESPONSE,
    API_HEALTH_ROUTE,
    get_api_entry_file,
    get_api_overlay_dir,
    validate_api_skeleton,
)


class TestApiOverlayPaths:
    """Test suite for API overlay path resolution."""

    def test_api_overlay_paths_exist(self) -> None:
        """Test API overlay directory and entry script exist."""
        assert get_api_overlay_dir().is_dir()
        assert get_api_entry_file().is_file()


class TestApiOverlayValidation:
    """Test suite for API overlay skeleton validation."""

    def test_validate_api_skeleton_when_files_present_returns_true(self) -> None:
        """Test API skeleton validation returns success for baseline layout."""
        is_valid, missing = validate_api_skeleton()

        assert is_valid is True
        assert missing == []

    def test_api_contract_constants_are_stable(self) -> None:
        """Test API contract constants remain stable for smoke tests."""
        assert API_APP_NAME == "Py App Foundation API Profile"
        assert API_HEALTH_ROUTE == "/health"
        assert API_HEALTH_RESPONSE == "ok"
