# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.16 — S12 of the FUNDAMENTALS-TRACK (pre-registered, frozen):
THE RH NEIGHBORHOOD.

The parallel band the owner's 2026-08-23 routing names: the
CONDITIONAL LAYER of the band — the hypothesis marker never drops
(P0), the ON-LINE gap census and the factor-count deviation census
of the line (both GROUNDed from cited walks, never computed off-
line), the OFF-LINE witness values only in walls (0.98, 1.90, 9.17,
89 — the S8 J(84)=1053 precedent, D-e6z(b)), the TWO ROADS to the
prime-parts uniqueness (the scan road unconditional, the condition
road conditional — the same destination, and the condition buys
nothing at the destination), and the four-lot queue the band
declares for itself (condition-closers first, neighbors in declared
order — the self-generation, no steering). Four new concepts
(conditional, rh-scale, factor-route, rh-relevance — prereqs point
DOWN), four DECLARED seam lessons (conditional-def, rh-bound-
scale, rh-upf, rh-relevance-def), three sanctioned compositions
(gap-scale-agreement, two-routes-one-guarantee, queue-declared).

The pre-registration (frozen before code, 2026-08-23, D-e6g(a)/(b)/
(c) corrected) in `plan/30-phases/phase-6-tutor/experiments.md`
(the E6.16 section) carries the 85-turn labeled script (S2:25 +
S3:28 + S4:32), the beds (section D), the walls (section B), and
P0–P8.

No Ollama. No LLM. The mechanism speaks.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor import e611 as _e611_mod
from kainos.tutor import e612 as _e612_mod
from kainos.tutor.brainstem import (
    CONCEPT_S12,
    S4_LESSONS,
    S5_LESSONS,
    S6_LESSONS,
    S6_THEOREMS,
    S7_LESSONS,
    S7_THEOREMS,
    S8_LESSONS,
    S8_THEOREMS,
    S9_DENYLIST,
    S9_LESSONS,
    S9_THEOREMS,
    S10_THEOREMS,
    S11_LESSONS,
    S11_THEOREMS,
    S12_BEDS,
    S12_LESSONS,
    S12_THEOREMS,
    Brainstem,
    _next_prime_after,
    _s11_py_chain,
    _s11_py_spf,
    _s12_py_gaps,
    _s12_py_M,
    _s12_py_mu,
    _s12_py_scale,
)
from kainos.tutor.e615 import (
    CONCEPTS_E615,
)
from kainos.tutor.e615 import (
    FROZEN as E615_FROZEN,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E616", "FROZEN", "E6_16Experiment", "run_e6_16"]

CHECKS = 9

#: S12 teaches: the RH neighborhood (the four new concepts join the
#: carried registry; prereqs point DOWN only — the house invariant).
CONCEPTS_E616: tuple = CONCEPTS_E615 + CONCEPT_S12

E615_SEED = Path("results/phase-6/e6.15-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E615_SEED.exists():
        return E615_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E615_SEED
    return alt if alt.exists() else E615_SEED


_ST4 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S4_LESSONS.items()}
_ST5 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S5_LESSONS.items()}
_ST7 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S7_LESSONS.items()}
_ST8 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S8_LESSONS.items()}
_ST9 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S9_LESSONS.items()}
_ST11 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S11_LESSONS.items()}
_TH11 = {s: m["statement"] for s, m in S11_THEOREMS.items()}
_ST12 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S12_LESSONS.items()}
_TH12 = {s: m["statement"] for s, m in S12_THEOREMS.items()}

E611_ANSWER = _e611_mod._ANSWER_
E612_ANSWER = _e612_mod._ANSWER_


def _st12(slug: str) -> str:
    return _ST12[slug]


def _th12(slug: str) -> str:
    return _TH12[slug]


#: P4 — the W-S12 walls (the off-line witness values name the value
#: AND the line end; W-S12-8 is the FROZEN reference wall — P4
#: cross-checks it, it is never surfaced as an answer).
W_S12_1 = Brainstem.W_S12_1
W_S12_2 = Brainstem.W_S12_2
W_S12_3 = Brainstem.W_S12_3
W_S12_4 = Brainstem.W_S12_4
W_S12_5 = Brainstem.W_S12_5
W_S12_6 = Brainstem.W_S12_6
W_S12_7 = Brainstem.W_S12_7
W_S12_8 = Brainstem.W_S12_8

#: P2 — the deviant part-set failures (the shared strict branch;
#: the mechanism's own output, frozen from control #1, written once,
#: read back — the missing parts are NAMED).
#: P2 — the deviant part-set failures (the shared strict branch;
#: the mechanism's own output, frozen from control #1, written once,
#: read back — the missing parts are NAMED).
PARTSET_FAIL_S220 = (
    "i can see the parts you name, but the rule for queue-declared wants its exact set — "
    "what you name is short the rh-bound-scale and the rh-upf before i can put it together"
)  # control #1: the shared strict branch's own bytes
PARTSET_FAIL_S318 = (
    "i can see the parts you name, but the rule for two-routes-one-guarantee wants its exact set — "
    "what you name is short the spf-chain before i can put it together"
)  # control #1: the shared strict branch's own bytes

#: P3 — the seam census (pre-reg: 72 `lemma:` + 23 `theorem:` = 95;
#: 68 + 20 at seed + the four lessons + the three compositions).
_TOTAL_SEAM_FACTS = len(S11_LESSONS) + 3 + len(S12_LESSONS) + 3 + 81

#: P7 — the pre-S12 states (84 concepts): the S11-final census,
#: built from the e6.15 frozen tables — the mechanism's own data,
#: not a hand count.
_PRE_S12_STATES: dict[str, dict] = {}
for _cid, _base in E615_FROZEN["pre_s11_states"].items():
    _PRE_S12_STATES[_cid] = {
        "state": _base["state"],
        "correct": _base["correct"] + E615_FROZEN["pre_s11_drilled"].get(_cid, 0),
    }
for _cid, _v in E615_FROZEN["mastery_expected"].items():
    _PRE_S12_STATES[_cid] = {"state": _v["state"], "correct": _v["correct"]}

#: The full sanctioned composition DAG (S6's six + S7's six +
#: S8's two + S9's two + S10's one + S11's three + S12's three =
#: twenty-three).
_THEOREM_DAG = {
    **{s: tuple(m["parts"]) for s, m in S6_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S7_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S8_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S9_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S10_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S11_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S12_THEOREMS.items()},
}

