# UI Desktop Profile

This profile provides a minimal desktop-oriented skeleton with a deterministic
window-title and marker contract.

This desktop profile requires Python with `tkinter`/Tk support. Some Python
builds do not include it by default, especially on minimal Linux installs.

If `tkinter` is missing, install Tk support for your platform and retry:

- Linux (Debian/Ubuntu): install `python3-tk`
- macOS: use a Python build that includes Tk support, such as the official
	Python.org installer
- Windows: use the official Python.org installer, which typically includes Tk

If you cannot run the GUI locally, use the validation command below as an
alternate no-GUI validation path.

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
