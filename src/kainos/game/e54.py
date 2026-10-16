"""E5.4 — the LLM-surface messaging arm (T6 #166, M4 stretch).

Pre-registered in ``plan/30-phases/phase-5-multi-agent/experiments.md``
— E5.4 (frozen before implementation). The claim: the E5.1 acceptance
matrix (2 episodes × 3 variants = 12 runs + the forced-V0 sub-check)
run through the natural-language message-surface codec (every
Say/Correct delta travels as a plain-English sentence, deterministically
re-parsed into the same delta before merge) reproduces the E5.1
acceptance EXACTLY, with store content bit-identical to the structured
arm modulo the surface's own audit log. Official arm = the SKIP arm
(canonical codec; no LLM backend — the LLM render-only seam is the
separately-labelled live addendum, E6.4 precedent).

Checks (threshold 5/5 exact): X1 metrics survive (all 12 E5.1 claims),
X2 seam neutrality (bit-level), X3 honest drops (the frozen
perturbation), X4 seam + SKIP record, X5 determinism.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from kainos.game.actions import Correct, Pass
from kainos.game.agent import Agent
from kainos.game.scheduler import Game
from kainos.game.shared_grid import (
    CAPS,
    CELLS,
    DOOR_FACT,
    GAMERUN_SEED,
    ROW3_CELLS,
    build_game,
    correct_delta,
    make_episode,
    score_run,
)
from kainos.game.surface import (
    GRAMMAR_SHA,
    CanonicalRenderer,
    ClaimSpec,
    LlmRenderer,
    ScriptedDropRenderer,
    SurfaceCodec,
)

__all__ = ["CHECKS", "E5_4Experiment", "run_e5_4"]

CHECKS = 5

EPISODES: tuple[str, ...] = ("clean", "false")
VARIANTS: tuple[str, ...] = ("V0", "V1", "V2")
ARM_CANONICAL = "canonical"

#: The frozen X3 perturbation: b's round-3 anchor (its only anchor-form
#: delta) renders unparseably -> dropped.
X3_DROP: tuple[str, str] = ("b", "anchor")


def _run_key(episode: str, variant: str) -> str:
    return f"e5.4-{episode}-{variant.lower()}"


def _build(
    episode: str, variant: str, codec: SurfaceCodec | None, rename: str | None = None
) -> tuple[Game, dict[str, Any]]:
    """A matrix run: the E5.1 game (renamed into the e5.4 artifact
    namespace) carrying the codec (None = the structured arm)."""

    ep = make_episode(episode)
    g = build_game(episode, variant)
    name = rename or _run_key(episode, variant)
    g = dataclasses.replace(
        g, spec=dataclasses.replace(g.spec, name=name), surface=codec
    )
    return g, ep


def _strip_surface(report: dict[str, Any]) -> dict[str, Any]:
    """The report with the surface's own audit blocks removed (the X2
    strip): the only machine content the codec arm adds is its log."""

    r = json.loads(json.dumps(report, ensure_ascii=False))
    for e in r["transcript"]:
        e.pop("surface", None)
    r.pop("determinism_hash", None)
    return r


def _stripped_hash(report: dict[str, Any]) -> str:
    return (
        "sha256:"
        + hashlib.sha256(
            json.dumps(
                _strip_surface(report), indent=2, sort_keys=True, ensure_ascii=False
            ).encode("utf-8")
        ).hexdigest()
    )


def _store_fingerprint(g: Game) -> dict[str, list[tuple[Any, ...]]]:
    """Each agent's full store content, order-free (the X2 store
    comparison): every assertion's identity tuple."""

    out: dict[str, list[tuple[Any, ...]]] = {}
    for p in g.spec.players:
        a = g.agents[p]
        out[p] = sorted(
            (
                x.id,
                x.subject.id,
                x.relation.id,
                str(x.object_id),
                x.provenance.source.uri
                if x.provenance is not None and x.provenance.source is not None
                else None,
                x.status.value,
            )
            for x in a.codex.query()
        )
    return out


def _surface_stats(report: dict[str, Any]) -> dict[str, int]:
    n = {"delivered": 0, "dropped": 0, "structured": 0}
    for e in report["transcript"]:
        for d in e.get("surface", {}).get("deltas", []):
            n[d["status"]] += 1
    return n


