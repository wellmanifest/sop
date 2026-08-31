# Ticket 014: License and publish SOP v0.1.0 release

- **ID**: ticket-014
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-31

## Goal and scope

Apply the human-selected Apache-2.0 license, declare it in package metadata,
finalize the v0.1.0 changelog, run all deterministic release gates, publish the
exact-head change through validator-agent, then create the authorized final
GitHub Release `v0.1.0`. No package-registry publication and no paid model calls
are in scope.

The human instruction explicitly selected Apache-2.0, rejected paid model calls,
and authorized the GitHub release. `--force-new` was required only because the
merged pre-upgrade ticket-012 lacks a terminal activity receipt.

## Acceptance criteria

- [x] AC-01: Repository and package metadata declare Apache-2.0.
- [x] AC-02: CHANGELOG contains one truthful final v0.1.0 release section dated 2026-08-31.
- [ ] AC-03: Governance, tests, Ruff, wheel build and installed CLI smoke tests pass.
- [ ] AC-04: The exact-head PR is approved and merged by validator-agent.
- [ ] AC-05: Annotated tag and final GitHub Release `v0.1.0` identify the merged release commit.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
