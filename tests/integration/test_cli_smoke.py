"""Integration smoke tests for starter CLI commands."""

import json

import pytest

from starter.cli import main


class TestCliSmoke:
    """Smoke-level validation for CLI behavior."""

    def test_health_command_smoke(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test health command can run end-to-end in process."""
        exit_code = main(["health"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "ok"

    def test_config_show_command_smoke(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test config show command can run end-to-end in process."""
        exit_code = main(["config", "show"])

        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert exit_code == 0
        assert payload["app_name"] == "starter"

    def test_health_command_config_error_smoke(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test health command reports deterministic error on invalid config."""
        monkeypatch.setenv("LOG_LEVEL", "INVALID")

        exit_code = main(["health"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert captured.out == ""
        assert (
            captured.err.strip()
            == "Configuration error while running 'health': Failed to load settings."
        )

    def test_version_flag_smoke(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test version flag can run end-to-end in process."""
        exit_code = main(["--version"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.err == ""
        assert captured.out.startswith("starter ")
