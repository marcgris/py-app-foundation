# Release Checklist

Use this checklist for every release tag.

## Versioning Policy

- Use Semantic Versioning: MAJOR.MINOR.PATCH.
- Bump MAJOR for breaking template/API changes.
- Bump MINOR for backward-compatible additions.
- Bump PATCH for fixes and non-breaking maintenance.
- Keep the project version in pyproject.toml as the source of truth.

## Pre-Release Checklist

1. Confirm all planned release items are merged to main.
2. Update CHANGELOG.md:
   - Move completed items from Unreleased into the new version section.
   - Add release date in YYYY-MM-DD format.
3. Bump version in pyproject.toml.
4. Run local validation:

```bash
uv sync
uv run ruff check .
uv run ruff format . --check
uv run pyright src/
uv run pytest tests/ -v
uv run bandit -r src/
```

5. Confirm CI is green on the release PR.
6. Verify docs are current for any user-facing changes.
7. Update the overlay compatibility matrix in `docs/guide/index.md` (status, introduced version, and stable-as-of fields).
8. If CLI status changes to Beta in this release, include a CLI compatibility statement in changelog/release notes covering command surface, exit codes, and deterministic config-error stderr format.
9. Run AI-assisted review checks and resolve material findings:
   - Architecture/code-quality review
   - Test coverage and edge-case review
   - Security review

Use prompts like:

- `@code-reviewer review this release diff for architecture violations, type-safety regressions, and missing tests.`
- `Use python-testing: review changed tests for missing assertions and uncovered edge cases in this release.`
- `Use security-audit: perform an OWASP-focused review of changed files and rank findings by severity.`

## UI Beta Readiness Checklist

Use this checklist before promoting any UI component from `Experimental` to `Beta`.

Current baseline status snapshot:

| Item | Current Status | Notes |
|---|---|---|
| UI Shared Base | Completed | Implemented and marked `Experimental` |
| UI Web Profile | Completed | Implemented and marked `Experimental` |
| UI Desktop Profile | Completed | Implemented and marked `Experimental` |
| UI Mobile Profile | Completed | Implemented and marked `Experimental` |
| Checkpoint 1 (skill-library) | Completed | Recorded in roadmap |
| Checkpoint 2 (skill-library) | Completed | Recorded in roadmap |
| Checkpoint 3 (skill-library) | Not yet completed | Required before Beta promotion |
| Beta freeze statement for UI surfaces | Not yet completed | Must be added in release docs/changelog when promoting |
| One full release cycle stability evidence | Not yet completed | Required by UI contract promotion guidance |

Promotion checklist:

1. Confirm promotion scope:
   - UI Shared Base, UI Web Profile, UI Desktop Profile, UI Mobile Profile (promote individually or as a set).
2. Confirm contract and docs alignment:
   - `docs/guide/ui-overlay-contract.md`
   - `docs/guide/index.md`
   - `docs/plan/ROADMAP.md`
   - `README.md`
3. Run full validation gates:
   - `uv sync`
   - `uv run ruff check .`
   - `uv run ruff format . --check`
   - `uv run pyright src/`
   - `uv run pytest tests/ -v`
   - `uv run bandit -r src/`
4. Complete Checkpoint 3 and record outcome in roadmap.
5. Add Beta promotion notes to `CHANGELOG.md` including what is frozen for one release cycle.
6. Verify no open High/Critical review findings for UI contract behavior.

Definition of done for UI Beta promotion:

1. Status in matrix and contract docs updated from `Experimental` to `Beta` for promoted components.
2. Beta freeze expectations are documented (commands, markers, and error behavior where applicable).
3. Release notes include compatibility statement for promoted UI components.

## Tagging And Publishing

1. Merge the release prep PR into main.
2. Create an annotated tag from main:

```bash
git checkout main
git pull
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

3. Create a GitHub release for tag vX.Y.Z using changelog entries as release notes.
4. Do not retag or modify an existing version tag.

## Post-Release

1. Add a fresh Unreleased section to CHANGELOG.md if needed.
2. Confirm downstream template consumers can bootstrap and pass validation from a clean checkout.
