"""Typed records shared by the local SOP synchronization runtime."""

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class ActionType(StrEnum):
    DETERMINISTIC_AUTOMATION = "deterministic_automation"
    LLM_MODULATION = "llm_modulation"
    HUMAN_GATE = "human_gate"
    SUBACTOR_REPAIR = "subactor_repair"
    VALIDATION_CHECK = "validation_check"


class FailureAction(StrEnum):
    ABORT = "abort"
    INVOKE_SUBACTOR = "invoke_subactor"
    RETRY = "retry"
    ESCALATE_TO_HUMAN = "escalate_to_human"


@dataclass(frozen=True)
class OnFailurePolicy:
    action: FailureAction
    fallback_procedure: str | None = None


@dataclass(frozen=True)
class SOPStep:
    step_number: int
    name: str
    instruction: str
    action_type: ActionType
    command: str | None = None
    required_evidence: list[str] = field(default_factory=list)
    postconditions: list[str] = field(default_factory=list)
    on_failure: OnFailurePolicy | None = None


@dataclass(frozen=True)
class SOPDocument:
    schema: str
    id: str
    title: str
    version: str
    domain: str
    philosophy: str
    preconditions: list[str]
    roles: dict[str, str]
    steps: list[SOPStep]
    postconditions: list[str]


@dataclass(frozen=True)
class DriftFinding:
    repo_name: str
    repo_path: str
    rule_id: str
    severity: str
    message: str
    relative_path: str
    source_path: str | None = None
    expected_sha256: str | None = None
    actual_sha256: str | None = None
    auto_fixable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PatchOperation:
    repo_path: str
    relative_path: str
    source_path: str
    expected_sha256: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class ScanReport:
    scanned_repos_count: int
    findings: list[DriftFinding] = field(default_factory=list)
    clean_repos_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "scanned_repos_count": self.scanned_repos_count,
            "clean_repos_count": self.clean_repos_count,
            "findings": [finding.to_dict() for finding in self.findings],
        }
