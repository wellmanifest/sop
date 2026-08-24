# Ticket 001: Bootstrap Standard Operating Procedure (SOP) Standard and Runtime

- **ID**: ticket-001
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-24

## Goal and scope

Define the Standard Operating Procedure (SOP) standard for WellManifest ecosystem, including:
1. Canonical SOP specification format (DSL/schema) for step-by-step procedures.
2. Cross-repository governance and SOP synchronization engine.
3. Git commit triggers & validator-agent integration.
4. Subactor priority rule enforcement for autonomous issue resolution.
5. Dual-LLM benchmarking framework (ChatGPT <-> Gemini cross-validation).

## Acceptance criteria

- [x] AC-01: Full wellmanifest/new-project governance baseline established and locked.
- [x] AC-02: SOP DSL and schema defined in spec/ and schemas/.
- [x] AC-03: SOP scanner and synchronization runtime implemented in src/.
- [x] AC-04: Test suites covering SOP verification and schema validation pass.
- [x] AC-05: Dual-LLM benchmarking guidelines and workflow documented in docs/.
- [x] AC-06: Local governance-check passes with zero errors.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-gemini.md](ai-gemini.md)
