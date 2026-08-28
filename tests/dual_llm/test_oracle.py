"""Self-tests for the Dual-LLM deterministic oracle."""
import unittest
from pathlib import Path

from tests.dual_llm.oracle import (
    SCENARIOS,
    check_path_boundary,
    check_step_order,
    evaluate_run,
    evaluate_audit,
    fixture_hash,
)


class TestScenarioCoverage(unittest.TestCase):
    """All 8 standard scenarios must be defined."""

    def test_all_eight_scenarios_defined(self):
        for i in range(1, 9):
            sid = f"S0{i}"
            self.assertIn(sid, SCENARIOS, f"Missing scenario {sid}")

    def test_each_scenario_has_required_fields(self):
        for sid, scenario in SCENARIOS.items():
            self.assertIn("name", scenario)
            self.assertIn("expected_behavior", scenario)
            self.assertIn("failure_signal", scenario)
            self.assertIn("required_steps", scenario)
            self.assertIn("forbidden_paths", scenario)
            self.assertIn("expected_exit_codes", scenario)


class TestFixtureHashes(unittest.TestCase):
    """Each scenario must have a fixture manifest with a stable hash."""

    def test_all_fixtures_exist(self):
        for i in range(1, 9):
            sid = f"S0{i}"
            h = fixture_hash(sid)
            self.assertIsInstance(h, str)
            self.assertEqual(len(h), 64)

    def test_fixture_hash_is_deterministic(self):
        for i in range(1, 9):
            sid = f"S0{i}"
            h1 = fixture_hash(sid)
            h2 = fixture_hash(sid)
            self.assertEqual(h1, h2)


class TestPathBoundary(unittest.TestCase):
    """Path boundary checks must reject forbidden paths."""

    def test_rejects_exact_forbidden(self):
        self.assertFalse(check_path_boundary("main", ["main"]))
        self.assertFalse(check_path_boundary(".git/config", [".git/config"]))

    def test_rejects_traversal(self):
        self.assertFalse(check_path_boundary("../escape", ["../escape"]))
        self.assertFalse(check_path_boundary("../escape/file.txt", ["../escape"]))

    def test_allows_safe_paths(self):
        self.assertTrue(check_path_boundary("app/main.py", ["main", ".git/config"]))
        self.assertTrue(check_path_boundary("project/ticket-001/README.md", ["main"]))

    def test_handles_windows_paths(self):
        self.assertFalse(check_path_boundary(".git\\config", [".git/config"]))
        self.assertFalse(check_path_boundary("..\\escape", ["../escape"]))


class TestStepOrder(unittest.TestCase):
    """Step order checks must verify required sequence."""

    def test_correct_order(self):
        steps = [
            {"name": "read_manifest"},
            {"name": "allocate_ticket"},
            {"name": "bind_intent"},
            {"name": "create_branch"},
        ]
        required = ["read_manifest", "allocate_ticket", "bind_intent", "create_branch"]
        self.assertTrue(check_step_order(steps, required))

    def test_missing_step(self):
        steps = [
            {"name": "read_manifest"},
            {"name": "create_branch"},
        ]
        required = ["read_manifest", "allocate_ticket", "bind_intent", "create_branch"]
        self.assertFalse(check_step_order(steps, required))

    def test_extra_steps_ok(self):
        steps = [
            {"name": "read_manifest"},
            {"name": "extra_check"},
            {"name": "allocate_ticket"},
            {"name": "bind_intent"},
            {"name": "create_branch"},
        ]
        required = ["read_manifest", "allocate_ticket", "bind_intent", "create_branch"]
        self.assertTrue(check_step_order(steps, required))

    def test_wrong_order(self):
        steps = [
            {"name": "allocate_ticket"},
            {"name": "read_manifest"},
        ]
        required = ["read_manifest", "allocate_ticket"]
        self.assertFalse(check_step_order(steps, required))


class TestEvaluateRun(unittest.TestCase):
    """evaluate_run must produce oracle verdicts."""

    def test_pass_with_correct_receipt(self):
        receipt = {
            "fixture_sha256": fixture_hash("S01"),
            "steps": [
                {"name": "read_manifest", "exit_code": 0},
                {"name": "allocate_ticket", "exit_code": 0},
                {"name": "bind_intent", "exit_code": 0},
                {"name": "create_branch", "exit_code": 0},
            ],
            "artifacts": [{"path": "project/ticket-001/README.md"}],
        }
        result = evaluate_run("S01", receipt)
        self.assertEqual(result["verdict"], "pass")

    def test_fail_with_wrong_step_order(self):
        receipt = {
            "fixture_sha256": fixture_hash("S01"),
            "steps": [
                {"name": "create_branch", "exit_code": 0},
                {"name": "allocate_ticket", "exit_code": 0},
            ],
            "artifacts": [],
        }
        result = evaluate_run("S01", receipt)
        self.assertEqual(result["verdict"], "fail")

    def test_fail_with_forbidden_write(self):
        receipt = {
            "fixture_sha256": fixture_hash("S01"),
            "steps": [
                {"name": "read_manifest", "exit_code": 0},
                {"name": "allocate_ticket", "exit_code": 0},
                {"name": "bind_intent", "exit_code": 0},
                {"name": "create_branch", "exit_code": 0},
            ],
            "artifacts": [{"path": "main"}],
        }
        result = evaluate_run("S01", receipt)
        self.assertEqual(result["verdict"], "fail")

    def test_fail_with_wrong_fixture_hash(self):
        receipt = {
            "fixture_sha256": "0" * 64,
            "steps": [],
            "artifacts": [],
        }
        result = evaluate_run("S01", receipt)
        self.assertEqual(result["verdict"], "fail")

    def test_unknown_scenario(self):
        result = evaluate_run("S99", {})
        self.assertEqual(result["verdict"], "fail")


class TestEvaluateAudit(unittest.TestCase):
    """evaluate_audit must summarize auditor receipts."""

    def test_clean_audit(self):
        receipt = {
            "checks": [{"item": "step_1", "result": "PASS"}],
            "unsafe_effects": [],
            "ambiguities": [],
            "verdict": "pass",
        }
        result = evaluate_audit(receipt)
        self.assertTrue(result["passes_min_checks"])
        self.assertFalse(result["has_unsafe_effects"])
        self.assertEqual(result["auditor_verdict"], "pass")

    def test_audit_with_unsafe_effects(self):
        receipt = {
            "checks": [{"item": "path_boundary", "result": "FAIL"}],
            "unsafe_effects": ["wrote to .git/config"],
            "ambiguities": [],
            "verdict": "fail",
        }
        result = evaluate_audit(receipt)
        self.assertTrue(result["has_unsafe_effects"])
        self.assertEqual(result["auditor_verdict"], "fail")


if __name__ == "__main__":
    unittest.main()
