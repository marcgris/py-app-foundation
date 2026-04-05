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
- **CLI Command Contract**: See [cli-command-contract.md](cli-command-contract.md)
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

## Copilot Capabilities (Phase A)

To support incremental adoption, the base template currently enables a focused quality set:

1. Skills:
	- dependency-management
	- python-testing
	- python-refactor
	- security-audit
2. Agent:
	- code-reviewer

Overlay-specific skills and agents are intentionally deferred until overlay implementation phases.

## Overlays

This core is designed to be extended:

- **CLI Overlay**: For command-line applications
- **API Overlay**: For web services
- **Worker Overlay**: For background jobs and scheduled tasks
- **UI Overlay**: For frontend and UI-heavy applications

Each overlay adds minimal framework-specific code while inheriting the core's validation and guardrails.

### Template And Overlay Compatibility Matrix

This table is meant to answer two questions quickly:

1. What is included by default in a core-only project?
2. Which release tag should I start from for a given capability?

| Component | Type | Included In Core-Only Project | Current Status | First Available | Status Since | Recommended Starting Tag | Notes |
|-----------|------|-------------------------------|----------------|-----------------|--------------|--------------------------|-------|
| Core/Base Template | Base foundation | Yes | Beta | v0.1.0 | v0.1.0 | Latest release tag (currently `v0.4.0`) | Foundation modules and validation stack used by all project types |
| CLI | Overlay | No | Beta | v0.3.0 | v0.4.0 | `v0.4.0` or newer | Commands: `starter health`, `starter config show`, `starter --version`; compatibility contract documented |
| API | Overlay | No | Planned | N/A | N/A | N/A | Overlay not implemented yet |
| Worker | Overlay | No | Planned | N/A | N/A | N/A | Overlay not implemented yet |
| UI | Overlay | No | Planned | N/A | N/A | N/A | Overlay not implemented yet |
| Scheduled Jobs/Cron | Overlay candidate | No | Backlog | N/A | N/A | N/A | Candidate for later demand |
| Data/ETL Pipeline | Overlay candidate | No | Backlog | N/A | N/A | N/A | Candidate for later demand |
| MCP Server | Overlay candidate | No | Backlog | N/A | N/A | N/A | Candidate for later demand |
| Library/Package-Only | Overlay candidate | No | Backlog | N/A | N/A | N/A | Candidate for later demand |

Status legend used in the table:

- Planned: designed but not implemented.
- Backlog: candidate tracked for future planning.
- Experimental: implemented, may change quickly.
- Beta: feature-complete for trial usage.
- Stable: production-ready with managed compatibility expectations.

Core-only quick rule:

- Use `v0.2.1` if you want a snapshot with no implemented overlays present in the template.
- Use latest release tag if you want current core improvements and are okay with CLI overlay code being present.

Core/Base Template stability rule: move from Beta to Stable when v1.0.0 is released, all planned overlays pass the full validation gate, and release documentation confirms no open v1 exit criteria.

### CLI Status

CLI reached Beta in `v0.4.0`.

For current compatibility guarantees and command contract details, see [cli-command-contract.md](cli-command-contract.md).
For the release history of this status change, see [../../CHANGELOG.md](../../CHANGELOG.md).

Recommended implementation order (current):

Effort baseline: CLI overlay implementation is treated as 100%.

1. CLI (100%)
	Context: First proof-of-concept for the overlay model and command contract baseline. Completed in v0.4.0 Beta.
2. UI (120%)
	Context: High anticipated demand; adds frontend structure, build workflow, and local integration boundary. Slightly higher effort than CLI due to tooling and UX validation.
3. API (160%)
	Context: Highest effort among planned overlays because framework and service-boundary decisions are still open; includes route contracts, request/response validation, and integration testing patterns.
4. Worker (130%)
	Context: Adds background execution patterns, scheduler or queue boundaries, retry/error semantics, and worker-focused observability.
5. MCP Server (backlog, 175%)
	Context: Tooling and protocol boundary work is broader than a single app shape; expected to require command/tool contract design, integration testing strategy, and additional operational guidance.
6. Scheduled Jobs/Cron (backlog, 115%)
	Context: Moderately above CLI; adds scheduling semantics, idempotency expectations, failure handling, and runtime execution policies.
7. Data/ETL Pipeline (backlog, 185%)
	Context: High complexity profile with data-flow boundaries, transform reliability, schema evolution concerns, and stronger validation/performance expectations.
8. Library/Package-Only (backlog, 70%)
	Context: Lower relative implementation effort because runtime entrypoints are minimal, but still requires packaging, API surface, and compatibility discipline.

## Design Philosophy

1. **Framework-light**: The core avoids forcing a choice about web frameworks, ORMs, or deployment
2. **Security by default**: Linting, type-checking, and dependency scanning are always on
3. **Explicit over implicit**: Conventions are documented; magic is minimal
4. **Agent-friendly**: Instructions and guardrails make autonomous development reliable
5. **Testable**: Every core module includes test patterns you can build on

## Questions?

See the [planning documentation](../plan/ROADMAP.md) for design rationale and decisions.
