---
name: python-cli-overlay
description: >
  Use when creating, extending, or hardening CLI commands for this starter.
  Covers argparse parser design, command dispatch, exit codes, deterministic
  stderr handling, and command contract tests. Trigger on: "add command",
  "new CLI command", "argparse", "exit code", "stderr", "config show",
  "version flag", "command contract".
---

# Python CLI Overlay Skill

Use this skill for all changes to `src/starter/cli.py` and related CLI tests.

## Required Workflow

1. Update `build_parser()` for command and subcommand registration.
2. Implement command logic in focused helper functions.
3. Preserve deterministic failure behavior:
   - Non-zero exit code on failure
   - Stable stderr message format
4. Add or update tests:
   - `tests/unit/test_cli.py`
   - `tests/integration/test_cli_smoke.py`
5. Run validation gates before commit.

## Command Contract Rules

- Command names and subcommands are treated as public contract.
- Exit code behavior must be explicit and tested.
- Error output must be deterministic and written to stderr.
- Success output should remain concise and stable.
- `starter config show` output is JSON and should keep a stable key shape.

## Prompt Patterns

- "Use python-cli-overlay: add a new <command> with parser wiring and tests."
- "Use python-cli-overlay: harden error handling for <command> and verify exit codes."
- "Use python-cli-overlay: review command contract stability for CLI beta criteria."

## Validation Commands

```bash
uv sync
uv run ruff check .
uv run ruff format . --check
uv run pyright src/
uv run pytest tests/ -v
uv run bandit -r src/
```
