"""Experiment-runner harness (P0.08–P0.09) — the "measure, don't argue" mechanism.

Every claim in the project is an **experiment** (hypothesis + metric + threshold +
evidence file), never prose (plan 40-testing/harness.md):

- `run(exp)` executes one experiment, completes the reproducibility `config` block
  (seed / commit / dataset_hash) and persists `results/<name>.json` (full audit
  record) + `results/<name>.md` (markdown table).
- `REGISTRY` maps registry keys (`e<phase>.<name>`) to registered experiments;
  `kainos experiment run` resolves names exactly or by unique short name, `--phase N`
  selects all `eN.*` keys.
- `python -m kainos.harness.runner --all | --name N | --phase N` is the same runner
  (wired to `make bench`).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable

from kainos.harness.dummy import DummyExperiment
from kainos.harness.report import render
from kainos.q20.bench import (
    E2_1Experiment,
    E2_2Experiment,
    E2_3Experiment,
    E2_4Experiment,
    E2_5Experiment,
)
from kainos.regex.bench import (
    E1_1Experiment,
    E1_2Experiment,
    E1_3Experiment,
    E1_4Experiment,
    E1_5Experiment,
)
from kainos.regex.bench_e31 import E3_1Experiment

# The top-level `benchmarks/` package (experiments, not library code —
# ADR-0007 repo layout) is importable from the package location, not the CWD
# (the D-m4 package-anchored repo-root convention). No-op when the repo root
# is already on sys.path (CWD runs, pytest, `python -m` from the checkout).
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks.phi.bench import E3_5Experiment
from benchmarks.topology.bench import E3_2Experiment
from kainos.exchange.bench import E3_3Experiment
from kainos.game.bench import E5_0Experiment
from kainos.game.e52 import E5_2Experiment
from kainos.game.e53 import E5_3Experiment
from kainos.game.e54 import E5_4Experiment
from kainos.game.shared_grid import E5_1Experiment
from kainos.multimodal.bench import E3_4Experiment
from kainos.projection.bench import E3_6Experiment
from kainos.puzzle.bench import E4_1Experiment
from kainos.tutor.bench import E6_1Experiment
from kainos.tutor.e62 import E6_2Experiment
from kainos.tutor.e64 import E6_4Experiment
from kainos.tutor.e65 import E6_5Experiment
from kainos.tutor.e66 import E6_6Experiment
from kainos.tutor.e67 import E6_7Experiment
from kainos.tutor.e68 import E6_8Experiment
from kainos.tutor.e69 import E6_9Experiment
from kainos.tutor.e610 import E6_10Experiment
from kainos.tutor.e611 import E6_11Experiment
from kainos.tutor.e612 import E6_12Experiment
from kainos.tutor.e613 import E6_13Experiment
from kainos.tutor.e614 import E6_14Experiment
from kainos.tutor.e615 import E6_15Experiment
from kainos.tutor.e616 import E6_16Experiment
from kainos.tutor.e617 import E6_17Experiment
from kainos.tutor.e618 import E6_18Experiment
from kainos.tutor.e619 import E6_19Experiment
from kainos.tutor.e620 import E6_20Experiment
from kainos.tutor.e621 import E6_21Experiment
from kainos.tutor.e622 import E6_22Experiment
from kainos.tutor.e623 import E6_23Experiment
from kainos.tutor.e624 import E6_24Experiment
from kainos.tutor.e625 import E6_25Experiment
from kainos.tutor.e626 import E6_26Experiment
from kainos.tutor.e627 import E6_27Experiment
from kainos.tutor.e635 import E6_35Experiment
from kainos.tutor.e636 import E6_36Experiment
from kainos.tutor.loop import E6_3Experiment
from kainos.workspace.bench import E3_7Experiment

__all__ = [
    "REGISTRY",
    "RESULTS_DIR",
    "Experiment",
    "Result",
    "git_commit",
    "load_results",
    "main",
    "render_listing",
    "resolve",
    "result_to_dict",
    "run",
    "run_experiments",
    "selected",
]

RESULTS_DIR = Path("results")


@dataclass
class Result:
    """Outcome of one experiment run.

    `threshold` is an additive field beyond the plan-40 contract (the report table
    needs it; the contract's five fields are unchanged and in order).
    `skipped` (P3.01): the experiment's precondition was unmet (e.g. the LLM
    backend is unreachable) — reported as SKIP, never as a pass or a genuine
    fail; the exit code is unaffected.
    """

    name: str
    passed: bool
    value: float
    evidence: list[Path] = field(default_factory=list)
    config: dict = field(default_factory=dict)  # seed, commit, dataset_hash — reproducibility
    threshold: str | None = None
    skipped: bool = False


@runtime_checkable
class Experiment(Protocol):
    name: str
    hypothesis: str
    metric: str
    threshold: str

    def run(self) -> Result: ...


# ── registry ────────────────────────────────────────────────────────────────

REGISTRY: dict[str, Experiment] = {
    "e0.dummy": DummyExperiment(),
    "e1.1": E1_1Experiment(),
    "e1.2": E1_2Experiment(),
    "e1.3": E1_3Experiment(),
    "e1.4": E1_4Experiment(),
    "e1.5": E1_5Experiment(),
    "e2.1": E2_1Experiment(),
    "e2.2": E2_2Experiment(),
    "e2.3": E2_3Experiment(),
    "e2.4": E2_4Experiment(),
    "e2.5": E2_5Experiment(),
    "e3.1": E3_1Experiment(),
    "e3.2": E3_2Experiment(),
    "e3.3": E3_3Experiment(),
    "e3.4": E3_4Experiment(),
    "e3.5": E3_5Experiment(),
    "e3.6": E3_6Experiment(),
    "e3.7": E3_7Experiment(),
    "e4.1": E4_1Experiment(),
    "e5.0": E5_0Experiment(),
    "e5.1": E5_1Experiment(),
    "e5.2": E5_2Experiment(),
    "e5.3": E5_3Experiment(),
    "e5.4": E5_4Experiment(),
    "e6.1": E6_1Experiment(),
    "e6.2": E6_2Experiment(),
    "e6.3": E6_3Experiment(),
    "e6.4": E6_4Experiment(),
    "e6.5": E6_5Experiment(),
    "e6.6": E6_6Experiment(),
    "e6.7": E6_7Experiment(),
    "e6.8": E6_8Experiment(),
    "e6.9": E6_9Experiment(),
    "e6.10": E6_10Experiment(),
    "e6.11": E6_11Experiment(),
    "e6.12": E6_12Experiment(),
    "e6.13": E6_13Experiment(),
    "e6.14": E6_14Experiment(),
    "e6.15": E6_15Experiment(),
    "e6.16": E6_16Experiment(),
    "e6.17": E6_17Experiment(),
    "e6.18": E6_18Experiment(),
    "e6.19": E6_19Experiment(),
    "e6.20": E6_20Experiment(),
    "e6.21": E6_21Experiment(),
    "e6.22": E6_22Experiment(),
    "e6.23": E6_23Experiment(),
    "e6.24": E6_24Experiment(),
    "e6.25": E6_25Experiment(),
    "e6.26": E6_26Experiment(),
    "e6.27": E6_27Experiment(),
    "e6.35": E6_35Experiment(),
    "e6.36": E6_36Experiment(),
}


def resolve(name: str) -> Experiment:
    """Resolve by exact registry key or unique short name (key after the last '.')."""

    if name in REGISTRY:
        return REGISTRY[name]
    candidates = sorted(k for k in REGISTRY if k.split(".", 1)[-1] == name)
    if len(candidates) == 1:
        return REGISTRY[candidates[0]]
    if not candidates:
        raise LookupError(f"unknown experiment {name!r}; registered: {', '.join(sorted(REGISTRY))}")
    raise LookupError(f"ambiguous experiment {name!r}: {', '.join(candidates)}")


def selected(name: str | None = None, all: bool = False, phase: int | None = None) -> list[Experiment]:
    """The experiments a run command selected (exactly one of name / all / phase)."""

    if all:
        return [REGISTRY[k] for k in sorted(REGISTRY)]
    if name is not None:
        return [resolve(name)]
    if phase is not None:
        prefix = f"e{phase}."
        keys = sorted(k for k in REGISTRY if k.startswith(prefix))
        if not keys:
            phases = sorted({k[: k.index(".")] for k in REGISTRY if "." in k})
            raise LookupError(f"no experiments registered for phase {phase} (phases: {', '.join(phases)})")
        return [REGISTRY[k] for k in keys]
    raise LookupError("nothing selected — use --name, --all, or --phase")


# ── execution + persistence ─────────────────────────────────────────────────


def git_commit() -> str:
    """Short commit of the working tree: `KAINOS_GIT_COMMIT` (injected by the Makefile,
    so in-container runs still carry the host's commit) > `git rev-parse` > "unknown"."""

    env = os.environ.get("KAINOS_GIT_COMMIT")
    if env:
        return env
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=False
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except (OSError, FileNotFoundError):
        pass
    return "unknown"


def result_to_dict(result: Result, exp: Experiment | None = None) -> dict:
    d = {
        "name": result.name,
        "passed": result.passed,
        "value": result.value,
        "threshold": result.threshold,
        "evidence": [str(p) for p in result.evidence],
        "config": result.config,
        "skipped": result.skipped,
    }
    if exp is not None:
        d["hypothesis"] = exp.hypothesis
        d["metric"] = exp.metric
    return d


def run(exp: Experiment, out_dir: Path = RESULTS_DIR) -> Result:
    """Execute one experiment; complete its reproducibility config; persist JSON + md."""

    result = exp.run()
    config = dict(result.config)
    config.setdefault("seed", 0)
    config.setdefault("dataset_hash", None)
    config["commit"] = git_commit()
    result.config = config
    if result.threshold is None:
        result.threshold = exp.threshold
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{result.name}.json").write_text(
        json.dumps(result_to_dict(result, exp), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out_dir / f"{result.name}.md").write_text(render([result]) + "\n", encoding="utf-8")
    return result


def run_experiments(exps: Sequence[Experiment], out_dir: Path = RESULTS_DIR) -> tuple[list[Result], int]:
    results: list[Result] = []
    rc = 0
    print(f"running {len(exps)} experiment(s) [commit {git_commit()}]")
    for exp in exps:
        r = run(exp, out_dir)
        results.append(r)
        if r.skipped:
            reason = r.config.get("skip_reason", "precondition unmet")
            print(f"SKIP  {r.name}: {reason} — {out_dir / (r.name + '.md')}")
            continue
        mark = "PASS" if r.passed else "FAIL"
        print(f"{mark}  {r.name}: {r.value} (threshold: {r.threshold}) — {out_dir / (r.name + '.md')}")
        rc = rc or (0 if r.passed else 1)
    return results, rc


def load_results(out_dir: Path = RESULTS_DIR, phase: int | None = None) -> list[dict]:
    """Persisted result JSONs (flat and `phase-*/` subdirs), optionally filtered to a phase
    via the `e<phase>.` registry-key prefix."""

    files = sorted(out_dir.glob("*.json")) + sorted(out_dir.glob("phase-*/*.json"))
    allowed = None
    if phase is not None:
        allowed = {key for key in REGISTRY if key.startswith(f"e{phase}.")}
    out = []
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        # A result record has a fixed shape; this skips non-result JSON in the
        # same directory (e.g. evidence artifacts). ``value`` is part of the
        # persisted contract (Result) — full experiment reports that merely
        # share name/passed/config must not be mistaken for result records.
        if not isinstance(d, dict) or not {"name", "passed", "config", "value"} <= d.keys():
            continue
        if allowed is not None and d["name"] not in allowed:
            continue
        out.append(d)
    return out


def render_listing() -> str:
    rows = ["| name | metric | threshold | hypothesis |", "|------|--------|-----------|------------|"]
    for key in sorted(REGISTRY):
        exp = REGISTRY[key]
        rows.append(f"| {key} | {exp.metric} | {exp.threshold} | {exp.hypothesis} |")
    return "\n".join(rows)


def main(argv: Sequence[str] | None = None) -> int:
    """Module entry point (`python -m kainos.harness.runner`) — same commands as the CLI."""

    p = argparse.ArgumentParser(prog="kainos-experiment-runner", description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="run every registered experiment")
    group.add_argument("--name", help="run one experiment (exact key or unique short name)")
    group.add_argument("--phase", type=int, help="run all experiments registered for phase N")
    p.add_argument("--results-dir", default=str(RESULTS_DIR), help=f"output dir (default: {RESULTS_DIR})")
    args = p.parse_args(argv)
    try:
        exps = selected(name=args.name, all=args.all, phase=args.phase)
    except LookupError as e:
        print(str(e), file=sys.stderr)
        return 1
    _, rc = run_experiments(exps, Path(args.results_dir))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
