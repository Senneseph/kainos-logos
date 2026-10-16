# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.8 — S4 of the SAVANT-TRACK (pre-REGISTERED, frozen): the unit
distance problem band, with the theorem/lemma seam.

The seam (the architecture freeze in the pre-registration) is the
store itself: ``lemma:{slug}`` / ``conjecture:{slug}`` facts are
ESTABLISHED declared-source facts at lesson time (a stated source is
high-authority — the honest status is "given from a source"), and the
new grammar families (state / why / status / confounder-no / the
empirical derivations / the band-end wall probe) ride the existing
line-0..72 machinery. The power-growth proof itself is S6/S7 — this
band's frozen terminal probes are the MEASURED HONEST WALLS: "can
you prove that for infinitely many n the unit pairs grow to a power
above one?" => honest ``needs_info``, zero evidence (the erdosguess
NEVER a premise — P5), and the 7x7 grid wall (84 > 72, the line is
frozen — the line extension is a SEPARATE pre-registration), the
first off-line numeric wall of the track.

The paper NEVER reaches the student: P0 scans the full frozen script
and the seam statements against the frozen denylist (the standing
transcription rule of the track).
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT4,
    S4_DENYLIST,
    S4_LESSONS,
)
from kainos.tutor.e67 import CONCEPTS_E67
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E68", "FROZEN", "E6_8Experiment", "run_e6_8"]

CHECKS = 9

