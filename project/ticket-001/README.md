# Ticket 001: SOP v1 Foundation and Local Conformance Runtime

- **ID**: ticket-001
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-08-24

## Goal and scope

Publish the bounded foundation slice: the `wellmanifest.sop/v1` schema and catalog, canonical `sop-new-ticket`, a safe deterministic local scanner/diff/patch/sync/verify runtime, architecture documentation, and reproducible Dual-LLM methodology. Repair, validator-dispatch, and cross-sync procedures are pending a dependent integration slice after ticket-001 merge and closure.

## Acceptance criteria

- [x] AC-01: Managed governance payload is restored byte-for-byte from the index after clean-path preflight; all 51 SHA-256 values match `manifest.lock.json` without changing Git config or the lock.
- [x] AC-02: Closed `wellmanifest.sop/v1` schema, foundation catalog, semantic validator, and canonical `sop-new-ticket` procedure exist.
- [x] AC-03: Local-only scanner/diff/patch/sync/verify CLI is deterministic, dry-run by default, path-safe, network-free, and atomic per file after whole-batch preflight; multi-file writes are not transactional.
- [x] AC-04: Tests cover validation, worktrees, drift, dry-run/write/verify, stale plans, CLI, managed-path validation, and source/target symlink safety.
- [x] AC-05: Architecture and Dual-LLM methodology, scenarios, prompts, receipts, and scoring are documented.
- [x] AC-06: Local governance-check passes: `GOV-PASS` with 0 errors and 0 warnings.

## Deferred work

- Repair, validator-dispatch, and cross-sync canonical procedures are pending a dependent integration ticket after ticket-001 closure.
- Real hook rollout, repair/validator dispatch, and bidirectional model evaluation remain blocked on their external trusted boundaries; no external result is claimed.

## Participants

- Human participant: unresolved; no `user-*` file was created or changed.
- Initial agent participant: [ai-gemini.md](ai-gemini.md)
- Completion subactor: [ai-subactor.md](ai-subactor.md)

## Current disposition

Keep `IN_PROGRESS / PUBLICATION` through exact-head review and trusted merge. Do not create the dependent ticket while ticket-001 still reserves the integration workstream.
