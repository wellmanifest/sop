# wellmanifest/sop

Standard Operating Procedure (SOP) standard, autonomous validation, cross-ecosystem synchronization, and dual-model LLM benchmarking.

## Cel projektu

Projekt **SOP (Standard Operating Procedure)** służy do automatycznego audytu, egzekwowania oraz propagacji standardów WellManifest w poprzek wszystkich repozytoriów i organizacji w ekosystemie (`wellmanifest`, `subactor`, `semcod`, `if-uri`, itp.).

### Kluczowe założenia

1. **Wymuszanie standardów poprzez WellManifest na LLM** — Procedury SOP stanowią jednoznaczne, deterministyczne instrukcje "krok po kroku", eliminujące niepewność i halucynacje modeli.
2. **Automatyczna synchronizacja zmian w ekosystemie** — Gdy pojawia się nowa reguła (np. format nazewnictwa ticketów z datą, wymóg użycia subactora, nowe githooki), narzędzie skanuje repozytoria i automatycznie aplikuje zaktualizowane standardy, nie marnując tokenów i czasu na ręczne poprawki.
3. **Commit Triggers i Bramki Jakości** — Wymuszanie standardów poprzez akcje git commit / githooks / CI oraz integrację z `subactor/validator-agent`.
4. **Zasada Subactora** — Narzucenie priorytetu używania subactora do realizacji bieżących zadań oraz naprawiania w pierwszej kolejności wykrytych błędów w trybie autonomicznym.
5. **Filozofia działania**:
   > *Autonomia — moduluje, Automatyka — generuje.*
6. **Cross-Model Dual Benchmarking (ChatGPT <-> Gemini)**:
   - Testowanie procedur SOP w pętli krzyżowej (jeden model wykonuje procedurę, drugi weryfikuje zgodność i wychwytuje niejednoznaczności, a następnie zamiana ról).

## Struktura projektu

```text
├── docs/             # Architektura, specyfikacje i dokumentacja procedur
├── spec/             # Formalne definicje procedur SOP (DSL / YAML / Markdown)
├── src/              # Narzędzia audytu, synchronizacji i walidacji
├── tests/            # Testy jednostkowe i scenariusze weryfikacji procedur
├── project/          # Śledzenie ticketów i prac zgodnie ze standardem WellManifest
├── AGENTS.md         # Wytyczne dla agentów AI pracujących w repozytorium
├── CONTRIBUTING.md   # Zasady współpracy i governance
└── TODO.md           # Lista zadań i roadmapa
```
