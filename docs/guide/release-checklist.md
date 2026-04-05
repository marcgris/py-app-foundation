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
10. Run the recommendation register review gate:
   - Review `docs/plan/ROADMAP.md` recommendation register entries tied to the release scope.
   - Mark each relevant recommendation as addressed or explicitly deferred with rationale.
   - Include recommendation IDs in the release PR description.

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
| Checkpoint 3 (skill-library) | Completed | Recorded in roadmap hardening outcomes |
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
7. Review recommendation register entries for UI scope and capture addressed/deferred IDs in the promotion PR.

Definition of done for UI Beta promotion:

1. Status in matrix and contract docs updated from `Experimental` to `Beta` for promoted components.
2. Beta freeze expectations are documented (commands, markers, and error behavior where applicable).
3. Release notes include compatibility statement for promoted UI components.

## API Beta Readiness Checklist

Use this checklist before promoting API overlay from `Experimental` to `Beta`.

Current baseline status snapshot:

| Item | Current Status | Notes |
|---|---|---|
| API overlay skeleton | Completed | Implemented and marked `Experimental` |
| API Skill-Library Checkpoint 1 | Completed | Recorded in roadmap |
| API Skill-Library Checkpoint 2 | Not yet completed | Required before Beta promotion |
| Beta freeze statement for API surface | Not yet completed | Must be added in release docs/changelog when promoting |
| One full release cycle stability evidence | Not yet completed | Required by promotion guidance |

Promotion checklist:

1. Confirm API contract surface to freeze for one release cycle.
2. Confirm docs/changelog alignment:
   - `docs/guide/index.md`
   - `docs/plan/ROADMAP.md`
   - `CHANGELOG.md`
3. Run full validation gates (ruff, format-check, pyright, pytest, bandit).
4. Complete API Skill-Library Checkpoint 2 and record outcome in roadmap.
5. Verify no open High/Critical review findings for API contract behavior.
6. Review recommendation register entries for API scope and capture addressed/deferred IDs in the promotion PR.

## Worker Beta Readiness Checklist

Use this checklist before promoting worker overlay from `Experimental` to `Beta`.

Current baseline status snapshot:

| Item | Current Status | Notes |
|---|---|---|
| Worker overlay skeleton | Completed | Implemented and marked `Experimental` |
| Worker Skill-Library Checkpoint 1 | Completed | Recorded in roadmap |
| Worker Skill-Library Checkpoint 2 | Not yet completed | Required before Beta promotion |

Promotion checklist:

1. Implement worker skeleton and baseline smoke contract tests.
2. Run Worker Skill-Library Checkpoint 1 and record outcomes.
3. Complete full validation gates and CI checks.
4. Run Worker Skill-Library Checkpoint 2 before Beta promotion.
5. Review recommendation register entries for worker scope and capture addressed/deferred IDs in the promotion PR.

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
