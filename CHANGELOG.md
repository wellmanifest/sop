# CHANGELOG

## [0.1.0] - 2026-08-31

### Dodano
- Utworzono publiczne repozytorium `wellmanifest/sop` i strukturę governance.
- Dodano zamknięty kontrakt `wellmanifest.sop/v1`, schemat i cztery kanoniczne procedury.
- Dodano dependency-free lokalny runtime scan/diff/patch/sync/verify z dry-run default, jawnym `--write`, atomowym zapisem i weryfikacją SHA-256.
- Dodano ochronę managed paths, traversal, `.git`, symlinków, worktrees i stale planów.
- Dodano architekturę oraz metodologię Dual-LLM benchmarking.
- Dodano manifesty ośmiu scenariuszy, prompt runner/auditor, deterministic oracle, receipt schemas i testy dry-run (ticket-009, PR #9).
- Dodano konsolową komendę `sop`, uruchamianie `python -m sop` i instrukcje operatorskie (ticket-013, PR #13).
- Dodano licencję Apache-2.0 (ticket-014).

### Naprawiono
- Przywrócono executable mode na `.githooks/pre-commit` (ticket-003, PR #3).
- Uzupełniono katalog `spec/sop-procedures.yaml` o wszystkie cztery procedury (ticket-008, PR #8).
- Uzgodniono komendy `sop-cross-sync` z wykonywalnym CLI i zachowano write wyłącznie przez `sync --write` (ticket-011, PR #11).
- Zaktualizowano adoption governance do finalnego `wellmanifest/new-project` v0.19.15 (ticket-012, PR #12).
