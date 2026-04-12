## Step 0.1: Required Planning and Contributor Docs

Every new project **must** include the following files, copied and adapted from the template root:

- `TEMPLATE_ROADMAP.md` → `docs/plan/ROADMAP.md`
- `TEMPLATE_DECISIONS.md` → `docs/plan/DECISIONS.md`
- `TEMPLATE_CONTRIBUTING.md` → `docs/guide/CONTRIBUTING.md`

Update these files as your project evolves. They are referenced by `.copilot-instructions.md` and are required for agent and contributor workflow clarity.
## Step 0: Required Project Instructions Files

Every new project **must** include a `.copilot-instructions.md` file at the project root. This file sets guardrails and workflow expectations for Copilot agents and contributors. Copy and adapt the template from py-app-foundation, updating project-specific paths as needed.

You must also follow the [agent and skill file placement guide](../../luminara-app/docs/guide/agent-skill-file-placement.md) to ensure `.github/skills/` and `.github/instructions/` are set up for agent discovery.

# New Project Checklist

Use this checklist every time you generate a new project from the Py App Foundation template.

For a visual big-picture flow and explicit cut-and-paste generation commands, use [bootstrap-generation-playbook.md](bootstrap-generation-playbook.md).

## Step 1: Create the Repository

### Option A — GitHub Template (no tooling required)

1. Visit `https://github.com/marcgris/py-app-foundation`.
2. Click `Use this template` → `Create a new repository`.
3. Set the name, visibility, and owner, then create the repo.
4. Clone it locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_PROJECT_NAME.git
   cd YOUR_PROJECT_NAME
   ```

### Option B — Copy Locally

```bash
cp -r path/to/py-app-foundation YOUR_PROJECT_NAME
cd YOUR_PROJECT_NAME
rm -rf .git
git init -b main
```

---

## Step 2: Rename the Package

The core package is named `starter`. Replace it throughout with your project's package name.

1. Rename the source directory:
   ```bash
   mv src/starter src/YOUR_PACKAGE_NAME
   ```

2. Update references in `pyproject.toml`:
   - `name` under `[project]`
   - `version` (reset to `0.1.0`)
   - `authors` under `[project]`
   - `packages` under `[tool.hatch.build.targets.wheel]`:
     ```toml
     packages = ["src/YOUR_PACKAGE_NAME"]
     ```
   - `source` under `[tool.coverage.run]`:
     ```toml
     source = ["src/YOUR_PACKAGE_NAME"]
     ```
   - `known-first-party` under `[tool.ruff.lint.isort]`:
     ```toml
     known-first-party = ["YOUR_PACKAGE_NAME"]
     ```
   - `include` under `[tool.pyright]`:
     ```toml
     include = ["src/YOUR_PACKAGE_NAME", "tests"]
     ```
   - `[tool.pytest.ini_options]` (verify `testpaths` stays `["tests"]`; update `addopts`):
     ```toml
     [tool.pytest.ini_options]
     testpaths = ["tests"]
     addopts = "--cov=src/YOUR_PACKAGE_NAME --cov-report=term-missing --cov-fail-under=80"
     ```

3. Update the project URLs under `[project.urls]`.

4. Update imports inside the renamed package files:
   - `src/YOUR_PACKAGE_NAME/__init__.py`: replace all `from starter.` imports.
   - `src/YOUR_PACKAGE_NAME/config.py`: replace `from starter.exceptions` import.
   - `src/YOUR_PACKAGE_NAME/logging.py`: replace `from starter.config` import.

5. Update test imports across all files under `tests/`:
   - Replace all `from starter.` and `import starter.` references with `YOUR_PACKAGE_NAME`.

---

## Step 3: Update Metadata

In `pyproject.toml`:

```toml
[project]
name = "YOUR_PROJECT_NAME"
version = "0.1.0"
description = "A short description of your project"
authors = [
    { name = "Your Name", email = "your@email.com" }
]

[project.urls]
Repository = "https://github.com/YOUR_USERNAME/YOUR_PROJECT_NAME"
Documentation = "https://github.com/YOUR_USERNAME/YOUR_PROJECT_NAME/tree/main/docs"
Issues = "https://github.com/YOUR_USERNAME/YOUR_PROJECT_NAME/issues"
```

Update `README.md` title and description to reflect the new project.

---

## Step 4: Install Dependencies and Validate

```bash
uv sync
uv run ruff check .
uv run ruff format . --check
uv run pyright src/
uv run pytest tests/
uv run bandit -r src/
```

If `uv run ruff format . --check` fails, run `uv run ruff format .` to apply formatting fixes, then rerun the validation commands.

All checks must pass before you begin development.

---

## Step 5: Apply an Overlay (Optional)

If building a CLI, API, or worker application, apply the relevant overlay on top of the core:

- **CLI Overlay**: Adds entry point and argument handling.
- **API Overlay**: Adds web service structure.
- **Worker Overlay**: Adds job runner pattern.

See the overlay documentation when available. Each overlay passes the same validation gate.

---

## Step 6: First Commit

```bash
git add .
git commit -m "chore: initialise project from py-app-foundation template"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_PROJECT_NAME.git
git push -u origin main
```

---

## Quick Reference: Files to Update

| File | What to Change |
|------|----------------|
| `pyproject.toml` | name, version, authors, URLs, package paths, tool configs |
| `src/starter/__init__.py` | rename directory, update imports |
| `src/starter/config.py` | update imports |
| `src/starter/logging.py` | update imports |
| `tests/**/*.py` | update all `from starter.` imports |
| `README.md` | title, description, badges |
| `CHANGELOG.md` | reset to Unreleased with blank history |
