# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.15 — S11 of the FUNDAMENTALS-TRACK (pre-registered, frozen):
the sieve (the full process + the scan ledger; THE BACKWARD LAYER +
THE RECORDER).

The band-1 backward step from the S10 store frontier: the
DIVISIBILITY UNDER THE PRIMES — the furthest layer the owner's
2026-08-23 ruling digs for, plus the same day's scan-ledger
direction: "we don't want to do an optimization, we want to record
the points where we could say things like 'yeah, this is nth time
we've checked an even number for divisibility by 2'… the real
pattern is in how many integers did you hit before your last prime
(because the history grows by that factor)". Four new concepts
(divides, composite, first-divisor, scan-ledger — prereqs point
DOWN), four DECLARED seam lessons (divides-def, composite-def,
spf-def, ledger-growth), three sanctioned compositions
(first-divisor-prime, sieve-equality, spf-chain — owning concept
first-divisor, strict part sets), the full 85-turn labeled script
(S2:25 + S3:28 + S4:32), the ON-LINE / OFF-LINE split (values
above 84 appear ONLY in value-named walls, the S8 J(84)=1053
precedent, D-e6z(b)), the audit answerable from the store's own
ledger, and the SAVANT-TRACK carry probes (P6: erdosguess still
falsified, kstbound byte-identical — the owner's 2026-08-23
carry-over question, encoded as a standing check).

The pre-registration (frozen before code, 2026-08-23, D-e6f(a)
corrected) in `plan/30-phases/phase-6-tutor/experiments.md` (the
E6.15 section) carries the script, the beds (section D), the walls
(section B), and P0–P8.

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
    CONCEPT_S11,
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
    S11_BEDS,
    S11_LESSONS,
    S11_THEOREMS,
    _s11_py_cand_row,
    _s11_py_chain,
    _s11_py_comp_count,
    _s11_py_est_total,
    _s11_py_fd_count,
    _s11_py_kill_trials,
    _s11_py_prime_row,
    _s11_py_spf,
)
from kainos.tutor.e614 import (
    CONCEPTS_E614,
)
from kainos.tutor.e614 import (
    FROZEN as E614_FROZEN,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E615", "FROZEN", "E6_15Experiment", "run_e6_15"]

CHECKS = 9

#: S11 teaches: the divisibility layer (the four new concepts join
#: the carried registry; prereqs point DOWN only — the house
#: invariant).
CONCEPTS_E615: tuple = CONCEPTS_E614 + CONCEPT_S11

#: The official e6.14 S10 store (the S11 seed: 1101 assertions,
#: line 0..84, identity b68e23bae96eca13, 81 seam facts,
#: `riemann` open, `erdosguess` falsified), repo-relative.
E614_SEED = Path("results/phase-6/e6.14-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E614_SEED.exists():
        return E614_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E614_SEED
    return alt if alt.exists() else E614_SEED


_ST4 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S4_LESSONS.items()}
_ST8 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S8_LESSONS.items()}
_ST11 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S11_LESSONS.items()}
_TH11 = {s: m["statement"] for s, m in S11_THEOREMS.items()}

E611_ANSWER = _e611_mod._ANSWER_
E612_ANSWER = _e612_mod._ANSWER_


def _st11(slug: str) -> str:
    return _ST11[slug]


def _th11(slug: str) -> str:
    return _TH11[slug]


def _whychain11(slug: str) -> str:
    """The WHY-SPLIT (the S8 pattern): a derived theorem's proof IS
    in the store — the articulation cites the sanctioned parts."""

    return f"i derived it from {', '.join(S11_THEOREMS[slug]['parts'])}: {_TH11[slug]}"


#: The AUDIT string (byte-frozen, D-e6f(a) corrected: the owner's
#: own question, answerable from the store's own ledger; it cites
#: ONLY on-line ledger rows — the grand totals 923/340/583 live in
#: the walls and the beds, never as a store answer).
AUDIT = (
    "no, in the marks — and yes, in the ledger: both sieves mark the same 60 composites "
    "from 2 to 84 — every composite's first divisor is prime, so a composite candidate can "
    "never win the scan first; what the full ledger keeps that the prime scan throws away "
    "is exactly the composite-candidate tests — candidate 4: 27 tests, 0 hits; candidate 6: "
    "22 tests, 0 hits; the composite candidates 8 through 82 keep theirs the same way — "
    "nothing more is kept, and there are no different marks"
)

#: The frozen per-instance walls (the D-e6f(a) wall family: each
#: off-line instance names the value AND the 0..84 line end; the
#: value-named aggregates name the mechanism's own number).
W_S11_1 = (
    "i begin the census at two: 1 is neither prime nor composite — 1 divides every number, "
    "and no k above 1 and below 1 can exist"
)
W_S11_3_7 = (
    "7 has no first divisor below itself: no k above 1 and below 7 divides 7 — it is prime, "
    "and first divisors belong to the composites"
)
W_S11_5_1000 = (
    "1000 is off my line — i sieve where the line runs: to 84; the method does not stop "
    "there, but my census does"
)
W_S11_6 = "zero is not on my line — i begin my line at one, so i cannot test a division of zero"
W_S11_7_84 = "84 is composite — 2 is its first divisor: the establishing scan belongs to the primes"


def _wall_offline(n: int, verb: str) -> str:
    return f"{n} is off my 0..84 line — i cannot {verb} what my line does not reach"