def _run_matrix(
    codec: SurfaceCodec | None, out_dir: Path | None = None, write: bool = False
) -> dict[str, dict[str, Any]]:
    runs: dict[str, dict[str, Any]] = {}
    for episode in EPISODES:
        for variant in VARIANTS:
            g, ep = _build(episode, variant, codec)
            report = g.run(write=write, out_dir=out_dir)
            runs[_run_key(episode, variant)] = {
                "episode": episode,
                "variant": variant,
                "planted_col": ep["planted_col"],
                "game": g,
                "report": report,
                "score": score_run(report, ep["spec"]),
            }
    return runs


def _forced_v0(codec: SurfaceCodec | None) -> dict[str, Any]:
    """The E5.1 forced-V0 sub-check, carried through the codec (the
    correction attempt is capability-gated BEFORE the surface — a named
    gap, never delivered, never rendered)."""

    ep = make_episode("clean")
    spec = dataclasses.replace(ep["spec"], name="e5.4-forced-v0")

    def rogue(
        view: dict[str, str], round_no: int, transcript: list[dict[str, Any]]
    ) -> Any:
        if round_no != 1:
            return Pass()
        return Correct(
            "b", DOOR_FACT, (correct_delta("a", "b", "c1", "c2", 1, spec.name, ()),)
        )

    a = Agent(
        "a",
        spec,
        rogue,
        capabilities=CAPS["V0"],
        policy_note="V0 forced attempt (codec)",
    )
    b = Agent(
        "b", spec, lambda view, r, t: Pass(), capabilities=CAPS["V0"], policy_note="V0"
    )
    g = Game(spec, {"a": a, "b": b}, seed=GAMERUN_SEED, surface=codec)
    report = g.run(write=False)
    rej = report["agents"]["a"]["rejections"]
    return {
        "rejected": bool(rej) and "assert_about_other" in rej[0]["reason"],
        "named_gap": rej[0]["reason"] if rej else None,
        "n_corrects_in_transcript": sum(
            1 for e in report["transcript"] if e["action"]["kind"] == "correct"
        ),
    }


