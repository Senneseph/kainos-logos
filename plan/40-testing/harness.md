# 40 — Harness (experiment-runner contract)

## The contract

```python
class Experiment(Protocol):
    name: str
    hypothesis: str
    metric: str
    threshold: str
    def run(self) -> Result: ...

@dataclass
class Result:
    name: str
    passed: bool
    value: float
    evidence: list[Path]
    config: dict          # seed, commit, dataset hash — for reproducibility
```

- `harness.runner.run(exp)` executes one experiment.
- `harness.report.render(results) -> str` writes `results.md` tables.
- Every result file (`results/<phase>/e*.json`) includes a `config` block so any
  number can be reproduced or audited.

## Rules

1. A phase is **not done** until its experiments run through the harness and their
   `passed` flags are true (or a gated experiment is explicitly recorded
   adopt/reject).
2. Thresholds are committed in the experiment spec *before* running (prevents
   post-hoc goalpost moving).
3. Baselines are part of the experiment, not an afterthought.
4. Evidence = file paths, not prose.

## CLI

```
kainos experiment list
kainos experiment run --name <name>
kainos experiment run --all
kainos experiment run --phase 1
kainos experiment report --phase 1 --out results/phase-1/SUMMARY.md
```
