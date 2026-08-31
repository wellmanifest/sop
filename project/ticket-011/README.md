# Ticket 011: Align cross-sync SOP commands with the local CLI

- **ID**: ticket-011
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-31

## Goal and scope

Fix the executable contract mismatch between `spec/sop-cross-sync.yaml` and the
local CLI. Make the installed-module invocation `python -m sop` available,
change the procedure commands to the runtime's canonical `--root` argument and
`sync --write` operation, and make `patch` perform deterministic dry-run
preflight rather than duplicate `diff`. Add contract tests proving that every
command declared by the SOP is accepted by the parser and preserves dry-run
safety.

## Acceptance criteria

- [x] AC-01: `python -m sop` delegates to the local CLI entry point.
- [x] AC-02: Every command in `sop-cross-sync.yaml` uses supported CLI commands and arguments.
- [x] AC-03: `patch` performs full dry-run preflight and never writes.
- [x] AC-04: The explicit write step uses `sync --write`; all other steps remain read-only.
- [x] AC-05: Contract tests parse all five SOP commands and verify patch/write behavior.
- [x] AC-06: `project\\governance-check.bat` and the complete unittest suite pass.
- [ ] AC-07: The exact-head PR is approved and merged by validator-agent.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-devin.md](ai-devin.md)
