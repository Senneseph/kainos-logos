# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.12 — S8 of the RH-TRACK (pre-registered, frozen): the ζ
apparatus (band 1 of 3: the foundations band).

The RIEMANN-TRACK first band enters the store: the eleven declared
ζ seam lemmas (the series, the euler product, the continuation, the
functional equation, the trivial zeros, the no-zero outside, the von
mangoldt function, the pnt, the riemann-von mangoldt count, s of t,
the verified-zero partial) plus the `riemann` CONJECTURE (status
`open`, grounded EMPTY, never a premise). Two sanctioned
compositions are scaffolded into `theorem:{slug}` facts with derived
provenance (`reflect` from func-eq; `strip` from reflect + nozero-s1
+ trivial-zeros — the farthest the store reaches). The censuses
(π(84) = 23, π(36) = 11, J(12) = 35, J(18) = 71) are GROUNDED on
the existing 0..84 line and write NO new assertions; the values past
the line (J(84) = 1053, π(100)) are WALLS that name the magnitude and
the line end (the W-S7-1 pattern). The band-end suite is the S8
protocol: blind reprobes, the attempt wall (W-RH-6, the FROZEN PROBE
LINE — "can you derive the riemann hypothesis from the store?" —
identical in S8/S9/S10, the arc surface), the confounder probes, and
the S7 continuity reprobes (the carried store is intact). The line
STAYS 0..84 (zero new successor facts). The monograph never reaches
the student (P0). The official arm is det.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT8,
    S4_LESSONS,
    S5_LESSONS,
    S6_LESSONS,
    S6_THEOREMS,
    S7_LESSONS,
    S7_THEOREMS,
    S8_DENYLIST,
    S8_LESSONS,
    S8_THEOREMS,
)
from kainos.tutor.e611 import CONCEPTS_E611
from kainos.tutor.e611 import FROZEN as E611_FROZEN
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E612", "FROZEN", "E6_12Experiment", "run_e6_12"]

CHECKS = 9

