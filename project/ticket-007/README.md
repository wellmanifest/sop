# Ticket 007: Governance closure of ticket-006 and stale branch cleanup

- **ID**: ticket-007
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-28

## Goal and scope

Governance-only closure ticket for ticket-006. ticket-006 (PR #6) was merged
with three new SOP spec slices but was never formally closed as DONE/DONE.
Additionally, `CHANGELOG.md` was not updated with the ticket-006 spec slices
entry, and seven stale local branches from prior merged tickets need cleanup
per AGENTS.md rule 16.

The `sop-procedures.yaml` catalog fix (moving three specs from
`pendingDependentSlice` to `procedures`) is deferred to a separate
integration-workstream ticket, as `spec/**` is owned by the integration
workstream.

## Acceptance criteria

- [ ] AC-01: `project/ticket-006/README.md` status is `DONE` and workflow state is `DONE`
- [ ] AC-02: `./project/governance-check.sh` passes
- [ ] AC-03: `CHANGELOG.md` has an entry for ticket-006 spec slices
- [ ] AC-04: Stale local branches from merged tickets are cleaned up

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-devin.md](ai-devin.md)
