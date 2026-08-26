# Ticket 003: Restore executable pre-commit hook mode

- **ID**: ticket-003
- **Owner**: unresolved:human
- **Status**: DONE
- **Workflow state**: DONE
- **Created**: 2026-08-25

## Goal and scope

Restore only the executable Git mode on `.githooks/pre-commit`. Linux CI rejects ticket-001 because the managed hook is committed as non-executable, although its content and pinned digest are correct.

## Acceptance criteria

- [x] AC-01: The hook content and managed SHA-256 remain unchanged.
- [x] AC-02: The Git index records mode `100755` for `.githooks/pre-commit`.
- [x] AC-03: Local governance-check passes with zero errors and warnings; hosted checks are required before trusted merge.
- [x] AC-04: The implementation diff contains only the hook mode change plus ticket evidence after the plan-only commit.

## Participants

- Human participant: unresolved; no `user-*` file was created or changed.
- Agent participant: [ai-devin.md](ai-devin.md)

## Current disposition

Closed as `DONE / DONE` in governance-only transaction ticket-004 based on
integrated main. PR #3 merged at 2026-08-26T09:36:09Z, merge commit
`96480c65a3b45579652c3c4d42bf0fcdacdd212d`.
