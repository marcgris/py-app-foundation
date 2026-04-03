"""Tests for the exceptions module."""

import pytest

from starter.exceptions import (
    AppRuntimeError,
    ConfigError,
    StarterError,
    ValidationError,
)


class TestStarterError:
    """Test suite for StarterError base class."""

    def test_starter_error_message(self) -> None:
        """Test that StarterError preserves the error message."""
        message = "Something went wrong"
        error = StarterError(message)

        assert str(error) == message
        assert error.message == message

    def test_starter_error_with_details(self) -> None:
        """Test that StarterError can store additional details."""
        message = "Configuration failed"
        details = {"key": "database_url", "reason": "invalid format"}
        error = StarterError(message, details=details)

        assert error.message == message
        assert error.details == details

    def test_starter_error_is_exception(self) -> None:
        """Test that StarterError is an Exception."""
        error = StarterError("test")

        assert isinstance(error, Exception)

    def test_starter_error_inheritance(self) -> None:
        """Test that other errors inherit from StarterError."""
        error1 = ConfigError("test")
        error2 = ValidationError("test")

        assert isinstance(error1, StarterError)
        assert isinstance(error2, StarterError)


class TestConfigError:
    """Test suite for ConfigError."""

    def test_config_error_message(self) -> None:
        """Test that ConfigError preserves message."""
        message = "DEBUG environment variable is invalid"
        error = ConfigError(message)

        assert error.message == message

    def test_config_error_with_details(self) -> None:
        """Test that ConfigError can include details about the config problem."""
        message = "Missing required setting"
        details = {"setting": "DATABASE_URL"}
        error = ConfigError(message, details=details)

        assert error.details == details

    def test_config_error_can_be_caught_as_starter_error(self) -> None:
        """Test that ConfigError can be caught as StarterError."""
        with pytest.raises(StarterError):
            raise ConfigError("test")

    def test_config_error_can_be_caught_as_config_error(self) -> None:
        """Test that ConfigError can be caught specifically."""
        with pytest.raises(ConfigError):
            raise ConfigError("test")


class TestValidationError:
    """Test suite for ValidationError."""

    def test_validation_error_message(self) -> None:
        """Test that ValidationError preserves message."""
        message = "Invalid email format"
        error = ValidationError(message)

        assert error.message == message

    def test_validation_error_with_details(self) -> None:
        """Test that ValidationError can include validation details."""
        message = "Validation failed"
        details = {"field": "email", "error": "invalid format"}
        error = ValidationError(message, details=details)

        assert error.details == details

    def test_validation_error_can_be_caught_as_starter_error(self) -> None:
        """Test that ValidationError can be caught as StarterError."""
        with pytest.raises(StarterError):
            raise ValidationError("test")


class TestAppRuntimeError:
    """Test suite for AppRuntimeError."""

    def test_runtime_error_message(self) -> None:
        """Test that AppRuntimeError preserves message."""
        message = "Database connection failed"
        error = AppRuntimeError(message)

        assert error.message == message

    def test_runtime_error_with_details(self) -> None:
        """Test that AppRuntimeError can include runtime context."""
        message = "Service initialization failed"
        details = {"service": "cache", "error": "connection refused"}
        error = AppRuntimeError(message, details=details)

        assert error.details == details


class TestExceptionHierarchy:
    """Test suite for exception hierarchy and catching."""

    def test_catch_specific_error(self) -> None:
        """Test that specific errors can be caught independently."""
        with pytest.raises(ConfigError):
            raise ConfigError("config error")

        with pytest.raises(ValidationError):
            raise ValidationError("validation error")

        # ConfigError should not be caught by ValidationError handler
        with pytest.raises(ConfigError):
            try:
                raise ConfigError("test")
            except ValidationError:
                pytest.fail("ConfigError should not be caught by ValidationError")

    def test_catch_base_starter_error(self) -> None:
        """Test that StarterError catches all custom error types."""
        errors = [
            ConfigError("config"),
            ValidationError("validation"),
            AppRuntimeError("runtime"),
        ]

        for error in errors:
            with pytest.raises(StarterError):
                raise error
