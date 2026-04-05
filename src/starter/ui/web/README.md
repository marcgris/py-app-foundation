# UI Web Profile

This profile provides a minimal web-oriented UI skeleton built on plain HTML, CSS,
and JavaScript so the template remains framework-light.

## Local Run Contract

From repository root:

```bash
uv run python -m http.server 4173 --directory src/starter/ui/web
```

Then open `http://localhost:4173/`.

## Validation Contract

From repository root:

```bash
uv run pytest tests/unit/test_ui.py tests/integration/test_ui_smoke.py -v
```

## Deterministic Smoke Marker

The web entry page includes a deterministic marker element:

- element id: `starter-ui-smoke-marker`
- marker text: `starter-ui-web-ready`

Tests assert this marker to validate baseline profile behavior.
