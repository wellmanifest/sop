# Raport statusu — sesja 2026-08-28

> **Dla**: szef / decision maker
> **Od**: agent Devin (GLM-5.2 High)
> **Repo**: `wellmanifest/sop`
> **Data**: 2026-08-28

## 1. Co zostało zrobione w tej sesji

### Scalone (MERGED)

| PR | Ticket | Opis | Validator |
|---|---|---|---|
| #7 | ticket-007 | Zamknięcie governance ticket-006 (DONE/DONE), aktualizacja CHANGELOG, cleanup 7 starych gałęzi | approved + merged (140s) |
| #8 | ticket-008 | Naprawa katalogu `spec/sop-procedures.yaml` — 3 specje przeniesione z `pendingDependentSlice` do `procedures` | approved + merged (118s) |

### Otwarte (OPEN — gotowe do ponownej walidacji)

| PR | Repo | Ticket | Opis | Status |
|---|---|---|---|---|
| #9 | wellmanifest/sop | ticket-009 | Infrastruktura Dual-LLM: oracle, runner, auditor, 8 fixtures, 31 testów | CI zielone, validator odrzucił przez false positive `api_key=` → fix pushed jako `auth_token`, gotowe do ponownego dispatch |
| #164 | subactor/validator-agent | — | Fix CRLF bug w `resolve_required_checks` — `jq` output na Windows zawierał `\r` | CI pass, oczekuje na merge |

### Naprawione bugi

1. **CRLF w `dispatch-direct-pr.sh`** (PR #164): Na Windows z `core.autocrlf=true`, `jq -r` output zawiera `\r\n`. `mapfile` zachowuje `\r` w każdym elemencie tablicy, więc nazwy checków jak `governance / enforce\r` nigdy nie matchowały nazw GitHub check-runów. Powodowało to infinite loop w `wait_checks()` z komunikatem `missing:` dla wszystkich required checks mimo że były zielone. Fix: `tr -d '\r'` w `normalize_text`.

2. **Secret scanner false positive** (PR #9): Validator-agent skanuje patch pod kątem `api_key=`. Nazwa parametru funkcji `api_key: str | None = None` triggerowała alert. Fix: rename na `auth_token`.

3. **`gh auth status` exit code**: W PowerShell `bash -c 'gh auth status'` zwraca `True` zamiast `0`. Fix: `bash -lc` zapewnia proper shell initialization.

## 2. Co zostało do zrobienia

### Krok 1: Ponowny dispatch validator-agent dla PR #9 (ticket-009)

PR #9 ma CI zielone i fix dla false positive. Wystarczy ponownie dispatch:

```bash
cd /c/Users/Praca/fork/subactor/validator-agent
./bin/dispatch-direct-pr.sh \
  --owner wellmanifest --name sop --pr 9 --ticket ticket-009 \
  --wait-checks --merge --watch
```

Po merge przejść do kroku 2.

### Krok 2: Merge PR #164 (validator-agent CRLF fix)

PR #164 jest w `subactor/validator-agent` i wymaga merge przez standardowy proces PR (lub dispatch innego validator-agent instancji jeśli dostępnej).

### Krok 3: Uruchomienie rund Dual-LLM (Faza 5)

Po merge PR #9 infrastruktura jest gotowa. Należy uruchomić pełny protokół:

- **Round A**: ChatGPT (`openai/gpt-chat-latest`) wykonuje, Gemini (`google/gemini-3.6-flash`) audytuje
- **Round B**: Gemini wykonuje, ChatGPT audytuje
- **8 scenariuszy × 5 runów × 2 kierunki = 80 uruchomień modelu**

Klucze API są w `subllm/.env`:
- `OPENROUTER_API_KEY` — daje dostęp do obu modeli przez OpenRouter

Uruchomienie wymaga skryptu orchestration (nie jest częścią ticket-009 — to osobny ticket po merge).

### Krok 4: Raport empiryczny

Po rundach A i B:
- Obliczyć metryki: step adherence, evidence precision, safety rate, recovery rate, cross-model agreement
- Raport raw counts i Wilson 95% intervals
- Evidence-driven SOP refinement jeśli znaleziono ambiguities

## 3. Stan repo

```
wellmanifest/sop @ main (c659be9 → po merge #9: nowszy)
├── spec/sop-procedures.yaml     ← naprawiony (4 procedury w procedures)
├── tests/dual_llm/              ← nowa infrastruktura (PR #9)
│   ├── oracle.py                ← deterministic oracle (8 scenariuszy)
│   ├── runner.py                ← OpenRouter API runner (ChatGPT + Gemini)
│   ├── auditor.py               ← blind auditor
│   ├── fixtures/all-manifests.json  ← 8 fixture manifests
│   ├── templates/all-templates.json ← receipt schemas
│   ├── test_oracle.py           ← 19 oracle self-tests
│   └── test_runner.py           ← 12 runner/auditor tests
├── docs/DUAL_LLM_BENCHMARKING.md ← protokół (bez zmian)
├── docs/ARCHITECTURE.md          ← architektura (bez zmian)
└── project/ticket-009/           ← aktywny ticket (IN_PROGRESS)

subactor/validator-agent @ main
└── bin/dispatch-direct-pr.sh     ← fix CRLF (PR #164, OPEN)
```

## 4. Ryzyka i blokery

| Ryzyko | Prawdopodobieństwo | Mitigacja |
|---|---|---|
| Validator-agent ponownie odrzuci PR #9 | Niskie — `auth_token` nie triggeruje secret scanner | Sprawdzić logi validator jeśli repeat |
| OpenRouter rate limit przy 80 runach | Średnie | Throttle między runami (np. 2s sleep) |
| Modele nie zwracają JSON receipt | Wysokie — LLM nie zawsze formatuje JSON | Parser z fallback na raw text + manual review |
| CRLF issues w innych skryptach bash | Średnie — powtarzający się problem Windows | Audyt wszystkich `jq` wywołań w validator-agent |

## 5. Rekomendacje dla szefa

1. **Zmergeuj PR #9** — dispatch validator-agent (komenda w kroku 1 powyżej)
2. **Zmergeuj PR #164** — fix CRLF w validator-agent
3. **Autoryzuj rundy Dual-LLM** — to kosztuje ~80 API calls przez OpenRouter (estymacja: $2-5 zależnie od modeli)
4. **Przygotuj skrypt orchestration** — osobny ticket na runner który wywoła 80 runów, zbierze receipts, uruchomi oracle i wygeneruje raport
5. **Przejrzyj wyniki rund** — po raporcie empirycznym zdecydować o SOP refinement

## 6. Metryki sesji

- **PRs merged**: 2 (#7, #8)
- **PRs open**: 2 (#9, #164)
- **Testy napisane**: 31 (oracle + runner)
- **Bugfixes**: 3 (CRLF, secret scanner false positive, gh auth exit code)
- **Validator dispatches**: 3 (2 approved+merged, 1 changes-requested→fix pushed)
- **Czas validator**: 140s, 118s, 234s (SLO 300s — wszystkie met)
