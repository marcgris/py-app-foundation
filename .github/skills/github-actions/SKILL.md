---
name: github-actions
description: >
  Use when creating, debugging, or improving GitHub Actions CI/CD workflows for
  Python projects. Covers CI quality gates, test pipelines, Docker builds,
  deployment workflows, Dependabot, and workflow debugging.
  Trigger on: "add CI", "create a workflow", "fix my pipeline", "GitHub Actions",
  "deployment workflow", "add automated testing", "workflow is failing",
  "add a release workflow".
---

# GitHub Actions Skill

GitHub Actions workflows are infrastructure-as-code. Apply the same quality
standards to them as your application code.

## Workflow Anatomy

```
.github/
└── workflows/
    ├── ci.yml          ← runs on every push/PR: lint, type-check, test
    ├── release.yml     ← runs on tags: build, publish, deploy
    └── dependabot.yml  ← automated dependency updates
```

## The Core CI Workflow

See `.github/workflows/ci.yml` for the complete, production-ready workflow.

Every CI run must execute these gates **in order, failing fast**:

1. **Lint & Format** — `ruff check` + `ruff format --check`
2. **Type Check** — `pyright` (strict mode)
3. **Security Scan** — `bandit -r src/` or `pip-audit`
4. **Tests + Coverage** — `pytest` with `--cov-fail-under=80`
5. **Aggregate Code Quality** — rerun core checks in final gate

## Canonical CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

env:
  PYTHON_VERSION: "3.14"

jobs:
  lint:
    name: Lint and Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v2

      - name: Install dependencies
        run: uv sync

      - name: Lint (ruff)
        run: uv run ruff check .

      - name: Format check (ruff)
        run: uv run ruff format . --check

  type-check:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v2

      - name: Install dependencies
        run: uv sync

      - name: Pyright
        run: uv run pyright src/

  test:
    name: Test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.14"]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install uv
        uses: astral-sh/setup-uv@v2

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest tests/ -v --cov=src/starter --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.python-version == '3.14'
        with:
          files: ./coverage.xml
          fail_ci_if_error: false

  code-quality:
    name: Code Quality
    runs-on: ubuntu-latest
    needs: [lint, type-check, test]
    if: success()
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v2

      - name: Install dependencies
        run: uv sync

      - name: Security scan (bandit)
        run: uv run bandit -r src/ -q
```

## Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*.*.*"

jobs:
  build-and-push:
    name: Build & Push Docker Image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    groups:
      dev-dependencies:
        patterns: ["pytest*", "ruff", "pyright", "coverage"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Environment & Secrets Pattern

```yaml
# Use environments for deployment protection rules
jobs:
  deploy-staging:
    environment: staging
    env:
      DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
      SECRET_KEY: ${{ secrets.STAGING_SECRET_KEY }}

  deploy-production:
    environment: production  # requires manual approval
    needs: [deploy-staging]
```

## Debugging Failing Workflows

When a workflow fails, check in this order:

1. **Read the full log** — expand each step, look for the first red line
2. **Check for missing secrets** — `${{ secrets.MY_SECRET }}` evaluates to empty string silently
3. **Check service health** — the Postgres `--health-cmd` must pass before steps run
4. **Reproduce locally** — use `act` to run GitHub Actions locally:
   ```bash
   brew install act
   act pull_request -j quality
   ```
5. **Add debug output** — temporarily add `ACTIONS_STEP_DEBUG: true` to env

## Common Fixes

| Symptom | Cause | Fix |
|---|---|---|
| `uv: command not found` | setup-uv not installed | Add an `astral-sh/setup-uv` step |
| DB connection refused | Service not healthy | Add `options: --health-cmd pg_isready` |
| Tests pass locally, fail in CI | Missing env var | Add to workflow `env:` block |
| Coverage drops on merge | PR coverage not enforced | Add `--cov-fail-under=80` |
| Slow workflow (> 5min) | No caching | Add `enable-cache: true` to setup-uv |
| Old workflow still running | No concurrency control | Add `concurrency:` block |
