"""E6.7 — "Band 3: geometry-advanced ∥ vectors/statics (9–12, the product band)"
(T7 #157, the M3 band sweep, band 3; owner-directed 2026-08-22
"Continue to BAND 3". The alignment declared in the band map for
this rung: geometry-advanced ∥ vectors/statics.)

Pre-registered in plan/30-phases/phase-6-tutor/experiments.md
(section E6.7 — design, frozen 48-turn script, checks P1–P8,
what-is-not-claimed). The band: GEOMETRY-ADVANCED (rectangle
perimeter/area, triangle area, area comparison — the product
corridor) learns the SAME TIME as 1-D VECTORS/STATICS (net
displacement, moment F·d, lever balance — moment is the product
corridor again, the lever is the taking corridor's third door),
and the ALIGNMENT is structural:
  (a) ONE CORRIDOR, MANY DOORS — distance (band 2), area, moment
      and perimeter×2 all derive through the same grounded
      repeated-addition helper; algebra division (band 2), pace
      (band 2) and lever force all derive through the same
      repeated-taking helper. The frozen twin probes measure the
      doors byte-equal (same chain cites, only the rule fact
      differs).
  (b) the stored prereq edges ARE the alignment: stat-moment ←
      geom-area (cross-domain, intra-band), geom-area-triangle ←
      alg-inverse-mul and stat-balance ← alg-inverse-mul
      (cross-domain, cross-band — pointing at band-2 concepts from
      the seed), measured from the FINAL store (edges established
      + active, prereq gaps empty at the band end).
The line bounds compose: THREE measured walls — the PRODUCT wall
(9×9 = 81 off the line, through BOTH the area and the moment
door), the NEGATIVE wall (a net west of the start is past the
line's origin), the INEXACT walls (½·35, 30/4 leave remainders).
Band 3 writes ZERO successor facts (line end stays 72 — the line
now serves four domains).

The run continues from the OFFICIAL e6.6 final store
(375 assertions, line end 72, eighteen concepts stable, one
established kin phrasing, ten rule facts, the band-2 stored
prereq edges), sessions S2–S4, official arm = det (no Ollama; a
live addendum, if run, is separately labelled per the
E5.4/E6.4/E6.5/E6.6 precedent).
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_ALG_MUL,
    CONCEPT_BAND2,
    CONCEPT_BAND3,
    CONCEPT_GEO_AREA,
    CONCEPT_GEO_PERIM,
    CONCEPT_GEO_TRI,
    CONCEPT_STA_BAL,
    CONCEPT_STA_MOM,
    CONCEPT_STA_NET,
    RULE_LESSONS,
)
from kainos.tutor.mastery import Concept, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E67", "FROZEN", "E6_7Experiment", "run_e6_7"]

CHECKS = 8

#: The official e6.6 final store (the seed; M8 of the E6.5/E6.6 lineage), repo-relative.
E66_SEED = Path("results/phase-6/e6.6-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E66_SEED.exists():
        return E66_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E66_SEED
    return alt if alt.exists() else E66_SEED


#: The E6.7 curriculum: everything the band ends carrying (six numerics,
#: phrasology, the band-1 geometry strip, the band-2 aligned strip, the
#: band-3 product strip).
CONCEPTS_E67: tuple = (
    InfantRuntime.PILOT_CONCEPTS
    + (
        Concept(
            "phrasology",
            "Phrasology — learned intake phrasings",
            "k-5",
            "language",
        ),
        Concept(
            "shape-triangle",
            "The triangle (sides and corners)",
            "k-5",
            "geometry",
            prereqs=("count-successor",),
        ),
        Concept(
            "shape-square",
            "The square (sides and corners)",
            "k-5",
            "geometry",
            prereqs=("count-successor",),
        ),
        Concept(
            "shape-rectangle",
            "The rectangle (sides and corners)",
            "k-5",
            "geometry",
            prereqs=("count-successor",),
        ),
        Concept(
            "shape-circle",
            "The circle (no sides, no corners)",
            "k-5",
            "geometry",
            prereqs=("count-successor",),
        ),
    )
    + CONCEPT_BAND2
    + CONCEPT_BAND3
)


FROZEN: dict = {
    "seed": str(E66_SEED),
    "sessions": [2, 3, 4],
    "seed_total": 375,
    "line_end_start": 72,
    "line_end_final": 72,  # band 3 writes ZERO successor facts
    "script": {
        2: [
            "what is the area of a 6 by 4 rectangle?",
            "the area of a rectangle is the length times the width",
            "what is the area of a 6 by 4 rectangle?",
            "what is the area of a 8 by 9 rectangle?",
            "what is the area of a 9 by 9 rectangle?",
            "the perimeter of a rectangle is twice what you get by adding the length to the width",
            "what is the perimeter of a 6 by 4 rectangle?",
            "what is the perimeter of a 12 by 9 rectangle?",
            "the area of a triangle is half of the base times the height",
            "what is the area of a triangle with base 6 and height 5?",
            "what is the area of a triangle with base 8 and height 9?",
            "what is the area of a triangle with base 5 and height 7?",
            "is a 4 by 6 rectangle bigger than a 3 by 8 rectangle?",
            "is a 7 by 6 rectangle bigger than a 8 by 5 rectangle?",
            "a cart leaving 5 at 6 a minute: where is it after 4 minutes?",
            "what is the perimeter of a 29 by 7 rectangle?",
        ],
        3: [
            "what is the moment of a 6 newton force at 4 meters?",
            "a moment is the force times its distance from the pivot",
            "what is the moment of a 6 newton force at 4 meters?",
            "what is the moment of a 8 newton force at 9 meters?",
            "what is the moment of a 9 newton force at 9 meters?",
            "moving east then west, the net is what is left after you take the west part away from the east part",
            "a cart moves 12 meters east then 5 meters west: how far from the start?",
            "a cart moves 20 meters east then 20 meters west: how far from the start?",
            "a cart moves 5 meters east then 8 meters west: how far from the start?",
            "a beam balances when the moment on one side equals the moment on the other",
            "a beam balances a 4 newton at 6 meters against what force at 3 meters?",
            "a beam balances a 5 newton at 8 meters against what force at 4 meters?",
            "a beam balances a 5 newton at 6 meters against what force at 4 meters?",
            "3 times x is 24: what is x?",
            "what is the moment of a 5 newton force at 8 meters?",
            "a beam balances a 7 newton at 8 meters against what force at 7 meters?",
        ],
        4: [
            "what is the area of a 7 by 8 rectangle?",
            "what is the moment of a 7 newton force at 8 meters?",
            "what is the perimeter of a 8 by 10 rectangle?",
            "what is the area of a triangle with base 9 and height 8?",
            "is a 4 by 9 rectangle bigger than a 6 by 6 rectangle?",
            "a cart moves 45 meters east then 9 meters west: how far from the start?",
            "a cart moves 9 meters east then 11 meters west: how far from the start?",
            "a beam balances a 3 newton at 8 meters against what force at 4 meters?",
            "a beam balances a 6 newton at 7 meters against what force at 6 meters?",
            "what is the moment of a 9 newton force at 9 meters?",
            "what is the area of a 9 by 9 rectangle?",
            "what is the area of a triangle with base 6 and height 9?",
            "a cart moves 45 meters east then 9 meters west: how far from the start?",
            "what is the perimeter of a 17 by 19 rectangle?",
            "72 - 58 is what?",
            "a beam balances a 8 newton at 6 meters against what force at 4 meters?",
        ],
    },
    "total_turns": 48,
    # P2: the per-session DOMAIN sequence (frozen: concurrency is
    # SCRIPTED, not emergent) — G geometry-advanced, S statics,
    # B a band-2 concept applied, N numeric, U pre-teach gap
    # (honest impossible), H honest boundary (the three walls).
    "domain_sequence": {
        2: "UGGGHGGGGGGHGGBG",
        3: "USSSHSSSHSSSHBSS",
        4: "GSGGGSHSSHHGSGNS",
    },
    # P2: the pre-teach honest gaps (frozen refs)
    "pre_teach_gaps": {
        "S02:01": CONCEPT_GEO_AREA,
        "S03:01": CONCEPT_STA_MOM,
    },
    # P4: the THREE band-3 walls (frozen refs + note)
    "wall_probes": {
        "S02:05": "product wall: 81 off the line (the 9-12 square probe, the area door)",
        "S03:05": "product wall: the SAME 81 through the moment door (domain-agnostic)",
        "S04:11": "product wall reproduced, area door",
        "S04:10": "product wall reproduced, moment door",
        "S03:09": "negative wall: 3 past the start (grounded difference)",
        "S04:07": "negative wall reproduced: 2 past the start",
    },
    "inexact_probes": {
        "S02:12": "triangle: half of 35 leaves 1",
        "S03:13": "lever: 30 taken in 4s leaves 2",
    },
    "negative_articulation": "does not reach past the start",
    # on-line maximals that still derive (the walls are measured knees)
    "on_line_maximals": {
        "S02:04": "72",  # 8 x 9 area
        "S02:16": "72",  # perimeter 29 by 7
        "S03:04": "72",  # 8 N at 9 m moment
        "S02:11": "36",  # half of 72
        "S04:12": "27",  # half of 54
        "S04:14": "72",  # perimeter 17 by 19
        "S04:15": "14",  # 72 - 58 (numeric, maximal walk-back)
    },
    # P3: the exact grounded band-3 derivations (frozen expected
    # answers; all must be `derived` with non-empty grounded evidence
    # that includes the concept's rule fact)
    "derived_table": {
        "S02:03": "24",  # 6 x 4 area
        "S02:07": "20",  # perimeter 6 by 4
        "S02:08": "42",  # perimeter 12 by 9
        "S02:10": "15",  # triangle 6 x 5 halved
        "S02:13": "no",  # 24 = 24 (equal)
        "S02:14": "yes",  # 42 > 40
        "S03:03": "24",  # moment 6 N at 4 m (twin of the area)
        "S03:07": "7",  # 12 east, 5 west
        "S03:08": "0",  # 20 east, 20 west (at the start)
        "S03:11": "8",  # lever: 24 taken in 3s
        "S03:12": "10",  # lever: 40 taken in 4s
        "S03:15": "40",  # 5 N at 8 m
        "S03:16": "8",  # 7 N at 8 m against 7 m
        "S04:01": "56",  # 7 x 8 area
        "S04:03": "36",  # perimeter 8 by 10
        "S04:04": "36",  # triangle 9 x 8 halved (72/2)
        "S04:05": "no",  # 36 = 36 (equal)
        "S04:06": "36",  # 45 east, 9 west
        "S04:08": "6",  # 24 taken in 4s
        "S04:09": "7",  # 42 taken in 6s
        "S04:13": "36",  # 45 east, 9 west (repeat)
        "S04:16": "12",  # 48 taken in 4s
    },
    # P5: the alignment twins (one corridor, many doors — the SAME
    # numbers through the different doors must cite byte-equal
    # chains, differing only in the rule fact)
    "product_twins": [
        {
            "area": "S02:03",  # 6 x 4 = 24
            "moment": "S03:03",  # 6 N at 4 m = 24
            "answer": "24",
            "area_rule": f"cap:{CONCEPT_GEO_AREA}:rule",
            "moment_rule": f"cap:{CONCEPT_STA_MOM}:rule",
        },
        {
            "area": "S04:01",  # 7 x 8 = 56
            "moment": "S04:02",  # 7 N at 8 m = 56
            "answer": "56",
            "area_rule": f"cap:{CONCEPT_GEO_AREA}:rule",
            "moment_rule": f"cap:{CONCEPT_STA_MOM}:rule",
        },
    ],
    "taking_twin": {
        "balance": "S03:11",  # 4 N at 6 m against ? at 3 m -> 8
        "algebra": "S03:14",  # 3 times x is 24 -> 8
        "answer": "8",
        "balance_rule": f"cap:{CONCEPT_STA_BAL}:rule",
        "algebra_rule": f"cap:{CONCEPT_ALG_MUL}:rule",
    },
    # P5: the STORED alignment edges (the cross-domain prereqs that
    # ARE the alignment — queried from the final store)
    "alignment_prereqs": {
        CONCEPT_STA_MOM: (CONCEPT_GEO_AREA,),  # cross-domain, intra-band
        CONCEPT_GEO_TRI: (
            CONCEPT_ALG_MUL,
        ),  # cross-domain, cross-band (halving rides band 2)
        CONCEPT_STA_BAL: (
            CONCEPT_ALG_MUL,
        ),  # cross-domain, cross-band (lever rides band 2)
    },
    # P6: the surface strip composes ACROSS bands
    "cross_band_phrasing": {
        "fact_ref": "phrasing:S03:16",  # the band-2 kin phrasing, in the seed
        "applied": ["S02:15"],
        "expected_answer": "29",
        "expected_parse_source": "lexicon:phrasing:S03:16",
    },
    # P7: the JOINT band-end evaluation (ONE frozen probe set, ONE
    # check, both domains — geometry-advanced ∥ vectors/statics)
    "band_end_probes": {
        "S04:01": "56",
        "S04:02": "56",
        "S04:03": "36",
        "S04:04": "36",
        "S04:05": "no",
        "S04:06": "36",
        "S04:07": "needs_info",  # the negative wall (2 past the start)
        "S04:08": "6",
        "S04:09": "7",
        "S04:10": "needs_info",  # the product wall (moment door)
        "S04:11": "needs_info",  # the product wall (area door)
        "S04:12": "27",
        "S04:13": "36",
        "S04:14": "72",
        "S04:15": "14",
        "S04:16": "12",
    },
    # P8: mastery at the band end (K = 4 is the bar)
    "mastery_expected": {
        CONCEPT_GEO_PERIM: {"state": "stable", "correct": 5},
        CONCEPT_GEO_AREA: {"state": "stable", "correct": 6},
        CONCEPT_GEO_TRI: {"state": "stable", "correct": 4},
        CONCEPT_STA_NET: {"state": "stable", "correct": 4},
        CONCEPT_STA_MOM: {"state": "stable", "correct": 4},
        CONCEPT_STA_BAL: {"state": "stable", "correct": 6},
    },
    # P8: the eighteen seed/band-1/band-2 concepts remain stable
    # (band 3 regressed nothing across TWO prior bands)
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
        "alg-inverse-1step",
        "alg-inverse-mul",
        "alg-two-step",
        "kin-distance",
        "kin-position",
        "kin-solve-time",
        "kin-rate",
    ],
    "gap_articulation": "not a capability i have been taught",
    "line_wall_articulation": "my number line ends at 72",
    "inexact_articulation": "not a whole number on my line",
    # frozen from the control run (the official run must reproduce):
    # 375 seed + 20 new fact assertions (6 band-3 rule lessons + 6
    # curriculum facts + 8 band-3 prereq edges) + N mastery-event
    # assertions (events are store data, P11)
    "final_total": 441,
    "new_facts": 20,
    "new_events": 46,
}

#: frozen dataset identity
SCRIPT_HASH = hashlib.sha256(
    json.dumps(
        {s: [t for t in ls] for s, ls in sorted(FROZEN["script"].items())},
        sort_keys=True,
    ).encode("utf-8")
).hexdigest()[:16]

_RULE_CONCEPT = {cid for _, (cid, _, _) in RULE_LESSONS.items()}


def _line_end(store) -> int:
    end = 0
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        sid, oid = a.subject.id, a.object_id
        if (
            sid.startswith("count-successor:succ-of(")
            and oid.startswith("count-successor:num(")
            and (a.validity is None or a.validity.to is None)
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
    G geometry-advanced, S statics, B band-2 concept applied,
    N numeric, U pre-teach gap, H honest boundary. Pure function of
    the turn record."""

    ir = t.get("response_ir") or {}
    slots = t.get("slots") or {}
    if t["kind"] == "ambiguous":
        return "B"
    if ir.get("uncertainty_state") == "needs_info":
        return "H"
    if t["kind"] == "impossible":
        return "U"
    concept = t.get("concept")
    if isinstance(concept, str):
        if concept.startswith("geom-"):
            return "G"
        if concept.startswith("stat-"):
            return "S"
        if concept.startswith(("alg-", "kin-")):
            return "B"
    rule = slots.get("rule")
    if isinstance(rule, str) and rule in RULE_LESSONS:
        cid = RULE_LESSONS[rule][0]
        if cid.startswith("geom-"):
            return "G"
        if cid.startswith("stat-"):
            return "S"
    return "N"


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E67)
    out: list[dict] = []
    for s in FROZEN["sessions"]:
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.6 S4 store, id-for-id."""

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


def run_e6_7(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.6 S4 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P1–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: dict[str, list[dict]] = {}
    for name in ("e6.7-run1", "e6.7-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.6 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed (M8)
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — the owner's
    # directives as data, with band 3's official evidence
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E67}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.7-run1", "e6.7-run2"):
        (out_dir / name / "e6.7-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return report


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.7-run1"]:
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
        "arm": {
            "classifier": "det",
            "llm_arm": "skipped-no-backend",
            "note": "hermetic official: no Ollama, no backend",
        },
        "turns": turns,
        "seed": str(E66_SEED),
        "script_hash": SCRIPT_HASH,
        "alignment_prereqs": {
            k: list(v) for k, v in FROZEN["alignment_prereqs"].items()
        },
    }


def _ir_answer(t: dict) -> Any:
    return (t.get("response_ir") or {}).get("answer")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.7-run1"
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
    checks["p1_script_contract"] = {
        "pass": not p1_bad,
        "bad": p1_bad,
        "turns": len(turns),
    }

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
        actual = "".join(
            turns[f"S{s:02d}:{tn:02d}"]["domain"]
            for tn, _ in enumerate(FROZEN["script"][s], 1)
        )
        if actual != frozen_seq:
            p2_bad.append(
                f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}"
            )
    checks["p2_honest_gaps_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — exact grounded derivations (both band-3 domains; each cites
    # its RULE FACT + the line steps)
    p3_bad: list[str] = []
    concept_by_mode = {
        "geo-perim": CONCEPT_GEO_PERIM,
        "geo-area": CONCEPT_GEO_AREA,
        "geo-cmp": CONCEPT_GEO_AREA,  # comparison rides the AREA concept
        "geo-tri": CONCEPT_GEO_TRI,
        "sta-net": CONCEPT_STA_NET,
        "sta-mom": CONCEPT_STA_MOM,
        "sta-bal": CONCEPT_STA_BAL,
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
            p3_bad.append(
                f"{ref}: not a grounded derivation ({ir.get('uncertainty_state')})"
            )
        if not t["grounded"]:
            p3_bad.append(f"{ref}: zero grounded evidence")
        mode = (t.get("slots") or {}).get("mode")
        cid_b3 = concept_by_mode.get(mode, "") if isinstance(mode, str) else ""
        rule_id = f"cap:{cid_b3}:rule" if cid_b3 else ""
        if rule_id and rule_id not in (ir.get("evidence") or []):
            p3_bad.append(f"{ref}: the rule fact {rule_id} is not cited")
    # the INEXACT probes: honest, not rounded
    for ref, note in FROZEN["inexact_probes"].items():
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing {ref} ({note})")
            continue
        if str(_ir_answer(t) or "")[:11] != "needs_info:":
            p3_bad.append(
                f"{ref}: the inexact probe must be needs_info (got {_ir_answer(t)!r})"
            )
        if FROZEN["inexact_articulation"] not in (t["response_text"] or ""):
            p3_bad.append(f"{ref}: the inexact articulation is missing ({note})")
        if t["grounded"]:
            p3_bad.append(
                f"{ref}: an inexact probe cited derivation evidence (fabrication)"
            )
    checks["p3_exact_grounded_derivations"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "derived": len(FROZEN["derived_table"]),
        "inexact": list(FROZEN["inexact_probes"]),
    }

    # P4 — THE THREE band-3 walls compose (product / negative / inexact)
    p4_bad: list[str] = []
    for ref, note in FROZEN["wall_probes"].items():
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref} ({note})")
            continue
        if str(_ir_answer(t) or "")[:11] != "needs_info:":
            p4_bad.append(
                f"{ref}: the wall probe must be needs_info (got {_ir_answer(t)!r})"
            )
        if "negative wall" in note:
            if FROZEN["negative_articulation"] not in (t["response_text"] or ""):
                p4_bad.append(
                    f"{ref}: the negative-wall articulation is missing ({note})"
                )
            # the grounded difference IS cited (real, not fabricated)
            if not t["grounded"]:
                p4_bad.append(f"{ref}: the grounded difference is not cited ({note})")
        else:  # the product wall: nothing is cited (the product is off the line)
            if FROZEN["line_wall_articulation"] not in (t["response_text"] or ""):
                p4_bad.append(f"{ref}: the line-end articulation is missing ({note})")
            if t["grounded"]:
                p4_bad.append(
                    f"{ref}: a product-wall probe cited evidence (fabrication)"
                )
    for ref, expected in FROZEN["on_line_maximals"].items():
        t = turns.get(ref)
        if t is None or _ir_answer(t) != expected:
            p4_bad.append(
                f"{ref}: the on-line maximal must answer {expected} (got {_ir_answer(t) if t else None!r})"
            )
    checks["p4_three_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "walls": list(FROZEN["wall_probes"]),
        "inexact": list(FROZEN["inexact_probes"]),
    }

    # P5 — the alignment is literal: one corridor, many doors
    p5_bad: list[str] = []
    for tw in FROZEN["product_twins"]:
        ta, tm = turns.get(tw["area"]), turns.get(tw["moment"])
        if ta is None or tm is None:
            p5_bad.append(f"product twin refs missing ({tw['area']}/{tw['moment']})")
            continue
        if _ir_answer(ta) != tw["answer"] or _ir_answer(tm) != tw["answer"]:
            p5_bad.append(
                f"{tw['area']}/{tw['moment']}: twin answers {_ir_answer(ta)!r} / {_ir_answer(tm)!r} (both {tw['answer']})"
            )
        ea = list(ta["response_ir"].get("evidence") or [])
        em = list(tm["response_ir"].get("evidence") or [])
        if ea[-1] != tw["area_rule"] or em[-1] != tw["moment_rule"]:
            p5_bad.append(
                f"{tw['area']}/{tw['moment']}: twin rule facts {ea[-1]!r} / {em[-1]!r}"
            )
        if sorted(ea[:-1]) != sorted(em[:-1]):
            p5_bad.append(
                f"{tw['area']}/{tw['moment']}: the two doors must cite the SAME product chain"
            )
    tt = FROZEN["taking_twin"]
    tb, tx = turns.get(tt["balance"]), turns.get(tt["algebra"])
    if tb is None or tx is None:
        p5_bad.append("taking twin refs missing")
    else:
        if _ir_answer(tb) != tt["answer"] or _ir_answer(tx) != tt["answer"]:
            p5_bad.append(
                f"taking twin answers: {_ir_answer(tb)!r} / {_ir_answer(tx)!r} (both {tt['answer']})"
            )
        eb = list(tb["response_ir"].get("evidence") or [])
        ex = list(tx["response_ir"].get("evidence") or [])
        if eb[-1] != tt["balance_rule"] or ex[-1] != tt["algebra_rule"]:
            p5_bad.append(f"taking twin rule facts: {eb[-1]!r} / {ex[-1]!r}")
        # the algebra door's evidence IS the taking chain (every algebra
        # cite appears in the balance evidence; the balance door adds the
        # product chain on top)
        taking = [c for c in ex if c != tt["algebra_rule"]]
        if not taking or any(c not in eb for c in taking):
            p5_bad.append(
                "the algebra taking cites are not shared by the balance evidence"
            )
        if len(eb) <= len(ex):
            p5_bad.append(
                "the balance door must cite MORE (the product chain + the shared taking)"
            )
    # the STORED alignment edges: established + active in the final store
    from kainos.tutor.mastery import concept as _concept
    from kainos.tutor.mastery import mastery_view

    _declared = {c.id: frozenset(c.prereqs) for c in CONCEPT_BAND3}
    for cid, pres in FROZEN["alignment_prereqs"].items():
        if not frozenset(pres) <= _declared[cid]:
            p5_bad.append(
                f"{cid}: the alignment prereqs {tuple(pres)} are not declared in CONCEPT_BAND3"
            )
        got = frozenset(_concept(cid).prereqs)
        if got != _declared[cid]:
            p5_bad.append(
                f"{cid}: runtime prereqs {sorted(got)} != declared {sorted(_declared[cid])}"
            )
        for pre in pres:
            edge_id = f"curriculum:prereq:{cid}>{pre}"
            edge = final.get(edge_id)
            if edge is None or (
                edge.validity is not None and edge.validity.to is not None
            ):
                p5_bad.append(
                    f"{cid}: the stored alignment edge {edge_id} is missing/inactive in the final store"
                )
    # ALL band-3 prereq edges (alignment included) in the final store
    for c in CONCEPT_BAND3:
        for pre in c.prereqs:
            edge_id = f"curriculum:prereq:{c.id}>{pre}"
            edge = final.get(edge_id)
            if edge is None or (
                edge.validity is not None and edge.validity.to is not None
            ):
                p5_bad.append(
                    f"band-3 edge {edge_id} missing/inactive in the final store"
                )
    # the STORE PRECONDITIONS: all six band-3 concepts show EMPTY
    # prereq gaps at the band end (the cross-band edges included)
    mv = mastery_view(final, [c.id for c in CONCEPT_BAND3])
    for cid in mv:
        if mv[cid].prereq_gaps:
            p5_bad.append(f"{cid}: prereq gaps {mv[cid].prereq_gaps} at the band end")
    checks["p5_alignment"] = {
        "pass": not p5_bad,
        "bad": p5_bad,
        "product_twins": FROZEN["product_twins"],
        "taking_twin": tt,
        "stored_edges": [
            f"curriculum:prereq:{cid}>{pre}"
            for cid, pres in FROZEN["alignment_prereqs"].items()
            for pre in pres
        ],
    }

    # P6 — the surface strip composes ACROSS bands
    p6_bad: list[str] = []
    cb = FROZEN["cross_band_phrasing"]
    t = turns.get(cb["applied"][0])
    if t is None:
        p6_bad.append(f"missing {cb['applied'][0]}")
    else:
        if _ir_answer(t) != cb["expected_answer"]:
            p6_bad.append(
                f"{cb['applied'][0]}: {_ir_answer(t)!r} != {cb['expected_answer']!r}"
            )
        if t.get("parse_source") != cb["expected_parse_source"]:
            p6_bad.append(
                f"{cb['applied'][0]}: parse_source {t.get('parse_source')!r} != {cb['expected_parse_source']!r}"
            )
        if not t["grounded"]:
            p6_bad.append(f"{cb['applied'][0]}: the cross-band phrasing cited nothing")
    # the surface never FORGETS, only grows: every phrasing established
    # in the seed is still established in the final store
    from kainos.tutor.brainstem import REL_PHRASING

    seed_path = _resolve_seed()
    seed_store = load_store(seed_path)
    seed_est = {
        a.id
        for a in seed_store.query(relation=REL_PHRASING)
        if a.validity is None or a.validity.to is None
    }
    final_est = {
        a.id
        for a in final.query(relation=REL_PHRASING)
        if a.validity is None or a.validity.to is None
    }
    forgotten = seed_est - final_est
    if forgotten:
        p6_bad.append(
            f"phrasings that were established in the seed are no longer established: {sorted(forgotten)}"
        )
    shrunk = [
        a.id
        for a in final.query(relation=REL_PHRASING)
        if (a.validity is not None and a.validity.to is not None)
    ]
    if len(final_est) + len(shrunk) < len(seed_est):
        p6_bad.append(
            f"established phrasings shrank: seed {len(seed_est)} -> final {len(final_est)}"
        )
    if cb["fact_ref"] not in final_est:
        p6_bad.append(f"{cb['fact_ref']} is not established in the final store")
    # zero open disputes
    from kainos.codex.models import EpistemicState

    disputes = [
        a
        for a in final.query()
        if a.status == EpistemicState.disputed
        and (a.validity is None or a.validity.to is None)
    ]
    if disputes:
        p6_bad.append(f"{len(disputes)} open disputes at the band end")
    checks["p6_surface_composes"] = {
        "pass": not p6_bad,
        "bad": p6_bad,
        "cross_band": cb,
        "established_seed": len(seed_est),
        "established_final": len(final_est),
    }

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
        {
            "ref": ref,
            "domain": turns[ref]["domain"],
            "family": _family(turns[ref]),
            "answer": _ir_answer(turns[ref]),
        }
        for ref in sorted(FROZEN["band_end_probes"])
    ]
    checks["p7_joint_band_end"] = {
        "pass": not p7_bad,
        "bad": p7_bad,
        "joint_table": joint_table,
    }

    # P8 — mastery of the ALIGNED band + determinism + seed continuity
    p8_bad: list[str] = []
    seed = _seed_check(run1_root)
    if seed["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed['seed_total']} != {FROZEN['seed_total']}")
    if seed["reproduced_in_s2_pre"] != FROZEN["seed_total"] or seed["missing"]:
        p8_bad.append(f"seed continuity: {seed}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(
            f"line end {_line_end(final)} != {FROZEN['line_end_final']} (band 3 must write zero successor facts)"
        )
    all_final = list(final.query())
    if FROZEN["final_total"] is not None and len(all_final) != FROZEN["final_total"]:
        p8_bad.append(
            f"final store total {len(all_final)} != frozen {FROZEN['final_total']}"
        )
    seed_ids = {a.id for a in seed_store.query()}
    new = [a for a in all_final if a.id not in seed_ids]
    new_events = [
        a for a in new if (a.context.data or {}).get("kind") == "mastery-event"
    ]
    new_facts = [
        a for a in new if (a.context.data or {}).get("kind") != "mastery-event"
    ]
    if FROZEN["new_facts"] is not None and len(new_facts) != FROZEN["new_facts"]:
        p8_bad.append(
            f"new facts {len(new_facts)} != frozen {FROZEN['new_facts']}: {sorted(a.id for a in new_facts)}"
        )
    if FROZEN["new_events"] is not None and len(new_events) != FROZEN["new_events"]:
        p8_bad.append(
            f"new mastery events {len(new_events)} != frozen {FROZEN['new_events']}"
        )
    mv = mastery_view(final, [c.id for c in CONCEPTS_E67])
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
            p8_bad.append(
                f"{cid}: band 1/2/seed concept regressed ({v.state if v else 'absent'})"
            )
    # determinism
    r1 = runs["e6.7-run1"]
    r2 = runs["e6.7-run2"]
    a = json.dumps(r1, sort_keys=True)
    b = json.dumps(r2, sort_keys=True)
    if a != b:
        p8_bad.append("run1 != run2")
    det_arm = all(
        (t.get("arm") or {}).get("classifier") == "det"
        for srow in r1
        for t in srow.get("turns", [])
    )
    if not det_arm:
        p8_bad.append("a turn was not the det arm")
    checks["p8_mastery_determinism"] = {
        "pass": not p8_bad,
        "bad": p8_bad,
        "mastery": {
            cid: {"state": mv[cid].state, "correct": mv[cid].correct_derivations}
            for cid in FROZEN["mastery_expected"]
            if cid in mv
        },
        "seed": seed,
        "line_end": _line_end(final),
        "final_total": len(all_final),
        "new_facts": [a2.id for a2 in new_facts],
        "new_events": len(new_events),
        "run_identity": hashlib.sha256(a.encode("utf-8")).hexdigest()[:16],
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    value = (
        f"PASS e6.7: {passed}/{len(checks)}"
        if passed == len(checks)
        else f"FAIL e6.7: {passed}/{len(checks)}"
    )
    return {"checks": checks, "passed": passed, "value": value}


class E6_7Experiment:
    """E6.7 — band 3: geometry-advanced ∥ vectors/statics (the product band)."""

    name = "e6.7"
    hypothesis = (
        "Geometry-advanced ∥ vectors/statics learns as ONE aligned band (9–12), the PRODUCT BAND: "
        "rectangle perimeter/area and triangle area (the math side) and 1-D net displacement, "
        "moment F·d and lever balance (the physics side) ride the same teachable-strip seam, and "
        "the alignment is ONE corridor with many doors — area, moment, perimeter×2 and distance "
        "all derive through the same grounded product helper (twin probes byte-equal, only the "
        "rule fact differs), while the lever is the repeated-taking corridor's third door after "
        "algebra division and pace; the alignment is stored, not described (stat-moment ← "
        "geom-area, geom-area-triangle ← alg-inverse-mul, stat-balance ← alg-inverse-mul — "
        "cross-domain, cross-band edges from the seed, established in the final store, prereq "
        "gaps empty); THREE measured walls compose (9×9 = 81 off the line through BOTH the area "
        "and the moment door — the wall is domain-agnostic; a net west of the start is the "
        "negative wall, past the line's origin; ½·35 and 30/4 are inexact, never rounded); the "
        "band-2 kin phrasing from the seed composes across bands (parsed via the learned "
        "phrasing, grounded); the band ENDS on a JOINT evaluation — one frozen probe set "
        "spanning both domains, all six band-3 concepts stable (K = 4) against the eighteen "
        "seed/band-1/band-2 concepts, line untouched at 72 (now serving four domains), two runs "
        "byte-identical."
    )
    metric = "band-3 checks passed (P1..P8)"
    threshold = "8/8"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_7()
        if "error" in report:
            return Result(
                name=self.name,
                passed=False,
                value=0.0,
                evidence=[Path("results/phase-6")],
                config={"seed": FROZEN["seed"], "error": report["error"]},
            )
        return Result(
            name=self.name,
            passed=report["passed"] == CHECKS,
            value=report["value"],
            evidence=[
                Path("results/phase-6/e6.7-run1/session-S02.json"),
                Path("results/phase-6/e6.7-run1/session-S03.json"),
                Path("results/phase-6/e6.7-run1/session-S04.json"),
                Path("results/phase-6/e6.7-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
