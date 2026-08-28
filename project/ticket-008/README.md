# Ticket 008: Fix sop-procedures.yaml catalog

- **ID**: ticket-008
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-28

## Goal and scope

Fix the `spec/sop-procedures.yaml` catalog gap left by ticket-006. ticket-006
(PR #6) added three new SOP spec slices but its `intent.json` `allowedPaths`
did not include `spec/sop-procedures.yaml`, so the catalog was never updated.
The three specs remain in `pendingDependentSlice` instead of `procedures`.

This ticket moves them to `procedures` and clears `pendingDependentSlice`.

## Acceptance criteria

- [ ] AC-01: `spec/sop-procedures.yaml` lists all four procedures in `procedures`
- [ ] AC-02: `spec/sop-procedures.yaml` `pendingDependentSlice` is empty
- [ ] AC-03: `./project/governance-check.sh` passes

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-devin.md](ai-devin.md)
