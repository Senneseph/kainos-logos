"""E5.2 "The Range Game" — kernel wiring + acceptance bench (T3, #163).

Pre-registration (frozen 2026-08-21):
``plan/30-phases/phase-5-multi-agent/experiments.md``; verdict +
deviations (D-e5d/e5e/f) in ``.../results.md``.

The game (see ``kainos.game.range_game`` for the exact math): two
view-isolated CODEX agents, private values in 1..48, two rounds of
budgeted window-claims (R1 about one's own value — may bluff per the
declared deceiver set B; R2 about one's estimate of the other's value),
then a committed estimate of the other's number. The smaller error
takes the pot.

The V-ablation (equal lines, equal budgets; only the commit
conditioning differs — the ToM slots are POLICY slots, as pre-
registered, not kernel capability gates in this game):

* V0 — frozen zero-information commit (24).
* V1 — exact Bayes posterior on R1 claims only (``model_other_beliefs``).
* V2 — exact Bayes posterior on the full transcript
  (``model_other_state``).

ToM agents additionally store a SUPPORTED belief assertion about the
other's number (self-sourced, evidence citing the other's claim
assertions — the T5 audit support rule), so the audit has real belief
content to check; V0's store holds self-claims only.

The official bench: 5 pair games × 48 balanced episodes (240 kernel
runs; 10 written as per-run evidence files), the 500-sample leakage
estimate, the 8 pre-registered checks, and a full re-execution for
determinism (C1/C7).
"""

from __future__ import annotations

import json
import random
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

from kainos.exchange.protocol import merge
from kainos.game import range_game as rg
from kainos.game.actions import ALL_CAPABILITIES, Action, Commit, Pass, Say
from kainos.game.agent import Agent, belief_assertion, fact_delta_for
from kainos.game.scheduler import Game, default_out_dir
from kainos.game.spec import ChannelSpec, GameSpec

__all__ = [
    "CHECKS",
    "N_SAMPLES",
    "PAIRS",
    "SEED_EPISODES",
    "SEED_LEAKAGE",
    "B",
    "E5_2Experiment",
    "build_episode",
    "run_e5_2",
]

#: The declared deceiver set (12/48, every 4th — the filing's target
#: frequency; the exact incentive analysis is in the pre-registration,
#: D-e5d).
B: frozenset[int] = frozenset(x for x in range(1, rg.N + 1) if x % 4 == 0)

SEED_EPISODES = 5102  # balanced design + per-episode draws (510200+i+1)
SEED_LEAKAGE = 5103  # 500-sample leakage estimate
N_SAMPLES = 5000
PAIRS: tuple[tuple[str, str], ...] = (
    ("V0", "V0"),
    ("V1", "V1"),
    ("V2", "V2"),
    ("V1", "V2"),
    ("V2", "V1"),
)

CHECKS = 8

_POLICY_NOTES = {
    "V0": "frozen zero-information commit (24); no ToM slots",
    "V1": "model_other_beliefs: exact Bayes posterior on R1 claims only",
    "V2": "model_other_state: exact Bayes posterior on the full transcript",
}

REPRESENTATIVE_EPISODES = (0, 3)  # i=1 (xa=1, honest) and i=4 (xa=4, bluffs)


# frozen check values (derived offline from this same code; experiments.md)
FROZEN: dict[str, Any] = {
    "pooled_err": {"V0": Fraction(12), "V1": Fraction(583, 96), "V2": Fraction(79, 48)},
    "v2_pooled_h2h_share": Fraction(113, 192),
    "v1_h2h_share": Fraction(37, 96),
    "v2_h2h_share": Fraction(9, 16),
    "leakage_own": 4.5787,
    "leakage_full": 4.670479,
    "leakage_full_reported": 4.6705,
    "mi_tolerance": 0.05,
    "detection_v2": 48,  # of 48 bluff-receiving positions
    "detection_v1": 8,
    "support_v2": 48,
    "support_v1": 42,
    "localize_v2": 16,
    "localize_v1": 14,
}


# ── policy construction ────────────────────────────────────────────────────


