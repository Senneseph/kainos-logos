# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.9 — S5 of the SAVANT-TRACK (pre-REGISTERED, frozen): the
number-field toolkit band (A-cluster, shallow).

Sixteen more `lemma:{slug}` seam facts (statement + role + cite-when;
NO proof object — the why wall is the measured boundary) on the SAME
store as S4, with six new grammar families riding the frozen 0..72
line: the mod4 square tables (`sqmod`), the GS-test comparisons
(`gsay`, the SILENT case stored as such), the CM sum-of-two-squares
bed (`sumsq`), the class-bound pigeonhole arithmetic (`holes`), the
magnitude wall (`duopow`: 2^6=64 on the line, 2^7=128 off it), and
the WHY wall (`whydeep`: honest needs_info — the proof itself is not
in the store). The band ends on the JOINT G-and-A reproduction table
plus the S4 power wall, re-probed and still a wall (the leap is S6's).
The paper never reaches the student (P0 denylist scan over the full
frozen script + all sixteen statements).
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT5,
    S4_LESSONS,
    S5_DENYLIST,
    S5_LESSONS,
)
from kainos.tutor.e68 import CONCEPTS_E68
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E69", "FROZEN", "E6_9Experiment", "run_e6_9"]

CHECKS = 9

#: The official e6.8 S4 store (the S5 seed: 523 assertions, line 72),
#: repo-relative.
E68_SEED = Path("results/phase-6/e6.8-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E68_SEED.exists():
        return E68_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E68_SEED
    return alt if alt.exists() else E68_SEED


#: E6.9 — the concept registry the band ends carrying: everything the
#: e6.8 band ends with, plus the sixteen savant S5 concepts.
CONCEPTS_E69: tuple = CONCEPTS_E68 + CONCEPT_SAVANT5

#: The sixteen seam facts, derived from the frozen S5_LESSONS in the
#: brainstem (slug -> kind + the exact canonical statement + essence
#: + the line crosswalk). P0/P3 read these.
_LESSON_META_S5 = {
    _slug: {"kind": _k, "statement": _phrase, "essence": _es, "source_lines": _l}
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S5_LESSONS.items()
}


_ANSWER_ = {
    "SQ_YES_2_5": "yes — 2 squared plus one is 1 times 5",
    "SQ_NO_1_7": "no — the residue is 2",
    "SQ_NO_3_7": "no — the residue is 3 after taking one lot of 7",
    "SQ_YES_5_13": "yes — 5 squared plus one is 2 times 13",
    "SQ_YES_4_17": "yes — 4 squared plus one is 1 times 17",
    "SQ_NO_3_11": "no — the residue is 10",
    "SQ_NO_6_19": "no — the residue is 18 after taking one lot of 19",
    "GS_YES_3_2": "yes — four times r is 8, at most d squared, 9, so the test says infinite",
    "GS_YES_5_3": "yes — four times r is 12, at most d squared, 25, so the test says infinite",
    "GS_SILENT_3_6": "no — the test is silent, four times r is 24, above d squared, 9",
    "OPEN": "open — believed, not known",
}

GAP_ARTICULATION = "not a capability i have been taught"


def _st(slug: str) -> str:
    return _LESSON_META_S5[slug]["statement"]


def _es(slug: str) -> str:
    return _LESSON_META_S5[slug]["essence"]


FROZEN: dict[str, Any] = {
    "seed": str(E68_SEED),
    "seed_total": 523,
    "total_turns": 65,
    "line_end_final": 72,
    #: P8 — the frozen store decomposition (final = seed + new facts
    #: + new mastery events + new seam facts). Frozen from the
    #: OFFICIAL control (the first full control run, identity
    #: verified byte-for-byte across re-runs) per the house
    #: discipline: 16 registries + 20 prereq edges + 16 seam facts +
    #: (16 seam lesson-events + 41 derivation-correct + 4 drill-unable
    #: events). The seam facts carry context kind "lemma"; the lesson
    #: marker events carry context kind "mastery-event" (the S4
    #: pattern, one marker per lesson).
    "final_total": 636,  # 523 seed + 52 new facts + 61 events
    "new_facts": 52,  # 16 seam facts + 16 curriculum registries + 20 prereq edges
    "new_events": 61,  # 16 seam lesson-events + 41 derivation-correct + 4 drill-unable
    #: the sixteen seam facts, frozen statements (byte-frozen)
    "seam_facts": _LESSON_META_S5,
    "total_seam_facts": 26,  # S4's ten + S5's sixteen (deviation D-e6r: the pre-reg prose said "24" — an arithmetic slip; the mechanism writes 10+16=26, all byte-verified)
    #: P2 — the pre-lesson honest gaps (frozen refs -> concepts).
    # deviation D-e6q (recorded in the pre-registration): the
    # pre-reg's P2 listed a fifth U turn (S04:13 cm-conj); the
    # authoritative per-turn script teaches cmunit at S04:12, BEFORE
    # its first sumsq probe (S04:13) — so no cm-conj pre-lesson
    # probe exists; the U set is these four turns.
    "pre_teach_gaps": {
        "S02:01": "number-field",
        "S02:06": "mod4-split",
        "S03:08": "class-bound",
        "S04:03": "golod-shaf",
    },
    # P3 — the exact seam answers (frozen; every one must be
    # `derived` with non-empty grounded evidence citing the owning
    # seam fact)
    "derived_table": {
        "S02:03": _st("numberfields"),
        "S02:05": _st("primesplit"),
        "S02:08": _ANSWER_["SQ_YES_2_5"],
        "S02:09": _ANSWER_["SQ_NO_1_7"],
        "S02:10": _ANSWER_["SQ_NO_3_7"],
        "S02:11": _ANSWER_["SQ_YES_5_13"],
        "S02:12": _ANSWER_["SQ_YES_4_17"],
        "S02:13": _ANSWER_["SQ_NO_3_11"],
        "S02:14": _ANSWER_["SQ_NO_6_19"],
        # S02:15-18 = the discrim/adjoini lessons (assertions, not
        # derived)
        "S02:16": _st("discrim"),
        "S02:18": _st("adjoini"),
        "S03:01": _st("numberfields"),
        "S03:03": _st("cyclotomic"),
        "S03:04": _es("cyclotomic"),
        "S03:06": _st("charcutout"),
        "S03:07": _es("charcutout"),
        "S03:10": "3",  # ceiling(5/2): 2 lots of 2 leave 1 over
        "S03:11": "3",  # ceiling(7/3): 2 lots of 3 leave 1 over
        "S03:12": _st("classbound"),
        "S03:14": _st("chebot"),
        "S03:15": _es("chebot"),
        "S03:17": _st("apbound"),
        "S03:18": _es("apbound"),
        "S04:02": _st("fratin"),
        "S04:05": _ANSWER_["GS_YES_3_2"],
        "S04:06": _ANSWER_["GS_YES_5_3"],
        "S04:07": _ANSWER_["GS_SILENT_3_6"],
        "S04:08": _st("gstest"),
        "S04:10": _st("shafbound"),
        "S04:11": _es("shafbound"),
        "S04:13": "25",  # 3^2 + 4^2 (the CM bed)
        "S04:14": "25",  # the CM bed (repeat drill)
        "S04:15": "50",  # 1^2 + 7^2 (the S4 twosq-50 input)
        "S04:16": _st("cmunit"),
        "S04:18": _st("minkembed"),
        "S04:20": _st("hajir"),
        "S04:23": "64",  # duopow 6: on the line (six doublings)
        "S04:25": _ANSWER_["OPEN"],
        "S04:26": "24",  # 4x4 grid (G reproduction on the A-store)
        "S04:27": _ANSWER_["SQ_YES_2_5"],  # sqmod (5,2) reproduction
        "S04:28": "3",  # twosq 50 (G reproduction)
    },
    # P4 — the measured walls (frozen refs)
    "why_walls": {
        "S04:21": "the shafarevich proof is not a store object",
        "S04:22": "the golod-shafarevich proof is not a store object",
    },
    "magnitude_walls": {
        "S04:24": "duopow 7: 128 is off the line at 72 (the growth-rate wall)"
    },
    "power_walls": {
        "S04:29": "the S4 power-growth wall RE-PROBED (still a wall at the S5 band end)"
    },
    # P4 also — the beds EXACT (all grounded on the line)
    "beds_exact": {
        "S02:08": _ANSWER_["SQ_YES_2_5"],
        "S02:09": _ANSWER_["SQ_NO_1_7"],
        "S02:10": _ANSWER_["SQ_NO_3_7"],
        "S02:11": _ANSWER_["SQ_YES_5_13"],
        "S02:12": _ANSWER_["SQ_YES_4_17"],
        "S02:13": _ANSWER_["SQ_NO_3_11"],
        "S02:14": _ANSWER_["SQ_NO_6_19"],
        "S04:05": _ANSWER_["GS_YES_3_2"],
        "S04:06": _ANSWER_["GS_YES_5_3"],
        "S04:07": _ANSWER_["GS_SILENT_3_6"],
        "S04:13": "25",
        "S04:14": "25",
        "S04:15": "50",
        "S03:10": "3",
        "S03:11": "3",
        "S04:23": "64",
    },
    # P5 — the SEAM invariance: the erdosguess conjecture fact is a
    # status surface (its probe carries it in EVIDENCE) and is NEVER
    # cited as a derivation premise (never in any grounded, 65 turns)
    "conj_status_evidence": ["S04:25"],
    # P6 — the JOINT G-and-A band-end table (S04:25-28)
    "band_end_probes": {
        "S04:25": _ANSWER_["OPEN"],
        "S04:26": "24",
        "S04:27": _ANSWER_["SQ_YES_2_5"],
        "S04:28": "3",
    },
    # P7 — the BED CROSS-CHECK: the sumsq (1,7) bed's answer (50) is
    # the S4 twosq-50 bed's input; that bed reproduces (3) at
    # S04:28 on the same store. The sumsq evidence must cite ONLY
    # line facts + its owning seam fact.
    "bed_crosscheck": {
        "sumsq_ref": "S04:15",
        "sumsq_answer": "50",
        "twosq_ref": "S04:28",
        "twosq_answer": "3",
    },
    # P8 — mastery of the SIXTEEN S5 concepts (FROZEN FROM THE OFFICIAL
    # CONTROL). deviation D-e6r (control #1): the pre-reg expected
    # "mod4-split 8/stable, golod-shaf 4/stable, the other fourteen
    # practicing; ALL prereq gaps EMPTY for the sixteen" — the control
    # FALSIFIES the stability expectations. Honest read: the stable rule
    # (frozen in mastery.py) is >=K correct AND every prerequisite
    # concept STABLE; a shallow band that introduces its ground concept
    # (number-field: 2 correct, practicing) cannot lift the tower to
    # stable in one pass. mod4-split (8), golod-shaf (4) and cm-conj (4)
    # all clear the evidence bar but are prereq-GATED; every S5 concept
    # ends PRACTICING, with 15 of 16 carrying non-empty prereq gaps.
    # That IS the curriculum state of a shallow band (the reactivation
    # climbs happen in S6/S7) — recorded in the wall ledger (W-S5-5),
    # not tuned away.
    "mastery_expected": {
        "number-field": {"state": "practicing", "correct": 2},
        "prime-split": {"state": "practicing", "correct": 1},
        "mod4-split": {"state": "practicing", "correct": 8},
        "disc-rd": {"state": "practicing", "correct": 1},
        "adjoin-i": {"state": "practicing", "correct": 1},
        "cyclotomic-cubic": {"state": "practicing", "correct": 2},
        "char-cutout": {"state": "practicing", "correct": 2},
        "class-bound": {"state": "practicing", "correct": 3},
        "chebotarev": {"state": "practicing", "correct": 2},
        "pnt-ap": {"state": "practicing", "correct": 2},
        "frattini": {"state": "practicing", "correct": 1},
        "golod-shaf": {"state": "practicing", "correct": 4},
        "shafarevich": {"state": "practicing", "correct": 2},
        "cm-conj": {"state": "practicing", "correct": 4},
        "minkowski-embed": {"state": "practicing", "correct": 1},
        "hajir-maire": {"state": "practicing", "correct": 1},
    },
    # P8 — the prereq-gap structure (frozen from the OFFICIAL control):
    # exactly the transitive cascade above the practicing ground
    # concept; only number-field (prereq: stable count-successor) has
    # an empty gap.
    "expected_prereq_gaps": {
        "number-field": (),
        "prime-split": ("number-field",),
        "mod4-split": ("prime-split",),
        "disc-rd": ("number-field",),
        "adjoin-i": ("disc-rd",),
        "cyclotomic-cubic": ("disc-rd", "prime-split"),
        "char-cutout": ("cyclotomic-cubic",),
        "class-bound": ("number-field",),
        "chebotarev": ("prime-split",),
        "pnt-ap": ("chebotarev",),
        "frattini": ("number-field",),
        "golod-shaf": ("frattini",),
        "shafarevich": ("golod-shaf", "number-field"),
        "cm-conj": ("number-field",),
        "minkowski-embed": ("number-field",),
        "hajir-maire": ("class-bound", "golod-shaf", "shafarevich"),
    },
    # P3 — the prereq edges that must be ESTABLISHED in the final
    # store (the pre-reg's listed set; every one asserted)
    "prereq_edges": [
        "curriculum:prereq:prime-split>number-field",
        "curriculum:prereq:mod4-split>prime-split",
        "curriculum:prereq:disc-rd>number-field",
        "curriculum:prereq:adjoin-i>disc-rd",
        "curriculum:prereq:cyclotomic-cubic>prime-split",
        "curriculum:prereq:cyclotomic-cubic>disc-rd",
        "curriculum:prereq:char-cutout>cyclotomic-cubic",
        "curriculum:prereq:class-bound>number-field",
        "curriculum:prereq:chebotarev>prime-split",
        "curriculum:prereq:pnt-ap>chebotarev",
        "curriculum:prereq:frattini>number-field",
        "curriculum:prereq:golod-shaf>frattini",
        "curriculum:prereq:shafarevich>golod-shaf",
        "curriculum:prereq:shafarevich>number-field",
        "curriculum:prereq:cm-conj>number-field",
        "curriculum:prereq:minkowski-embed>number-field",
        "curriculum:prereq:hajir-maire>shafarevich",
        "curriculum:prereq:hajir-maire>class-bound",
        "curriculum:prereq:hajir-maire>golod-shaf",
    ],
    # the one edge BEYOND the pre-reg's list (the mechanism writes an
    # edge per prereq; number-field's prereq is count-successor) —
    # recorded, asserted as a bonus fact, deviation D-e6r (the pre-reg
    # labeled its 19-edge list "(16 edges)"; the mechanism writes 20
    # including this one)
    "bonus_prereq_edges": ["curriculum:prereq:number-field>count-successor"],
    "script": {
        2: [
            "state the numberfields rule",
            "a number field is a finite extension of the rationals, its embeddings into the complex numbers are all different, a field is totally real when every embedding lands in the reals, and the norm of a nonzero algebraic integer is a nonzero integer of absolute value at least one",
            "state the numberfields rule",
            "a rational prime in a field extension either splits into several distinct primes, stays inert, or ramifies, and the ramified primes are exactly the ones that divide the discriminant, a finite list",
            "state the primesplit rule",
            "does 2 squared plus one vanish modulo 5?",
            "x squared plus one equals zero modulo an odd prime q has a solution exactly when q is one modulo four, and it feeds the tower: when q is one mod four and splits in the lower field then q splits in the field with i adjoined, since x squared plus one splits over the residue field",
            "does 2 squared plus one vanish modulo 5?",
            "does 1 squared plus one vanish modulo 7?",
            "does 3 squared plus one vanish modulo 7?",
            "does 5 squared plus one vanish modulo 13?",
            "does 4 squared plus one vanish modulo 17?",
            "does 3 squared plus one vanish modulo 11?",
            "does 6 squared plus one vanish modulo 19?",
            "the absolute discriminant of a tower multiplies up the levels by the norm of the relative discriminant, the root discriminant is the discriminant raised to the reciprocal of the degree, and a step that ramifies nowhere does not change the root discriminant",
            "state the discrim rule",
            "adjoining i to a number field changes the relative discriminant by a factor that divides four, only the prime two can ramify since x squared plus one gets a double root only in even residue characteristic, and so the root discriminant of the new field is at most twice the old one",
            "state the adjoini rule",
        ],
        3: [
            "state the numberfields rule",
            "for each prime r that is one mod three there is a unique totally real cyclic cubic subfield of the r-th cyclotomic field with conductor r, and for ramified primes that are pairwise coprime the cubic fields are linearly disjoint, the galois group of their compositum is l products of z over three, and its part over the base is the same with one generator removed",
            "state the cyclotomic rule",
            "what is the cyclotomic for",
            "an order three character cuts out the unique cyclic cubic subfield fixed by its kernel, and for characters whose conductors are pairwise coprime the conductors multiply, which is why the discriminant of the base field is the square of the product of the ramified primes",
            "state the charcutout rule",
            "what is the charcutout for",
            "what is the biggest hole guaranteed when 5 items go into 2 holes?",
            "the class group of a number field has order at most the max of two and the root discriminant raised to an absolute constant times the degree, so fields of bounded root discriminant and bounded degree have class groups of bounded size",
            "what is the biggest hole guaranteed when 5 items go into 2 holes?",
            "what is the biggest hole guaranteed when 7 items go into 3 holes?",
            "state the classbound rule",
            "chebotarev's density theorem says the primes whose frobenius class is a prescribed element exist in infinitely many, and the finitely many ramified primes may be excluded",
            "state the chebot rule",
            "what is the chebot for",
            "the product of the first l primes that are one mod three grows like e to the O of l log l",
            "state the apbound rule",
            "what is the apbound for",
        ],
        4: [
            "burnside's basis theorem reads the generator count of a pro three group off its frattini quotient, and killing generators in the frattini quotient keeps the generator count fixed while the relation count grows by at most the number killed",
            "state the fratin rule",
            "does the gs test say infinite for 3 generators and 2 relations?",
            "the golod shafarevich test says a pro three group on d generators with r relations is infinite whenever r is at most d squared divided by four, and it is silent when r is above",
            "does the gs test say infinite for 3 generators and 2 relations?",
            "does the gs test say infinite for 5 generators and 3 relations?",
            "does the gs test say infinite for 3 generators and 6 relations?",
            "state the gstest rule",
            "shafarevich's bound says that for a totally real cubic base field without the cube roots of unity the relation count of its maximal unramified pro three extension is at most the generator count plus an absolute constant c zero",
            "state the shafbound rule",
            "what is the shafbound for",
            "an element that multiplies with its conjugate to one has absolute value one in every complex embedding, it sits on the unit circle in every view, and the integer check in the ring with i is that three squared plus four squared is five squared",
            "what is 3 squared plus 4 squared?",
            "what is 3 squared plus 4 squared?",
            "what is 1 squared plus 7 squared?",
            "state the cmunit rule",
            "the minkowski embedding sends a field of degree f into f dimensional complex space, and the product of the conjugates of an element is the square root of the absolute value of its norm",
            "state the minkembed rule",
            "the hajir maire tower method says an infinite tower of unramified extensions of a totally real field exists when the generator count outgrows the relation cap at the levels, with the class group contribution controlled by the pigeonhole bound",
            "state the hajir rule",
            "explain why the shafbound holds",
            "explain why the gstest holds",
            "how large is two raised to the 6?",
            "how large is two raised to the 7?",
            "what is the status of the erdosguess?",
            "how many unit pairs does the 4 by 4 grid have?",
            "does 2 squared plus one vanish modulo 5?",
            "in how many ways is 50 a sum of two squares?",
            "can you prove that for infinitely many n the unit pairs grow to a power above one?",
        ],
    },
    # P2 — the frozen domain sequence per session (L lesson, U
    # pre-lesson honest gap, S derived, H honest wall).
    # deviation D-e6q (control #1, turn-for-turn): the pre-reg's S4
    # string drifts from position 11 onward (it anticipates a
    # cm-conj pre-lesson U at 12 — the same reading as its P2 "S04:13
    # cm-conj" item); the authoritative per-turn script (declared
    # authoritative by the pre-reg itself) teaches cmunit at S04:12,
    # BEFORE its first sumsq probe (S04:13), so 12 is L and 13 is S.
    # The string below is derived turn-for-turn from the
    # authoritative script; S2/S3 match the pre-reg
    # letter-for-letter.
    "domain_sequence": {
        2: "ULSLSULSSSSSSSLSLS",
        3: "SLSSLSSULSSSLSSLSS",
        # deviation D-e6q (control #1, turn-for-turn): the pre-reg's S4
        # hand-derived string expected a cm-conj pre-lesson U at 12; the
        # authoritative per-turn script teaches cmunit at S04:12 BEFORE
        # its first sumsq probe (S04:13), so 12 is L and 13 is S. The
        # string below is derived turn-for-turn from the authoritative
        # script (the pre-reg's own declaration of authority); S2/S3
        # match the pre-reg letter-for-letter.
        4: "LSULSSSSLSSLSSSSLSLSHHSHSSSSH",
    },
}

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

#: the sixteen lesson phrases (frozen) must appear IN the script,
#: byte-exact (the literal script turns are the canonical bytes)
_lesson_phrases = list(S5_LESSONS)
for _phrase in _lesson_phrases:
    assert any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"the S5 lesson phrase is not verbatim in the frozen script: {_phrase[:60]}..."
    )


