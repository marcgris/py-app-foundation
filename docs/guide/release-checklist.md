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
8. Run AI-assisted review checks and resolve material findings:
   - Architecture/code-quality review
   - Test coverage and edge-case review
   - Security review

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
