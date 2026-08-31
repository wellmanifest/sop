# Ticket 012: Upgrade adopted governance to new-project v0.19.15

- **ID**: ticket-012
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-31

## Goal and scope

Upgrade the repository's adopted `wellmanifest/new-project` package from
v0.18.6 to the final published v0.19.15 revision
`efdb30aec5985d49cbf19bb18012524b941ba3ef`. Use the Goal adoption generator
in upgrade mode; do not hand-edit lock-managed files. The upgrade must preserve
SOP source/spec behavior while adopting current ticket lifecycle, diagnostics,
host contracts, and workspace checks.

The human instruction to finish SOP today authorizes the allocator's
`--force-new` option because stale merged tickets 010 and 011 still reserve the
governance and integration workstreams under the old adopted lifecycle.

## Acceptance criteria

- [ ] AC-01: The adoption lock identifies new-project v0.19.15 at the exact published SHA.
- [ ] AC-02: Every managed file matches its regenerated lock digest.
- [ ] AC-03: Existing SOP source, specifications and tests are unchanged by the generator.
- [ ] AC-04: The managed governance gate passes after the upgrade.
- [ ] AC-05: The complete SOP unittest suite passes.
- [ ] AC-06: The exact-head PR is approved and merged by validator-agent.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-devin.md](ai-devin.md)
