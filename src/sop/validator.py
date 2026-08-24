import json
import os
import re
from typing import Dict, Any, List, Tuple
from .models import SOPDocument, SOPStep, ActionType, FailureAction, OnFailurePolicy

class SOPValidationError(Exception):
    pass

class SOPValidator:
    @staticmethod
    def validate_dict(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        required_fields = ["id", "title", "version", "domain", "steps"]
        for f in required_fields:
            if f not in data or not data[f]:
                errors.append(f"Missing required top-level field: '{f}'")

        if "id" in data and not re.match(r"^sop-[a-z0-9-]+$", str(data["id"])):
            errors.append(f"Invalid ID format: '{data.get('id')}'. Must match ^sop-[a-z0-9-]+$")

        if "steps" in data:
            if not isinstance(data["steps"], list) or len(data["steps"]) == 0:
                errors.append("Field 'steps' must be a non-empty list.")
            else:
                for idx, step in enumerate(data["steps"]):
                    step_num = step.get("stepNumber", idx + 1)
                    if "name" not in step or not step["name"]:
                        errors.append(f"Step {step_num}: Missing 'name'")
                    if "instruction" not in step or not step["instruction"]:
                        errors.append(f"Step {step_num}: Missing 'instruction'")
                    if "actionType" not in step:
                        errors.append(f"Step {step_num}: Missing 'actionType'")
                    elif step["actionType"] not in [a.value for a in ActionType]:
                        errors.append(f"Step {step_num}: Invalid actionType '{step['actionType']}'")

        return (len(errors) == 0, errors)

    @staticmethod
    def parse_dict(data: Dict[str, Any]) -> SOPDocument:
        is_valid, errors = SOPValidator.validate_dict(data)
        if not is_valid:
            raise SOPValidationError(f"Invalid SOP document: {'; '.join(errors)}")

        steps = []
        for s in data["steps"]:
            on_failure = None
            if "onFailure" in s and isinstance(s["onFailure"], dict):
                on_failure = OnFailurePolicy(
                    action=FailureAction(s["onFailure"]["action"]),
                    fallback_procedure=s["onFailure"].get("fallbackProcedure")
                )
            steps.append(SOPStep(
                step_number=s.get("stepNumber", len(steps) + 1),
                name=s["name"],
                instruction=s["instruction"],
                action_type=ActionType(s["actionType"]),
                command=s.get("command"),
                required_evidence=s.get("requiredEvidence"),
                postcondition=s.get("postcondition"),
                on_failure=on_failure
            ))

        return SOPDocument(
            id=data["id"],
            title=data["title"],
            version=data["version"],
            domain=data["domain"],
            philosophy=data.get("philosophy", "Autonomia moduluje, Automatyka generuje"),
            preconditions=data.get("preconditions", []),
            roles=data.get("roles", {}),
            steps=steps
        )