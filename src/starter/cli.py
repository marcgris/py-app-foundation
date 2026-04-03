"""Command-line interface for the starter overlay."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from importlib import metadata

from starter.config import load_settings
from starter.exceptions import ConfigError
from starter.logging import get_logger, log_context, setup_logging_from_settings

PACKAGE_NAME = "py-app-foundation"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        Configured argument parser for starter CLI commands.
    """
    parser = argparse.ArgumentParser(
        prog="starter",
        description="Py App Foundation starter CLI.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"starter {_get_package_version()}",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    subparsers.add_parser("health", help="Run a lightweight health check.")

    config_parser = subparsers.add_parser("config", help="Configuration commands.")
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    config_subparsers.required = True
    config_subparsers.add_parser("show", help="Print resolved runtime configuration.")

    return parser


def _get_package_version() -> str:
    """Resolve the package version from installed distribution metadata.

    Returns:
        Installed package version or "unknown" when metadata is unavailable.
    """
    try:
        return metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        return "unknown"


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


def _run_config_show_command() -> int:
    """Print resolved runtime settings.

    Returns:
        Process exit code (0 on success).
    """
    settings = load_settings()
    print(json.dumps(settings.to_dict(), sort_keys=True))
    return 0


def _handle_config_error(command_name: str, error: ConfigError) -> int:
    """Print a deterministic config error message to stderr.

    Args:
        command_name: User-facing command identifier.
        error: Underlying configuration exception.

    Returns:
        Non-zero exit code for command failure.
    """
    print(
        f"Configuration error while running '{command_name}': {error.message}.",
        file=sys.stderr,
    )
    return 1


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
            return _handle_config_error("health", exc)

    if parsed_args.command == "config" and parsed_args.config_command == "show":
        try:
            return _run_config_show_command()
        except ConfigError as exc:
            return _handle_config_error("config show", exc)

    parser.print_help()
    return 1


def run() -> None:
    """Console script entrypoint for the starter CLI."""
    raise SystemExit(main())
