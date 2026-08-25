# Ticket 003: Restore executable pre-commit hook mode

- **ID**: ticket-003
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-25

## Goal and scope

Restore only the executable Git mode on `.githooks/pre-commit`. Linux CI rejects ticket-001 because the managed hook is committed as non-executable, although its content and pinned digest are correct.

## Acceptance criteria

- [ ] AC-01: The hook content and managed SHA-256 remain unchanged.
- [ ] AC-02: The Git index records mode `100755` for `.githooks/pre-commit`.
- [ ] AC-03: Local and hosted governance checks pass with zero errors and warnings.
- [ ] AC-04: The implementation diff contains only the hook mode change after this plan-only commit.

## Participants

- Human participant: unresolved; no `user-*` file was created or changed.
- Agent participant: [ai-devin.md](ai-devin.md)
