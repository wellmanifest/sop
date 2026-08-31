"""Command-line interface for deterministic, local-only SOP synchronization."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .engine import SOPDiffer, SOPPatcher
from .scanner import DEFAULT_MANAGED_PATHS, RepositoryScanner
from .validator import SOPValidator


def _scanner(args: argparse.Namespace) -> RepositoryScanner:
    managed = tuple(args.managed_path) if args.managed_path else DEFAULT_MANAGED_PATHS
    return RepositoryScanner(args.root, args.standard, managed)


def _dump(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def _add_sync_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".", help="Repository or parent directory to scan")
    parser.add_argument(
        "--standard", help="Local standard/template repository; network URLs are rejected"
    )
    parser.add_argument(
        "--managed-path", action="append", help="Relative managed path (repeatable)"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sop", description="Local WellManifest SOP conformance runtime"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("scan", "Inspect local repositories without modification"),
        ("diff", "Render deterministic drift and patch operations"),
        ("patch", "Preview a deterministic patch plan"),
        ("sync", "Preview synchronization; --write explicitly enables changes"),
        ("verify", "Verify local repositories against a local standard"),
    ):
        command = commands.add_parser(name, help=help_text)
        _add_sync_arguments(command)
        if name == "sync":
            command.add_argument("--write", action="store_true", help="Apply planned local changes")
    validate = commands.add_parser(
        "validate-spec", help="Validate one canonical JSON-compatible YAML SOP"
    )
    validate.add_argument("file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate-spec":
        try:
            data = SOPValidator.load(args.file)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"Unable to read SOP: {exc}", file=sys.stderr)
            return 2
        valid, errors = SOPValidator.validate_dict(data)
        _dump({"file": str(Path(args.file)), "valid": valid, "errors": errors})
        return 0 if valid else 1

    if args.standard and "://" in args.standard:
        print("Network standards are forbidden; provide a local path", file=sys.stderr)
        return 2
    scanner = _scanner(args)
    report = scanner.scan_all()
    operations = SOPDiffer.build_patch(report.findings)

    if args.command == "scan":
        _dump(report.to_dict())
        return 0
    if args.command == "diff":
        _dump(
            {
                "summary": SOPDiffer.calculate_drift_summary(report.findings),
                "operations": [operation.to_dict() for operation in operations],
            }
        )
        return 0
    if args.command == "patch":
        result = SOPPatcher.apply_all(operations)
        _dump(
            {
                "summary": SOPDiffer.calculate_drift_summary(report.findings),
                "operations": [operation.to_dict() for operation in operations],
                "preflight": result,
            }
        )
        return 0
    if args.command == "sync":
        result = SOPPatcher.apply_all(operations, write=args.write)
        _dump({"mode": "write" if args.write else "dry-run", **result})
        return 0

    errors = [finding.message for finding in report.findings]
    _dump({"valid": not errors, "errors": errors})
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
