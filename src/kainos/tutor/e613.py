# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.13 — S9 of the RH-TRACK (pre-registered, frozen): the
criterion gallery (band 2 of 3: the equivalences and the partial
results).

The RH-TRACK second band brings the C-cluster into the store: the
ELEVEN declared criterion facts (the psi/pi/St equivalences, the Li
criterion, the Polya–Hilbert program, the Lindelöf direction, the
zero-free region, the best classical error, Hardy's line zeros, the
mean square, the zero-density bound) — each a declared-source seam
fact with its honest split (the theorem vs. what remains OPEN — the
Li check is a declared numerical fact, not a proof; the Polya–Hilbert
step is an open program; the Lindelöf direction is stored one way
only) — plus the TWO sanctioned compositions (mirror-region from
zero-free + reflect; criterion-gap from psi-eq + pnt-error — the
store's own derived gap: the best error term does not meet the
equivalence's scale). The band-end suite is the S9 protocol: blind
reprobes, the beds (the gap-comparison growth claim, the Li partial,
the carried line censuses), the honesty walls (W-RH-10/11/12/14 + the
carried W-RH-1/3/4/5/8), the attempt in its S9 form (W-RH-6, the
FROZEN PROBE LINE — "can you derive the riemann hypothesis from the
store?" — identical in S8/S9/S10 — now GROUNDED on the store's own
derived gap), the conj-state probes, and the S7 continuity
reprobes. The line STAYS 0..84. The monograph never reaches the
student (P0). The official arm is det.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT9,
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
)
from kainos.tutor.e611 import FROZEN as E611_FROZEN
from kainos.tutor.e612 import (
    _ANSWER_ as A12,
)
from kainos.tutor.e612 import (
    CONCEPTS_E612,
)
from kainos.tutor.e612 import (
    FROZEN as E612_FROZEN,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E613", "FROZEN", "E6_13Experiment", "run_e6_13"]

CHECKS = 9

#: The official e6.12 S8 store (the S9 seed: 944 assertions, line end
#: 84, the two S8 theorems derived, `riemann` open), repo-relative.
E612_SEED = Path("results/phase-6/e6.12-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E612_SEED.exists():
        return E612_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E612_SEED
    return alt if alt.exists() else E612_SEED


#: E6.13 — the concept registry the band ends carrying: everything
#: the e6.12 band ends with, plus the ten RH S9 concepts.
CONCEPTS_E613: tuple = CONCEPTS_E612 + CONCEPT_SAVANT9

#: The eleven S9 seam facts (derived from the frozen S9_LESSONS in
#: the brainstem: slug -> kind + the exact canonical statement +
#: essence + the line crosswalk). P0/P3 read these.
_LESSON_META_S9 = {
    _slug: {"kind": _k, "statement": _phrase, "essence": _es, "source_lines": _l}
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S9_LESSONS.items()
}

#: The two S9 theorem facts (slug -> the exact canonical statement +
#: the sanctioned parts + the owning concept).
_THEOREM_META_S9 = {
    _slug: {
        "statement": _meta["statement"],
        "parts": tuple(_meta["parts"]),
        "concept": _meta["concept"],
    }
    for _slug, _meta in S9_THEOREMS.items()
}

#: The full sanctioned composition DAG (S6's six + S7's six + S8's
#: two + S9's two), frozen from the brainstem tables (P7).
_THEOREM_DAG = {
    **{s: tuple(m["parts"]) for s, m in S6_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S7_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S8_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S9_THEOREMS.items()},
}

_ST8 = {
    _slug: _phrase
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S8_LESSONS.items()
}
_TH8 = {s: m["statement"] for s, m in S8_THEOREMS.items()}


def _st9(slug: str) -> str:
    return _LESSON_META_S9[slug]["statement"]


def _th9(slug: str) -> str:
    return _THEOREM_META_S9[slug]["statement"]


def _whychain9(slug: str) -> str:
    meta = _THEOREM_META_S9[slug]
    return f"i derived it from {', '.join(meta['parts'])}: {meta['statement']}"

def _pre_st(slug: str, lessons: dict[str, tuple]) -> str:
    for _phrase, (_c, _s, _k, _es, _d, _l) in lessons.items():
        if _s == slug:
            return _phrase
    raise KeyError(slug)  # pragma: no cover


_ANSWER_ = {
    "CONJ_OPEN": E612_FROZEN["derived_table"]["S03:17"],  # byte-carried
    "SINCYCLE": A12["SINCYCLE"],
    "GROWTH": A12["GROWTH"],
    "GAP_COMP": (
        "for every fixed c greater than zero and every epsilon below one-half, x times e to the minus c times the "
        "square root of log x eventually exceeds x to the one-half plus epsilon, and the ratio grows without bound — "
        "the threshold is not a number in my store, and the point where it crosses is not in my store"
    ),
    "LI_CHECK": (
        "the check up to n = ten to the fifth is a declared numerical fact in my store; past that is not in my store"
    ),
    "WALL_CVALUE": (
        "i have been taught some constant c greater than zero exists, not its value — the sharp constant is not in my "
        "store: the region holds for some c, and which c is the open numerical content"
    ),
    "WALL_LHCONF": (
        "no — the stored direction runs one way only: the riemann hypothesis implies lindelof; the reverse is not in my "
        "store — lindelof is a status surface i hold, and nothing in the store closes the gap"
    ),
    "WALL_PHCONF": (
        "no — the reformulation is a theorem (the conjecture as a spectral statement about a positive self-adjoint "
        "operator); the step that recovers the conjecture from the spectrum is an open program, not in my store"
    ),
    "WALL_LIPROOF": (
        "no — the positivity for all n is exactly what the criterion equates with the conjecture, and it is unproven in "
        "my store; the check up to n = ten to the fifth is a declared numerical fact, not a proof"
    ),
    "WALL_ATTEMPT_S9": (
        "no — the conjecture is a status surface, never a part: my own store tells me why. the farthest the store "
        "reaches is the criterion gap i derived from the equivalence and the best error term: my error, of order x times "
        "e to the minus c times the square root of log x, does not meet the scale the equivalence demands, x to the "
        "one-half plus epsilon — their ratio grows without bound. the square-root improvement is not a capability i have "
        "been taught — and it is the conjecture itself"
    ),
}

GAP_ARTICULATION = "not a capability i have been taught"

#: P4 — the per-wall articulations (frozen from control #1): every
#: wall must carry its exact honest phrases (the W-RH ledger rows).
WALL_ARTICULATIONS: dict[str, tuple[str, ...]] = {
    "S03:03": ("open program",),  # W-RH-11 (the Polya–Hilbert step)
    "S03:12": ("not in my store",),  # W-RH-14 (the c-value)
    "S03:13": ("one way only",),  # W-RH-10 (the Lindelöf direction)
    "S03:15": ("not a proof",),  # W-RH-12 (the Li positivity)
    "S04:22": ("not a proof",),  # W-RH-1 (first appearance in the S9 run)
    "S04:23": ("no proof that there is none",),  # W-RH-3
    "S04:24": ("the other way",),  # W-RH-4
    "S04:25": ("away from the critical strip",),  # W-RH-5
    "S04:26": ("not in my store",),  # W-RH-8
}

#: The eleven NEW declared criterion facts (frozen; P3 checks every
#: one ESTABLISHED declared-source, byte-equal).
S9_SEAM_FROZEN = {slug: meta for slug, meta in _LESSON_META_S9.items()}

#: The two NEW theorem facts (frozen; P3 checks every one DERIVED
#: with exactly the sanctioned parts).
S9_THEOREM_FROZEN = {slug: meta for slug, meta in _THEOREM_META_S9.items()}

#: The thirteen NEW prereq edges (frozen curriculum data).
S9_PREREQ_EDGES = [
    "curriculum:prereq:psi-eq>pnt",
    "curriculum:prereq:pi-eq>prime-count",
    "curriculum:prereq:st-eq>s-of-t",
    "curriculum:prereq:li-criterion>psi-eq",
    "curriculum:prereq:polya-hilbert>critical-strip",
    "curriculum:prereq:lindelof>rv-count",
    "curriculum:prereq:lindelof>critical-strip",
    "curriculum:prereq:zero-free>func-eq",
    "curriculum:prereq:pnt-error>zero-free",
    "curriculum:prereq:hardy-line>rv-count",
    "curriculum:prereq:hardy-line>s-of-t",
    "curriculum:prereq:zero-density>rv-count",
    "curriculum:prereq:zero-density>zero-free",
]

#: The thirty-six NEW fact ids (11 lemmas + 2 theorems + 10
#: registries + 13 prereq edges) — all deterministic, frozen NOW.
S9_NEW_FACT_IDS = (
    [f"lemma:{s}" for s in S9_SEAM_FROZEN]
    + [f"theorem:{s}" for s in S9_THEOREM_FROZEN]
    + [
        "curriculum:psi-eq",
        "curriculum:pi-eq",
        "curriculum:st-eq",
        "curriculum:li-criterion",
        "curriculum:polya-hilbert",
        "curriculum:lindelof",
        "curriculum:zero-free",
        "curriculum:pnt-error",
        "curriculum:hardy-line",
        "curriculum:zero-density",
    ]
    + S9_PREREQ_EDGES
)

#: The ten NEW S9 concepts (frozen by name).
S9_CONCEPT_IDS = (
    "psi-eq",
    "pi-eq",
    "st-eq",
    "li-criterion",
    "polya-hilbert",
    "lindelof",
    "zero-free",
    "pnt-error",
    "hardy-line",
    "zero-density",
)

FROZEN: dict[str, Any] = {
    # P8 — the seed (the official e6.12 S8 final store).
    "seed": str(E612_SEED),
    "seed_total": 944,
    "total_turns": 75,
    "line_end_final": 84,  # the line STAYS 0..84 (zero new successor facts)
    # P2 — the typed honesty turns (the four pre-lesson gaps, the
    # one scaffold failure, the two derive-successes).
    "pre_teach_gaps": {
        "S02:01": "zero-free",
        "S02:25": "polya-hilbert",
        "S03:04": "hardy-line",
        "S03:08": "zero-density",
    },
    "scaffold_failures": {
        "S02:06": "criterion-gap: missing psi-eq",
    },
    "derive_successes": {
        "S02:09": "criterion-gap",
        "S02:17": "mirror-region",
    },
    # P2/P4 — the conj-state probes (evidence carries the conj id,
    # grounded EMPTY all run; S9 has NO conj-teach turn — the M8
    # self-citation exception does not apply).
    "conj_status_open": ("S03:16", "S04:28"),
    "conj_evidence_refs": ("S03:16", "S04:28"),
    # P3 — the why-split refs (mechanical).
    "why_chains": {
        "S02:11": "criterion-gap",
        "S02:19": "mirror-region",
        "S04:14": "mirror-region",
        "S04:15": "criterion-gap",
    },
    "why_walls": {},  # the S9 frozen script has no declared-lemma why-deep probes
    # P4 — the beds exact (the line censuses write no new assertions).
    "beds_exact": {
        "S02:12": _ANSWER_["GAP_COMP"],
        "S02:22": _ANSWER_["LI_CHECK"],
        "S03:11": _ANSWER_["GAP_COMP"],
        "S03:14": _ANSWER_["LI_CHECK"],
        "S03:17": "23",
        "S03:18": "35",
        "S04:16": "23",
        "S04:17": "71",
        "S04:18": _ANSWER_["SINCYCLE"],
        "S04:19": _ANSWER_["GROWTH"],
        "S04:20": _ANSWER_["GAP_COMP"],
        "S04:21": _ANSWER_["LI_CHECK"],
    },
    "bed_owners": {
        "S02:12": "lemma:pnt-error",
        "S02:22": "lemma:li-criterion",
        "S03:11": "lemma:pnt-error",
        "S03:14": "lemma:li-criterion",
        "S03:17": "lemma:euler-product",
        "S03:18": "lemma:euler-product",
        "S04:16": "lemma:euler-product",
        "S04:17": "lemma:euler-product",
        "S04:18": "lemma:trivial-zeros",
        "S04:19": "lemma:pnt",
        "S04:20": "lemma:pnt-error",
        "S04:21": "lemma:li-criterion",
    },
    "walls_honest": {
        "S03:03": "the polya-hilbert open program (W-RH-11)",
        "S03:12": "the c-value wall (W-RH-14: some c, not the value)",
        "S03:13": "the lindelof directionality (W-RH-10: one stored direction)",
        "S03:15": "the li-proof wall (W-RH-12: the check is not a proof)",
        "S04:22": "the numerical-check wall re-run (W-RH-1: first appearance in the S9 run)",
        "S04:23": "off-line zeros (W-RH-3: beyond store)",
        "S04:24": "the pnt-confusion (W-RH-4: directionality)",
        "S04:25": "the product-confusion (W-RH-5: scope)",
        "S04:26": "zeta at 3/4 (W-RH-8: no value tables)",
    },
    "attempt_turns": ("S03:20", "S04:27"),
    # P4/P6 — the band-end table (the S9 protocol: blind reprobes +
    # beds + walls + the attempt in its S9 form + the conj-state
    # probes + the S7 continuity reprobes).
    "band_end_probes": {
        "S04:01": _st9("zero-free-region"),
        "S04:02": _st9("pnt-error"),
        "S04:03": _st9("psi-eq"),
        "S04:04": _st9("pi-eq"),
        "S04:05": _st9("st-eq"),
        "S04:06": _st9("li-criterion"),
        "S04:07": _st9("polya-hilbert"),
        "S04:08": _st9("hardy"),
        "S04:09": _st9("mean-square"),
        "S04:10": _st9("zero-density"),
        "S04:11": _st9("lindelof"),
        "S04:12": _th9("mirror-region"),
        "S04:13": _th9("criterion-gap"),
        "S04:14": _whychain9("mirror-region"),
        "S04:15": _whychain9("criterion-gap"),
        "S04:16": "23",
        "S04:17": "71",
        "S04:18": _ANSWER_["SINCYCLE"],
        "S04:19": _ANSWER_["GROWTH"],
        "S04:20": _ANSWER_["GAP_COMP"],
        "S04:21": _ANSWER_["LI_CHECK"],
        "S04:22": "needs_info: " + A12["WALL_NUMCHECK"],
        "S04:23": "needs_info: " + A12["WALL_OFFZERO"],
        "S04:24": "needs_info: " + A12["WALL_PNTCONF"],
        "S04:25": "needs_info: " + A12["WALL_PRODCONF"],
        "S04:26": "needs_info: " + A12["WALL_ZETAVAL"],
        "S04:27": "needs_info: " + _ANSWER_["WALL_ATTEMPT_S9"],
        "S04:28": _ANSWER_["CONJ_OPEN"],
        "S04:29": _pre_st("tower-base", S7_LESSONS),
        "S04:30": S7_THEOREMS["theorem-main"]["statement"],
    },
    # P3 — the derived table (every state/why/bed/status answer
    # exact).
    "derived_table": {
        "S02:03": _st9("zero-free-region"),
        "S02:05": _st9("pnt-error"),
        "S02:08": _st9("psi-eq"),
        "S02:10": _th9("criterion-gap"),
        "S02:11": _whychain9("criterion-gap"),
        "S02:12": _ANSWER_["GAP_COMP"],
        "S02:14": _st9("pi-eq"),
        "S02:16": _st9("st-eq"),
        "S02:18": _th9("mirror-region"),
        "S02:19": _whychain9("mirror-region"),
        "S02:21": _st9("li-criterion"),
        "S02:22": _ANSWER_["LI_CHECK"],
        "S02:24": _st9("lindelof"),
        "S03:02": _st9("polya-hilbert"),
        "S03:06": _st9("hardy"),
        "S03:10": _st9("zero-density"),
        "S03:11": _ANSWER_["GAP_COMP"],
        "S03:14": _ANSWER_["LI_CHECK"],
        "S03:16": _ANSWER_["CONJ_OPEN"],
        "S03:17": "23",
        "S03:18": "35",
        "S03:19": _TH8["strip"],
        "S04:01": _st9("zero-free-region"),
        "S04:02": _st9("pnt-error"),
        "S04:03": _st9("psi-eq"),
        "S04:04": _st9("pi-eq"),
        "S04:05": _st9("st-eq"),
        "S04:06": _st9("li-criterion"),
        "S04:07": _st9("polya-hilbert"),
        "S04:08": _st9("hardy"),
        "S04:09": _st9("mean-square"),
        "S04:10": _st9("zero-density"),
        "S04:11": _st9("lindelof"),
        "S04:12": _th9("mirror-region"),
        "S04:13": _th9("criterion-gap"),
        "S04:14": _whychain9("mirror-region"),
        "S04:15": _whychain9("criterion-gap"),
        "S04:16": "23",
        "S04:17": "71",
        "S04:18": _ANSWER_["SINCYCLE"],
        "S04:19": _ANSWER_["GROWTH"],
        "S04:20": _ANSWER_["GAP_COMP"],
        "S04:21": _ANSWER_["LI_CHECK"],
        "S04:28": _ANSWER_["CONJ_OPEN"],
        "S04:29": _pre_st("tower-base", S7_LESSONS),
        "S04:30": S7_THEOREMS["theorem-main"]["statement"],
    },
    # P5 — the theorem ids may appear in `grounded` ONLY on the
    # frozen allow-set refs (state/why/derive turns over the theorems
    # + the two attempt turns carrying criterion-gap).
    "theorem_allowed": {
        "S02:10": ("criterion-gap",),
        "S02:17": ("reflect",),  # the mirror derive grounds on its own parts
        "S02:18": ("mirror-region",),
        "S02:19": ("reflect",),
        "S03:19": ("strip",),
        "S03:20": ("criterion-gap",),
        "S04:12": ("mirror-region",),
        "S04:13": ("criterion-gap",),
        "S04:14": ("reflect",),
        "S04:27": ("criterion-gap",),
        "S04:30": ("theorem-main",),  # the S7 continuity reprobe
    },
    # P7 — the full sanctioned DAG (S6 + S7 + S8 + S9: sixteen
    # theorems) is check-able.
    "theorem_dag": _THEOREM_DAG,
    # P7 — the one-line-two-beds cross-check (the S9 rung: the pi-84
    # re-bed and the jfunc-12 re-bed reproduce the S8 shared
    # citations EXACTLY — the determinism of the carried grounding).
    "bed_crosscheck": {
        "pi_ref": "S03:17",
        "jfunc_ref": "S03:18",
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
    "prereq_edges": S9_PREREQ_EDGES,
    "new_fact_ids": S9_NEW_FACT_IDS,
    "total_seam_facts": 82,  # 69 carried (the e6.12 final census) + 13 (11 lemmas + 2 theorems)
    # P2 — the frozen domain sequences (letters: L lesson,
    # U pre-lesson gap, F scaffold-failure, T derive-success,
    # S derived, H honest wall). Per house policy 2026-08-23 rule 3:
    # mechanically derived from the labeled per-turn table, frozen
    # from control #1, written once to /tmp/rh-s9-domains.txt.
    "domain_sequence": {
        # control #1 (evidence /tmp/rh-s9-control1.txt; written once, read back)
        2: "ULSLSFLSTSSSLSLSTSSLSSLSU",
        3: "LSHULSLULSSHHSHSSSSH",
        4: "SSSSSSSSSSSSSSSSSSSSSHHHHHHSSS",
    },
    # P8 — store totals (FROZEN FROM CONTROL #1; the D-e6y-pattern
    # collision at the S4:30 continuity reprobe — the exact e6.11/
    # e6.12 S4:30 coordinate on `disproof` — dedupes AGAIN; the
    # ACTUAL total freezes, never the hand count).
    "final_total": 1037,  # control #1: 944 + 36 facts + 57 events
    "new_facts": len(S9_NEW_FACT_IDS),  # 36 (frozen NOW — all deterministic)
    "new_events": 57,  # control #1 (the D-e6y-family dedupes at the carried seed's s04-t coordinates)
    # P8 — mastery of the TEN S9 concepts (FROZEN FROM CONTROL #1).
    # HONEST PRAW EXPECTATION (W-S9): TWO NEW STABLES riding stable
    # prereqs — psi-eq (prereq pnt stable) and li-criterion (prereq
    # psi-eq stable at band end); eight PRACTICING with their
    # prereq gaps per the frozen table (see the pre-reg).
    "mastery_expected": {
        "psi-eq": {"state": "stable", "correct": 7},
        "li-criterion": {"state": "stable", "correct": 5},
        "pi-eq": {"state": "practicing", "correct": 2},
        "st-eq": {"state": "practicing", "correct": 2},
        "polya-hilbert": {"state": "practicing", "correct": 2},
        "lindelof": {"state": "practicing", "correct": 2},
        "zero-density": {"state": "practicing", "correct": 2},
        "hardy-line": {"state": "practicing", "correct": 3},
        "pnt-error": {"state": "practicing", "correct": 5},
        "zero-free": {"state": "practicing", "correct": 7},
    },
    # control #1 — the honest read matched the PRAW forecast exactly
    # (two new stables: psi-eq and li-criterion; eight practicing).
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
    },
    # P8 — the pre-S9 states that must NOT change (the e6.12 final
    # census: the 56 carried + the five S7 at their S8-final values
    # + the nine S8 at their S8-final values = 71 concepts). The
    # drilled moves (tower-base, prime-count, func-eq, pnt, and the
    # D-e6y-deduped disproof) are the frozen deltas below.
    "pre_s9_states": {
        **E611_FROZEN["pre_s7_states"],
        "tower-base": {"state": "practicing", "correct": 8},
        "tower-group": {"state": "practicing", "correct": 11},
        "tower-primes": {"state": "practicing", "correct": 8},
        "tower-class": {"state": "practicing", "correct": 8},
        "disproof": {"state": "practicing", "correct": 10},
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
    # control #1 — the D-e6y family at the carried seed: the S4-band
    # re-probes (s04t16..s04t30) already exist in the e6.12 seed and
    # dedupe (tower-base, func-eq, pnt, disproof ALL +0); the movers
    # are the NEW session-local coordinates written in S3.
    "pre_s9_drilled": {
        "critical-strip": 1,  # S03:19 strip state (new coord s03t19)
        "prime-count": 1,  # S03:17 pi-84 re-bed (new coord s03t17; S03:18 j-12 dedupes)
        "riemann": 1,  # S03:16 conj-state (new coord s03t16)
    },
    "script": {
        2: [
            "state the zero-free-region rule",
            _st9("zero-free-region"),
            "state the zero-free-region rule",
            _st9("pnt-error"),
            "state the pnt-error rule",
            "derive criterion-gap from psi-eq and pnt-error",
            _st9("psi-eq"),
            "state the psi-eq rule",
            "derive criterion-gap from psi-eq and pnt-error",
            "state the criterion-gap rule",
            "explain why the criterion-gap holds",
            "what is the expected growth of the gap ratio?",
            _st9("pi-eq"),
            "state the pi-eq rule",
            _st9("st-eq"),
            "state the st-eq rule",
            "derive mirror-region from zero-free-region and reflect",
            "state the mirror-region rule",
            "explain why the mirror-region holds",
            _st9("li-criterion"),
            "state the li-criterion rule",
            "have li's numbers been verified positive up to a bound?",
            _st9("lindelof"),
            "state the lindelof rule",
            "state the polya-hilbert rule",
        ],
        3: [
            _st9("polya-hilbert"),
            "state the polya-hilbert rule",
            "does the polya-hilbert program prove the riemann hypothesis?",
            "state the hardy rule",
            _st9("hardy"),
            "state the hardy rule",
            _st9("mean-square"),
            "state the zero-density rule",
            _st9("zero-density"),
            "state the zero-density rule",
            "what is the expected growth of the gap ratio?",
            "what is the exact value of c in the zero-free region?",
            "does lindelof imply the riemann hypothesis?",
            "have li's numbers been verified positive up to a bound?",
            "is li's positivity proven for all n?",
            "what is the status of the riemann hypothesis?",
            "how many primes are at most 84?",
            "what is the prime-power phi count at 12?",
            "state the strip rule",
            "can you derive the riemann hypothesis from the store?",
        ],
        4: [
            "state the zero-free-region rule",
            "state the pnt-error rule",
            "state the psi-eq rule",
            "state the pi-eq rule",
            "state the st-eq rule",
            "state the li-criterion rule",
            "state the polya-hilbert rule",
            "state the hardy rule",
            "state the mean-square rule",
            "state the zero-density rule",
            "state the lindelof rule",
            "state the mirror-region rule",
            "state the criterion-gap rule",
            "explain why the mirror-region holds",
            "explain why the criterion-gap holds",
            "how many primes are at most 84?",
            "what is the prime-power phi count at 18?",
            "does the sine vanish at every integer multiple of pi from one to 84?",
            "what is the expected growth of the prime-power phi count?",
            "what is the expected growth of the gap ratio?",
            "have li's numbers been verified positive up to a bound?",
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

#: the eleven S9 lesson phrases (frozen) must appear IN the script,
#: byte-exact (the literal script turns are the canonical bytes)
for _phrase in S9_LESSONS:
    assert any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"the S9 lesson phrase is not verbatim in the frozen script: {_phrase[:60]}..."
    )

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict
#: (the sentinels are replaced by control #1, evidence in /tmp).
_UNFROZEN = (
    (FROZEN["domain_sequence"].get(2) or "").startswith("##FREEZE")
    or (FROZEN["domain_sequence"].get(3) or "").startswith("##FREEZE")
    or str(FROZEN["final_total"]).startswith("##FREEZE")
    or str(FROZEN["new_events"]).startswith("##FREEZE")
    or str(FROZEN["mastery_expected"]).startswith("##FREEZE")
    or str(FROZEN["expected_prereq_gaps"]).startswith("##FREEZE")
    or str(FROZEN["pre_s9_drilled"]).startswith("##FREEZE")
)


def _line_end(store) -> int:
    """The current line end = the largest successor fact v+1 in the
    store (the e6.8 machinery, unchanged by S9)."""

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
    rt = InfantRuntime(root, concepts=CONCEPTS_E613)
    out: list[dict] = []
    for s in (2, 3, 4):
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.12 S8 store, id-for-id."""

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
    of the final store (the S7/S8 pattern, P1/P8)."""

    pairs = []
    for a in store.query():
        pairs.append((a.id, json.dumps(a.to_dict(), sort_keys=True, default=str)))
    pairs.sort()
    return hashlib.sha256(json.dumps(pairs, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.13-run1"]:
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
        "rh_facts": {slug: {"statement": meta["statement"], "kind": meta["kind"]} for slug, meta in S9_SEAM_FROZEN.items()},
        "theorem_facts": {slug: {"statement": meta["statement"]} for slug, meta in S9_THEOREM_FROZEN.items()},
    }


def run_e6_13(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.12 S8 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {"error": "S9 frozen constants are not yet frozen (control #1 must replace the ##FREEZE## sentinels; see the E6.13 pre-reg open points)"}
    runs: dict[str, list[dict]] = {}
    for name in ("e6.13-run1", "e6.13-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.12 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — with the RH S9
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E613}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.13-run1", "e6.13-run2"):
        (out_dir / name / "e6.13-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.13.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict[str, list[dict]], report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.13-run1"
    final = _fresh_store(run1_root, 4)

    # P0 — the monograph NEVER reached the student: the S9 denylist
    # (the S8 44 UNCHANGED) over EVERY script turn, every turn's
    # actual response (the new S9 grammar articulations included),
    # every carried + new declared seam statement, and every
    # theorem statement.
    p0_bad: list[str] = []
    surfaces: list[str] = []
    for s, script in sorted(FROZEN["script"].items()):
        surfaces.extend(script)
    for ref, t in sorted(turns.items()):
        surfaces.append(str(t.get("response_text") or ""))
        ir = t.get("response_ir") or {}
        surfaces.append(str(ir.get("answer") or ""))
    for lessons in (S4_LESSONS, S5_LESSONS, S6_LESSONS, S7_LESSONS, S8_LESSONS, S9_LESSONS):
        surfaces.extend(lessons)  # the lesson phrases are the dict keys
    for theorems in (S6_THEOREMS, S7_THEOREMS, S8_THEOREMS, S9_THEOREMS):
        for meta in theorems.values():
            surfaces.append(meta["statement"])
    for term in S9_DENYLIST:
        for surface in surfaces:
            if term in surface:
                p0_bad.append(f"banned source text in a surface: {term!r}")
                break
    for slug, meta in S9_SEAM_FROZEN.items():
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

    # P2 — the typed honesty: the four pre-lesson gaps (U), the one
    # scaffold failure (F), the two derive-successes (T), the frozen
    # interleave, and the line end
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
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S9 adds ZERO successor facts)")
    checks["p2_typed_honesty_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — the SEAM + the THEOREMS: 82 seam-family facts (69 carried
    # + 13 new), ALL S9 statements byte-equal to the frozen
    # canonical statements, ALL pre-S9 seam facts byte-unchanged,
    # the S9 theorems DERIVED with evidence exactly the sanctioned
    # parts, the conj STILL `open` (S9 has no conj-teach turn), the
    # prereq edges established, every derived answer exact +
    # grounded, the why-split mechanical
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
    # the eleven S9 seam facts
    for slug, meta in sorted(S9_SEAM_FROZEN.items()):
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
    # the conj: STILL open, STILL declared-source (no flip in S9)
    try:
        conj = final.get("conjecture:riemann")
    except KeyError:
        conj = None
    if conj is None:
        p3_bad.append("conjecture:riemann: not in the final store")
    else:
        if conj.context.data.get("conjecture_status") != "open":
            p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S9 must not flip)")
    # the two S9 theorem facts (DERIVED provenance, exact parts)
    for slug, meta in sorted(S9_THEOREM_FROZEN.items()):
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
    # every pre-S9 seam fact: byte-exact (no drift)
    for _lessons, _label in (
        (S4_LESSONS, "S4"),
        (S5_LESSONS, "S5"),
        (S6_LESSONS, "S6"),
        (S7_LESSONS, "S7"),
        (S8_LESSONS, "S8"),
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
    # articulation (the S9 script has no declared-lemma why-deep
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
    # ATTEMPT in its S9 form (grounded on the store's own derived
    # gap), EXACT
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
    # the ATTEMPT in its S9 form: the frozen probe line, the frozen
    # articulation, needs_info, grounded EXACTLY on the derived gap
    for ref in FROZEN["attempt_turns"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing the S9-form attempt {ref}")
            continue
        ir = t["response_ir"] or {}
        if _ir_answer(t) != "needs_info: " + _ANSWER_["WALL_ATTEMPT_S9"]:
            p4_bad.append(f"{ref}: the S9 attempt articulation is not exact")
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append(f"{ref}: the S9 attempt is not an honest needs_info")
        if tuple(str(x) for x in t["grounded"]) != ("theorem:criterion-gap",):
            p4_bad.append(f"{ref}: the S9 attempt grounded {list(t['grounded'])} != exactly [theorem:criterion-gap]")
    for ref in FROZEN["conj_status_open"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        if _ir_answer(t) != FROZEN["derived_table"][ref]:
            p4_bad.append(f"{ref}: the conj-state probe is not exact")
    checks["p4_beds_walls_attempt"] = {"pass": not p4_bad, "bad": p4_bad, "bed_refs": len(FROZEN["beds_exact"])}

    # P5 — the SEAM invariance + the conjecture: the riemann fact
    # id in ZERO `grounded` lists across ALL 75 turns (S9 has no
    # conj-teach turn — the M8 exception does not apply); the beds
    # ground ONLY on line facts + their owning seam fact; no
    # theorem is a premise outside the frozen allow-set
    p5_bad: list[str] = []
    CONJ = "conjecture:riemann"
    for ref, t in sorted(turns.items()):
        if any(CONJ in str(x) for x in t["grounded"]):
            p5_bad.append(f"{ref}: the conjecture was cited as a derivation premise")
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
        owners = {owner}
        if owner == "lemma:pnt-error":
            owners.add("lemma:psi-eq")  # the gap-compare bed cites its TWO owning seam facts (frozen P5 design)
        for g in t["grounded"]:
            g = str(g)
            if not (g.startswith(("cs-", "count-successor")) or g in owners):
                p5_bad.append(f"{ref}: the bed cited a non-line fact {g} (allowed: line facts + the owning seam facts)")
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

    # P6 — the band-end table (blind reprobes + beds + walls + the
    # attempt in its S9 form + the conj-state probes + the S7
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
    # derivation DAG from ALL sixteen theorem facts (S6 + S7 + S8 +
    # S9) reproduces the sanctioned composition DAG exactly; every
    # theorem's evidence list ⊆ store ids; the one-line-two-beds
    # check at the S9 rung (the pi-84 re-bed and the jfunc-12 re-bed
    # share EXACTLY the S8 frozen 36 shared ids — the determinism of
    # the carried grounding)
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
        p8_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S9 adds ZERO successor facts)")
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
    # the conjecture: STILL open, STILL declared-source (the S10
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
            p8_bad.append("the conj is no longer declared-source (it must not change in S9)")
    mv = mastery_view(final, [c.id for c in CONCEPTS_E613])
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
    # the pre-S9 census: every OTHER concept keeps its exact
    # (state, correct) except the frozen drilled deltas; the
    # D-e6y-pattern collision at the S4:30 theorem-main continuity
    # reprobe dedupes AGAIN (disproof +0)
    drilled = dict(FROZEN["pre_s9_drilled"])
    for cid, exp in FROZEN["pre_s9_states"].items():
        if cid in drilled:
            continue
        v = mv.get(cid)
        if v is None:
            p8_bad.append(f"{cid}: a pre-S9 concept left the mastery view")
            continue
        if v.state != exp["state"]:
            p8_bad.append(f"{cid}: pre-S9 state CHANGED ({v.state} != {exp['state']}) — W-S9 measures this")
        if v.correct_derivations != exp["correct"]:
            p8_bad.append(f"{cid}: pre-S9 correct derivations {v.correct_derivations} != frozen {exp['correct']}")
    for cid, delta in drilled.items():
        v = mv.get(cid)
        base = FROZEN["pre_s9_states"][cid]
        if v is None:
            p8_bad.append(f"{cid}: a drilled concept left the mastery view")
            continue
        if v.state != base["state"]:
            p8_bad.append(f"{cid}: drilled concept state CHANGED ({v.state} != {base['state']})")
        if v.correct_derivations != base["correct"] + delta:
            p8_bad.append(f"{cid}: drilled correct {v.correct_derivations} != {base['correct']} + {delta}")
    # determinism
    r1 = runs["e6.13-run1"]
    r2 = runs["e6.13-run2"]
    a = json.dumps(r1, sort_keys=True)
    b = json.dumps(r2, sort_keys=True)
    if a != b:
        p8_bad.append("run1 != run2")
    final2 = _fresh_store(out_dir / "e6.13-run2", 4)
    if _store_identity(final) != _store_identity(final2):
        p8_bad.append("the two runs end in different stores (the store identity)")
    det_arm = all((t.get("arm") or {}).get("classifier") == "det" for srow in r1 for t in srow.get("turns", []))
    if not det_arm:
        p8_bad.append("a turn was not the det arm")
    checks["p8_mastery_determinism"] = {
        "pass": not p8_bad,
        "bad": p8_bad,
        "mastery": {
            cid: {"state": mv[cid].state, "correct": mv[cid].correct_derivations} for cid in S9_CONCEPT_IDS if cid in mv
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
    value = f"PASS e6.13: {passed}/{len(checks)}" if passed == len(checks) else f"FAIL e6.13: {passed}/{len(checks)}"
    return {"checks": checks, "passed": passed, "value": value}


class E6_13Experiment:
    """E6.13 — S9 of the RH-TRACK: the criterion gallery (the
    equivalences and the partial results: the store's own derived
    gap, the arcs of the store's reach, and the attempt wall
    grounded on the store's own reasoning)."""

    name = "e6.13"
    hypothesis = (
        "The RH-TRACK second band (S9) stores the criterion gallery NOT as lessons "
        "about the conclusion but as DECLARED seam lemmas (the psi/pi/St "
        "equivalences, the Li criterion, the Polya–Hilbert program, the Lindelöf "
        "direction, the zero-free region, the best classical error, Hardy's line "
        "zeros, the mean square, the zero-density bound — each with its honest "
        "split: theorem vs. open) plus the two sanctioned compositions (mirror-"
        "region from zero-free + reflect; criterion-gap from psi-eq + pnt-error — "
        "the store's own derived gap: the best error term does not meet the "
        "equivalence's scale and their ratio grows without bound); the riemann "
        "conjecture stays open, declared-source, the id in zero grounded lists "
        "across all 75 turns; the attempt probe (the frozen S8/S9/S10 line) now "
        "articulates the criterion gap GROUNDED on the store's own derived "
        "theorem; the beds (the gap-comparison growth claim, the Li partial, the "
        "carried line censuses) ground on line facts + owning seam facts and "
        "write no new assertions; the honesty walls are the W-RH-10/11/12/14 rows "
        "(one stored direction, the open program, the check-not-a-proof, the "
        "free parameter); the line stays 0..84; the monograph never reaches the "
        "student (P0); two runs byte-identical."
    )
    metric = "S9 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_13()
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
                Path("results/phase-6/e6.13-run1/session-S02.json"),
                Path("results/phase-6/e6.13-run1/session-S03.json"),
                Path("results/phase-6/e6.13-run1/session-S04.json"),
                Path("results/phase-6/e6.13-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
