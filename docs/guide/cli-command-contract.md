# CLI Command Contract

This document defines the public command contract for the current CLI overlay.

## Scope

The contract applies to the `starter` entrypoint defined in `pyproject.toml` and implemented in `src/starter/cli.py`.

## Frozen Window

This command contract is frozen for one release cycle starting with `v0.3.0`.

During this freeze window:

- Command names and subcommand names must remain unchanged.
- Existing command success behavior must remain backward compatible.
- Existing error behavior (exit code class and deterministic stderr format) must remain backward compatible.

Any breaking change to this contract must be deferred until the freeze window is complete and must be called out in release notes.

## Stable Command Surface

| Command | Description | Success Exit Code | Success Output | Failure Exit Code | Failure Output |
|---------|-------------|-------------------|----------------|-------------------|----------------|
| `starter health` | Run lightweight health check using current settings | `0` | `ok` on stdout | `1` on configuration failure | `Configuration error while running 'health': <message>.` on stderr |
| `starter config show` | Print resolved runtime settings as JSON | `0` | JSON object on stdout with stable key shape | `1` on configuration failure | `Configuration error while running 'config show': <message>.` on stderr |
| `starter --version` | Print installed package version | `0` | `starter <version>` on stdout | N/A | N/A |

## Argparse Usage Errors

For invalid invocations rejected by the parser, the CLI returns usage error exit code `2`.

Examples:

- Missing required command (for example, `starter`)
- Unknown command (for example, `starter not-a-command`)
- Missing required subcommand (for example, `starter config`)

## Exit Code Matrix

The following process exit codes are part of the public contract:

| Exit Code | Meaning | Representative Cases |
|-----------|---------|----------------------|
| `0` | Command completed successfully | `starter health`, `starter config show`, `starter --version` |
| `1` | Runtime command failure due to invalid configuration | `starter health` with invalid settings, `starter config show` with invalid settings |
| `2` | Parser usage error | Missing command, unknown command, missing required subcommand |

## Deterministic Config-Error Stderr Contract

Configuration failures must emit a deterministic stderr message using this exact template:

`Configuration error while running '<command>': <message>.`

Contract rules:

- Output goes to stderr only.
- stdout must be empty on configuration failure.
- The message prefix and punctuation are stable API surface.
- Exit code is `1` for this failure class.

Current command examples:

- `starter health` failure message:
	`Configuration error while running 'health': Failed to load settings.`
- `starter config show` failure message:
	`Configuration error while running 'config show': Failed to load settings.`

## Enforcement

Contract expectations are enforced by tests in:

- `tests/unit/test_cli.py`
- `tests/integration/test_cli_smoke.py`
