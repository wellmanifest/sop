# TODO — wellmanifest/sop

> **Cel nadrzędny**: Automatyczny audyt, propagacja i egzekwowanie procedur operacyjnych (Standard Operating Procedures) w całym ekosystemie repozytoriów (wellmanifest, subactor, semcod, if-uri), eliminacja marnowania tokenów na ręczne poprawki oraz podwójna walidacja modeli LLM (Dual-Model Benchmarking).
>
> **Zasada przewodnia**: *„Autonomia — moduluje, Automatyka — generuje.”*

---

## 1. Dlaczego powstaje ten projekt? (Kontekst i Uzasadnienie)

W dynamicznie rozwijającym się ekosystemie organizacji WellManifest pojawiają się nowe reguły i standardy inżynieryjne (np. bilet z datą w nazwie, obowiązek używania subactora w pierwszej kolejności do usuwania błędów, pre-commit githooki, governance locki).

### Problemy obecnego podejścia:
1. **Marnowanie tokenów i czasu**: Zlecanie modelom LLM ręcznego przepisywania lub dopasowywania plików konfiguracyjnych w dziesiątkach repozytoriów jest powolne, kosztowne i podatne na halucynacje.
2. **Dryf standardów (Governance Drift)**: Repozytoria stworzone wcześniej nie otrzymują automatycznie aktualizacji reguł z wellmanifest/new-project.
3. **Niejednoznaczność instrukcji dla modeli AI**: Modele językowe bez sztywnych procedur krok-po-kroku (SOP) interpretują polecenia niejednolicie.

---

## 2. Moduły do wdrożenia („Co i Po Co”)

### Moduł 1: Standard i Specyfikacja Procedur SOP (spec/, schemas/)
* **Co robimy**:
  - Tworzymy formalną specyfikację Standard Operating Procedure (wellmanifest.sop/v1 w formacie JSON Schema + YAML/DSL).
  - Definiujemy procedury krok-po-kroku: warunki wstępne (preconditions), sekwencja działań, dowody wykonania (evidence receipts), warunki końcowe (postconditions) i fallbacki naprawcze.
* **Po co**:
  - Aby zamienić ogólne opisy zadań na deterministyczne algorytmy postępowania dla modeli LLM i agentów, eliminując niepewność i błędy.