def _e51_claims(
    runs: dict[str, dict[str, Any]], forced: dict[str, Any]
) -> list[dict[str, Any]]:
    """The twelve E5.1 acceptance claims re-stated as X1's content
    (exactly the frozen E5.1 values — E5.4 derives none of them; it
    reproduces them on the surface arm)."""

    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append(
            {
                "check": len(checks) + 1,
                "name": name,
                "passed": bool(passed),
                "detail": detail,
            }
        )

    def red(key: str, p: str) -> dict[str, int]:
        return runs[key]["score"]["redundancy"][p]

    def frac(d: dict[str, int]) -> Fraction:
        return Fraction(d["redundant"], d["sent"]) if d["sent"] else Fraction(0)

    clean_keys = [k for k, r in runs.items() if r["episode"] == "clean"]
    add(
        "1-clean-recovery-all-variants",
        all(runs[k]["score"]["recovery"] for k in clean_keys),
        {k: runs[k]["score"]["correct_cells"] for k in sorted(clean_keys)},
    )
    add(
        "2-clean-redundancy-v1-v2-exact-1-of-9",
        all(
            frac(red(f"e5.4-clean-{v.lower()}", p)) == Fraction(1, 9)
            for v in ("V1", "V2")
            for p in ("a", "b")
        ),
        {
            f"{v}/{p}": f"{red(f'e5.4-clean-{v.lower()}', p)['redundant']}/{red(f'e5.4-clean-{v.lower()}', p)['sent']}"
            for v in ("V1", "V2")
            for p in ("a", "b")
        },
    )
    gap = Fraction(5, 13) - Fraction(1, 9)
    add(
        "3-clean-redundancy-v0-exact-5-of-13-and-gap",
        all(frac(red("e5.4-clean-v0", p)) == Fraction(5, 13) for p in ("a", "b"))
        and gap == Fraction(32, 117)
        and gap >= Fraction(25, 100),
        {"gap": f"{gap.numerator}/{gap.denominator}"},
    )
    for idx, variant in (("4", "V1"), ("5", "V2")):
        key = f"e5.4-false-{variant.lower()}"
        fc = runs[key]["score"]["first_correct"]
        add(
            f"{idx}-false-{variant.lower()}-detection-round-4-and-recovery",
            fc is not None
            and fc["round"] == 4
            and fc["by"] == "a"
            and fc["target"] == "b"
            and runs[key]["score"]["recovery"],
            {
                **(fc or {}),
                "recovery": runs[key]["score"]["recovery"],
                "correct_cells": runs[key]["score"]["correct_cells"],
            },
        )
    v0 = runs["e5.4-false-v0"]
    v0_grid_a = v0["report"]["commits"].get("a", {}).get("grid", {})
    ep_false = make_episode("false")
    truth3 = {c: ep_false["truth"][c] for c in ROW3_CELLS}
    wrong_a = sorted(c for c in ROW3_CELLS if v0_grid_a.get(c) != truth3[c])
    wrong_total = sorted(c for c in CELLS if v0_grid_a.get(c) != ep_false["truth"][c])
    add(
        "6-false-v0-structurally-uncorrectable",
        v0["score"]["n_corrects"] == 0
        and wrong_a == wrong_total
        and len(wrong_a) == 2
        and v0["score"]["correct_cells"]["b"] == len(CELLS)
        and forced["rejected"]
        and forced["n_corrects_in_transcript"] == 0,
        {"wrong_cells_a": wrong_total, "forced_attempt": forced},
    )
    add(
        "7-false-disputed-pairs-preserved-in-all-four-stores",
        all(
            runs[f"e5.4-false-{v.lower()}"]["report"]["audit"][p][
                "n_disputes_preserved"
            ]
            >= 2
            for v in ("V1", "V2")
            for p in ("a", "b")
        ),
        {
            f"{v}/{p}": runs[f"e5.4-false-{v.lower()}"]["report"]["audit"][p][
                "n_disputes_preserved"
            ]
            for v in ("V1", "V2")
            for p in ("a", "b")
        },
    )
    viol = {
        k: sum(len(a.get("violations", [])) for a in r["report"]["audit"].values())
        for k, r in runs.items()
    }
    add(
        "8-all-runs-zero-audit-violations",
        all(v == 0 for v in viol.values()),
        {k: v for k, v in viol.items() if v} or "0 everywhere",
    )
    leaks = {k: r["report"]["negative_control"]["view_leaks"] for k, r in runs.items()}
    add(
        "9-all-runs-zero-view-leaks",
        all(v == 0 for v in leaks.values()),
        {k: v for k, v in leaks.items() if v} or "0 everywhere",
    )
    events = {
        k: [e["kind"] for e in r["report"]["channel"]["events"]]
        for k, r in runs.items()
    }
    add(
        "10-all-runs-no-budget-rejections-no-corruption",
        all(not ev for ev in events.values()),
        {k: v for k, v in events.items() if v} or "clean",
    )
    bad = [
        f"{k}/{p}: {len(r['report']['commits'].get(p, {}).get('grid', {}))} cells"
        for k, r in runs.items()
        for p in r["report"]["players"]
        if set(r["report"]["commits"].get(p, {}).get("grid", {})) != set(CELLS)
    ]
    add(
        "11-all-24-commits-are-20-cell-reconstructions",
        not bad,
        bad or "24/24 full grids",
    )
    expected_keys = [f"e5.4-{e}-{v.lower()}" for e in EPISODES for v in VARIANTS]
    add(
        "12-matrix-completeness-exactly-the-e5-1-set",
        sorted(runs) == expected_keys,
        {"runs": len(runs)},
    )
    return checks


def _load_frozen() -> dict[str, Any]:
    """The derived constants frozen from the offline control (written
    before the official run); absent => no freeze yet (the run is a
    control, not the official)."""

    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        cand = base / "results" / "phase-5" / "e5.4-derived.json"
        if cand.exists():
            return json.loads(cand.read_text(encoding="utf-8"))
    return {}


