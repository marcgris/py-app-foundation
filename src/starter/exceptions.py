"""Custom exception hierarchy for the starter and applications built on it."""


class StarterError(Exception):
    """Base exception for all starter-related errors.

    All custom exceptions should inherit from this to allow catching
    starter-specific errors distinctly from other exceptions.
    """

    def __init__(self, message: str, details: dict[str, str] | None = None) -> None:
        """Initialize StarterError with optional details.

        Args:
            message: Human-readable error message
            details: Optional dictionary of additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigError(StarterError):
    """Raised when configuration loading or validation fails.

    Indicates problems with:
    - Missing required environment variables
    - Invalid configuration values
    - Failed config file parsing
    - Invalid settings
    """


class ValidationError(StarterError):
    """Raised when data validation fails.

    Indicates problems with:
    - Invalid input schema
    - Failed validation rules
    - Type mismatches
    """


class AppRuntimeError(StarterError):
    """Raised when runtime errors occur during application execution.

    Indicates problems with:
    - Resource initialization
    - Service unavailability
    - Unexpected state
    """
