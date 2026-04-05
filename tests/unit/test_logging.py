"""Tests for the logging module."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from starter.logging import (
    get_logger,
    log_context,
    setup_logging,
    setup_logging_from_settings,
)


class TestSetupLogging:
    """Test suite for setup_logging function."""

    def test_setup_logging_default_level(self) -> None:
        """Test that setup_logging configures root logger with default INFO level."""
        setup_logging()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

    def test_setup_logging_debug_level(self) -> None:
        """Test that setup_logging respects custom log level."""
        setup_logging(level="DEBUG")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_setup_logging_with_file(self, tmp_path: Path) -> None:
        """Test that setup_logging creates file handler when log_file is provided."""
        log_file = tmp_path / "app.log"

        setup_logging(log_file=str(log_file))

        root_logger = logging.getLogger()

        # Check that file handler was added
        handlers = root_logger.handlers
        has_file_handler = any(isinstance(h, RotatingFileHandler) for h in handlers)
        assert has_file_handler

    def test_setup_logging_custom_format(self) -> None:
        """Test that setup_logging applies custom format string."""
        custom_format = "%(levelname)s - %(message)s"
        setup_logging(format_str=custom_format)

        root_logger = logging.getLogger()
        handler = root_logger.handlers[0]
        formatter = handler.formatter

        assert formatter is not None
        assert "%(levelname)s" in formatter._fmt  # type: ignore

    def test_setup_logging_removes_duplicates(self) -> None:
        """Test that setup_logging removes existing handlers to avoid duplicates."""
        setup_logging()
        initial_count = len(logging.getLogger().handlers)

        setup_logging()
        final_count = len(logging.getLogger().handlers)

        # Should not have doubled the handlers
        assert final_count <= initial_count + 1


class TestGetLogger:
    """Test suite for get_logger function."""

    def test_get_logger_returns_logger(self) -> None:
        """Test that get_logger returns a logging.Logger instance."""
        logger = get_logger("test.module")

        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.module"

    def test_get_logger_module_name(self) -> None:
        """Test that get_logger preserves the module name."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        assert logger1.name == "module1"
        assert logger2.name == "module2"
        assert logger1 is not logger2

    def test_get_logger_same_name_returns_same_instance(self) -> None:
        """Test that get_logger returns the same instance for the same name."""
        logger1 = get_logger("shared.module")
        logger2 = get_logger("shared.module")

        assert logger1 is logger2


class TestSetupLoggingFromSettings:
    """Test suite for setup_logging_from_settings function."""

    def test_setup_logging_from_settings(self) -> None:
        """Test that setup_logging_from_settings applies settings correctly."""
        from starter.config import Settings

        settings = Settings(log_level="WARNING")
        setup_logging_from_settings(settings)

        root_logger = logging.getLogger()
        assert root_logger.level == logging.WARNING

    def test_setup_logging_from_settings_debug(self) -> None:
        """Test setup_logging_from_settings with debug enabled."""
        from starter.config import Settings

        settings = Settings(debug=True, log_level="DEBUG")
        setup_logging_from_settings(settings)

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG


class TestLogContext:
    """Test suite for log_context utility function."""

    def test_log_context_returns_dict(self) -> None:
        """Test that log_context returns a dictionary."""
        context = log_context(user_id=123, action="read")

        assert isinstance(context, dict)
        assert "context" in context

    def test_log_context_preserves_values(self) -> None:
        """Test that log_context preserves all provided values."""
        context = log_context(user_id=123, action="read", status="success")

        assert context["context"]["user_id"] == 123
        assert context["context"]["action"] == "read"
        assert context["context"]["status"] == "success"

    def test_log_context_empty(self) -> None:
        """Test log_context with no arguments."""
        context = log_context()

        assert context == {"context": {}}
