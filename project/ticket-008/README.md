# Ticket 008: Fix sop-procedures.yaml catalog

- **ID**: ticket-008
- **Owner**: unresolved:human
- **Status**: DONE
- **Workflow state**: DONE
- **Created**: 2026-08-28

## Goal and scope

Fix the `spec/sop-procedures.yaml` catalog gap left by ticket-006. ticket-006
(PR #6) added three new SOP spec slices but its `intent.json` `allowedPaths`
did not include `spec/sop-procedures.yaml`, so the catalog was never updated.
The three specs remain in `pendingDependentSlice` instead of `procedures`.

This ticket moves them to `procedures` and clears `pendingDependentSlice`.

## Acceptance criteria

- [x] AC-01: `spec/sop-procedures.yaml` lists all four procedures in `procedures`
- [x] AC-02: `spec/sop-procedures.yaml` `pendingDependentSlice` is empty
- [x] AC-03: `./project/governance-check.sh` passes

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-devin.md](ai-devin.md)
