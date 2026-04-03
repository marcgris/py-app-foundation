# Contributing to Py App Foundation

This document explains how humans and agents should work in this repository.

## Core Principles

1. **Planning First**: Before implementing changes, write a brief plan or comment explaining intent
2. **Explicit Guardrails**: Agent behavior is guided by `.copilot-instructions.md` and `.instructions.md`
3. **Tests Come First**: Every public API must have test coverage
4. **Validation Always Passes**: No exception—PRs must pass all local checks before review
5. **Small Changes**: Keep logical changes small and focused
6. **Incremental Copilot Adoption**: Introduce Copilot capabilities in phases and only standardize what proves valuable

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

### Copilot Adoption Workflow (Incremental)

Use this sequence when applying Copilot capabilities to new work:

1. **Plan First**: Capture scope, constraints, risks, and test strategy before coding.
2. **Implement Minimally**: Prefer smallest safe change with clear tests.
3. **Run Quality Gates**: Ruff, format, pyright, pytest, and bandit must pass.
4. **Run AI-Assisted Review**: Perform architecture/test/security review prompts before release or merge.
5. **Promote Proven Patterns**: Move successful workflows from plan docs into standard project docs.

When these patterns are fully embedded in contributor/release/overlay docs, the temporary adoption plan in roadmap documents can be retired.

Source of this adoption workflow: the Copilot capability reference documented in `docs/plan/ROADMAP.md` under "Copilot Capability Adoption Plan" and "Source Reference".

### Enabled Copilot Capabilities (Phase A)

The base template currently enables a quality-focused subset only:

1. Skills:
   - `.github/skills/dependency-management/`
   - `.github/skills/python-cli-overlay/`
   - `.github/skills/python-testing/`
   - `.github/skills/python-refactor/`
   - `.github/skills/security-audit/`
   - `.github/skills/observability/`
2. Agent:
   - `.github/agents/code-reviewer.agent.md`

Scope note:

- These capabilities are intended for base-template quality workflows.
- Overlay-specific skills (for API, worker, UI, etc.) remain deferred until overlay implementation phases.

### Copilot Invocation Cookbook (Phase A)

Use these prompts directly in Agent mode for consistent results:

1. dependency-management
   - "Use dependency-management: add <package> as a runtime dependency and update pyproject/lock safely."
   - "Use dependency-management: explain version constraint options for <package> and recommend one for this repo."
2. python-testing
   - "Use python-testing: add meaningful tests for <file> covering happy path, edge cases, and failure modes."
   - "Use python-testing: review existing tests in <file> and identify missing assertions or scenarios."
3. python-cli-overlay
   - "Use python-cli-overlay: add a new CLI command with parser wiring, deterministic error handling, and tests."
   - "Use python-cli-overlay: verify command contract stability for exit codes, stderr, and output schema."
4. python-refactor
   - "Use python-refactor: refactor <file> to reduce coupling while preserving behavior and tests."
   - "Use python-refactor: identify top code smells in <file> and apply smallest safe improvements first."
5. security-audit
   - "Use security-audit: perform a structured OWASP-focused review of <file/folder> with severity-ranked findings."
   - "Use security-audit: verify no secrets/logging leaks and check injection risks in <file>."
6. observability
   - "Use observability: improve logging and diagnostics for <command/module> using starter logging patterns."
   - "Use observability: review this change for secret-safe logs and useful operational signals."
7. code-reviewer agent
   - "@code-reviewer review <file or PR diff> for architecture violations, type safety gaps, regression risk, and missing tests."

Expected output for reviews:

1. Findings ordered by severity (must-fix first)
2. Concrete remediation guidance with file-level references
3. Explicit statement when no material findings are present

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

### Extending The CLI Overlay

The CLI overlay lives in `src/starter/cli.py` and currently includes:

1. `starter health`
2. `starter config show`
3. `starter --version`

When adding CLI commands, follow this workflow:

1. Register parser changes in `build_parser()`.
2. Implement command logic in a dedicated helper function.
3. Ensure configuration failures return deterministic stderr output and non-zero exit codes.
4. Add unit tests in `tests/unit/test_cli.py`.
5. Add or update smoke tests in `tests/integration/test_cli_smoke.py`.
6. Run full validation before commit:
   ```bash
   uv sync
   uv run ruff check .
   uv run ruff format . --check
   uv run pyright src/
   uv run pytest tests/ -v
   uv run bandit -r src/
   ```

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
3. Run AI-assisted review checks for architecture, testing, and security
4. Merge to `main`
5. Create annotated tag `vX.Y.Z`
6. Publish GitHub release notes from changelog entries

## Questions?

- **Design Questions**: See [ARCHITECTURE.md](../plan/ARCHITECTURE.md) and [DECISIONS.md](../plan/DECISIONS.md)
- **Roadmap Questions**: See [ROADMAP.md](../plan/ROADMAP.md)
- **Code Questions**: Add a comment to the relevant file or issue

Thank you for contributing!
