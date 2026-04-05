"""Integration smoke tests for API overlay profile skeleton."""

import json
import runpy
from collections.abc import Callable
from typing import cast

import pytest

from starter.api_overlay import (
    API_APP_NAME,
    API_HEALTH_RESPONSE,
    API_HEALTH_ROUTE,
    get_api_entry_file,
)


class TestApiSmoke:
    """Smoke-level validation for API profile contract behavior."""

    def test_api_entry_contains_contract_constants(self) -> None:
        """Test API entry script includes stable contract constant values."""
        source = get_api_entry_file().read_text(encoding="utf-8")

        assert f'APP_NAME = "{API_APP_NAME}"' in source
        assert f'HEALTH_ROUTE = "{API_HEALTH_ROUTE}"' in source
        assert f'HEALTH_RESPONSE = "{API_HEALTH_RESPONSE}"' in source

    def test_api_shell_output_contract_shape(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test API shell run output emits JSON with expected contract keys."""
        namespace = runpy.run_path(str(get_api_entry_file()))
        run_fn = cast(Callable[[], None], namespace["run"])

        run_fn()

        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["app_name"] == API_APP_NAME
        assert payload["health_route"] == API_HEALTH_ROUTE
        assert payload["health_response"] == API_HEALTH_RESPONSE
