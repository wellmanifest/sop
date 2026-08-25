# Ticket 002: Restore executable pre-commit hook mode

- **ID**: ticket-002
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-08-25

## Goal and scope

Restore only the executable Git mode on `.githooks/pre-commit`. Linux CI currently rejects ticket-001 because the managed hook is committed as non-executable, although its content and pinned digest are correct.

## Acceptance criteria

- [x] AC-01: The hook content and managed SHA-256 remain unchanged.
- [x] AC-02: The Git index records mode `100755` for `.githooks/pre-commit`.
- [x] AC-03: Local governance-check passes with zero errors and warnings.
- [x] AC-04: The diff contains only ticket evidence, the ticket index, and the hook mode change.

## Participants

- Human participant: unresolved; no `user-*` file was created or changed.
- Agent participant: [ai-devin.md](ai-devin.md)
