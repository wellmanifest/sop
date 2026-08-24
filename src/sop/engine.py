import os
import re
import sys
import subprocess
from typing import List, Dict, Any, Tuple
from .models import DriftFinding

class SOPDiffer:
    @staticmethod
    def calculate_drift_summary(findings: List[DriftFinding]) -> Dict[str, Any]:
        summary = {
            "total_drifts": len(findings),
            "by_severity": {"ERROR": 0, "WARNING": 0, "INFO": 0},
            "by_rule": {},
            "by_repo": {}
        }
        for f in findings:
            summary["by_severity"][f.severity] = summary["by_severity"].get(f.severity, 0) + 1
            summary["by_rule"][f.rule_id] = summary["by_rule"].get(f.rule_id, 0) + 1
            summary["by_repo"][f.repo_name] = summary["by_repo"].get(f.repo_name, 0) + 1
        return summary

class SOPPatcher:
    """Automatyczny generator i aplikator poprawek bez użycia tokenów LLM."""

    @staticmethod
    def apply_fix(finding: DriftFinding, dry_run: bool = False) -> bool:
        if not finding.auto_fixable or not finding.target_path:
            return False

        target_file = finding.target_path
        if finding.rule_id == "SOP-TICKET-DATE-001" and os.path.isfile(target_file):
            from datetime import date
            today_str = date.today().isoformat()
            if dry_run:
                return True
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                new_lines = []
                date_added = False
                for line in lines:
                    new_lines.append(line)
                    if line.startswith("- **Status**:") and not date_added:
                        new_lines.append(f"- **Created**: {today_str}\n")
                        date_added = True
                with open(target_file, "w", encoding="utf-8", newline="\n") as f:
                    f.writelines(new_lines)
                return True
            except Exception:
                return False

        return False

    @classmethod
    def apply_all(cls, findings: List[DriftFinding], dry_run: bool = False) -> Dict[str, int]:
        applied = 0
        skipped = 0
        for f in findings:
            if cls.apply_fix(f, dry_run=dry_run):
                applied += 1
            else:
                skipped += 1
        return {"applied": applied, "skipped": skipped}

class SubactorPriorityGate:
    """Weryfikuje zasadę pierwszeństwa naprawy błędów przez Subactora."""

    @staticmethod
    def check_clean_state() -> Tuple[bool, List[str]]:
        errors = []
        try:
            res = subprocess.run(
                [sys.executable, ".governance/governance_check.py", "--root", ".", "--manifest", ".governance/manifest.json", "--lock", ".governance/manifest.lock.json", "--stack-profiles", ".governance/stack-profiles.json"],
                capture_output=True,
                text=True
            )
            if res.returncode != 0:
                errors.append("Wykryto niespójność governance. Naruszenie zasady pierwszeństwa Subactora: napraw błędy przed kontynuacją!")
        except Exception as e:
            errors.append(f"Nie udało się uruchomić bramki walidacyjnej: {e}")

        return (len(errors) == 0, errors)