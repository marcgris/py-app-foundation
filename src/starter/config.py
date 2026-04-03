"""Configuration loading and management using pydantic-settings."""

from typing import Any, Literal

from pydantic import Field
from pydantic import ValidationError as PydanticValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from starter.exceptions import ConfigError


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file.

    Settings follow 12-factor app principles: configuration via environment.
    Defaults are for local development; override via environment variables.

    Attributes:
        debug: Enable debug mode with verbose logging
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        app_name: Application name for logging and identification
    """

    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )
    app_name: str = Field(default="starter", description="Application name")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to dictionary.

        Returns:
            Dictionary representation of settings.
        """
        return self.model_dump()


def load_settings(env_file: str | None = None) -> Settings:
    """Load and validate application settings.

    Loads configuration from:
    1. Environment variables (highest priority)
    2. .env file or custom env_file (if provided)
    3. Class defaults (lowest priority)

    Args:
        env_file: Optional path to custom .env file. If None, uses default .env

    Returns:
        Validated Settings object

    Raises:
        ConfigError: If settings validation fails
    """
    try:
        settings_kwargs: dict[str, Any] = {}
        if env_file:
            settings_kwargs["_env_file"] = env_file
        return Settings(**settings_kwargs)
    except PydanticValidationError as exc:
        raise ConfigError(
            "Failed to load settings",
            details={"errors": str(exc)},
        ) from exc
