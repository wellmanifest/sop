# Ticket 006: SOP subactor-repair, validator-dispatch and cross-sync spec slices

- **ID**: ticket-006
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-27

## Goal and scope

Implement three PENDING dependent SOP spec slices from TODO.md Faza 2:

1. `spec/sop-subactor-repair.yaml` — kanoniczna procedura stop-on-failure i bounded repair
   dla subactor/repair, z deterministycznymi krokami i wymaganym readbackiem.
2. `spec/sop-validator-dispatch.yaml` — procedura dispatch validator-agent dla trusted merge
   approval, z freeze, exact-head binding i brakiem self-approval.
3. `spec/sop-cross-sync.yaml` — procedura cross-repo synchronizacji managed paths,
   z dry-run default, atomowym zapisem per-file i weryfikacją SHA-256.

Każdy spec jest zgodny z `wellmanifest.sop/v1` JSON Schema i jest walidowany przez
`src/sop/validator.py`.

## Acceptance criteria

- [ ] AC-01: `spec/sop-subactor-repair.yaml` jest schema-valid i definiuje stop-on-failure + bounded repair
- [ ] AC-02: `spec/sop-validator-dispatch.yaml` jest schema-valid i definiuje freeze + exact-head dispatch
- [ ] AC-03: `spec/sop-cross-sync.yaml` jest schema-valid i definiuje dry-run default + atomowy zapis
- [ ] AC-04: Pozytywne i negatywne testy dla każdego spec w `tests/test_sop_*_spec.py`
- [ ] AC-05: `python -m pytest tests/ -x` przechodzi
- [ ] AC-06: `./project/governance-check.sh` przechodzi

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-devin.md](ai-devin.md)
