import unittest
from pathlib import Path

from src.sop.validator import SCHEMA_ID, SOPValidationError, SOPValidator

ROOT = Path(__file__).resolve().parents[1]
NEW_PROCEDURES = (
    "sop-subactor-repair.yaml",
    "sop-validator-dispatch.yaml",
    "sop-cross-sync.yaml",
)


class TestNewSpecSlices(unittest.TestCase):
    def test_all_new_procedures_validate_and_parse(self):
        for name in NEW_PROCEDURES:
            with self.subTest(name=name):
                data = SOPValidator.load(ROOT / "spec" / name)
                valid, errors = SOPValidator.validate_dict(data)
                self.assertTrue(valid, errors)
                self.assertEqual(SOPValidator.parse_dict(data).schema, SCHEMA_ID)

    def test_subactor_repair_has_stop_on_failure_and_bounded_scope(self):
        data = SOPValidator.load(ROOT / "spec" / "sop-subactor-repair.yaml")
        valid, errors = SOPValidator.validate_dict(data)
        self.assertTrue(valid, errors)
        step_names = [s["name"].lower() for s in data["steps"]]
        self.assertTrue(any("stop on failure" in n for n in step_names))
        self.assertTrue(any("scope" in n for n in step_names))
        self.assertTrue(any("re-delegate" in n for n in step_names))

    def test_validator_dispatch_has_freeze_and_exact_head(self):
        data = SOPValidator.load(ROOT / "spec" / "sop-validator-dispatch.yaml")
        valid, errors = SOPValidator.validate_dict(data)
        self.assertTrue(valid, errors)
        step_names = [s["name"].lower() for s in data["steps"]]
        self.assertTrue(any("freeze" in n for n in step_names))
        self.assertTrue(any("exact-head" in n for n in step_names))
        self.assertTrue(any("confirm merge" in n for n in step_names))

    def test_cross_sync_has_dry_run_default_and_atomic_write(self):
        data = SOPValidator.load(ROOT / "spec" / "sop-cross-sync.yaml")
        valid, errors = SOPValidator.validate_dict(data)
        self.assertTrue(valid, errors)
        step_names = [s["name"].lower() for s in data["steps"]]
        self.assertTrue(any("dry-run" in n for n in step_names))
        self.assertTrue(any("apply" in n for n in step_names))
        self.assertTrue(any("verify" in n for n in step_names))

    def test_procedures_catalog_lists_all_four(self):
        import json
        catalog = json.loads((ROOT / "spec" / "sop-procedures.yaml").read_text(encoding="utf-8"))
        self.assertEqual(catalog["schema"], "wellmanifest.sop/catalog-v1")
        self.assertIn("sop-new-ticket.yaml", catalog["procedures"])
        self.assertIn("sop-subactor-repair.yaml", catalog["procedures"])
        self.assertIn("sop-validator-dispatch.yaml", catalog["procedures"])
        self.assertIn("sop-cross-sync.yaml", catalog["procedures"])
        self.assertEqual(catalog["pendingDependentSlice"], [])

    def test_rejects_missing_required_field(self):
        data = SOPValidator.load(ROOT / "spec" / "sop-subactor-repair.yaml")
        del data["postconditions"]
        valid, errors = SOPValidator.validate_dict(data)
        self.assertFalse(valid)

    def test_rejects_invalid_action_type(self):
        data = SOPValidator.load(ROOT / "spec" / "sop-validator-dispatch.yaml")
        data["steps"][0]["actionType"] = "invalid_action"
        valid, errors = SOPValidator.validate_dict(data)
        self.assertFalse(valid)

    def test_rejects_non_sequential_steps(self):
        data = SOPValidator.load(ROOT / "spec" / "sop-cross-sync.yaml")
        data["steps"][0]["stepNumber"] = 5
        valid, errors = SOPValidator.validate_dict(data)
        self.assertFalse(valid)

    def test_rejects_unknown_top_level_field(self):
        data = SOPValidator.load(ROOT / "spec" / "sop-subactor-repair.yaml")
        data["unexpected_field"] = True
        valid, errors = SOPValidator.validate_dict(data)
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()