#: P2 — the deviant part-set failures (the shared strict branch;
#: the mechanism's own output, frozen from control #1, written
#: once, read back — the missing part is NAMED).
PARTSET_FAIL_S309 = (
    "i can see the parts you name, but the rule for sieve-equality wants its exact set — "
    "what you name is short the first-divisor-prime before i can put it together"
)  # control #1: the shared strict branch's own bytes
PARTSET_FAIL_S402 = (
    "i can see the parts you name, but the rule for spf-chain wants its exact set — "
    "what you name is short the spf-def before i can put it together"
)  # control #1: the shared strict branch's own bytes


#: P3 — the seam census (pre-reg: 68 `lemma:` + 20 `theorem:` = 88;
#: 64 + 17 at seed + the four lessons + the three compositions).
_TOTAL_SEAM_FACTS = len(_ST11) + 3 + 81

#: P7 — the pre-S11 states (80 concepts): the S10-final census,
#: built from the e6.14 frozen tables — the mechanism's own data,
#: not a hand count.
_PRE_S11_STATES: dict[str, dict] = {}
for _cid, _base in E614_FROZEN["pre_s10_states"].items():
    _PRE_S11_STATES[_cid] = {
        "state": _base["state"],
        "correct": _base["correct"] + E614_FROZEN["pre_s10_drilled"].get(_cid, 0),
    }
for _cid, _v in E614_FROZEN["mastery_expected"].items():
    _PRE_S11_STATES[_cid] = {"state": _v["state"], "correct": _v["correct"]}

#: The full sanctioned composition DAG (S6's six + S7's six +
#: S8's two + S9's two + S10's one + S11's three = twenty).
_THEOREM_DAG = {
    **{s: tuple(m["parts"]) for s, m in S6_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S7_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S8_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S9_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S10_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S11_THEOREMS.items()},
}

