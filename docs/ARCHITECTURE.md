# Architektura wellmanifest/sop

## 1. Wstęp i Filozofia
System **SOP (Standard Operating Procedure)** realizuje zasadę:
> **„Autonomia — moduluje, Automatyka — generuje.”**

Modele LLM (ChatGPT, Gemini, Claude) są wykorzystywane do wysokopoziomowego podejmowania decyzji, zrozumienia kontekstu biznesowego i modulacji przepływu, natomiast powtarzalne modyfikacje kodu, instalacja szablonów, weryfikacja sum kontrolnych i egzekwowanie bramek są delegowane do **deterministycznych skryptów i automatyki**.

`mermaid
graph TD
    A[WellManifest Standardy SSOT] --> B[SOP Skaner / Differ]
    B --> C{Wykryto rozbieżności?}
    C -->|Tak| D[SOP Patcher - Automatyka]
    C -->|Nie| E[Repozytoria Zgodne]
    D --> F[Git Commit Trigger / Hook]
    F --> G[subactor/validator-agent]
    G --> H[Zatwierdzenie i Merge]
`

## 2. Główne Komponenty
1. **Specyfikacja Procedur (spec/, schemas/)**:
   - Definicje procedur operacyjnych w formacie maszynowo-odczytywalnym (JSON Schema / YAML).
   - Zawierają sztywne warunki wejściowe, sekwencje kroków, dowody wykonania i procedury naprawcze w razie błędu.
2. **Silnik Skanowania i Synchronizacji (src/sop/)**:
   - Skaner bada wszystkie repozytoria w organizacji (wellmanifest, subactor, semcod, if-uri).
   - Patcher automatycznie i deterministycznie nanosi poprawki bez użycia tokenów LLM.
3. **Commit Triggery i Subactor Priority Gate**:
   - Githooki oraz reguły wymuszające natychmiastowe zatrzymanie prac i naprawę wykrytych błędów przez subactora w pierwszej kolejności.
4. **Dual-Model Cross-Validation**:
   - Protokół testów krzyżowych, w którym dwa różne modele weryfikują nawzajem swoje zachowanie pod kątem ścisłego przestrzegania procedur SOP.

# Dual-Model LLM Benchmarking (ChatGPT âź· Gemini)

## Cel
Wyeliminowanie niejednoznacznoĹ›ci w procedurach operacyjnych (SOP) oraz zapewnienie, ĹĽe modele LLM wykonujÄ… zadania powtarzalnie i bezbĹ‚Ä™dnie bez koniecznoĹ›ci kosztownego douczania wag modelu (fine-tuningu).

## Procedura Badawcza

### Runda 1: ChatGPT jako Wykonawca, Gemini jako Audytor
1. **Zadanie**: ChatGPT otrzymuje specyfikacjÄ™ procedury (np. spec/sop-new-ticket.yaml) oraz zadanie do zrealizowania.
2. **Obserwacja**: Gemini monitoruje kaĹĽdy wygenerowany krok, modyfikacjÄ™ plikĂłw i logi weryfikacyjne.
3. **Ocena zgodnoĹ›ci**:
   - Czy kolejnoĹ›Ä‡ krokĂłw zostaĹ‚a zachowana?
   - Czy warunki wstÄ™pne i koĹ„cowe zostaĹ‚y speĹ‚nione?
   - Czy w przypadku symulowanego bĹ‚Ä™du wykonawca zastosowaĹ‚ reguĹ‚Ä™ pierwszeĹ„stwa subactora?

### Runda 2: Gemini jako Wykonawca, ChatGPT jako Audytor
1. Zamiana rĂłl i powtĂłrzenie tego samego scenariusza.
2. Zarejestrowanie rĂłĹĽnic w interpretacji tych samych zapisĂłw procedury SOP przez oba modele.

### Runda 3: Synteza WnioskĂłw i Usprawnienie SOP
1. Zestawienie raportĂłw z obu rund.
2. Wykrycie sĹ‚Ăłw-kluczy lub instrukcji powodujÄ…cych bĹ‚Ä™dy lub pomijanie krokĂłw.
3. Doprecyzowanie definicji SOP w spec/.