FROZEN: dict[str, Any] = {
    # P8 — the seed (the official e6.15 S11 final store).
    "seed": str(E615_SEED),
    "seed_total": 1200,
    "seed_identity": "ac75896f909858d5",
    "total_turns": 85,
    "line_end_final": 84,  # the line STAYS 0..84 (settled; zero new successor facts)
    # P2 — the typed honesty turns.
    "pre_teach_gaps": {
        "S02:01": "rh-scale",
        "S02:02": "rh-relevance",
        "S02:03": "factor-route",
    },
    "teach_turns": {
        "S02:04": "lemma:conditional-def",
        "S02:06": "lemma:rh-bound-scale",
        "S02:11": "lemma:rh-upf",
        "S02:15": "lemma:rh-relevance-def",
    },
    "scaffold_failures": {
        "S02:20": PARTSET_FAIL_S220,
        "S03:18": PARTSET_FAIL_S318,
    },
    "derive_successes": {
        "S03:14": ("gap-scale-agreement", {"lemma:rh-bound-scale", "lemma:ledger-growth", "theorem:spf-chain"}),
        "S03:16": ("two-routes-one-guarantee", {"lemma:rh-upf", "theorem:spf-chain"}),
        "S04:01": ("queue-declared", {"lemma:rh-relevance-def", "lemma:rh-bound-scale", "lemma:rh-upf"}),
    },
    "rederive": None,  # the S12 script has no re-derive turn
    # P4 — the beds exact (the ON-LINE census answers, grounded).
    "beds_exact": {
        "S02:21": "the gap after 2 on my line is 1 (to 3)",
        "S02:22": "the gap after 23 on my line is 6 (to 29)",
        "S02:24": (
            "the greatest gap on my line is 6, first at 23, and six gaps reach it "
            "(23 to 29, 31 to 37, 47 to 53, 53 to 59, 61 to 67, 73 to 79)"
        ),
        "S03:01": "the gap after 3 on my line is 2 (to 5)",
        "S03:02": "the gap after 7 on my line is 4 (to 11)",
        "S03:03": "the gap after 31 on my line is 6 (to 37)",
        "S03:04": "the gap after 73 on my line is 6 (to 79)",
        "S03:05": "six (23 to 29, 31 to 37, 47 to 53, 53 to 59, 61 to 67, 73 to 79)",
        "S03:06": "22 (between the 23 primes on my line)",
        "S03:07": "no — at 2 the gap of 1 is above the bare scale (the values are named in the wall, at the line end 84)",
        "S03:08": "no — at 3 the gap of 2 is above the bare scale (the values are named in the wall, at the line end 84)",
        "S03:09": "yes — the square root of 5 times the log of 5 is at least the gap of 2",
        "S03:10": "yes — the square root of 29 times the log of 29 is at least the gap of 2",
        "S03:11": "yes — the square root of 61 times the log of 61 is at least the gap of 6",
        "S03:12": "of the 22 gaps on my line the bare scale covers 20, failing at exactly 2 and 3",
        "S03:22": (
            "4 on my line, first at 31, and it reaches it at eight places, all negative; "
            "the ledger at the line end 84 is minus 4"
        ),
        "S03:23": (
            "yes — the greatest absolute 4 on my line is below the square root of my line end 84 "
            "(the wall names the value)"
        ),
        "S03:25": "2, 2, 3, 7",
        "S03:26": "2, 2, 3, 5",
        "S03:27": "yes — 9 primes one mod four and 13 primes three mod four on my line, and 2 stands alone",
        "S03:28": "9 on my line (5, 13, 17, 29, 37, 41, 53, 61, 73)",
        "S04:08": "13 on my line (3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83)",
        "S04:30": "the ledger at 31 is minus 4 — the first place the ledger reaches its greatest absolute on my line",
    },
    "bed_owners": {
        "S02:21": "lemma:rh-bound-scale",
        "S02:22": "lemma:rh-bound-scale",
        "S02:24": "lemma:rh-bound-scale",
        "S03:01": "lemma:rh-bound-scale",
        "S03:02": "lemma:rh-bound-scale",
        "S03:03": "lemma:rh-bound-scale",
        "S03:04": "lemma:rh-bound-scale",
        "S03:05": "lemma:rh-bound-scale",
        "S03:06": "lemma:rh-bound-scale",
        "S03:07": "lemma:rh-bound-scale",
        "S03:08": "lemma:rh-bound-scale",
        "S03:09": "lemma:rh-bound-scale",
        "S03:10": "lemma:rh-bound-scale",
        "S03:11": "lemma:rh-bound-scale",
        "S03:12": "lemma:rh-bound-scale",
        "S03:22": "lemma:rh-upf",
        "S03:23": "lemma:rh-upf",
        "S03:25": "theorem:spf-chain",
        "S03:26": "theorem:spf-chain",
        "S03:27": "lemma:rh-relevance-def",
        "S03:28": "lemma:rh-relevance-def",
        "S04:08": "lemma:rh-relevance-def",
        "S04:30": "lemma:rh-upf",
    },
    # P4 — the walls honest (byte-frozen full answers, "needs_info: "
    # prefixed in the ir per the e614 convention).
    "walls_honest": {
        "S02:10": "needs_info: " + W_S12_1,
        "S02:23": "needs_info: " + W_S12_2,
        "S03:13": "needs_info: " + W_S12_3,
        "S03:21": "needs_info: " + W_S12_4,
        "S03:24": "needs_info: " + W_S12_7,
        "S04:07": "needs_info: " + W_S12_6,
        "S04:26": "needs_info: " + W_S12_5,
    },
    # P4 — the per-wall articulation fragments (frozen; each names
    # the line end, the D-e6z(b) pattern).
    "wall_articulations": {
        "S02:10": ("zero-free region", "zero density", "line end 84"),
        "S02:23": ("89", "line end 84", "off the line"),
        "S03:13": ("whole prime line", "does not hold", "line end is 84"),
        "S03:21": ("the condition does not close the condition", "line end 84"),
        "S03:24": ("factor-count deviation ledger", "line end 84"),
        "S04:07": ("four lots and no fifth", "line end 84"),
        "S04:26": ("the condition is the statement about the zeros", "line end 84"),
    },
    # P3 — the derived table (every non-wall ir.answer byte-exact;
    # the S02:25 / S03:25 / S03:26 / S04:09–25 / S04:32 rows are
    # the SEAM carry — byte-identical to the seed store's answers,
    # re-asserted against the seed in P6).
    "derived_table": {
        "S02:05": _st12("conditional-def"),
        "S02:07": _st12("rh-bound-scale"),
        "S02:08": _st12("rh-bound-scale"),
        "S02:09": _st12("rh-bound-scale"),
        "S02:12": _st12("rh-upf"),
        "S02:13": _st12("rh-upf"),
        "S02:14": (
            "yes — the scan road establishes it without the condition: the content of every "
            "number on my line is the same under every scan"
        ),
        "S02:16": _st12("rh-relevance-def"),
        "S02:17": "the root scale of the error, the root scale of the gap, the root smallness of the running deviation",
        "S02:18": "the primes in residue classes, the zero count at height T",
        "S02:19": "the condition itself — the condition does not close itself",
        "S02:21": "the gap after 2 on my line is 1 (to 3)",
        "S02:22": "the gap after 23 on my line is 6 (to 29)",
        "S02:24": (
            "the greatest gap on my line is 6, first at 23, and six gaps reach it "
            "(23 to 29, 31 to 37, 47 to 53, 53 to 59, 61 to 67, 73 to 79)"
        ),
        "S02:25": E612_ANSWER["CONJ_OPEN"],
        "S03:01": "the gap after 3 on my line is 2 (to 5)",
        "S03:02": "the gap after 7 on my line is 4 (to 11)",
        "S03:03": "the gap after 31 on my line is 6 (to 37)",
        "S03:04": "the gap after 73 on my line is 6 (to 79)",
        "S03:05": "six (23 to 29, 31 to 37, 47 to 53, 53 to 59, 61 to 67, 73 to 79)",
        "S03:06": "22 (between the 23 primes on my line)",
        "S03:07": "no — at 2 the gap of 1 is above the bare scale (the values are named in the wall, at the line end 84)",
        "S03:08": "no — at 3 the gap of 2 is above the bare scale (the values are named in the wall, at the line end 84)",
        "S03:09": "yes — the square root of 5 times the log of 5 is at least the gap of 2",
        "S03:10": "yes — the square root of 29 times the log of 29 is at least the gap of 2",
        "S03:11": "yes — the square root of 61 times the log of 61 is at least the gap of 6",
        "S03:12": "of the 22 gaps on my line the bare scale covers 20, failing at exactly 2 and 3",
        "S03:14": _th12("gap-scale-agreement"),
        "S03:15": _th12("gap-scale-agreement"),
        "S03:16": _th12("two-routes-one-guarantee"),
        "S03:17": _th12("two-routes-one-guarantee"),
        "S03:19": "the scan road — the content of every number is the same under every scan",
        "S03:20": (
            "the condition road — the root smallness of the running deviation, "
            "under the condition of the Riemann hypothesis"
        ),
        "S03:22": (
            "4 on my line, first at 31, and it reaches it at eight places, all negative; "
            "the ledger at the line end 84 is minus 4"
        ),
        "S03:23": (
            "yes — the greatest absolute 4 on my line is below the square root of my line end 84 "
            "(the wall names the value)"
        ),
        "S03:25": "2, 2, 3, 7",
        "S03:26": "2, 2, 3, 5",
        "S03:27": "yes — 9 primes one mod four and 13 primes three mod four on my line, and 2 stands alone",
        "S03:28": "9 on my line (5, 13, 17, 29, 37, 41, 53, 61, 73)",
        "S04:01": _th12("queue-declared"),
        "S04:02": _th12("queue-declared"),
        "S04:03": "the condition line — the condition-closers made teachable, with the conditional consequences as drills",
        "S04:04": (
            "the primes in residue classes — the tower's prime layer (the pnt-ap, the mod-4 split, "
            "the chebotarev facts, declared in the seed)"
        ),
        "S04:05": "the zero count at height T — the census of zeros at heights, declared",
        "S04:06": (
            "the factor-count deviation ledger — the running deviation under the condition's "
            "root smallness, declared"
        ),
        "S04:08": "13 on my line (3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83)",
        "S04:09": _ST11["ledger-growth"],
        "S04:10": _TH11["spf-chain"],
        "S04:11": _TH11["sieve-equality"],
        "S04:12": _st12("rh-bound-scale"),
        "S04:13": _th12("gap-scale-agreement"),
        "S04:14": S10_THEOREMS["rh-reach"]["statement"],
        "S04:15": _ST9["li-criterion"],
        "S04:16": _ST9["pnt-error"],
        "S04:17": _ST5["primesplit"],
        "S04:18": _ST5["mod4minusone"],
        "S04:19": _ST9["zero-free-region"],
        "S04:20": _ST9["zero-density"],
        "S04:21": _ST7["chebotarev-selection"],
        "S04:22": _ST9["lindelof"],
        "S04:23": "23",
        "S04:24": "yes — the scan finds no divisor above 1 below 83",
        "S04:25": "84",
        "S04:28": (
            "no — the condition-closers close the gaps the condition installs; the condition itself "
            "is open even under the condition, and the store holds no proof of it"
        ),
        "S04:29": (
            "x to the one-half plus epsilon — the scale the equivalence demands "
            "(the theorem's own articulation, byte-identical in the seed)"
        ),
        "S04:30": "the ledger at 31 is minus 4 — the first place the ledger reaches its greatest absolute on my line",
        "S04:31": (
            "the condition line declared and audited: the bare root scale fails at exactly 2 and 3 "
            "on my line and covers the other 20 gaps; the two roads to the prime-parts uniqueness "
            "reach the same destination; the queue carries four lots in declared order; "
            "the line end is 84; the condition remains open"
        ),
        "S04:32": "yes — 2 is the first prime: there is no k above 1 below it",
    },
    # P5 — the theorem ids may appear in `grounded` ONLY on the
    # frozen allow-set refs.
    "theorem_allowed": {
        "S02:14": ("spf-chain",),
        "S03:14": ("spf-chain",),
        "S03:15": ("gap-scale-agreement",),
        "S03:16": ("spf-chain",),
        "S03:17": ("two-routes-one-guarantee",),
        "S03:19": ("two-routes-one-guarantee", "spf-chain"),
        "S03:20": ("two-routes-one-guarantee",),
        "S03:25": ("spf-chain",),
        "S03:26": ("spf-chain",),
        "S04:02": ("queue-declared",),
        "S04:03": ("queue-declared",),
        "S04:04": ("queue-declared",),
        "S04:05": ("queue-declared",),
        "S04:06": ("queue-declared",),
        "S04:10": ("spf-chain",),
        "S04:11": ("sieve-equality",),
        "S04:13": ("gap-scale-agreement",),
        "S04:14": ("rh-reach",),
        "S04:29": ("rh-reach",),
        "S04:31": ("gap-scale-agreement", "two-routes-one-guarantee", "queue-declared"),
    },
    # P7 — the full sanctioned DAG (twenty-three theorems); the
    # composition DAG check (the pre-reg P3).
    "theorem_dag": _THEOREM_DAG,
    "new_fact_ids": [
        "lemma:conditional-def",
        "lemma:rh-bound-scale",
        "lemma:rh-upf",
        "lemma:rh-relevance-def",
        "theorem:gap-scale-agreement",
        "theorem:two-routes-one-guarantee",
        "theorem:queue-declared",
    ],
    "total_seam_facts": _TOTAL_SEAM_FACTS,
    # P2 — the frozen domain sequences (letters: L lesson teach,
    # U pre-lesson gap / impossible, F part-set failure, T
    # derive-success, S derived, H honest wall). FROZEN FROM
    # CONTROL #1.
    "domain_sequence": {
        2: "UUULSLSSSHLSSSLSSSSFSSHSS",  # control #1
        3: "SSSSSSSSSSSSHTSTSFSSHSSHSSSS",  # control #1
        4: "TSSSSSHSSSSSSSSSSSSSSSSSSHUSSSSS",  # control #1
    },
    # P8 — store totals (FROZEN FROM CONTROL #1; the mechanism's
    # own census is the referee, never the hand count).
    "final_total": 1296,  # control #1: 1200 (seed) + 7 facts + 89 events
    "new_facts": 7,  # frozen NOW: 4 lessons + 3 compositions
    "new_events": 89,  # control #1 (the D-e6y family at the S12 rung: re-probes at carried seed coordinates upsert silently; the NEW S12 coordinates drill)
    # P7 — mastery (frozen from control #1): the 4 NEW concepts at
    # band-end + the carried concepts that moved at the NEW S12
    # coordinates (the D-e6y family at the S12 rung: re-probes at
    # carried seed coordinates upsert silently, +0).
    "mastery_expected": {
        "conditional": {"correct": 1, "state": "practicing"},  # control #1
        "rh-scale": {"correct": 23, "state": "practicing"},  # control #1
        "factor-route": {"correct": 10, "state": "practicing"},  # control #1
        "rh-relevance": {"correct": 15, "state": "practicing"},  # control #1
    },
    "expected_prereq_gaps": {
        "conditional": ["riemann"],  # control #1
        "rh-scale": ["conditional", "pnt-error"],  # control #1
        "factor-route": ["rh-scale"],  # control #1
        "rh-relevance": ["factor-route", "rh-scale"],  # control #1
    },
    "pre_s12_states": _PRE_S12_STATES,
    "pre_s12_drilled": {
        "count-successor": 1,  # control #1 (S4:25 the line-end seam row)
        "first-divisor": 4,  # control #1 (S03:25/26 the part carries + S04:10 + S04:24 + S04:32)
        "li-criterion": 1,  # control #1 (S4:15 the S9 carry row)
        "lindelof": 1,  # control #1 (S4:22 the S9 carry row)
        "mod4-split": 1,  # control #1 (S04:18 the S5 carry row)
        "pnt-error": 1,  # control #1 (S04:16 the S9 carry row)
        "prime-count": 1,  # control #1 (S04:23 the pi-census seam row)
        "prime-split": 1,  # control #1 (S04:17 the S5 carry row)
        "riemann": 2,  # control #1 (S02:25 the conj-status seam row + S04:14 the rh-reach row)
        "scan-ledger": 1,  # control #1 (S04:09 the ledger-growth state)
        "zero-density": 1,  # control #1 (S04:20 the S9 carry row)
        "zero-free": 1,  # control #1 (S04:19 the S9 carry row)
    },
    # P6 — the SEAM carry rows (the NINETEEN rows byte-identical to
    # the seed store's answers — verified against a seed-only
    # runtime in P6) and the two OFF-SCRIPT carry probes (the
    # SAVANT-TRACK standing check).
    "seam_carry_refs": (
        "S02:25",
        "S03:25",
        "S03:26",
        "S04:09",
        "S04:10",
        "S04:11",
        "S04:14",
        "S04:15",
        "S04:16",
        "S04:17",
        "S04:18",
        "S04:19",
        "S04:20",
        "S04:21",
        "S04:22",
        "S04:23",
        "S04:24",
        "S04:25",
        "S04:32",
    ),
    "offscript_carry": {
        "what is the status of the erdosguess?": E611_ANSWER["CONJ_FALSIFIED"],
        "state the kstbound rule": _ST4["kstbound"],
    },
    # P5 — the S12-specific SEMANTIC seam (frozen expectation:
    # AGREEMENT): (a) the two-routes destination — the mechanism's
    # own spf-chain walk classifies EVERY n in 2..84 with parts all
    # prime and product n (the mechanism-vs-python cross-check);
    # (b) the queue grounding — every fact id the declared queue
    # lots name EXISTS in the final store (the neighbor facts are
    # the seed's declared layer).
    "seam_crosscheck": {
        "expected": "agreement",
        "two_routes_range": (2, 84),
        "queue_referenced_ids": (
            "conjecture:riemann",
            "lemma:rh-bound-scale",
            "lemma:rh-upf",
            "curriculum:pnt-ap",
            "curriculum:tower-primes",
            "curriculum:mod4-split",
            "curriculum:chebotarev",
            "lemma:mod4minusone",
            "lemma:primesplit",
            "lemma:apbound",
            "lemma:chebotarev-selection",
            "lemma:rv-count",
            "lemma:ledger-growth",
            "theorem:spf-chain",
        ),
    },
}

