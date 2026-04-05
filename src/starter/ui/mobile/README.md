# UI Mobile Profile

This profile provides a minimal mobile-oriented shell contract with deterministic
app-name and marker constants for smoke validation.

## Local Run Contract

From repository root:

```bash
uv run python src/starter/ui/mobile/app.py
```

## Validation Contract

From repository root:

```bash
uv run pytest tests/unit/test_ui_mobile.py tests/integration/test_ui_mobile_smoke.py -v
```

## Deterministic Smoke Marker

The mobile profile defines:

- app name: `Py App Foundation Mobile Profile`
- marker text: `starter-ui-mobile-ready`

Tests assert these constants to validate baseline profile behavior.
