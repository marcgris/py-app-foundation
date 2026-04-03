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

### Overlay Compatibility Matrix

Use this matrix to track base template and overlay maturity while keeping a single repository version stream.

| Overlay | Status | Introduced In | Last Breaking Change | Current Stable As Of | Notes |
|---------|--------|---------------|----------------------|----------------------|-------|
| Core/Base Template | Beta | v0.1.0 | N/A | v0.3.0 | Implemented and validated; overall project remains pre-v1 |
| CLI | Experimental | v0.3.0 | v0.3.0 | N/A | Implemented baseline commands: `starter health`, `starter config show`, and `starter --version` |
| API | Planned | N/A | N/A | N/A | Overlay not implemented yet |
| Worker | Planned | N/A | N/A | N/A | Overlay not implemented yet |
| UI | Planned | N/A | N/A | N/A | Overlay not implemented yet |
| Scheduled Jobs/Cron | Backlog | N/A | N/A | N/A | Candidate for later demand |
| Data/ETL Pipeline | Backlog | N/A | N/A | N/A | Candidate for later demand |
| MCP Server | Backlog | N/A | N/A | N/A | Candidate for later demand |
| Library/Package-Only | Backlog | N/A | N/A | N/A | Candidate for later demand |

Status definitions:

- Planned: designed but not implemented
- Backlog: candidate overlay tracked for future planning
- Experimental: implemented, may change quickly
- Beta: feature-complete for trial usage
- Stable: production-ready with managed compatibility expectations

Core/Base Template stability rule: move from Beta to Stable when v1.0.0 is released, all planned overlays pass the full validation gate, and release documentation confirms no open v1 exit criteria.

### CLI Beta Acceptance Criteria

Move CLI from Experimental to Beta only when all checklist items are completed:

- [ ] CLI command contract is documented and frozen for one release cycle.
- [ ] Command names and semantics are stable for `starter health`, `starter config show`, and `starter --version`.
- [ ] Exit codes are documented and covered by tests.
- [ ] Deterministic config-error stderr format is documented and covered by tests.
- [ ] `config show` JSON output shape is documented and covered by tests.
- [ ] Unit and integration smoke tests for CLI commands are passing in CI.
- [ ] Validation gates pass with no CLI-specific exceptions: ruff, pyright, pytest, and bandit.
- [ ] Changelog and release notes include the CLI compatibility statement for the release where status changes to Beta.

Recommended implementation order (current):

1. CLI
2. UI
3. API
4. Worker
5. MCP Server (backlog)
6. Scheduled Jobs/Cron (backlog)
7. Data/ETL Pipeline (backlog)
8. Library/Package-Only (backlog)

## Design Philosophy

1. **Framework-light**: The core avoids forcing a choice about web frameworks, ORMs, or deployment
2. **Security by default**: Linting, type-checking, and dependency scanning are always on
3. **Explicit over implicit**: Conventions are documented; magic is minimal
4. **Agent-friendly**: Instructions and guardrails make autonomous development reliable
5. **Testable**: Every core module includes test patterns you can build on

## Questions?

See the [planning documentation](../plan/ROADMAP.md) for design rationale and decisions.
