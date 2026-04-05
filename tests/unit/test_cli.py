"""Tests for the CLI module."""

import argparse
import json

import pytest

from starter.cli import build_parser, main


class TestBuildParser:
    """Test suite for parser configuration."""

    def test_build_parser_supports_health_command(self) -> None:
        """Test that parser recognizes the health command."""
        parser = build_parser()

        parsed = parser.parse_args(["health"])

        assert parsed.command == "health"

    def test_build_parser_supports_config_show(self) -> None:
        """Test that parser recognizes the config show command."""
        parser = build_parser()

        parsed = parser.parse_args(["config", "show"])

        assert parsed.command == "config"
        assert parsed.config_command == "show"

    def test_build_parser_command_tree_matches_contract(self) -> None:
        """Test parser command and subcommand names remain contract-stable."""
        parser = build_parser()

        top_level_subparsers = next(
            action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
        )
        assert sorted(top_level_subparsers.choices.keys()) == ["config", "health"]

        config_parser = top_level_subparsers.choices["config"]
        config_subparsers = next(
            action
            for action in config_parser._actions
            if isinstance(action, argparse._SubParsersAction)
        )
        assert sorted(config_subparsers.choices.keys()) == ["show"]


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

    def test_main_config_without_subcommand_returns_usage_error(self) -> None:
        """Test that missing config subcommand returns argparse usage code."""
        exit_code = main(["config"])

        assert exit_code == 2

    def test_main_version_returns_success(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that --version returns zero and emits version text."""
        exit_code = main(["--version"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.err == ""
        assert captured.out.startswith("starter ")

    def test_main_config_show_returns_settings_json(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that config show prints settings as JSON and exits zero."""
        exit_code = main(["config", "show"])

        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert exit_code == 0
        assert payload["app_name"] == "starter"
        assert payload["debug"] is False
        assert payload["log_level"] == "INFO"

    def test_main_health_config_error_returns_stable_stderr(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test health command config failures are stable and return non-zero."""
        monkeypatch.setenv("LOG_LEVEL", "INVALID")

        exit_code = main(["health"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert captured.out == ""
        assert (
            captured.err.strip()
            == "Configuration error while running 'health': Failed to load settings."
        )

    def test_main_config_show_config_error_returns_stable_stderr(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test config show failures are stable and return non-zero."""
        monkeypatch.setenv("LOG_LEVEL", "INVALID")

        exit_code = main(["config", "show"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert captured.out == ""
        assert (
            captured.err.strip()
            == "Configuration error while running 'config show': Failed to load settings."
        )
