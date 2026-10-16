# Action Step 04 — Golden files + CLI (P0.06–P0.07)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

Byte-stable golden serialization tests + a `kainos` CLI for codex and IR inspection.

## Prerequisites

- [ ] Step 03 done (`explain`, IR codec, `validate` all work).

## Background

Golden files catch silent schema drift; the CLI gives humans (and later experiments) a
way to inspect the CODEX and IR without writing code — the concrete form of
inspectability (invariant #9).

## Steps

### 1. Golden fixtures + test

- Commit `tests/codex/golden/dump.json` and `tests/ir/golden/minimal.json`
  (already created in step 03) as the reference snapshots.
- `tests/golden/test_golden.py`:
  - build a small store with 2 assertions → `dump()` → compare to `dump.json` (exact
    JSON string equality, sorted keys).
  - `load()` the IR golden → `dump()` → compare to the file.

### 2. `src/kainos/cli.py`

`argparse` with subcommands:

```
kainos codex add  --file assertion.json
kainos codex query --subject S [--relation R] [--status STATUS]
kainos codex explain <id>
kainos codex dump  [--out out.json]
kainos ir validate <file.json>
```

- `codex add` reads a JSON assertion file, `from_dict`s it, adds to a `SqliteCodexStore`
  (default path `data/codex.sqlite`, overridable via `--db`).
- `codex query` prints matching assertions as JSON lines.
- `ir validate` prints `OK` (exit 0) or the schema error (exit 1).
- Add `pyproject.toml` `[project.scripts] kainos = "kainos.cli:main"`.

### 3. Tests

`tests/cli/test_cli.py` (use `subprocess` or `argparse`-in-proc with a tmp `--db`):
- add an assertion via CLI, then `dump`, and assert the assertion appears.
- `kainos ir validate` on the golden IR → exit 0; on `{}` → exit 1.

## Verification

```bash
pytest tests/golden tests/cli -q && kainos ir validate tests/ir/golden/minimal.json
```

Expect: all green; final command prints `OK`.

## Done when

- [ ] golden test compares byte-stable serialization (and fails if a field drifts)
- [ ] `kainos codex add/query/explain/dump` and `kainos ir validate` all work
- [ ] CLI round-trip (add → dump) shows the assertion
- [ ] `pytest tests/golden tests/cli -q` green

## If stuck

`plan/30-phases/phase-0-foundation/actions.md` → P0.06–P0.07.
