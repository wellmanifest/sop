# CHANGELOG

## [Unreleased]
### Naprawiono
- Przywrócono executable mode (100755) na `.githooks/pre-commit` (ticket-003, PR #3)

### Dodano
- SOP v1 foundation: `wellmanifest.sop/v1` JSON Schema, procedura `sop-new-ticket`, lokalny scanner/diff/patch/sync/verify runtime (ticket-001, PR #1)
- Trzy spec slices: `sop-subactor-repair.yaml` (bounded repair, stop-on-failure), `sop-validator-dispatch.yaml` (exact-head freeze, trusted merge), `sop-cross-sync.yaml` (dry-run default cross-repo sync) (ticket-006, PR #6)
- Architektura i metodologia Dual-LLM benchmarking (`docs/ARCHITECTURE.md`, `docs/DUAL_LLM_BENCHMARKING.md`)
- Testy: validation, worktrees, drift, dry-run/write/verify, stale plans, CLI, managed-path validation, symlink safety, spec slices positive/negative
- Infrastruktura Dual-LLM benchmarking: `tests/dual_llm/` — deterministic oracle, runner (OpenRouter API), blind auditor, 8 fixture manifests, receipt templates, 31 self-tests (ticket-009, PR #9)

### Zmieniono
- Zaktualizowano `spec/sop-procedures.yaml` katalog: wszystkie cztery procedury w `procedures`, puste `pendingDependentSlice` (ticket-008, PR #8)
- Zamknięto ticket-006 jako DONE/DONE; zaktualizowano CHANGELOG i posprzątano 7 starych gałęzi (ticket-007, PR #7)

## [0.1.0] - 2026-08-24
### Dodano
- Utworzenie publicznego repozytorium wellmanifest/sop
- Inicjalizacja dokumentacji bazowej: README.md, TODO.md, VERSION, .gitignore
