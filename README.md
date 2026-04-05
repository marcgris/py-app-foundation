# Py App Foundation

A reusable, professional, secure foundation for building Python applications with strong defaults for code quality, testing, security, and autonomous development workflows.

## Features

- **Framework-Light Core**: No premature choices about web frameworks, ORMs, or deployment
- **Secure by Default**: Linting, type-checking, and security scanning always on
- **Agent-Friendly**: Explicit guardrails and instructions for reliable autonomous development
- **Composable**: One core foundation plus optional overlays for CLI, UI, API, and worker applications
- **Strong Defaults**: Tested patterns for configuration, logging, and error handling

## Quick Start

1. Clone or download this repository
2. Copy the core modules to your project or use as a template
3. Run `uv sync` to install dependencies
4. Run validation: `uv run pytest tests/ && uv run ruff check . && uv run pyright src/`

## Documentation

- **Getting Started**: See [docs/guide/index.md](docs/guide/index.md)
- **Contributing**: See [docs/guide/contributing.md](docs/guide/contributing.md)
- **Release Checklist**: See [docs/guide/release-checklist.md](docs/guide/release-checklist.md)
- **Architecture**: See [docs/plan/ARCHITECTURE.md](docs/plan/ARCHITECTURE.md)
- **Roadmap**: See [docs/plan/ROADMAP.md](docs/plan/ROADMAP.md)
- **Decisions**: See [docs/plan/DECISIONS.md](docs/plan/DECISIONS.md)
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md)
- **Template Version Selection (Core vs Overlays)**: See the Overlay Compatibility Matrix in [docs/guide/index.md](docs/guide/index.md)

## Core Modules

```
src/starter/
├── config.py       # Typed, environment-driven settings using pydantic
├── logging.py      # Structured logging bootstrap and conventions
├── exceptions.py   # Custom exception hierarchy for applications
```

## CLI Overlay (Current)

The first CLI overlay increment is available through the `starter` command.

```bash
uv run starter health
# ok

uv run starter config show
# {"app_name": "starter", "debug": false, "log_level": "INFO"}

uv run starter --version
# starter 0.4.0
```

The `config show` command reads the same environment-driven settings as the core
starter modules, and command failures from invalid configuration return a
deterministic non-zero error response.

## UI Overlay (Shared Base + Web Profile)

The UI overlay now supports a shared-base plus profile model. The first
implemented profile is Web.

```bash
# Start local UI preview server (shared base + web profile)
uv run python -m http.server 4173 --directory src/starter/ui

# Open the web profile
# http://localhost:4173/web/

# Validate UI shared base + web profile contract
uv run pytest tests/unit/test_ui.py tests/integration/test_ui_smoke.py -v
```

Deterministic smoke marker contract for the web profile:

- Element ID: `starter-ui-smoke-marker`
- Marker text: `starter-ui-web-ready`

See [docs/guide/ui-overlay-contract.md](docs/guide/ui-overlay-contract.md) for
the full shared-base and profile contract model.

## UI Desktop Profile (Current)

The Desktop profile now includes a minimal deterministic shell contract.

```bash
# Run desktop profile shell
uv run python src/starter/ui/desktop/app.py

# Validate desktop profile contract tests
uv run pytest tests/unit/test_ui_desktop.py tests/integration/test_ui_desktop_smoke.py -v
```

## UI Mobile Profile (Current)

The Mobile profile now includes a minimal deterministic shell contract.

```bash
# Run mobile profile shell
uv run python src/starter/ui/mobile/app.py

# Validate mobile profile contract tests
uv run pytest tests/unit/test_ui_mobile.py tests/integration/test_ui_mobile_smoke.py -v
```

## API Overlay Profile (Current)

The API profile now includes a minimal framework-light skeleton with a
deterministic health-route contract.

```bash
# Run API profile shell
uv run python src/starter/api/app.py

# Validate API profile contract tests
uv run pytest tests/unit/test_api.py tests/integration/test_api_smoke.py -v
```

## Worker Overlay Profile (Current)

The worker profile now includes a minimal framework-light skeleton with a
deterministic job-result contract.

```bash
# Run worker profile shell
uv run python src/starter/worker/app.py

# Validate worker profile contract tests
uv run pytest tests/unit/test_worker.py tests/integration/test_worker_smoke.py -v
```

## Validation

Every project built from this starter must pass:

```bash
uv sync                    # Install dependencies
uv run ruff check .        # Lint check
uv run ruff format .       # Format code
uv run pyright src/        # Type checking
uv run pytest tests/       # Run tests
uv run bandit -r src/      # Security scanning
```

## Python Version

Requires Python 3.14 or later. See `.python-version` for the pinned version.

## License

Apache 2.0. See LICENSE for details.

## Contributing

This is a foundation template meant to be extended and customized. See [docs/guide/contributing.md](docs/guide/contributing.md) for guidelines.

## Release Process

Releases use Semantic Versioning and are documented in [CHANGELOG.md](CHANGELOG.md).

Use [docs/guide/release-checklist.md](docs/guide/release-checklist.md) for the full release flow:

1. Prepare release PR (version bump + changelog update)
2. Validate locally and in CI
3. Merge to `main`
4. Create annotated tag `vX.Y.Z`
5. Publish GitHub release notes from changelog entries
