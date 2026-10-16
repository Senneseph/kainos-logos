# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.14 — S10 of the RH-TRACK (pre-registered, frozen): the
attempt (band 3 of 3 — THE RH TEST PROPER).

The A-cluster of the frozen RH-TRACK pre-registration: NO new
teaching. The scaffolded attempt (the main route's typed
part-set failure + the maximal assembly derive), the FULL Stage
A of the S8 + S9 corpus reproduced byte-exact from the final
store, the deviant-route walls (the Li route, the S-of-T route —
each closed off by the store's own content: the route's open
direction IS the conjecture), the attempt wall in its S10 form
(full assembly + the exact missing ingredient — the square-root
improvement — + the conjecture still `open`), and the final
store census. The ONE new fact is the maximal assembly theorem
`rh-reach` (derived, infant provenance, parts exactly
(strip, mirror-region, criterion-gap)). The
DISCOVERY-CANDIDATE invariant (P5): no sanctioned composition
produces a `theorem:riemann`; if the store ever carried one, the
check FIRES — stop, human review, full evidence, never a
threshold loosening.

The pre-registration (frozen before code, 2026-08-23) in
`plan/30-phases/phase-6-tutor/experiments.md` (the E6.14
section) carries:
  * the 75-turn labeled script (S2/S3/S4: 25 + 20 + 30);
  * the assembly theorem + its byte-frozen statement;
  * the S10 attempt form (W-RH-6's third rung, grounded on
    theorem:rh-reach);
  * the deviant-route walls (W-S10-1, W-S10-2);
  * the P0 denylist (the S9 44 UNCHANGED);
  * P0–P8 (mastery + the determinism twin + the cross-check
    reusing the S8 36 shared ids).

No Ollama. No LLM. The mechanism speaks.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
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
)
from kainos.tutor.e612 import FROZEN as E612_FROZEN
from kainos.tutor.e613 import CONCEPTS_E613
from kainos.tutor.e613 import FROZEN as E613_FROZEN
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E614", "FROZEN", "E6_14Experiment", "run_e6_14"]

CHECKS = 9

#: S10 has NO new concepts (a measurement band) — the runtime
#: concept registry is the e6.13 registry as-is.
CONCEPTS_E614: tuple = CONCEPTS_E613