FROZEN: dict[str, Any] = {
    # P8 — the seed (the official e6.14 S10 final store).
    "seed": str(E614_SEED),
    "seed_total": 1101,
    "seed_identity": "b68e23bae96eca13",
    "total_turns": 85,
    "line_end_final": 84,  # the line STAYS 0..84 (owner settled; zero new successor facts)
    # P2 — the typed honesty turns.
    "pre_teach_gaps": {
        "S02:01": "divides",
        "S02:02": "composite",
        "S02:03": "first-divisor",
    },
    "teach_turns": {
        "S02:04": "lemma:divides-def",
        "S02:05": "lemma:composite-def",
        "S02:06": "lemma:spf-def",
        "S03:17": "lemma:ledger-growth",
    },
    "scaffold_failures": {
        "S03:09": PARTSET_FAIL_S309,
        "S04:02": PARTSET_FAIL_S402,
    },
    "derive_successes": {
        "S03:07": ("first-divisor-prime", {"lemma:composite-def", "lemma:spf-def"}),
        "S03:08": ("sieve-equality", {"theorem:first-divisor-prime", "lemma:divides-def"}),
        "S04:01": ("spf-chain", {"theorem:sieve-equality", "lemma:spf-def", "lemma:divides-def"}),
    },
    "rederive": ("S03:27", "sieve-equality"),
    # P4 — the beds exact (the ON-LINE census answers, grounded).
    "beds_exact": {
        "S03:01": "5",
        "S03:02": "60",
        "S03:03": "41",
        "S03:04": "13",
        "S03:05": "4",
        "S03:06": "2",
        "S03:12": "6",
        "S03:13": "6",
        "S03:14": "21",
        "S03:15": "20",
        "S03:18": "41",
        "S03:19": "82",
        "S03:20": "40",
        "S03:21": "21",
        "S03:22": "2",
        "S03:23": "27",
        "S03:24": "22",
        "S03:25": "22",
        "S03:28": "5",
        "S04:03": "2, 2, 3, 5",
        "S04:04": "2, 2, 3, 7",
        "S04:05": "7, 7",
        "S04:06": "7, 11",
        "S04:07": "2, 2, 2, 3, 3",
        "S04:08": "3, 3, 3, 3",
        "S04:09": "83 is prime — its only part is itself",
        "S04:11": "no — 7 is its first divisor: 49 is 7 times 7",
        "S04:12": "no — 2 is its first divisor: 82 is 2 times 41",
        "S04:13": "yes — the scan finds no divisor above 1 below 79",
        "S04:14": "no — 3 is its first divisor: 9 is 3 times 3",
        "S04:16": "22 primes and 59 integers",
        "S04:17": "4 primes and 5 integers",
        "S04:18": "2 primes and 1 integer",
        "S04:22": "23",
    },
    "bed_owners": {
        "S03:01": "lemma:composite-def",
        "S03:02": "lemma:composite-def",
        "S03:03": "lemma:spf-def",
        "S03:04": "lemma:spf-def",
        "S03:05": "lemma:spf-def",
        "S03:06": "lemma:spf-def",
        "S03:12": "lemma:spf-def",
        "S03:13": "lemma:spf-def",
        "S03:14": "lemma:spf-def",
        "S03:15": "lemma:spf-def",
        "S03:18": "lemma:ledger-growth",
        "S03:19": "lemma:ledger-growth",
        "S03:20": "lemma:ledger-growth",
        "S03:21": "lemma:ledger-growth",
        "S03:22": "lemma:ledger-growth",
        "S03:23": "lemma:ledger-growth",
        "S03:24": "lemma:ledger-growth",
        "S03:25": "lemma:ledger-growth",
        "S03:28": "lemma:spf-def",
        "S04:03": "theorem:spf-chain",
        "S04:04": "theorem:spf-chain",
        "S04:05": "theorem:spf-chain",
        "S04:06": "theorem:spf-chain",
        "S04:07": "theorem:spf-chain",
        "S04:08": "theorem:spf-chain",
        "S04:09": "theorem:spf-chain",
        "S04:11": "lemma:spf-def",
        "S04:12": "lemma:spf-def",
        "S04:13": "lemma:spf-def",
        "S04:14": "lemma:spf-def",
        "S04:16": "lemma:ledger-growth",
        "S04:17": "lemma:ledger-growth",
        "S04:18": "lemma:ledger-growth",
        "S04:22": "lemma:euler-product",
    },
    # P4 — the walls honest (byte-frozen full answers, "needs_info: "
    # prefixed in the ir per the e614 convention).
    "walls_honest": {
        "S02:15": "needs_info: " + _wall_offline(91, "test"),
        "S02:16": "needs_info: " + W_S11_1,
        "S02:22": "needs_info: " + W_S11_3_7,
        "S02:23": "needs_info: " + _wall_offline(90, "test"),
        "S02:24": "needs_info: " + _wall_offline(87, "test"),
        "S02:25": "needs_info: " + W_S11_6,
        "S03:10": (
            "needs_info: the full sieve's kill trials over the composites up to 84 are 95 — "
            "past my line which ends at 84: a census like that is a value, not a number i can hold"
        ),
        "S03:11": (
            "needs_info: the prime sieve's kill trials over the composites up to 84 are 87 — "
            "past my line which ends at 84: a census like that is a value, not a number i can hold"
        ),
        "S03:26": "needs_info: " + _wall_offline(200, "count"),
        "S04:10": "needs_info: " + _wall_offline(85, "strip"),
        "S04:15": "needs_info: " + _wall_offline(97, "test"),
        "S04:19": (
            "needs_info: the sieve's establishing comparisons over the primes up to 84 are 828 — "
            "past my line which ends at 84: a census like that is a value, not a number i can hold"
        ),
        "S04:20": "needs_info: " + W_S11_7_84,
        "S04:27": "needs_info: " + W_S11_5_1000,
        "S04:28": "needs_info: " + _wall_offline(120, "test"),
        "S04:29": "needs_info: " + _wall_offline(121, "test"),
    },
    # P4 — the per-wall articulation fragments (frozen).
    "wall_articulations": {
        "S02:15": ("91", "off my 0..84 line"),
        "S02:16": ("i begin the census at two", "neither prime nor composite"),
        "S02:22": ("no first divisor below itself", "first divisors belong to the composites"),
        "S02:23": ("90",),
        "S02:24": ("87",),
        "S02:25": ("zero is not on my line",),
        "S03:10": ("95", "past my line which ends at 84"),
        "S03:11": ("87", "past my line which ends at 84"),
        "S03:26": ("200", "count"),
        "S04:10": ("85", "strip"),
        "S04:15": ("97",),
        "S04:19": ("828", "past my line which ends at 84"),
        "S04:20": ("84 is composite", "the establishing scan belongs to the primes"),
        "S04:27": ("1000", "to 84", "the method does not stop there"),
        "S04:28": ("120",),
        "S04:29": ("121",),
    },
    # P3 — the derived table (every non-wall ir.answer byte-exact;
    # the audit carries the D-e6f(a) string; the S4:22–26 and
    # S4:30 rows are the SEAM carry — byte-identical to the seed
    # store's answers, re-asserted against the seed in P6).
    "derived_table": {
        "S02:07": "yes — 21 is 3 times 7",
        "S02:08": "no — the walk by 4s reaches 20 with 1 left over: 21 is not 4 times any number on my line",
        "S02:09": "yes — 81 is 9 times 9",
        "S02:10": "no — 7 is above 6: one copy already overshoots",
        "S02:11": "yes — 1 divides every number",
        "S02:12": "yes — 7 times 7 is 49",
        "S02:13": "yes — 2 times 6 is 12",
        "S02:14": "no — the scan finds no divisor above 1 below 2: it is prime",
        "S02:17": "yes — 2 times 41 is 82",
        "S02:18": "2",
        "S02:19": "7",
        "S02:20": "7",
        "S02:21": "3",
        "S03:01": "5",
        "S03:02": "60",
        "S03:03": "41",
        "S03:04": "13",
        "S03:05": "4",
        "S03:06": "2",
        "S03:07": _th11("first-divisor-prime"),
        "S03:08": _th11("sieve-equality"),
        "S03:12": "6",
        "S03:13": "6",
        "S03:14": "21",
        "S03:15": "20",
        "S03:16": AUDIT,
        "S03:18": "41",
        "S03:19": "82",
        "S03:20": "40",
        "S03:21": "21",
        "S03:22": "2",
        "S03:23": "27",
        "S03:24": "22",
        "S03:25": "22",
        "S03:27": _th11("sieve-equality"),  # the re-derive: ir.answer = the stored statement
        "S03:28": "5",
        "S04:01": _th11("spf-chain"),
        "S04:03": "2, 2, 3, 5",
        "S04:04": "2, 2, 3, 7",
        "S04:05": "7, 7",
        "S04:06": "7, 11",
        "S04:07": "2, 2, 2, 3, 3",
        "S04:08": "3, 3, 3, 3",
        "S04:09": "83 is prime — its only part is itself",
        "S04:11": "no — 7 is its first divisor: 49 is 7 times 7",
        "S04:12": "no — 2 is its first divisor: 82 is 2 times 41",
        "S04:13": "yes — the scan finds no divisor above 1 below 79",
        "S04:14": "no — 3 is its first divisor: 9 is 3 times 3",
        "S04:16": "22 primes and 59 integers",
        "S04:17": "4 primes and 5 integers",
        "S04:18": "2 primes and 1 integer",
        "S04:21": _whychain11("first-divisor-prime"),
        "S04:22": "23",
        "S04:23": E612_ANSWER["NUMZERO"],
        "S04:24": E612_ANSWER["CONJ_OPEN"],
        "S04:25": S10_THEOREMS["rh-reach"]["statement"],
        "S04:26": _ST8["euler-product"],
        "S04:30": "84",
        "S04:31": AUDIT,
        "S04:32": "yes — 2 is the first prime: there is no k above 1 below it",
    },
    # P5 — the theorem ids may appear in `grounded` ONLY on the
    # frozen allow-set refs.
    "theorem_allowed": {
        "S03:08": ("first-divisor-prime",),
        "S03:16": ("sieve-equality",),  # the audit cites exactly [theorem:sieve-equality] + the census trace
        "S03:27": ("first-divisor-prime",),
        "S04:01": ("sieve-equality",),
        "S04:03": ("spf-chain",),
        "S04:04": ("spf-chain",),
        "S04:05": ("spf-chain",),
        "S04:06": ("spf-chain",),
        "S04:07": ("spf-chain",),
        "S04:08": ("spf-chain",),
        "S04:09": ("spf-chain",),
        "S04:25": ("rh-reach",),
        "S04:31": ("sieve-equality",),
    },
    # P7 — the full sanctioned DAG (twenty theorems).
    "theorem_dag": _THEOREM_DAG,
    "new_fact_ids": [
        "lemma:divides-def",
        "lemma:composite-def",
        "lemma:spf-def",
        "lemma:ledger-growth",
        "theorem:first-divisor-prime",
        "theorem:sieve-equality",
        "theorem:spf-chain",
    ],
    "total_seam_facts": _TOTAL_SEAM_FACTS,
    # P2 — the frozen domain sequences (letters: L lesson teach,
    # U pre-lesson gap, F part-set failure, T derive-success /
    # re-derive (+0), S derived, H honest wall). FROZEN FROM CONTROL
    # #1 (the mechanism's own turn-level census, never the hand).
    "domain_sequence": {
        2: "UUULLLSSSSSSSSHHSSSSSHHHH",  # control #1
        3: "SSSSSSTTFHHSSSSSLSSSSSSSSHTS",  # control #1
        4: "TFSSSSSSSHSSSSHSSSHHSSSSSSHHHSSS",  # control #1
    },
    # P8 — store totals (FROZEN FROM CONTROL #1; the mechanism's
    # own census is the referee, never the hand count).
    "final_total": 1200,  # control #1: 1101 (seed) + 7 facts + 92 events
    "new_facts": 7,  # frozen NOW: 4 lessons + 3 compositions
    "new_events": 92,  # control #1 (the D-e6y family at the S11 rung: re-probes at carried seed coordinates upsert silently; the NEW S11 coordinates drill)
    # P7 — mastery (frozen from control #1): the 4 NEW concepts at
    # band-end + the carried concepts that moved at the NEW S11
    # coordinates (the D-e6y family at the S11 rung: re-probes at
    # carried seed coordinates upsert silently, +0).
    "mastery_expected": {
        "composite": {"correct": 6, "state": "stable"},  # control #1
        "divides": {"correct": 5, "state": "stable"},  # control #1
        "first-divisor": {"correct": 32, "state": "stable"},  # control #1
        "scan-ledger": {"correct": 11, "state": "stable"},  # control #1
    },
    "expected_prereq_gaps": {
        "composite": [],  # control #1
        "divides": [],  # control #1
        "first-divisor": [],  # control #1
        "scan-ledger": [],  # control #1
    },
    "pre_s11_states": _PRE_S11_STATES,
    "pre_s11_drilled": {
        "count-successor": 1,  # control #1 (S4:30 "what comes after 83?" — a NEW S11 coordinate)
        "prime-count": 1,  # control #1 (S4:22 the pi-census seam row)
        "riemann": 2,  # control #1 (S4:24 the conj-status seam row + the S4:25 rh-reach reprobe coordinate)
        "rv-count": 1,  # control #1 (S4:23 the num-zeros seam row)
        "zeta-series": 1,  # control #1 (S4:26 the euler-product seam row)
    },
    # P6 — the SEAM carry rows (S4:22–26, S4:30 byte-identical to
    # the seed store's answers — verified against a seed-only
    # runtime in P6) and the two OFF-SCRIPT carry probes (the
    # SAVANT-TRACK carry: the owner's 2026-08-23 question, encoded
    # as a standing check).
    "seam_carry_refs": ("S04:22", "S04:23", "S04:24", "S04:25", "S04:26", "S04:30"),
    "offscript_carry": {
        "what is the status of the erdosguess?": E611_ANSWER["CONJ_FALSIFIED"],
        "state the kstbound rule": _ST4["kstbound"],
    },
    # P5 — the S11-specific SEMANTIC seam (frozen expectation:
    # AGREEMENT): the S11 lower layer's first-divisor prime test
    # over 2..84 classifies EXACTLY the S8 π-census prime set
    # (both 23). A mismatch is not an error to fix — it is a tier-2
    # breakthrough candidate (the lower layer altered the upper
    # layer) → fundamentals-breakthroughs.md, PENDING the owner.
    "seam_crosscheck": {
        "expected": "agreement",
        "s8_pi_count": 23,
        "s11_prime_set_size": 23,
    },
    "script": {
        2: [
            "does 3 divide 21?",
            "is 49 composite?",
            "what is the first divisor of 12?",
            _st11("divides-def"),
            _st11("composite-def"),
            _st11("spf-def"),
            "does 3 divide 21?",
            "does 4 divide 21?",
            "does 9 divide 81?",
            "does 7 divide 6?",
            "does 1 divide 49?",
            "is 49 composite?",
            "is 12 composite?",
            "is 2 composite?",
            "is 91 composite?",
            "is 1 composite?",
            "is 82 composite?",
            "what is the first divisor of 12?",
            "what is the first divisor of 49?",
            "what is the first divisor of 77?",
            "what is the first divisor of 81?",
            "what is the first divisor of 7?",
            "does 3 divide 90?",
            "is 87 composite?",
            "does 3 divide 0?",
        ],
        3: [
            "how many composites are there up to 10?",
            "how many composites are there up to 84?",
            "how many composites up to 84 have first divisor 2?",
            "how many composites up to 84 have first divisor 3?",
            "how many composites up to 84 have first divisor 5?",
            "how many composites up to 84 have first divisor 7?",
            "derive first-divisor-prime from composite-def and spf-def",
            "derive sieve-equality from first-divisor-prime and divides-def",
            "derive sieve-equality from divides-def",
            "how many trials does the full sieve spend on the composites up to 84?",
            "how many trials does the prime sieve spend on the composites up to 84?",
            "how many trials does the full sieve spend on the composites up to 10?",
            "how many trials does the prime sieve spend on the composites up to 10?",
            "how many trials does the full sieve spend on the composites up to 25?",
            "how many trials does the prime sieve spend on the composites up to 25?",
            "does the full sieve keep anything the prime sieve throws away?",
            _st11("ledger-growth"),
            "how many times does the full sieve check an even number for divisibility by 2?",
            "how many times does the full sieve test the candidate 2 up to 84?",
            "how many times does the full sieve test the candidate 3 up to 84?",
            "how many times does the full sieve test the candidate 7 up to 84?",
            "how many times does the full sieve hit the candidate 7 up to 84?",
            "how many times does the full sieve miss the candidate 4 up to 84?",
            "how many times does the full sieve miss the candidate 5 up to 84?",
            "how many times does the full sieve miss the candidate 6 up to 84?",
            "how many composites are there up to 200?",
            "derive sieve-equality from first-divisor-prime and divides-def",
            "what is the first divisor of 25?",
        ],
        4: [
            "derive spf-chain from sieve-equality and spf-def and divides-def",
            "derive spf-chain from sieve-equality and divides-def",
            "what are the prime parts of 60?",
            "what are the prime parts of 84?",
            "what are the prime parts of 49?",
            "what are the prime parts of 77?",
            "what are the prime parts of 72?",
            "what are the prime parts of 81?",
            "what are the prime parts of 83?",
            "what are the prime parts of 85?",
            "is 49 a prime?",
            "is 82 a prime?",
            "is 79 a prime?",
            "is 9 a prime?",
            "is 97 a prime?",
            "for the prime 83, how many primes and how many integers did the sieve compare?",
            "for the prime 11, how many primes and how many integers did the sieve compare?",
            "for the prime 5, how many primes and how many integers did the sieve compare?",
            "how many comparisons did the sieve spend in total establishing the primes up to 84?",
            "for the prime 84, how many primes and how many integers did the sieve compare?",
            "what is the first-divisor-prime for",
            "how many primes are at most 84?",
            "what is the height of the first nontrivial zero?",
            "what is the status of the riemann hypothesis?",
            "state the rh-reach rule",
            "state the euler-product rule",
            "run the sieve up to 1000?",
            "what is the first divisor of 120?",
            "does 11 divide 121?",
            "what comes after 83?",
            "does the full sieve keep anything the prime sieve throws away?",
            "is 2 a prime?",
        ],
    },
}


SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]


#: The Stage-A discipline (the S10 pattern): no S4–S10 seam
#: statement may appear IN the S11 script verbatim (the S11 script
#: re-asserts only its OWN four lessons; the carried corpus is
#: reproduced by PROBE, never by re-assertion).
for _phrase in list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS) + list(S8_LESSONS) + list(S9_LESSONS) + list(S10_THEOREMS.values()):
    if isinstance(_phrase, dict):
        continue
    assert not any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"an S11 script turn re-asserts a seam statement: {_phrase[:60]}..."
    )

#: The S11 beds cross-check (D-e6f(a)): the mechanism's python-side
#: reference functions reproduce EVERY bed of section D, on-line AND
#: off-line (the off-line values name themselves in the walls). This
#: is the pre-freeze referee the pre-reg names: a hand/mechanism
#: disagreement is a deviation BEFORE the freeze, never an edit.
_PRIMES_84 = [p for p in range(2, 85) if _s11_py_spf(p) == p]
_BED_BUDGET = [
    ("comp_count_10", _s11_py_comp_count(10) == S11_BEDS["comp_count"][10] == 5),
    ("comp_count_84", _s11_py_comp_count(84) == S11_BEDS["comp_count"][84] == 60),
    ("fd_count_84", all(_s11_py_fd_count(84, d) == c for d, c in S11_BEDS["fd_count_84"].items())),
    ("primes_84", len(_PRIMES_84) == S11_BEDS["primes_84"] == 23 and sum(_PRIMES_84) == 874),
    ("kill_full", all(_s11_py_kill_trials(n, False) == v for n, v in S11_BEDS["kill_trials_full"].items())),
    ("kill_prime", all(_s11_py_kill_trials(n, True) == v for n, v in S11_BEDS["kill_trials_prime"].items())),
    ("first_divergence", all(_s11_py_kill_trials(n, False) == _s11_py_kill_trials(n, True) for n in range(2, 25))
    and _s11_py_kill_trials(25, False) != _s11_py_kill_trials(25, True)),
    ("est_total", all(_s11_py_est_total(n) == v for n, v in S11_BEDS["est_total"].items())),
    ("cand_rows", all(_s11_py_cand_row(d, 84) == row for d, row in S11_BEDS["cand_rows_84"].items())),
    ("prime_rows", all(_s11_py_prime_row(p)[:2] == row for p, row in S11_BEDS["prime_rows"].items())),
    (
        "prime_row_sums",
        (sum(_s11_py_prime_row(p)[0] for p in _PRIMES_84), sum(_s11_py_prime_row(p)[1] for p in _PRIMES_84))
        == S11_BEDS["prime_row_sums"]
        == (253, 575),
    ),
    ("whole_process", S11_BEDS["whole_process_84"] == (923, 340, 583)),
    (
        "audit_rows",
        S11_BEDS["audit_rows"]
        == (
            _s11_py_comp_count(84),
            _s11_py_cand_row(2, 84)[1],
            _s11_py_cand_row(4, 84)[0],
            _s11_py_cand_row(4, 84)[1],
            _s11_py_cand_row(6, 84)[0],
            _s11_py_cand_row(6, 84)[1],
        )
        == (60, 41, 27, 0, 22, 0),
    ),
    ("chains", all(tuple(_s11_py_chain(n)) == row for n, row in S11_BEDS["chains"].items())),
]
assert all(ok for _name, ok in _BED_BUDGET), f"S11 beds failed the mechanism cross-check: {_BED_BUDGET}"

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict.
_UNFROZEN = (
    str(FROZEN["domain_sequence"].get(2, "")).startswith("##FREEZE")
    or str(FROZEN["domain_sequence"].get(3, "")).startswith("##FREEZE")
    or str(FROZEN["domain_sequence"].get(4, "")).startswith("##FREEZE")
    or str(FROZEN["final_total"]).startswith("##FREEZE")
    or str(FROZEN["new_events"]).startswith("##FREEZE")
    or str(FROZEN["mastery_expected"]).startswith("##FREEZE")
    or str(FROZEN["expected_prereq_gaps"]).startswith("##FREEZE")
    or str(FROZEN["pre_s11_drilled"]).startswith("##FREEZE")
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
    teach, U pre-lesson gap, F part-set failure, T derive-success /
    re-derive (+0), S derived, H honest wall."""

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
    rt = InfantRuntime(root, concepts=CONCEPTS_E615)
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
    for srow in runs["e6.15-run1"]:
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
            s: {"parts": tuple(S11_THEOREMS[s]["parts"]), "statement": S11_THEOREMS[s]["statement"]}
            for s in ("first-divisor-prime", "sieve-equality", "spf-chain")
        },
    }


def run_e6_15(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.14 S10 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S11 frozen constants are not yet frozen (control #1 must replace the ##FREEZE## sentinels; see the E6.15 pre-reg open points)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.15-run1", "e6.15-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.14 seed store is missing: {seed}"}
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E615}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.15-run1", "e6.15-run2"):
        (out_dir / name / "e6.15-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.15.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.15-run1"
    root2 = out_dir / "e6.15-run2"
    final = _fresh_store(root1, 4)
    store2 = _fresh_store(root2, 4)
    total1 = len(final.query())
    total2 = len(store2.query())
    seed_total_check = _seed_check(root1)
    all_lessons = {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS, **S9_LESSONS, **S11_LESSONS}
    all_theorems = {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS, **S11_THEOREMS}

    # P0 — the denylist: S9_DENYLIST (the 44, UNCHANGED) — no
    # savant/RH corpus content may appear in the S11 script, in any
    # response, in any band lesson, or in any theorem statement
    # (the S11 band teaches the divisibility layer; its surface is
    # the S2/S3/S4 probe script, no monograph content).
    p0_bad: list[str] = []
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
    checks["p0_denylist"] = {
        "pass": not p0_bad,
        "bad": p0_bad[:20],
        "denylist_size": len(deny),
        "checked_corpora": "S11 script + all responses + band lessons (S4–S9 + S11) + all twenty theorem statements",
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
    # the ONE re-derive (+0, the stored statement), the frozen
    # domain sequences, the line end, and ZERO seeded-fact object
    # bytes changed (the actual touch set of the seeded facts = ∅).
    p2_bad: list[str] = []
    impossible = [k for k, t in turns.items() if t["kind"] == "impossible"]
    if sorted(impossible) != sorted(FROZEN["pre_teach_gaps"]):
        p2_bad.append(f"impossible turns {sorted(impossible)} != frozen {sorted(FROZEN['pre_teach_gaps'])}")
    from kainos.tutor.brainstem import concept_map

    for ref, cid in sorted(FROZEN["pre_teach_gaps"].items()):
        ir = (turns.get(ref) or {}).get("response_ir") or {}
        # the gap names the concept's LABEL (the honest unlearned form).
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
        if _ir_answer(t) != _th11(slug):
            p2_bad.append(f"{ref}: the derive answer is not the frozen {slug} statement")
        if not t["memory_diff"]:
            p2_bad.append(f"{ref}: the derive stored nothing")
        if set(map(str, t["grounded"])) != prem_ids:
            p2_bad.append(f"{ref}: the derive grounded premises {t['grounded']} != exactly the sanctioned parts {sorted(prem_ids)}")
    rref, rslug = FROZEN["rederive"]
    rt = turns.get(rref)
    if rt is None:
        p2_bad.append(f"missing re-derive {rref}")
    else:
        if _ir_answer(rt) != _th11(rslug):
            p2_bad.append(f"{rref}: the re-derive answer is not the stored {rslug} statement")
        if not str(rt.get("response_text", "")).startswith("already put together in my store: "):
            p2_bad.append(f"{rref}: the re-derive is not in its +0 form (already put together in my store)")
        if rt["memory_diff"]:
            p2_bad.append(f"{rref}: the re-derive wrote the store (it must be +0)")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S11 keeps the line ZERO successor facts unchanged)")
    # the seeded facts' objects are byte-unchanged (P2 pre-reg: the
    # actual touch set of the seeded facts = ∅).
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
    checks["p2_typed_honesty_interleave"] = {"pass": not p2_bad, "bad": p2_bad, "seed_drift_checked": len(list(seed_store.query()))}

    # P3 — the SEAM: ALL carried lesson + S11 lesson statements
    # byte-unchanged (the store->table direction, D-e6k(e)), the
    # TWENTY theorem facts exactly the sanctioned DAG (ALL
    # infant-derived, byte-exact statements and parts — the three
    # S11 composition facts NEW), the total seam census 88, the
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
        sl = a.id[len("lemma:"):]
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
        p3_bad.append(
            f"total seam-family facts {len(th_facts) + len(seam_facts)} != frozen {FROZEN['total_seam_facts']}"
        )
    try:
        conj = final.get("conjecture:riemann")
    except KeyError:
        conj = None
    if conj is None:
        p3_bad.append("conjecture:riemann: not in the final store")
    elif conj.context.data.get("conjecture_status") != "open":
        p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S11 must not flip)")
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
    # D-e6z(b) pattern).
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
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant (carried): no grounded list in the run carries the
    # conj id (S11 has no conj-teach turn); NO `theorem:riemann`
    # assertion exists in the final store (if this list is
    # non-empty: STOP, human review, full evidence, never a
    # threshold loosening); the conj fact byte-identical to the
    # seed (open, declared-source); the bed owners; the theorem
    # allow-set; and the S11-specific SEMANTIC seam (the AGREEMENT:
    # the lower layer's prime test classifies EXACTLY the S8
    # π-census set — a mismatch is a tier-2 breakthrough candidate,
    # NOT an error: it is recorded, never fixed).
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S11 has no conj-teach turn)")
    riemann_th = [a.id for a in final.query() if a.id.startswith("theorem:riemann")]
    if riemann_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {riemann_th} — the sanctioned corpus now produces theorem:riemann")
    seed_conj = seed_store.get("conjecture:riemann")
    live_conj = conj
    if live_conj is None or (live_conj.context.data.get("conjecture_status") != "open") or (live_conj.object != seed_conj.object) or (live_conj.context.data.get("source_role") != "declared-source"):
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
    # the SEMANTIC seam (mechanism vs mechanism): the S11 lower
    # layer's GROUNDed first-divisor prime test over 2..84 (a
    # scratch runtime on the FINAL S11 store — the seed store has no
    # S11 lessons, so the test must run where they live) vs the
    # GROUNDed S8 pi-census on the same store (AGREEMENT expected;
    # a mismatch is a tier-2 breakthrough candidate, PENDING owner —
    # recorded in the report, never fixed here).
    seam_s11 = {n for n in range(2, FROZEN["line_end_final"] + 1) if _s11_py_spf(n) == n}
    seam_expected_n = FROZEN["seam_crosscheck"]["s8_pi_count"]
    seam_candidate: list[str] = []
    seam_root = out_dir / "e6.15-seam"
    seam_root.mkdir(parents=True, exist_ok=True)
    (seam_root / "codeX-S01.json").write_bytes((out_dir / "e6.15-run1" / "codeX-S04.json").read_bytes())
    srt = InfantRuntime(seam_root, concepts=CONCEPTS_E615)
    srt.boot(2)
    grounded_yes: list[int] = []
    for n in range(2, FROZEN["line_end_final"] + 1):
        sr = srt.turn(f"is {n} a prime?")
        sir = sr.response_ir or {}
        if sir.get("uncertainty_state") == "derived" and str(sir.get("answer", "")).startswith("yes"):
            grounded_yes.append(n)
    spr = srt.turn("how many primes are at most 84?")
    s_pi = str((spr.response_ir or {}).get("answer"))
    srt.lapse()
    if s_pi != str(seam_expected_n):
        seam_candidate.append(f"the S8 pi-census on the S11 store answered {s_pi!r}, not {seam_expected_n} — TIER-2 breakthrough candidate (PENDING owner)")
    if len(grounded_yes) != seam_expected_n:
        seam_candidate.append(
            f"the S11 lower-layer prime test classified {len(grounded_yes)} primes, the S8 pi-census says {seam_expected_n} — TIER-2 breakthrough candidate (PENDING owner)"
        )
    if set(grounded_yes) != seam_s11:
        p5_bad.append(f"the grounded S11 prime set drifted from the mechanism's reference set: {sorted(set(grounded_yes) ^ seam_s11)[:6]}...")
    checks["p5_conjecture_discovery_seam"] = {
        "pass": not p5_bad,
        "bad": p5_bad,
        "conj_grounded_refs": conj_grounded,
        "discovery_candidate_riemann_theorem_facts": riemann_th,
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "s11_prime_set_size": len(grounded_yes),
            "s8_pi_count": seam_expected_n,
            "s_pi_answer": s_pi,
            "agreement": not seam_candidate,
        },
        "seam_tier2_candidates": seam_candidate,
    }

    # P6 — the SEAM carry (S4:22–26, S4:30 byte-identical to the
    # seed store's answers — verified against a SEED-ONLY
    # runtime) + the two OFF-SCRIPT carry probes (erdosguess
    # falsified, kstbound byte-identical — the SAVANT-TRACK carry
    # intact in the S11 store).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.15-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E615)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S11-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 80 seed concepts: NO
    # regressions — no stable->practicing/unknown; every carried
    # correct-derivation count equals its S10-final base + the
    # frozen drill at the NEW S11 coordinates, the D-e6y family at
    # the S11 rung; the four NEW concepts at their frozen
    # band-end values with their frozen prereq-gap sets).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E615])
    for cid in list(FROZEN["pre_s11_states"]) + ["divides", "composite", "first-divisor", "scan-ledger"]:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = dict(FROZEN["pre_s11_drilled"])
    for cid, exp in FROZEN["pre_s11_states"].items():
        v = mv.get(cid)
        if v is None:
            continue
        want = exp["correct"] + drilled.get(cid, 0)
        if v.state != exp["state"]:
            p7_bad.append(f"{cid}: pre-S11 state CHANGED ({v.state} != {exp['state']}) (no regressions)")
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
        "carried_refs": len(FROZEN["pre_s11_states"]),
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
    if runs["e6.15-run1"] != runs["e6.15-run2"]:
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
            "determinism_twin": runs["e6.15-run1"] == runs["e6.15-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.15-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s11_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


# ---------------------------------------------------------------------------
# harness registration
# ---------------------------------------------------------------------------


class E6_15Experiment:
    """E6.15 — S11 of the FUNDAMENTALS-TRACK: the sieve (the full
    process + the scan ledger; the backward divisibility layer +
    the recorder)."""

    name = "e6.15"
    hypothesis = (
        "S11 of the FUNDAMENTALS-TRACK digs the layer UNDER the primes: divisibility, "
        "composites, the first divisor, and the scan ledger — the full process RECORDED, "
        "never optimized. It stores SEVEN new deterministic facts: four declared lessons "
        "(divides-def, composite-def, spf-def, ledger-growth) and three compositions "
        "(first-divisor-prime, sieve-equality, spf-chain), all infant-derived with the "
        "strict part sets, the seam census closing 64+17 -> 68+20 = 88. Every census the "
        "line can hold (composites 60, spf census 41/13/4/2, kill trials 6/6/21/20, "
        "candidate rows 82/41/41, prime rows 22 primes vs 59 integers at 83) answers "
        "grounded from cited on-line walks; every census above the line (95, 87, 828, "
        "923, 340, 583) appears ONLY in value-named walls that name the value and the "
        "0..84 line end — the D-e6z(b) pattern. The audit (the owner's own question) "
        "answers from the store's own ledger: the two sieves mark the same 60 composites; "
        "the ledger keeps exactly the composite-candidate tests (candidate 4: 27/0, "
        "candidate 6: 22/0) and nothing more. The line stays 0..84; the conj stays "
        "open, byte-identical to the seed; NO theorem:riemann exists (the discovery-"
        "candidate invariant); the lower layer's prime test classifies EXACTLY the S8 "
        "pi-census set (23 = 23, the frozen AGREEMENT — a mismatch would be a tier-2 "
        "breakthrough candidate, never an error); the SAVANT-TRACK carry survives (the "
        "erdosguess still falsified by the tower, kstbound byte-identical); two runs "
        "byte-identical."
    )
    metric = "S11 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_15()
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
                Path("results/phase-6/e6.15-run1/session-S02.json"),
                Path("results/phase-6/e6.15-run1/session-S03.json"),
                Path("results/phase-6/e6.15-run1/session-S04.json"),
                Path("results/phase-6/e6.15-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
