"""Logging configuration and utilities."""

import logging
import logging.handlers
from typing import Any

from starter.config import Settings


def setup_logging(
    level: str = "INFO",
    format_str: str | None = None,
    log_file: str | None = None,
) -> None:
    """Configure application logging with optional file output.

    Sets up the root logger with console output and optional file rotation.
    Apply once at application startup.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_str: Custom format string. Defaults to timestamp - name - level - message
        log_file: Optional file path for log rotation. If provided, logs to both
                 console and file with daily rotation (7 day retention)

    Example:
        ```python
        from starter.logging import setup_logging

        setup_logging(level="DEBUG", log_file="app.log")
        logger = logging.getLogger(__name__)
        logger.info("Application started")
        ```
    """
    if format_str is None:
        format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_str)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with rotation (if requested)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=7,
        )
        file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger for the given module name.

    Always use this function to create module-level loggers.
    Ensures consistent logger naming across the application.

    Args:
        name: Logger name, typically __name__ of the module

    Returns:
        Configured logger for the module

    Example:
        ```python
        from starter.logging import get_logger

        logger = get_logger(__name__)
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        ```
    """
    return logging.getLogger(name)


def setup_logging_from_settings(settings: Settings) -> None:
    """Configure logging from application settings.

    Convenience function to apply logging configuration from a Settings object.

    Args:
        settings: Application settings object

    Example:
        ```python
        from starter.config import Settings
        from starter.logging import setup_logging_from_settings

        settings = Settings()
        setup_logging_from_settings(settings)
        ```
    """
    setup_logging(level=settings.log_level)


def log_context(**kwargs: Any) -> dict[str, Any]:
    """Create structured logging context for enhanced debugging.

    Useful for adding structured context to log messages:

    Args:
        **kwargs: Key-value pairs to include in context

    Returns:
        Dictionary of context for logging

    Example:
        ```python
        logger.info(
            "Processing request",
            extra=log_context(user_id=123, action="read")
        )
        ```
    """
    return {"context": kwargs}
