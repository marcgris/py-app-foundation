# Py App Foundation

Welcome to Py App Foundation—a reusable, professional, secure foundation for building Python applications.

## What This Is

This repository is a template and reference implementation for bootstrapping production-grade Python projects. It provides:

- **Strong Defaults**: Linting, type-checking, testing, and security scanning out of the box
- **Composable Architecture**: One core foundation plus optional overlays for CLI, API, and background worker applications
- **Agent-Friendly**: Explicit guardrails and instruction files that make autonomous development workflows reliable
- **Framework-Light**: No premature choices about web frameworks, ORMs, or deployment targets

## Quick Links

- **Starting a New Project**: See [new-project.md](new-project.md)
- **For Contributors**: See [contributing.md](contributing.md)
- **For Releases**: See [release-checklist.md](release-checklist.md)
- **For Design Context**: See the [planning docs](../plan/ROADMAP.md)
- **Architecture Details**: See [ARCHITECTURE.md](../plan/ARCHITECTURE.md)
- **Change History**: See [../../CHANGELOG.md](../../CHANGELOG.md)

## Structure

```
├── src/starter/          # Core starter modules (config, logging, exceptions)
├── tests/                # Test infrastructure (unit, integration)
├── .github/workflows/    # CI automation
├── docs/plan/            # Planning and decision artifacts
├── docs/guide/           # Contributor and usage guidance
└── pyproject.toml        # Project metadata and tool configuration
```

## Core Modules

The starter provides reusable patterns for every generated project:

- **config.py**: Typed environment-driven settings using pydantic-settings
- **logging.py**: Structured logging bootstrap and conventions
- **exceptions.py**: Custom exception hierarchy for application errors

## Validation

Every project built from this starter must pass:

```bash
uv sync                          # Install dependencies
uv run ruff check .              # Lint
uv run ruff format .             # Format
uv run pyright src/              # Type-check
uv run pytest tests/             # Test
uv run bandit -r src/            # Security scan
```

## Getting Started

1. Clone or copy this repository
2. Customize the package name in `src/starter/`
3. Run `uv sync` to install dependencies
4. Run the validation commands above
5. Start building your application

For more detailed guidance, see [contributing.md](contributing.md).

## Overlays

This core is designed to be extended:

- **CLI Overlay**: For command-line applications
- **API Overlay**: For web services
- **Worker Overlay**: For background jobs and scheduled tasks

Each overlay adds minimal framework-specific code while inheriting the core's validation and guardrails.

## Design Philosophy

1. **Framework-light**: The core avoids forcing a choice about web frameworks, ORMs, or deployment
2. **Security by default**: Linting, type-checking, and dependency scanning are always on
3. **Explicit over implicit**: Conventions are documented; magic is minimal
4. **Agent-friendly**: Instructions and guardrails make autonomous development reliable
5. **Testable**: Every core module includes test patterns you can build on

## Questions?

See the [planning documentation](../plan/ROADMAP.md) for design rationale and decisions.
