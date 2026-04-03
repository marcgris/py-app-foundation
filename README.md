# Py App Foundation

A reusable, professional, secure foundation for building Python applications with strong defaults for code quality, testing, security, and autonomous development workflows.

## Features

- **Framework-Light Core**: No premature choices about web frameworks, ORMs, or deployment
- **Secure by Default**: Linting, type-checking, and security scanning always on
- **Agent-Friendly**: Explicit guardrails and instructions for reliable autonomous development
- **Composable**: One core foundation plus optional overlays for CLI, API, and worker applications
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

## Core Modules

```
src/starter/
├── config.py       # Typed, environment-driven settings using pydantic
├── logging.py      # Structured logging bootstrap and conventions
├── exceptions.py   # Custom exception hierarchy for applications
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
