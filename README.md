# wellmanifest/sop

Portable Standard Operating Procedure contracts and a deterministic local
conformance runtime for the WellManifest ecosystem.

## Release status

The installable package is version 0.1.0 and is licensed under Apache-2.0. This
repository does not claim a PyPI publication; installation currently uses a
verified checkout or locally built wheel.

## Scope

The repository owns:

- the closed `wellmanifest.sop/v1` contract and canonical procedures;
- local repository scanning, deterministic drift plans and safe synchronization;
- dry-run-by-default CLI behavior with explicit write authorization;
- checksums, path-boundary validation and machine-readable receipts;
- a reproducible Dual-LLM benchmarking protocol and test fixtures.

The runtime does not fetch standards, call GitHub, commit, push, open or merge
pull requests, invoke repair services, or run model evaluations. Those effects
belong to separately authorized Subactor boundaries.

## Requirements

- Python 3.11 or newer
- Git repositories or linked worktrees available on the local filesystem
- a local checkout containing the standard files to compare

The runtime has no third-party runtime dependencies.

## Install

From a checkout:

```bash
python -m pip install .
sop --help
```

The equivalent module entry point is:

```bash
python -m sop --help
```

## CLI

Validate a canonical procedure:

```bash
sop validate-spec spec/sop-new-ticket.yaml
```

Scan one repository or the direct child repositories of a local directory:

```bash
sop scan --root /path/to/repos --standard /path/to/standard
```

Render deterministic drift and patch operations:

```bash
sop diff --root /path/to/repos --standard /path/to/standard
```

Preflight the complete patch without writing:

```bash
sop patch --root /path/to/repos --standard /path/to/standard
```

Preview synchronization, which is the default:

```bash
sop sync --root /path/to/repos --standard /path/to/standard
```

Apply a reviewed synchronization plan explicitly:

```bash
sop sync --root /path/to/repos --standard /path/to/standard --write
```

Verify that managed files match the local standard:

```bash
sop verify --root /path/to/repos --standard /path/to/standard
```

Use `--managed-path` repeatedly to replace the default managed-path set. All
commands emit deterministic JSON.

## Safety model

- Network standard URLs are rejected; `--standard` must be a local path.
- Scan, diff, patch and sync without `--write` do not modify target files.
- Managed paths reject absolute paths, traversal, `.git`, backslashes and
  non-canonical segments.
- Symlink sources and target components are rejected.
- A planned operation binds the source SHA-256 and fails if the source changes.
- Every write uses a same-directory temporary file and `os.replace`.
- Each file is verified after replacement; a multi-file batch is not a
  transaction and does not automatically roll back earlier successful writes.

See [Architecture](docs/ARCHITECTURE.md) for the full trust boundary.

## Canonical procedures

- `spec/sop-new-ticket.yaml`
- `spec/sop-subactor-repair.yaml`
- `spec/sop-validator-dispatch.yaml`
- `spec/sop-cross-sync.yaml`

All are indexed by `spec/sop-procedures.yaml` and validated against
`schemas/sop.schema.json`.

## Development verification

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m ruff check src
./project/governance-check.sh
```

On Windows, use `project\governance-check.bat`. Two symlink tests may be skipped
when the current account lacks the Windows symlink privilege.

## Dual-LLM benchmark status

The repository includes the protocol, scenario manifests, prompts, receipt
schemas and deterministic oracle self-tests. It does not yet claim empirical
ChatGPT/Gemini results. Paid or networked runs require an authorized execution
boundary, isolated materialized fixtures, validated receipts and an explicit
budget. See [Dual-LLM benchmarking](docs/DUAL_LLM_BENCHMARKING.md).

## Governance

Changes follow the adopted `wellmanifest/new-project` policy. Allocate tickets
with `project/new-ticket.sh`, work in the canonical ticket worktree, run the
managed gate, and publish only through exact-head validator-agent review.

Project status and remaining external work are tracked in [TODO](TODO.md).
