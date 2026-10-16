"""E5.0 — kernel acceptance (T1 kernel + T5 ToM store-audit, phase 5).

Hypothesis (the T1 claim): agents with VIEW-ISOLATED CODEX stores can
form supported, auditable mental models of each other through a
budgeted, corruption-capable assertion-delta channel — deterministically
— and the T5 white-box audit reads those models back: formation,
correctness, support (no unbacked mind-reading), and dispute discipline
(A5 at the social scale: contradictions survive as disputed pairs, never
averaged).

Metric: 12/12 acceptance checks across the two kernel demos (clean
sharing + seeded contradiction) plus the kernel invariants (determinism,
corruption recording, all-or-nothing budget). Threshold: 12/12.

Evidence: ``results/phase-5/e5.0.json`` (full report incl. both demo
reports, the audit blocks, and the check list) +
``results/phase-5/{shared-view,contradiction-talk}.json``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kainos.game.actions import Pass, Say
from kainos.game.agent import Agent, fact_delta_for
from kainos.game.demo import run_demo_games
from kainos.game.scheduler import Game
from kainos.game.spec import ChannelSpec, GameSpec
from kainos.harness.paths import default_results_dir

__all__ = ["E5_0Experiment", "check_kernel_invariants", "run_e5_0"]

CHECKS = 12


def _spec_noise() -> GameSpec:
    return GameSpec(
        "e5-noise", ("a", "b"), {"fa": "1", "fb": "2"},
        {"a": frozenset({"fa"}), "b": frozenset({"fb"})},
        ChannelSpec(budget_per_round=4, corruption=1.0), rounds=2,
    )


def _budget_game() -> Game:
    spec = GameSpec(
        "e5-budget", ("a", "b"), {"fa": "1", "fb": "2"},
        {"a": frozenset({"fa"}), "b": frozenset({"fb"})},
        ChannelSpec(budget_per_round=1, corruption=0.0), rounds=2,
    )

    def two_sends(view, round_no, transcript):
        if round_no != 1:
            return Pass()
        return Say("shared", tuple(fact_delta_for("say", "a", "fa", view["fa"], 1, i, "e5-budget") for i in range(2)))

    a = Agent("a", spec, two_sends)
    b = Agent("b", spec, lambda view, r, t: Pass())
    return Game(spec, {"a": a, "b": b}, seed=1)


def check_kernel_invariants() -> list[dict[str, Any]]:
    """Checks 10–12: the kernel invariants, exercised outside the demos."""

    out: list[dict[str, Any]] = []

    # 10 — determinism: a fresh re-run of both demos is bit-identical
    r1 = run_demo_games(write=False)
    r2 = run_demo_games(write=False)
    ok = all(r1[n]["determinism_hash"] == r2[n]["determinism_hash"] for n in r1)
    out.append({"check": 10, "name": "deterministic-rerun", "passed": bool(ok),
                "detail": {n: r1[n]["determinism_hash"] for n in r1}})

    # 11 — corruption is seeded and recorded WITH the original value
    spec = _spec_noise()

    def noisemaker(p: str):
        key = "fa" if p == "a" else "fb"

        def step(view: dict[str, str], round_no: int, transcript: list) -> Pass | Say:
            if round_no != 1:
                return Pass()
            return Say("shared", (fact_delta_for("say", p, key, view[key], 1, 0, "e5-noise"),))

        return step

    def mk() -> dict[str, Agent]:
        return {p: Agent(p, spec, noisemaker(p)) for p in spec.players}

    n1 = Game(spec, mk(), seed=42).run(write=False)
    n2 = Game(spec, mk(), seed=42).run(write=False)
    events = [e for e in n1["channel"]["events"] if e["kind"] == "corruption"]
    ok = (
        n1["determinism_hash"] == n2["determinism_hash"]
        and bool(events)
        and all(e["detail"]["original"].startswith("value=") and e["detail"]["transmitted"] != e["detail"]["original"] for e in events)
    )
    out.append({"check": 11, "name": "corruption-seeded-and-recorded", "passed": bool(ok),
                "detail": {"n_events": len(events), "sample": events[:2]}})

    # 12 — the round budget is ALL-OR-NOTHING and recorded
    g = _budget_game()
    b1 = g.run(write=False)
    rejects = [e for e in b1["channel"]["events"] if e["kind"] == "budget_reject"]
    ok = len(rejects) == 1 and b1["channel"]["sent_totals"]["a"] == 0
    out.append({"check": 12, "name": "budget-all-or-nothing", "passed": bool(ok),
                "detail": {"rejects": rejects[:1], "sent_totals": b1["channel"]["sent_totals"]}})
    return out


def run_e5_0(out_dir: Path | None = None) -> dict[str, Any]:
    """The official T1/T5 acceptance run. Returns the full report and
    writes ``phase-5/e5.0.json`` + the two demo reports."""

    out_dir = out_dir if out_dir is not None else default_results_dir()  # results hygiene
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "phase-5").mkdir(parents=True, exist_ok=True)
    demos = run_demo_games(write=True, out_dir=out_dir)
    sv, ct = demos["shared-view"], demos["contradiction-talk"]

    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append({"check": len(checks) + 1, "name": name, "passed": bool(passed), "detail": detail})

    # 1–5: the clean-sharing demo
    add("shared-score-both-correct", sv["scores"].get("score") == 1.0, sv["scores"])
    add("shared-view-isolation", sv["negative_control"]["view_leaks"] == 0, sv["negative_control"])
    add("shared-audit-a", all(
        sv["audit"]["a"][k] == v
        for k, v in (("violations", []), ("n_about_other", 1), ("n_correct", 1), ("n_supported", 1))
    ), sv["audit"]["a"])
    add("shared-audit-b", all(
        sv["audit"]["b"][k] == v
        for k, v in (("violations", []), ("n_about_other", 1), ("n_correct", 1), ("n_supported", 1))
    ), sv["audit"]["b"])
    dupes = [o for p in ("a", "b") for o in sv["agents"][p]["observe_reports"] if o["duplicates"] == 1]
    confs = [o for p in ("a", "b") for o in sv["agents"][p]["observe_reports"] if o["conflicts_preserved"] > 0]
    add("shared-idempotent-reread", len(dupes) == 2 and not confs, {"duplicates": len(dupes), "conflicts": len(confs)})

    # 6–9: the contradiction (dispute discipline) demo
    add("contradiction-recovery-score", ct["scores"].get("score") == 1.0, ct["scores"])
    add("contradiction-disputes-preserved", ct["audit"]["a"]["n_disputes_preserved"] == 2,
        {"n_disputes_preserved": ct["audit"]["a"]["n_disputes_preserved"]})
    add("contradiction-belief-layer", all(
        ct["audit"]["a"][k] == v
        for k, v in (("n_about_other", 3), ("n_correct", 2), ("n_supported", 3), ("violations", []))
    ), ct["audit"]["a"])
    landed = [o for o in ct["agents"]["a"]["observe_reports"] if o["conflicts_preserved"] == 2]
    add("contradiction-single-merge", len(landed) == 1 and landed[0]["disputed_pairs"] == 1, landed)

    # 10–12: kernel invariants
    checks.extend(check_kernel_invariants())

    passed = sum(1 for c in checks if c["passed"])
    report = {
        "experiment": "e5.0",
        "claim": "T1 kernel + T5 audit acceptance (see module docstring)",
        "checks_total": CHECKS,
        "checks_passed": passed,
        "value": passed / CHECKS,
        "checks": checks,
        "demos": {
            n: {k: demos[n][k] for k in ("determinism_hash", "scores", "negative_control", "audit", "commits")}
            for n in demos
        },
    }
    (out_dir / "phase-5" / "e5.0.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


class E5_0Experiment:
    """House-style experiment object (plain class; benches lazily import
    ``Result`` inside ``run`` and write their full report themselves)."""

    name = "e5.0"
    hypothesis = (
        "View-isolated CODEX agents form supported, auditable mental models of each "
        "other through a budgeted assertion-delta channel; the white-box ToM audit "
        "reads formation/correctness/support back and contradictions survive as "
        "disputed pairs (never averaged) — deterministically."
    )
    metric = "acceptance checks passed (0–12)"
    threshold = "12/12"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e5_0()
        passed = report["checks_passed"]
        return Result(
            name=self.name,
            passed=passed == CHECKS,
            value=float(passed),
            evidence=[Path("results") / "phase-5" / "e5.0.json",
                      Path("results") / "phase-5" / "shared-view.json",
                      Path("results") / "phase-5" / "contradiction-talk.json"],
            config={"seed": 1, "runs": ["shared-view", "contradiction-talk"], "dataset_hash": None},
            threshold=self.threshold,
        )
