# TODO — wellmanifest/sop

> **Cel nadrzędny**: automatyczny, lokalny audyt i deterministyczna propagacja procedur operacyjnych w ekosystemie repozytoriów oraz mierzalna walidacja Dual-LLM.
>
> **Zasada przewodnia**: *„Autonomia — moduluje, Automatyka — generuje.”*

## Zakres i granice

Projekt definiuje `wellmanifest.sop/v1` i lokalny runtime conformance. Runtime nie wykonuje dostępu sieciowego, commitów, pushy, PR-ów ani merge. Operacje organizacyjne, prawdziwy dispatch subactora/validator-agent oraz ewaluacje modeli wymagają osobnej autoryzowanej granicy wykonawczej.

## Roadmapa i dowody

### Faza 1: Bootstrap & Governance

- [x] Utworzenie publicznego repozytorium GitHub `wellmanifest/sop` (stan odziedziczony; bez efektu zewnętrznego w tej sesji).
- [x] Inicjalizacja struktury `wellmanifest/new-project` v0.18.6.
- [x] Konfiguracja `.governance/manifest.json`, `manifest.lock.json`, `required-checks.json`.
- [x] Istniejący hook `.githooks/pre-commit` i ticket-001.
- [x] Indeks `project/TICKETS.md` i `project/ticket-001/`.
- [x] Dokumentacja architektoniczna: `docs/ARCHITECTURE.md`.
- [x] Przywrócenie dokładnych bajtów 51 zarządzanych plików z indeksu po weryfikacji czystego statusu; SHA-256 są zgodne z `manifest.lock.json`, bez zmiany Git config lub locka.
- [x] Finalny governance gate dla foundation slice: `GOV-PASS` (0 errors, 0 warnings).

### Faza 2: Specyfikacja SOP DSL i schemat

- [x] Zamknięty JSON Schema `schemas/sop.schema.json` dla `wellmanifest.sop/v1`.
- [x] Format JSON-compatible YAML 1.2 i dependency-free validator w `src/sop/validator.py`.
- [x] `spec/sop-new-ticket.yaml` — alokacja ticketu i bounded intent.
- [x] `spec/sop-subactor-repair.yaml` — bounded repair procedure with stop-on-failure (ticket-006).
- [x] `spec/sop-validator-dispatch.yaml` — exact-head validator dispatch with freeze (ticket-006).
- [x] `spec/sop-cross-sync.yaml` — dry-run default cross-repo sync with atomic write (ticket-006).
- [x] Katalog `spec/sop-procedures.yaml` zaktualizowany: wszystkie cztery procedury w `procedures`, puste `pendingDependentSlice` (ticket-007).

### Faza 3: Lokalny silnik skanowania i synchronizacji

- [x] Deterministyczny scanner regularnych clone/worktree: `src/sop/scanner.py`.
- [x] Stabilny drift summary i plan patcha: `src/sop/engine.py` (`SOPDiffer`).
- [x] Walidacja managed paths, ochrona traversal/`.git`/symlink, batch preflight, plan-bound SHA-256, atomowy zapis per-file i verify (`SOPPatcher`); batch nie jest transakcją wieloplikową.
- [x] CLI `scan`, `diff`, `patch`, `sync`, `verify`, `validate-spec`; `sync` ma domyślny dry-run, zapis wymaga `--write`.
- [x] Brak sieci i zależności runtime; standard musi być lokalną ścieżką.
- [x] Testy kontraktu i integracyjne: `tests/test_sop.py`, `tests/test_sync.py` (foundation suite: 15 testów; dwa symlink tests mogą być pominięte wyłącznie bez uprawnień Windows).

### Faza 4: Commit triggery, subactor i validator

- [x] Local-only command contracts w `src/sop/engine.py`; samo renderowanie nie wykonuje procesów ani efektów sieciowych.
- [x] Kanoniczna reguła stop-on-failure i bounded repair w `spec/sop-subactor-repair.yaml` (ticket-006).
- [ ] **BLOCKED external**: uniwersalna instalacja hooków w organizacjach. Modyfikacje `.githooks/**` są poza allowedPaths, a wykonanie cross-repo wymaga autoryzacji właścicieli.
- [ ] **BLOCKED external**: rzeczywisty dispatch `subactor/repair`; w tej sesji nie uruchamiano zewnętrznego runtime.
- [x] Rzeczywista walidacja PR przez `subactor/validator-agent`: PR #1 (ticket-001) i PR #3 (ticket-003) scalone przez exact-head trusted approval.

### Faza 5: Dual-Model LLM Benchmarking (ChatGPT ↔ Gemini)

- [x] Metodologia i cross-over design: `docs/DUAL_LLM_BENCHMARKING.md`.
- [x] Osiem ustandaryzowanych scenariuszy, deterministic oracle i scoring.
- [x] Prompty wykonawcy/audytora oraz szablony receiptów.
- [x] Infrastruktura benchmarking: `tests/dual_llm/` — oracle, runner, auditor, fixtures, receipt templates (ticket-009, PR #9).
- [x] 31 testów oracle/runner przechodzi; runner używa OpenRouter API (`openai/gpt-chat-latest`, `google/gemini-3.6-flash`) z `OPENROUTER_API_KEY` z `subllm/.env`.
- [ ] **BLOCKED on PR #9 merge**: runda ChatGPT jako wykonawca, Gemini jako audytor — infrastruktura gotowa, oczekuje na merge ticket-009.
- [ ] **BLOCKED on PR #9 merge**: runda Gemini jako wykonawca, ChatGPT jako audytor — infrastruktura gotowa, oczekuje na merge ticket-009.
- [ ] **BLOCKED on rundy**: raport empiryczny i evidence-driven aktualizacja SOP — zależą od obu rzeczywistych rund.
