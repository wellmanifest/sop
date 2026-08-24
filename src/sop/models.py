from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum

class ActionType(str, Enum):
    DETERMINISTIC_AUTOMATION = "deterministic_automation"
    LLM_MODULATION = "llm_modulation"
    HUMAN_GATE = "human_gate"
    SUBACTOR_REPAIR = "subactor_repair"
    VALIDATION_CHECK = "validation_check"

class FailureAction(str, Enum):
    ABORT = "abort"
    INVOKE_SUBACTOR = "invoke_subactor"
    RETRY = "retry"
    ESCALATE_TO_HUMAN = "escalate_to_human"

@dataclass
class OnFailurePolicy:
    action: FailureAction
    fallback_procedure: Optional[str] = None

@dataclass
class SOPStep:
    step_number: int
    name: str
    instruction: str
    action_type: ActionType
    command: Optional[str] = None
    required_evidence: Optional[str] = None
    postcondition: Optional[str] = None
    on_failure: Optional[OnFailurePolicy] = None

@dataclass
class SOPDocument:
    id: str
    title: str
    version: str
    domain: str
    philosophy: str = "Autonomia moduluje, Automatyka generuje"
    preconditions: List[str] = field(default_factory=list)
    roles: Dict[str, str] = field(default_factory=dict)
    steps: List[SOPStep] = field(default_factory=list)

@dataclass
class DriftFinding:
    repo_name: str
    rule_id: str
    severity: str  # ERROR, WARNING, INFO
    message: str
    remediation_action: str
    target_path: Optional[str] = None
    auto_fixable: bool = True

@dataclass
class ScanReport:
    timestamp: str
    scanned_repos_count: int
    findings: List[DriftFinding] = field(default_factory=list)
    clean_repos_count: int = 0