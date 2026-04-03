# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]

## [0.2.1] - 2026-04-03

### Added
- Phase A Copilot workspace enablement files under `.vscode/`:
	- `settings.json` (strict analysis, Copilot settings, cross-platform terminal env)
	- `extensions.json` (lean recommended extension baseline)
	- `mcp.json` (minimal MCP servers: github, filesystem, fetch, git)
- Quality-focused Copilot skill set in `.github/skills/`:
	- `dependency-management`
	- `python-testing`
	- `python-refactor`
	- `security-audit`
- `code-reviewer` agent in `.github/agents/` for architecture/type/security/test-focused review.
- Copilot invocation cookbook in contributor documentation for repeatable skill and agent usage.
- Concrete AI-assisted review prompts in the release checklist.

### Changed
- Updated `.gitignore` to track selected workspace config files:
	- `.vscode/settings.json`
	- `.vscode/extensions.json`
	- `.vscode/mcp.json`
- Normalized `code-reviewer` agent configuration for portability (`model: auto`) and valid tool references.
- Aligned dependency-management skill examples and snippets to Python 3.14 baseline.

### Documentation
- Extended roadmap/contributing/release docs for incremental Copilot adoption and review-gate operationalization.

## [0.2.0] - 2026-04-03

### Added
- Python 3.14 baseline with updated CI/CD, pre-commit, and type checking configuration.
- Overlay compatibility matrix for tracking base template and overlay maturity independently.
- UI overlay as fourth planned overlay alongside CLI, API, and Worker.
- Future overlay backlog: Scheduled Jobs/Cron, Data/ETL Pipeline, MCP Server, Library/Package-Only.
- Recommended overlay implementation order and stability criteria for v1.0.0 promotion.
- Overlay matrix update requirement in release checklist.

### Changed
- Upgraded project to Python 3.14 as baseline (requires Python >=3.14).
- Simplified `Generator` type annotation in test fixtures (Python 3.14 compat).
- Updated Ruff target version, Pyright Python version, and mypy configuration to 3.14.
- Regenerated `uv.lock` for Python 3.14 dependency resolution.

### Documentation
- Added overlay compatibility matrix to guide with status definitions (Planned, Backlog, Experimental, Beta, Stable).
- Updated ROADMAP and ARCHITECTURE for four-overlay portfolio with backlog candidates.
- Added Core/Base Template stability rule: moves from Beta to Stable at v1.0.0 when all planned overlays pass validation.

## [0.1.1] - 2026-04-02

### Added
- Release checklist and changelog governance for repeatable template releases.
- New project bootstrap checklist (`docs/guide/new-project.md`).
- Release guard CI workflow enforcing version/changelog sync on PRs to main.

### Changed
- Strict `Literal` log-level validation on `Settings`; `load_settings` now raises `ConfigError` instead of pydantic `ValidationError`.
- Renamed custom `RuntimeError` to `AppRuntimeError` to avoid shadowing the built-in.
- Migrated `[tool.uv] dev-dependencies` to `[dependency-groups]` (uv ≥ 0.4 standard).
- Fixed pip-audit CI to export dependencies before auditing, avoiding local package resolution failure.
- Clarified release process in repository documentation.

## [0.1.0] - 2026-04-02

### Added
- Initial Py App Foundation baseline with core modules, validation stack, and CI/security workflows.