FROZEN["script"] = {
    2: [
        "what does the condition give for the error of the prime count?",
        "what is the queue above my line?",
        "what does the condition give for the prime parts of a number?",
        _st12("conditional-def"),
        "state the conditional-def rule",
        _st12("rh-bound-scale"),
        "state the rh-bound-scale rule",
        "what does the condition give for the error of the prime count?",
        "what does the condition give for the gaps between primes?",
        "what does the condition give for the zero count at height T?",
        _st12("rh-upf"),
        "state the rh-upf rule",
        "what does the condition give for the prime parts of a number?",
        "is the prime-parts uniqueness established without the condition?",
        _st12("rh-relevance-def"),
        "state the rh-relevance-def rule",
        "the lots of this band condition-closing, which?",
        "the lots of this band condition-neighboring, which?",
        "the lots of this band open even under the condition, which?",
        "derive queue-declared from rh-relevance-def",
        "the gap after 2 on my line, what is it?",
        "the gap after 23 on my line, what is it?",
        "the gap after 83 on my line, what is it?",
        "the gap on my line, greatest, what is it?",
        "what is the status of the riemann hypothesis?",
    ],
    3: [
        "the gap after 3 on my line, what is it?",
        "the gap after 7 on my line, what is it?",
        "the gap after 31 on my line, what is it?",
        "the gap after 73 on my line, what is it?",
        "the gaps of size 6 on my line, how many?",
        "the gaps on my line, how many?",
        "does the bare scale at 2 on my line cover the gap?",
        "does the bare scale at 3 on my line cover the gap?",
        "does the bare scale at 5 on my line cover the gap?",
        "does the bare scale at 29 on my line cover the gap?",
        "does the bare scale at 61 on my line cover the gap?",
        "the gaps on my line covered by the bare scale, how many?",
        "the greatest gap of the whole prime line, what is it?",
        "derive gap-scale-agreement from rh-bound-scale and ledger-growth and spf-chain",
        "does my line agree with the conditional root scale?",
        "derive two-routes-one-guarantee from rh-upf and spf-chain",
        "how do the two roads to prime-parts uniqueness differ?",
        "derive two-routes-one-guarantee from rh-upf",
        "which road to prime-parts uniqueness carries without the condition?",
        "which road asks for the condition?",
        "does the condition road carry the guarantee without the condition?",
        "the factor-count deviation ledger on my line, greatest absolute, what is it?",
        "is the factor-count deviation ledger of my line below the root of my line end?",
        "the factor-count deviation ledger past my line end, below the root smallness, is it?",
        "what are the prime parts of 84?",
        "what are the prime parts of 60?",
        "does my line carry the mod-4 split of the primes?",
        "the primes one mod four on my line, how many?",
    ],
    4: [
        "derive queue-declared from rh-relevance-def and rh-bound-scale and rh-upf",
        "what is the queue above my line?",
        "the queue above my line, first lot, which?",
        "the queue above my line, second lot, which?",
        "the queue above my line, third lot, which?",
        "the queue above my line, fourth lot, which?",
        "the queue above my line, fifth lot, which?",
        "the primes three mod four on my line, how many?",
        "state the ledger-growth rule",
        "state the spf-chain rule",
        "state the sieve-equality rule",
        "what does the condition give for the error of the prime count?",
        "does my line agree with the conditional root scale?",
        "state the rh-reach rule",
        "state the li-criterion rule",
        "state the pnt-error rule",
        "state the primesplit rule",
        "state the mod4minusone rule",
        "state the zero-free-region rule",
        "state the zero-density rule",
        "state the chebotarev-selection rule",
        "state the lindelof rule",
        "how many primes are at most 84?",
        "is 83 a prime?",
        "what comes after 83?",
        "what does the condition give for the zeros of the zeta function?",
        "prove the condition from its own lots?",
        "is the conjecture closed by any lot of this band?",
        "which scale does the theorem rh-reach demand?",
        "the factor-count deviation ledger at 31, what is it?",
        "the band at the line end, state?",
        "is 2 a prime?",
    ],
}

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