def make_policy(players_level: dict[str, str], game_name: str) -> Callable:
    """Per-episode policy factory: one StepFn bound to the agents that
    will exist (the holder dict is filled at agent-creation time and
    captured by reference)."""

    def factory(player: str, agent_holder: dict[str, Agent]) -> Callable:
        other = "b" if player == "a" else "a"
        level = players_level[player]
        own_key, other_key = ("xa", "xb") if player == "a" else ("xb", "xa")
        d1_key, d2_key = ("da1", "da2") if player == "a" else ("db1", "db2")

        def _claim(store, sender: str, kind: str) -> tuple[int, int] | None:
            subject = f"fact:{kind}:{sender}"
            hits = [
                a
                for a in store.query(subject=subject)
                if a.provenance is not None
                and a.provenance.source is not None
                and a.provenance.source.uri == f"agent:{sender}"
            ]
            if not hits:
                return None
            obj = hits[-1].object_id
            lo, hi = obj[len("value=") :].split("-")
            return (int(lo), int(hi))

        def _claim_ids(store, sender: str) -> tuple[str, ...]:
            ids: list[str] = []
            for kind in ("r1", "r2"):
                for a in store.query(subject=f"fact:{kind}:{sender}"):
                    if (
                        a.provenance is not None
                        and a.provenance.source is not None
                        and a.provenance.source.uri == f"agent:{sender}"
                    ):
                        ids.append(a.id)
            return tuple(ids)

        def step(view: dict[str, str], round_no: int, transcript: list[dict[str, Any]]) -> Action:
            agent = agent_holder[player]
            store = agent.codex
            my_val = int(view[own_key])
            in_B = my_val in B

            if round_no in (1, 2):
                draw = int(view[d1_key if round_no == 1 else d2_key])
                if round_no == 1:
                    w = rg.r1_window(my_val, in_B, draw if in_B else None)
                else:
                    r1_other = _claim(store, other, "r1")
                    if r1_other is None:
                        return Pass()
                    declared = rg.declared_r2_window(r1_other, B)
                    w = rg._farset_of_window(declared)[draw] if in_B else declared
                delta = fact_delta_for(
                    "e52-claim",
                    player,
                    f"r{round_no}:{player}",
                    f"{w[0]}-{w[1]}",
                    round_no,
                    0,
                    game_name,
                )
                # the sender also merges its own claim into its own store
                # (self-knowledge of what was said — same discipline as
                # e5.1's self-recorded anchor).
                merge(store, [delta])
                return Say("shared", (delta,))

            if round_no == 3:
                r1_s = _claim(store, other, "r1")
                r2_s = _claim(store, other, "r2")
                r1_own = rg.r1_window(my_val, in_B, int(view[d1_key]) if in_B else None)
                if r1_s is None or r2_s is None:
                    return Pass()
                est = rg.commit_estimate(level, r1_s, r2_s, r1_own, B)
                if level in ("V1", "V2"):
                    # supported belief about the other's value (the T5
                    # audit reads this): self-sourced, evidence cites the
                    # other's claim assertions.
                    agent.remember(
                        belief_assertion(
                            player,
                            other,
                            other_key,
                            str(est),
                            source_uri=f"agent:{player}",
                            evidence=_claim_ids(store, other),
                        )
                    )
                return Commit({"estimate": int(est)})

            return Pass()

        return step

    return factory


# ── episode construction ───────────────────────────────────────────────────


def build_episode(
    xa: int,
    xb: int,
    level_a: str,
    level_b: str,
    draws: tuple[int, int, int, int],
    index: int,
) -> Game:
    """One kernel-backed episode. Draw order (fixed): (b_r1, a_r1, a_r2,
    b_r2); a draw is consumed only when that sender bluffs."""

    state = {
        "xa": str(xa),
        "xb": str(xb),
        "da1": str(draws[1]),
        "da2": str(draws[2]),
        "db1": str(draws[0]),
        "db2": str(draws[3]),
    }
    spec = GameSpec(
        name=f"e5.2-{level_a}-{level_b}-{index:02d}",
        players=("a", "b"),
        state=state,
        views={
            "a": frozenset({"xa", "da1", "da2"}),
            "b": frozenset({"xb", "db1", "db2"}),
        },
        channel=ChannelSpec(budget_per_round=1, corruption=0.0),
        rounds=3,
    )
    factory = make_policy({"a": level_a, "b": level_b}, spec.name)
    holder: dict[str, Agent] = {}
    for p, lvl in (("a", level_a), ("b", level_b)):
        holder[p] = Agent(p, spec, factory(p, holder), ALL_CAPABILITIES, policy_note=_POLICY_NOTES[lvl])
    return Game(spec, holder, seed=9000 + index)


