# Ticket 013: Complete installable SOP package and operator documentation

- **ID**: ticket-013
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-31

## Goal and scope

Complete the existing Python distribution as an operator-usable v0.1.0 package.
Expose the `sop` console command, align package metadata with `VERSION` and
`sop.__version__`, and replace the aspirational root README with tested install,
usage, safety-boundary and project-status instructions. Record the user request
to finish SOP today as SESSION_EXECUTION_AUTHORIZATION and the reason for the
single forced allocation: merged ticket-012 remained a stale local activity
projection after protected delivery.

## Acceptance criteria

- [x] AC-01: Package, VERSION and module metadata consistently identify v0.1.0.
- [x] AC-02: Installing the wheel provides both `sop --help` and `python -m sop --help`.
- [x] AC-03: README documents installation, all CLI commands, dry-run/write safety and honest benchmark status.
- [x] AC-04: Wheel build and clean-environment CLI smoke tests pass.
- [ ] AC-05: Governance and the complete unittest suite pass.
- [ ] AC-06: The exact-head PR is approved and merged by validator-agent.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
