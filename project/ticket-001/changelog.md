# Ticket 001: Changelog

## 2026-08-24 — initial bootstrap

- Initialized ticket-001 and the inherited new-project governance baseline.
- Added an initial SOP schema, bundled procedures, scanner/runtime, CLI, architecture notes, and unit tests.

## 2026-08-24 — audited completion pass

- Replaced the loose contract with a closed `wellmanifest.sop/v1` schema and matching dependency-free semantic validator.
- Prepared the publishable foundation slice with the SOP v1 schema, catalog, and independently validated `sop-new-ticket` procedure. Repair, validator-dispatch, and cross-sync procedures are deferred to a dependent slice.
- Implemented deterministic local repository discovery, validated managed paths, SHA-256 drift planning, whole-batch preflight, explicit per-file atomic writes, and verification. Multi-file writes remain non-transactional.
- Added `scan`, `diff`, `patch`, `sync`, `verify`, and `validate-spec`; rejected network standard URLs.
- Added traversal, `.git`, source/target symlink, stale-plan, linked-worktree, CLI, schema, and foundation procedure tests.
- Rewrote architecture documentation and added complete Dual-LLM methodology, scenarios, prompts, receipts, scoring, and blocked execution status.
- Added local-only hook/subactor/validator command contracts without performing external effects.
- Corrected corrupted control characters and synchronized TODO/acceptance status to real evidence.
- Restored all 51 managed files byte-for-byte from index payloads after clean-path preflight, verified every SHA-256 against the lock, and obtained final GOV-PASS without changing the lock or persistent Git configuration.
- Narrowed publication to three public paths: schema, catalog, and `sop-new-ticket`; deferred the other three procedures to a dependent slice.
