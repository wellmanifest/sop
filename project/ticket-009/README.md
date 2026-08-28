# Ticket 009: Dual-LLM benchmarking infrastructure

- **ID**: ticket-009
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-28

## Goal and scope

Create the Dual-LLM benchmarking infrastructure defined in
`docs/DUAL_LLM_BENCHMARKING.md`:

1. **8 disposable fixtures** matching the standard scenarios S01-S08
2. **Python runner** (`runner.py`) that calls OpenRouter API for executor
   models (`openai/gpt-chat-latest` and `google/gemini-3.6-flash`)
3. **Blind auditor script** (`auditor.py`) that evaluates executor transcripts
   without seeing the executor identity
4. **Deterministic oracle** (`oracle.py`) that decides file hashes, path
   boundaries, command exit codes, and step order
5. **Receipt templates** (executor and auditor JSON schemas)
6. **Oracle self-tests** verifying the deterministic checks

No actual model runs are executed in this ticket — that is deferred to a
dependent ticket after infrastructure review.

## Acceptance criteria

- [x] AC-01: 8 fixtures exist under `tests/dual_llm/fixtures/` with pinned SHA-256 manifests
- [x] AC-02: `runner.py` can construct executor prompts for all 8 scenarios
- [x] AC-03: `auditor.py` can construct blind auditor prompts for all 8 scenarios
- [x] AC-04: `oracle.py` implements deterministic checks for all 8 scenarios
- [x] AC-05: `python -m unittest tests.dual_llm.test_oracle -v` passes
- [x] AC-06: `./project/governance-check.sh` passes

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-devin.md](ai-devin.md)
