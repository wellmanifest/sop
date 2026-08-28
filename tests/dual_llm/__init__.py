"""Dual-LLM SOP benchmarking infrastructure.

Implements the protocol from docs/DUAL_LLM_BENCHMARKING.md:
- 8 standard scenarios (S01-S08) with disposable fixtures
- Deterministic oracle for file hashes, path boundaries, command exits, step order
- Runner that calls OpenRouter API for executor models
- Blind auditor that evaluates transcripts without executor identity
- Receipt templates for executor and auditor outputs

No model runs are executed by this package; runner/auditor provide the
prompt construction and API call surface for a dependent execution ticket.
"""