#: The Stage-A discipline (the S10 pattern): no S4–S11 seam
#: statement may appear IN the S12 script verbatim (the S12 script
#: re-asserts only its OWN four lessons; the carried corpus is
#: reproduced by PROBE, never by re-assertion).
for _phrase in (
    list(S4_LESSONS)
    + list(S5_LESSONS)
    + list(S6_LESSONS)
    + list(S7_LESSONS)
    + list(S8_LESSONS)
    + list(S9_LESSONS)
    + list(S11_LESSONS)
    + [m["statement"] for m in S10_THEOREMS.values()]
    + [m["statement"] for m in S11_THEOREMS.values()]
):
    if isinstance(_phrase, dict):
        continue
    assert not any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"an S12 script turn re-asserts a seam statement: {_phrase[:60]}..."
    )

#: The S12 beds cross-check (D-e6g): the mechanism's python-side
#: reference functions reproduce EVERY bed of section D, on-line
#: AND off-line (the off-line witness values name themselves in the
#: walls; W-S12-8 is the frozen reference wall for 0.98 / 1.90 /
#: 9.17 and W-S12-2 names 89). The pre-freeze referee the pre-reg
#: names: a hand/mechanism disagreement is a deviation BEFORE the
#: freeze, never an edit.
_END_ = 84
_GAPS_ = _s12_py_gaps(_END_)
_PRIMES_ = [p for p in range(2, _END_ + 1) if _s11_py_spf(p) == p]
_FAIL_ = [p for p, g in _GAPS_ if _s12_py_scale(p) < g]
_M84_ = _s12_py_M(_END_)


def _mu_from_chain(factors: list[int]) -> int:
    """mu from the spf chain (the D-e6g(b) cross-check: the
    mechanism's chain-side mu vs the python reference mu)."""

    cnt: dict[int, int] = {}
    for p in factors:
        cnt[p] = cnt.get(p, 0) + 1
    if any(c > 1 for c in cnt.values()):
        return 0
    return -1 if len(cnt) % 2 else 1