#: The official e6.13 S9 store (the S10 seed: 1037 assertions,
#: line end 84, identity 9b42f6649c4f30c5, sixteen theorems
#: derived, `riemann` open), repo-relative.
E613_SEED = Path("results/phase-6/e6.13-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E613_SEED.exists():
        return E613_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E613_SEED
    return alt if alt.exists() else E613_SEED


_ST8 = {
    _slug: _phrase
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S8_LESSONS.items()
}
_ST9 = {
    _slug: _phrase
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S9_LESSONS.items()
}
_TH8 = {s: m["statement"] for s, m in S8_THEOREMS.items()}
_TH9 = {s: m["statement"] for s, m in S9_THEOREMS.items()}


def _st10(slug: str) -> str:
    if slug in _ST8:
        return _ST8[slug]
    return _ST9[slug]


def _th10(slug: str) -> str:
    if slug in _TH8:
        return _TH8[slug]
    if slug in _TH9:
        return _TH9[slug]
    return S10_THEOREMS[slug]["statement"]


def _whychain(slug: str) -> str:
    for table in (S8_THEOREMS, S9_THEOREMS, S10_THEOREMS):
        if slug in table:
            return f"i derived it from {', '.join(table[slug]['parts'])}: {table[slug]['statement']}"
    raise KeyError(slug)  # pragma: no cover


#: The full sanctioned composition DAG (S6's six + S7's six +
#: S8's two + S9's two + S10's one = seventeen).
_THEOREM_DAG = {
    **{s: tuple(m["parts"]) for s, m in S6_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S7_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S8_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S9_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S10_THEOREMS.items()},
}

# the carried bed/wall strings (byte-carried from the e6.12 frozen
# tables — the single source of truth)
from kainos.tutor import e612 as _e612_mod

_ANSWER_ = {
    "CONJ_OPEN": E612_FROZEN["derived_table"]["S03:17"],
    "SINCYCLE": _e612_mod._ANSWER_["SINCYCLE"],
    "GROWTH": _e612_mod._ANSWER_["GROWTH"],
    "NUMZERO": _e612_mod._ANSWER_["NUMZERO"],
    "WALL_NUMCHECK": _e612_mod._ANSWER_["WALL_NUMCHECK"],
    "WALL_OFFZERO": _e612_mod._ANSWER_["WALL_OFFZERO"],
    "WALL_PNTCONF": _e612_mod._ANSWER_["WALL_PNTCONF"],
    "WALL_PRODCONF": _e612_mod._ANSWER_["WALL_PRODCONF"],
    "WALL_ZETAVAL": _e612_mod._ANSWER_["WALL_ZETAVAL"],
    "WALL_STIGHT": _e612_mod._ANSWER_["WALL_STIGHT"],
    "WALL_PI100": _e612_mod._ANSWER_["WALL_PI100"],
    "GAP_COMP": (
        "for every fixed c greater than zero and every epsilon below one-half, x times e to the minus c times the "
        "square root of log x eventually exceeds x to the one-half plus epsilon, and the ratio grows without bound — "
        "the threshold is not a number in my store, and the point where it crosses is not in my store"
    ),
    "LI_CHECK": (
        "the check up to n = ten to the fifth is a declared numerical fact in my store; past that is not in my store"
    ),
    "WALL_LICLOSE": (
        "no — li's positivity for all n is exactly what the criterion equates with the conjecture, and it is unproven "
        "in my store; the check up to n = ten to the fifth is a declared numerical fact, not a proof — the route ends "
        "where the conjecture begins"
    ),
    "WALL_STCLOSE": (
        "no — that the wiggle S of T is little-o of log T is exactly what the equivalence makes of the conjecture, "
        "and it is unproven in my store; i hold the equivalence, not the open direction — the route ends where the "
        "conjecture begins"
    ),
    "WALL_CVALUE": (
        "i have been taught some constant c greater than zero exists, not its value — the sharp constant is not in my "
        "store: the region holds for some c, and which c is the open numerical content"
    ),
    "WALL_LHCONF": (
        "no — the stored direction runs one way only: the riemann hypothesis implies lindelof; the reverse is not in "
        "my store — lindelof is a status surface i hold, and nothing in the store closes the gap"
    ),
    "WALL_PHCONF": (
        "no — the reformulation is a theorem (the conjecture as a spectral statement about a positive self-adjoint "
        "operator); the step that recovers the conjecture from the spectrum is an open program, not in my store"
    ),
    "WALL_ATTEMPT_S10": (
        "no — the conjecture is a status surface, never a part: my own store has told me the whole route. what i "
        "assembled from it: every nontrivial zero is inside the strip, between zero and one, and its mirror under the "
        "map s to 1 minus s; and the equivalence demands a scale on the prime shadow, x to the one-half plus epsilon, "
        "where the store's best error term sits, x times e to the minus c times the square root of log x — and their "
        "ratio grows without bound. no part of the store closes it: the square-root improvement is not a capability i "
        "have been taught — and it is the conjecture itself"
    ),
}

GAP_ARTICULATION = "not a capability i have been taught"

#: P4 — the per-wall articulations (frozen; the carried walls use
#: their frozen e6.12/e6.13 phrases, the deviant-route walls their
#: frozen S10 phrases).
WALL_ARTICULATIONS: dict[str, tuple[str, ...]] = {
    "S02:23": ("not a proof",),  # W-RH-1
    "S02:24": ("open question",),  # W-RH-2 (the s-tight bound)
    "S02:25": ("not count past my line", "100"),  # W-RH-7
    "S03:06": ("open program",),  # W-RH-11
    "S03:08": ("one way only",),  # W-RH-10
    "S03:10": ("not in my store",),  # W-RH-14
    "S04:19": ("not a proof", "the route ends where the conjecture begins"),  # W-S10-1 (deviant Li route)
    "S04:20": ("not the open direction", "the route ends where the conjecture begins"),  # W-S10-2 (deviant S-of-T route)
    "S04:21": ("not a proof",),  # W-RH-1 stability
    "S04:22": ("no proof that there is none",),  # W-RH-3
    "S04:23": ("the other way",),  # W-RH-4
    "S04:24": ("away from the critical strip",),  # W-RH-5
    "S04:25": ("not in my store",),  # W-RH-8
}

#: P4 — the per-wall articulation for the S10 typed part-set
#: failure (frozen from the mechanism's own output at control #1,
#: written once, read back: the missing part must be NAMED).
PARTSET_FAIL_ARTICULATION = (
        "needs_info: i can see the parts you name, but the rule for rh-reach wants its exact set — "
        "what you name is short the mirror-region before i can put it together"
    )  # control #1: the mechanism's own output (it names the mirror-region, the W-S6-2 family)

def _tower_state() -> str:
    for _phrase, (_c, _s, _k, _es, _d, _l) in S7_LESSONS.items():
        if _s == "tower-base":
            return _phrase
    raise KeyError("tower-base")  # pragma: no cover


#: The pre-S10 census (80 concepts): the 70 carried pre-S9
#: concepts at their S9-final values (base + the S9 drilled
#: deltas) + the 10 S9 concepts at their S9-final (measured)
#: values. Built from the e6.13 frozen tables — the mechanism's
#: own data.
_PRE_S10_STATES: dict[str, dict] = {}
for _cid, _base in E613_FROZEN["pre_s9_states"].items():
    _PRE_S10_STATES[_cid] = {
        "state": _base["state"],
        "correct": _base["correct"] + E613_FROZEN["pre_s9_drilled"].get(_cid, 0),
    }
for _cid, _v in E613_FROZEN["mastery_expected"].items():
    _PRE_S10_STATES[_cid] = {"state": _v["state"], "correct": _v["correct"]}

FROZEN: dict[str, Any] = {
    # P8 — the seed (the official e6.13 S9 final store).
    "seed": str(E613_SEED),
    "seed_total": 1037,
    "total_turns": 75,
    "line_end_final": 84,  # the line STAYS 0..84 (zero new successor facts)
    # P2 — the typed honesty turns (S10 has NO teaching: zero
    # pre-lesson gaps, the ONE part-set failure, the ONE derive).
    "pre_teach_gaps": {},
    "scaffold_failures": {
        "S03:18": "rh-reach: the requested part set is not the sanctioned set (short the mirror-region)",
    },
    "derive_successes": {
        "S03:19": "rh-reach",
    },
    # P2/P4 — the conj-state probes (evidence carries the conj id,
    # grounded EMPTY all run; S10 has NO conj-teach turn).
    "conj_status_open": ("S02:15", "S04:26", "S04:28"),
    "conj_evidence_refs": ("S02:15", "S04:26", "S04:28"),
    # P3 — the why-split refs (mechanical).
    "why_chains": {
        "S02:14": "strip",
        "S03:16": "mirror-region",
        "S04:11": "criterion-gap",
        "S04:12": "rh-reach",
    },
    "why_walls": {},  # the S10 script has no declared-lemma why-deep probes
    # P4 — the beds exact (the line censuses write no new assertions).
    "beds_exact": {
        "S02:16": "23",
        "S02:17": "35",
        "S02:18": _ANSWER_["SINCYCLE"],
        "S02:19": _ANSWER_["GROWTH"],
        "S02:20": _ANSWER_["NUMZERO"],
        "S02:21": _ANSWER_["GAP_COMP"],
        "S02:22": _ANSWER_["LI_CHECK"],
        "S04:13": "23",
        "S04:14": "71",
        "S04:15": _ANSWER_["SINCYCLE"],
        "S04:16": _ANSWER_["GROWTH"],
        "S04:17": _ANSWER_["GAP_COMP"],
        "S04:18": _ANSWER_["LI_CHECK"],
    },
    "bed_owners": {
        "S02:16": "lemma:euler-product",
        "S02:17": "lemma:euler-product",
        "S02:18": "lemma:trivial-zeros",
        "S02:19": "lemma:pnt",
        "S02:20": "lemma:num-zeros",
        "S02:21": "lemma:pnt-error",
        "S02:22": "lemma:li-criterion",
        "S04:13": "lemma:euler-product",
        "S04:14": "lemma:euler-product",
        "S04:15": "lemma:trivial-zeros",
        "S04:16": "lemma:pnt",
        "S04:17": "lemma:pnt-error",
        "S04:18": "lemma:li-criterion",
    },
    "walls_honest": {
        "S02:23": "the numerical-check wall (W-RH-1)",
        "S02:24": "the S of T tight bound (W-RH-2: open question)",
        "S02:25": "pi(100) off the line (W-RH-7; names 100 and 84)",
        "S03:06": "the polya-hilbert open program (W-RH-11)",
        "S03:08": "the lindelof directionality (W-RH-10: one stored direction)",
        "S03:10": "the c-value wall (W-RH-14: some c, not the value)",
        "S04:19": "the deviant Li route (W-S10-1: the route IS the conjecture)",
        "S04:20": "the deviant S-of-T route (W-S10-2: the route IS the conjecture)",
        "S04:21": "the numerical-check wall stability (W-RH-1)",
        "S04:22": "off-line zeros (W-RH-3: beyond store)",
        "S04:23": "the pnt-confusion (W-RH-4: directionality)",
        "S04:24": "the product-confusion (W-RH-5: scope)",
        "S04:25": "zeta at 3/4 (W-RH-8: no value tables)",
    },
    "attempt_turns": ("S03:20", "S04:27"),
    # P4/P6 — the band-end table (the S10 terminal measurement:
    # blind reprobes + beds + walls + the deviant routes + conj-
    # state + the attempt in its S10 form + the S7 continuity).
    "band_end_probes": {
        "S04:01": _st10("zeta-series"),
        "S04:02": _st10("pnt"),
        "S04:03": _st10("psi-eq"),
        "S04:04": _st10("li-criterion"),
        "S04:05": _st10("zero-free-region"),
        "S04:06": _st10("pnt-error"),
        "S04:07": _th10("strip"),
        "S04:08": _th10("mirror-region"),
        "S04:09": _th10("criterion-gap"),
        "S04:10": _th10("rh-reach"),
        "S04:11": _whychain("criterion-gap"),
        "S04:12": _whychain("rh-reach"),
        "S04:13": "23",
        "S04:14": "71",
        "S04:15": _ANSWER_["SINCYCLE"],
        "S04:16": _ANSWER_["GROWTH"],
        "S04:17": _ANSWER_["GAP_COMP"],
        "S04:18": _ANSWER_["LI_CHECK"],
        "S04:19": "needs_info: " + _ANSWER_["WALL_LICLOSE"],
        "S04:20": "needs_info: " + _ANSWER_["WALL_STCLOSE"],
        "S04:21": "needs_info: " + _ANSWER_["WALL_NUMCHECK"],
        "S04:22": "needs_info: " + _ANSWER_["WALL_OFFZERO"],
        "S04:23": "needs_info: " + _ANSWER_["WALL_PNTCONF"],
        "S04:24": "needs_info: " + _ANSWER_["WALL_PRODCONF"],
        "S04:25": "needs_info: " + _ANSWER_["WALL_ZETAVAL"],
        "S04:26": _ANSWER_["CONJ_OPEN"],
        "S04:27": "needs_info: " + _ANSWER_["WALL_ATTEMPT_S10"],
        "S04:28": _ANSWER_["CONJ_OPEN"],
        "S04:29": _tower_state(),
        "S04:30": S7_THEOREMS["theorem-main"]["statement"],
    },
    # P3 — the derived table (every state/why/bed/status answer
    # exact).
    "derived_table": {
        "S02:01": _st10("zeta-series"),
        "S02:02": _st10("euler-product"),
        "S02:03": _st10("zeta-cont"),
        "S02:04": _st10("func-eq"),
        "S02:05": _st10("trivial-zeros"),
        "S02:06": _st10("nozero-s1"),
        "S02:07": _st10("von-mangoldt"),
        "S02:08": _st10("pnt"),
        "S02:09": _st10("rv-count"),
        "S02:10": _st10("s-of-t"),
        "S02:11": _st10("num-zeros"),
        "S02:12": _th10("reflect"),
        "S02:13": _th10("strip"),
        "S02:14": _whychain("strip"),
        "S02:15": _ANSWER_["CONJ_OPEN"],
        "S02:16": "23",
        "S02:17": "35",
        "S02:18": _ANSWER_["SINCYCLE"],
        "S02:19": _ANSWER_["GROWTH"],
        "S02:20": _ANSWER_["NUMZERO"],
        "S02:21": _ANSWER_["GAP_COMP"],
        "S02:22": _ANSWER_["LI_CHECK"],
        "S03:01": _st10("psi-eq"),
        "S03:02": _st10("pi-eq"),
        "S03:03": _st10("st-eq"),
        "S03:04": _st10("li-criterion"),
        "S03:05": _st10("polya-hilbert"),
        "S03:07": _st10("lindelof"),
        "S03:09": _st10("zero-free-region"),
        "S03:11": _st10("pnt-error"),
        "S03:12": _st10("hardy"),
        "S03:13": _st10("mean-square"),
        "S03:14": _st10("zero-density"),
        "S03:15": _th10("mirror-region"),
        "S03:16": _whychain("mirror-region"),
        "S03:17": _th10("criterion-gap"),
        "S04:01": _st10("zeta-series"),
        "S04:02": _st10("pnt"),
        "S04:03": _st10("psi-eq"),
        "S04:04": _st10("li-criterion"),
        "S04:05": _st10("zero-free-region"),
        "S04:06": _st10("pnt-error"),
        "S04:07": _th10("strip"),
        "S04:08": _th10("mirror-region"),
        "S04:09": _th10("criterion-gap"),
        "S04:10": _th10("rh-reach"),
        "S04:11": _whychain("criterion-gap"),
        "S04:12": _whychain("rh-reach"),
        "S04:13": "23",
        "S04:14": "71",
        "S04:15": _ANSWER_["SINCYCLE"],
        "S04:16": _ANSWER_["GROWTH"],
        "S04:17": _ANSWER_["GAP_COMP"],
        "S04:18": _ANSWER_["LI_CHECK"],
        "S04:26": _ANSWER_["CONJ_OPEN"],
        "S04:28": _ANSWER_["CONJ_OPEN"],
        "S04:29": _tower_state(),
        "S04:30": S7_THEOREMS["theorem-main"]["statement"],
    },
    # P5 — the theorem ids may appear in `grounded` ONLY on the
    # frozen allow-set refs.
    "theorem_allowed": {
        "S02:12": ("reflect",),
        "S02:13": ("strip",),
        "S02:14": ("reflect",),
        "S03:15": ("mirror-region",),
        "S03:16": ("reflect",),
        "S03:17": ("criterion-gap",),
        "S03:19": ("strip", "mirror-region", "criterion-gap"),  # the assembly derive grounds on its three parts
        "S03:20": ("rh-reach",),
        "S04:07": ("strip",),
        "S04:08": ("mirror-region",),
        "S04:09": ("criterion-gap",),
        "S04:10": ("rh-reach",),
        "S04:11": ("criterion-gap",),
        "S04:12": ("strip", "mirror-region", "criterion-gap"),  # the assembly why chains cite the parts
        "S04:27": ("rh-reach",),
        "S04:30": ("theorem-main",),  # the S7 continuity reprobe
    },
    # P7 — the full sanctioned DAG (seventeen theorems).
    "theorem_dag": _THEOREM_DAG,
    # P7 — the one-line-two-beds cross-check at the S10 rung: the
    # pi-84 bed and the jfunc-12 bed share EXACTLY the frozen 36
    # ids (carried from the S8/S9 rungs — the determinism of the
    # carried grounding, measured at each rung).
    "bed_crosscheck": {
        "pi_ref": "S02:16",
        "jfunc_ref": "S02:17",
        "shared": list(E612_FROZEN["bed_crosscheck"]["shared"]),
    },
    "prereq_edges": [],  # S10 adds NO prereq edges (no new concepts)
    "new_fact_ids": ["theorem:rh-reach"],
    "total_seam_facts": 81,  # control #1 — the ACTUAL store census (lemma:+theorem: facts): 80 at seed + 1 (the assembly)
    # (the pre-reg narrative's "82 -> 83" is the D-e6k(e) hand-count continuation; the store speaks)
    # P2 — the frozen domain sequences (letters: L lesson,
    # U pre-lesson gap, F part-set failure, T derive-success,
    # S derived, H honest wall). Mechanically derived from the
    # labeled table, frozen from control #1, written once to
    # /tmp/rh-s10-domains.txt.
    "domain_sequence": {
        2: "SSSSSSSSSSSSSSSSSSSSSSHHH",        # control #1
        3: "SSSSSHSHSHSSSSSSSFTH",             # control #1 (the F: the typed part-set failure; the T: the assembly)
        4: "SSSSSSSSSSSSSSSSSSHHHHHHHSHSSS",   # control #1 (the 7 walls; the 2 attempt turns; the conj probes)
    },
    # P8 — store totals (FROZEN FROM CONTROL #1; the D-e6y-family
    # dedupes at the carried seed's coordinates; the ACTUAL total
    # freezes, never the hand count).
    "final_total": 1101,  # control #1: 1037 (seed) + 1 fact + 63 events
    "new_facts": 1,  # frozen NOW: the one assembly theorem
    "new_events": 63,  # control #1 (the D-e6y family at the S10 rung: the carried coordinates dedupe; the NEW S10 coordinates drill)
    # P8 — mastery (S10 has NO new concepts; the 80-concept census
    # carries EXACT except the frozen drilled deltas, control #1).
    "mastery_expected": {
        "psi-eq": {"state": "stable", "correct": 11},
        "li-criterion": {"state": "stable", "correct": 8},
        "pi-eq": {"state": "practicing", "correct": 3},
        "st-eq": {"state": "practicing", "correct": 3},
        "polya-hilbert": {"state": "practicing", "correct": 3},
        "lindelof": {"state": "practicing", "correct": 3},
        "zero-density": {"state": "practicing", "correct": 3},
        "hardy-line": {"state": "practicing", "correct": 5},
        "pnt-error": {"state": "practicing", "correct": 8},
        "zero-free": {"state": "practicing", "correct": 12},
    },  # control #1 — S10 adds NO new stables: the gates behind the S10 frontier (func-eq, critical-strip, rv-count) stay practicing
    "expected_prereq_gaps": {
        "psi-eq": (),
        "li-criterion": (),
        "pi-eq": (),
        "st-eq": ("s-of-t",),
        "polya-hilbert": ("critical-strip",),
        "lindelof": ("critical-strip", "rv-count"),
        "zero-density": ("rv-count", "zero-free"),
        "hardy-line": ("rv-count", "s-of-t"),
        "pnt-error": ("zero-free",),
        "zero-free": ("func-eq",),
    },  # control #1 (pi-eq's gate closed: prime-count went stable in S10 — its count crossed K on its stable prereq; pi-eq itself remains below K)
    # P8 — the pre-S10 states (the e6.13 final census: the 70
    # carried + the 10 S9 concepts at their S9-final values = the
    # 80 concepts — built NOW from the e6.13 frozen tables, the
    # mechanism's own data, not a hand count).
    "pre_s10_states": _PRE_S10_STATES,
    "pre_s10_drilled": {
        "critical-strip": 4,
        "func-eq": 3,
        "pnt": 4,
        "prime-count": 5,
        "riemann": 5,
        "rv-count": 3,  # the NUMZERO bed (S02:20, the D-e6k(d) fixed line) drills its concept at the NEW S10 coordinate
        "s-of-t": 1,
        "zeta-cont": 1,
        "zeta-series": 2,
        "psi-eq": 4,
        "li-criterion": 3,
        "pi-eq": 1,
        "st-eq": 1,
        "polya-hilbert": 1,
        "lindelof": 1,
        "zero-density": 1,
        "hardy-line": 2,
        "pnt-error": 3,
        "zero-free": 5,
    },  # control #1 — the NEW S10 coordinates (19 of the 80 concepts; the other 61 dedupe or stay at the S9-final value)
    "script": {
        2: [
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
            "what is the status of the riemann hypothesis?",
            "how many primes are at most 84?",
            "what is the prime-power phi count at 12?",
            "does the sine vanish at every integer multiple of pi from one to 84?",
            "what is the expected growth of the prime-power phi count?",
            "what is the height of the first nontrivial zero?",
            "what is the expected growth of the gap ratio?",
            "have li's numbers been verified positive up to a bound?",
            "does the numerical check of the first ten to the thirteenth zeros prove the conjecture?",
            "what is the tight bound for S of T?",
            "how many primes are at most 100?",
        ],
        3: [
            "state the psi-eq rule",
            "state the pi-eq rule",
            "state the st-eq rule",
            "state the li-criterion rule",
            "state the polya-hilbert rule",
            "does the polya-hilbert program prove the riemann hypothesis?",
            "state the lindelof rule",
            "does lindelof imply the riemann hypothesis?",
            "state the zero-free-region rule",
            "what is the exact value of c in the zero-free region?",
            "state the pnt-error rule",
            "state the hardy rule",
            "state the mean-square rule",
            "state the zero-density rule",
            "state the mirror-region rule",
            "explain why the mirror-region holds",
            "state the criterion-gap rule",
            "derive rh-reach from strip and criterion-gap",
            "derive rh-reach from strip, mirror-region and criterion-gap",
            "can you derive the riemann hypothesis from the store?",
        ],
        4: [
            "state the zeta-series rule",
            "state the pnt rule",
            "state the psi-eq rule",
            "state the li-criterion rule",
            "state the zero-free-region rule",
            "state the pnt-error rule",
            "state the strip rule",
            "state the mirror-region rule",
            "state the criterion-gap rule",
            "state the rh-reach rule",
            "explain why the criterion-gap holds",
            "explain why the rh-reach holds",
            "how many primes are at most 84?",
            "what is the prime-power phi count at 18?",
            "does the sine vanish at every integer multiple of pi from one to 84?",
            "what is the expected growth of the prime-power phi count?",
            "what is the expected growth of the gap ratio?",
            "have li's numbers been verified positive up to a bound?",
            "can you prove li's numbers are positive for all n from the store?",
            "can you prove the wiggle S of T is little-o of log T from the store?",
            "does the numerical check of the first ten to the thirteenth zeros prove the conjecture?",
            "what is the smallest zero off the critical line, if one exists?",
            "does the prime number theorem imply the riemann hypothesis?",
            "does the euler product alone settle the location of the zeros?",
            "what is the value of zeta at three quarters?",
            "what is the status of the riemann hypothesis?",
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

#: S10 has NO new teaching: NO S4–S9 seam statement may appear IN
#: the script verbatim (the script reproduces them by PROBE, never
#: by re-assertion — the Stage A discipline).
for _phrase in list(S4_LESSONS) + list(S7_LESSONS) + list(S8_LESSONS) + list(S9_LESSONS):
    assert not any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"an S10 script turn re-asserts a seam statement (S10 has NO teaching): {_phrase[:60]}..."
    )

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict.
_UNFROZEN = (
    (FROZEN["domain_sequence"].get(2) or "").startswith("##FREEZE")
    or (FROZEN["domain_sequence"].get(3) or "").startswith("##FREEZE")
    or (FROZEN["domain_sequence"].get(4) or "").startswith("##FREEZE")
    or str(FROZEN["final_total"]).startswith("##FREEZE")
    or str(FROZEN["new_events"]).startswith("##FREEZE")
    or str(FROZEN["mastery_expected"]).startswith("##FREEZE")
    or str(FROZEN["expected_prereq_gaps"]).startswith("##FREEZE")
    or str(FROZEN["pre_s10_drilled"]).startswith("##FREEZE")
    or PARTSET_FAIL_ARTICULATION.startswith("##FREEZE")
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
    """The per-turn domain (the S8 letter mapping): L lesson, U
    pre-lesson gap, F part-set failure, T derive-success, S
    derived, H honest wall."""

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
    rt = InfantRuntime(root, concepts=CONCEPTS_E614)
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
    for srow in runs["e6.14-run1"]:
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
        "assembly": {
            "statement": _th10("rh-reach"),
            "parts": tuple(S10_THEOREMS["rh-reach"]["parts"]),
        },
    }


def run_e6_14(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.13 S9 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {"error": "S10 frozen constants are not yet frozen (control #1 must replace the ##FREEZE## sentinels; see the E6.14 pre-reg open points)"}
    runs: dict[str, list[dict]] = {}
    for name in ("e6.14-run1", "e6.14-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.13 seed store is missing: {seed}"}
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E614}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.14-run1", "e6.14-run2"):
        (out_dir / name / "e6.14-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.14.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.14-run1"
    root2 = out_dir / "e6.14-run2"
    final = _fresh_store(root1, 4)
    store2 = _fresh_store(root2, 4)
    total1 = len(final.query())
    total2 = len(store2.query())
    seed_total_check = _seed_check(root1)
    all_lessons = {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS, **S9_LESSONS}
    all_theorems = {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS}

    # P0 — the denylist: no S2/S3/S7/S9 corpus content may appear in
    # the S10 script, in any response, in any band lesson, or in any
    # theorem statement (the S10 band adds NO teaching and ONE
    # derived theorem; its surface is the S2/S4 probe script).
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
        "checked_corpora": "S10 script + all responses + band lessons (S4–S9) + all seventeen theorem statements",
    }

    # P1 — the contract: 75 turns, every turn on the det arm and
    # contract-valid, the script identity.
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
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — the typed honesty: ZERO impossible turns (S10 has no
    # untaught probe: no pre-lesson gaps — the part-set failure and
    # everything else resolve as derived/needs_info), the ONE typed
    # part-set failure (named, needs_info, ungrounded, store-inert),
    # the ONE derive success (stored, grounded exactly on the three
    # parts), the conj-state probes (grounded EMPTY, evidence carries
    # the conj id), the frozen domain sequences, the line end.
    p2_bad: list[str] = []
    impossible = [k for k, t in turns.items() if t["kind"] == "impossible"]
    for ref in impossible:
        p2_bad.append(f"{ref}: an S10 turn is impossible (S10 teaches nothing — every probe resolves)")
    pf = turns.get("S03:18")
    if pf is None:
        p2_bad.append("S03:18: the typed part-set failure is missing")
    else:
        ir = pf["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p2_bad.append(f"S03:18: the part-set failure is not needs_info ({ir.get('uncertainty_state')})")
        if PARTSET_FAIL_ARTICULATION not in str(ir.get("answer", "")):
            p2_bad.append("S03:18: the frozen part-set articulation is missing (the missing part must be named)")
        if pf["grounded"]:
            p2_bad.append("S03:18: a scaffold failure cited evidence (fabrication)")
        if pf["memory_diff"]:
            p2_bad.append("S03:18: a scaffold failure wrote the store")
    ts = turns.get("S03:19")
    if ts is None:
        p2_bad.append("S03:19: the maximal assembly derive is missing")
    else:
        ir = ts["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p2_bad.append(f"S03:19: the assembly derive is not derived ({ir.get('uncertainty_state')})")
        if _ir_answer(ts) != _th10("rh-reach"):
            p2_bad.append("S03:19: the assembly statement is not the frozen rh-reach statement")
        if not ts["memory_diff"]:
            p2_bad.append("S03:19: the assembly derive stored nothing")
    if set(map(str, turns["S03:19"]["grounded"])) != {"theorem:strip", "theorem:mirror-region", "theorem:criterion-gap"}:
        p2_bad.append(f"S03:19: the assembly grounded premises {turns['S03:19']['grounded']} != exactly the sanctioned parts")
    for k in FROZEN["conj_status_open"]:
        t = turns.get(k)
        if t is None:
            p2_bad.append(f"missing {k}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p2_bad.append(f"{k}: the conj-state probe is not a derived fact ({ir.get('uncertainty_state')})")
        if _ir_answer(t) != _ANSWER_["CONJ_OPEN"]:
            p2_bad.append(f"{k}: the conj-state answer is not the byte-carried frozen phrase")
        if t["grounded"]:
            p2_bad.append(f"{k}: the conj-state probe cited grounded premises")
        if not any("conjecture:riemann" in str(x) for x in (ir.get("evidence") or [])):
            p2_bad.append(f"{k}: the conj-state probe lost its conjecture evidence")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S10 adds ZERO successor facts)")
    checks["p2_typed_honesty_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — the SEAM: ALL carried lesson statements byte-unchanged
    # (nothing re-teaches), the seventeen theorem facts exactly the
    # sanctioned DAG (ALL infant-derived, byte-exact statements and
    # parts — the rh-reach fact NEW, derived from exactly
    # (strip, mirror-region, criterion-gap)), the total seam fact
    # count, the conj STILL `open`.
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
    # the seam invariant (store -> table): every lemma: fact that
    # EXISTS in the final store carries its byte-canonical statement
    # from the frozen table (nothing re-teaches, nothing drifts).
    # The store->table direction is the honest one: the falsified
    # erdosguess lesson and the riemann conj-lesson are not valid
    # lemma: facts in the store (the store's own falsification and
    # the conjecture surface are the store's data, not drift).
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
        p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S10 must not flip)")
    checks["p3_seam_and_theorems"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_lessons": len(seam_facts),
        "seam_theorems": len(th_facts),
        "total_seam_facts": len(seam_facts) + len(th_facts),
    }

    # P4 — the beds exact + grounded, the walls honest with their
    # frozen articulations, the attempt wall in its S10 form
    # grounded exactly on [theorem:rh-reach].
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
    for ref, arts in sorted(WALL_ARTICULATIONS.items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing wall {ref}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the wall is not an honest needs_info ({ir.get('uncertainty_state')})")
        ans = str(ir.get("answer", ""))
        for art in arts:
            if art not in ans:
                p4_bad.append(f"{ref}: the frozen articulation fragment {art!r} is missing")
    for k in FROZEN["attempt_turns"]:
        t = turns.get(k)
        if t is None:
            p4_bad.append(f"missing attempt {k}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{k}: the attempt is not an honest needs_info ({ir.get('uncertainty_state')})")
        if _ir_answer(t) != "needs_info: " + _ANSWER_["WALL_ATTEMPT_S10"]:
            p4_bad.append(f"{k}: the attempt answer is not the frozen S10 form")
        if list(map(str, t["grounded"])) != ["theorem:rh-reach"]:
            p4_bad.append(f"{k}: the attempt grounded premises {t['grounded']} != exactly [theorem:rh-reach]")
    checks["p4_beds_walls_attempt"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(WALL_ARTICULATIONS),
        "attempt_refs": list(FROZEN["attempt_turns"]),
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant: no grounded list in the run carries the conj id
    # (S10 has no conj-teach turn: the M8 exception does not apply);
    # NO `theorem:riemann` assertion exists in the final store (the
    # discovery candidate has not materialized — if this list is
    # non-empty, STOP, human review, full evidence); the bed
    # owners; the theorem allow-set.
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S10 has no conj-teach turn)")
    riemann_th = [a.id for a in final.query() if a.id.startswith("theorem:riemann")]
    if riemann_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {riemann_th} — the sanctioned corpus now produces theorem:riemann")
    for ref, owner in sorted(FROZEN["bed_owners"].items()):
        t = turns.get(ref)
        if t is None:
            p5_bad.append(f"missing bed {ref}")
            continue
        owners = {owner}
        if owner == "lemma:pnt-error":
            owners.add("lemma:psi-eq")  # the gap-compare bed cites its TWO owning seam facts (frozen P5 design)
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
    checks["p5_conjecture_and_discovery"] = {
        "pass": not p5_bad,
        "bad": p5_bad,
        "conj_grounded_refs": conj_grounded,
        "conj_exceptions": [],
        "discovery_candidate_riemann_theorem_facts": riemann_th,
    }

    # P6 — the band-end table (S4:30 probes): every ref exact.
    p6_bad: list[str] = []
    for ref, expected in sorted(FROZEN["band_end_probes"].items()):
        t = turns.get(ref)
        if t is None:
            p6_bad.append(f"missing {ref}")
            continue
        ans = _ir_answer(t)
        if ans != expected:
            p6_bad.append(f"{ref}: answer {ans!r} != {expected!r}")
    checks["p6_band_end_table"] = {"pass": not p6_bad, "bad": p6_bad, "refs": len(FROZEN["band_end_probes"])}

    # P7 — the sanctioned DAG is complete in the store (seventeen
    # theorems, byte-exact depends) and the one-line-two-beds
    # cross-check (the 36 shared ids carry from the S8/S9 rungs
    # into S10 — the determinism of the carried grounding).
    p7_bad: list[str] = []
    for slug, parts in sorted(FROZEN["theorem_dag"].items()):
        try:
            a = final.get(f"theorem:{slug}")
        except KeyError:
            p7_bad.append(f"theorem:{slug}: missing from the final store")
            continue
        got = tuple((a.context.data.get("depends") or ()) if a.context else ())
        if got != tuple(parts):
            p7_bad.append(f"theorem:{slug}: depends {got} != frozen {tuple(parts)}")
    bref = turns[FROZEN["bed_crosscheck"]["pi_ref"]]
    jref = turns[FROZEN["bed_crosscheck"]["jfunc_ref"]]
    shared = set(map(str, bref["grounded"])) & set(map(str, jref["grounded"]))
    if shared != set(FROZEN["bed_crosscheck"]["shared"]):
        p7_bad.append(
            f"cross-check: the pi-84 bed (S02:16) and the jfunc-12 bed (S02:17) share {len(shared)} ids, not the frozen 36 "
            f"(drift: {sorted(shared ^ set(FROZEN['bed_crosscheck']['shared']))[:6]}...)"
        )
    checks["p7_dag_and_crosscheck"] = {
        "pass": not p7_bad,
        "bad": p7_bad,
        "dag_size": len(FROZEN["theorem_dag"]),
        "shared_count": len(shared),
    }

    # P8 — the store totals, the line census, the ONE new fact, the
    # determinism twin, the run/store identities, and the mastery
    # census (S10 adds no concepts: the 80-concept view carries
    # exact except the frozen drilled deltas at the NEW S10
    # coordinates — the D-e6y family at the S10 rung; the ACTUAL
    # deltas freeze, never the hand count).
    p8_bad: list[str] = []
    succ1 = _successor_objects(final)
    if seed_total_check["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed_total_check['seed_total']} != {FROZEN['seed_total']}")
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
    if total1 - FROZEN["seed_total"] != int(FROZEN["new_facts"] + FROZEN["new_events"]):
        p8_bad.append(
            f"delta {total1 - FROZEN['seed_total']} != new_facts ({FROZEN['new_facts']}) + new_events ({FROZEN['new_events']})"
        )
    try:
        conj = final.get("conjecture:riemann")
    except KeyError:
        conj = None
    if conj is None:
        p8_bad.append("conjecture:riemann: not in the final store")
    else:
        if conj.context.data.get("conjecture_status") != "open":
            p8_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open")
        if conj.context.data.get("source_role") != "declared-source":
            p8_bad.append("the conj fact is not declared-source")
    if runs["e6.14-run1"] != runs["e6.14-run2"]:
        p8_bad.append("the determinism twin failed: run1 != run2 (byte-identity)")
    if _store_identity(final) != _store_identity(store2):
        p8_bad.append("the determinism twin failed: store1 identity != store2 identity")
    mv = mastery_view(final, [c.id for c in CONCEPTS_E614])
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
    # the 80-concept census: every concept keeps its S9-final state and
    # carries EXACT except the frozen drilled deltas at the NEW S10
    # coordinates (the D-e6y family at the S10 rung — the ACTUAL
    # deltas freeze, never the hand count).
    drilled = dict(FROZEN["pre_s10_drilled"])
    for cid, exp in FROZEN["pre_s10_states"].items():
        v = mv.get(cid)
        if v is None:
            p8_bad.append(f"{cid}: a pre-S10 concept left the mastery view")
            continue
        want = exp["correct"] + drilled.get(cid, 0)
        if v.state != exp["state"]:
            p8_bad.append(f"{cid}: pre-S10 state CHANGED ({v.state} != {exp['state']})")
        if v.correct_derivations != want:
            p8_bad.append(f"{cid}: correct derivations {v.correct_derivations} != frozen {want} (base {exp['correct']} + drill {drilled.get(cid, 0)})")
    pre: dict[str, dict] = FROZEN["pre_s10_states"]
    mast: dict[str, dict] = FROZEN["mastery_expected"]
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
            "conj_open_declared": conj is not None
            and conj.context.data.get("conjecture_status") == "open"
            and conj.context.data.get("source_role") == "declared-source",
            "determinism_twin": runs["e6.14-run1"] == runs["e6.14-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.14-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "mastery_census": {
                cid: {"state": mv[cid].state, "correct": mv[cid].correct_derivations} for cid in mast if cid in mv
            },
            "carried_census_refs": len(pre),
            "drilled": drilled,
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


class E6_14Experiment:
    """E6.14 — S10 of the RH-TRACK: the attempt (the RH test
    proper)."""

    name = "e6.14"
    hypothesis = (
        "The RH-TRACK third band (S10) teaches NOTHING: it stores the maximal typed "
        "assembly as the store\u2019s ONE new deterministic fact \u2014 the theorem "
        "rh-reach, derived (infant provenance) from exactly (strip, mirror-region, "
        "criterion-gap), owned by the riemann line \u2014 and measures the attempt "
        "wall in its S10 form: every nontrivial zero is inside the strip and mirrored "
        "under s to 1 minus s, and the equivalence\u2019s scale meets the store\u2019s "
        "best error term with a ratio that grows without bound, and NO part of the "
        "store closes it (the square-root improvement is not a capability taught \u2014 "
        "it is the conjecture itself), grounded exactly on [theorem:rh-reach] at both "
        "attempt turns; the typed part-set failure names the missing mirror-region; "
        "the deviant routes (Li, S-of-T) close off where the conjecture begins; the "
        "conjecture stays open, declared-source, its id in ZERO grounded lists across "
        "all 75 turns; NO theorem:riemann exists in the final store (the discovery-"
        "candidate invariant); the line stays 0..84 (the ONE new fact, no successor "
        "facts); the monograph never reaches the student (P0); two runs byte-identical."
    )
    metric = "S10 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_14()
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
                Path("results/phase-6/e6.14-run1/session-S02.json"),
                Path("results/phase-6/e6.14-run1/session-S03.json"),
                Path("results/phase-6/e6.14-run1/session-S04.json"),
                Path("results/phase-6/e6.14-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
