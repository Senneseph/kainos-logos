# Action Step 05 — Harness + CI + Phase 0 sign-off (P0.08–P0.10)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

An experiment-runner harness (the "measure, don't argue" mechanism), a CI pipeline,
and the Phase 0 results file that signs off the substrate.

## Prerequisites

- [ ] Steps 01–04 done.

## Background

From now on, every claim is an **experiment** (hypothesis + metric + threshold +
evidence file), never prose. This step builds that machinery and locks the CI gate
that all later phases must keep green.

## Steps

### 1. `src/kainos/harness/runner.py`

```python
@dataclass
class Result:
    name: str; passed: bool; value: float
    evidence: list[Path]; config: dict

class Experiment(Protocol):
    name: str; hypothesis: str; metric: str; threshold: str
    def run(self) -> Result: ...

def run(exp: Experiment) -> Result: ...
```

- `config` always includes `seed`, `commit` (from `git rev-parse --short HEAD` if
  available, else `"unknown"`), and a `dataset_hash` the caller may set.
- CLI (contract per `plan/40-testing/harness.md` — implement all of it):
  `kainos experiment list` (registered names + thresholds),
  `kainos experiment run --name <n>`, `kainos experiment run --all`,
  `kainos experiment run --phase <N>` (all experiments registered for phase N).
  `run` resolves by name from the registry dict `REGISTRY: dict[str, Experiment]`
  (or name prefix `e1.`/`e2.`/`e3.` for `--phase`).

### 2. `src/kainos/harness/report.py`

`render(results: list[Result]) -> str` → markdown table (name / passed / value /
threshold / evidence). `kainos experiment report --out <path>` writes it.

### 3. A dummy experiment

`src/kainos/harness/dummy.py` — `DummyExperiment` whose `run()` returns
`Result(passed=True, value=1.0, ...)`. Register it. `kainos experiment run --name dummy`
must create `results/dummy.md` with the table.

### 4. Wire `make bench` (replaces the step-01 no-op)

`Makefile` target: `bench: ; python -m kainos.harness.runner --all` (so `make bench`
and `kainos experiment run --all` are equivalent). `runner` must be executable as a
module (`__main__` entry) with `--all` / `--name` flags matching the CLI above.

### 5. CI

`.github/workflows/ci.yml`: on push/PR — `pip install -e '.[dev]'`, `pytest -q`,
`make typecheck`, `make lint`. (Any local CI is fine if not GitHub; keep the same
three checks.)

### 6. Phase 0 results + sign-off

Fill in the pre-seeded template `plan/30-phases/phase-0-foundation/results.md` with:
- the claim (substrate is sound + inspectable);
- the dummy-experiment result;
- test counts (`pytest --collect-only -q | tail -1`);
- a mapping of each of the 6 exit criteria (from `phase-0-foundation/README.md`) to a
  concrete artifact path + passing test.

## Verification

```bash
kainos experiment run --name dummy && cat results/dummy.md && pytest -q
```

Expect: dummy result writes `results/dummy.md`; full suite green.

## Done when

- [ ] `kainos experiment run --name dummy` writes `results/dummy.md`
- [ ] `report.render` emits a markdown table
- [ ] CI config exists and runs `pytest` + typecheck + lint
- [ ] `plan/30-phases/phase-0-foundation/results.md` signs off all 6 exit criteria

## Phase 0 is DONE after this step.

Mark step 05 ✅ in `action-steps/README.md`; proceed to `06-regex-ir-emitter.md`.

## If stuck

`plan/40-testing/harness.md`, `plan/30-phases/phase-0-foundation/actions.md` → P0.08–P0.10.
