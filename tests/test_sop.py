import unittest
import os
import json
from src.sop.models import SOPDocument, ActionType, FailureAction, DriftFinding
from src.sop.validator import SOPValidator
from src.sop.engine import SOPDiffer, SOPPatcher

class TestSOPEngine(unittest.TestCase):
    def test_validator_valid_document(self):
        doc_data = {
            "id": "sop-test-case",
            "title": "Test SOP Document",
            "version": "1.0.0",
            "domain": "test/domain",
            "philosophy": "Autonomia moduluje, Automatyka generuje",
            "steps": [
                {
                    "stepNumber": 1,
                    "name": "Step 1",
                    "instruction": "Do something",
                    "actionType": "deterministic_automation",
                    "command": "echo test"
                }
            ]
        }
        is_valid, errors = SOPValidator.validate_dict(doc_data)
        self.assertTrue(is_valid, f"Expected valid, got errors: {errors}")
        doc = SOPValidator.parse_dict(doc_data)
        self.assertEqual(doc.id, "sop-test-case")
        self.assertEqual(len(doc.steps), 1)
        self.assertEqual(doc.steps[0].action_type, ActionType.DETERMINISTIC_AUTOMATION)

    def test_validator_invalid_document(self):
        doc_data = {
            "id": "INVALID_ID_FORMAT",
            "title": "",
            "steps": []
        }
        is_valid, errors = SOPValidator.validate_dict(doc_data)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(errors), 2)

    def test_differ_summary(self):
        findings = [
            DriftFinding(repo_name="repo1", rule_id="SOP-GOV-001", severity="ERROR", message="Missing gov", remediation_action="Fix"),
            DriftFinding(repo_name="repo2", rule_id="SOP-HOOK-001", severity="WARNING", message="Missing hook", remediation_action="Fix")
        ]
        summary = SOPDiffer.calculate_drift_summary(findings)
        self.assertEqual(summary["total_drifts"], 2)
        self.assertEqual(summary["by_severity"]["ERROR"], 1)
        self.assertEqual(summary["by_severity"]["WARNING"], 1)

if __name__ == "__main__":
    unittest.main()