#: The official e6.7 S4 store (the S4 seed: 441 assertions, line 72),
#: repo-relative.
E67_SEED = Path("results/phase-6/e6.7-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E67_SEED.exists():
        return E67_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E67_SEED
    return alt if alt.exists() else E67_SEED


#: E6.8 — the concept registry the band ends carrying: everything the
#: e6.7 band ends with, plus the ten savant S4 concepts.
CONCEPTS_E68: tuple = CONCEPTS_E67 + CONCEPT_SAVANT4

#: The ten seam facts, derived from the frozen S4_LESSONS in the
#: brainstem (slug -> kind + the exact canonical statement + essence
#: + the line crosswalk). P0/P3 read these.
_LESSON_META = {
    _slug: {"kind": _k, "statement": _phrase, "essence": _es, "source_lines": _l}
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S4_LESSONS.items()
}

#: The exact seam fact statements (frozen mirrors; P3 checks store ==
#: these AND the brainstem's frozen lesson phrases).
ST_UNITPAIRS = "the number of unit pairs of a point set is the count of the pairs of its points that are exactly one apart"
ST_GRIDDIAG = "among the points of an integer grid the unit pairs are exactly the horizontal and vertical neighbor pairs, for a diagonal step is never exactly one apart"
ST_TWOSQUARES = "the products of numbers that are sums of two squares are sums of two squares in many ways"
ST_UNITCIRCLES = "two unit circles with different centers meet in two points when the squared distance between the centers is below four, in exactly one point when it is four, and in no point when it is above four"
ST_KST = "because two unit circles meet in at most two points the unit pair graph of a planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs at a constant times n to the three halves power"
ST_SST = "the spencer szemerdi trotter crossing number count pushes the unit pair bound down to a constant times n to the four thirds power"
ST_FLATAREA = "in a normed plane whose unit ball has a flat side point sets can have quadratically many unit pairs"
ST_CONVEXNORM = "for a strictly convex norm the crossing number bound still bounds unit pairs at a constant times n to the four thirds power, and valtr's construction attains that exponent"
ST_GENERICNORM = "for most norms on the plane the unit pair count grows no faster than a constant times n times log n times log log n, and in d dimensions a comeagre set of norms stays below d squared times n times log squared n with a matching lower bound up to lower order"
ST_ERDOS = "the erdosguess is that for all large n the unit pairs among any n points are at most n to the power one plus c over log log n, for an absolute constant c"

ANS_OPEN = "open — believed, not known"
ANS_PROVEN = "no — the erdosguess is believed, not known; its status is open"
CONF_ANS = {
    "flatarea": "no — the flat unit ball fact is about a different norm, not the euclidean plane; it does not touch the erdosguess",
    "convexnorm": "no — the strictly convex norm fact is about a different norm, not the euclidean plane; it does not touch the erdosguess",
    "genericnorm": "no — the generic norm fact is about a different norm, not the euclidean plane; it does not touch the erdosguess",
}
GAP_ARTICULATION = "not a capability i have been taught"

FROZEN: dict[str, Any] = {
    "seed": str(E67_SEED),
    "seed_total": 441,
    "total_turns": 61,
    "line_end_final": 72,
    #: P8 — the frozen store decomposition (final = seed + new facts
    #: + new mastery events). The exact total / new-fact / new-event
    #: constants are frozen from the offline control per the house
    #: discipline (see the Deviations note of the pre-registration).
    "final_total": 523,  # 441 seed + 26 new facts + 56 new mastery events
    "new_facts": 26,  # 10 seam facts + 10 curriculum registries + 6 prereq edges
    "new_events": 56,
    #: the ten seam facts (9 lemma + 1 conjecture), frozen statements
    "seam_facts": _LESSON_META,
    "total_seam_facts": 10,
    #: P2 — the five pre-lesson honest gaps (frozen refs -> concepts)
    "pre_teach_gaps": {
        "S02:01": "unit-distance",
        "S02:04": "gaussian-int",
        "S02:08": "circle-pair-2",
        "S02:12": "erdos-conj",
        "S02:15": "grid-lattice",
    },
    # P3 — the exact seam answers (frozen; every one must be `derived`
    # with non-empty grounded evidence citing the seam fact)
    "derived_table": {
        "S02:03": ST_UNITPAIRS,
        "S02:06": "4",  # 25 = 0²+5² = 3²+4² (ordered, x4)
        "S02:07": "3",  # 50 = 1²+7² = 5²+5² (x3)
        "S02:10": "2",  # (1,1): d² = 2 < 4
        "S02:11": "1",  # (2,0): d² = 4
        "S02:14": ANS_OPEN,
        "S02:17": "12",  # 3x3 = 2*3*2
        "S02:18": "24",  # 4x4 = 2*4*3
        "S03:01": ST_UNITPAIRS,
        "S03:03": ST_KST,
        "S03:04": "the first ceiling on unit pairs — a power above one but below n squared",
        "S03:06": ST_SST,
        "S03:07": "the sharper ceiling — the crossing number pushes the exponent from three half to four third",
        "S03:09": CONF_ANS["flatarea"],
        "S03:11": CONF_ANS["convexnorm"],
        "S03:13": CONF_ANS["genericnorm"],
        "S03:14": "4",  # 25 (reproduction)
        "S03:15": "0",  # (1,2): d² = 5 > 4
        "S03:16": "60",  # 6x6 (the on-line maximal)
        "S03:18": ANS_OPEN,
        "S04:01": ST_UNITPAIRS,
        "S04:02": ST_UNITPAIRS,
        "S04:03": ST_GRIDDIAG,
        "S04:04": ST_TWOSQUARES,
        "S04:05": ST_UNITCIRCLES,
        "S04:06": "it tells the grid exactly which neighbor pairs are unit — the count two times m times m minus one falls out of it",
        "S04:07": ST_KST,
        "S04:08": "the first ceiling on unit pairs — a power above one but below n squared",
        "S04:09": ST_SST,
        "S04:10": "the sharper ceiling — the crossing number pushes the exponent from three half to four third",
        "S04:11": ST_FLATAREA,
        "S04:12": CONF_ANS["flatarea"],
        "S04:13": "a true fact about a different norm — the ceiling changes with the shape of the unit ball",
        "S04:14": ST_CONVEXNORM,
        "S04:15": CONF_ANS["convexnorm"],
        "S04:16": "even for a rounder ball the crossing number ceiling holds, and it is exactly tight there",
        "S04:17": ST_GENERICNORM,
        "S04:18": CONF_ANS["genericnorm"],
        "S04:19": "for a generic ball the count collapses to log squared growth — the far side of the norm family",
        "S04:20": "3",  # 50 (band-end reproduction)
        "S04:21": "40",  # 5x5 (band-end empirical)
        "S04:22": ANS_OPEN,
        "S04:23": ANS_PROVEN,
    },
    # P4 — the measured walls (frozen refs)
    "power_walls": {
        "S03:17": "the mid-band power-growth probe (honest not-yet-taught)",
        "S04:24": "the JOINT band-end power-growth probe (the terminal wall)",
    },
    "offline_walls": {
        "S04:25": "7x7 grid = 84, off the line at 72 (the line-extension pre-registration trigger)",
    },
    #"P5 — the SEAM invariance: the conjecture fact is a STATUS
    # surface (its probes carry it in EVIDENCE) and is NEVER cited as
    # a derivation PREMISE (never in any `grounded`, all 61 turns)
    "conj_status_evidence": ["S02:14", "S03:18", "S04:22", "S04:23"],
    # P6 — the six confounder REFUTATION probes (stored, grounded,
    # named as different-norm facts)
    "conf_refs": ["S03:09", "S03:11", "S03:13", "S04:12", "S04:15", "S04:18"],
    # P7 — the JOINT band-end table (S4:20–23)
    "band_end_probes": {
        "S04:20": "3",
        "S04:21": "40",
        "S04:22": ANS_OPEN,
        "S04:23": ANS_PROVEN,
    },
    # P8 — mastery of the TEN S4 concepts (frozen expected values;
    # confirmed by the offline control)
    "mastery_expected": {
        "unit-distance": {"state": "stable", "correct": 4},
        "grid-lattice": {"state": "stable", "correct": 6},
        "gaussian-int": {"state": "stable", "correct": 5},
        "circle-pair-2": {"state": "stable", "correct": 4},
        "kst-bound": {"state": "stable", "correct": 4},
        "sst-bound": {"state": "stable", "correct": 4},
        "norm-flat": {"state": "stable", "correct": 4},
        "norm-convex": {"state": "stable", "correct": 4},
        "norm-generic": {"state": "stable", "correct": 4},
        "erdos-conj": {"state": "stable", "correct": 4},
    },
    # P3 — the concept-prereq edges that must be ESTABLISHED in the
    # final store + every S4 concept's prereq gap must be empty
    "prereq_edges": [
        "curriculum:prereq:kst-bound>circle-pair-2",
        "curriculum:prereq:grid-lattice>unit-distance",
        "curriculum:prereq:erdos-conj>unit-distance",
        "curriculum:prereq:norm-flat>unit-distance",
        "curriculum:prereq:norm-convex>unit-distance",
        "curriculum:prereq:norm-generic>unit-distance",
    ],
    "script": {
        2: [
            "state the unitpairs rule",
            "the number of unit pairs of a point set is the count of the pairs of its points that are exactly one apart",
            "state the unitpairs rule",
            "in how many ways is 25 a sum of two squares?",
            "the products of numbers that are sums of two squares are sums of two squares in many ways",
            "in how many ways is 25 a sum of two squares?",
            "in how many ways is 50 a sum of two squares?",
            "unit circles whose centers are 1 over and 1 across: how many meeting points?",
            "two unit circles with different centers meet in two points when the squared distance between the centers is below four, in exactly one point when it is four, and in no point when it is above four",
            "unit circles whose centers are 1 over and 1 across: how many meeting points?",
            "unit circles whose centers are 2 over and 0 across: how many meeting points?",
            "what is the status of the erdosguess?",
            "the erdosguess is that for all large n the unit pairs among any n points are at most n to the power one plus c over log log n, for an absolute constant c",
            "what is the status of the erdosguess?",
            "how many unit pairs does the 3 by 3 grid have?",
            "among the points of an integer grid the unit pairs are exactly the horizontal and vertical neighbor pairs, for a diagonal step is never exactly one apart",
            "how many unit pairs does the 3 by 3 grid have?",
            "how many unit pairs does the 4 by 4 grid have?",
        ],
        3: [
            "state the unitpairs rule",
            "because two unit circles meet in at most two points the unit pair graph of a planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs at a constant times n to the three halves power",
            "state the kstbound rule",
            "what is the kstbound for",
            "the spencer szemerdi trotter crossing number count pushes the unit pair bound down to a constant times n to the four thirds power",
            "state the sstbound rule",
            "what is the sstbound for",
            "in a normed plane whose unit ball has a flat side point sets can have quadratically many unit pairs",
            "does the flatarea rule disprove the erdosguess?",
            "for a strictly convex norm the crossing number bound still bounds unit pairs at a constant times n to the four thirds power, and valtr's construction attains that exponent",
            "does the convexnorm rule disprove the erdosguess?",
            "for most norms on the plane the unit pair count grows no faster than a constant times n times log n times log log n, and in d dimensions a comeagre set of norms stays below d squared times n times log squared n with a matching lower bound up to lower order",
            "does the genericnorm rule disprove the erdosguess?",
            "in how many ways is 25 a sum of two squares?",
            "unit circles whose centers are 1 over and 2 across: how many meeting points?",
            "how many unit pairs does the 6 by 6 grid have?",
            "can you prove that for infinitely many n the unit pairs grow to a power above one?",
            "what is the status of the erdosguess?",
        ],
        4: [
            "state the unitpairs rule",
            "state the unitpairs rule",
            "state the griddiag rule",
            "state the twosquares rule",
            "state the unitcircles rule",
            "what is the griddiag for",
            "state the kstbound rule",
            "what is the kstbound for",
            "state the sstbound rule",
            "what is the sstbound for",
            "state the flatarea rule",
            "does the flatarea rule disprove the erdosguess?",
            "what is the flatarea for",
            "state the convexnorm rule",
            "does the convexnorm rule disprove the erdosguess?",
            "what is the convexnorm for",
            "state the genericnorm rule",
            "does the genericnorm rule disprove the erdosguess?",
            "what is the genericnorm for",
            "in how many ways is 50 a sum of two squares?",
            "how many unit pairs does the 5 by 5 grid have?",
            "what is the status of the erdosguess?",
            "is the erdosguess proven?",
            "can you prove that for infinitely many n the unit pairs grow to a power above one?",
            "how many unit pairs does the 7 by 7 grid have?",
        ],
    },
    # P2 — the frozen domain sequence per session (L lesson, U
    # pre-lesson honest gap, S success, C confounder honest-no, H
    # honest wall)
    "domain_sequence": {
        2: "ULSULSSULSSULSULSS",
        # deviation D-e6p: the hand-computed frozen string had the L/S of turns 5/6 swapped; the per-turn script (authoritative) puts the lesson at 5, the probe at 6
        3: "SLSSLSSLCLCLCSSSHS",
        4: "SSSSSSSSSSSCSSCSSCSSSSSHH",
    },
}

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]