### Moduł 2: Ekosystemowy Skaner i Synchronizator Standardów (src/sop_sync/)
* **Co robimy**:
  - Narzędzie CLI (sop scan, sop diff, sop sync, sop apply), które:
    1. Pobiera / odczytuje najnowsze standardy z wellmanifest/* (np. 
ew-project, policy-dsl, epair-lifecycle, 	icket-lifecycle).
    2. Skanuje wszystkie lokalne repozytoria i organizacje GitHub (wellmanifest, subactor, semcod, if-uri).
    3. Wykrywa rozbieżności (np. brakujące reguły ticketów, przestarzałe pliki agent-hosts, brakujące githooki).
    4. **Automatycznie generuje i aplikuje poprawki** (deterministycznie skryptem, bez udziału LLM).
* **Po co**:
  - Aby wprowadzenie nowej zasady w WellManifest (np. dodanie daty obok nazwy ticketu) było aplikowane do 50 repozytoriów jednym poleceniem w 2 sekundy, bez zużycia ani jednego tokena LLM.

### Moduł 3: Commit Triggery i Zasada Pierwszeństwa Subactora (src/sop_triggers/, .githooks/)
* **Co robimy**:
  - Wdrożenie githooków (pre-commit, commit-msg) oraz integracji z subactor/validator-agent.
  - Egzekwowanie zasady: **Jeśli w projekcie występują wykryte błędy lub niespójności, agent ma bezwzględny zakaz dalszej implementacji dopóki subactor nie naprawi błędów w trybie autonomicznym**.
  - Commit trigger blokuje commity w dowolnym repozytorium, jeśli nie spełnia ono aktualnego standardu wellmanifest/new-project.
* **Po co**:
  - Aby zapewnić twardą bramkę jakości (machine-enforced quality gate) uniemożliwiającą regresję kodu i omijanie procedur.

### Moduł 4: Framework Testów Krzyżowych Dual-LLM (ChatGPT ⟷ Gemini) (docs/, src/benchmarks/)
* **Co robimy**:
  - Środowisko testowe do ewaluacji procedur SOP w pętli dwóch niezależnych modeli:
    - **Faza A**: ChatGPT realizuje zadanie według specyfikacji SOP -> Gemini audytuje każdy krok, weryfikuje logi i zgłasza nieścisłości.
    - **Faza B**: Gemini realizuje projekt według SOP -> ChatGPT weryfikuje wykonanie i wyciąga wnioski.
    - **Faza C**: Refaktoryzacja procedur SOP na podstawie raportów z testów, doprowadzając je do stanu 100% jednoznaczności.
* **Po co**:
  - Aby sprawdzić, jak różne rodziny modeli interpretują procedury SOP i dopracować język wytycznych tak, by model nie miał możliwości popełnienia błędu bez konieczności kosztownego szkolenia (fine-tuningu).

---

## 3. Szczegółowy Plan Działań (Roadmapa)

### Faza 1: Bootstrap & Governance (Status: W TRAKCIE)
- [x] Utworzenie publicznego repozytorium GitHub wellmanifest/sop.
- [x] Inicjalizacja pełnej struktury wellmanifest/new-project (v0.18.6).
- [x] Konfiguracja .governance/manifest.json, manifest.lock.json, equired-checks.json.
- [x] Aktywacja .githooks/pre-commit i utworzenie brancha 	icket/001-sop-bootstrap.
- [x] Utworzenie indeksu project/TICKETS.md oraz project/ticket-001/.
- [ ] Opracowanie wyczerpującej dokumentacji architektonicznej w docs/ARCHITECTURE.md.

### Faza 2: Specyfikacja SOP DSL i Schematów
- [ ] Zdefiniowanie schematu JSON schemas/sop.schema.json dla procedur operacyjnych.
- [ ] Opracowanie formatu DSL/YAML dla procedur SOP w spec/.
- [ ] Zdefiniowanie kanonicznych procedur bazowych:
  - spec/sop-new-ticket.yaml — procedura tworzenia ticketu z datą i bounded intent.
  - spec/sop-subactor-repair.yaml — procedura pierwszeństwa naprawy błędów przez subactora.
  - spec/sop-validator-dispatch.yaml — procedura delegowania weryfikacji do subactor/validator-agent.
  - spec/sop-cross-sync.yaml — procedura audytu i propagacji zmian standardów.

### Faza 3: Silnik Skanowania i Synchronizacji Repozytoriów
- [ ] Implementacja src/sop/scanner.py — inspekcja repozytoriów w organizacji pod kątem reguł WellManifest.
- [ ] Implementacja src/sop/diff_engine.py — kalkulacja różnic (driftu) między stanem faktycznym a wzorcem.
- [ ] Implementacja src/sop/patcher.py — deterministyczne generowanie i aplikowanie zmian w plikach i hookach.
- [ ] Implementacja CLI src/sop/cli.py (sop scan, sop sync --all, sop verify).
- [ ] Testy jednostkowe i integracyjne w 	ests/test_sync.py i 	ests/test_scanner.py.

### Faza 4: Egzekwowanie Commit Triggerów i Integracja z Subactorem
- [ ] Implementacja uniwersalnego instalatora hooków commit-trigger dla organizacji.
- [ ] Konfiguracja reguł wymuszających uruchomienie subactor przy wykrytych anomaliach.
- [ ] Integracja wywołań z subactor/validator-agent do automatycznego sprawdzania PR-ów synchronizacyjnych.

### Faza 5: Dual-Model LLM Benchmarking (ChatGPT ⟷ Gemini)
- [ ] Dokumentacja metodologii w docs/DUAL_LLM_BENCHMARKING.md.
- [ ] Przygotowanie ustandaryzowanego zestawu zadań testowych (benchmark scenarios).
- [ ] Utworzenie promptów i szablonów audytorskich dla modelu-obserwatora.
- [ ] Przeprowadzenie rundy ewaluacji (ChatGPT jako wykonawca, Gemini jako sędzia/audytor).
- [ ] Przeprowadzenie rundy odwrotnej (Gemini jako wykonawca, ChatGPT jako sędzia/audytor).
- [ ] Raport z wnioskami i uaktualnienie specyfikacji SOP o wyeliminowane niejednoznaczności.