def run_e5_4(out_dir: Path | None = None, write: bool = True) -> dict[str, Any]:
    from kainos.harness.paths import default_results_dir

    out_dir = out_dir or default_results_dir()
    (out_dir / "phase-5").mkdir(parents=True, exist_ok=True)

    canonical = SurfaceCodec(CanonicalRenderer())

    # ── the arms ────────────────────────────────────────────────────────
    off_runs = _run_matrix(None)  # the structured baseline
    on_runs = _run_matrix(
        canonical, out_dir=out_dir, write=write
    )  # the official SKIP arm
    forced_on = _forced_v0(canonical)
    forced_off = _forced_v0(None)

    # the drop arm: 11 canonical runs (the X1 runs themselves) + the
    # frozen perturbation in their place (its own artifact name).
    drop_codec = SurfaceCodec(ScriptedDropRenderer(drop=X3_DROP))
    g3, ep3 = _build("false", "V1", drop_codec, rename="e5.4-false-v1-drop")
    r3 = g3.run(write=write, out_dir=out_dir)
    s3 = score_run(r3, ep3["spec"])

    # ── X1: the twelve E5.1 claims on the codec arm ─────────────────────
    claims = _e51_claims(on_runs, forced_on)
    x1_ok = (
        sum(1 for c in claims if c["passed"]) == len(claims)
        and all(c["name"] for c in claims)
        and forced_off["rejected"]
    )

    # ── X2: seam neutrality (bit-level) ─────────────────────────────────
    x2_detail: dict[str, dict[str, bool]] = {
        "stores_identical": {},
        "stripped_hash_match": {},
    }
    x2_ok = True
    for k in sorted(on_runs):
        same_store = _store_fingerprint(on_runs[k]["game"]) == _store_fingerprint(
            off_runs[k]["game"]
        )
        same_hash = (
            _stripped_hash(on_runs[k]["report"])
            == off_runs[k]["report"]["determinism_hash"]
        )
        x2_detail["stores_identical"][k] = same_store
        x2_detail["stripped_hash_match"][k] = same_hash
        x2_ok = x2_ok and same_store and same_hash

    # ── X3: the frozen honest-drop perturbation ─────────────────────────
    drops_logged = sum(
        1
        for e in r3["transcript"]
        for d in e.get("surface", {}).get("deltas", [])
        if d["status"] == "dropped"
    )
    beliefs_a = [
        a
        for a in g3.agents["a"].codex.query()
        if a.relation.id == "believes" and a.subject.id == "agent:b"
    ]
    beliefs_b = [
        a
        for a in g3.agents["b"].codex.query()
        if a.relation.id == "believes" and a.subject.id == "agent:a"
    ]
    x3_observed = {
        "first_correct": s3["first_correct"],
        "recovery": s3["recovery"],
        "n_corrects": s3["n_corrects"],
        "drops_logged": drops_logged,
        "a_beliefs_about_b": len(beliefs_a),
        "b_beliefs_about_a": len(beliefs_b),
        "correct_cells": s3["correct_cells"],
        "disputes": {p: r3["audit"][p]["n_disputes_preserved"] for p in r3["players"]},
    }
    # the eleven untouched runs ARE the X1 runs (the same execution —
    # identity is structural); their pin is the frozen hash file.
    frozen = _load_frozen()
    x3_expected = frozen.get("x3", {}).get("expected", {})
    x3_ok = (
        x3_expected
        and all(x3_observed.get(kk) == vv for kk, vv in x3_expected.items())
        and x3_observed["drops_logged"] == 1
        and all(
            on_runs[k]["report"]["determinism_hash"] == frozen["x1"]["run_hashes"][k]
            for k in on_runs
            if k in frozen.get("x1", {}).get("run_hashes", {}) and k != "e5.4-false-v1"
        )
    )

    # ── X4: seam + SKIP record ──────────────────────────────────────────
    from kainos.lang.llm import (
        MockBackend,  # the shared seam (one surface, two consumers)
    )

    probe = ClaimSpec("cell", "a", {"cell": "r1c2", "value": "door"})
    mock = MockBackend([render_for_mock(probe)])
    llm = LlmRenderer(mock, "mock")
    x4_detail = {
        "arm": {
            "codec": ARM_CANONICAL,
            "backend": "none",
            "note": "hermetic: the live LLM is the separately-labelled addendum (X6)",
        },
        "grammar_sha": GRAMMAR_SHA,
        "llm_seam": {
            "renderer": llm.name,
            "backend_object": type(mock).__name__,
            "prompt_sample": llm._user_prompt(probe),
        },
        "grammar_sha_match": (frozen.get("grammar_sha", GRAMMAR_SHA) == GRAMMAR_SHA)
        if frozen
        else True,
        "frozen_present": bool(frozen),
    }
    x4_ok = x4_detail["grammar_sha_match"] and llm.name == "llm:mock"

    # ── X5: determinism of the codec arm ────────────────────────────────
    re_runs = _run_matrix(canonical)
    x5_ok = all(
        re_runs[k]["report"]["determinism_hash"]
        == on_runs[k]["report"]["determinism_hash"]
        for k in on_runs
    )
    x5_detail = {
        "sample": {
            k: re_runs[k]["report"]["determinism_hash"][:24]
            for k in sorted(on_runs)[:3]
        }
    }

    checks = [
        {
            "check": 1,
            "name": "x1-e51-claims-survive-exactly",
            "passed": bool(x1_ok),
            "detail": {
                "e51_claims": {c["name"]: c["passed"] for c in claims},
                "e51_claims_passed": sum(1 for c in claims if c["passed"]),
                "forced_off_attempt": forced_off,
            },
        },
        {
            "check": 2,
            "name": "x2-seam-neutrality-bit-level",
            "passed": bool(x2_ok),
            "detail": x2_detail,
        },
        {
            "check": 3,
            "name": "x3-honest-drop-measured",
            "passed": bool(x3_ok),
            "detail": {"observed": x3_observed, "expected": x3_expected},
        },
        {
            "check": 4,
            "name": "x4-seam-and-skip-record",
            "passed": bool(x4_ok),
            "detail": x4_detail,
        },
        {
            "check": 5,
            "name": "x5-codec-arm-determinism",
            "passed": bool(x5_ok),
            "detail": x5_detail,
        },
    ]
    passed = sum(1 for c in checks if c["passed"])

    report = {
        "experiment": "e5.4",
        "claim": "The E5.1 acceptance survives the natural-language message surface exactly; the surface is a semantic-transparent transport; a surface drop is honest and measured (E5.4 X1-X5)",
        "arm": x4_detail["arm"],
        "grammar_sha": GRAMMAR_SHA,
        "runs": {
            k: {
                "episode": r["episode"],
                "variant": r["variant"],
                "determinism_hash": r["report"]["determinism_hash"],
                "score": r["score"],
                "surface_stats": _surface_stats(r["report"]),
            }
            for k, r in on_runs.items()
        },
        "runs_drop_arm": {
            "e5.4-false-v1-drop": {
                "determinism_hash": r3["determinism_hash"],
                "first_correct": s3["first_correct"],
                "recovery": s3["recovery"],
                "surface_stats": _surface_stats(r3),
            }
        },
        "forced_v0_attempt": forced_on,
        "checks_total": CHECKS,
        "checks_passed": passed,
        "checks": checks,
    }
    if write:
        (out_dir / "phase-5" / "e5.4.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return report


def render_for_mock(claim: ClaimSpec) -> str:
    """X4's canned LLM reply: the canonical sentence of the probe claim
    (the mock render round-trips exactly — proving the seam, not the
    model)."""

    from kainos.game.surface import render_sentence

    return render_sentence(claim)


class E5_4Experiment:
    """E5.4 — the LLM-surface messaging arm (T6 #166, M4 stretch)."""

    name = "e5.4"
    hypothesis = (
        "The E5.1 acceptance (redundancy separation, the false-belief probe, disputed-pair "
        "preservation, zero audit violations) survives the natural-language message surface "
        "EXACTLY on the SKIP (canonical-codec) arm, with store content bit-identical to the "
        "structured arm modulo the surface's own audit log; a surface drop is honest and "
        "measured (the frozen X3 perturbation), never silent."
    )
    metric = "acceptance checks passed (X1..X5)"
    threshold = "5/5"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e5_4()
        passed = report["checks_passed"]
        return Result(
            name=self.name,
            passed=passed == CHECKS,
            value=passed / CHECKS,
            evidence=[
                Path("results/phase-5/e5.4.json"),
                Path("results/phase-5/e5.4-false-v1-drop.json"),
            ]
            + [Path(f"results/phase-5/{k}.json") for k in sorted(report["runs"])],
            config={
                "arm": report["arm"],
                "grammar_sha": report["grammar_sha"],
                "runs": sorted(report["runs"]),
                "checks_passed": passed,
                "checks": CHECKS,
            },
            threshold=self.threshold,
        )
