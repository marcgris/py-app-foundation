"""Command-line interface for the starter overlay."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from starter.config import load_settings
from starter.exceptions import ConfigError
from starter.logging import get_logger, log_context, setup_logging_from_settings


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        Configured argument parser for starter CLI commands.
    """
    parser = argparse.ArgumentParser(
        prog="starter",
        description="Py App Foundation starter CLI.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    subparsers.add_parser("health", help="Run a lightweight health check.")

    return parser


def _run_health_command() -> int:
    """Run the health check command.

    Returns:
        Process exit code (0 on success).
    """
    settings = load_settings()
    setup_logging_from_settings(settings)

    logger = get_logger("starter.cli")
    logger.info("Health check passed", extra=log_context(app_name=settings.app_name))
    print("ok")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI command dispatch.

    Args:
        argv: Optional command-line arguments excluding executable name.

    Returns:
        Exit code for the executed command.
    """
    parser = build_parser()
    try:
        parsed_args = parser.parse_args(list(argv) if argv is not None else None)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 1

    if parsed_args.command == "health":
        try:
            return _run_health_command()
        except ConfigError as exc:
            print(f"Configuration error: {exc}")
            return 1

    parser.print_help()
    return 1


def run() -> None:
    """Console script entrypoint for the starter CLI."""
    raise SystemExit(main())