def _claims_from_report(report: dict[str, Any]) -> dict[str, tuple[tuple[int, int], tuple[int, int]]]:
    """(r1a, r2a, r1b, r2b) from the transcript — the PUBLIC line."""

    out: dict[str, tuple[int, int]] = {}
    for e in report["transcript"]:
        act = e["action"]
        if act["kind"] != "say" or not e.get("delivered"):
            continue
        for d in act["deltas"]:
            subject: str = d["subject"][len("fact:") :]
            kind, sender = subject.split(":", 1)
            lo, hi = d["object"][len("value=") :].split("-")
            out[f"{kind}:{sender}"] = (int(lo), int(hi))
    return {
        "a": (out["r1:a"], out["r2:a"]),
        "b": (out["r1:b"], out["r2:b"]),
    }


def _episode_record(
    xa: int,
    xb: int,
    draws: tuple[int, int, int, int],
    level_a: str,
    level_b: str,
    report: dict[str, Any],
) -> dict[str, Any]:
    """One episode as the bench sees it: kernel evidence + the exact math
    the pre-registration pins (C1 compares these field-for-field)."""

    lines = _claims_from_report(report)
    est_a_of_b = int(report["commits"]["a"]["estimate"])
    est_b_of_a = int(report["commits"]["b"]["estimate"])
    sim = rg.simulate_pair(xa, xb, level_a, level_b, B, draws)
    e_a, e_b = abs(est_a_of_b - xb), abs(est_b_of_a - xa)
    win_a = 1.0 if e_a < e_b else (0.5 if e_a == e_b else 0.0)
    return {
        "xa": xa,
        "xb": xb,
        "level_a": level_a,
        "level_b": level_b,
        "line_a": [list(w) for w in lines["a"]],
        "line_b": [list(w) for w in lines["b"]],
        "a_bluffed": xa in B,
        "b_bluffed": xb in B,
        "est_a_of_b": est_a_of_b,
        "est_b_of_a": est_b_of_a,
        "e_a": e_a,
        "e_b": e_b,
        "win_a": win_a,
        "determinism_hash": report["determinism_hash"],
        "audit": {k: v["violations"] for k, v in report["audit"].items()},
        "view_leaks": report["negative_control"]["view_leaks"],
        # exact math side (the frozen derivation):
        "math_line_a": [list(w) for w in sim["line_a"]],
        "math_line_b": [list(w) for w in sim["line_b"]],
        "math_est_a_of_b": sim["est_a_of_b"],
        "math_est_b_of_a": sim["est_b_of_a"],
        "post_b_on_a": {str(k): v for k, v in (sim["post_b_on_a"] or {}).items()},
        "post_a_on_b": {str(k): v for k, v in (sim["post_a_on_b"] or {}).items()},
    }


# ── the bench ──────────────────────────────────────────────────────────────


def _detection_stats(records: list[dict[str, Any]], level: str) -> dict[str, int]:
    """Bluff-receiving positions for agents of `level`: posterior mass on
    B (detection), top-8 support, commit inside the true honest window
    (localization). Both receivers of a record are counted independently
    (an episode can have BOTH sides bluff)."""

    det = sup = loc = n = 0
    for r in records:
        positions: list[tuple] = []
        if r["level_a"] == level and r["b_bluffed"]:
            positions.append((r["post_a_on_b"], r["est_a_of_b"], r["xb"]))
        if r["level_b"] == level and r["a_bluffed"]:
            positions.append((r["post_b_on_a"], r["est_b_of_a"], r["xa"]))
        for post, est, truth in positions:
            if not post:
                continue
            n += 1
            total = sum(post.values())
            mass_b = sum(v for k, v in post.items() if int(k) in B)
            if mass_b == total:
                det += 1
            top8 = sorted(post, key=lambda k: (-post[k], int(k)))[:8]
            if str(truth) in top8:
                sup += 1
            hw = rg.honest_window(truth)
            if hw[0] <= est <= hw[1]:
                loc += 1
    return {"n": n, "det": det, "sup": sup, "loc": loc}


