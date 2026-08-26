"""Deterministic, local-only repository conformance scanner."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath

from .models import DriftFinding, ScanReport

DEFAULT_MANAGED_PATHS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".githooks/pre-commit",
    ".governance/manifest.json",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_repository(path: Path) -> bool:
    """Accept regular clones and linked worktrees without invoking Git."""
    marker = path / ".git"
    return marker.is_dir() or marker.is_file()


def has_symlink_component(path: Path) -> bool:
    """Inspect an unresolved path and its existing parents without following links."""
    absolute = path.absolute()
    return any(candidate.is_symlink() for candidate in (absolute, *absolute.parents))


def validate_managed_path(value: str) -> str:
    """Return a canonical repository-relative POSIX path or reject it."""
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError(f"Managed path must be canonical and relative: {value!r}")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or path.as_posix() != value
        or any(part in {"", ".", ".."} for part in path.parts)
        or any(part.casefold() == ".git" for part in path.parts)
        or (path.parts and path.parts[0].endswith(":"))
    ):
        raise ValueError(f"Unsafe managed path: {value}")
    return value


def safe_regular_file(root: Path, relative: str) -> Path | None:
    """Return a contained regular file without traversing symlink components."""
    candidate = root / validate_managed_path(relative)
    if has_symlink_component(candidate):
        return None
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


class RepositoryScanner:
    def __init__(
        self,
        root_dir: str | Path,
        standard_root: str | Path | None = None,
        managed_paths: tuple[str, ...] = DEFAULT_MANAGED_PATHS,
    ) -> None:
        self.root_dir = Path(root_dir).resolve()
        self.standard_root = Path(standard_root).absolute() if standard_root else None
        self.managed_paths = tuple(sorted({validate_managed_path(item) for item in managed_paths}))

    def repositories(self) -> list[Path]:
        if is_repository(self.root_dir):
            return [self.root_dir]
        if not self.root_dir.is_dir():
            return []
        repositories = (
            child.resolve()
            for child in self.root_dir.iterdir()
            if child.is_dir() and is_repository(child)
        )
        return sorted(repositories, key=lambda item: item.as_posix().casefold())

    def scan_repository(self, repo_path: str | Path) -> list[DriftFinding]:
        repo = Path(repo_path).resolve()
        if not is_repository(repo):
            return []

        findings: list[DriftFinding] = []
        for relative in self.managed_paths:
            target = safe_regular_file(repo, relative)
            source = (
                safe_regular_file(self.standard_root, relative) if self.standard_root else None
            )
            expected = sha256_file(source) if source else None
            actual = sha256_file(target) if target else None

            if actual is None:
                findings.append(
                    DriftFinding(
                        repo_name=repo.name,
                        repo_path=str(repo),
                        rule_id="SOP-FILE-MISSING",
                        severity="ERROR",
                        message=f"Missing managed file: {relative}",
                        relative_path=relative,
                        source_path=str(source) if source and source.is_file() else None,
                        expected_sha256=expected,
                        auto_fixable=expected is not None,
                    )
                )
            elif expected is not None and actual != expected:
                findings.append(
                    DriftFinding(
                        repo_name=repo.name,
                        repo_path=str(repo),
                        rule_id="SOP-FILE-DRIFT",
                        severity="ERROR",
                        message=f"Managed file differs from standard: {relative}",
                        relative_path=relative,
                        source_path=str(source),
                        expected_sha256=expected,
                        actual_sha256=actual,
                        auto_fixable=True,
                    )
                )
        return findings

    def scan_all(self) -> ScanReport:
        repositories = self.repositories()
        findings = [finding for repo in repositories for finding in self.scan_repository(repo)]
        dirty = {finding.repo_path for finding in findings}
        return ScanReport(
            scanned_repos_count=len(repositories),
            clean_repos_count=len(repositories) - len(dirty),
            findings=findings,
        )
