---
name: dependency-management
description: >
  Use when managing Python project dependencies, virtual environments, packaging,
  pyproject.toml configuration, or uv workflows. Covers adding/removing packages,
  dependency groups, lock files, version constraints, and publishing.
  Trigger on: "add a package", "install dependency", "uv command", "pyproject.toml",
  "requirements.txt", "pin versions", "create a virtual environment", "package this",
  "dependency conflict", "publish to PyPI".
---

# Dependency Management Skill

Use **`uv`** for everything. It replaces `pip`, `pip-tools`, `virtualenv`,
`venv`, and `poetry` with a single, dramatically faster tool.

## Quick Reference — Common uv Commands

```bash
# Project setup
uv init my-project          # create new project
uv init --lib my-library    # create a library (with src layout)
uv python install 3.14      # install a specific Python version
uv python pin 3.14          # pin this project to Python 3.14 (.python-version)

# Dependencies
uv add fastapi              # add runtime dependency
uv add --dev pytest ruff    # add dev-only dependency
uv add --optional email "fastapi[email]"  # add optional extra
uv remove requests          # remove a dependency

# Running things
uv run pytest               # run in project venv
uv run python src/main.py   # run a script
uv run -- uvicorn src.main:app --reload  # run with args

# Lock file
uv lock                     # regenerate uv.lock from pyproject.toml
uv sync                     # install exactly what's in uv.lock
uv sync --all-extras        # install all optional extras too
uv sync --no-dev            # production install (no dev deps)

# Auditing
uv run pip-audit            # scan for CVEs in installed packages
```

## pyproject.toml — Complete Reference

```toml
[project]
name = "my-app"
version = "0.1.0"
description = "A FastAPI application"
readme = "README.md"
requires-python = ">=3.14"
license = { text = "MIT" }
authors = [{ name = "Your Name", email = "you@example.com" }]

# Runtime dependencies — these ship with your package
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.29.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.2.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[argon2]>=1.7.4",
    "structlog>=24.1.0",
    "httpx>=0.27.0",
]

# Optional extras — installed with: uv sync --extra email
[project.optional-dependencies]
email = ["sendgrid>=6.11.0"]
redis = ["redis[hiredis]>=5.0.0"]

# ── Tool Configuration ────────────────────────────────────────────────────────

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
    "pytest-docker>=3.1.0",
    "ruff>=0.4.0",
    "mypy>=1.9.0",
    "bandit>=1.7.0",
    "pip-audit>=2.7.0",
    "pre-commit>=3.7.0",
]

[tool.ruff]
target-version = "py314"
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "S",   # flake8-bandit (security)
    "B",   # flake8-bugbear
    "A",   # flake8-builtins
    "C4",  # flake8-comprehensions
    "DTZ", # flake8-datetimez (timezone awareness)
    "T20", # flake8-print (no print statements)
    "RUF", # ruff-specific rules
]
ignore = [
    "S101",  # use of assert (OK in tests)
    "S104",  # possible binding to all interfaces
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101", "S106"]  # allow assert and hardcoded passwords in tests

[tool.mypy]
python_version = "3.14"
strict = true
plugins = ["pydantic.mypy"]
exclude = ["alembic/"]

[[tool.mypy.overrides]]
module = ["sqlalchemy.*", "alembic.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src"]
omit = ["src/main.py", "src/config.py", "alembic/*", "tests/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## Version Constraint Strategy

| Operator | Meaning | Use for |
|---|---|---|
| `>=1.0.0` | minimum version | Most runtime deps — allow upgrades |
| `>=1.0.0,<2.0.0` | bounded range | When v2 has breaking changes |
| `==1.0.0` | exact pin | Almost never — too restrictive |
| `~=1.2.3` | compatible release | Patches only (1.2.x) |

**Rule of thumb:** Use `>=X.Y.Z` for runtime deps. Let `uv.lock` handle exact
versions. Only bound the upper version if you've tested that v+1 breaks things.

## Dependency Groups Pattern

Structure dev dependencies logically:

```toml
[tool.uv]
dev-dependencies = [
    # Testing
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    # Code quality
    "ruff>=0.4",
    "mypy>=1.9",
    # Security
    "bandit>=1.7",
    "pip-audit>=2.7",
    # Dev tooling
    "pre-commit>=3.7",
    "httpie>=3.2",    # manual API testing
]
```

## Pre-commit Setup

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-all]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
```

Install: `uv run pre-commit install`

## Migrating from requirements.txt

```bash
# Convert requirements.txt to pyproject.toml
# 1. Create the project
uv init --no-readme

# 2. Import existing requirements
uv add $(cat requirements.txt | grep -v "^#" | tr "\n" " ")

# 3. Import dev requirements
uv add --dev $(cat requirements-dev.txt | grep -v "^#" | tr "\n" " ")

# 4. Generate lock file
uv lock
```

## Troubleshooting Dependency Conflicts

```bash
# See why a package is installed
uv tree | grep <package>

# Check for conflicts
uv lock --check

# Force resolution with a specific constraint
uv add "package>=1.0,<2.0"

# See what uv resolves without installing
uv lock --dry-run
```
