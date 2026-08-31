# Raport statusu — sesja 2026-08-31 (post-release v0.1.0)

> **Dla**: szef / decision maker
> **Od**: agent Devin (GLM-5.2 High)
> **Repo**: `wellmanifest/sop`
> **Data**: 2026-08-31
> **Wersja**: v0.1.0 (opublikowana)

## 0. TL;DR

**`wellmanifest/sop` v0.1.0 jest opublikowane.** Tag `v0.1.0` i GitHub Release są live.
Repozytorium jest w stanie release: czysty `main`, brak otwartych PR-ów, brak śmieci
lokalnych ani zdalnych. Pierwszy kamień milowy MVP (kontrakt + lokalny runtime +
infrastruktura benchmarkowa + licencja) jest domknięty. Pozostałe prace leżą za granicą
tego repozytorium — w `subactor` (runtime wykonawczy) i `semcod/goal` (orchestracja).

Linki publiczne:

- Release: https://github.com/wellmanifest/sop/releases/tag/v0.1.0
- README: https://github.com/wellmanifest/sop/blob/v0.1.0/README.md
- Roadmapa: https://github.com/wellmanifest/sop/blob/v0.1.0/TODO.md
- Changelog: https://github.com/wellmanifest/sop/blob/v0.1.0/CHANGELOG.md
- Architektura: https://github.com/wellmanifest/sop/blob/v0.1.0/docs/ARCHITECTURE.md
- Metodologia Dual-LLM: https://github.com/wellmanifest/sop/blob/v0.1.0/docs/DUAL_LLM_BENCHMARKING.md

## 1. Co zostało zrobione w tej sesji

### Scalone (MERGED)

| PR | Ticket | Opis | Validator |
|---|---|---|---|
| #12 | ticket-012 | Upgrade governance do `wellmanifest/new-project` v0.19.15 — resolucja `GOV-SYNC-001` | approved + merged |
| #13 | ticket-013 | Instalowalny pakiet SOP: `pyproject.toml` build-system, `src/__init__.py`, `src/sop/__main__.py`, wersje, README, smoke wheel | approved + merged |
| #14 | ticket-014 | Licencja Apache-2.0, finalny CHANGELOG v0.1.0, bind `LICENSE` w manifest, release | approved + merged (141s, SLO met) |

### Release

- Annotated tag `v0.1.0` utworzony na merge commit `180677b` i wypchnięty.
- GitHub Release v0.1.0 opublikowany (nie-draft, nie-prerelease): https://github.com/wellmanifest/sop/releases/tag/v0.1.0
- Brak PyPI publication i brak paid-model requests — zgodnie z `intent.json` ticket-014.

### Cleanup (rule 16)

- 3 zintegrowane worktrees usunięte przez `git worktree remove` (ticket-012, 013, 014).
- 3 disposable local branches usunięte; `git worktree prune` wykonane.
- Pozostał tylko czysty checkout `main` na `180677b`.
- Brak otwartych PR-ów. Jedyna gałąź zdalna to `origin/main`.

## 2. Stan repozytorium

```
wellmanifest/sop @ main (180677b) ← v0.1.0
├── .governance/manifest.json      ← new-project v0.19.15
├── AGENTS.md / CLAUDE.md / GEMINI.md / .cursor/rules/new-project-standard.mdc
├── LICENSE                         ← Apache-2.0 (ticket-014)
├── VERSION                         ← 0.1.0
├── pyproject.toml                  ← build-system, version=0.1.0
├── README.md                       ← release status, scope, install, CLI
├── CHANGELOG.md                    ← pełna historia v0.1.0
├── TODO.md                         ← roadmapa 5 faz z dowodami
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DUAL_LLM_BENCHMARKING.md
│   └── SESSION_STATUS_2026-08-31.md  ← ten raport
├── spec/
│   └── sop-procedures.yaml          ← 4 kanoniczne procedury
├── schemas/sop.schema.json          ← wellmanifest.sop/v1
├── src/sop/                         ← runtime: scan/diff/patch/sync/verify
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── scanner.py
│   ├── engine.py
│   ├── validator.py
│   └── patcher.py
├── tests/
│   ├── test_sop.py
│   ├── test_sync.py
│   └── dual_llm/                    ← infrastruktura benchmarkowa (ticket-009)
│       ├── oracle.py                ← deterministic oracle (8 scenariuszy)
│       ├── runner.py                ← OpenRouter API runner
│       ├── auditor.py               ← blind auditor
│       ├── fixtures/all-manifests.json
│       ├── templates/all-templates.json
│       ├── test_oracle.py           ← 19 oracle self-tests
│       └── test_runner.py           ← 12 runner/auditor tests
└── project/
    ├── TICKETS.md
    └── ticket-{001..014}/           ← 14 ticketów, wszystkie DONE
```

## 3. Roadmapa — status faz

| Faza | Status | Dowód |
|------|--------|-------|
| 1. Bootstrap & Governance | ✅ kompletne | `GOV-PASS`, v0.19.15, 14 ticketów domkniętych |
| 2. Specyfikacja SOP DSL i schemat | ✅ kompletne | `schemas/sop.schema.json`, 4 procedury w `spec/sop-procedures.yaml` |
| 3. Lokalny silnik skanowania i synchronizacji | ✅ kompletne | `scan`/`diff`/`patch`/`sync`/`verify`, 15+ testów, dry-run default |
| 4. Commit triggery, subactor i validator | ⚠️ częściowo | Kontrakty gotowe; universal hook install i real `subactor/repair` dispatch = BLOCKED external |
| 5. Dual-Model LLM Benchmarking | ⚠️ infrastruktura gotowa, rundy BLOCKED | 31 testów oracle/runner przechodzi; brak empirycznych rund |