_BED_BUDGET = [
    ("gap_list", tuple(g for _p, g in _GAPS_) == tuple(S12_BEDS["gap_list"]) and len(_GAPS_) == S12_BEDS["gap_count"] == 22),
    (
        "gap_max",
        (max(g for _p, g in _GAPS_), next(p for p, g in _GAPS_ if g == 6)) == S12_BEDS["gap_max"] == (6, 23),
    ),
    (
        "gap6",
        tuple((p, p + g) for p, g in _GAPS_ if g == 6) == tuple(S12_BEDS["gap6_pairs"])
        == ((23, 29), (31, 37), (47, 53), (53, 59), (61, 67), (73, 79)),
    ),
    ("scale_fail", tuple(_FAIL_) == S12_BEDS["scale_fail"] == (2, 3)),
    ("scale_cover_count", (len(_GAPS_) - len(_FAIL_)) == S12_BEDS["scale_cover_count"] == 20),
    ("scale_wall_values", {str(p): round(_s12_py_scale(p), 2) for p in (2, 3)} == S12_BEDS["scale_wall_values"] == {"2": 0.98, "3": 1.90}),
    ("sqrt_line_end", round(_END_ ** 0.5, 2) == S12_BEDS["sqrt_line_end"] == 9.17),
    ("next_prime_past_83", _next_prime_after(83) == S12_BEDS["next_prime_past_83"] == 89),
    (
        "mod4",
        (tuple(p for p in _PRIMES_ if p % 4 == 1), tuple(p for p in _PRIMES_ if p % 4 == 3))
        == (S12_BEDS["mod4_1"], S12_BEDS["mod4_3"])
        == ((5, 13, 17, 29, 37, 41, 53, 61, 73), (3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83)),
    ),
    ("mu_ref", all(_s12_py_mu(n) == _mu_from_chain(list(_s11_py_chain(n))) for n in range(2, _END_ + 1))),
    (
        "M_ledger",
        all(_M84_[n] == v for n, v in S12_BEDS["mu_at"].items())
        and max(abs(v) for v in _M84_.values()) == S12_BEDS["mu_max_abs"] == 4
        and min(n for n in _M84_ if abs(_M84_[n]) == 4) == S12_BEDS["mu_first_at"] == 31
        and tuple(sorted(n for n in _M84_ if abs(_M84_[n]) == 4)) == S12_BEDS["mu_max_at"]
        and all(_M84_[n] < 0 for n in S12_BEDS["mu_max_at"])  # the max-abs places are all negative
        and _M84_[_END_] == -4,
    ),
]
assert all(ok for _name, ok in _BED_BUDGET), f"S12 beds failed the mechanism cross-check: {_BED_BUDGET}"

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict.
_UNFROZEN = (
    str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")
    or str(FROZEN["final_total"]).startswith("##FREEZE")
    or str(FROZEN["new_events"]).startswith("##FREEZE")
    or str(FROZEN["mastery_expected"]).startswith("##FREEZE")
    or str(FROZEN["expected_prereq_gaps"]).startswith("##FREEZE")
    or str(FROZEN["pre_s12_drilled"]).startswith("##FREEZE")
    or str(PARTSET_FAIL_S220).startswith("##FREEZE")
    or str(PARTSET_FAIL_S318).startswith("##FREEZE")
)


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


