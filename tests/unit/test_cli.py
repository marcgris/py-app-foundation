"""Tests for the CLI module."""

import pytest

from starter.cli import build_parser, main


class TestBuildParser:
    """Test suite for parser configuration."""

    def test_build_parser_supports_health_command(self) -> None:
        """Test that parser recognizes the health command."""
        parser = build_parser()

        parsed = parser.parse_args(["health"])

        assert parsed.command == "health"


class TestMain:
    """Test suite for CLI command dispatch."""

    def test_main_health_returns_success(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that health command returns zero and prints ok."""
        exit_code = main(["health"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "ok"

    def test_main_without_command_returns_usage_error(self) -> None:
        """Test that missing command returns argparse usage code."""
        exit_code = main([])

        assert exit_code == 2

    def test_main_with_invalid_command_returns_usage_error(self) -> None:
        """Test that invalid command returns argparse usage code."""
        exit_code = main(["not-a-command"])

        assert exit_code == 2
