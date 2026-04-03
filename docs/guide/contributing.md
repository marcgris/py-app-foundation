# Contributing to Py App Foundation

This document explains how humans and agents should work in this repository.

## Core Principles

1. **Planning First**: Before implementing changes, write a brief plan or comment explaining intent
2. **Explicit Guardrails**: Agent behavior is guided by `.copilot-instructions.md` and `.instructions.md`
3. **Tests Come First**: Every public API must have test coverage
4. **Validation Always Passes**: No exception—PRs must pass all local checks before review
5. **Small Changes**: Keep logical changes small and focused

## For Humans: How to Contribute

### Before You Start

1. Read [ROADMAP.md](../plan/ROADMAP.md) to understand the current phase and priorities
2. Check [DECISIONS.md](../plan/DECISIONS.md) for architectural context
3. Claim an issue or create one for your change

### Development Workflow

1. Create a feature branch: `git checkout -b your-feature`
2. Make your changes in the appropriate module or test file
3. Run validation locally:
   ```bash
   uv sync
   uv run ruff check . && uv run ruff format .
   uv run pyright src/
   uv run pytest tests/ -v
   uv run bandit -r src/
   ```
4. Commit with clear messages: `git commit -m "feat: add new feature"`
5. Push and open a PR with a description of what changed and why

### Code Style

- **Naming**: Use clear, searchable names; avoid generic terms like `util` or `helper`
- **Docstrings**: Google style for all public functions
- **Type Hints**: Required everywhere; use `pyright --strict` as the standard
- **Tests**: Unit tests in `tests/unit/`, integration tests in `tests/integration/`
- **Imports**: Keep them organized; let ruff sort them automatically

## For Agents: How to Work in This Repository

### Allowed Operations

- ✅ Read any file under `src/` and `tests/`
- ✅ Create or modify test files
- ✅ Modify implementation files if changes pass all validation
- ✅ Update configuration in `pyproject.toml`
- ✅ Create new utility patterns in `src/starter/`

### Restricted Operations

- ❌ Do not merge pull requests
- ❌ Do not modify CI workflows without human review
- ❌ Do not change `.instructions.md` or `copilot-instructions.md` without approval
- ❌ Do not add dependencies without documenting why

### Agent Workflow

1. **Understand Intent**: Read the issue, planning docs, and relevant code
2. **Propose a Plan**: Comment on the issue with your approach before implementing
3. **Implement with Tests**: Write tests first, then implementation
4. **Validate Locally**: Ensure all checks pass before opening a PR
5. **Self-Review**: Comment on your own PR explaining intent and decisions
6. **Await Human Review**: Do not merge; let humans approve and merge

## Repository Structure

```
src/starter/
├── config.py       # Typed settings pattern
├── logging.py      # Logging bootstrap
└── exceptions.py   # Exception hierarchy

tests/
├── unit/           # Fast isolated tests
└── integration/    # Multi-component tests
```

### Adding New Core Modules

1. Create the module under `src/starter/`
2. Create corresponding tests under `tests/unit/` or `tests/integration/`
3. Update `src/starter/__init__.py` if exporting public APIs
4. Document the pattern in a docstring and in this guide

## CI/CD

- **On every push**: Linting (ruff), type-checking (pyright), tests (pytest)
- **On every push**: Security scanning (bandit, pip-audit)
- **On PR merge**: Documentation build (currently manual)

All checks must pass before a PR can be merged. There are no exceptions.

## Release Workflow

Releases are versioned with Semantic Versioning and tracked in CHANGELOG.md.

Use [release-checklist.md](release-checklist.md) for the complete release procedure.

The release cadence follows this pattern:

1. Open a release prep PR with version bump and changelog updates
2. Verify local validation and green CI
3. Merge to `main`
4. Create annotated tag `vX.Y.Z`
5. Publish GitHub release notes from changelog entries

## Questions?

- **Design Questions**: See [ARCHITECTURE.md](../plan/ARCHITECTURE.md) and [DECISIONS.md](../plan/DECISIONS.md)
- **Roadmap Questions**: See [ROADMAP.md](../plan/ROADMAP.md)
- **Code Questions**: Add a comment to the relevant file or issue

Thank you for contributing!
