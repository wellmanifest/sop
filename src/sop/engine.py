"""Safe diff, patch, sync, verification, and integration contracts."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from .models import DriftFinding, PatchOperation
from .scanner import has_symlink_component, sha256_file, validate_managed_path


class UnsafePathError(ValueError):
    """Raised when a patch could escape its declared repository root."""


def _safe_target(root: Path, relative_path: str) -> Path:
    try:
        validate_managed_path(relative_path)
    except ValueError as exc:
        raise UnsafePathError(str(exc)) from exc
    unresolved_target = root / relative_path
    if has_symlink_component(unresolved_target):
        raise UnsafePathError(f"Refusing symlink target component: {unresolved_target}")
    target = unresolved_target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise UnsafePathError(f"Path escapes repository: {relative_path}") from exc
    return target


def _prepare_operation(operation: PatchOperation) -> tuple[Path, Path]:
    root = Path(operation.repo_path).resolve()
    unresolved_source = Path(operation.source_path)
    if has_symlink_component(unresolved_source):
        raise UnsafePathError(f"Refusing symlink template source: {unresolved_source}")
    source = unresolved_source.resolve()
    target = _safe_target(root, operation.relative_path)
    if not source.is_file():
        raise FileNotFoundError(f"Invalid template source: {source}")
    if sha256_file(source) != operation.expected_sha256:
        raise ValueError(f"Template changed after patch planning: {source}")
    if target.exists() and (target.is_symlink() or not target.is_file()):
        raise UnsafePathError(f"Refusing non-regular target: {target}")
    return source, target


class SOPDiffer:
    @staticmethod
    def calculate_drift_summary(findings: list[DriftFinding]) -> dict[str, Any]:
        return {
            "total_drifts": len(findings),
            "by_severity": dict(sorted(Counter(item.severity for item in findings).items())),
            "by_rule": dict(sorted(Counter(item.rule_id for item in findings).items())),
            "by_repo": dict(sorted(Counter(item.repo_name for item in findings).items())),
        }

    @staticmethod
    def build_patch(findings: list[DriftFinding]) -> list[PatchOperation]:
        operations = []
        for finding in findings:
            if finding.auto_fixable and finding.source_path and finding.expected_sha256:
                operations.append(
                    PatchOperation(
                        repo_path=finding.repo_path,
                        relative_path=finding.relative_path,
                        source_path=finding.source_path,
                        expected_sha256=finding.expected_sha256,
                    )
                )
        return sorted(operations, key=lambda item: (item.repo_path.casefold(), item.relative_path))


class SOPPatcher:
    """Apply byte-for-byte local templates; dry-run is the mandatory default."""

    @staticmethod
    def _write_prepared(source: Path, target: Path, expected_sha256: str) -> bool:
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected_sha256:
            raise ValueError(f"Template changed during patch application: {source}")
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, target)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)
        return sha256_file(target) == expected_sha256

    @classmethod
    def apply_operation(cls, operation: PatchOperation, *, write: bool = False) -> bool:
        source, target = _prepare_operation(operation)
        if not write:
            return True
        return cls._write_prepared(source, target, operation.expected_sha256)

    @classmethod
    def apply_all(cls, operations: list[PatchOperation], *, write: bool = False) -> dict[str, int]:
        prepared = [(operation, *_prepare_operation(operation)) for operation in operations]
        if not write:
            return {"planned": len(prepared), "skipped": 0}
        applied = sum(
            cls._write_prepared(source, target, operation.expected_sha256)
            for operation, source, target in prepared
        )
        return {"applied": applied, "skipped": len(operations) - applied}

    @staticmethod
    def verify(operations: list[PatchOperation]) -> list[str]:
        errors = []
        for operation in operations:
            target = _safe_target(Path(operation.repo_path), operation.relative_path)
            if not target.is_file() or target.is_symlink():
                errors.append(f"Missing or unsafe target: {target}")
            elif sha256_file(target) != operation.expected_sha256:
                errors.append(f"Checksum mismatch: {target}")
        return errors


class SubactorPriorityGate:
    """Local-only preflight. It never starts a subprocess outside the repository gate."""

    @staticmethod
    def check_clean_state(root: str | Path = ".") -> tuple[bool, list[str]]:
        root_path = Path(root).resolve()
        command = [
            sys.executable,
            str(root_path / ".governance" / "governance_check.py"),
            "--root",
            str(root_path),
            "--manifest",
            str(root_path / ".governance" / "manifest.json"),
            "--lock",
            str(root_path / ".governance" / "manifest.lock.json"),
            "--stack-profiles",
            str(root_path / ".governance" / "stack-profiles.json"),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return True, []
        return False, [
            "Governance failed; stop implementation and dispatch an authorized repair subactor."
        ]


class IntegrationContract:
    """Render commands only; callers must explicitly execute them at trusted boundaries."""

    @staticmethod
    def hook_install_command(source: str, target: str) -> list[str]:
        return [
            "./scripts/install-agent-hosts.sh",
            "--source",
            source,
            "--target",
            target,
        ]

    @staticmethod
    def subactor_repair_command(ticket: str, error_log: str) -> list[str]:
        return ["python", "-m", "subactor.repair", "--ticket", ticket, "--error-log", error_log]

    @staticmethod
    def validator_dispatch_command(owner: str, repo: str, pr: int, ticket: str) -> list[str]:
        return [
            "./bin/dispatch-direct-pr.sh",
            "--owner",
            owner,
            "--name",
            repo,
            "--pr",
            str(pr),
            "--ticket",
            ticket,
            "--wait-checks",
            "--merge",
            "--watch",
        ]
