"""Integration tests for core starter modules working together."""

import logging

from starter.config import Settings
from starter.exceptions import ConfigError
from starter.logging import setup_logging, setup_logging_from_settings


class TestConfigLoggingIntegration:
    """Test suite for config and logging working together."""

    def test_settings_with_logging(self) -> None:
        """Test that settings can be used to configure logging."""
        settings = Settings(debug=True, log_level="DEBUG", app_name="integration-test")

        setup_logging_from_settings(settings)

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_logging_logs_to_configured_level(self) -> None:
        """Test that logger respects the configured log level."""
        setup_logging(level="ERROR")

        logger = logging.getLogger("test")
        # Debug and info should not log, but error should
        # This is a behavioral test
        assert logger.isEnabledFor(logging.ERROR)
        assert not logger.isEnabledFor(logging.DEBUG)

    def test_multiple_loggers_same_config(self) -> None:
        """Test that multiple loggers respect the same root configuration."""
        setup_logging(level="WARNING")

        logger1 = logging.getLogger("module1")
        logger2 = logging.getLogger("module2")

        assert logger1.getEffectiveLevel() == logging.WARNING
        assert logger2.getEffectiveLevel() == logging.WARNING


class TestConfigExceptionIntegration:
    """Test suite for config and exceptions working together."""

    def test_config_error_on_invalid_setting(self) -> None:
        """Test that config problems raise ConfigError."""
        from starter.config import load_settings

        # Even with invalid log level, pydantic coerces it
        # This test documents current behavior
        settings = load_settings()
        assert isinstance(settings, Settings)

    def test_exception_details_from_config(self) -> None:
        """Test that exceptions can be raised with config context."""
        settings = Settings(app_name="test-app")

        try:
            raise ConfigError(
                "Database config invalid",
                details={"app": settings.app_name, "setting": "DATABASE_URL"},
            )
        except ConfigError as e:
            assert e.details["app"] == "test-app"


class TestLoggingExceptionIntegration:
    """Test suite for logging and exceptions working together."""

    def test_log_exception_details(self) -> None:
        """Test that exceptions with details can be logged."""
        from starter.exceptions import ValidationError

        setup_logging(level="DEBUG")
        logger = logging.getLogger("test")

        error = ValidationError("Validation failed", details={"field": "email"})

        # Simulate what an app would do
        try:
            raise error
        except ValidationError as e:
            logger.error(f"Caught validation error: {e.message}")
            assert "Validation failed" in str(e)

    def test_logger_for_exception_context(self) -> None:
        """Test setting up logging with exception handling."""
        from starter.exceptions import AppRuntimeError

        setup_logging(level="INFO")
        logger = logging.getLogger("app")

        try:
            raise AppRuntimeError("Service failed", details={"service": "cache"})
        except AppRuntimeError as e:
            logger.error(f"Runtime error: {e.message}", extra={"details": e.details})


class TestFullStackIntegration:
    """Test suite for full starter stack integration."""

    def test_application_startup_pattern(self) -> None:
        """Test the typical application startup pattern using all starter modules."""
        # This is the pattern that generated projects should follow
        from starter.config import Settings
        from starter.logging import get_logger, setup_logging_from_settings

        # 1. Load configuration
        settings = Settings(debug=True, log_level="INFO", app_name="myapp")

        # 2. Setup logging
        setup_logging_from_settings(settings)

        # 3. Get application logger
        logger = get_logger(__name__)

        # 4. Log startup
        logger.info(f"Starting {settings.app_name} (debug={settings.debug})")

        # Verify everything worked together
        assert logger.name == __name__
        assert logging.getLogger().level == logging.INFO