def _line_end(store) -> int:
    """The current line end = the largest successor fact v+1 in the
    store (the e6.7 machinery, unchanged by S4)."""

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
    L savant lesson, U pre-lesson capability gap, H honest
    needs_info wall, C confounder refutation, S derived. Pure
    function of the turn record."""

    if t["kind"] == "assertion" and (t["slots"] or {}).get("lemma"):
        return "L"
    if t["kind"] == "impossible":
        return "U"
    ir = t["response_ir"] or {}
    if ir.get("uncertainty_state") == "needs_info":
        return "H"
    if (t["slots"] or {}).get("mode") == "confounder-no" and ir.get("uncertainty_state") == "derived":
        return "C"
    return "S"


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E68)
    out: list[dict] = []
    for s in (2, 3, 4):
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.7 S4 store, id-for-id."""

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


def _ir_answer(t: dict) -> Any:
    return (t.get("response_ir") or {}).get("answer")


def _default_out_dir() -> Path:
    base = Path(os.environ.get("KAINOS_RESULTS_DIR", "results")) / "phase-6"
    base.mkdir(parents=True, exist_ok=True)
    return base


def run_e6_8(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.7 S4 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: dict[str, list[dict]] = {}
    for name in ("e6.8-run1", "e6.8-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.7 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed (M8)
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — with the S4
    # savant band implemented, its official evidence attached
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E68}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.8-run1", "e6.8-run2"):
        (out_dir / name / "e6.8-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return report


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.8-run1"]:
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
        "seed": str(_resolve_seed()),
        "script_hash": SCRIPT_HASH,
        "seam_facts": FROZEN["seam_facts"],
    }


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.8-run1"
    final = _fresh_store(run1_root, 4)

    # P0 — the paper NEVER reached the student (the frozen denylist
    # over EVERY script turn and the seam statements; the seam
    # statements carry their line crosswalks)
    p0_bad: list[str] = []
    for s, script in sorted(FROZEN["script"].items()):
        for surface in script:
            for term in S4_DENYLIST:
                if term in surface:
                    p0_bad.append(f"S{s:02d}: banned paper text in the script: {term!r}")
    for slug, meta in sorted(FROZEN["seam_facts"].items()):
        if not meta["source_lines"]:
            p0_bad.append(f"{slug}: the canonical statement has no line crosswalk")
        for term in S4_DENYLIST:
            if term in meta["statement"]:
                p0_bad.append(f"{slug}: banned paper text in the seam statement: {term!r}")
    checks["p0_no_paper_text"] = {"pass": not p0_bad, "bad": p0_bad}

    # P1 — script & contract (61 turns, contract-valid, det arm)
    p1_bad: list[str] = []
    if len(turns) != FROZEN["total_turns"]:
        p1_bad.append(f"{len(turns)} turns != {FROZEN['total_turns']}")
    for ref, t in turns.items():
        if not t["contract_valid"]:
            p1_bad.append(f"{ref}: contract invalid")
    if report["script_hash"] != SCRIPT_HASH:
        p1_bad.append("script identity mismatch")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — pre-lesson honesty + the interleave is FROZEN
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
        if GAP_ARTICULATION not in (t["response_text"] or ""):
            p2_bad.append(f"{ref}: the frozen gap articulation is missing")
        if t["concept"] != concept_id:
            p2_bad.append(f"{ref}: routed to {t['concept']}, not {concept_id}")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    checks["p2_honest_gaps_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — the SEAM: exactly nine lemma + one conjecture fact, all
    # established, statements byte-equal, declared-source with the
    # line crosswalk; the conjecture carries status "open"; every
    # seam answer exact + grounded; the prereq edges established
    p3_bad: list[str] = []
    for ref, expected in sorted(FROZEN["derived_table"].items()):
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing {ref}")
            continue
        ans = _ir_answer(t)
        if ans != expected:
            p3_bad.append(f"{ref}: answer {ans!r} != {expected!r}")
            continue
        ir = t["response_ir"]
        if ir.get("uncertainty_state") != "derived":
            p3_bad.append(f"{ref}: not a grounded derivation ({ir.get('uncertainty_state')})")
        if not t["grounded"] and ref not in FROZEN["conj_status_evidence"]:
            # the conj-state probes are grounded-empty by design (the
            # conjecture is a status surface, never a premise — P5
            # checks that their EVIDENCE carries the fact instead)
            p3_bad.append(f"{ref}: zero grounded evidence")
    stored_seam = {a.id for a in final.query() if a.id in {f"{m['kind']}:{s}" for s, m in _LESSON_META.items()}}
    if len(stored_seam) != FROZEN["total_seam_facts"]:
        p3_bad.append(f"{len(stored_seam)} seam facts in the final store != {FROZEN['total_seam_facts']}")
    for slug, meta in sorted(_LESSON_META.items()):
        found = False
        for a in final.query():
            if a.id != f"{meta['kind']}:{slug}":
                continue
            found = True
            if a.context.data.get("kind") != meta["kind"]:
                p3_bad.append(f"{slug}: stored kind != frozen kind")
            if isinstance(a.object, str) and a.object != meta["statement"]:
                p3_bad.append(f"{slug}: stored statement != frozen canonical statement")
            if a.context.data.get("source_role") != "declared-source":
                p3_bad.append(f"{slug}: the seam fact is not declared-source")
            if not a.context.data.get("source_lines"):
                p3_bad.append(f"{slug}: the stored fact lost its line crosswalk")
            if meta["kind"] == "conjecture" and a.context.data.get("conjecture_status") != "open":
                p3_bad.append(f"{slug}: the conjecture must carry conjecture_status='open'")
            break
        if not found:
            p3_bad.append(f"{slug}: the seam fact is not in the final store")
    for edge_id in FROZEN["prereq_edges"]:
        try:
            edge = final.get(edge_id)
        except KeyError:
            p3_bad.append(f"{edge_id}: not in the final store")
            continue
        if edge.validity is not None and edge.validity.to is not None:
            p3_bad.append(f"{edge_id}: inactive in the final store")
    checks["p3_seam_facts"] = {"pass": not p3_bad, "bad": p3_bad, "seam_facts": len(FROZEN["seam_facts"])}

    # P4 — the measured walls: the two power-growth probes (honest
    # NOT-YET-TAUGHT — the leap is S6's) and the 7x7 off-line wall
    # (84 > 72; the line extension is a separate pre-registration)
    p4_bad: list[str] = []
    for ref, note in sorted(FROZEN["power_walls"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref} ({note})")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the power probe is not an honest needs_info gap")
        if GAP_ARTICULATION not in str(ir.get("answer", "")):
            p4_bad.append(f"{ref}: the not-yet-taught articulation is missing")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a gap cited evidence")
    for ref, note in sorted(FROZEN["offline_walls"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref} ({note})")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the 7x7 wall ({note}) is not an honest needs_info gap")
        if "84" not in str(ir.get("answer", "")) or "72" not in str(ir.get("answer", "")):
            p4_bad.append(f"{ref}: the 7x7 wall must articulate the count (84) and the line end (72)")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited evidence")
    # the on-line maximal (6x6 = 60) still derives at the band end
    t66 = turns.get("S03:16")
    if t66 is not None and _ir_answer(t66) != "60":
        p4_bad.append("S03:16: the 6x6 maximal (60) is wrong")
    checks["p4_walls"] = {"pass": not p4_bad, "bad": p4_bad, "power_refs": list(FROZEN["power_walls"])}

    # P5 — the SEAM invariance: the erdosguess fact id appears in
    # ZERO `grounded` lists across all 61 turns (never a premise);
    # the status probes carry it in EVIDENCE only
    p5_bad: list[str] = []
    CONJ = "conjecture:erdosguess"
    for ref, t in sorted(turns.items()):
        if t["kind"] == "assertion":
            continue  # the lesson turn cites the fact it establishes (the write)
        if any(CONJ in str(x) for x in t["grounded"]):
            p5_bad.append(f"{ref}: the conjecture was cited as a derivation premise")
    for ref in FROZEN["conj_status_evidence"]:
        if t := turns.get(ref):
            ev = (t["response_ir"] or {}).get("evidence") or []
            if not any(CONJ in str(x) for x in ev):
                p5_bad.append(f"{ref}: the status probe lost its conjecture evidence")
            if "open" not in str(_ir_answer(t)):
                p5_bad.append(f"{ref}: the status probe must surface 'open'")
    checks["p5_conjecture_never_premise"] = {"pass": not p5_bad, "bad": p5_bad}

    # P6 — the confounders are TRUE but irrelevant: stored
    # declared-source, and every refutation probe grounds + names
    # the distinction (a different norm, not the euclidean plane)
    p6_bad: list[str] = []
    for ref in FROZEN["conf_refs"]:
        if t := turns.get(ref):
            ir = t["response_ir"] or {}
            if ir.get("uncertainty_state") != "derived":
                p6_bad.append(f"{ref}: the confounder refutation is not grounded")
            if "different norm" not in str(ir.get("answer", "")):
                p6_bad.append(f"{ref}: the refutation must name the different norm")
            if not t["grounded"]:
                p6_bad.append(f"{ref}: the refutation cited nothing")
    for slug in ("flatarea", "convexnorm", "genericnorm"):
        a = None
        for x in final.query():
            if x.id == f"lemma:{slug}":
                a = x
                break
        if a is None:
            p6_bad.append(f"{slug}: the confounder lemma is not stored")
        elif a.context.data.get("source_role") != "declared-source":
            p6_bad.append(f"{slug}: the confounder lemma is not declared-source")
    checks["p6_confounders"] = {"pass": not p6_bad, "bad": p6_bad, "conf_refs": FROZEN["conf_refs"]}

    # P7 — the JOINT band-end table (S4:20–23: one frozen probe set
    # spanning the band — reproduction across the whole store)
    p7_bad: list[str] = []
    for ref, expected in sorted(FROZEN["band_end_probes"].items()):
        t = turns.get(ref)
        if t is None:
            p7_bad.append(f"missing {ref}")
            continue
        got = _ir_answer(t)
        if got != expected:
            p7_bad.append(f"{ref}: band-end answer {got!r} != {expected!r}")
    t25 = turns.get("S04:25")
    if t25 is None or (t25["response_ir"] or {}).get("uncertainty_state") != "needs_info":
        p7_bad.append("S04:25: the terminal 7x7 wall is not an honest gap")
    checks["p7_joint_band_end"] = {"pass": not p7_bad, "bad": p7_bad}

    # P8 — mastery, store integrity, determinism
    p8_bad: list[str] = []
    seed = _seed_check(run1_root)
    if seed["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed['seed_total']} != {FROZEN['seed_total']}")
    if seed["reproduced_in_s2_pre"] != FROZEN["seed_total"] or seed["missing"]:
        p8_bad.append(f"seed continuity: {seed}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(
            f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S4 must write zero successor facts)"
        )
    all_final = list(final.query())
    if FROZEN["final_total"] is not None and len(all_final) != FROZEN["final_total"]:
        p8_bad.append(f"final store total {len(all_final)} != frozen {FROZEN['final_total']}")
    seedstore = load_store(_resolve_seed())
    seed_ids = {a.id for a in seedstore.query()}
    new = [a for a in all_final if a.id not in seed_ids]
    new_events = [a for a in new if (a.context.data or {}).get("kind") == "mastery-event"]
    new_facts = [a for a in new if (a.context.data or {}).get("kind") != "mastery-event"]
    if FROZEN["new_facts"] is not None and len(new_facts) != FROZEN["new_facts"]:
        p8_bad.append(f"new facts {len(new_facts)} != frozen {FROZEN['new_facts']}: {sorted(a.id for a in new_facts)}")
    if FROZEN["new_events"] is not None and len(new_events) != FROZEN["new_events"]:
        p8_bad.append(f"new mastery events {len(new_events)} != frozen {FROZEN['new_events']}")
    mv = mastery_view(final, [c.id for c in CONCEPTS_E68])
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
    for c in CONCEPTS_E67:
        v = mv.get(c.id)
        if v is None or v.state != "stable":
            p8_bad.append(f"{c.id}: pre-S4 concept regressed ({v.state if v else 'absent'})")
    # determinism
    r1 = runs["e6.8-run1"]
    r2 = runs["e6.8-run2"]
    a = json.dumps(r1, sort_keys=True)
    b = json.dumps(r2, sort_keys=True)
    if a != b:
        p8_bad.append("run1 != run2")
    det_arm = all((t.get("arm") or {}).get("classifier") == "det" for srow in r1 for t in srow.get("turns", []))
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
        f"PASS e6.8: {passed}/{len(checks)}"
        if passed == len(checks)
        else f"FAIL e6.8: {passed}/{len(checks)}"
    )
    return {"checks": checks, "passed": passed, "value": value}


