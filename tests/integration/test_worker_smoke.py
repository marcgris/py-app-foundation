"""Integration smoke tests for worker overlay profile skeleton."""

import json
import runpy
from collections.abc import Callable
from typing import cast

import pytest

from starter.worker_overlay import (
    WORKER_APP_NAME,
    WORKER_JOB_NAME,
    WORKER_JOB_STATUS,
    get_worker_entry_file,
)


class TestWorkerSmoke:
    """Smoke-level validation for worker profile contract behavior."""

    def test_worker_entry_contains_contract_constants(self) -> None:
        """Test worker entry script includes stable contract constant values."""
        source = get_worker_entry_file().read_text(encoding="utf-8")

        assert f'APP_NAME = "{WORKER_APP_NAME}"' in source
        assert f'JOB_NAME = "{WORKER_JOB_NAME}"' in source
        assert f'JOB_STATUS = "{WORKER_JOB_STATUS}"' in source

    def test_worker_shell_output_contract_shape(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test worker shell run output emits JSON with expected contract keys."""
        namespace = runpy.run_path(str(get_worker_entry_file()))
        run_fn = cast(Callable[[], None], namespace["run"])

        run_fn()

        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["app_name"] == WORKER_APP_NAME
        assert payload["job_name"] == WORKER_JOB_NAME
        assert payload["job_status"] == WORKER_JOB_STATUS
