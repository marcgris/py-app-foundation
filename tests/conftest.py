"""Shared test fixtures and utilities."""

import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from starter.config import Settings
from starter.logging import get_logger


@pytest.fixture
def temp_env_file() -> Generator[Path]:
    """Provide a temporary .env file for testing.

    Yields:
        Path to a temporary file that will be cleaned up after the test
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def mock_settings() -> Settings:
    """Provide a test settings object with debug enabled.

    Returns:
        Settings object configured for testing
    """
    return Settings(debug=True, log_level="DEBUG", app_name="test-app")


@pytest.fixture
def test_logger():
    """Provide a test logger.

    Returns:
        Logger for test output
    """
    return get_logger("test")


@pytest.fixture
def monkeypatch_env(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Provide a dict-like object to set environment variables in tests.

    Args:
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        Dictionary tracking env vars set during test
    """
    env_vars: dict[str, str] = {}

    def set_env(key: str, value: str) -> None:
        env_vars[key] = value
        monkeypatch.setenv(key, value)

    # Add a method to the dict for convenience
    env_vars["set"] = set_env  # type: ignore

    return env_vars


@pytest.fixture
def isolation(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, Any]:
    """Provide test isolation: temporary directory and env cleanup.

    Args:
        monkeypatch: pytest's monkeypatch fixture
        tmp_path: pytest's temporary directory fixture

    Returns:
        Dictionary with isolation context (cwd, tmp_dir)
    """
    original_cwd = Path.cwd()

    # Change to temp directory for test
    monkeypatch.chdir(str(tmp_path))

    yield {"cwd": original_cwd, "tmp_dir": tmp_path}

    # Restore original directory (monkeypatch handles env cleanup)
    monkeypatch.chdir(str(original_cwd))
