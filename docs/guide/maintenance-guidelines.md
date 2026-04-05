# Maintenance Guidelines

This document defines how Py App Foundation is maintained after `v1.0.0`.
Use it together with `release-checklist.md` and `contributing.md`.

## Scope And Support Model

1. `main` is the only actively developed branch.
2. Only tagged releases are considered supported baselines.
3. Community support is best-effort through issues and pull requests.
4. Security fixes and correctness regressions are prioritized over feature requests.

## Release Cadence

1. Patch releases (`x.y.Z`) are cut as needed for bug fixes, security fixes, and non-breaking documentation corrections.
2. Minor releases (`x.Y.0`) are cut for backward-compatible additions to core modules, overlays, or developer workflow.
3. Major releases (`X.0.0`) are cut only for intentional breaking contract changes with explicit migration notes.
4. Every release must follow `docs/guide/release-checklist.md`.

## Compatibility And Stability

1. Core/Base Template is treated as stable starting at `v1.0.0`.
2. Overlay maturity remains independent and is tracked in the compatibility matrix in `docs/guide/index.md`.
3. Beta overlays must include explicit compatibility statements in changelog/release notes before status promotion.
4. Experimental overlays may change more quickly but still require deterministic smoke contracts and validation gates.

## Deprecation Policy

1. Deprecations are announced in `CHANGELOG.md` at least one minor release before removal whenever practical.
2. Each deprecation entry must include:
   - what is deprecated,
   - why,
   - the recommended replacement,
   - planned removal version.
3. Breaking removals are only applied in a major release unless required for urgent security reasons.

## Security And Dependency Maintenance

1. Keep dependency and security workflows green (`bandit`, `pip-audit`, and CI security jobs).
2. Address High/Critical findings before cutting a release.
3. Keep skill guidance aligned with repository truth (for example `pyproject.toml`, `.github/workflows/*.yml`).
4. Treat documentation drift as a maintenance issue and fix it in the next patch/minor release.

## Operational Ownership

1. Release owner for each version is identified in the release-prep PR.
2. Release owner responsibilities:
   - confirm changelog/version consistency,
   - run full validation locally,
   - ensure CI and release guard checks are green,
   - publish release notes.
3. Any contributor merging release-affecting changes must keep docs and matrix entries current.

## Quality Gates For Maintenance Changes

All maintenance PRs that modify code or contracts must pass:

```bash
uv sync
uv run ruff check .
uv run ruff format . --check
uv run pyright src/
uv run pytest tests/ -v
uv run bandit -r src/
```

## Incident Response For Regressions

1. Confirm and reproduce the issue from a clean checkout.
2. Add or update a test that captures the regression.
3. Ship the smallest safe fix.
4. Backfill changelog and release notes with impact and remediation.
