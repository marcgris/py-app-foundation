# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]

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
