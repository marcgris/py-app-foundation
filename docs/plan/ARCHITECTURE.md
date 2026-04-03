# Py App Foundation Architecture

## Overview

The starter uses a layered model: one reusable core foundation plus optional overlays for specific application shapes. The core contains the engineering baseline shared by all generated projects. Overlays add the smallest viable runtime and structure for a specific project type without weakening the core standards.

## Goals

1. Provide a reusable base for professional Python applications.
2. Keep startup cost low for new projects.
3. Enforce strong defaults for testing, typing, linting, and security.
4. Make agent behavior more reliable through explicit repository guidance.
5. Allow new project shapes to be added without rewriting the core.

## Non-Goals

1. Becoming a full internal platform.
2. Supporting every Python framework in v1.
3. Embedding cloud deployment logic in the base starter.
4. Choosing a universal data layer for all projects.

## System Model

1. The core template defines the common engineering foundation.
2. An overlay adds project-shape-specific files, dependencies, and entry points.
3. A generated project is the result of applying the core plus zero or one initial overlay.
4. Planning documents define intent, decisions, and handoff state outside the generated code itself.

## Core Template Responsibilities

1. Python version and packaging defaults.
2. Project layout under a src-based structure.
3. Dependency and environment management approach.
4. Linting, formatting, and type-checking configuration.
5. Test layout and baseline fixtures.
6. Security scanning configuration.
7. Typed settings pattern (pydantic-settings).
8. Logging and error-handling pattern.
9. Documentation baseline.
10. Agent instruction files and repository guardrails.

## Overlays

### CLI Overlay
- Adds command entry point and argument handling
- Includes CLI-focused example layout
- Builds on top of core config and logging patterns

### API Overlay
- Adds service entry point (framework TBD)
- Includes minimal web app structure
- API-focused validation and examples

### Worker Overlay
- Adds job runner pattern
- Scheduler or queue integration boundary
- Worker-focused validation and examples

### UI Overlay
- Adds frontend project structure and build workflow
- Defines local dev integration boundary to backend services
- UI-focused validation and examples

### Future Candidate Overlays (Backlog)
- Scheduled jobs/cron profile
- Data/ETL pipeline profile
- MCP server profile
- Library/package-only profile

## Cross-Cutting Concerns

1. **Configuration**: Environment-driven and typed via pydantic-settings.
2. **Logging**: Structured, production-friendly output.
3. **Error Handling**: Explicit and testable exception hierarchy.
4. **Secrets**: Never stored in examples or defaults.
5. **Dependencies**: Locked and auditable via uv.lock.
6. **Validation**: Same expectations locally and in CI.

## Repository Layout

```
py-app-foundation/
├── docs/
│   ├── plan/           # Design artifacts and session context
│   └── guide/          # User-facing contributor and usage guidance
├── src/starter/        # Core starter modules
├── tests/
│   ├── unit/           # Fast isolated tests
│   └── integration/    # Multi-component validation
├── .github/workflows/  # CI automation
├── pyproject.toml      # Single control plane
├── .pre-commit-hooks.yaml
├── .copilot-instructions.md
├── .instructions.md
└── [root config files]
```

## Validation Model

1. Local validation covers linting, formatting, typing, tests, and security scans.
2. CI re-runs the same validation with consistent thresholds.
3. A generated project passes validation from a clean checkout without manual fixes.
4. Agent-generated changes are not considered ready unless validation passes.

## Extension Strategy

1. Add overlays only when a project shape is common enough to justify standardization.
2. Keep optional capabilities modular and additive.
3. Avoid introducing dependencies into the core unless all overlays benefit.
4. Prefer stable interfaces between core and overlays.

## Deferred Decisions

1. Deployment target and container strategy.
2. API framework selection for the API overlay.
3. Task runner beyond uv (e.g., Makefile, just, etc.).
4. Generator implementation mechanism (copy-based, template engine, etc.).
5. Observability tooling beyond the baseline logging pattern.
