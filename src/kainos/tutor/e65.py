"""E6.5 — "The K–5 Band: numerics ∥ geometry (band 1 of the M3 band
sweep)" (T7 #157; the owner's 2026-08-22 directives, comment 450).

Pre-registered in plan/30-phases/phase-6-tutor/experiments.md
(section E6.5 — design, frozen 48-turn script, checks P1–P8,
what-is-not-claimed). The band: geometry learns CONCURRENTLY with
math from K–5 (second domain strip on the same teachable-strip seam:
shape lessons as rule-gated store definitions, shape drills as the
two-family grammar, shape question families INSIDE the phrasology
strip with vocabulary slots) — and the band ends on a JOINT
evaluation (one frozen probe set spanning both domains, one check),
with all four shape concepts verified `stable` (K = 4) at the band
end against the seed-stable numerics. One line, two domains: the
geometry strip writes ZERO successor facts (line end stays 72).

The run continues from the OFFICIAL e6.4 final store (245 assertions,
line end 72, all six numeric concepts stable, phrasology stable),
sessions S2–S4, official arm = det (no Ollama; a live addendum, if
run, is separately labelled per the E5.4/E6.4 precedent).
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import EpistemicState
from kainos.tutor.brainstem import REL_PHRASING, REL_POLICY, SHAPES, det_classify
from kainos.tutor.mastery import Concept, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E65", "FROZEN", "E6_5Experiment", "run_e6_5"]

CHECKS = 8

#: The official e6.4 final store (the seed; M8 of E6.4 lineage), repo-relative.
E64_SEED = Path("results/phase-6/e6.4-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E64_SEED.exists():
        return E64_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E64_SEED
    return alt if alt.exists() else E64_SEED

#: The E6.5 curriculum: the six numeric pilot concepts + the phrasology
#: strip + the band-1 geometry strip (directive #1: concurrent domains).
CONCEPTS_E65: tuple = InfantRuntime.PILOT_CONCEPTS + (
    Concept("phrasology", "Phrasology — learned intake phrasings", "k-5", "language"),
    Concept("shape-triangle", "The triangle (sides and corners)", "k-5", "geometry", prereqs=("count-successor",)),
    Concept("shape-square", "The square (sides and corners)", "k-5", "geometry", prereqs=("count-successor",)),
    Concept("shape-rectangle", "The rectangle (sides and corners)", "k-5", "geometry", prereqs=("count-successor",)),
    Concept("shape-circle", "The circle (no sides, no corners)", "k-5", "geometry", prereqs=("count-successor",)),
)

FROZEN: dict = {
    "seed": str(E64_SEED),
    "sessions": [2, 3, 4],
    "seed_total": 245,  # assertions in the official e6.4 S4 store
    "line_end_start": 72,
    "line_end_final": 72,  # the geometry strip writes ZERO successor facts
    "script": {
        2: [
            "what comes after 58?",
            "how many sides does a triangle have?",
            "the triangle has 3 sides and 3 corners",
            "how many sides does a triangle have?",
            "how many corners does a triangle have?",
            "17 + 25 is what?",
            "how many edges does a pentagon have?",
            "the square has 4 sides and 3 corners",
            "how many corners does a square have?",
            "no \u2014 that was a mistake; the square has 4 sides and 4 corners",
            "how many corners does a square have?",
            "9 * 8 is what?",
            'the phrasing "how many edges does a {shape} have?" is the same as "how many sides does a {shape} have?"',
            "how many edges does a triangle have?",
            "how many sides does a rectangle have?",
            "the rectangle has 4 sides and 4 corners",
        ],
        3: [
            "how many sides does a circle have?",
            "the circle has no sides and no corners",
            "how many sides does a circle have?",
            "how many corners does a circle have?",
            "33 - 14 is what?",
            'the phrasing "how many points does a {shape} have?" is the same as "how many sides does a {shape} have?"',
            "how many points does a triangle have?",
            'no \u2014 that was a mistake; the phrasing "how many points does a {shape} have?" is the same as "how many corners does a {shape} have?"',
            "how many points does a circle have?",
            "6 * 6 is what?",
            "is 38 larger than 29?",
            'the phrasing "how many sides does a {shape} have?" is the same as "what comes after {n}?"',
            "how many sides does a rectangle have?",
            "what number follows 63?",
        ],
        4: [
            "how many sides does a triangle have?",
            "how many corners does a triangle have?",
            "how many sides does a square have?",
            "how many corners does a square have?",
            "how many sides does a rectangle have?",
            "how many corners does a rectangle have?",
            "how many sides does a circle have?",
            "how many corners does a circle have?",
            "how many edges does a square have?",
            "how many points does a rectangle have?",
            "what comes after 72?",
            "26 + 9 is what?",
            "68 - 25 is what?",
            "4 * 9 is what?",
            "is 51 larger than 47?",
            "the number after 45 is 46",
            "what number follows 71?",
            "how many points does a circle have?",
        ],
    },
    "total_turns": 48,
    # The per-session DOMAIN sequence (frozen P2: concurrency is
    # SCRIPTED, not emergent) — N numeric, G geometry, B boundary
    # (honestly ambiguous surface event): the frozen values are filled
    # from the control run and match the script by construction.
    "domain_sequence": {
        # 2:  N G G G G N B G G G G N G G G G   (succ, tri gap/lesson/drills, add, pentagon-boundary, wrong-value square arc, mult, edges phrasing + drill, rectangle gap/lesson)
        2: "NGGGGNBGGGGNGGGG",
        # 3:  G G G G N G G G G N N B G N        (circle gap/lesson/drills, sub, points sibling-mapping arc, mult, cmp, slot-type rejection, rectangle drill, seed phrasing)
        3: "GGGGNGGGGNNBGN",
        # 4:  G..G G G N N N N N N N G            (the JOINT band-end set: 8 shape drills + 2 phrasings + line wall + 4 numeric families + 2 seed phrasings + points-circle composition)
        4: "GGGGGGGGGGNNNNNNNG",
    },
    # P2: the pre-teach honest gaps (frozen refs; the arc's honest half)
    "pre_teach_gaps": {
        "S02:02": "shape-triangle",
        "S02:15": "shape-rectangle",
        "S03:01": "shape-circle",
    },
    # P2: the out-of-band surface boundary (frozen ref + articulation class)
    "out_of_band_probe": "S02:07",
    # P3: the wrong-value arc (frozen refs; E6.4 S02:15 pattern)
    "wrong_value_arc": {
        "wrong_lesson": "S02:08",
        "wrong_probe": "S02:09",  # answers "3" while the wrong claimant is active
        "correction": "S02:10",
        "after_probe": "S02:11",  # answers "4" after the correction
    },
    # P3: the phrasology sibling-mapping arc (frozen refs)
    "sibling_arc": {
        "wrong_mapping": "S03:06",  # points phrasing -> the SIDES family
        "wrong_side_probe": "S03:07",  # parsed as sides (the value 3 is family-blind, recorded honestly)
        "correction": "S03:08",  # points phrasing -> the CORNERS family
        "corner_probe": "S03:09",  # circles points -> "none" via the corner family
    },
    # P4: the slot-type discipline (a vocabulary slot is never mapped
    # onto a number family) — honestly rejected, no store write
    "slot_type_rejection": "S03:12",
    # P4: the shape-phrasology applied turns (parse_source = lexicon:<shape fact>)
    "shape_phrasing_applied": ["S02:14", "S03:07", "S03:09", "S04:09", "S04:10", "S04:18"],
    # P4: the SEED phrasology still working THROUGH the band (parse_source
    # = lexicon:<seed fact> — the surface strip composes across bands)
    "seed_phrasing_applied": ["S03:14", "S04:16", "S04:17"],
    # P4: the shape-phrasing facts (frozen ids by turn of teaching)
    "shape_phrasing_facts": {
        "phrasing:S02:13": "pat:shape-sides",  # edges -> sides (established)
        "phrasing:S03:06": "pat:shape-sides",  # points -> sides (SUPERSEDED by S03:08)
        "phrasing:S03:08": "pat:shape-corners",  # points -> corners (established)
    },
    "shape_phrasing_established_final": 2,
    "shape_phrasing_superseded_final": 1,
    # P5: the frozen table (the world the band ends knowing)
    "shape_table": {
        "triangle": [3, 3],
        "square": [4, 4],
        "rectangle": [4, 4],
        "circle": ["none", "none"],
    },
    # P6: seed continuity (id-for-id)
    "seed_total_check": 245,
    # P7: the JOINT band-end evaluation (frozen expected values; ONE
    # probe set, ONE check, both domains — the T7 "probe -> verify")
    "band_end_probes": {
        "S04:01": "3",
        "S04:02": "3",
        "S04:03": "4",
        "S04:04": "4",
        "S04:05": "4",
        "S04:06": "4",
        "S04:07": "none",
        "S04:08": "none",
        "S04:09": "4",
        "S04:10": "4",
        "S04:11": "needs_info",  # the line wall (the geometry band did not move the line)
        "S04:12": "35",
        "S04:13": "43",
        "S04:14": "36",
        "S04:15": "yes",
        "S04:16": "assertion",  # corroborated numeric phrasing (assertion, established)
        "S04:17": "72",
        "S04:18": "none",
    },
    # P8: mastery at the band end (K = 4 is the bar; the script gives
    # each shape 4+ correct derivations)
    "mastery_expected": {
        "shape-triangle": {"state": "stable", "correct": 6},  # incl. S03:07 under the (then-wrong) sibling mapping — recorded honestly
        "shape-square": {"state": "stable", "correct": 5},  # S02:09 under the wrong claimant counts for the strip (the derivation was grounded)
        "shape-rectangle": {"state": "stable", "correct": 4},
        "shape-circle": {"state": "stable", "correct": 6},
    },
    "seed_numeric_stable": ["count-successor", "add-within-10", "add-two-digit", "sub-within-30", "mult-within-100", "compare-numbers"],
    "gap_articulation": "not a capability i have been taught",
    "rejection_articulation": "i can't take that as a mapping",
}

#: frozen dataset identity
SCRIPT_HASH = hashlib.sha256(
    json.dumps({s: [t for t in ls] for s, ls in sorted(FROZEN["script"].items())}, sort_keys=True).encode("utf-8")
).hexdigest()[:16]


def _line_end(store) -> int:
    end = 0
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        sid, oid = a.subject.id, a.object_id
        if sid.startswith("count-successor:succ-of(") and oid.startswith("count-successor:num(") and (a.validity is None or a.validity.to is None):
            end = max(end, int(oid[len("count-successor:num(") : -1]))
    return end


def _fresh_store(root: Path, s: int):
    p = codex_dump_path(root, s)
    if p is None or not p.exists():
        return InMemoryCodexStore()
    return load_store(p)


def _turn_domain(t: dict) -> str:
    """The per-turn domain for the frozen interleave check (P2):
    N numeric, G geometry, B boundary (an honestly ambiguous surface
    event). Pure function of the turn record."""

    if t["kind"] == "ambiguous":
        return "B"
    if isinstance(t.get("concept"), str) and t["concept"].startswith("shape-"):
        return "G"
    surface = t["surface"]
    if "phrasing" in surface and any(w in surface for w in ("triangle", "square", "rectangle", "circle", "{shape}")):
        return "G"
    return "N"


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E65)
    out: list[dict] = []
    for s in FROZEN["sessions"]:
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P6: the seed dump is the official e6.4 S4 store, id-for-id."""

    seed_path = _resolve_seed()
    seed = load_store(seed_path) if seed_path.exists() else None
    pre = _fresh_store(root, 2)
    seed_ids = {a.id for a in seed.query()} if seed is not None else set()
    pre_ids = {a.id for a in pre.query()}
    return {"seed_total": len(seed_ids), "reproduced_in_s2_pre": len(seed_ids & pre_ids), "missing": sorted(seed_ids - pre_ids)}


