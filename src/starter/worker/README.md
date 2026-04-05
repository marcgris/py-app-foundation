# Worker Overlay Profile

This profile provides a minimal framework-light worker skeleton with a deterministic
job-result contract.

## Local Run Contract

From repository root:

```bash
uv run python src/starter/worker/app.py
```

## Validation Contract

From repository root:

```bash
uv run pytest tests/unit/test_worker.py tests/integration/test_worker_smoke.py -v
```

## Deterministic Contract

The worker profile defines:

- app name: `Py App Foundation Worker Profile`
- job name: `baseline-job`
- job status: `processed`

Tests assert these constants to validate baseline profile behavior.