class E6_8Experiment:
    """E6.8 — S4 of the SAVANT-TRACK: the unit-distance problem band
    (the seam: the theorem/lemma layer of the store)."""

    name = "e6.8"
    hypothesis = (
        "The unit-distance problem band (S4) learns on the NEW theorem/lemma seam: the "
        "nine lemma facts and the erdosguess CONJECTURE are ESTABLISHED declared-source "
        "facts in the same codex store (no schema change); the student can STATE each one "
        "exactly, report the conjecture's status (open — never citable as a derivation "
        "premise, P5), and derive the empirical bed on the frozen 0..72 line (grid "
        "3x3=12 / 4x4=24 / 5x5=40 / 6x6=60; two-square counts 25->4, 50->3; unit-circle "
        "meetings (1,1)->2, (2,0)->1, (1,2)->0 by the d2 rule); the confounders (flat / "
        "convex / generic norms) are stored and REFUTED as different-norm facts, never a "
        "refutation of the euclidean conjecture; the JOINT band-end ends on the measured "
        "walls — the power-growth probe (the proof is S6/S7) and the 7x7 grid wall (84 > "
        "72, the line is frozen — the line extension is a separate pre-registration) — "
        "both honest needs_info with zero evidence; the paper never reaches the student "
        "(the frozen denylist scan over the whole script, P0); two runs byte-identical."
    )
    metric = "S4 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_8()
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
                Path("results/phase-6/e6.8-run1/session-S02.json"),
                Path("results/phase-6/e6.8-run1/session-S03.json"),
                Path("results/phase-6/e6.8-run1/session-S04.json"),
                Path("results/phase-6/e6.8-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