def _default_out_dir() -> Path:
    base = Path(os.environ.get("KAINOS_RESULTS_DIR", "results")) / "phase-6"
    base.mkdir(parents=True, exist_ok=True)
    return base


def run_e6_5(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.4 S4 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P1–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: dict[str, list[dict]] = {}
    for name in ("e6.5-run1", "e6.5-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.4 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed (M8)
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — the owner's
    # directives as data, with band 1's official evidence
    from kainos.tutor.bands import BAND_MAP, validate_band_map

    map_doc = {
        "bands": [
            {"name": b.name, "band": b.band, "domains": list(b.domains), "aligned_physics": list(b.aligned_physics),
             "concepts": list(b.concepts), "status": b.status, "evidence": list(b.evidence)}
            for b in BAND_MAP
        ],
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E65}),
    }
    (out_dir / "bands-map.json").write_text(json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.5-run1", "e6.5-run2"):
        (out_dir / name / "e6.5-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.5-run1"]:
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
                "parse_source": t["response_ir"].get("parse_source"),
                "memory_diff": t["memory_diff"],
                "domain": _turn_domain(t),
            }
    return {
        "arm": {"classifier": "det", "llm_arm": "skipped-no-backend", "note": "hermetic official: no Ollama, no backend"},
        "turns": turns,
        "seed": str(E64_SEED),
        "script_hash": SCRIPT_HASH,
    }


