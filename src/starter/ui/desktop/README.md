# UI Desktop Profile

This profile provides a minimal desktop-oriented skeleton with a deterministic
window-title and marker contract.

## Local Run Contract

From repository root:

```bash
uv run python src/starter/ui/desktop/app.py
```

## Validation Contract

From repository root:

```bash
uv run pytest tests/unit/test_ui_desktop.py tests/integration/test_ui_desktop_smoke.py -v
```

## Deterministic Smoke Marker

The desktop profile defines:

- window title: `Py App Foundation Desktop Profile`
- marker text: `starter-ui-desktop-ready`

Tests assert these constants to validate baseline profile behavior.