def _math_record(la: str, lb: str, xa: int, xb: int, dr: tuple[int, int, int, int]) -> dict[str, Any]:
    """The exact-math twin of a kernel episode record (for the reduced-
    mode expected values; in full mode this IS the frozen derivation)."""

    sim = rg.simulate_pair(xa, xb, la, lb, B, dr)
    win_a = 1.0 if sim["e_a"] < sim["e_b"] else (0.5 if sim["e_a"] == sim["e_b"] else 0.0)
    return {
        "level_a": la,
        "level_b": lb,
        "xa": xa,
        "xb": xb,
        "win_a": win_a,
        "a_bluffed": xa in B,
        "b_bluffed": xb in B,
        "est_a_of_b": sim["est_a_of_b"],
        "est_b_of_a": sim["est_b_of_a"],
        "e_a": sim["e_a"],
        "e_b": sim["e_b"],
        "post_a_on_b": {str(k): v for k, v in (sim["post_a_on_b"] or {}).items()},
        "post_b_on_a": {str(k): v for k, v in (sim["post_b_on_a"] or {}).items()},
    }


def run_e5_2(out_dir: Path | str | None = None) -> dict[str, Any]:
    """The acceptance bench. Official (default) = 48 balanced episodes x
    5 pair games + 5000 leakage samples, checked against the FROZEN
    constants. Reduced (KAINOS_E52_EPISODES / KAINOS_E52_SAMPLES, gate
    smoke): same structure, expected values derived from the exact math
    at run time (the frozen constants are full-design artifacts)."""

    import os

    episodes = int(os.environ.get("KAINOS_E52_EPISODES", rg.N))
    samples_n = int(os.environ.get("KAINOS_E52_SAMPLES", N_SAMPLES))
    full = episodes == rg.N and samples_n == N_SAMPLES
    root = Path(out_dir) if out_dir is not None else default_out_dir(None)
    (root / "phase-5").mkdir(parents=True, exist_ok=True)
    rg.clear_caches()

    pairs = rg.balanced_pairs(SEED_EPISODES)[:episodes]
    draws = [rg.episode_draws(random.Random(510200 + i + 1)) for i in range(episodes)]

    runs: dict[str, list[dict[str, Any]]] = {}
    math_runs: dict[str, list[dict[str, Any]]] = {}
    for la, lb in PAIRS:
        recs = []
        mrecs = []
        for i, ((xa, xb), dr) in enumerate(zip(pairs, draws)):
            g = build_episode(xa, xb, la, lb, dr, i)
            rep = g.run(write=full and i in REPRESENTATIVE_EPISODES, out_dir=root)
            recs.append(_episode_record(xa, xb, dr, la, lb, rep))
            mrecs.append(_math_record(la, lb, xa, xb, dr))
        runs[f"{la}-{lb}"] = recs
        math_runs[f"{la}-{lb}"] = mrecs

    # C8 data: re-execute ALL episodes (write=False), compare hashes
    rerun_ok = True
    for la, lb in PAIRS:
        for i, ((xa, xb), dr) in enumerate(zip(pairs, draws)):
            rep = build_episode(xa, xb, la, lb, dr, i).run(write=False, out_dir=root)
            if rep["determinism_hash"] != runs[f"{la}-{lb}"][i]["determinism_hash"]:
                rerun_ok = False

    all_recs = [r for k in sorted(runs) for r in runs[k]]
    all_math = [r for k in sorted(math_runs) for r in math_runs[k]]
    fallback_uses = rg.FALLBACK_USES

    # leakage
    rng = random.Random(SEED_LEAKAGE)
    samples = []
    for _ in range(samples_n):
        xa_s, xb_s = rng.randrange(1, rg.N + 1), rng.randrange(1, rg.N + 1)
        samples.append(rg.simulate_pair(xa_s, xb_s, "V2", "V2", B, rg.episode_draws(rng)))
    mi_emp = rg.posterior_leakage_bits(samples, B)
    mi_own_an = rg.analytic_leakage(B, "own") if full else 0.0
    if full:
        mi_full_an = rg.analytic_leakage(B, "full")
        assert abs(mi_full_an - FROZEN["leakage_full"]) < 1e-4
    else:
        mi_full_an = FROZEN["leakage_full"]  # frozen analytic (reduced smoke skips the 32s enumeration)
    mi_raw_full = rg.empirical_leakage(samples, "full") if full else None

    # pooled mean errors, kernel vs exact math
    def pooled(kre: list[dict[str, Any]], mre: list[dict[str, Any]]) -> tuple[Fraction, Fraction]:
        return (
            Fraction(sum(r["e_a"] + r["e_b"] for r in kre), 2 * len(kre)),
            Fraction(sum(r["e_a"] + r["e_b"] for r in mre), 2 * len(mre)),
        )

    ek0, mk0 = pooled(runs["V0-V0"], math_runs["V0-V0"])
    ek1, mk1 = pooled(runs["V1-V1"], math_runs["V1-V1"])
    ek2, mk2 = pooled(runs["V2-V2"], math_runs["V2-V2"])

    # head-to-head shares, kernel vs math
    def h2h(kre12, kre21, mre12, mre21) -> tuple[Fraction, Fraction]:
        v1 = Fraction(sum(Fraction(str(r["win_a"])) for r in kre12), len(kre12))
        v2 = Fraction(sum(Fraction(str(r["win_a"])) for r in kre21), len(kre21))
        mv1 = Fraction(sum(Fraction(str(r["win_a"])) for r in mre12), len(mre12))
        mv2 = Fraction(sum(Fraction(str(r["win_a"])) for r in mre21), len(mre21))
        return (Fraction(1) - v1 + v2) / 2, (Fraction(1) - mv1 + mv2) / 2

    h2h_k, h2h_m = h2h(
        runs["V1-V2"], runs["V2-V1"], math_runs["V1-V2"], math_runs["V2-V1"]
    )
    v1_share = Fraction(sum(Fraction(str(r["win_a"])) for r in runs["V1-V2"]), len(runs["V1-V2"]))
    v2_share = Fraction(sum(Fraction(str(r["win_a"])) for r in runs["V2-V1"]), len(runs["V2-V1"]))

    # usage
    usage_a = Fraction(sum(1 for r in all_recs if r["a_bluffed"]), len(all_recs))
    usage_b = Fraction(sum(1 for r in all_recs if r["b_bluffed"]), len(all_recs))
    bluffed_values = len([x for x in (p[0] for p in pairs) if x in B])

    # detection
    det_v2 = _detection_stats(all_recs, "V2")
    det_v1 = _detection_stats(all_recs, "V1")
    det_v2_m = _detection_stats(all_math, "V2")
    det_v1_m = _detection_stats(all_math, "V1")

    # C1: kernel == math, field-for-field
    c1_field = all(
        r["line_a"] == r["math_line_a"]
        and r["line_b"] == r["math_line_b"]
        and r["est_a_of_b"] == r["math_est_a_of_b"]
        and r["est_b_of_a"] == r["math_est_b_of_a"]
        for r in all_recs
    )
    c1 = c1_field and fallback_uses == 0

    c2_exact = ek0 == FROZEN["pooled_err"]["V0"] and ek1 == FROZEN["pooled_err"]["V1"] and ek2 == FROZEN["pooled_err"]["V2"]
    c2 = (ek0, ek1, ek2) == (mk0, mk1, mk2) and ek0 > ek1 > ek2 and (c2_exact if full else ek0 == mk0 and ek1 == mk1 and ek2 == mk2)
    c2_note = (
        f"V0={float(ek0):.4f} V1={float(ek1):.4f} V2={float(ek2):.4f} "
        f"(gaps V1-V2={float(ek1 - ek2):.4f}, V0-V2={float(ek0 - ek2):.4f}); "
        + ("frozen constants match" if full else "reduced: matches exact math (frozen constants are full-design)")
    )

    c3 = h2h_k == h2h_m and h2h_k > Fraction(1, 2) and (
        (h2h_k == FROZEN["v2_pooled_h2h_share"] and h2h_k - Fraction(1, 2) >= Fraction(1, 20))
        if full
        else True
    )

    c4 = all(
        sum(1 for r in recs if r["a_bluffed"]) == bluffed_values
        and sum(1 for r in recs if r["b_bluffed"]) == bluffed_values
        for recs in runs.values()
    ) and usage_a == Fraction(1, 4) and usage_b == Fraction(1, 4)

    band = FROZEN["mi_tolerance"] if full else 0.15
    c5 = abs(mi_emp - mi_full_an) <= band

    c6 = (det_v2 == det_v2_m) and (det_v1 == det_v1_m) and det_v2["det"] == det_v2["n"] and (
        (det_v2["det"] == FROZEN["detection_v2"] and det_v2["sup"] == FROZEN["support_v2"]
         and det_v1["det"] == FROZEN["detection_v1"] and det_v1["sup"] == FROZEN["support_v1"])
        if full
        else det_v2["det"] >= det_v1["det"]
    )

    c7 = det_v2["loc"] == det_v2_m["loc"] and det_v1["loc"] == det_v1_m["loc"] and (
        (det_v2["loc"] == FROZEN["localize_v2"] and det_v1["loc"] == FROZEN["localize_v1"])
        if full
        else True
    )

    c8 = (
        rerun_ok
        and all(len(v) == 0 for r in all_recs for v in r["audit"].values())
        and all(r["view_leaks"] == 0 for r in all_recs)
    )

    checks = [
        {
            "id": "C1",
            "name": "kernel run reproduces the exact math field-for-field (all episodes)",
            "passed": c1,
            "detail": f"consistent={c1_field}; FALLBACK_USES={fallback_uses}",
        },
        {
            "id": "C2",
            "name": "pooled mean |error|: V0=12 > V1=583/96 > V2=79/48 (kernel == exact math; frozen when full)",
            "passed": c2,
            "detail": c2_note,
        },
        {
            "id": "C3",
            "name": "state-slot value: V2 pooled head-to-head share vs V1 (113/192, >= 0.55 when full; > 0.5 when reduced; kernel == math)",
            "passed": c3,
            "detail": f"V1 share (V1,V2)={float(v1_share):.4f}; V2 share (V2,V1)={float(v2_share):.4f}; "
            f"pooled V2={float(h2h_k):.4f} (math {float(h2h_m):.4f})",
        },
        {
            "id": "C4",
            "name": "bluff usage exactly 1/4 per sender per balanced run (12/48 full-design); incentive record stands (41/48, D-e5d)",
            "passed": c4,
            "detail": f"usage_a={float(usage_a):.4f} usage_b={float(usage_b):.4f} "
            f"({bluffed_values}/{episodes} bluffed per side per run)",
        },
        {
            "id": "C5",
            "name": f"rational-listener leakage (exact per-sample posterior entropy) within "
            f"{'0.05' if full else '0.15 (reduced-mode tolerance)'} bits of the analytic 4.6705",
            "passed": c5,
            "detail": f"posterior-entropy estimate={mi_emp:.4f} vs analytic {mi_full_an:.4f} "
            + (
                f"(plug-in contrast: {mi_raw_full:.4f}; analytic own-claims scope: {mi_own_an:.4f})"
                if full and mi_raw_full is not None
                else ""
            ),
        },
        {
            "id": "C6",
            "name": "detection after a bluff: V2 all-mass-on-B == all positions (kernel == math; frozen 48/48 + V1 8/48 / 42/48 when full)",
            "passed": c6,
            "detail": f"V2 {det_v2}  V1 {det_v1}  (math: V2 {det_v2_m} V1 {det_v1_m})",
        },
        {
            "id": "C7",
            "name": "localization (reported, no directional check): commit inside true window (frozen V2 16/48, V1 14/48 when full)",
            "passed": c7,
            "detail": f"V2 {det_v2['loc']}/{det_v2['n']}  V1 {det_v1['loc']}/{det_v1['n']} (K-way random-draw information limit)",
        },
        {
            "id": "C8",
            "name": "hygiene: full re-execution bit-identical; audit violations 0; view leaks 0; no rejected budgets / corruption",
            "passed": c8,
            "detail": f"rerun_ok={rerun_ok}",
        },
    ]

    report = {
        "experiment": "e5.2",
        "mode": "full" if full else "reduced",
        "checks": checks,
        "checks_passed": sum(1 for c in checks if c["passed"]),
        "B": sorted(B),
        "episodes": episodes,
        "seeds": {"episodes": SEED_EPISODES, "leakage": SEED_LEAKAGE, "samples": samples_n},
        "pooled_mean_err": {
            "V0": [str(ek0), f"{float(ek0):.4f}", f"math {float(mk0):.4f}"],
            "V1": [str(ek1), f"{float(ek1):.4f}", f"math {float(mk1):.4f}"],
            "V2": [str(ek2), f"{float(ek2):.4f}", f"math {float(mk2):.4f}"],
        },
        "head_to_head": {
            "V1_in_(V1,V2)": [str(v1_share), f"{float(v1_share):.4f}"],
            "V2_in_(V2,V1)": [str(v2_share), f"{float(v2_share):.4f}"],
            "V2_pooled": [str(h2h_k), f"{float(h2h_k):.4f}", f"math {float(h2h_m):.4f}"],
        },
        "leakage_bits": {
            "analytic_full": round(mi_full_an, 4),
            "analytic_own": round(mi_own_an, 4) if full else None,
            "posterior_entropy_estimate": round(mi_emp, 4),
            "sample_count": samples_n,
            **({"plug_in_contrast": round(mi_raw_full, 4)} if mi_raw_full is not None else {}),
        },
        "detection": {"V2": det_v2, "V1": det_v1, "math_V2": det_v2_m, "math_V1": det_v1_m},
        "per_pair_games": {
            k: [
                {kk: vv for kk, vv in r.items() if kk not in ("post_b_on_a", "post_a_on_b", "math_line_a", "math_line_b", "math_est_a_of_b", "math_est_b_of_a")}
                for r in recs
            ]
            for k, recs in sorted(runs.items())
        },
        "fallback_uses": fallback_uses,
    }

    (root / "phase-5" / "e5.2.json").write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report


