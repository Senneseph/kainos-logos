"""E6.6 — "Band 2: algebra ∥ kinematics (6–8, the first aligned band)"
(T7 #157, the M3 band sweep, band 2; the owner's directive #2 —
"later bands align physics ↔ math on overlapping topics, with a
JOINT band-end evaluation", comment 450).

Pre-registered in plan/30-phases/phase-6-tutor/experiments.md
(section E6.6 — design, frozen 48-turn script, checks P1–P8,
what-is-not-claimed). The band: ALGEBRA (one/two-step linear
equations solved by grounded inverses on the existing line) learns
the SAME TIME as KINEMATICS (constant-velocity cart motion), and
the ALIGNMENT is structural:
  (a) kin-solve-time and alg-two-step are the SAME grounded helper
      (one solver, two doors — measured: identical cite structure,
      differing only in the rule fact cited);
  (b) the concept prereq graph gates kinematics stability on the
      algebra counterpart (kin-solve-time ← alg-two-step,
      kin-rate ← alg-inverse-mul) — measured from the FINAL store:
      prereq gaps empty at the band end.
Line discipline: band 2 writes ZERO successor facts (line end
stays 72); mathematically-correct-but-off-line probes are the
honest wall (15·x = 120 → x = 8 in the math, off the line).

The run continues from the OFFICIAL e6.5 final store
(309 assertions, line end 72, eleven concepts stable, one shape
phrasology), sessions S2–S4, official arm = det (no Ollama; a live
addendum, if run, is separately labelled per the E5.4/E6.4/E6.5
precedent).
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_ALG_2STEP,
    CONCEPT_ALG_ADD1,
    CONCEPT_ALG_MUL,
    CONCEPT_BAND2,
    CONCEPT_KIN_FAR,
    CONCEPT_KIN_POS,
    CONCEPT_KIN_RATE,
    CONCEPT_KIN_TIME,
    RULE_LESSONS,
)
from kainos.tutor.mastery import Concept, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E66", "FROZEN", "E6_6Experiment", "run_e6_6"]

CHECKS = 8

#: The official e6.5 final store (the seed; M8 of the E6.5 lineage), repo-relative.
E65_SEED = Path("results/phase-6/e6.5-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E65_SEED.exists():
        return E65_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E65_SEED
    return alt if alt.exists() else E65_SEED

#: The E6.6 curriculum: everything the band ends carrying (six numerics,
#: phrasology, the band-1 geometry strip, the band-2 aligned strip).
CONCEPTS_E66: tuple = InfantRuntime.PILOT_CONCEPTS + (
    Concept("phrasology", "Phrasology — learned intake phrasings", "k-5", "language"),
    Concept("shape-triangle", "The triangle (sides and corners)", "k-5", "geometry", prereqs=("count-successor",)),
    Concept("shape-square", "The square (sides and corners)", "k-5", "geometry", prereqs=("count-successor",)),
    Concept("shape-rectangle", "The rectangle (sides and corners)", "k-5", "geometry", prereqs=("count-successor",)),
    Concept("shape-circle", "The circle (no sides, no corners)", "k-5", "geometry", prereqs=("count-successor",)),
) + CONCEPT_BAND2

FROZEN: dict = {
    "seed": str(E65_SEED),
    "sessions": [2, 3, 4],
    "seed_total": 309,
    "line_end_start": 72,
    "line_end_final": 72,  # band 2 writes ZERO successor facts
    "script": {
        2: [
            "what is x, if x + 6 is 12?",
            "an unknown added to a number is found by taking that number away from the total",
            "what is x, if x + 6 is 12?",
            "what is x, if x + 9 is 40?",
            "17 + 25 is what?",
            "an unknown that a number times gives a total is found by taking away that number again and again until the total is gone",
            "4 times x is 28: what is x?",
            "5 times x is 35: what is x?",
            "7 times x is 20: what is x?",
            "two changes in a row are undone in reverse order",
            "6 times x plus 4 is 40: what is x?",
            "5 times x plus 3 is 38: what is x?",
            "a cart starts at 0 and goes 6 every minute: where is it after 4 minutes?",
            "15 times x is 120: what is x?",
            "45 + 27 is what?",
            "what is x, if x + 45 is 72?",
        ],
        3: [
            "at a steady pace, the distance is the pace times the time",
            "how far does a cart go in 4 minutes at 6 a minute?",
            "how far does a cart go in 9 minutes at 8 a minute?",
            "position is the start plus the distance",
            "a cart starts at 5 and goes 6 every minute: where is it after 4 minutes?",
            "a cart starts at 12 and goes 5 every minute: where is it after 6 minutes?",
            "a cart starts at 60 and goes 8 every minute: where is it after 4 minutes?",
            "time is found the same way any unknown is found: undo the equation",
            "a cart starts at 4 and goes 6 every minute and is at 40: how many minutes did it take?",
            "a cart starts at 3 and goes 5 every minute and is at 38: how many minutes did it take?",
            "6 times x is 48: what is x?",
            "a steady pace is found by taking the time away from the distance again and again until the distance is gone",
            "a cart covers 36 miles in 4 minutes: how many miles every minute was that?",
            "a cart covers 40 miles in 8 minutes: how many miles every minute was that?",
            'the phrasing "a cart leaving {start} at {r} a minute: where is it after {t} minutes?" is the same as "a cart starts at {start} and goes {r} every minute and is at {c}: how many minutes did it take?"',
            'the phrasing "a cart leaving {start} at {r} a minute: where is it after {t} minutes?" is the same as "a cart starts at {start} and goes {r} every minute: where is it after {t} minutes?"',
        ],
        4: [
            "what is x, if x + 25 is 72?",
            "a cart leaving 5 at 6 a minute: where is it after 4 minutes?",
            "7 times x is 56: what is x?",
            "6 times x plus 4 is 40: what is x?",
            "how far does a cart go in 7 minutes at 5 a minute?",
            "how far does a cart go in 9 minutes at 8 a minute?",
            "a cart starts at 5 and goes 6 every minute: where is it after 4 minutes?",
            "a cart covers 36 miles in 4 minutes: how many miles every minute was that?",
            "a cart starts at 0 and goes 8 every minute and is at 64: how many minutes did it take?",
            "a cart leaving 12 at 5 a minute: where is it after 6 minutes?",
            "15 times x is 120: what is x?",
            "4 times x plus 6 is 30: what is x?",
            "a cart covers 45 miles in 9 minutes: how many miles every minute was that?",
            "what is x, if x + 7 is 42?",
            "a cart starts at 27 and goes 3 every minute and is at 51: how many minutes did it take?",
            "72 - 58 is what?",
        ],
    },
    "total_turns": 48,
    # P2: the per-session DOMAIN sequence (frozen: concurrency is
    # SCRIPTED, not emergent) — A algebra, K kinematics, N numeric,
    # G pre-teach gap (honest impossible), H honest boundary
    # (line wall / inexact), B honest rejection (the mapping
    # discipline). Intent values — the control run verifies them
    # against the frozen script (a mismatch is a finding, recorded as
    # a deviation, never silent).
    "domain_sequence": {
        2: "GAAANAAAHAAAGHNA",
        3: "KKKKKKHKKKAKKKBK",
        4: "AKAAKKKKKKHAKAKN",
    },
    # P2: the pre-teach honest gaps (frozen refs)
    "pre_teach_gaps": {
        "S02:01": CONCEPT_ALG_ADD1,
        "S02:13": CONCEPT_KIN_POS,
    },
    # P4: the honest boundary probes (frozen refs + articulation class)
    "wall_probes": {
        "S02:14": "off-line: 120 is past the line (x = 8 in the math)",
        "S03:07": "off-line: position 92 is past the line (distance 32 fits)",
        "S04:11": "off-line again (reproducible wall)",
    },
    "inexact_probe": "S02:09",  # 7·x = 20: inexact, not a whole number
    # P3: the exact grounded inverses (frozen expected answers; all
    # must be `derived` with non-empty grounded evidence that includes
    # the concept's rule fact)
    "derived_table": {
        "S02:03": "6", "S02:04": "31", "S02:07": "7", "S02:08": "7",
        "S02:11": "6", "S02:12": "7", "S02:16": "27",
        "S03:02": "24", "S03:03": "72", "S03:05": "29", "S03:06": "42",
        "S03:09": "6", "S03:10": "7", "S03:11": "8", "S03:13": "9", "S03:14": "5",
        "S04:01": "47", "S04:02": "29", "S04:03": "8", "S04:04": "6",
        "S04:05": "35", "S04:06": "72", "S04:07": "29", "S04:08": "9",
        "S04:09": "8", "S04:10": "42", "S04:12": "6", "S04:13": "5",
        "S04:14": "35", "S04:15": "8",
    },
    # P5: the alignment twin (one solver, two doors — the SAME numbers
    # through the algebra door and the kinematics door)
    "alignment_twin": {
        "algebra": "S02:11",  # 6·x + 4 is 40 → 6
        "kin": "S03:09",  # starts 4, goes 6, is at 40 → 6 minutes
        "answer": "6",
        "algebra_rule": f"cap:{CONCEPT_ALG_2STEP}:rule",
        "kin_rule": f"cap:{CONCEPT_KIN_TIME}:rule",
    },
    # P5: the prereq edges that ARE the alignment (queried from the
    # concept graph; their effect is measured on the final store:
    # prereq gaps empty at the band end)
    "alignment_prereqs": {
        CONCEPT_KIN_TIME: (CONCEPT_ALG_2STEP,),
        CONCEPT_KIN_RATE: (CONCEPT_ALG_MUL,),
    },
    # P6: the kin phrasology + the name-bijection discipline
    "kin_phrasing": {
        "rejected_attempt": "S03:15",  # → the TIME family (t vs c): rejected
        "taught": "S03:16",  # → the POSITION family: established
        "fact_ref": "phrasing:S03:16",
        "applied": ["S04:02", "S04:10"],
        "twin": {"lex": "S04:02", "canon": "S03:05"},
        "established_final": 1,
    },
    # P7: the JOINT band-end evaluation (ONE frozen probe set, ONE
    # check, both domains — the T7 "probe -> verify")
    "band_end_probes": {
        "S04:01": "47",
        "S04:02": "29",
        "S04:03": "8",
        "S04:04": "6",
        "S04:05": "35",
        "S04:06": "72",
        "S04:07": "29",
        "S04:08": "9",
        "S04:09": "8",
        "S04:10": "42",
        "S04:11": "needs_info",  # the reproducible line wall
        "S04:12": "6",
        "S04:13": "5",
        "S04:14": "35",
        "S04:15": "8",
        "S04:16": "14",
    },
    # P8: mastery at the band end (K = 4 is the bar)
    "mastery_expected": {
        CONCEPT_ALG_ADD1: {"state": "stable", "correct": 5},
        CONCEPT_ALG_MUL: {"state": "stable", "correct": 4},
        CONCEPT_ALG_2STEP: {"state": "stable", "correct": 4},
        CONCEPT_KIN_FAR: {"state": "stable", "correct": 4},
        CONCEPT_KIN_POS: {"state": "stable", "correct": 5},
        CONCEPT_KIN_TIME: {"state": "stable", "correct": 4},
        CONCEPT_KIN_RATE: {"state": "stable", "correct": 4},
    },
    # P8: the band-1 + seed concepts remain stable (band 2 regressed
    # nothing) — the 6 numerics, phrasology, the 4 shapes
    "seed_stable": [
        "count-successor",
        "add-within-10",
        "add-two-digit",
        "sub-within-30",
        "mult-within-100",
        "compare-numbers",
        "phrasology",
        "shape-triangle",
        "shape-square",
        "shape-rectangle",
        "shape-circle",
    ],
    "gap_articulation": "not a capability i have been taught",
    "rejection_articulation": "i can't take that as a mapping",
    "line_wall_articulation": "my number line ends at 72",
    "inexact_articulation": "not a whole number on my line",
    # frozen from the control run (the official run must reproduce):
    # 309 seed + 8 new fact assertions (7 band-2 rule lessons + 1 kin
    # phrasing) + 58 mastery-event assertions = 375 (events are store
    # data, P11 — recorded per turn, not in memory_diff)
    "final_total": 375,
    "new_facts": 22,  # 7 rule lessons + 1 kin phrasing + 7 curriculum facts + 7 prereq edges
    "new_events": 44,
}

#: frozen dataset identity
SCRIPT_HASH = hashlib.sha256(
    json.dumps({s: [t for t in ls] for s, ls in sorted(FROZEN["script"].items())}, sort_keys=True).encode("utf-8")
).hexdigest()[:16]

_RULE_CONCEPT = {cid for _, (cid, _, _) in RULE_LESSONS.items()}


def _line_end(store) -> int:
    end = 0
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        sid, oid = a.subject.id, a.object_id
        if sid.startswith("count-successor:succ-of(") and oid.startswith("count-successor:num(") and (
            a.validity is None or a.validity.to is None
        ):
            end = max(end, int(oid[len("count-successor:num(") : -1]))
    return end


def _fresh_store(root: Path, s: int):
    p = codex_dump_path(root, s)
    if p is None or not p.exists():
        return InMemoryCodexStore()
    return load_store(p)


def _turn_domain(t: dict) -> str:
    """The per-turn domain for the frozen interleave check (P2):
    A algebra, K kinematics, N numeric, G pre-teach gap, H honest
    boundary, B honest rejection. Pure function of the turn record."""

    ir = t.get("response_ir") or {}
    slots = t.get("slots") or {}
    if t["kind"] == "ambiguous":
        return "B"
    if ir.get("uncertainty_state") == "needs_info":
        return "H"
    if t["kind"] == "impossible":
        return "G"
    concept = t.get("concept")
    if isinstance(concept, str):
        if concept.startswith("alg-"):
            return "A"
        if concept.startswith("kin-"):
            return "K"
    rule = slots.get("rule")
    if isinstance(rule, str) and rule in RULE_LESSONS:
        cid = RULE_LESSONS[rule][0]
        if cid.startswith("alg-"):
            return "A"
        if cid.startswith("kin-"):
            return "K"
    if "new" in slots and "leaving" in t["surface"]:
        return "K"  # the kin phrasology lesson
    return "N"


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E66)
    out: list[dict] = []
    for s in FROZEN["sessions"]:
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.5 S4 store, id-for-id."""

    seed_path = _resolve_seed()
    seed = load_store(seed_path) if seed_path.exists() else None
    pre = _fresh_store(root, 2)
    seed_ids = {a.id for a in seed.query()} if seed is not None else set()
    pre_ids = {a.id for a in pre.query()}
    return {
        "seed_total": len(seed_ids),
        "reproduced_in_s2_pre": len(seed_ids & pre_ids),
        "missing": sorted(seed_ids - pre_ids),
    }