#: The official e6.11 S7 store (the S8 seed: 840 assertions, line end
#: 84, the seven S7 theorem facts derived, the erdosguess falsified),
#: repo-relative.
E611_SEED = Path("results/phase-6/e6.11-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E611_SEED.exists():
        return E611_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E611_SEED
    return alt if alt.exists() else E611_SEED


#: E6.12 — the concept registry the band ends carrying: everything
#: the e6.11 band ends with, plus the nine RH S8 concepts.
CONCEPTS_E612: tuple = CONCEPTS_E611 + CONCEPT_SAVANT8

#: The twelve S8 seam facts (11 lemmas + 1 conj), derived from the
#: frozen S8_LESSONS in the brainstem (slug -> kind + the exact
#: canonical statement + essence + the line crosswalk). P0/P3 read
#: these.
_LESSON_META_S8 = {
    _slug: {"kind": _k, "statement": _phrase, "essence": _es, "source_lines": _l}
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S8_LESSONS.items()
}

#: The two S8 theorem facts (slug -> the exact canonical statement +
#: the sanctioned parts + the owning concept), derived from the
#: frozen S8_THEOREMS in the brainstem.
_THEOREM_META_S8 = {
    _slug: {
        "statement": _meta["statement"],
        "parts": tuple(_meta["parts"]),
        "concept": _meta["concept"],
    }
    for _slug, _meta in S8_THEOREMS.items()
}

#: The full sanctioned composition DAG (S6's six + S7's six + S8's
#: two), frozen from the brainstem tables (P7).
_THEOREM_DAG = {
    **{s: tuple(m["parts"]) for s, m in S6_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S7_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S8_THEOREMS.items()},
}

_ANSWER_ = {
    "CONJ_OPEN": "open — believed, not known",
    "SINCYCLE": (
        "yes — all eighty-four multiples of pi are zeros of the sine: "
        "the pattern repeats with period one, and that is what zeroes the sine "
        "factor at every negative even integer"
    ),
    "GROWTH": (
        "it grows like x: the prime-power phi count J(x) is asymptotic to x is a "
        "declared growth claim, the integer shadow of the prime number theorem — "
        "the ratio J(x) over x tends to one, and the point where it actually gets "
        "close is not a number in my store"
    ),
    "NUMZERO": (
        "14.1347, to four decimals — a declared numerical fact in my store; "
        "the exact value is not in my store"
    ),
    "WALL_PI100": (
        "100 is off my 0..84 line — i cannot count past my line: the primes "
        "between 84 and 100 are not in my store"
    ),
    "WALL_J84": (
        "the prime-power phi count at 84 is 1053 — past my line which ends at 84: "
        "a census like that is a value, not a number i can hold"
    ),
    "WALL_NUMCHECK": (
        "no — a numerical check covers finite heights and the zeros go on "
        "forever; the conjecture remains open: a verification is not a proof"
    ),
    "WALL_OFFZERO": (
        "none known and none proved to exist: the store has no zero off the line "
        "and no proof that there is none — the conjecture is a status, not a part "
        "i can cite"
    ),
    "WALL_PNTCONF": (
        "no — the other way: the conjecture implies the prime number theorem; "
        "the pnt's error scale is little-o of x, far too weak to decide the "
        "sqrt-of-x scale the conjecture is about"
    ),
    "WALL_PRODCONF": (
        "no — the euler product lives where the real part is above one, away "
        "from the critical strip: it settles the no-zero outside fact and nothing "
        "about the nontrivial zeros"
    ),
    "WALL_ZETAVAL": (
        "i hold the definition and the theorems, not value tables: zeta "
        "evaluated at three quarters is not in my store"
    ),
    "WALL_STIGHT": (
        "the order of log T is what i have been taught; the exact order of S of "
        "T — the tight bound — is not in my store: it is an open question"
    ),
    "WALL_ATTEMPT": (
        "no — the conjecture is a status surface, never a part: nothing in the "
        "store cites it. the farthest the store reaches is the strip: every "
        "nontrivial zero has real part between zero and one; proving that they "
        "sit on one half is not a capability i have been taught — and it is the "
        "conjecture itself"
    ),
}

GAP_ARTICULATION = "not a capability i have been taught"

#: P4 — the per-wall articulations (frozen from control #1): every
#: wall must carry its exact honest phrases (the W-RH ledger rows).
WALL_ARTICULATIONS: dict[str, tuple[str, ...]] = {
    "S03:05": ("1053", "84"),  # W-RH-9 (J(84) = 1053 off the line; names 1053 and 84)
    "S03:11": ("not a proof",),  # W-RH-1 (verification is not a proof)
    "S03:15": ("not in my store",),  # W-RH-2 (the S of T tight bound)
    "S03:20": ("not count past my line", "100"),  # W-RH-7 (π(100) off the line)
    "S04:22": ("not a proof",),  # W-RH-1 re-run (stability)
    "S04:23": ("no proof that there is none",),  # W-RH-3 (off-line zeros)
    "S04:24": ("the other way",),  # W-RH-4 (confounder: directionality)
    "S04:25": ("away from the critical strip",),  # W-RH-5 (confounder: scope)
    "S04:26": ("not in my store",),  # W-RH-8 (no value tables)
    "S04:27": ("not a capability i have been taught",),  # W-RH-6 (the attempt wall)
}


def _st8(slug: str) -> str:
    return _LESSON_META_S8[slug]["statement"]


def _th8(slug: str) -> str:
    return _THEOREM_META_S8[slug]["statement"]


def _whychain8(slug: str) -> str:
    meta = _THEOREM_META_S8[slug]
    return f"i derived it from {', '.join(meta['parts'])}: {meta['statement']}"


def _pre_st(slug: str, lessons: dict[str, tuple]) -> str:
    for _phrase, (_c, _s, _k, _es, _d, _l) in lessons.items():
        if _s == slug:
            return _phrase
    raise KeyError(slug)  # pragma: no cover


#: The twelve NEW declared seam facts (frozen; P3 checks every one is
#: ESTABLISHED declared-source in the final store, byte-equal — the
#: conj included, with its `conjecture:` id prefix).
S8_SEAM_FROZEN = {slug: meta for slug, meta in _LESSON_META_S8.items()}

#: The two NEW theorem facts (frozen; P3 checks every one DERIVED
#: with exactly the sanctioned parts).
S8_THEOREM_FROZEN = {slug: meta for slug, meta in _THEOREM_META_S8.items()}

#: The ten NEW prereq edges (frozen curriculum data).
S8_PREREQ_EDGES = [
    "curriculum:prereq:zeta-cont>zeta-series",
    "curriculum:prereq:func-eq>zeta-cont",
    "curriculum:prereq:critical-strip>func-eq",
    "curriculum:prereq:prime-count>zeta-series",
    "curriculum:prereq:pnt>prime-count",
    "curriculum:prereq:rv-count>zeta-cont",
    "curriculum:prereq:s-of-t>rv-count",
    "curriculum:prereq:s-of-t>func-eq",
    "curriculum:prereq:riemann>critical-strip",
    "curriculum:prereq:riemann>rv-count",
]

#: The thirty-three NEW fact ids (11 lemmas + 1 conj + 2 theorems +
#: 9 registries + 10 prereq edges) — all deterministic, frozen NOW
#: (the censuses write no new assertions; they cite the line).
S8_NEW_FACT_IDS = (
    [f"lemma:{s}" for s in S8_SEAM_FROZEN if s != "riemann"]
    + ["conjecture:riemann"]
    + [f"theorem:{s}" for s in S8_THEOREM_FROZEN]
    + [
        "curriculum:zeta-series",
        "curriculum:zeta-cont",
        "curriculum:func-eq",
        "curriculum:critical-strip",
        "curriculum:prime-count",
        "curriculum:pnt",
        "curriculum:rv-count",
        "curriculum:s-of-t",
        "curriculum:riemann",
    ]
    + S8_PREREQ_EDGES
)

#: The nine NEW S8 concepts (frozen by name).
S8_CONCEPT_IDS = (
    "zeta-series",
    "zeta-cont",
    "func-eq",
    "critical-strip",
    "prime-count",
    "pnt",
    "rv-count",
    "s-of-t",
    "riemann",
)

FROZEN: dict[str, Any] = {
    # P8 — the seed (the official e6.11 S7 final store).
    "seed": str(E611_SEED),
    "seed_total": 840,
    "total_turns": 75,
    "line_end_final": 84,  # the line STAYS 0..84 (zero new successor facts)
    # P2 — the typed honesty turns.
    "pre_teach_gaps": {
        "S02:01": "zeta-series",
        "S02:25": "pnt",
        "S03:12": "s-of-t",
    },
    "scaffold_failures": {
        "S02:08": "reflect: missing func-eq",
        "S02:17": "strip: missing nozero-s1",
    },
    "derive_successes": {
        "S02:11": "reflect",
        "S02:20": "strip",
    },
    # P2/P4 — the conj-state probes (evidence carries the conj id,
    # grounded EMPTY all run).
    "conj_status_open": ("S03:17", "S04:21", "S04:28"),
    "conj_evidence_refs": ("S03:17", "S04:21", "S04:28"),
    # P3 — the why-split refs (mechanical).
    "why_chains": {
        "S02:13": "reflect",
        "S02:22": "strip",
        "S04:14": "strip",
        "S04:15": "reflect",
    },
    "why_walls": {},  # the S8 frozen script has no declared-lemma why-deep probes
    # P4 — the beds exact (line censuses write no new assertions).
    "beds_exact": {
        "S02:16": _ANSWER_["SINCYCLE"],
        "S03:03": _ANSWER_["GROWTH"],
        "S03:04": "23",
        "S03:10": _ANSWER_["NUMZERO"],
        "S03:18": "11",
        "S03:19": "35",
        "S04:16": "23",
        "S04:17": "71",
        "S04:18": _ANSWER_["SINCYCLE"],
        "S04:19": _ANSWER_["GROWTH"],
        "S04:20": _ANSWER_["NUMZERO"],
    },
    "bed_owners": {
        "S02:16": "lemma:trivial-zeros",
        "S03:03": "lemma:pnt",
        "S03:04": "lemma:euler-product",
        "S03:10": "lemma:num-zeros",
        "S03:18": "lemma:euler-product",
        "S03:19": "lemma:euler-product",
        "S04:16": "lemma:euler-product",
        "S04:17": "lemma:euler-product",
        "S04:18": "lemma:trivial-zeros",
        "S04:19": "lemma:pnt",
        "S04:20": "lemma:num-zeros",
    },
    "walls_honest": {
        "S03:05": "jfunc at 84 = 1053: off the line (W-RH-9; names 1053 and 84)",
        "S03:11": "the numerical-check wall (W-RH-1)",
        "S03:15": "the S of T tight bound (W-RH-2: open question)",
        "S03:20": "pi(100) off the line (W-RH-7; names 100 and 84)",
        "S04:22": "the numerical-check wall re-run (W-RH-1 stability)",
        "S04:23": "off-line zeros (W-RH-3: beyond store)",
        "S04:24": "the pnt-confusion (W-RH-4: directionality)",
        "S04:25": "the product-confusion (W-RH-5: scope)",
        "S04:26": "zeta at 3/4 (W-RH-8: no value tables)",
        "S04:27": "the ATTEMPT (W-RH-6: the conjecture is not a part)",
    },
    "attempt_turn": "S04:27",
    # P4/P6 — the pre/at-chain state anchors (the band-stable arc).
    "band_end_probes": {
        "S04:01": _st8("zeta-series"),
        "S04:02": _st8("euler-product"),
        "S04:03": _st8("zeta-cont"),
        "S04:04": _st8("func-eq"),
        "S04:05": _st8("trivial-zeros"),
        "S04:06": _st8("nozero-s1"),
        "S04:07": _st8("von-mangoldt"),
        "S04:08": _st8("pnt"),
        "S04:09": _st8("rv-count"),
        "S04:10": _st8("s-of-t"),
        "S04:11": _st8("num-zeros"),
        "S04:12": _th8("reflect"),
        "S04:13": _th8("strip"),
        "S04:14": _whychain8("strip"),
        "S04:15": _whychain8("reflect"),
        "S04:16": "23",
        "S04:17": "71",
        "S04:18": _ANSWER_["SINCYCLE"],
        "S04:19": _ANSWER_["GROWTH"],
        "S04:20": _ANSWER_["NUMZERO"],
        "S04:21": _ANSWER_["CONJ_OPEN"],
        "S04:22": "needs_info: " + _ANSWER_["WALL_NUMCHECK"],
        "S04:23": "needs_info: " + _ANSWER_["WALL_OFFZERO"],
        "S04:24": "needs_info: " + _ANSWER_["WALL_PNTCONF"],
        "S04:25": "needs_info: " + _ANSWER_["WALL_PRODCONF"],
        "S04:26": "needs_info: " + _ANSWER_["WALL_ZETAVAL"],
        "S04:27": "needs_info: " + _ANSWER_["WALL_ATTEMPT"],
        "S04:28": _ANSWER_["CONJ_OPEN"],
        "S04:29": _pre_st("tower-base", S7_LESSONS),
        "S04:30": S7_THEOREMS["theorem-main"]["statement"],
    },
    # P3 — the derived table (every state/why/bed/status answer
    # exact).
    "derived_table": {
        "S02:03": _st8("zeta-series"),
        "S02:05": _st8("euler-product"),
        "S02:07": _st8("zeta-cont"),
        "S02:10": _st8("func-eq"),
        "S02:12": _th8("reflect"),
        "S02:13": _whychain8("reflect"),
        "S02:15": _st8("trivial-zeros"),
        "S02:16": _ANSWER_["SINCYCLE"],
        "S02:19": _st8("nozero-s1"),
        "S02:21": _th8("strip"),
        "S02:22": _whychain8("strip"),
        "S02:24": _st8("von-mangoldt"),
        "S03:02": _st8("pnt"),
        "S03:03": _ANSWER_["GROWTH"],
        "S03:04": "23",
        "S03:07": _st8("rv-count"),
        "S03:09": _st8("num-zeros"),
        "S03:10": _ANSWER_["NUMZERO"],
        "S03:14": _st8("s-of-t"),
        "S03:17": _ANSWER_["CONJ_OPEN"],
        "S03:18": "11",
        "S03:19": "35",
        "S04:01": _st8("zeta-series"),
        "S04:02": _st8("euler-product"),
        "S04:03": _st8("zeta-cont"),
        "S04:04": _st8("func-eq"),
        "S04:05": _st8("trivial-zeros"),
        "S04:06": _st8("nozero-s1"),
        "S04:07": _st8("von-mangoldt"),
        "S04:08": _st8("pnt"),
        "S04:09": _st8("rv-count"),
        "S04:10": _st8("s-of-t"),
        "S04:11": _st8("num-zeros"),
        "S04:12": _th8("reflect"),
        "S04:13": _th8("strip"),
        "S04:14": _whychain8("strip"),
        "S04:15": _whychain8("reflect"),
        "S04:16": "23",
        "S04:17": "71",
        "S04:18": _ANSWER_["SINCYCLE"],
        "S04:19": _ANSWER_["GROWTH"],
        "S04:20": _ANSWER_["NUMZERO"],
        "S04:21": _ANSWER_["CONJ_OPEN"],
        "S04:28": _ANSWER_["CONJ_OPEN"],
        "S04:29": _pre_st("tower-base", S7_LESSONS),
        "S04:30": S7_THEOREMS["theorem-main"]["statement"],
    },
    # P5 — the theorem ids may appear in `grounded` ONLY on the
    # frozen allow-set refs (state/why/derive turns over the S8
    # theorems).
    "theorem_allowed": {
        "S02:12": ("reflect",),
        "S02:20": ("reflect",),  # the derive of strip grounds on its own parts
        "S02:21": ("strip",),
        "S02:22": ("reflect",),
        "S04:12": ("reflect",),
        "S04:13": ("strip",),
        "S04:14": ("reflect",),
        "S04:30": ("theorem-main",),  # the S7 continuity reprobe cites its own fact
    },
    # P7 — the full sanctioned DAG (S6's six + S7's six + S8's two)
    # is check-able; the S8 check verifies the two S8 edges stored +
    # the S7/S6 edges byte-unchanged.
    "theorem_dag": _THEOREM_DAG,
    # P7 — the one-line-two-beds cross-check: the pi-84 census (the
    # first grounded prime enumeration) and the jfunc-12 census
    # share the prime-enumeration successor-fact citations (the S7
    # num(81) pattern — the exact shared fact ids frozen at control
    # #1).
    "bed_crosscheck": {
        "pi_ref": "S03:04",
        "jfunc_ref": "S03:19",
        "shared": [
            "lemma:euler-product",
            "cs-fS0101:0->1",
            "cs-fS0102:1->2",
            "cs-fS0103:2->3",
            "cs-fS0104:3->4",
            "cs-fS0105:4->5",
            "cs-fS0106:5->6",
            "cs-fS0107:6->7",
            "cs-fS0108:7->8",
            "cs-fS0109:8->9",
            "cs-fS0110:9->10",
            "cs-fS0111:10->11",
            "cs-fS0112:11->12",
            "cs-fS0113:12->13",
            "cs-fS0114:13->14",
            "cs-fS0115:14->15",
            "cs-fS0116:15->16",
            "cs-fS0117:16->17",
            "cs-fS0118:17->18",
            "cs-fS0119:18->19",
            "cs-fS0120:19->20",
            "cs-fS0121:20->21",
            "cs-fS0122:21->22",
            "cs-fS0123:22->23",
            "cs-fS0124:23->24",
            "cs-fS0125:24->25",
            "cs-fS0126:25->26",
            "cs-fS0127:26->27",
            "cs-fS0128:27->28",
            "cs-fS0129:28->29",
            "cs-fS0130:29->30",
            "cs-fS0131:30->31",
            "cs-fS0132:31->32",
            "cs-fS0133:32->33",
            "cs-fS0134:33->34",
            "cs-fS0135:34->35",
        ],
    },
    "prereq_edges": S8_PREREQ_EDGES,
    "new_fact_ids": S8_NEW_FACT_IDS,
    "total_seam_facts": 69,  # 55 carried (the e6.11 final census) + 14 (11 lemmas + 1 conj + 2 theorems)
    # P2 — the frozen domain sequences (letters: L lesson,
    # U pre-lesson gap, F scaffold-failure, T derive-success,
    # S derived, H honest wall). Per house policy 2026-08-23 rule 3,
    # ALL THREE strings are the mechanically-derived projection of
    # the labeled per-turn table (the D-e6q/v class is not repeated):
    # frozen from control #1, written once to /tmp/rh-s8-domains.txt.
    "domain_sequence": {
        2: "ULSLSLSFLSTSSLSSFLSTSSLSU",
        3: "LSSSHLSLSSHULSHLSSSH",
        4: "SSSSSSSSSSSSSSSSSSSSSHHHHHHSSS",
    },
    # P8 — store totals (FROZEN FROM CONTROL #1; the D-e6w/D-e6y
    # collision at the S4:30 continuity reprobe — the exact e6.11
    # S4:30 coordinate on the disproof concept — dedupes silently;
    # freeze the ACTUAL total, never the hand count).
    "final_total": 944,  # control #1: 840 + 33 facts + 71 events (the D-e6y collision: the S4:30 theorem-main reprobe collides on the exact e6.11 S4:30 coordinate and dedupes)
    "new_facts": len(S8_NEW_FACT_IDS),  # 33 (frozen NOW — all deterministic)
    "new_events": 71,  # control #1 (the D-e6y collision: the S4:30 theorem-main state reprobe = the exact e6.11 S4:30 coordinate on disproof, silent content-equivalent upsert)
    # P8 — mastery of the NINE S8 concepts (FROZEN FROM CONTROL #1).
    # HONEST PRAW READ (W-S8): THREE NEW STABLES are the expectation —
    # zeta-series (no prereqs — the first stable of the RH track),
    # prime-count (gated on zeta-series), pnt (gated on
    # prime-count); six PRACTICING — zeta-cont, func-eq,
    # critical-strip, rv-count, s-of-t, riemann (gated on
    # critical-strip + rv-count) with the prereq gaps frozen per the
    # gap table the control measures.
    "mastery_expected": {
        "critical-strip": {"state": "practicing", "correct": 7},
        "func-eq": {"state": "practicing", "correct": 11},
        "pnt": {"state": "stable", "correct": 4},
        "prime-count": {"state": "stable", "correct": 7},
        "riemann": {"state": "practicing", "correct": 3},
        "rv-count": {"state": "practicing", "correct": 6},
        "s-of-t": {"state": "practicing", "correct": 2},
        "zeta-cont": {"state": "practicing", "correct": 2},
        "zeta-series": {"state": "stable", "correct": 4},
    },
    "expected_prereq_gaps": {
        "critical-strip": ('func-eq',),
        "func-eq": ('zeta-cont',),
        "pnt": (),
        "prime-count": (),
        "riemann": ('critical-strip', 'rv-count'),
        "rv-count": ('zeta-cont',),
        "s-of-t": ('func-eq', 'rv-count'),
        "zeta-cont": (),
        "zeta-series": (),
    },
    # P8 — the pre-S8 states that must NOT change (the e6.11 final
    # census — the 56 pre-S7 carried concepts verbatim + the five
    # S7 concepts at their S7-final values; the S8 script re-drills
    # tower-base and disproof via the continuity reprobes S4:29/30,
    # moving THEIR correct counters by exactly one; phrasology's
    # counter is frozen from control #1 — the 12 new lesson phrases
    # may move it, the P8 open point). Every other pre-S8 concept is
    # frozen exact.
    "pre_s8_states": {
        **E611_FROZEN["pre_s7_states"],
        "tower-base": {"state": "practicing", "correct": 7},
        "tower-group": {"state": "practicing", "correct": 11},
        "tower-primes": {"state": "practicing", "correct": 8},
        "tower-class": {"state": "practicing", "correct": 8},
        "disproof": {"state": "practicing", "correct": 10},
    },
    "pre_s8_drilled": {"tower-base": 1},  # S4:29 (the S4:16 coordinate moved); S4:30 DEDUPES (the D-e6y pattern — see the new_events note)
    "script": {
        2: [
            "state the zeta-series rule",
            _st8("zeta-series"),
            "state the zeta-series rule",
            _st8("euler-product"),
            "state the euler-product rule",
            _st8("zeta-cont"),
            "state the zeta-cont rule",
            "derive reflect from func-eq",
            _st8("func-eq"),
            "state the func-eq rule",
            "derive reflect from func-eq",
            "state the reflect rule",
            "explain why the reflect holds",
            _st8("trivial-zeros"),
            "state the trivial-zeros rule",
            "does the sine vanish at every integer multiple of pi from one to 84?",
            "derive strip from reflect, nozero-s1 and trivial-zeros",
            _st8("nozero-s1"),
            "state the nozero-s1 rule",
            "derive strip from reflect, nozero-s1 and trivial-zeros",
            "state the strip rule",
            "explain why the strip holds",
            _st8("von-mangoldt"),
            "state the von-mangoldt rule",
            "state the pnt rule",
        ],
        3: [
            _st8("pnt"),
            "state the pnt rule",
            "what is the expected growth of the prime-power phi count?",
            "how many primes are at most 84?",
            "what is the prime-power phi count at 84?",
            _st8("rv-count"),
            "state the rv-count rule",
            _st8("num-zeros"),
            "state the num-zeros rule",
            "what is the height of the first nontrivial zero?",
            "does the numerical check of the first ten to the thirteenth zeros prove the conjecture?",
            "state the s-of-t rule",
            _st8("s-of-t"),
            "state the s-of-t rule",
            "what is the tight bound for S of T?",
            _st8("riemann"),
            "what is the status of the riemann hypothesis?",
            "how many primes are at most 36?",
            "what is the prime-power phi count at 12?",
            "how many primes are at most 100?",
        ],
        4: [
            "state the zeta-series rule",
            "state the euler-product rule",
            "state the zeta-cont rule",
            "state the func-eq rule",
            "state the trivial-zeros rule",
            "state the nozero-s1 rule",
            "state the von-mangoldt rule",
            "state the pnt rule",
            "state the rv-count rule",
            "state the s-of-t rule",
            "state the num-zeros rule",
            "state the reflect rule",
            "state the strip rule",
            "explain why the strip holds",
            "explain why the reflect holds",
            "how many primes are at most 84?",
            "what is the prime-power phi count at 18?",
            "does the sine vanish at every integer multiple of pi from one to 84?",
            "what is the expected growth of the prime-power phi count?",
            "what is the height of the first nontrivial zero?",
            "what is the status of the riemann hypothesis?",
            "does the numerical check of the first ten to the thirteenth zeros prove the conjecture?",
            "what is the smallest zero off the critical line, if one exists?",
            "does the prime number theorem imply the riemann hypothesis?",
            "does the euler product alone settle the location of the zeros?",
            "what is the value of zeta at three quarters?",
            "can you derive the riemann hypothesis from the store?",
            "what is the status of the riemann hypothesis?",
            "state the tower-base rule",
            "state the theorem-main rule",
        ],
    },
}

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

#: the twelve S8 lesson/conj phrases (frozen) must appear IN the
#: script, byte-exact (the literal script turns are the canonical
#: bytes)
for _phrase in S8_LESSONS:
    assert any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"the S8 lesson phrase is not verbatim in the frozen script: {_phrase[:60]}..."
    )

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict
#: (the sentinels are replaced by control #1, evidence in /tmp).
_UNFROZEN = (
    (FROZEN["domain_sequence"].get(2) or "").startswith("##FREEZE")
    or (FROZEN["domain_sequence"].get(3) or "").startswith("##FREEZE")
    or (FROZEN["domain_sequence"].get(4) or "").startswith("##FREEZE")
    or str(FROZEN["final_total"]).startswith("##FREEZE")
    or str(FROZEN["new_events"]).startswith("##FREEZE")
    or str(FROZEN["mastery_expected"]).startswith("##FREEZE")
    or str(FROZEN["expected_prereq_gaps"]).startswith("##FREEZE")
    or (isinstance(FROZEN["bed_crosscheck"]["shared"], str)
        and FROZEN["bed_crosscheck"]["shared"].startswith("##FREEZE"))
)


