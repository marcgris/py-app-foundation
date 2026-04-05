# API Overlay Profile

This profile provides a minimal framework-light API skeleton with a deterministic
health-route contract.

## Local Run Contract

From repository root:

```bash
uv run python src/starter/api/app.py
```

## Validation Contract

From repository root:

```bash
uv run pytest tests/unit/test_api.py tests/integration/test_api_smoke.py -v
```

## Deterministic Contract

The API profile defines:

- app name: `Py App Foundation API Profile`
- health route: `/health`
- health response: `ok`

Tests assert these constants to validate baseline profile behavior.