def _ir_answer(t: dict) -> Any:
    return (t.get("response_ir") or {}).get("answer")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.5-run1"
    final = _fresh_store(run1_root, 4)

    # P1 — script & contract
    p1_bad: list[str] = []
    if len(turns) != FROZEN["total_turns"]:
        p1_bad.append(f"{len(turns)} turns != {FROZEN['total_turns']}")
    for ref, t in turns.items():
        if not t["contract_valid"]:
            p1_bad.append(f"{ref}: contract invalid")
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
    oob = turns.get(FROZEN["out_of_band_probe"])
    if oob is None:
        p2_bad.append("S02:07 missing")
    else:
        if oob["kind"] != "ambiguous":
            p2_bad.append(f"S02:07: out-of-band shape parsed (got {oob['kind']})")
        if oob["memory_diff"] or oob["grounded"]:
            p2_bad.append("S02:07: the out-of-band probe wrote/cited the store")
    # the interleave (frozen domain sequence per session)
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    checks["p2_honest_gaps_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — the single-current-claimant arc (shapes + the phrasology mirror)
    p3_bad: list[str] = []
    wv = FROZEN["wrong_value_arc"]
    wrong_t, after_t = turns.get(wv["wrong_probe"]), turns.get(wv["after_probe"])
    if wrong_t is None or after_t is None:
        p3_bad.append("wrong-value arc refs missing")
    else:
        if _ir_answer(wrong_t) != "3":
            p3_bad.append(f"S02:09: the wrong value must answer 3 while active (got {_ir_answer(wrong_t)})")
        if _ir_answer(after_t) != "4":
            p3_bad.append(f"S02:11: the corrected value must answer 4 (got {_ir_answer(after_t)})")
    # the final claimants: EXACTLY ONE established per shape, matching the frozen table
    for shape, (sides, corners) in SHAPES.items():
        concept_id = f"shape-{shape}"
        est = [
            a
            for a in final.query(relation=REL_POLICY)
            if a.context.data.get("concept") == concept_id
            and a.context.data.get("kind") == "definition"
            and a.status == EpistemicState.established
            and (a.validity is None or a.validity.to is None)
        ]
        if len(est) != 1:
            p3_bad.append(f"{concept_id}: {len(est)} established claimants (expected 1)")
            continue
        fact = est[0]
        d = fact.context.data
        want_s = "none" if sides is None else str(sides)
        want_c = "none" if corners is None else str(corners)
        got_s = "none" if d.get("sides") is None else str(d.get("sides"))
        got_c = "none" if d.get("corners") is None else str(d.get("corners"))
        if [got_s, got_c] != [want_s, want_c]:
            p3_bad.append(f"{concept_id}: final claimant {got_s}/{got_c} != frozen table {want_s}/{want_c}")
    # the wrong square claimant: obsolete, validity ENDED, LINKED to its replacement
    sup = [
        a
        for a in final.query(relation=REL_POLICY)
        if a.context.data.get("concept") == "shape-square"
        and a.context.data.get("kind") == "definition"
        and a.status == EpistemicState.obsolete
    ]
    if len(sup) != 1:
        p3_bad.append(f"{len(sup)} obsolete square claimants (expected 1)")
    else:
        old = sup[0]
        if old.validity is None or old.validity.to is None:
            p3_bad.append("the obsolete square claimant's validity was not ended")
        new_id = [
            a.id
            for a in final.query(relation=REL_POLICY)
            if a.context.data.get("concept") == "shape-square"
            and a.status == EpistemicState.established
            and (a.validity is None or a.validity.to is None)
        ]
        linked = old.provenance is not None and any(e == new_id[0] for e in old.provenance.evidence) if new_id else False
        new_fact = final.get(new_id[0]) if new_id else None
        linked = linked or (new_fact is not None and new_fact.provenance is not None and old.id in new_fact.provenance.evidence)
        if not linked:
            p3_bad.append("the obsolete square claimant is not linked to its replacement")
    # the phrasology mirror: points phrasing on CORNERS, the sibling superseded
    facts = [a for a in final.query(relation=REL_PHRASING) if a.id in FROZEN["shape_phrasing_facts"]]
    if len(facts) != len(FROZEN["shape_phrasing_facts"]):
        p3_bad.append(f"{len(facts)} shape phrasing facts != {len(FROZEN['shape_phrasing_facts'])}")
    est_f = [a for a in facts if a.status == EpistemicState.established and (a.validity is None or a.validity.to is None)]
    obs_f = [a for a in facts if a.status == EpistemicState.obsolete]
    if len(est_f) != FROZEN["shape_phrasing_established_final"]:
        p3_bad.append(f"{len(est_f)} established shape phrasings (expected {FROZEN['shape_phrasing_established_final']})")
    if len(obs_f) != FROZEN["shape_phrasing_superseded_final"]:
        p3_bad.append(f"{len(obs_f)} superseded shape phrasings (expected {FROZEN['shape_phrasing_superseded_final']})")
    for fid, pat in FROZEN["shape_phrasing_facts"].items():
        f = final.get(fid)
        if f is None:
            p3_bad.append(f"{fid}: the frozen phrasing fact is gone")
            continue
        if f.object_id != pat:
            p3_bad.append(f"{fid}: maps to {f.object_id}, expected {pat}")
    # ZERO open disputes anywhere (shape definitions + all phrasings)
    open_disp = [a for a in final.query() if a.status == EpistemicState.disputed and (a.validity is None or a.validity.to is None)]
    if open_disp:
        p3_bad.append(f"open disputed assertions at the band end: {[a.id for a in open_disp]}")
    checks["p3_claimant_arc"] = {"pass": not p3_bad, "bad": p3_bad}

    # P4 — shape phrasology A/B + slot discipline
    p4_bad: list[str] = []
    for ref in FROZEN["shape_phrasing_applied"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        ps = t.get("parse_source") or ""
        if not ps.startswith("lexicon:"):
            p4_bad.append(f"{ref}: expected a lexicon parse (parse_source={ps})")
        elif ps.split(":", 1)[1] not in FROZEN["shape_phrasing_facts"]:
            p4_bad.append(f"{ref}: parsed via {ps.split(':', 1)[1]}, not a shape phrasing fact")
    for ref in FROZEN["seed_phrasing_applied"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        ps = t.get("parse_source") or ""
        if not ps.startswith("lexicon:"):
            p4_bad.append(f"{ref}: the seed phrasing must still parse via the lexicon (parse_source={ps})")
        elif final.get(ps.split(":", 1)[1]) is None:
            p4_bad.append(f"{ref}: the seed phrasing fact {ps} is gone from the final store")
    # the grammar-first discipline on canonical shape probes
    for ref, t in turns.items():
        if t["kind"] == "ambiguous":
            continue
        ps = t.get("parse_source") or ""
        g_kind, _ = det_classify(t["surface"])
        if g_kind != "ambiguous":
            if ps != "grammar":
                p4_bad.append(f"{ref}: the grammar matches but parse_source={ps}")
        elif ps is None or not ps.startswith("lexicon:"):
            p4_bad.append(f"{ref}: not grammar and not lexicon (parse_source={ps})")
    # the slot-type rejection (frozen ref): honestly rejected, NO store write
    rej = turns.get(FROZEN["slot_type_rejection"])
    if rej is None:
        p4_bad.append("S3:12 missing")
    else:
        if rej["kind"] != "ambiguous":
            p4_bad.append(f"S3:12: the slot-type mismatch mapped (got {rej['kind']})")
        if rej["memory_diff"]:
            p4_bad.append("S3:12: the rejected mapping wrote the store")
        if FROZEN["rejection_articulation"] not in (rej["response_text"] or ""):
            p4_bad.append(f"S3:12: the frozen rejection articulation is missing: {(rej['response_text'] or '')[:80]}")
    # the sibling arc: while wrong, parsed into the SIDE family (recorded
    # honestly: the value 3 is family-blind for a triangle — the FAMILY
    # change, not the value, is the evidence); after correction, the
    # corner family (the circle probe answers none via corners)
    sa = FROZEN["sibling_arc"]
    wp = turns.get(sa["wrong_side_probe"])
    cp = turns.get(sa["corner_probe"])
    if wp is None or cp is None:
        p4_bad.append("sibling arc refs missing")
    else:
        wpf = wp.get("parse_source") or ""
        cpf = cp.get("parse_source") or ""
        if not wpf.startswith("lexicon:phrasing:S03:06"):
            p4_bad.append(f"S03:07: not parsed via the (wrong) sibling mapping (parse_source={wpf})")
        if not cpf.startswith("lexicon:phrasing:S03:08"):
            p4_bad.append(f"S03:09: not parsed via the corrected mapping (parse_source={cpf})")
        if _ir_answer(cp) != "none":
            p4_bad.append(f"S03:09: the corner-family circle probe must answer none (got {_ir_answer(cp)})")
    checks["p4_shape_phrasology"] = {"pass": not p4_bad, "bad": p4_bad}

    # P5 — grounding & no-fabrication (re-auditable)
    p5_bad: list[str] = []
    for ref, t in turns.items():
        if t["kind"] != "question":
            continue
        ir = t["response_ir"]
        if ir.get("uncertainty_state") != "derived":
            continue  # honest needs_info is the other legitimate class (P2/P7 own it)
        if not t["grounded"]:
            p5_bad.append(f"{ref}: an ungrounded derived answer (fabrication)")
            continue
        if isinstance(t.get("concept"), str) and t["concept"].startswith("shape-"):
            if len(t["grounded"]) != 1:
                p5_bad.append(f"{ref}: a shape drill cited {len(t['grounded'])} facts (expected exactly 1)")
                continue
            cited = final.get(t["grounded"][0])
            if cited is None:
                p5_bad.append(f"{ref}: the cited shape fact is gone from the final store")
                continue
            _m = t["slots"].get("mode")
            if _m == "shape-corners":
                prop = "corners"
            elif _m == "shape-sides":
                prop = "sides"
            else:
                prop = t["slots"].get("property", "sides")
            v = cited.context.data.get(prop)
            want = "none" if v is None else str(v)
            if str(ir.get("answer")) != want:
                p5_bad.append(f"{ref}: answered {ir.get('answer')} != the cited claimant's stored {prop} {want}")
    checks["p5_grounding"] = {"pass": not p5_bad, "bad": p5_bad}

    # P6 — line discipline + seed continuity
    p6_bad: list[str] = []
    seed_check = _seed_check(run1_root)
    if seed_check["seed_total"] != FROZEN["seed_total_check"] or seed_check["reproduced_in_s2_pre"] != FROZEN["seed_total_check"]:
        p6_bad.append(f"seed continuity: {seed_check}")
    le = _line_end(final)
    if le != FROZEN["line_end_final"]:
        p6_bad.append(f"final line end {le} != {FROZEN['line_end_final']} (the geometry strip moved the line)")
    checks["p6_line_discipline_seed"] = {"pass": not p6_bad, "bad": p6_bad, "seed": seed_check, "line_end_final": le}

    # P7 — the JOINT band-end evaluation (ONE probe set, ONE check, both domains)
    p7_bad: list[str] = []
    table: dict[str, dict[str, Any]] = {}
    for ref, expected in FROZEN["band_end_probes"].items():
        t = turns.get(ref)
        if t is None:
            p7_bad.append(f"missing {ref}")
            continue
        if expected == "assertion":
            ok = t["kind"] == "assertion" and (t["response_ir"] or {}).get("epistemic_state") == "established"
            ans = (t["response_ir"] or {}).get("ack")
        else:
            ans = _ir_answer(t)
            ok = str(ans).startswith(expected) and (t["response_ir"] or {}).get("uncertainty_state") in ("derived", "needs_info")
        table[ref] = {"domain": t["domain"], "answer": ans, "ok": ok}
        if not ok:
            p7_bad.append(f"{ref}: expected {expected} (got {ans}, kind {t['kind']})")
    checks["p7_joint_band_end"] = {"pass": not p7_bad, "bad": p7_bad, "table": table}

    # P8 — mastery verification + determinism
    p8_bad: list[str] = []
    s4_report = json.loads((run1_root / "session-S04.json").read_text())
    mastery = s4_report["mastery"]
    for cid, expect in FROZEN["mastery_expected"].items():
        row = mastery.get(cid) or {}
        if row.get("state") != expect["state"]:
            p8_bad.append(f"{cid}: state {row.get('state')} != {expect['state']}")
        if row.get("correct_derivations", 0) < expect["correct"]:
            p8_bad.append(f"{cid}: correct {row.get('correct_derivations')} < {expect['correct']}")
        if row.get("unresolved_conflicts", 1) != 0:
            p8_bad.append(f"{cid}: unresolved conflicts {row.get('unresolved_conflicts')}")
    for cid in FROZEN["seed_numeric_stable"]:
        row = mastery.get(cid) or {}
        if row.get("state") != "stable":
            p8_bad.append(f"seed numeric {cid} regressed to {row.get('state')}")
    files_a = sorted(x.name for x in (out_dir / "e6.5-run1").iterdir() if x.is_file())
    files_b = sorted(x.name for x in (out_dir / "e6.5-run2").iterdir() if x.is_file())
    identical = files_a == files_b and all(
        hashlib.sha256((out_dir / "e6.5-run1" / f).read_bytes()).hexdigest() == hashlib.sha256((out_dir / "e6.5-run2" / f).read_bytes()).hexdigest() for f in files_a
    )
    if not identical:
        p8_bad.append(f"run1 != run2 ({files_a} vs {files_b})")
    det_arm_ok = all(t["arm"].get("classifier") == "det" for t in turns.values())
    if not det_arm_ok:
        p8_bad.append("a turn was not served by the det arm")
    total_final = len(list(final.query()))
    checks["p8_mastery_determinism"] = {
        "pass": not p8_bad,
        "bad": p8_bad,
        "mastery": {cid: (mastery.get(cid) or {}).get("state") for cid in list(FROZEN["mastery_expected"]) + FROZEN["seed_numeric_stable"]},
        "files": files_a,
        "final_store_total": total_final,
        "det_arm": det_arm_ok,
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    return {"checks": checks, "passed": passed, "value": round(passed / CHECKS, 4)}


class E6_5Experiment:
    """E6.5 — the K–5 band: numerics ∥ geometry (band 1 of the M3 sweep)."""

    name = "e6.5"
    hypothesis = (
        "Geometry learns CONCURRENTLY with math from K–5 on the same teachable-strip seam: shape "
        "definitions are store data (the rule-gated capability arc, P11 generalized to geometry), "
        "shape drills are a two-family grammar INSIDE the phrasology strip (vocabulary slots), the "
        "numeric line is untouched by the geometry strip (one line, two domains), the wrong-lesson "
        "and wrong-mapping arcs resolve through the single-current-claimant pair, and the band "
        "ENDS on a JOINT evaluation — one frozen probe set spanning both domains, all four shape "
        "concepts verified stable (K = 4) against the seed-stable numerics, two runs byte-identical."
    )
    metric = "band-1 checks passed (P1..P8)"
    threshold = "8/8"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_5()
        if "error" in report:
            return Result(name=self.name, passed=False, value=0.0, evidence=[Path("results/phase-6")], config={"seed": FROZEN["seed"], "error": report["error"]})
        return Result(
            name=self.name,
            passed=report["passed"] == CHECKS,
            value=report["value"],
            evidence=[
                Path("results/phase-6/e6.5-run1/session-S02.json"),
                Path("results/phase-6/e6.5-run1/session-S03.json"),
                Path("results/phase-6/e6.5-run1/session-S04.json"),
                Path("results/phase-6/e6.5-run1/codeX-S04.json"),
                Path("results/phase-6/e6.5-run2/codeX-S04.json"),
                Path("results/phase-6/bands-map.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "seed_assertions": FROZEN["seed_total"],
                "script_hash": SCRIPT_HASH,
            },
        )