### Co działa teraz (v0.1.0)

- **Lokalny runtime conformance**: `python -m sop scan --root <path>`, `diff`, `patch --write`, `sync --write`, `verify`.
- **Dry-run default**: każdy zapis wymaga jawnego `--write`.
- **Closed contract** `wellmanifest.sop/v1`: schema + 4 procedury (new-ticket, subactor-repair, validator-dispatch, cross-sync).
- **Ochrona managed paths**: traversal, `.git`, symlinks, worktrees, stale plans.
- **Governance v0.19.15**: `governance-check.bat` / `.sh`, pre-commit hook, CI `governance / enforce`.
- **Infrastruktura benchmarkowa**: oracle, runner, auditor, 8 fixtures, receipt templates — gotowe do rund.

### Czego brakuje do "pełnego MVP"

1. **Rzeczywiste rundy Dual-LLM** (Faza 5, BLOCKED on benchmark runtime):
   - Round A: ChatGPT wykonuje, Gemini audytuje.
   - Round B: Gemini wykonaje, ChatGPT audytuje.
   - 8 scenariuszy × 5 runów × 2 kierunki = 80 uruchomień modelu.
   - Wymaga: izolowany wykonawca, materializowane fixtures, walidowane receipty.
   - **To jest praca w `subactor`, nie w `wellmanifest/sop`.**

2. **Universal hook installation** (Faza 4, BLOCKED external):
   - Modyfikacje `.githooks/**` cross-repo wymagają autoryzacji właścicieli organizacji.

3. **Real `subactor/repair` dispatch** (Faza 4, BLOCKED external):
   - W tej sesji nie uruchamiano zewnętrznego runtime repair.

## 4. Metryki sesji

- **PRs merged**: 3 (#12, #13, #14)
- **PRs open**: 0
- **Release**: v0.1.0 (tag + GitHub Release)
- **Testy**: 58 unit tests pass, 2 Windows symlink tests skipped
- **Lint**: `ruff check src` clean
- **Build**: `wellmanifest_sop-0.1.0-py3-none-any.whl` zbudowany (smoke)
- **Validator dispatches**: 3 (wszystkie approved + merged)
- **Czas validator**: 141s dla PR #14 (SLO 300s — met)
- **Worktrees cleaned**: 3 usunięte, 0 pozostałych
- **Lokalne gałęzie non-main**: 0

## 5. Ryzyka i blokery

| Ryzyko | Prawdopodobieństwo | Mitigacja |
|---|---|---|
| OpenRouter rate limit przy 80 runach Dual-LLM | Średnie | Throttle między runami (np. 2s sleep); batchowanie |
| Modele nie zwracają JSON receipt | Wysokie — LLM nie zawsze formatuje JSON | Parser z fallback na raw text + manual review; prompt engineering |
| Brak izolowanego wykonawcy dla rund | Wysokie — to bloker | Osobny ticket w `subactor` na runtime execution boundary |
| Koszt API dla 80 runów | Niskie — estymacja $2-5 | OpenRouter, free-tier modele gdzie możliwe |
| CRLF issues w innych skryptach bash | Średnie — powtarzający się problem Windows | Audyt wszystkich `jq` wywołań w validator-agent (PR #164 już merged) |

## 6. Rekomendacje dla szefa

1. **v0.1.0 jest live** — repozytorium jest w stanie release. Można promować / linkować publicznie.

2. **Następny kamień milowy: rundy Dual-LLM** — to wymaga:
   - Osobnego ticketu w `subactor` na runtime execution boundary (izolowany wykonawca).
   - Materializacji fixtures w tym runtime.
   - Skryptu orchestration: 80 runów → receipts → oracle → raport empiryczny.
   - Autoryzacji budżetu API (~$2-5 przez OpenRouter).

3. **Nie publikuj na PyPI** — `intent.json` ticket-014 wyraźnie tego zabrania. Instalacja przez verified checkout lub local wheel.

4. **Nie używaj paid modeli** — `intent.json` zabrania paid-model requests. Rundy Dual-LLM używają OpenRouter z free-tier modelami.

5. **Po rundach**: evidence-driven SOP refinement jeśli oracle znajdzie ambiguities w procedurach.

## 7. Architektura — gdzie co leży

```
wellmanifest/sop        ← kontrakt + lokalny runtime + metodologia benchmarkowa
  ├── v0.1.0 RELEASED

subactor                ← runtime wykonawczy (repair, validator, subllm, llm-code-benchmark)
  ├── validator-agent   ← zatwierdził PR #14, gotowy do kolejnych
  ├── subllm            ← routing modeli (OpenRouter, Z.AI, Cursor)
  ├── llm-code-benchmark ← kandydat na runtime dla rund Dual-LLM
  └── supervisor        ← orchestration

semcod/goal             ← workspace lifecycle + terminal audit
```

**Granica odpowiedzialności**: `wellmanifest/sop` definiuje *co* mierzyć (kontrakt,
metodologia, oracle, fixtures). `subactor` dostarcza *jak* to wykonać (runtime,
API calls, receipt collection). `semcod/goal` dostarcza *gdzie* to orchestrować
(workspace lifecycle, terminal audit).
