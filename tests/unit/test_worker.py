"""Unit tests for worker overlay helper behavior."""

from starter.worker_overlay import (
    WORKER_APP_NAME,
    WORKER_JOB_NAME,
    WORKER_JOB_STATUS,
    get_worker_entry_file,
    get_worker_overlay_dir,
    validate_worker_skeleton,
)


class TestWorkerOverlayPaths:
    """Test suite for worker overlay path resolution."""

    def test_worker_overlay_paths_exist(self) -> None:
        """Test worker overlay directory and entry script exist."""
        assert get_worker_overlay_dir().is_dir()
        assert get_worker_entry_file().is_file()


class TestWorkerOverlayValidation:
    """Test suite for worker overlay skeleton validation."""

    def test_validate_worker_skeleton_when_files_present_returns_true(self) -> None:
        """Test worker skeleton validation returns success for baseline layout."""
        is_valid, missing = validate_worker_skeleton()

        assert is_valid is True
        assert missing == []

    def test_worker_contract_constants_are_stable(self) -> None:
        """Test worker contract constants remain stable for smoke tests."""
        assert WORKER_APP_NAME == "Py App Foundation Worker Profile"
        assert WORKER_JOB_NAME == "baseline-job"
        assert WORKER_JOB_STATUS == "processed"