class E5_2Experiment:
    """House-style experiment object (benches lazily import Result and
    write their full report themselves)."""

    name = "e5.2"
    hypothesis = (
        "Under incentive, conditioning on more of the partner's model improves the competitive "
        "estimate exactly as information theory predicts: V2 (full transcript) achieves the "
        "Bayes lower bound and beats V1 (R1 only) head-to-head, V1 beats the zero-information "
        "ablation V0, deception is detected with full posterior mass by V2 (48/48) but only 8/48 "
        "by V1, and leakage is 4.58/4.67 of the 5.58 available bits — exact, pre-registered, "
        "and bit-identical on re-execution."
    )
    metric = "acceptance checks passed (0-8)"
    threshold = "8/8"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        rep = run_e5_2()
        passed = rep["checks_passed"]
        return Result(
            name=self.name,
            passed=passed == CHECKS,
            value=passed / CHECKS,
            evidence=[
                Path("results/phase-5/e5.2.json"),
            ]
            + [
                Path(f"results/phase-5/e5.2-{k}-{i:02d}.json")
                for k in (
                    "V0-V0",
                    "V1-V1",
                    "V2-V2",
                    "V1-V2",
                    "V2-V1",
                )
                for i in REPRESENTATIVE_EPISODES
            ],
            config={
                "declared_B": rep["B"],
                "seeds": rep["seeds"],
                "checks_passed": passed,
                "checks": CHECKS,
                "deviations": [
                    "D-e5d (12/48 = declared regime, not an equilibrium; 41/48 incentive record)",
                    "D-e5e (replaced unsupported per-episode direction check before freeze)",
                    "D-e5f (analytic leakage integrates the two values x four draws)",
                ],
                "dataset_hash": None,
            },
            threshold=self.threshold,
        )
