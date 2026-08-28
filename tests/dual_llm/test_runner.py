"""Tests for the Dual-LLM runner prompt construction (dry-run only)."""
import unittest

from tests.dual_llm.runner import (
    EXECUTOR_MODELS,
    build_executor_prompt,
    load_fixture,
    run_scenario,
)
from tests.dual_llm.auditor import (
    AUDITOR_MODELS,
    build_auditor_prompt,
    audit_run,
)


class TestExecutorModels(unittest.TestCase):
    def test_chatgpt_model_defined(self):
        self.assertIn("chatgpt", EXECUTOR_MODELS)
        self.assertEqual(EXECUTOR_MODELS["chatgpt"], "openai/gpt-chat-latest")

    def test_gemini_model_defined(self):
        self.assertIn("gemini", EXECUTOR_MODELS)
        self.assertEqual(EXECUTOR_MODELS["gemini"], "google/gemini-3.6-flash")


class TestAuditorModels(unittest.TestCase):
    def test_chatgpt_model_defined(self):
        self.assertIn("chatgpt", AUDITOR_MODELS)

    def test_gemini_model_defined(self):
        self.assertIn("gemini", AUDITOR_MODELS)


class TestBuildExecutorPrompt(unittest.TestCase):
    def test_prompt_contains_required_fields(self):
        prompt = build_executor_prompt(
            experiment_id="exp-001",
            run_id="run-001",
            scenario_id="S01",
            sop_path="spec/sop-new-ticket.yaml",
            sop_sha256="a" * 64,
            task="Allocate a ticket",
        )
        self.assertIn("exp-001", prompt)
        self.assertIn("run-001", prompt)
        self.assertIn("spec/sop-new-ticket.yaml", prompt)
        self.assertIn("a" * 64, prompt)
        self.assertIn("Allocate a ticket", prompt)
        self.assertIn("STEP_START", prompt)
        self.assertIn("STEP_END", prompt)

    def test_prompt_for_all_scenarios(self):
        for i in range(1, 9):
            sid = f"S0{i}"
            prompt = build_executor_prompt(
                experiment_id="exp-001",
                run_id="run-001",
                scenario_id=sid,
                sop_path="spec/sop-new-ticket.yaml",
                sop_sha256="b" * 64,
                task="test task",
            )
            self.assertIn("exp-001", prompt)
            self.assertIn("test task", prompt)


class TestBuildAuditorPrompt(unittest.TestCase):
    def test_prompt_is_blind(self):
        prompt = build_auditor_prompt(
            experiment_id="exp-001",
            scenario_id="S01",
            sop_path="spec/sop-new-ticket.yaml",
            sop_sha256="a" * 64,
            fixture_sha256="b" * 64,
            transcript="STEP_START 1\nSTEP_END 1\n",
        )
        self.assertIn("blind auditor", prompt)
        self.assertIn("exp-001", prompt)
        self.assertNotIn("openai", prompt.lower())
        self.assertNotIn("gemini", prompt.lower())
        self.assertNotIn("chatgpt", prompt.lower())


class TestRunScenarioDryRun(unittest.TestCase):
    def test_dry_run_returns_prompt(self):
        result = run_scenario(
            experiment_id="exp-001",
            run_id="run-001",
            scenario_id="S01",
            executor_model="chatgpt",
            sop_path="spec/sop-new-ticket.yaml",
            sop_sha256="a" * 64,
            task="test",
            dry_run=True,
        )
        self.assertTrue(result["dry_run"])
        self.assertIn("prompt", result)
        self.assertEqual(result["executor_model"], "openai/gpt-chat-latest")

    def test_dry_run_gemini(self):
        result = run_scenario(
            experiment_id="exp-001",
            run_id="run-001",
            scenario_id="S01",
            executor_model="gemini",
            sop_path="spec/sop-new-ticket.yaml",
            sop_sha256="a" * 64,
            task="test",
            dry_run=True,
        )
        self.assertEqual(result["executor_model"], "google/gemini-3.6-flash")

    def test_unknown_model_raises(self):
        with self.assertRaises(ValueError):
            run_scenario(
                experiment_id="exp-001",
                run_id="run-001",
                scenario_id="S01",
                executor_model="unknown",
                sop_path="spec/sop-new-ticket.yaml",
                sop_sha256="a" * 64,
                task="test",
                dry_run=True,
            )


class TestAuditRunDryRun(unittest.TestCase):
    def test_dry_run_returns_prompt(self):
        result = audit_run(
            experiment_id="exp-001",
            run_id="run-001",
            scenario_id="S01",
            auditor_model="gemini",
            sop_path="spec/sop-new-ticket.yaml",
            sop_sha256="a" * 64,
            fixture_sha256="b" * 64,
            transcript="STEP_START 1\n",
            dry_run=True,
        )
        self.assertTrue(result["dry_run"])
        self.assertIn("prompt", result)
        self.assertEqual(result["auditor_model"], "google/gemini-3.6-flash")


class TestLoadFixture(unittest.TestCase):
    def test_load_all_fixtures(self):
        for i in range(1, 9):
            sid = f"S0{i}"
            fixture = load_fixture(sid)
            self.assertEqual(fixture["scenario"], sid)
            self.assertIn("name", fixture)
            self.assertIn("task", fixture)


if __name__ == "__main__":
    unittest.main()
