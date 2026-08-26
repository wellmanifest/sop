import json
import unittest
from pathlib import Path

from src.sop.engine import IntegrationContract, SOPDiffer
from src.sop.models import DriftFinding
from src.sop.validator import SCHEMA_ID, SOPValidationError, SOPValidator

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ("sop-new-ticket.yaml",)


class TestSOPContracts(unittest.TestCase):
    def test_all_canonical_procedures_validate_and_parse(self):
        for name in CANONICAL:
            with self.subTest(name=name):
                data = SOPValidator.load(ROOT / "spec" / name)
                valid, errors = SOPValidator.validate_dict(data)
                self.assertTrue(valid, errors)
                self.assertEqual(SOPValidator.parse_dict(data).schema, SCHEMA_ID)

    def test_rejects_unknown_fields_and_non_sequential_steps(self):
        data = SOPValidator.load(ROOT / "spec" / CANONICAL[0])
        data["unexpected"] = True
        data["steps"][0]["stepNumber"] = 2
        valid, errors = SOPValidator.validate_dict(data)
        self.assertFalse(valid)
        self.assertTrue(any("Unknown" in error for error in errors))
        self.assertTrue(any("stepNumber" in error for error in errors))
        with self.assertRaises(SOPValidationError):
            SOPValidator.parse_dict(data)

    def test_schema_is_json_and_declares_closed_v1_contract(self):
        schema = json.loads((ROOT / "schemas" / "sop.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["schema"]["const"], SCHEMA_ID)

    def test_drift_summary_is_stable(self):
        findings = [
            DriftFinding("b", "/b", "R2", "WARNING", "m", "x"),
            DriftFinding("a", "/a", "R1", "ERROR", "m", "x"),
        ]
        summary = SOPDiffer.calculate_drift_summary(findings)
        self.assertEqual(list(summary["by_repo"]), ["a", "b"])
        self.assertEqual(summary["total_drifts"], 2)

    def test_integrations_render_commands_without_execution(self):
        self.assertEqual(
            IntegrationContract.hook_install_command("standard", "target"),
            [
                "./scripts/install-agent-hosts.sh",
                "--source",
                "standard",
                "--target",
                "target",
            ],
        )
        self.assertEqual(
            IntegrationContract.subactor_repair_command("ticket-001", "failure.log")[-2:],
            ["--error-log", "failure.log"],
        )
        validator = IntegrationContract.validator_dispatch_command("org", "repo", 7, "ticket-001")
        self.assertIn("--wait-checks", validator)
        self.assertIn("--merge", validator)


if __name__ == "__main__":
    unittest.main()
