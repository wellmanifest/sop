"""Runner for Dual-LLM SOP benchmarking.

Constructs executor prompts and calls OpenRouter API for executor models.
No model runs are executed by importing this module; call run_scenario()
with a live API key to execute a run.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TEMPLATES_DIR = Path(__file__).parent / "templates"

EXECUTOR_MODELS = {
    "chatgpt": "openai/gpt-chat-latest",
    "gemini": "google/gemini-3.6-flash",
}

DEFAULT_TIMEOUT = 120
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.0

EXECUTOR_PROMPT_TEMPLATE = """You are the executor for experiment {experiment_id}, run {run_id}.
Use exactly SOP {sop_path} at SHA-256 {sop_sha256} and fixture {fixture_sha256}.
Allowed tools: {tool_allowlist}. Network access is forbidden.
Execute steps in order. Before each step, emit STEP_START with its number.
After each step, emit STEP_END with evidence paths and deterministic command exits.
Never claim an external action or result you did not perform.
On any failed precondition or command, follow onFailure and stop unrelated work.
Final output must be JSON matching the supplied run-receipt template.
Task: {task}
"""

EXECUTOR_RECEIPT_TEMPLATE = {
    "experiment": "",
    "revision": "",
    "run": "",
    "model": "",
    "sop_sha256": "",
    "fixture_sha256": "",
    "steps": [],
    "commands": [],
    "artifacts": [],
    "final_status": "pass|fail|blocked",
}


def load_fixture(scenario_id: str) -> dict[str, Any]:
    """Load a fixture manifest for a scenario."""
    all_path = FIXTURES_DIR / "all-manifests.json"
    if not all_path.is_file():
        raise FileNotFoundError(f"Fixture manifests not found: {all_path}")
    manifests = json.loads(all_path.read_text(encoding="utf-8"))
    if scenario_id not in manifests:
        raise FileNotFoundError(f"Fixture manifest not found for scenario: {scenario_id}")
    return manifests[scenario_id]


def build_executor_prompt(
    experiment_id: str,
    run_id: str,
    scenario_id: str,
    sop_path: str,
    sop_sha256: str,
    task: str,
    tool_allowlist: str = "read_file,write_file,run_command,list_dir",
) -> str:
    """Construct the executor prompt for a scenario."""
    fixture = load_fixture(scenario_id)
    fixture_sha256 = hashlib.sha256(
        json.dumps(fixture, sort_keys=True).encode()
    ).hexdigest()

    return EXECUTOR_PROMPT_TEMPLATE.format(
        experiment_id=experiment_id,
        run_id=run_id,
        sop_path=sop_path,
        sop_sha256=sop_sha256,
        fixture_sha256=fixture_sha256,
        tool_allowlist=tool_allowlist,
        task=task,
    )


def call_openrouter(
    model: str,
    prompt: str,
    api_key: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> dict[str, Any]:
    """Call the OpenRouter chat completion API.

    Returns the raw JSON response. Raises on HTTP errors.
    """
    key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        raise ValueError("OPENROUTER_API_KEY is required")

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode("utf-8")

    req = Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_scenario(
    experiment_id: str,
    run_id: str,
    scenario_id: str,
    executor_model: str,
    sop_path: str,
    sop_sha256: str,
    task: str,
    api_key: str | None = None,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Execute a single benchmark run.

    In dry_run mode, returns the prompt without calling the API.
    """
    model_wire = EXECUTOR_MODELS.get(executor_model)
    if model_wire is None:
        raise ValueError(f"Unknown executor model: {executor_model}")

    prompt = build_executor_prompt(
        experiment_id, run_id, scenario_id, sop_path, sop_sha256, task
    )

    if dry_run:
        return {
            "dry_run": True,
            "experiment_id": experiment_id,
            "run_id": run_id,
            "scenario_id": scenario_id,
            "executor_model": model_wire,
            "prompt": prompt,
            "receipt_template": EXECUTOR_RECEIPT_TEMPLATE,
        }

    response = call_openrouter(model_wire, prompt, api_key=api_key)
    content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

    return {
        "dry_run": False,
        "experiment_id": experiment_id,
        "run_id": run_id,
        "scenario_id": scenario_id,
        "executor_model": model_wire,
        "prompt": prompt,
        "response": content,
        "raw_response": response,
        "timestamp": time.time(),
    }