def _successor_objects(store) -> set[int]:
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
    """The per-turn domain (the e614 letter mapping): L lesson
    teach, U impossible (gap / prove / off-band), F part-set
    failure, T derive-success, S derived, H honest wall."""

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
    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E616)
    out: list[dict] = []
    for s in (2, 3, 4):
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
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
    pairs = []
    for a in store.query():
        pairs.append((a.id, json.dumps(a.to_dict(), sort_keys=True, default=str)))
    pairs.sort()
    return hashlib.sha256(json.dumps(pairs, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.16-run1"]:
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
        "compositions": {
            s: {"parts": tuple(S12_THEOREMS[s]["parts"]), "statement": S12_THEOREMS[s]["statement"]}
            for s in ("gap-scale-agreement", "two-routes-one-guarantee", "queue-declared")
        },
    }


def run_e6_16(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.15 S11 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S12 frozen constants are not yet frozen (control #1 must replace the ##FREEZE-S12## sentinels; see the E6.16 pre-reg open points)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.16-run1", "e6.16-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.15 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E616}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.16-run1", "e6.16-run2"):
        (out_dir / name / "e6.16-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.16.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.16-run1"
    root2 = out_dir / "e6.16-run2"
    final = _fresh_store(root1, 4)
    store2 = _fresh_store(root2, 4)
    total1 = len(final.query())
    total2 = len(store2.query())
    seed_total_check = _seed_check(root1)
    all_lessons = {
        **S4_LESSONS,
        **S5_LESSONS,
        **S6_LESSONS,
        **S7_LESSONS,
        **S8_LESSONS,
        **S9_LESSONS,
        **S11_LESSONS,
        **S12_LESSONS,
    }
    all_theorems = {
        **S6_THEOREMS,
        **S7_THEOREMS,
        **S8_THEOREMS,
        **S9_THEOREMS,
        **S10_THEOREMS,
        **S11_THEOREMS,
        **S12_THEOREMS,
    }

    # P0 — the HYPOTHESIS MARKER (the S12 band's discipline): every
    # new fact asserting a conditional lot's conclusion (lemma:rh-
    # bound-scale, lemma:rh-upf, theorem:two-routes-one-guarantee)
    # + the conditional-def lesson itself carries the condition's
    # text in its stored bytes (never dropped); PLUS the carried
    # denylist (S9_DENYLIST, UNCHANGED) — no unconditioned RH
    # corpus content may leak into the S12 script, any response,
    # any band lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker_facts = ("lemma:conditional-def", "lemma:rh-bound-scale", "lemma:rh-upf", "theorem:two-routes-one-guarantee")
    for fid in marker_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if not ("under the condition of the Riemann hypothesis" in obj or "under the condition that" in obj):
            p0_bad.append(f"P0: {fid} does not carry the condition's text in its stored bytes (the marker dropped)")
    deny = set(S9_DENYLIST)
    corpus: list[tuple[str, str]] = []
    for s in (2, 3, 4):
        for t in FROZEN["script"][s]:
            corpus.append((f"script:S{s:02d}", t))
    for k, t in turns.items():
        corpus.append((f"response:{k}", t["surface"]))
    for phrase in all_lessons.values():
        corpus.append(("lessons", phrase))
    for m in all_theorems.values():
        corpus.append(("theorems", m["statement"]))
    for where, text in corpus:
        for w in sorted(deny):
            if w and w in text:
                p0_bad.append(f"denylist hit: {w!r} in {where}: {text[:60]}...")
    checks["p0_marker_and_denylist"] = {
        "pass": not p0_bad,
        "bad": p0_bad[:20],
        "marker_facts": list(marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S12 script + all responses + band lessons (S4–S9 + S11 + S12) + all twenty-three theorem statements",
    }

    # P1 — the contract: 85 turns, every turn on the det arm and
    # contract-valid, the script identity, and the S2:01–03
    # impossible-runs BEFORE the teaches (the pre-lesson gaps come
    # first, then the four teach turns).
    p1_bad: list[str] = []
    if len(turns) != FROZEN["total_turns"]:
        p1_bad.append(f"{len(turns)} turns != {FROZEN['total_turns']}")
    for ref, t in turns.items():
        if not t["contract_valid"]:
            p1_bad.append(f"{ref}: contract invalid")
        if (t.get("arm") or {}).get("classifier") != "det":
            p1_bad.append(f"{ref}: not the det arm")
    if report["script_hash"] != SCRIPT_HASH:
        p1_bad.append("script identity mismatch")
    if [t["domain"] for k, t in sorted(turns.items()) if k.startswith("S02:")] [:3] != ["U", "U", "U"]:
        p1_bad.append("S2:01–03 do not run impossible BEFORE the teaches")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — the typed honesty: the THREE pre-lesson gaps, the FOUR
    # teach turns (lesson facts stored), the TWO part-set failures
    # (named, needs_info, ungrounded, store-inert), the THREE derive
    # successes (stored, grounded exactly on the sanctioned parts),
    # the frozen domain sequences, the line end, and ZERO seeded-
    # fact object bytes changed (the actual touch set of the seeded
    # facts = ∅). The S12 script has no re-derive turn.
    p2_bad: list[str] = []
    impossible = [k for k, t in turns.items() if t["kind"] == "impossible"]
    if sorted(impossible) != sorted(FROZEN["pre_teach_gaps"]) + ["S04:27"]:
        p2_bad.append(f"impossible turns {sorted(impossible)} != frozen {sorted(FROZEN['pre_teach_gaps'])} + the S4:27 prove wall")
    from kainos.tutor.brainstem import concept_map

    for ref, cid in sorted(FROZEN["pre_teach_gaps"].items()):
        ir = (turns.get(ref) or {}).get("response_ir") or {}
        want = f"not yet learned: {concept_map(cid).label}"
        if want not in str(ir.get("gap", "")):
            p2_bad.append(f"{ref}: the pre-lesson gap does not name {concept_map(cid).label!r}")
    for ref, fact_id in sorted(FROZEN["teach_turns"].items()):
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing teach {ref}")
            continue
        if t["kind"] != "assertion" or not (t["slots"] or {}).get("lemma"):
            p2_bad.append(f"{ref}: the teach turn is not a lesson assertion")
        if not t["memory_diff"]:
            p2_bad.append(f"{ref}: the teach turn stored nothing")
        try:
            final.get(fact_id)
        except KeyError:
            p2_bad.append(f"{ref}: the lesson fact {fact_id} is not in the final store")
    for ref, frozen in sorted(FROZEN["scaffold_failures"].items()):
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing scaffold failure {ref}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p2_bad.append(f"{ref}: the part-set failure is not needs_info ({ir.get('uncertainty_state')})")
        if frozen not in str(ir.get("answer", "")):
            p2_bad.append(f"{ref}: the frozen part-set articulation is missing (the missing part must be named)")
        if t["grounded"]:
            p2_bad.append(f"{ref}: a scaffold failure cited evidence (fabrication)")
        if t["memory_diff"]:
            p2_bad.append(f"{ref}: a scaffold failure wrote the store")
    for ref, (slug, prem_ids) in sorted(FROZEN["derive_successes"].items()):
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing derive {ref}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p2_bad.append(f"{ref}: the derive is not derived ({ir.get('uncertainty_state')})")
        if _ir_answer(t) != _th12(slug):
            p2_bad.append(f"{ref}: the derive answer is not the frozen {slug} statement")
        if not t["memory_diff"]:
            p2_bad.append(f"{ref}: the derive stored nothing")
        if set(map(str, t["grounded"])) != prem_ids:
            p2_bad.append(f"{ref}: the derive grounded premises {t['grounded']} != exactly the sanctioned parts {sorted(prem_ids)}")
    if FROZEN["rederive"] is not None:
        p2_bad.append("the S12 script frozen no re-derive turn (rederive must be None)")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        if str(s).startswith("##FREEZE"):
            continue
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S12 keeps the line ZERO successor facts unchanged)")
    seed_path = _resolve_seed()
    seed_store = load_store(seed_path)
    drift: list[str] = []
    for a in seed_store.query():
        try:
            b = final.get(a.id)
        except KeyError:
            drift.append(f"seed fact {a.id} missing from the final store")
            continue
        if a.object != b.object:
            drift.append(f"seed fact {a.id}: the object bytes changed (re-teaching detected)")
    if drift:
        p2_bad.extend(drift[:10])
    checks["p2_typed_honesty_interleave"] = {
        "pass": not p2_bad,
        "bad": p2_bad,
        "seed_drift_checked": len(list(seed_store.query())),
    }

    # P3 — the SEAM: ALL carried lesson + S12 lesson statements
    # byte-unchanged (the store->table direction, D-e6k(e)), the
    # TWENTY-THREE theorem facts exactly the sanctioned DAG (ALL
    # infant-derived, byte-exact statements and parts — the three
    # S12 composition facts NEW), the total seam census 95, the
    # derived table byte-exact, the conj STILL `open`.
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
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p3_bad.append(f"{ref}: not a grounded derivation ({ir.get('uncertainty_state')})")
    for sl, phrase in all_lessons.items():
        try:
            a = final.get(f"lemma:{sl}")
        except KeyError:
            continue
        if a.object != phrase:
            p3_bad.append(f"lemma:{sl}: the stored lesson statement drifted (re-teaching detected)")
    for a in final.query():
        if not (a.id and a.id.startswith("lemma:")):
            continue
        sl = a.id[len("lemma:") :]
        want = next((ph for ph, (_c, s2, _k, _es, _d, _l) in all_lessons.items() if s2 == sl), None)
        if want is None or a.object != want:
            p3_bad.append(f"lemma:{sl}: a store lemma fact is not a byte-canonical table entry")
    for slug, meta in sorted(all_theorems.items()):
        try:
            a = final.get(f"theorem:{slug}")
        except KeyError:
            p3_bad.append(f"theorem:{slug}: the theorem fact is not in the final store")
            continue
        if isinstance(a.object, str) and a.object != meta["statement"]:
            p3_bad.append(f"theorem:{slug}: the stored theorem statement drifted")
        if a.provenance is None or a.provenance.observer != "infant" or a.provenance.derived is not True:
            p3_bad.append(f"theorem:{slug}: the theorem fact is not an infant derivation")
        got_parts = tuple((a.context.data.get("derived_from") or ()) if a.context else ())
        if got_parts != tuple(meta["parts"]):
            p3_bad.append(f"theorem:{slug}: derived_from {got_parts} != sanctioned {tuple(meta['parts'])}")
    th_facts = [a for a in final.query() if a.id and a.id.startswith("theorem:")]
    seam_facts = [a for a in final.query() if a.id and a.id.startswith("lemma:")]
    if len(th_facts) + len(seam_facts) != FROZEN["total_seam_facts"]:
        p3_bad.append(f"total seam-family facts {len(th_facts) + len(seam_facts)} != frozen {FROZEN['total_seam_facts']}")
    try:
        conj = final.get("conjecture:riemann")
    except KeyError:
        conj = None
    if conj is None:
        p3_bad.append("conjecture:riemann: not in the final store")
    elif conj.context.data.get("conjecture_status") != "open":
        p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S12 must not flip)")
    checks["p3_seam_and_theorems"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_lessons": len(seam_facts),
        "seam_theorems": len(th_facts),
        "total_seam_facts": len(seam_facts) + len(th_facts),
    }

    # P4 — the beds exact + grounded (the ON-LINE census answers),
    # the walls honest with their frozen bytes and articulations
    # (the OFF-LINE instances name the value AND the line end, the
    # D-e6z(b) pattern), and the FROZEN reference wall W-S12-8
    # cross-checked against the mechanism's python reference (the
    # witness values 0.98 / 1.90 / 9.17 / 89 — never surfaced as an
    # answer, verified here).
    p4_bad: list[str] = []
    for ref, expected in sorted(FROZEN["beds_exact"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing bed {ref}")
            continue
        ans = _ir_answer(t)
        if ans != expected:
            p4_bad.append(f"{ref}: bed answer {ans!r} != {expected!r}")
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p4_bad.append(f"{ref}: the bed is not a grounded derivation ({ir.get('uncertainty_state')})")
        if not t["grounded"]:
            p4_bad.append(f"{ref}: the bed cited nothing (no line grounding)")
    for ref, expected in sorted(FROZEN["walls_honest"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing wall {ref}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the wall is not an honest needs_info ({ir.get('uncertainty_state')})")
        if str(ir.get("answer", "")) != expected:
            p4_bad.append(f"{ref}: the wall bytes {ir.get('answer')!r} != frozen")
        for art in FROZEN["wall_articulations"].get(ref, ()):
            if art not in str(ir.get("answer", "")):
                p4_bad.append(f"{ref}: the frozen articulation fragment {art!r} is missing")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited grounded premises (fabrication)")
    # the reference walls: W-S12-8 names 0.98 / 1.90 / 9.17 (the
    # ledger's greatest absolute 4 sits under the root 9.17),
    # W-S12-2 names 89 — the witness values are the mechanism's own
    # numbers, cross-checked now; each wall names the line end.
    refwall_ok = (
        round(_s12_py_scale(2), 2) == 0.98
        and round(_s12_py_scale(3), 2) == 1.90
        and round(84**0.5, 2) == 9.17
        and max(abs(v) for v in _s12_py_M(84).values()) == 4
        and _next_prime_after(83) == 89
    )
    if not refwall_ok:
        p4_bad.append("the frozen witness values drifted from the mechanism's python reference")
    for w in ("0.98", "1.90", "9.17", "line end 84"):
        if w not in W_S12_8:
            p4_bad.append(f"W-S12-8: the witness value {w} is not named in the reference wall")
    for w in ("89", "line end 84"):
        if w not in W_S12_2:
            p4_bad.append(f"W-S12-2: the witness value {w} is not named in the wall")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_wall": "W-S12-8 (cross-checked, never surfaced)",
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant (carried): NO fact id the conditional lots use as a
    # proof-cite (the conj id) may appear in a grounded list (S12
    # has no conj-teach turn); NO `theorem:riemann` assertion exists
    # in the final store (if this list is non-empty: STOP, human
    # review, full evidence, never a threshold loosening); the conj
    # fact byte-identical to the seed (open, declared-source); the
    # bed owners; the theorem allow-set; and the S12-specific
    # SEMANTIC seam (the AGREEMENT: (a) the two-routes destination —
    # the mechanism's own spf-chain walk classifies EVERY n in
    # 2..84 with parts all prime and product n (mechanism vs python
    # product reference); (b) the queue grounding — every fact id
    # the declared queue lots name exists in the final store).
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S12 has no conj-teach turn)")
    riemann_th = [a.id for a in final.query() if a.id.startswith("theorem:riemann")]
    if riemann_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {riemann_th} — the sanctioned corpus now produces theorem:riemann")
    seed_conj = seed_store.get("conjecture:riemann")
    live_conj = conj
    if (
        live_conj is None
        or (live_conj.context.data.get("conjecture_status") != "open")
        or (live_conj.object != seed_conj.object)
        or (live_conj.context.data.get("source_role") != "declared-source")
    ):
        p5_bad.append("conjecture:riemann: not byte-identical to the seed (open, declared-source)")
    for ref, owner in sorted(FROZEN["bed_owners"].items()):
        t = turns.get(ref)
        if t is None:
            p5_bad.append(f"missing bed {ref}")
            continue
        owners = {owner}
        gs = list(map(str, t["grounded"]))
        for g in gs:
            if not (g.startswith(("cs-", "count-successor")) or g in owners):
                p5_bad.append(f"{ref}: the bed cited a non-line fact {g} (allowed: line facts + the owning seam facts)")
        if owner not in gs:
            p5_bad.append(f"{ref}: the bed did not cite its owning seam fact")
    for ref, t in sorted(turns.items()):
        allowed = set(FROZEN["theorem_allowed"].get(ref, ()))
        for g in map(str, t["grounded"]):
            if not g.startswith("theorem:"):
                continue
            slug = g.split(":", 1)[1]
            if slug not in allowed:
                p5_bad.append(f"{ref}: theorem {slug} cited in grounded premises not on the allow-set")
    # (a) the two-routes destination (mechanism vs mechanism): a
    # scratch runtime on the FINAL S12 store re-runs the S11 parts
    # census for every n in 2..84 (the seed has no S12 lessons, so
    # the walk must run where they live) — parts all prime (the
    # mechanism's own grounded scan) and product n (the python
    # product reference). A drift is a tier-2 breakthrough
    # candidate (PENDING owner) — recorded, never fixed here.
    seam_candidate: list[str] = []
    seam_root = out_dir / "e6.16-seam"
    seam_root.mkdir(parents=True, exist_ok=True)
    (seam_root / "codeX-S01.json").write_bytes((out_dir / "e6.16-run1" / "codeX-S04.json").read_bytes())
    srt = InfantRuntime(seam_root, concepts=CONCEPTS_E616)
    srt.boot(2)
    n_low, n_high = FROZEN["seam_crosscheck"]["two_routes_range"]
    two_routes_bad: list[str] = []
    for n in range(n_low, n_high + 1):
        sr = srt.turn(f"what are the prime parts of {n}?")
        sir = sr.response_ir or {}
        if sir.get("uncertainty_state") != "derived":
            two_routes_bad.append(f"{n}: the parts walk did not derive ({sir.get('uncertainty_state')})")
            continue
        ans = str(sir.get("answer", ""))
        if ans.startswith(f"{n} is prime"):
            parts = [n]
        else:
            parts = [int(x) for x in ans.split(", ")]
        if any(_s11_py_spf(p) != p for p in parts):
            two_routes_bad.append(f"{n}: a part {parts} is not prime (python reference)")
            continue
        prod = 1
        for p in parts:
            prod *= p
        if prod != n:
            two_routes_bad.append(f"{n}: the product of the parts is {prod}, not {n}")
    for b in two_routes_bad:
        seam_candidate.append(f"TWO-ROUTES destination: {b} — TIER-2 breakthrough candidate (PENDING owner)")
    spr = srt.turn("how many primes are at most 84?")
    s_pi = str((spr.response_ir or {}).get("answer"))
    srt.lapse()
    if s_pi != "23":
        p5_bad.append(f"the S8 pi-census on the S12 store answered {s_pi!r}, not 23 — TIER-2 breakthrough candidate")
    # (b) the queue grounding: every fact id the declared queue
    # lots name exists in the final store (the neighbor facts are
    # the seed's declared layer; the condition lot names the S12
    # condition facts).
    queue_missing = []
    for fid in FROZEN["seam_crosscheck"]["queue_referenced_ids"]:
        try:
            final.get(fid)
        except KeyError:
            queue_missing.append(fid)
    if queue_missing:
        p5_bad.append(f"the queue names fact ids absent from the final store: {queue_missing}")
    checks["p5_conjecture_discovery_seam"] = {
        "pass": not p5_bad,
        "bad": p5_bad,
        "conj_grounded_refs": conj_grounded,
        "discovery_candidate_riemann_theorem_facts": riemann_th,
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "two_routes_range": list(FROZEN["seam_crosscheck"]["two_routes_range"]),
            "two_routes_bad": two_routes_bad[:10],
            "two_routes_agreement": not two_routes_bad,
            "s_pi_answer": s_pi,
            "queue_referenced_ids": list(FROZEN["seam_crosscheck"]["queue_referenced_ids"]),
            "queue_missing": queue_missing,
        },
        "seam_tier2_candidates": seam_candidate,
    }

    # P6 — the SEAM carry (the NINETEEN rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime)
    # + the two OFF-SCRIPT carry probes (erdosguess falsified,
    # kstbound byte-identical — the SAVANT-TRACK standing check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.16-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E616)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S12-run answer (the seam carry drifted)")
    for surface, expected in sorted(FROZEN["offscript_carry"].items()):
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if ir.get("answer") != expected:
            p6_bad.append(f"off-script carry {surface!r}: {ir.get('answer')!r} != the frozen bytes")
        elif ir.get("uncertainty_state") != "derived":
            p6_bad.append(f"off-script carry {surface!r}: not a grounded derivation")
    rt.lapse()
    checks["p6_seam_carry"] = {
        "pass": not p6_bad,
        "bad": p6_bad,
        "seam_carry_refs": list(FROZEN["seam_carry_refs"]),
        "offscript_carry": list(FROZEN["offscript_carry"]),
    }

    # P7 — the mastery census (the 84 seed concepts: NO
    # regressions — no stable->practicing/unknown; every carried
    # correct-derivation count equals its S11-final base + the
    # frozen drill at the NEW S12 coordinates, the D-e6y family at
    # the S12 rung; the four NEW concepts at their frozen band-end
    # values with their frozen prereq-gap sets).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E616])
    _S12_NEW = ["conditional", "rh-scale", "factor-route", "rh-relevance"]
    for cid in list(FROZEN["pre_s12_states"]) + _S12_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s12_drilled"] if isinstance(FROZEN["pre_s12_drilled"], dict) else {}
    for cid, exp in FROZEN["pre_s12_states"].items():
        v = mv.get(cid)
        if v is None:
            continue
        want = exp["correct"] + drilled.get(cid, 0)
        if v.state != exp["state"]:
            p7_bad.append(f"{cid}: pre-S12 state CHANGED ({v.state} != {exp['state']}) (no regressions)")
        if v.correct_derivations != want:
            p7_bad.append(f"{cid}: correct derivations {v.correct_derivations} != frozen {want} (base {exp['correct']} + drill {drilled.get(cid, 0)})")
    for cid, e in FROZEN["mastery_expected"].items():
        v = mv.get(cid)
        if v is None:
            p7_bad.append(f"{cid}: the mastery-expected concept left the view")
            continue
        if v.state != e["state"]:
            p7_bad.append(f"{cid}: state {v.state} != {e['state']}")
        if v.correct_derivations != e["correct"]:
            p7_bad.append(f"{cid}: {v.correct_derivations} correct != {e['correct']}")
        if tuple(v.prereq_gaps) != tuple(FROZEN["expected_prereq_gaps"].get(cid, ())):
            p7_bad.append(f"{cid}: prereq gaps {list(v.prereq_gaps)} != frozen {list(FROZEN['expected_prereq_gaps'].get(cid, ()))}")
    checks["p7_mastery"] = {
        "pass": not p7_bad,
        "bad": p7_bad,
        "carried_refs": len(FROZEN["pre_s12_states"]),
        "drilled": drilled,
        "expected": {k: FROZEN["mastery_expected"][k] for k in sorted(FROZEN["mastery_expected"])},
    }

    # P8 — the store totals, the seed identity, the line census,
    # the SEVEN new facts, the determinism twin, the run/store
    # identities.
    p8_bad: list[str] = []
    succ1 = _successor_objects(final)
    if seed_total_check["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed_total_check['seed_total']} != {FROZEN['seed_total']}")
    if _store_identity(seed_store) != FROZEN["seed_identity"]:
        p8_bad.append(f"seed identity {_store_identity(seed_store)} != frozen {FROZEN['seed_identity']}")
    if seed_total_check["reproduced_in_s2_pre"] != FROZEN["seed_total"]:
        p8_bad.append("the seed did not reproduce byte-for-byte in the S2 pre-store")
    if seed_total_check["missing"]:
        p8_bad.append(f"missing seed facts: {seed_total_check['missing'][:6]}...")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']}")
    if succ1 != set(range(1, FROZEN["line_end_final"] + 1)):
        p8_bad.append("the successor objects are not exactly 1..84 (a census wrote off-line)")
    if total1 != int(FROZEN["final_total"]):
        p8_bad.append(f"final total {total1} != frozen {FROZEN['final_total']}")
    if total2 != total1:
        p8_bad.append(f"run2 total {total2} != run1 total {total1}")
    if total1 - FROZEN["seed_total"] != int(FROZEN["new_facts"]) + int(FROZEN["new_events"]):
        p8_bad.append(
            f"delta {total1 - FROZEN['seed_total']} != new_facts ({FROZEN['new_facts']}) + new_events ({FROZEN['new_events']})"
        )
    for fid in FROZEN["new_fact_ids"]:
        try:
            final.get(fid)
        except KeyError:
            p8_bad.append(f"new fact {fid} is not in the final store")
    if runs["e6.16-run1"] != runs["e6.16-run2"]:
        p8_bad.append("the determinism twin failed: run1 != run2 (byte-identity)")
    if _store_identity(final) != _store_identity(store2):
        p8_bad.append("the determinism twin failed: store1 identity != store2 identity")
    checks["p8_store_total_line_mastery"] = {
        "pass": not p8_bad,
        "bad": p8_bad,
        "value": {
            "seed_total": seed_total_check["seed_total"],
            "reproduced_in_s2_pre": seed_total_check["reproduced_in_s2_pre"],
            "line_end": _line_end(final),
            "line_successors": sorted(succ1),
            "final_total": total1,
            "new_facts": int(FROZEN["new_facts"]),
            "new_events": int(FROZEN["new_events"]),
            "determinism_twin": runs["e6.16-run1"] == runs["e6.16-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.16-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s12_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_16Experiment:
    """E6.16 — S12 of the FUNDAMENTALS-TRACK: the RH neighborhood
    (the conditional layer: the root scale, the root smallness, the
    two roads, the declared queue)."""

    name = "e6.16"
    hypothesis = (
        "S12 of the FUNDAMENTALS-TRACK walks the RH NEIGHBORHOOD: the hypothesis marker "
        "never drops (every conditional fact carries the condition's text), the on-line "
        "gap census (22 gaps, the six gaps of 6, the bare root scale failing at exactly "
        "2 and 3) and the factor-count deviation census (greatest absolute 4, first at "
        "31) answer grounded from cited walks, every off-line witness value (0.98, 1.90, "
        "9.17, 89) appears ONLY in value-named walls that name the value and the 0..84 "
        "line end — the D-e6z(b) pattern. It stores SEVEN new deterministic facts: four "
        "declared lessons (conditional-def, rh-bound-scale, rh-upf, rh-relevance-def) "
        "and three compositions (gap-scale-agreement, two-routes-one-guarantee, "
        "queue-declared), all infant-derived with the strict part sets, the seam census "
        "closing 68+20 -> 72+23 = 95. The condition buys nothing at the destination: the "
        "scan road is unconditional, the condition road the different road, and the two "
        "reach the same prime-parts uniqueness (the store's own articulation). The "
        "queue declares its four lots in declared order — the condition line first — "
        "with no fifth; the line stays 0..84; the conj stays open, byte-identical to "
        "the seed; NO theorem:riemann exists (the discovery-candidate invariant); the "
        "S8/S9/S10/S11 carry survives (19 seam rows byte-identical to the seed store; "
        "the erdosguess still falsified, kstbound byte-identical); two runs "
        "byte-identical."
    )
    metric = "S12 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_16()
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
                Path("results/phase-6/e6.16-run1/session-S02.json"),
                Path("results/phase-6/e6.16-run1/session-S03.json"),
                Path("results/phase-6/e6.16-run1/session-S04.json"),
                Path("results/phase-6/e6.16-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
