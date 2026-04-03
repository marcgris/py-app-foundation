---
name: observability
description: >
  Use when adding or improving logging, health checks, command telemetry, or
  operational diagnostics in this starter. Covers starter logging bootstrap,
  consistent log events, error-path visibility, and lightweight health probes.
  Trigger on: "add logging", "observability", "health check", "diagnostics",
  "command telemetry", "why did this command fail".
---

# Observability Skill

This repository currently standardizes on `src/starter/logging.py`.
Prefer extending that module and its usage patterns before introducing new
logging frameworks.

## Repository Alignment

- Logging bootstrap: `src/starter/logging.py`
- Settings-driven log level: `src/starter/config.py`
- CLI logging and command context: `src/starter/cli.py`

## Starter Logging Rules

- Use `setup_logging_from_settings()` for command or app startup paths.
- Use `get_logger(__name__)` (or module-specific logger names) for emitters.
- Use structured context via `log_context(...)` for important operations.
- Log outcomes and identifiers, not sensitive values.

## CLI Observability Checklist

- [ ] Each command has at least one success log event where appropriate.
- [ ] Error paths are logged or surfaced with deterministic stderr behavior.
- [ ] Output to stdout remains user-focused; diagnostics stay in logs/stderr.
- [ ] Health command remains lightweight and fast.

## Prompt Patterns

- "Use observability: improve logging context for starter CLI commands."
- "Use observability: add consistent success and failure log events to this command."
- "Use observability: review this change for secret-safe logging output."