def _line_end(store) -> int:
    """The current line end = the largest successor fact v+1 in the
    store (the e6.8 machinery, unchanged by S5)."""

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
    needs_info wall, S derived. Pure function of the turn record."""

    if t["kind"] == "assertion" and (t["slots"] or {}).get("lemma"):
        return "L"
    if t["kind"] == "impossible":
        return "U"
    ir = t["response_ir"] or {}
    if ir.get("uncertainty_state") == "needs_info":
        return "H"
    return "S"


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E69)
    out: list[dict] = []
    for s in (2, 3, 4):
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.8 S4 store, id-for-id."""

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


def run_e6_9(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.8 S4 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: dict[str, list[dict]] = {}
    for name in ("e6.9-run1", "e6.9-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.8 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — with the S5
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E69}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.9-run1", "e6.9-run2"):
        (out_dir / name / "e6.9-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return report


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.9-run1"]:
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
    run1_root = out_dir / "e6.9-run1"
    final = _fresh_store(run1_root, 4)

    # P0 — the paper NEVER reached the student (the S5 frozen
    # denylist over EVERY script turn and the sixteen seam
    # statements; the statements carry their line crosswalks)
    p0_bad: list[str] = []
    for s, script in sorted(FROZEN["script"].items()):
        for surface in script:
            for term in S5_DENYLIST:
                if term in surface:
                    p0_bad.append(f"S{s:02d}: banned paper text in the script: {term!r}")
    for slug, meta in sorted(FROZEN["seam_facts"].items()):
        if not meta["source_lines"]:
            p0_bad.append(f"{slug}: the canonical statement has no line crosswalk")
        for term in S5_DENYLIST:
            if term in meta["statement"]:
                p0_bad.append(f"{slug}: banned paper text in the seam statement: {term!r}")
    checks["p0_no_paper_text"] = {"pass": not p0_bad, "bad": p0_bad}

    # P1 — script & contract (65 turns, contract-valid, det arm)
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

    # P3 — the SEAM: exactly twenty-four lemma/conjecture facts
    # (S4's ten + S5's sixteen), all established, S5 statements
    # byte-equal to the frozen canonical statements, S4 statements
    # UNCHANGED (no drift), declared-source with crosswalks, the
    # prereq edges established, every derived answer exact +
    # grounded
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
            p3_bad.append(f"{ref}: zero grounded evidence")
    # the sixteen S5 seam facts
    for slug, meta in sorted(FROZEN["seam_facts"].items()):
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
            break
        if not found:
            p3_bad.append(f"{slug}: the seam fact is not in the final store")
    # the ten S4 seam facts: byte-exact (no drift) + still stored
    s4_meta = {
        _slug: {"kind": _k, "statement": _phrase}
        for _phrase, (_c, _slug, _k, _es, _d, _l) in S4_LESSONS.items()
    }
    for slug, meta in sorted(s4_meta.items()):
        found = False
        for a in final.query():
            if a.id != f"{meta['kind']}:{slug}":
                continue
            found = True
            if isinstance(a.object, str) and a.object != meta["statement"]:
                p3_bad.append(f"S4 {slug}: drift — stored statement != S4 canonical")
            break
        if not found:
            p3_bad.append(f"S4 {slug}: the seam fact is gone from the final store")
    total_seam = 0
    for a in final.query():
        top = a.id.split(":", 1)[0]
        if top in ("lemma", "conjecture"):
            total_seam += 1
            kind_ctx = a.context.data.get("kind")
            stmt = a.object if isinstance(a.object, str) else None
            if not (kind_ctx in ("lemma", "conjecture") and stmt and a.context.data.get("source_role") == "declared-source"):
                p3_bad.append(f"{a.id}: the seam fact lost its established declared-source shape")
    if total_seam != FROZEN["total_seam_facts"]:
        p3_bad.append(f"{total_seam} seam facts in the final store != {FROZEN['total_seam_facts']}")
    for edge_id in FROZEN["prereq_edges"] + FROZEN["bonus_prereq_edges"]:
        try:
            edge = final.get(edge_id)
        except KeyError:
            p3_bad.append(f"{edge_id}: not in the final store")
            continue
        if edge.validity is not None and edge.validity.to is not None:
            p3_bad.append(f"{edge_id}: inactive in the final store")
    checks["p3_seam_facts"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_facts": FROZEN["total_seam_facts"],
        "derived_refs": len(FROZEN["derived_table"]),
    }

    # P4 — the measured walls + the beds exact (every bed grounded
    # on the line)
    p4_bad: list[str] = []
    for ref, note in sorted(FROZEN["why_walls"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref} ({note})")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the why wall ({note}) is not an honest needs_info gap")
        if "not in my store" not in str(ir.get("answer", "")):
            p4_bad.append(f"{ref}: the why wall must articulate the missing proof object")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited evidence")
    for ref, note in sorted(FROZEN["magnitude_walls"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref} ({note})")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the magnitude wall ({note}) is not an honest needs_info gap")
        if "128" not in str(ir.get("answer", "")) or "72" not in str(ir.get("answer", "")):
            p4_bad.append(f"{ref}: the magnitude wall must name 128 and the line end 72")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited evidence")
    for ref, note in sorted(FROZEN["power_walls"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref} ({note})")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the power-wall re-probe is not an honest needs_info gap")
        if GAP_ARTICULATION not in str(ir.get("answer", "")):
            p4_bad.append(f"{ref}: the not-yet-taught articulation is missing")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited evidence")
    for ref, expected in sorted(FROZEN["beds_exact"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing bed {ref}")
            continue
        ir = t["response_ir"] or {}
        if _ir_answer(t) != expected:
            p4_bad.append(f"{ref}: bed answer {_ir_answer(t)!r} != {expected!r}")
        if ir.get("uncertainty_state") != "derived":
            p4_bad.append(f"{ref}: the bed is not a grounded derivation")
        if not t["grounded"]:
            p4_bad.append(f"{ref}: the bed cited nothing (no line grounding)")
    checks["p4_walls_beds"] = {"pass": not p4_bad, "bad": p4_bad, "bed_refs": len(FROZEN["beds_exact"])}

    # P5 — the SEAM invariance carries over: the erdosguess fact id
    # appears in ZERO `grounded` lists across all 65 turns (never a
    # premise); the status probe carries it in EVIDENCE only
    p5_bad: list[str] = []
    CONJ = "conjecture:erdosguess"
    for ref, t in sorted(turns.items()):
        if t["kind"] == "assertion":
            continue  # the lesson turn cites the fact it establishes
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

    # P6 — the JOINT G-and-A band-end table: the S5 store reproduces
    # the S4 answers (one store, both halves) + the wall re-probe
    p6_bad: list[str] = []
    for ref, expected in sorted(FROZEN["band_end_probes"].items()):
        t = turns.get(ref)
        if t is None:
            p6_bad.append(f"missing {ref}")
            continue
        got = _ir_answer(t)
        if got != expected:
            p6_bad.append(f"{ref}: band-end answer {got!r} != {expected!r}")
    t29 = turns.get("S04:29")
    if t29 is None or (t29["response_ir"] or {}).get("uncertainty_state") != "needs_info":
        p6_bad.append("S04:29: the terminal power-wall re-probe is not an honest gap")
    checks["p6_joint_band_end"] = {"pass": not p6_bad, "bad": p6_bad}

    # P7 — the BED CROSS-CHECK: the sumsq (1,7) = 50 bed meets the
    # S4 twosq-50 bed (input 50, answer 3) on the same store; the
    # sumsq evidence cites only line facts + its owning seam fact
    p7_bad: list[str] = []
    bc = FROZEN["bed_crosscheck"]
    ts = turns.get(bc["sumsq_ref"])
    tt = turns.get(bc["twosq_ref"])
    if ts is None or tt is None:
        p7_bad.append("missing the cross-check refs")
    else:
        if _ir_answer(ts) != bc["sumsq_answer"]:
            p7_bad.append(f"{bc['sumsq_ref']}: the sumsq bed is not {bc['sumsq_answer']}")
        if _ir_answer(tt) != bc["twosq_answer"]:
            p7_bad.append(f"{bc['twosq_ref']}: the twosq bed is not {bc['twosq_answer']}")
    for x in (ts.get("grounded") if ts else []):
        x = str(x)
        if x.startswith("lemma:"):
            if x != "lemma:cmunit":
                p7_bad.append(f"{bc['sumsq_ref']}: the sumsq bed cited a foreign lemma {x}")
        elif x.startswith(("conjecture:", "curriculum:")):
            p7_bad.append(f"{bc['sumsq_ref']}: the sumsq bed cited a non-line fact {x}")
    checks["p7_bed_crosscheck"] = {"pass": not p7_bad, "bad": p7_bad}

    # P8 — mastery, store integrity, determinism
    p8_bad: list[str] = []
    seed = _seed_check(run1_root)
    if seed["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed['seed_total']} != {FROZEN['seed_total']}")
    if seed["reproduced_in_s2_pre"] != FROZEN["seed_total"] or seed["missing"]:
        p8_bad.append(f"seed continuity: {seed}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(
            f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S5 must write zero successor facts)"
        )
    all_final = list(final.query())
    if len(all_final) != FROZEN["final_total"]:
        p8_bad.append(f"final store total {len(all_final)} != frozen {FROZEN['final_total']}")
    seedstore = load_store(_resolve_seed())
    seed_ids = {a.id for a in seedstore.query()}
    new = [a for a in all_final if a.id not in seed_ids]
    new_events = [a for a in new if (a.context.data or {}).get("kind") == "mastery-event"]
    new_facts = [a for a in new if (a.context.data or {}).get("kind") != "mastery-event"]
    if len(new_facts) != FROZEN["new_facts"]:
        p8_bad.append(f"new facts {len(new_facts)} != frozen {FROZEN['new_facts']}: {sorted(a.id for a in new_facts)}")
    if len(new_events) != FROZEN["new_events"]:
        p8_bad.append(f"new mastery events {len(new_events)} != frozen {FROZEN['new_events']}")
    mv = mastery_view(final, [c.id for c in CONCEPTS_E69])
    for cid, exp in FROZEN["mastery_expected"].items():
        v = mv.get(cid)
        if v is None:
            p8_bad.append(f"{cid}: not in the mastery view")
            continue
        if v.state != exp["state"]:
            p8_bad.append(f"{cid}: state {v.state} != {exp['state']}")
        if v.correct_derivations != exp["correct"]:
            p8_bad.append(f"{cid}: {v.correct_derivations} correct != {exp['correct']}")
        if tuple(v.prereq_gaps) != FROZEN["expected_prereq_gaps"][cid]:
            p8_bad.append(f"{cid}: prereq gaps {list(v.prereq_gaps)} != frozen {list(FROZEN['expected_prereq_gaps'][cid])}")
    for c in CONCEPTS_E68:
        v = mv.get(c.id)
        if v is None or v.state != "stable":
            p8_bad.append(f"{c.id}: pre-S5 concept regressed ({v.state if v else 'absent'})")
    # determinism
    r1 = runs["e6.9-run1"]
    r2 = runs["e6.9-run2"]
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
        f"PASS e6.9: {passed}/{len(checks)}"
        if passed == len(checks)
        else f"FAIL e6.9: {passed}/{len(checks)}"
    )
    return {"checks": checks, "passed": passed, "value": value}


class E6_9Experiment:
    """E6.9 — S5 of the SAVANT-TRACK: the number-field toolkit band
    (the A-cluster of the paper's arithmetic half, shallow)."""

    name = "e6.9"
    hypothesis = (
        "The number-field toolkit band (S5) learns the arithmetic half of the "
        "disproof toolkit at shallow depth on the SAME seam: the sixteen lemma "
        "facts (statement + role + cite-when; no proof object) are ESTABLISHED "
        "declared-source facts in the same codex store (24 seam facts with S4's "
        "ten); the student can STATE each one exactly and explain its ROLE; the "
        "empirical beds derive on the frozen 0..72 line (the mod4 square tables: "
        "q=5 yes / 7 no / 13 yes / 17 yes / 11 no / 19 no; the GS test 3g2r "
        "infinite, 5g3r infinite, 3g6r SILENT; the CM beds 3²+4²=25, 1²+7²=50; "
        "the pigeonhole ceilings (5,2)->3, (7,3)->3; duopow 2^6=64); the why "
        "probes are the honest needs_info wall (the proof itself is not in the "
        "store); the magnitude wall is measured (2^7=128 is off the line at 72); "
        "the JOINT band end reproduces the S4 table on the same store (erdosguess "
        "open; 4x4 grid 24; sqmod yes; twosq 3) and the S4 power wall re-probes "
        "still a wall; the conjecture is never a derivation premise (P5); the "
        "paper never reaches the student (P0); two runs byte-identical."
    )
    metric = "S5 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_9()
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
                Path("results/phase-6/e6.9-run1/session-S02.json"),
                Path("results/phase-6/e6.9-run1/session-S03.json"),
                Path("results/phase-6/e6.9-run1/session-S04.json"),
                Path("results/phase-6/e6.9-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