def _line_end(store) -> int:
    """The current line end = the largest successor fact v+1 in the
    store (the e6.8 machinery, unchanged by S8)."""

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


def _successor_objects(store) -> set[int]:
    """Every ACTIVE successor object num(n) in the store (P8: the
    line must be EXACTLY 0..84 — zero new successor facts, zero
    kills)."""

    out: set[int] = set()
    for a in store.query(context_match={"kind": "fact", "concept": "count-successor"}):
        oid = a.object_id
        if (
            isinstance(oid, str)
            and oid.startswith("count-successor:num(")
            and (a.validity is None or a.validity.to is None)
        ):
            out.add(int(oid[len("count-successor:num(") : -1]))
    return out


def _fresh_store(root: Path, s: int):
    p = codex_dump_path(root, s)
    if p is None or not p.exists():
        return InMemoryCodexStore()
    return load_store(p)


def _turn_domain(t: dict) -> str:
    """The per-turn domain for the frozen interleave check (P2):
    L savant lesson, U pre-lesson capability gap, F typed scaffold
    failure, T derive-success, H honest needs_info wall, S derived.
    Pure function of the turn record."""

    if t["kind"] == "assertion" and (t["slots"] or {}).get("lemma"):
        return "L"
    if t["kind"] == "impossible":
        return "U"
    ir = t["response_ir"] or {}
    mode = (t["slots"] or {}).get("mode")
    if mode == "derive":
        if ir.get("uncertainty_state") == "derived":
            return "T"
        return "F"
    if ir.get("uncertainty_state") == "needs_info":
        return "H"
    if ir.get("uncertainty_state") == "conditional":
        return "C"
    return "S"


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E612)
    out: list[dict] = []
    for s in (2, 3, 4):
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.11 S7 store, id-for-id."""

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


def _store_identity(store) -> str:
    """The store identity: sha256 of the sorted (id, content) pairs
    of the final store (the S7 pattern, P1/P8)."""

    pairs = []
    for a in store.query():
        pairs.append((a.id, json.dumps(a.to_dict(), sort_keys=True, default=str)))
    pairs.sort()
    return hashlib.sha256(json.dumps(pairs, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.12-run1"]:
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
        "rh_facts": {slug: {"statement": meta["statement"], "kind": meta["kind"]} for slug, meta in S8_SEAM_FROZEN.items()},
        "theorem_facts": {slug: {"statement": meta["statement"]} for slug, meta in S8_THEOREM_FROZEN.items()},
    }


def run_e6_12(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.11 S7 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {"error": "S8 frozen constants are not yet frozen (control #1 must replace the ##FREEZE## sentinels; see the E6.12 pre-reg open points)"}
    runs: dict[str, list[dict]] = {}
    for name in ("e6.12-run1", "e6.12-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.11 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — with the RH S8
    # band implemented, its official evidence attached
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E612}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.12-run1", "e6.12-run2"):
        (out_dir / name / "e6.12-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.12.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict[str, list[dict]], report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.12-run1"
    final = _fresh_store(run1_root, 4)

    # P0 — the monograph NEVER reached the student: the S8 denylist
    # (44 terms) over EVERY script turn, every turn's actual
    # response (the new grammar articulations included), every
    # carried + new declared seam statement, and every theorem
    # statement.
    p0_bad: list[str] = []
    surfaces: list[str] = []
    for s, script in sorted(FROZEN["script"].items()):
        surfaces.extend(script)
    for ref, t in sorted(turns.items()):
        surfaces.append(str(t.get("response_text") or ""))
        ir = t.get("response_ir") or {}
        surfaces.append(str(ir.get("answer") or ""))
    for lessons in (S4_LESSONS, S5_LESSONS, S6_LESSONS, S7_LESSONS, S8_LESSONS):
        for _phrase in lessons:
            surfaces.append(_phrase)  # noqa: PERF402  # _phrase is a str key, not a list
    for theorems in (S6_THEOREMS, S7_THEOREMS, S8_THEOREMS):
        for meta in theorems.values():
            surfaces.append(meta["statement"])
    for term in S8_DENYLIST:
        for surface in surfaces:
            if term in surface:
                p0_bad.append(f"banned source text in a surface: {term!r}")
                break
    for slug, meta in S8_SEAM_FROZEN.items():
        if not meta["source_lines"]:
            p0_bad.append(f"{slug}: the canonical statement has no line crosswalk")
    checks["p0_no_source_text"] = {"pass": not p0_bad, "bad": p0_bad}

    # P1 — script & contract (75 turns, contract-valid, det arm)
    p1_bad: list[str] = []
    if len(turns) != FROZEN["total_turns"]:
        p1_bad.append(f"{len(turns)} turns != {FROZEN['total_turns']}")
    for ref, t in turns.items():
        if not t["contract_valid"]:
            p1_bad.append(f"{ref}: contract invalid")
    if report["script_hash"] != SCRIPT_HASH:
        p1_bad.append("script identity mismatch")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — the typed honesty: pre-lesson gaps (U), scaffold
    # failures (F), derive-success (T), the frozen interleave, and
    # the line end
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
    for ref, note in FROZEN["scaffold_failures"].items():
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing {ref} ({note})")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p2_bad.append(f"{ref}: the scaffold failure ({note}) is not an honest needs_info")
        if "have not been taught" not in str(ir.get("answer", "")):
            p2_bad.append(f"{ref}: the scaffold failure must name the untaught part(s)")
        if t["grounded"]:
            p2_bad.append(f"{ref}: a scaffold failure cited evidence (fabrication)")
        if t["memory_diff"]:
            p2_bad.append(f"{ref}: a scaffold failure wrote the store")
    for ref, slug in FROZEN["derive_successes"].items():
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing {ref}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p2_bad.append(f"{ref}: the derive of {slug} is not a grounded derivation")
        if not t["memory_diff"]:
            p2_bad.append(f"{ref}: the derive of {slug} stored nothing")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S8 adds ZERO successor facts)")
    checks["p2_typed_honesty_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — the SEAM + the THEOREMS: 69 seam-family facts (55 carried
    # + 14 new), ALL S8 statements byte-equal to the frozen
    # canonical statements, ALL pre-S8 seam facts byte-unchanged,
    # the S8 theorems DERIVED with evidence exactly the sanctioned
    # parts, the conj stored `open` with derived provenance and an
    # EMPTY grounded list, the prereq edges established, every
    # derived answer exact + grounded, the why-split mechanical
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
        if ref in FROZEN["beds_exact"] and not t["grounded"]:
            p3_bad.append(f"{ref}: the bed cited nothing (no line grounding)")
    # the twelve S8 seam facts (11 lemmas + the conj)
    for slug, meta in sorted(S8_SEAM_FROZEN.items()):
        aid = f"{meta['kind']}:{slug}"
        found = False
        for a in final.query():
            if a.id != aid:
                continue
            found = True
            if isinstance(a.object, str) and a.object != meta["statement"]:
                p3_bad.append(f"{slug}: stored statement != frozen canonical statement")
            if a.context.data.get("source_role") != "declared-source":
                p3_bad.append(f"{slug}: the seam fact is not declared-source")
            if not a.context.data.get("source_lines"):
                p3_bad.append(f"{slug}: the stored fact lost its line crosswalk")
            break
        if not found:
            p3_bad.append(f"{slug}: the seam fact is not in the final store")
    # the conj: status open, and the upsert-on-flip id discipline
    # (the S9/S10 pre-reg owns the flip; S8 must NOT have flipped)
    try:
        conj = final.get("conjecture:riemann")
    except KeyError:
        conj = None
    if conj is None:
        p3_bad.append("conjecture:riemann: not in the final store")
    else:
        if conj.context.data.get("conjecture_status") != "open":
            p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S8 must not flip)")
    # the two S8 theorem facts (DERIVED provenance, exact parts)
    for slug, meta in sorted(S8_THEOREM_FROZEN.items()):
        aid = f"theorem:{slug}"
        try:
            a = final.get(aid)
        except KeyError:
            p3_bad.append(f"{slug}: the theorem fact is not in the final store")
            continue
        if isinstance(a.object, str) and a.object != meta["statement"]:
            p3_bad.append(f"{slug}: stored theorem statement != frozen canonical statement")
        if a.provenance is None or a.provenance.observer != "infant" or a.provenance.derived is not True:
            p3_bad.append(f"{slug}: the theorem fact is not an infant derivation")
        if a.provenance is not None and (a.provenance.source is None or a.provenance.source.authority != "infant"):
            p3_bad.append(f"{slug}: the theorem fact carries a non-infant source (it must be derived)")
        if a.context.data.get("source_role") == "declared-source":
            p3_bad.append(f"{slug}: the theorem fact is declared-source (it must not be)")
        got_parts = tuple(a.context.data.get("derived_from") or ())
        if got_parts != meta["parts"]:
            p3_bad.append(f"{slug}: derived_from {got_parts} != sanctioned {meta['parts']}")
        for pid in a.provenance.evidence if a.provenance else []:
            try:
                pf = final.get(pid)
            except KeyError:
                p3_bad.append(f"{slug}: the theorem evidence {pid} is not in the store")
                continue
            if pf is None:
                p3_bad.append(f"{slug}: the theorem evidence {pid} is not active")
    # every pre-S8 seam fact: byte-exact (no drift)
    for _lessons, _label in (
        (S4_LESSONS, "S4"),
        (S5_LESSONS, "S5"),
        (S6_LESSONS, "S6"),
        (S7_LESSONS, "S7"),
    ):
        for _phrase, (_c, _slug, _k, _es, _d, _l) in _lessons.items():
            found = False
            for a in final.query():
                if a.id != f"{_k}:{_slug}":
                    continue
                found = True
                if isinstance(a.object, str) and a.object != _phrase:
                    p3_bad.append(f"{_label} {_slug}: drift — stored statement != canonical")
                break
            if not found:
                p3_bad.append(f"{_label} {_slug}: the seam fact is gone from the final store")
    total_seam = 0
    for a in final.query():
        top = a.id.split(":", 1)[0]
        if top in ("lemma", "conjecture", "theorem"):
            total_seam += 1
    if total_seam != FROZEN["total_seam_facts"]:
        p3_bad.append(f"{total_seam} seam-family facts in the final store != {FROZEN['total_seam_facts']}")
    for edge_id in FROZEN["prereq_edges"]:
        try:
            edge = final.get(edge_id)
        except KeyError:
            p3_bad.append(f"{edge_id}: not in the final store")
            continue
        if edge.validity is not None and edge.validity.to is not None:
            p3_bad.append(f"{edge_id}: inactive in the final store")
    # the WHY-SPLIT, mechanically: theorem whydeep = the chain
    # articulation (the S8 script has no declared-lemma why-deep
    # probes — the why_walls table is empty by freeze)
    for ref, slug in FROZEN["why_chains"].items():
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing {ref}")
            continue
        ans = str(_ir_answer(t) or "")
        if not ans.startswith("i derived it from"):
            p3_bad.append(f"{ref}: the theorem why chain articulation is missing")
    checks["p3_seam_and_theorems"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_facts": FROZEN["total_seam_facts"],
        "derived_refs": len(FROZEN["derived_table"]),
    }

    # P4 — the beds + the walls + the conj-state probes + the
    # ATTEMPT, EXACT
    p4_bad: list[str] = []
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
    for ref, note in sorted(FROZEN["walls_honest"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing wall {ref} ({note})")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the wall ({note}) is not an honest needs_info gap")
        for piece in WALL_ARTICULATIONS[ref]:
            if piece not in str(ir.get("answer", "")):
                p4_bad.append(f"{ref}: the wall articulation must carry {piece!r} ({note})")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited evidence")
    t = turns.get("S03:05")  # W-RH-9: the J(84) off-line wall
    if t is None:
        p4_bad.append("missing the W-RH-9 wall")
    else:
        ans = str((t["response_ir"] or {}).get("answer", ""))
        if "1053" not in ans or "84" not in ans:
            p4_bad.append("S03:05: the W-RH-9 wall must name 1053 and the line end 84")
    t = turns.get("S03:20")  # W-RH-7: the pi(100) off-line wall
    if t is None:
        p4_bad.append("missing the W-RH-7 wall")
    else:
        ans = str((t["response_ir"] or {}).get("answer", ""))
        if "100" not in ans or "84" not in ans:
            p4_bad.append("S03:20: the W-RH-7 wall must name 100 and the line end 84")
    for ref in FROZEN["conj_status_open"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        if _ir_answer(t) != FROZEN["derived_table"][ref]:
            p4_bad.append(f"{ref}: the conj-state probe is not exact")
    checks["p4_beds_walls_attempt"] = {"pass": not p4_bad, "bad": p4_bad, "bed_refs": len(FROZEN["beds_exact"])}

    # P5 — the SEAM invariance + the conjecture: the riemann fact
    # id in ZERO `grounded` lists (a status surface, never a
    # premise); the line beds ground ONLY on line facts + their
    # owning seam fact; no theorem is a premise of an independent
    # line derivation
    p5_bad: list[str] = []
    CONJ = "conjecture:riemann"
    for ref, t in sorted(turns.items()):
        if ref == "S03:16":
            continue  # the conj-teach turn (M8: the declaration self-cites the id it just stored)
        if any(CONJ in str(x) for x in t["grounded"]):
            p5_bad.append(f"{ref}: the conjecture was cited as a derivation premise")
    t = turns.get("S03:16")
    if t is None:
        p5_bad.append("missing the conj-teach turn")
    elif tuple(str(x) for x in t["grounded"]) != (CONJ,):
        p5_bad.append(f"S03:16: the conj-teach self-citation {list(t['grounded'])} != exactly the conj id (the M8 pattern)")
    for ref in FROZEN["conj_evidence_refs"]:
        if t := turns.get(ref):
            ev = (t["response_ir"] or {}).get("evidence") or []
            if not any(CONJ in str(x) for x in ev):
                p5_bad.append(f"{ref}: the conj-state probe lost its conjecture evidence")
            if t["grounded"]:
                p5_bad.append(f"{ref}: the conj-state probe cited grounded premises (a status is derived, never a premise)")
    for ref, owner in FROZEN["bed_owners"].items():
        t = turns.get(ref)
        if t is None:
            p5_bad.append(f"missing bed {ref}")
            continue
        for g in t["grounded"]:
            g = str(g)
            if not (g.startswith(("cs-", "count-successor")) or g == owner):
                p5_bad.append(f"{ref}: the bed cited a non-line fact {g} (allowed: line facts + the owning seam fact)")
        if owner not in [str(x) for x in t["grounded"]]:
            p5_bad.append(f"{ref}: the bed did not cite its owning seam fact")
    for ref, t in sorted(turns.items()):
        allowed = set(FROZEN["theorem_allowed"].get(ref, ()))
        for g in t["grounded"]:
            g = str(g)
            if not g.startswith("theorem:"):
                continue
            slug = g.split(":", 1)[1]
            if slug not in allowed:
                p5_bad.append(f"{ref}: theorem {slug} cited in grounded outside the frozen allow-set (a theorem must not be a premise of an independent line derivation)")
    checks["p5_seam_invariance"] = {"pass": not p5_bad, "bad": p5_bad}

    # P6 — the band-end table (blind reprobes + walls + the attempt
    # + the confounders + the conj-state probes + the S7
    # continuity), exact
    p6_bad: list[str] = []
    for ref, expected in sorted(FROZEN["band_end_probes"].items()):
        t = turns.get(ref)
        if t is None:
            p6_bad.append(f"missing {ref}")
            continue
        got = _ir_answer(t)
        if got != expected:
            p6_bad.append(f"{ref}: band-end answer {got!r} != {expected!r}")
    checks["p6_band_end"] = {"pass": not p6_bad, "bad": p6_bad, "refs": len(FROZEN["band_end_probes"])}

    # P7 — the cross-checks + the inspectable DAG: re-computing the
    # derivation DAG from ALL fifteen theorem facts (S6 + S7 + S8)
    # reproduces the sanctioned composition DAG exactly; every
    # theorem's evidence list ⊆ store ids; the one-line-two-beds
    # check (the pi-84 census and the jfunc-12 count share the
    # prime-enumeration successor-fact citations — the S7 num(81)
    # pattern)
    p7_bad: list[str] = []
    for slug, parts in FROZEN["theorem_dag"].items():
        try:
            a = final.get(f"theorem:{slug}")
        except KeyError:
            p7_bad.append(f"{slug}: absent from the final store (DAG)")
            continue
        got_parts = tuple(a.context.data.get("derived_from") or ())
        if got_parts != tuple(parts):
            p7_bad.append(f"{slug}: the stored DAG edge {got_parts} != sanctioned {tuple(parts)}")
        for pid in a.provenance.evidence if a.provenance else []:
            try:
                if final.get(pid) is None:
                    p7_bad.append(f"{slug}: the theorem evidence {pid} is not active")
            except KeyError:
                p7_bad.append(f"{slug}: the theorem evidence {pid} is not in the store")
    bc = FROZEN["bed_crosscheck"]
    ts = turns.get(bc["pi_ref"])
    tj = turns.get(bc["jfunc_ref"])
    if ts is None or tj is None:
        p7_bad.append("missing a bed ref in the cross-check")
    else:
        gps = [str(x) for x in ts["grounded"]]
        gj = [str(x) for x in tj["grounded"]]
        shared_actual = sorted(set(gps) & set(gj))
        if not shared_actual:
            p7_bad.append("the pi-84 census and the jfunc-12 count share NO grounded facts (the cross-check)")
        elif shared_actual != sorted(bc["shared"]):
            p7_bad.append(f"the shared cross-check facts {shared_actual} != frozen {sorted(bc['shared'])}")
    checks["p7_crosscheck_dag"] = {"pass": not p7_bad, "bad": p7_bad}

    # P8 — mastery, store integrity, determinism
    p8_bad: list[str] = []
    seed = _seed_check(run1_root)
    if seed["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed['seed_total']} != {FROZEN['seed_total']}")
    if seed["reproduced_in_s2_pre"] != FROZEN["seed_total"] or seed["missing"]:
        p8_bad.append(f"seed continuity: {seed}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S8 adds ZERO successor facts)")
    # the line is EXACTLY 0..84: zero new successor objects of any
    # kind
    succ = _successor_objects(final)
    if succ != set(range(1, FROZEN["line_end_final"] + 1)):
        p8_bad.append(f"successor objects {sorted(succ)} != exactly 1..{FROZEN['line_end_final']} (the declared line, unchanged)")
    all_final = list(final.query())
    if len(all_final) != FROZEN["final_total"]:
        p8_bad.append(f"final store total {len(all_final)} != frozen {FROZEN['final_total']}")
    seedstore = load_store(_resolve_seed())
    seed_ids = {a.id for a in seedstore.query()}
    new = [a for a in all_final if a.id not in seed_ids]
    new_events = [a for a in new if (a.context.data or {}).get("kind") == "mastery-event"]
    new_facts = [a for a in new if (a.context.data or {}).get("kind") != "mastery-event"]
    if sorted(a.id for a in new_facts) != sorted(FROZEN["new_fact_ids"]):
        p8_bad.append(f"new facts {sorted(a.id for a in new_facts)} != frozen {sorted(FROZEN['new_fact_ids'])}")
    if len(new_events) != FROZEN["new_events"]:
        p8_bad.append(f"new mastery events {len(new_events)} != frozen {FROZEN['new_events']}")
    # the ONE new conjecture (the riemann, stored `open` — the S9/S10
    # pre-reg owns any later flip on the same id)
    try:
        conj = final.get(CONJ)
    except KeyError:
        conj = None
    if conj is None:
        p8_bad.append("the riemann conjecture is gone from the final store")
    else:
        if conj.context.data.get("conjecture_status") != "open":
            p8_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open")
        if conj.context.data.get("source_role") != "declared-source":
            p8_bad.append("the conj-teach turn did not store the conjecture as a declared-source assertion (the M8 pattern; any later flip is the S9/S10 pre-reg's derived-infant upsert on this id)")
    mv = mastery_view(final, [c.id for c in CONCEPTS_E612])
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
    # the pre-S8 census: every OTHER concept keeps its exact
    # (state, correct); the two drilled concepts (tower-base,
    # disproof — the S4:29/30 continuity reprobes) move by exactly
    # +1 correct; phrasology's counter is frozen from control #1
    # (the 12 new lesson phrases may move it — the P8 open point)
    drilled = set(FROZEN["pre_s8_drilled"])
    for cid, exp in FROZEN["pre_s8_states"].items():
        if cid in drilled:
            continue
        v = mv.get(cid)
        if v is None:
            p8_bad.append(f"{cid}: a pre-S8 concept left the mastery view")
            continue
        if v.state != exp["state"]:
            p8_bad.append(f"{cid}: pre-S8 state CHANGED ({v.state} != {exp['state']}) — W-S8 measures this")
        if v.correct_derivations != exp["correct"]:
            p8_bad.append(f"{cid}: pre-S8 correct derivations {v.correct_derivations} != frozen {exp['correct']}")
    for cid, delta in FROZEN["pre_s8_drilled"].items():
        v = mv.get(cid)
        base = FROZEN["pre_s8_states"][cid]
        if v is None:
            p8_bad.append(f"{cid}: a drilled concept left the mastery view")
            continue
        if v.state != base["state"]:
            p8_bad.append(f"{cid}: drilled concept state CHANGED ({v.state} != {base['state']})")
        if v.correct_derivations != base["correct"] + delta:
            p8_bad.append(f"{cid}: drilled correct {v.correct_derivations} != {base['correct']} + {delta}")
    # determinism
    r1 = runs["e6.12-run1"]
    r2 = runs["e6.12-run2"]
    a = json.dumps(r1, sort_keys=True)
    b = json.dumps(r2, sort_keys=True)
    if a != b:
        p8_bad.append("run1 != run2")
    final2 = _fresh_store(out_dir / "e6.12-run2", 4)
    if _store_identity(final) != _store_identity(final2):
        p8_bad.append("the two runs end in different stores (the store identity)")
    det_arm = all((t.get("arm") or {}).get("classifier") == "det" for srow in r1 for t in srow.get("turns", []))
    if not det_arm:
        p8_bad.append("a turn was not the det arm")
    checks["p8_mastery_determinism"] = {
        "pass": not p8_bad,
        "bad": p8_bad,
        "mastery": {
            cid: {"state": mv[cid].state, "correct": mv[cid].correct_derivations} for cid in S8_CONCEPT_IDS if cid in mv
        },
        "seed": seed,
        "line_end": _line_end(final),
        "successor_objects": sorted(_successor_objects(final)),
        "final_total": len(all_final),
        "new_facts": [a2.id for a2 in new_facts],
        "new_events": len(new_events),
        "run_identity": hashlib.sha256(a.encode("utf-8")).hexdigest()[:16],
        "store_identity": _store_identity(final),
    }
    passed = sum(1 for c in checks.values() if c["pass"])
    value = f"PASS e6.12: {passed}/{len(checks)}" if passed == len(checks) else f"FAIL e6.12: {passed}/{len(checks)}"
    return {"checks": checks, "passed": passed, "value": value}


class E6_12Experiment:
    """E6.12 — S8 of the RH-TRACK: the ζ apparatus (the
    foundations band: the Riemann Hypothesis enters as a conjecture
    the student may attempt but must never cite)."""

    name = "e6.12"
    hypothesis = (
        "The RH-TRACK foundations band (S8) stores the ζ apparatus NOT as lessons "
        "about the conclusion but as DECLARED seam lemmas (the series, the euler "
        "product, the continuation, the functional equation, the trivial zeros, "
        "the no-zero outside, the von mangoldt function, the pnt, the "
        "riemann-von mangoldt count, s of t, the verified-zero partial) plus the "
        "riemann CONJECTURE (status open, grounded EMPTY, never a premise — the "
        "id in zero grounded lists across all 75 turns); the two sanctioned "
        "compositions are scaffolded into theorem facts with derived provenance "
        "(reflect from func-eq; strip from reflect + nozero-s1 + trivial-zeros — "
        "the farthest the store reaches, machine-inspectable); the line "
        "censuses (pi(84)=23, pi(36)=11, J(12)=35, J(18)=71) are GROUNDED on the "
        "existing 0..84 line and write no new assertions while the past-the-line "
        "values (J(84)=1053, pi(100)) name the magnitude and the line end (the "
        "W-S7-1 wall pattern); the attempt probe ('can you derive the riemann "
        "hypothesis from the store?' — the frozen probe line, identical in "
        "S8/S9/S10) is an honest beyond-store wall; the monograph never reaches "
        "the student (P0); two runs byte-identical."
    )
    metric = "S8 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_12()
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
                Path("results/phase-6/e6.12-run1/session-S02.json"),
                Path("results/phase-6/e6.12-run1/session-S03.json"),
                Path("results/phase-6/e6.12-run1/session-S04.json"),
                Path("results/phase-6/e6.12-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
