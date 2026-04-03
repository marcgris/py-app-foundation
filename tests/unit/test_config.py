"""Tests for the config module."""

import pytest
from pydantic import ValidationError as PydanticValidationError

from starter.config import Settings, load_settings
from starter.exceptions import ConfigError


class TestSettings:
    """Test suite for Settings class."""

    def test_settings_defaults(self) -> None:
        """Test that Settings loads with default values."""
        settings = Settings()

        assert settings.debug is False
        assert settings.log_level == "INFO"
        assert settings.app_name == "starter"

    def test_settings_from_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that Settings loads from environment variables."""
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("APP_NAME", "myapp")

        settings = Settings()

        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        assert settings.app_name == "myapp"

    def test_settings_case_insensitive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that Settings environment variables are case-insensitive."""
        monkeypatch.setenv("debug", "true")  # lowercase
        monkeypatch.setenv("LOG_LEVEL", "WARNING")  # uppercase

        settings = Settings()

        assert settings.debug is True
        assert settings.log_level == "WARNING"

    def test_settings_invalid_log_level(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that invalid log level fails validation."""
        monkeypatch.setenv("LOG_LEVEL", "INVALID")

        with pytest.raises(PydanticValidationError):
            Settings()

    def test_settings_to_dict(self) -> None:
        """Test that Settings can be converted to dictionary."""
        settings = Settings(debug=True, log_level="ERROR")

        settings_dict = settings.to_dict()

        assert settings_dict["debug"] is True
        assert settings_dict["log_level"] == "ERROR"
        assert settings_dict["app_name"] == "starter"


class TestLoadSettings:
    """Test suite for load_settings function."""

    def test_load_settings_defaults(self) -> None:
        """Test that load_settings returns valid Settings with defaults."""
        settings = load_settings()

        assert isinstance(settings, Settings)
        assert settings.debug is False

    def test_load_settings_from_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that load_settings respects environment variables."""
        monkeypatch.setenv("APP_NAME", "custom-app")

        settings = load_settings()

        assert settings.app_name == "custom-app"

    def test_load_settings_invalid_raises_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that load_settings raises on invalid settings."""
        monkeypatch.setenv("LOG_LEVEL", "INVALID")

        with pytest.raises(ConfigError):
            load_settings()