def _default_out_dir() -> Path:
    base = Path(os.environ.get("KAINOS_RESULTS_DIR", "results")) / "phase-6"
    base.mkdir(parents=True, exist_ok=True)
    return base


def run_e6_6(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.5 S4 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P1–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: dict[str, list[dict]] = {}
    for name in ("e6.6-run1", "e6.6-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.5 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed (M8)
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — the owner's
    # directives as data, with band 2's official evidence
    from kainos.tutor.bands import BAND_MAP, validate_band_map

    map_doc = {
        "bands": [
            {
                "name": b.name,
                "band": b.band,
                "domains": list(b.domains),
                "aligned_physics": list(b.aligned_physics),
                "concepts": list(b.concepts),
                "status": b.status,
                "evidence": list(b.evidence),
            }
            for b in BAND_MAP
        ],
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E66}),
    }
    (out_dir / "bands-map.json").write_text(json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.6-run1", "e6.6-run2"):
        (out_dir / name / "e6.6-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.6-run1"]:
        for t in srow.get("turns", []):
            turns[t["turn"]] = {
                "surface": t["surface"],
                "kind": t["kind"],
                "concept": t["concept"],
                "slots": t["slots"],
                "arm": t["arm"],
                "grounded": t["grounded"],
                "contract_valid": t["contract_valid"],
                "response_ir": t["response_ir"],
                "response_text": t["response_text"],
                "parse_source": (t["response_ir"] or {}).get("parse_source"),
                "memory_diff": t["memory_diff"],
                "domain": _turn_domain(t),
            }
    return {
        "arm": {"classifier": "det", "llm_arm": "skipped-no-backend", "note": "hermetic official: no Ollama, no backend"},
        "turns": turns,
        "seed": str(E65_SEED),
        "script_hash": SCRIPT_HASH,
        "alignment_prereqs": {k: list(v) for k, v in FROZEN["alignment_prereqs"].items()},
    }


def _ir_answer(t: dict) -> Any:
    return (t.get("response_ir") or {}).get("answer")


def _strip_parse(ir: dict) -> dict:
    return {k: v for k, v in (ir or {}).items() if k != "parse_source"}


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.6-run1"
    final = _fresh_store(run1_root, 4)

    # P1 — script & contract
    p1_bad: list[str] = []
    if len(turns) != FROZEN["total_turns"]:
        p1_bad.append(f"{len(turns)} turns != {FROZEN['total_turns']}")
    for ref, t in turns.items():
        if not t["contract_valid"]:
            p1_bad.append(f"{ref}: contract invalid")
    if report["script_hash"] != SCRIPT_HASH:
        p1_bad.append("script identity mismatch")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — pre-teach honesty + the interleave is FROZEN
    p2_bad: list[str] = []
    for ref, concept_id in FROZEN["pre_teach_gaps"].items():
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing {ref}")
            continue
        if t["kind"] != "impossible":
            p2_bad.append(f"{ref}: not the honest capability gap (got {t['kind']})")
        if t["memory_diff"]:
            p2_bad.append(f"{ref}: an unlearned drill wrote the store")
        if t["grounded"]:
            p2_bad.append(f"{ref}: an unlearned drill cited evidence (fabrication)")
        if FROZEN["gap_articulation"] not in (t["response_text"] or ""):
            p2_bad.append(f"{ref}: the frozen gap articulation is missing")
        if t["concept"] != concept_id:
            p2_bad.append(f"{ref}: routed to {t['concept']}, not {concept_id}")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    checks["p2_honest_gaps_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — exact grounded inverses (algebra + kinematics, all derived,
    # citing their RULE FACT + the line steps)
    p3_bad: list[str] = []
    rule_by_concept = {cid: f"cap:{cid}:rule" for cid in _RULE_CONCEPT}
    concept_by_mode = {
        "alg-add": CONCEPT_ALG_ADD1,
        "alg-mul": CONCEPT_ALG_MUL,
        "alg-2step": CONCEPT_ALG_2STEP,
        "kin-far": CONCEPT_KIN_FAR,
        "kin-pos": CONCEPT_KIN_POS,
        "kin-time": CONCEPT_KIN_TIME,
        "kin-rate": CONCEPT_KIN_RATE,
    }
    for ref, expected in sorted(FROZEN["derived_table"].items()):
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing {ref}")
            continue
        if _ir_answer(t) != expected:
            p3_bad.append(f"{ref}: answer {_ir_answer(t)!r} != {expected!r}")
            continue
        ir = t["response_ir"]
        if ir.get("uncertainty_state") != "derived":
            p3_bad.append(f"{ref}: not a grounded derivation ({ir.get('uncertainty_state')})")
        if not t["grounded"]:
            p3_bad.append(f"{ref}: zero grounded evidence")
        mode = (t.get("slots") or {}).get("mode")
        cid_b2 = concept_by_mode.get(mode, "") if isinstance(mode, str) else ""
        rule_id = rule_by_concept.get(cid_b2, "")
        if rule_id and rule_id not in (ir.get("evidence") or []):
            p3_bad.append(f"{ref}: the rule fact {rule_id} is not cited")
    # the INEXACT probe: honest, not rounded
    ip = turns.get(FROZEN["inexact_probe"])
    if ip is None:
        p3_bad.append("inexact probe ref missing")
    else:
        if not str(_ir_answer(ip) or "").startswith("needs_info"):
            p3_bad.append(f"S02:09: the inexact probe must be needs_info (got {_ir_answer(ip)!r})")
        if FROZEN["inexact_articulation"] not in (ip["response_text"] or ""):
            p3_bad.append("S02:09: the inexact articulation is missing")
    checks["p3_exact_grounded_inverses"] = {"pass": not p3_bad, "bad": p3_bad, "derived": len(FROZEN["derived_table"])}

    # P4 — the line wall composes into the aligned band
    p4_bad: list[str] = []
    for ref, note in FROZEN["wall_probes"].items():
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref} ({note})")
            continue
        if str(_ir_answer(t) or "")[:11] != "needs_info:":
            p4_bad.append(f"{ref}: the wall probe must be needs_info (got {_ir_answer(t)!r})")
        if FROZEN["line_wall_articulation"] not in (t["response_text"] or ""):
            p4_bad.append(f"{ref}: the line-end articulation is missing ({note})")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall probe cited evidence (fabrication)")
    # on-line maximal probes still derive (the wall is a measured knee)
    for ref, expected in (("S02:15", "72"), ("S03:03", "72"), ("S04:06", "72"), ("S02:16", "27")):
        t = turns.get(ref)
        if t is None or _ir_answer(t) != expected:
            p4_bad.append(f"{ref}: the on-line maximal probe must answer {expected} (got {_ir_answer(t) if t else None!r})")
    checks["p4_line_wall"] = {"pass": not p4_bad, "bad": p4_bad, "walls": list(FROZEN["wall_probes"])}

    # P5 — the alignment is literal: one solver, two doors
    p5_bad: list[str] = []
    tw = FROZEN["alignment_twin"]
    ta, tk = turns.get(tw["algebra"]), turns.get(tw["kin"])
    if ta is None or tk is None:
        p5_bad.append("alignment twin refs missing")
    else:
        if _ir_answer(ta) != tw["answer"] or _ir_answer(tk) != tw["answer"]:
            p5_bad.append(f"twin answers: {_ir_answer(ta)!r} / {_ir_answer(tk)!r} (both must be {tw['answer']})")
        ea, ek = list(ta["response_ir"].get("evidence") or []), list(tk["response_ir"].get("evidence") or [])
        if ea[-1] != tw["algebra_rule"] or ek[-1] != tw["kin_rule"]:
            p5_bad.append(f"twin rule facts: {ea[-1]!r} / {ek[-1]!r}")
        if sorted(ea[:-1]) != sorted(ek[:-1]):
            p5_bad.append("the two doors must cite the SAME line steps (the one corridor)")
    # the prereq edges (queried from the concept graph — the store's
    # effect on them is measured in P8: prereq gaps empty)
    from kainos.tutor.mastery import concept as _concept

    for cid, pres in FROZEN["alignment_prereqs"].items():
        got = tuple(_concept(cid).prereqs)
        if got != tuple(pres):
            p5_bad.append(f"{cid}: prereqs {got} != {tuple(pres)}")
        for pre in pres:
            edge_id = f"curriculum:prereq:{cid}>{pre}"
            edge = final.get(edge_id)
            if edge is None or (edge.validity is not None and edge.validity.to is not None):
                p5_bad.append(f"{cid}: the stored alignment edge {edge_id} is missing/inactive in the final store")
    # the store PRECONDITIONS: mastery from the final store shows the
    # kin concepts have EMPTY prereq gaps (their algebra counterpart
    # was stable first — the alignment, measured)
    from kainos.tutor.mastery import mastery_view

    mv = mastery_view(final, [CONCEPT_KIN_TIME, CONCEPT_KIN_RATE, CONCEPT_KIN_POS, CONCEPT_KIN_FAR])
    for cid in mv:
        if mv[cid].prereq_gaps:
            p5_bad.append(f"{cid}: prereq gaps {mv[cid].prereq_gaps} at the band end")
    checks["p5_alignment"] = {"pass": not p5_bad, "bad": p5_bad, "twin": tw}

    # P6 — the kin phrasology + the name-bijection discipline
    p6_bad: list[str] = []
    kp = FROZEN["kin_phrasing"]
    rej = turns.get(kp["rejected_attempt"])
    if rej is None:
        p6_bad.append("rejected-attempt ref missing")
    else:
        if rej["kind"] != "ambiguous":
            p6_bad.append(f"S03:15: the wrong mapping must be honestly rejected (got {rej['kind']})")
        if FROZEN["rejection_articulation"] not in (rej["response_text"] or ""):
            p6_bad.append("S03:15: the rejection articulation is missing")
        if rej["memory_diff"]:
            p6_bad.append("S03:15: the rejected mapping wrote the store")
    taught = turns.get(kp["taught"])
    if taught is None:
        p6_bad.append("taught ref missing")
    elif kp["fact_ref"] not in taught["memory_diff"]:
        p6_bad.append(f"S03:16: the phrasing fact {kp['fact_ref']} was not written")
    twin = kp["twin"]
    tl, tc = turns.get(twin["lex"]), turns.get(twin["canon"])
    if tl is None or tc is None:
        p6_bad.append("twin refs missing")
    else:
        if _strip_parse(tl["response_ir"]) != _strip_parse(tc["response_ir"]):
            p6_bad.append("S04:02 vs S03:05: the kin phrasing twin is not byte-equal modulo parse_source")
        if tl["response_text"] != tc["response_text"]:
            p6_bad.append("S04:02 vs S03:05: the texts differ")
        if not str(tl.get("parse_source") or "").startswith("lexicon:"):
            p6_bad.append(f"S04:02: parse_source {tl.get('parse_source')!r} (must be the learned phrasing)")
    for ref in kp["applied"]:
        t = turns.get(ref)
        if t is None:
            p6_bad.append(f"missing {ref}")
            continue
        if not str(t.get("parse_source") or "").startswith("lexicon:"):
            p6_bad.append(f"{ref}: not parsed via the learned phrasing")
        if not t["grounded"]:
            p6_bad.append(f"{ref}: a phrasing application cited nothing")
    # exactly ONE established kin phrasing in the final store
    from kainos.tutor.brainstem import REL_PHRASING

    kin_phr = [
        a
        for a in final.query(relation=REL_PHRASING)
        if "leaving" in (a.subject.id or "") and (a.validity is None or a.validity.to is None)
    ]
    if len(kin_phr) != kp["established_final"]:
        p6_bad.append(f"{len(kin_phr)} established kin phrasings != {kp['established_final']}")
    # zero open disputes
    from kainos.codex.models import EpistemicState

    disputes = [a for a in final.query() if a.status == EpistemicState.disputed and (a.validity is None or a.validity.to is None)]
    if disputes:
        p6_bad.append(f"{len(disputes)} open disputes at the band end")
    checks["p6_kin_phrasology"] = {"pass": not p6_bad, "bad": p6_bad}

    # P7 — the JOINT band-end evaluation (one set, one check, both
    # domains)
    p7_bad: list[str] = []
    for ref, expected in sorted(FROZEN["band_end_probes"].items()):
        t = turns.get(ref)
        if t is None:
            p7_bad.append(f"missing {ref}")
            continue
        got = _ir_answer(t)
        if expected == "needs_info":
            if str(got or "")[:11] != "needs_info:":
                p7_bad.append(f"{ref}: expected the honest wall, got {got!r}")
        elif got != expected:
            p7_bad.append(f"{ref}: {got!r} != {expected!r}")
    def _family(t: dict) -> str:
        slots = t.get("slots") or {}
        if "mode" in slots:
            return str(slots["mode"])
        if "rule" in slots:
            return "rule-lesson"
        if "new" in slots:
            return "phrasing"
        return "surface"

    joint_table = [
        {"ref": ref, "domain": turns[ref]["domain"], "family": _family(turns[ref]), "answer": _ir_answer(turns[ref])}
        for ref in sorted(FROZEN["band_end_probes"])
    ]
    checks["p7_joint_band_end"] = {"pass": not p7_bad, "bad": p7_bad, "joint_table": joint_table}

    # P8 — mastery of the ALIGNED band + determinism + seed continuity
    p8_bad: list[str] = []
    seed = _seed_check(run1_root)
    if seed["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed['seed_total']} != {FROZEN['seed_total']}")
    if seed["reproduced_in_s2_pre"] != FROZEN["seed_total"] or seed["missing"]:
        p8_bad.append(f"seed continuity: {seed}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (band 2 must write zero successor facts)")
    all_final = list(final.query())
    if len(all_final) != FROZEN["final_total"]:
        p8_bad.append(f"final store total {len(all_final)} != frozen {FROZEN['final_total']}")
    seed_path = _resolve_seed()
    seed_store = load_store(seed_path)
    seed_ids = {a.id for a in seed_store.query()}
    new = [a for a in all_final if a.id not in seed_ids]
    new_events = [a for a in new if (a.context.data or {}).get("kind") == "mastery-event"]
    new_facts = [a for a in new if (a.context.data or {}).get("kind") != "mastery-event"]
    if len(new_facts) != FROZEN["new_facts"]:
        p8_bad.append(f"new facts {len(new_facts)} != frozen {FROZEN['new_facts']}: {sorted(a.id for a in new_facts)}")
    if len(new_events) != FROZEN["new_events"]:
        p8_bad.append(f"new mastery events {len(new_events)} != frozen {FROZEN['new_events']}")
    mv = mastery_view(final, [c.id for c in CONCEPTS_E66])
    for cid, exp in FROZEN["mastery_expected"].items():
        v = mv.get(cid)
        if v is None:
            p8_bad.append(f"{cid}: not in the mastery view")
            continue
        if v.state != exp["state"]:
            p8_bad.append(f"{cid}: state {v.state} != {exp['state']}")
        if v.correct_derivations != exp["correct"]:
            p8_bad.append(f"{cid}: {v.correct_derivations} correct != {exp['correct']}")
        if v.prereq_gaps:
            p8_bad.append(f"{cid}: prereq gaps {v.prereq_gaps}")
    for cid in FROZEN["seed_stable"]:
        v = mv.get(cid)
        if v is None or v.state != "stable":
            p8_bad.append(f"{cid}: band 1/seed concept regressed ({v.state if v else 'absent'})")
    # determinism
    r1 = runs["e6.6-run1"]
    r2 = runs["e6.6-run2"]
    a = json.dumps(r1, sort_keys=True)
    b = json.dumps(r2, sort_keys=True)
    if a != b:
        p8_bad.append("run1 != run2")
    det_arm = all(
        (t.get("arm") or {}).get("classifier") == "det" for srow in r1 for t in srow.get("turns", [])
    )
    if not det_arm:
        p8_bad.append("a turn was not the det arm")
    checks["p8_mastery_determinism"] = {
        "pass": not p8_bad,
        "bad": p8_bad,
        "mastery": {cid: {"state": mv[cid].state, "correct": mv[cid].correct_derivations} for cid in FROZEN["mastery_expected"] if cid in mv},
        "seed": seed,
        "line_end": _line_end(final),
        "final_total": len(all_final),
        "new_facts": [a.id for a in new_facts],
        "new_events": len(new_events),
        "run_identity": hashlib.sha256(a.encode("utf-8")).hexdigest()[:16],
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    value = f"PASS e6.6: {passed}/{len(checks)}" if passed == len(checks) else f"FAIL e6.6: {passed}/{len(checks)}"
    return {"checks": checks, "passed": passed, "value": value}


class E6_6Experiment:
    """E6.6 — band 2: algebra ∥ kinematics (the first aligned band)."""

    name = "e6.6"
    hypothesis = (
        "Algebra ∥ kinematics learns as ONE aligned band (6–8): one/two-step linear equations "
        "and constant-velocity cart motion ride the same teachable-strip seam, with the "
        "alignment STRUCTURAL — kin-solve-time and alg-two-step are the same grounded helper "
        "(one solver, two doors: byte-equal line-step cites, only the rule fact differs), and "
        "the prereq graph gates kinematics stability on its algebra counterpart (stored edges, "
        "empty gaps at the band end); inexact division is honest ('not a whole number on my "
        "line'), off-line probes are the measured wall (15·x = 120, x = 8 in the math, off the "
        "line), the kin phrasology's wrong cross-family mapping is rejected by the name "
        "bijection (never silently mis-mapped), and the band ENDS on a JOINT evaluation — one "
        "frozen probe set spanning both domains, all seven band-2 concepts stable (K = 4) "
        "against the eleven seed/band-1 concepts, line untouched at 72, two runs byte-identical."
    )
    metric = "band-2 checks passed (P1..P8)"
    threshold = "8/8"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_6()
        if "error" in report:
            return Result(name=self.name, passed=False, value=0.0, evidence=[Path("results/phase-6")], config={"seed": FROZEN["seed"], "error": report["error"]})
        return Result(
            name=self.name,
            passed=report["passed"] == CHECKS,
            value=report["value"],
            evidence=[
                Path("results/phase-6/e6.6-run1/session-S02.json"),
                Path("results/phase-6/e6.6-run1/session-S03.json"),
                Path("results/phase-6/e6.6-run1/session-S04.json"),
                Path("results/phase-6/e6.6-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
