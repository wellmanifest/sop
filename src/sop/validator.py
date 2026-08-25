"""Dependency-free semantic validator for wellmanifest.sop/v1."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import ActionType, FailureAction, OnFailurePolicy, SOPDocument, SOPStep

SCHEMA_ID = "wellmanifest.sop/v1"
_ID = re.compile(r"^sop-[a-z0-9]+(?:-[a-z0-9]+)*$")
_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
_TOP_LEVEL = {
    "schema",
    "id",
    "title",
    "version",
    "domain",
    "philosophy",
    "preconditions",
    "roles",
    "steps",
    "postconditions",
}
_STEP_FIELDS = {
    "stepNumber",
    "name",
    "instruction",
    "actionType",
    "command",
    "requiredEvidence",
    "postconditions",
    "onFailure",
}


class SOPValidationError(ValueError):
    pass


def _strings(value: Any, name: str, errors: list[str], *, nonempty: bool = False) -> None:
    if not isinstance(value, list) or (nonempty and not value):
        errors.append(f"'{name}' must be {'a non-empty ' if nonempty else 'a '}list of strings")
    elif any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"'{name}' entries must be non-empty strings")


class SOPValidator:
    @staticmethod
    def validate_dict(data: dict[str, Any]) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(data, dict):
            return False, ["SOP document must be an object"]
        unknown = sorted(set(data) - _TOP_LEVEL)
        if unknown:
            errors.append(f"Unknown top-level fields: {', '.join(unknown)}")
        for field in _TOP_LEVEL:
            if field not in data:
                errors.append(f"Missing required top-level field: '{field}'")
        if data.get("schema") != SCHEMA_ID:
            errors.append(f"'schema' must equal '{SCHEMA_ID}'")
        if not isinstance(data.get("id"), str) or not _ID.fullmatch(data.get("id", "")):
            errors.append("'id' must match ^sop-[a-z0-9]+(?:-[a-z0-9]+)*$")
        version = data.get("version")
        if not isinstance(version, str) or not _VERSION.fullmatch(version):
            errors.append("'version' must be semantic x.y.z")
        for field in ("title", "domain", "philosophy"):
            if not isinstance(data.get(field), str) or not data.get(field, "").strip():
                errors.append(f"'{field}' must be a non-empty string")
        _strings(data.get("preconditions"), "preconditions", errors, nonempty=True)
        _strings(data.get("postconditions"), "postconditions", errors, nonempty=True)
        roles = data.get("roles")
        if not isinstance(roles, dict) or not roles:
            errors.append("'roles' must be a non-empty string map")
        elif any(
            not isinstance(key, str) or not isinstance(value, str) or not value
            for key, value in roles.items()
        ):
            errors.append("'roles' must contain non-empty string keys and values")

        steps = data.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append("'steps' must be a non-empty list")
        else:
            for index, step in enumerate(steps, 1):
                if not isinstance(step, dict):
                    errors.append(f"Step {index} must be an object")
                    continue
                extra = sorted(set(step) - _STEP_FIELDS)
                if extra:
                    errors.append(f"Step {index} has unknown fields: {', '.join(extra)}")
                if step.get("stepNumber") != index:
                    errors.append(f"Step {index} must have stepNumber {index}")
                for field in ("name", "instruction"):
                    if not isinstance(step.get(field), str) or not step.get(field, "").strip():
                        errors.append(f"Step {index}: '{field}' must be a non-empty string")
                if step.get("actionType") not in {item.value for item in ActionType}:
                    errors.append(f"Step {index}: invalid actionType")
                _strings(
                    step.get("requiredEvidence"),
                    f"steps[{index}].requiredEvidence",
                    errors,
                    nonempty=True,
                )
                _strings(
                    step.get("postconditions"),
                    f"steps[{index}].postconditions",
                    errors,
                    nonempty=True,
                )
                failure = step.get("onFailure")
                if not isinstance(failure, dict) or set(failure) - {"action", "fallbackProcedure"}:
                    errors.append(f"Step {index}: invalid onFailure object")
                elif failure.get("action") not in {item.value for item in FailureAction}:
                    errors.append(f"Step {index}: invalid onFailure action")
        return not errors, errors

    @staticmethod
    def load(path: str | Path) -> dict[str, Any]:
        """Canonical SOP files use JSON syntax, which is also valid YAML 1.2."""
        with Path(path).open(encoding="utf-8") as stream:
            data = json.load(stream)
        if not isinstance(data, dict):
            raise SOPValidationError("SOP document must be an object")
        return data

    @staticmethod
    def parse_dict(data: dict[str, Any]) -> SOPDocument:
        valid, errors = SOPValidator.validate_dict(data)
        if not valid:
            raise SOPValidationError("Invalid SOP document: " + "; ".join(errors))
        steps = []
        for step in data["steps"]:
            failure = step["onFailure"]
            steps.append(
                SOPStep(
                    step_number=step["stepNumber"],
                    name=step["name"],
                    instruction=step["instruction"],
                    action_type=ActionType(step["actionType"]),
                    command=step.get("command"),
                    required_evidence=step["requiredEvidence"],
                    postconditions=step["postconditions"],
                    on_failure=OnFailurePolicy(
                        FailureAction(failure["action"]), failure.get("fallbackProcedure")
                    ),
                )
            )
        return SOPDocument(
            schema=data["schema"],
            id=data["id"],
            title=data["title"],
            version=data["version"],
            domain=data["domain"],
            philosophy=data["philosophy"],
            preconditions=data["preconditions"],
            roles=data["roles"],
            steps=steps,
            postconditions=data["postconditions"],
        )
