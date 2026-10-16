# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.11 — S7 of the SAVANT-TRACK (pre-REGISTERED, frozen): the
arithmetical half "tower ⇒ disproof" (savant-4, THE SAVANT TEST PROPER).

The ARITHMETICAL HALF of the paper enters the store: the seven tower
seam lemmas are TAUGHT as declared-source facts (the cyclic cubic
base, the unramified compositum, the base root-discriminant, the
selected split primes, the k = 3t count, the class bound per level,
the slack primitive) and the six sanctioned compositions are
SCAFFOLDED into `theorem:{slug}` facts with derived provenance
(gen-lower, gs-infinite, splitting, gamma-achieved, tower-feeds,
theorem-main — the paper's Theorem 1.1). The geometric criterion
(S6) is APPLIED: theorem-main = (tower-feeds, infinity-end), and the
`erdosguess` flips `open → falsified (by theorem:theorem-main)` by an
in-store derivation ALONE (the M8 upsert — a store-mediated state
change on the same id). The band-end suite is the SAVANT PROTOCOL:
Stage A (blind reproduction from the final store), Stage B (the
full disproof reconstructed from the conjecture-as-challenge, the
M-chain in evidence), confounder probes (a normed-plane route must
not derail), honesty probes (beyond-store ⇒ honest I-don't-knows).
The line STAYS 0..84 (zero new successor facts). The paper never
reaches the student (P0). The official arm is det.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT7,
    S4_LESSONS,
    S5_LESSONS,
    S6_LESSONS,
    S6_THEOREMS,
    S7_DENYLIST,
    S7_LESSONS,
    S7_THEOREMS,
)
from kainos.tutor.e610 import CONCEPTS_E610
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E611", "FROZEN", "E6_11Experiment", "run_e6_11"]

CHECKS = 9

#: The official e6.10 S6 store (the S7 seed: 734 assertions, line
#: end 84, the six S6 theorem facts derived, the erdosguess open),
#: repo-relative.
E610_SEED = Path("results/phase-6/e6.10-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E610_SEED.exists():
        return E610_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E610_SEED
    return alt if alt.exists() else E610_SEED


#: E6.11 — the concept registry the band ends carrying: everything
#: the e6.10 band ends with, plus the five savant S7 concepts.
CONCEPTS_E611: tuple = CONCEPTS_E610 + CONCEPT_SAVANT7

#: The seven S7 seam facts, derived from the frozen S7_LESSONS in the
#: brainstem (slug -> kind + the exact canonical statement + essence
#: + the line crosswalk). P0/P3 read these.
_LESSON_META_S7 = {
    _slug: {"kind": _k, "statement": _phrase, "essence": _es, "source_lines": _l}
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S7_LESSONS.items()
}

#: The six S7 theorem facts (slug -> the exact canonical statement +
#: the sanctioned parts + the owning concept), derived from the
#: frozen S7_THEOREMS in the brainstem.
_THEOREM_META_S7 = {
    _slug: {
        "statement": _meta["statement"],
        "parts": tuple(_meta["parts"]),
        "concept": _meta["concept"],
    }
    for _slug, _meta in S7_THEOREMS.items()
}

#: The full sanctioned composition DAG (S6's six + S7's six), frozen
#: from the brainstem tables (P7).
_THEOREM_DAG = {
    **{s: tuple(m["parts"]) for s, m in S6_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S7_THEOREMS.items()},
}

_ANSWER_ = {
    "CONJ_OPEN": "open — believed, not known",
    "CONJ_FALSIFIED": "falsified by theorem:theorem-main — the tower beats its cap for infinitely many n",
    "CONJ_FALSIFIED_PROVEN": (
        "yes — it was falsified by theorem:theorem-main; the tower gives "
        "infinitely many n with the unit pairs at least n to the one plus delta"
    ),
    "GS_YES_9_6": "yes — four times r is 24, at most d squared, 81, so the test says infinite",
    "GRID_7_7": "84",
    "GSLACK_9_3": "four times the slack is 9 — positive: d plus c zero plus 3t stays below d squared over four for large d",
    "GSLACK_9_7": (
        "four times the slack is 39 below zero — twelve times t (84) is above d squared minus "
        "four times d (45): no slack at this size, the comparison says the cap is not beaten"
    ),
    "SHOWDISPROOF": (
        "from the conjecture the disproof runs: the infinite tower, the split primes and the "
        "positive margin are established (the tower supplies the levels the criterion assumes), "
        "the geometric criterion turns the margin into the power above one for infinitely many "
        "n, and the erdosguess is falsified by the main theorem — every link is in my store"
    ),
    "FLIP": (
        "falsified — the erdosguess's cap is beaten for infinitely many n by "
        "theorem:theorem-main; the store now holds the disproof"
    ),
    "CONF_FLATAREA": "no — the flat unit ball fact is about a different norm, not the euclidean plane; it does not touch the erdosguess",
    "CONF_CONVEXNORM": (
        "no — the strictly convex norm fact refines a different norm's problem and is an upper "
        "bound, not a construction; it does not touch the erdosguess"
    ),
    "POWER_THIRD": (
        "yes — i have put it together: the tower supplies the levels, the split primes, the "
        "class bound and the positive margin, so the geometric criterion gives infinitely many "
        "n for which the unit pairs are at least n to the one plus delta; the erdosguess is "
        "falsified by the theorem in my store"
    ),
}

GAP_ARTICULATION = "not a capability i have been taught"

#: P4 — the per-wall articulations (frozen from control #1): every wall
#: must carry its exact honest phrases (the W-S7 ledger rows).
WALL_ARTICULATIONS: dict[str, tuple[str, ...]] = {
    "S03:12": ("past my line",),  # W-S7-1 (100 and 84 are checked separately)
    "S03:13": ("the proof of", "not in my store"),  # W-S7-6 (the declared-lemma proof wall)
    "S04:25": ("different problem", "not been taught"),  # W-S7-7 (distdist: beyond store)
    "S04:26": ("not in my store",),  # W-S7-7 (delta: the slack primitive's scope)
    "S04:27": ("not one instance number",),  # W-S6-5 persists (no concrete n)
}


def _st7(slug: str) -> str:
    return _LESSON_META_S7[slug]["statement"]


def _th7(slug: str) -> str:
    return _THEOREM_META_S7[slug]["statement"]


def _whychain7(slug: str) -> str:
    meta = _THEOREM_META_S7[slug]
    return f"i derived it from {', '.join(meta['parts'])}: {meta['statement']}"


def _pre_lemma(slug: str) -> str:
    """The byte-frozen S4/S5/S6 seam statement owning `slug` (the blind
    reprobe answers, P3/P6)."""

    for lessons in (S4_LESSONS, S5_LESSONS, S6_LESSONS):
        for _phrase, (_c, _s, _k, _es, _d, _l) in lessons.items():
            if _s == slug:
                return _phrase
    raise KeyError(slug)  # pragma: no cover


def _pre_theorem(slug: str) -> str:
    """The byte-frozen S6 theorem statement (the blind reprobe answer)."""

    return S6_THEOREMS[slug]["statement"]


#: The seven NEW declared seam lemmas (frozen; P3 checks every one is
#: ESTABLISHED declared-source in the final store, byte-equal).
S7_SEAM_FROZEN = {slug: meta for slug, meta in _LESSON_META_S7.items()}

#: The six NEW theorem facts (frozen; P3 checks every one DERIVED with
#: exactly the sanctioned parts).
S7_THEOREM_FROZEN = {slug: meta for slug, meta in _THEOREM_META_S7.items()}

#: The seventeen NEW prereq edges (frozen curriculum data).
S7_PREREQ_EDGES = [
    "curriculum:prereq:tower-base>cyclotomic-cubic",
    "curriculum:prereq:tower-base>char-cutout",
    "curriculum:prereq:tower-group>tower-base",
    "curriculum:prereq:tower-group>frattini",
    "curriculum:prereq:tower-group>golod-shaf",
    "curriculum:prereq:tower-group>shafarevich",
    "curriculum:prereq:tower-primes>tower-base",
    "curriculum:prereq:tower-primes>chebotarev",
    "curriculum:prereq:tower-primes>mod4-split",
    "curriculum:prereq:tower-class>tower-base",
    "curriculum:prereq:tower-class>class-bound",
    "curriculum:prereq:tower-class>adjoin-i",
    "curriculum:prereq:tower-class>slack-margins",
    "curriculum:prereq:disproof>criterion-chain",
    "curriculum:prereq:disproof>tower-group",
    "curriculum:prereq:disproof>tower-primes",
    "curriculum:prereq:disproof>tower-class",
]

#: The 35 NEW fact ids (7 seam + 6 theorems + 5 registries + 17
#: prereq edges) — all deterministic, frozen NOW.
S7_NEW_FACT_IDS = (
    [f"lemma:{s}" for s in S7_SEAM_FROZEN]
    + [f"theorem:{s}" for s in S7_THEOREM_FROZEN]
    + ["curriculum:tower-base", "curriculum:tower-group", "curriculum:tower-primes", "curriculum:tower-class", "curriculum:disproof"]
    + S7_PREREQ_EDGES
)

#: The five NEW S7 concepts (frozen by name).
S7_CONCEPT_IDS = ("tower-base", "tower-group", "tower-primes", "tower-class", "disproof")

FROZEN: dict[str, Any] = {
    # P8 — the seed (the official e6.10 S6 final store).
    "seed": str(E610_SEED),
    "seed_total": 734,
    "total_turns": 75,
    "line_end_final": 84,  # the line STAYS 0..84 (zero new successor facts)
    # P2 — the typed honesty turns.
    "pre_teach_gaps": {
        "S02:01": "tower-base",
        "S02:12": "tower-primes",
        "S02:20": "tower-class",
    },
    "scaffold_failures": {
        "S02:04": "gen-lower: missing tower-unramified",
        "S02:15": "gs-infinite: missing k-3t and slack-quadratic",
        "S03:01": "gamma-achieved: missing class-tower",
    },
    "derive_successes": {
        "S02:07": "gen-lower",
        "S02:23": "gs-infinite",
        "S03:04": "gamma-achieved",
        "S03:07": "splitting",
        "S04:01": "tower-feeds",
        "S04:04": "theorem-main",
    },
    "flip_turn": "S04:07",
    # P4/P5 — the conj-state probes (evidence carries the conj id).
    "conj_status_open": ("S03:10", "S03:18"),
    "conj_status_falsified": ("S04:08", "S04:29"),
    "conj_status_falsified_proven": ("S04:09",),
    "conj_evidence_refs": ("S03:10", "S03:18", "S04:07", "S04:08", "S04:09", "S04:29"),
    # P3 — the why-split refs (mechanical).
    "why_chains": {
        "S02:09": "gen-lower",
        "S02:25": "gs-infinite",
        "S03:06": "gamma-achieved",
        "S03:09": "splitting",
        "S03:14": "gs-infinite",
        "S04:03": "tower-feeds",
        "S04:06": "theorem-main",
    },
    "why_walls": {
        "S03:13": "tower-unramified (the declared-lemma proof wall, W-S7-6)",
    },
    # P4 — the beds exact (the line stays 0..84).
    "beds_exact": {
        "S02:18": _ANSWER_["GSLACK_9_3"],
        "S02:19": _ANSWER_["GSLACK_9_7"],
        "S03:11": _ANSWER_["GS_YES_9_6"],
        "S03:19": _ANSWER_["GRID_7_7"],
    },
    "bed_owners": {
        "S02:18": "lemma:gstest",
        "S02:19": "lemma:gstest",
        "S03:11": "lemma:gstest",
        "S03:19": "lemma:griddiag",
    },
    "walls_honest": {
        "S03:12": "gsslack 10x3: d squared = 100 is off the 0..84 line (W-S7-1; names 100 and 84)",
        "S03:13": "the tower-unramified proof wall (W-S7-6)",
        "S04:25": "distinct distances (W-S7-7: beyond store)",
        "S04:26": "delta value (W-S7-7: the slack primitive's scope)",
        "S04:27": "show-one (W-S6-5 persists: no concrete n in the store)",
    },
    "power_third_turn": "S04:28",
    "power_third_grounded": ("theorem:theorem-main", "theorem:tower-feeds"),
    # P4 — the pre-chain state anchors (the band-stable arc).
    "band_end_probes": {
        "S04:02": _th7("tower-feeds"),
        "S04:03": _whychain7("tower-feeds"),
        "S04:05": _th7("theorem-main"),
        "S04:06": _whychain7("theorem-main"),
        "S04:08": _ANSWER_["CONJ_FALSIFIED"],
        "S04:09": _ANSWER_["CONJ_FALSIFIED_PROVEN"],
        "S04:10": _ANSWER_["SHOWDISPROOF"],
        "S04:11": _th7("tower-feeds"),
        "S04:12": _th7("gamma-achieved"),
        "S04:13": _th7("gs-infinite"),
        "S04:14": _th7("gen-lower"),
        "S04:15": _th7("splitting"),
        "S04:16": _st7("tower-base"),
        "S04:17": _st7("base-rd"),
        "S04:18": _st7("class-tower"),
        "S04:19": _st7("slack-quadratic"),
        "S04:20": _st7("chebotarev-selection"),
        "S04:21": _st7("k-3t"),
        "S04:22": _st7("tower-unramified"),
        "S04:23": _ANSWER_["CONF_FLATAREA"],
        "S04:24": _ANSWER_["CONF_CONVEXNORM"],
        "S04:28": _ANSWER_["POWER_THIRD"],
        "S04:29": _ANSWER_["CONJ_FALSIFIED"],
        "S04:30": _th7("theorem-main"),
    },
    # P3 — the derived table (every state/why/bed/status answer exact).
    "derived_table": {
        "S02:03": _st7("tower-base"),
        "S02:06": _st7("tower-unramified"),
        "S02:08": _th7("gen-lower"),
        "S02:09": _whychain7("gen-lower"),
        "S02:11": _st7("base-rd"),
        "S02:14": _st7("chebotarev-selection"),
        "S02:17": _st7("k-3t"),
        "S02:18": _ANSWER_["GSLACK_9_3"],
        "S02:19": _ANSWER_["GSLACK_9_7"],
        "S02:22": _st7("slack-quadratic"),
        "S02:24": _th7("gs-infinite"),
        "S02:25": _whychain7("gs-infinite"),
        "S03:03": _st7("class-tower"),
        "S03:05": _th7("gamma-achieved"),
        "S03:06": _whychain7("gamma-achieved"),
        "S03:08": _th7("splitting"),
        "S03:09": _whychain7("splitting"),
        "S03:10": _ANSWER_["CONJ_OPEN"],
        "S03:11": _ANSWER_["GS_YES_9_6"],
        "S03:14": _whychain7("gs-infinite"),
        "S03:15": _pre_lemma("cyclotomic"),
        "S03:16": _pre_lemma("classbound"),
        "S03:17": _pre_theorem("infinity-end"),
        "S03:18": _ANSWER_["CONJ_OPEN"],
        "S03:19": _ANSWER_["GRID_7_7"],
        "S03:20": _st7("base-rd"),
        "S04:02": _th7("tower-feeds"),
        "S04:03": _whychain7("tower-feeds"),
        "S04:05": _th7("theorem-main"),
        "S04:06": _whychain7("theorem-main"),
        "S04:08": _ANSWER_["CONJ_FALSIFIED"],
        "S04:09": _ANSWER_["CONJ_FALSIFIED_PROVEN"],
        "S04:10": _ANSWER_["SHOWDISPROOF"],
        "S04:11": _th7("tower-feeds"),
        "S04:12": _th7("gamma-achieved"),
        "S04:13": _th7("gs-infinite"),
        "S04:14": _th7("gen-lower"),
        "S04:15": _th7("splitting"),
        "S04:16": _st7("tower-base"),
        "S04:17": _st7("base-rd"),
        "S04:18": _st7("class-tower"),
        "S04:19": _st7("slack-quadratic"),
        "S04:20": _st7("chebotarev-selection"),
        "S04:21": _st7("k-3t"),
        "S04:22": _st7("tower-unramified"),
        "S04:23": _ANSWER_["CONF_FLATAREA"],
        "S04:24": _ANSWER_["CONF_CONVEXNORM"],
        "S04:28": _ANSWER_["POWER_THIRD"],
        "S04:29": _ANSWER_["CONJ_FALSIFIED"],
        "S04:30": _th7("theorem-main"),
    },
    # P5 — the theorem ids may appear in `grounded` ONLY on the
    # frozen allow-set refs (the state turns, the why-chains that cite
    # theorem parts, the Stage B reconstruction, the third-state power
    # probe).
    "theorem_allowed": {
        "S02:08": ("gen-lower",),
        "S02:24": ("gs-infinite",),
        "S03:05": ("gamma-achieved",),
        "S03:07": ("gs-infinite",),  # the derive of splitting grounds on its own parts (the chain, not an independent line)
        "S03:08": ("splitting",),
        "S03:09": ("gs-infinite",),
        "S03:17": ("infinity-end",),
        "S04:01": ("gs-infinite", "splitting", "gamma-achieved"),  # the derive of tower-feeds (M6)
        "S04:02": ("tower-feeds",),
        "S04:03": ("gs-infinite", "splitting", "gamma-achieved"),  # the why-chain of tower-feeds
        "S04:04": ("tower-feeds", "infinity-end"),  # the derive of theorem-main (M7)
        "S04:05": ("theorem-main",),
        "S04:06": ("tower-feeds", "infinity-end"),
        "S04:10": ("gs-infinite", "splitting", "gamma-achieved", "tower-feeds", "infinity-end", "theorem-main"),
        "S04:11": ("tower-feeds",),
        "S04:12": ("gamma-achieved",),
        "S04:13": ("gs-infinite",),
        "S04:14": ("gen-lower",),
        "S04:15": ("splitting",),
        "S04:28": ("theorem-main", "tower-feeds"),
        "S04:30": ("theorem-main",),
    },
    # P7 — the Stage B evidence (the M-chain, ordered) and the
    # full sanctioned DAG (S6's six + S7's six).
    "showdisproof_evidence": (
        "theorem:gs-infinite",
        "theorem:splitting",
        "theorem:gamma-achieved",
        "theorem:tower-feeds",
        "theorem:infinity-end",
        "theorem:theorem-main",
    ),
    "theorem_dag": _THEOREM_DAG,
    "showdisproof_ref": "S04:10",
    # P7 — the one-line-two-beds cross-check (the shared 81 cs fact).
    "bed_crosscheck": {
        "slack_ref": "S02:18",
        "gsay_ref": "S03:11",
        "num": 81,
    },
    "prereq_edges": S7_PREREQ_EDGES,
    "new_fact_ids": S7_NEW_FACT_IDS,
    "total_seam_facts": 55,  # 43 declared (10 S4 + 16 S5 + 10 S6 + 7 S7) + 12 theorems
    # P2 — the frozen domain sequences (letters: L lesson,
    # U pre-lesson gap, F scaffold-failure, T derive-success,
    # S derived, H honest wall, C conditional, Ff flip-success).
    # S2 is the pre-reg's VERIFIED string (letter-for-letter against
    # the per-turn script). S3/S4 are FROZEN FROM CONTROL #1 and
    # written once to /tmp/s7-domains.txt (house policy 2026-08-23).
    "domain_sequence": {
        2: "ULSFLSTSSLSULSFLSSSULSTSS",
        3: "FLSTSSTSSSSHHSSSSSSS",
        4: "TSSTSSFfSSSSSSSSSSSSSSSSSHHHSSS",
    },
    # P8 — store totals (FROZEN FROM CONTROL #1; the event ids that
    # collide with seed coordinates dedupe silently — the D-e6w
    # pattern; freeze the ACTUAL total, never the hand count).
    "final_total": 840,  # control #1: 734 + 35 facts + 71 events (one event-id collision with the S5 seed, see the ledger)
    "new_facts": len(S7_NEW_FACT_IDS),  # 35 (frozen NOW — all deterministic)
    "new_events": 71,  # control #1 (the D-e6w pattern: ids colliding with seed coordinates dedupe)
    # P8 — mastery of the FIVE S7 concepts (FROZEN FROM CONTROL #1).
    # HONEST PREG READ (W-S7-8): the S5 gap cascade spans into S7 —
    # the five new concepts are EXPECTED to end practicing (every
    # prereq in the new band is itself practicing → the gate).
    "mastery_expected": {
        "tower-base": {"state": "practicing", "correct": 7},
        "tower-group": {"state": "practicing", "correct": 11},
        "tower-primes": {"state": "practicing", "correct": 8},
        "tower-class": {"state": "practicing", "correct": 8},
        "disproof": {"state": "practicing", "correct": 10},
    },
    "expected_prereq_gaps": {
        "tower-base": ("char-cutout", "cyclotomic-cubic"),
        "tower-group": ("frattini", "golod-shaf", "shafarevich", "tower-base"),
        "tower-primes": ("chebotarev", "mod4-split", "tower-base"),
        "tower-class": ("adjoin-i", "class-bound", "slack-margins", "tower-base"),
        "disproof": ("criterion-chain", "tower-class", "tower-group", "tower-primes"),
    },
    # P8 — the pre-S7 states that must NOT change (FROZEN FROM
    # CONTROL #1: exact (state, correct) for every pre-S7 concept —
    # the S7 script cites pre-S7 seam facts as parts and re-drills a
    # few of their concepts (the blind reprobes), which moves THEIR
    # correct counters but not their states).
    "pre_s7_states": {
        "add-two-digit": {"state": "stable", "correct": 11},
        "add-within-10": {"state": "stable", "correct": 5},
        "adjoin-i": {"state": "practicing", "correct": 1},
        "alg-inverse-1step": {"state": "stable", "correct": 5},
        "alg-inverse-mul": {"state": "stable", "correct": 5},
        "alg-two-step": {"state": "stable", "correct": 4},
        "averaging": {"state": "practicing", "correct": 4},
        "char-cutout": {"state": "practicing", "correct": 2},
        "chebotarev": {"state": "practicing", "correct": 2},
        "circle-pair-2": {"state": "stable", "correct": 4},
        "class-bound": {"state": "practicing", "correct": 4},
        "cm-conj": {"state": "practicing", "correct": 4},
        "compare-numbers": {"state": "stable", "correct": 11},
        "count-successor": {"state": "stable", "correct": 12},
        "criterion-chain": {"state": "practicing", "correct": 10},
        "cyclotomic-cubic": {"state": "practicing", "correct": 3},
        "disc-rd": {"state": "practicing", "correct": 1},
        "erdos-conj": {"state": "stable", "correct": 10},
        "frattini": {"state": "practicing", "correct": 1},
        "gaussian-int": {"state": "stable", "correct": 7},
        "geom-area": {"state": "stable", "correct": 6},
        "geom-area-triangle": {"state": "stable", "correct": 4},
        "geom-perimeter": {"state": "stable", "correct": 5},
        "golod-shaf": {"state": "practicing", "correct": 6},
        "grid-lattice": {"state": "stable", "correct": 10},
        "hajir-maire": {"state": "practicing", "correct": 1},
        "kin-distance": {"state": "stable", "correct": 4},
        "kin-position": {"state": "stable", "correct": 6},
        "kin-rate": {"state": "stable", "correct": 4},
        "kin-solve-time": {"state": "stable", "correct": 4},
        "kst-bound": {"state": "stable", "correct": 4},
        "minkowski-embed": {"state": "practicing", "correct": 1},
        "mod4-split": {"state": "practicing", "correct": 9},
        "mult-within-100": {"state": "stable", "correct": 9},
        "norm-convex": {"state": "stable", "correct": 5},
        "norm-flat": {"state": "stable", "correct": 5},
        "norm-generic": {"state": "stable", "correct": 4},
        "number-field": {"state": "practicing", "correct": 2},
        "packing": {"state": "practicing", "correct": 6},
        "phrasology": {"state": "stable", "correct": 24},
        "pnt-ap": {"state": "practicing", "correct": 2},
        "prime-split": {"state": "practicing", "correct": 1},
        "projection": {"state": "practicing", "correct": 4},
        "shafarevich": {"state": "practicing", "correct": 2},
        "shape-circle": {"state": "stable", "correct": 6},
        "shape-rectangle": {"state": "stable", "correct": 4},
        "shape-square": {"state": "stable", "correct": 5},
        "shape-triangle": {"state": "stable", "correct": 6},
        "slack-margins": {"state": "practicing", "correct": 1},
        "sst-bound": {"state": "stable", "correct": 4},
        "stat-balance": {"state": "stable", "correct": 6},
        "stat-moment": {"state": "stable", "correct": 4},
        "stat-net-1d": {"state": "stable", "correct": 4},
        "sub-within-30": {"state": "stable", "correct": 12},
        "unit-distance": {"state": "stable", "correct": 5},
        "window-setup": {"state": "practicing", "correct": 1},
    },
    "script": {
        2: [
            "state the tower-base rule",
            _st7("tower-base"),
            "state the tower-base rule",
            "derive gen-lower from tower-unramified and fratin",
            _st7("tower-unramified"),
            "state the tower-unramified rule",
            "derive gen-lower from tower-unramified and fratin",
            "state the gen-lower rule",
            "explain why the gen-lower holds",
            _st7("base-rd"),
            "state the base-rd rule",
            "state the chebotarev-selection rule",
            _st7("chebotarev-selection"),
            "state the chebotarev-selection rule",
            "derive gs-infinite from shafbound, fratin, k-3t, gstest and slack-quadratic",
            _st7("k-3t"),
            "state the k-3t rule",
            "what is the gs slack for 9 generators and 3 split primes?",
            "what is the gs slack for 9 generators and 7 split primes?",
            "state the slack-quadratic rule",
            _st7("slack-quadratic"),
            "state the slack-quadratic rule",
            "derive gs-infinite from shafbound, fratin, k-3t, gstest and slack-quadratic",
            "state the gs-infinite rule",
            "explain why the gs-infinite holds",
        ],
        3: [
            "derive gamma-achieved from class-tower, chebotarev-selection, slack-quadratic and gamma-positive",
            _st7("class-tower"),
            "state the class-tower rule",
            "derive gamma-achieved from class-tower, chebotarev-selection, slack-quadratic and gamma-positive",
            "state the gamma-achieved rule",
            "explain why the gamma-achieved holds",
            "derive splitting from gs-infinite and chebotarev-selection",
            "state the splitting rule",
            "explain why the splitting holds",
            "what is the status of the erdosguess?",
            "does the gs test say infinite for 9 generators and 6 relations?",
            "what is the gs slack for 10 generators and 3 split primes?",
            "explain why the tower-unramified holds",
            "explain why the gs-infinite holds",
            "state the cyclotomic rule",
            "state the classbound rule",
            "state the infinity-end rule",
            "what is the status of the erdosguess?",
            "how many unit pairs does the 7 by 7 grid have?",
            "state the base-rd rule",
        ],
        4: [
            "derive tower-feeds from gs-infinite, splitting, class-tower, gamma-achieved, hypo-infinity and gamma-positive",
            "state the tower-feeds rule",
            "explain why the tower-feeds holds",
            "derive theorem-main from tower-feeds and infinity-end",
            "state the theorem-main rule",
            "explain why the theorem-main holds",
            "falsify the erdosguess by theorem-main",
            "what is the status of the erdosguess?",
            "is the erdosguess proven?",
            "reconstruct the disproof from the erdosguess",
            "state the tower-feeds rule",
            "state the gamma-achieved rule",
            "state the gs-infinite rule",
            "state the gen-lower rule",
            "state the splitting rule",
            "state the tower-base rule",
            "state the base-rd rule",
            "state the class-tower rule",
            "state the slack-quadratic rule",
            "state the chebotarev-selection rule",
            "state the k-3t rule",
            "state the tower-unramified rule",
            "does the flatarea rule disprove the erdosguess?",
            "does the convexnorm route construct more unit distances in the euclidean plane?",
            "what is the tight bound for distinct distances in the plane?",
            "what is the exact value of delta?",
            "name a concrete n for which the unit pairs exceed n to the 1 plus delta",
            "can you prove that for infinitely many n the unit pairs grow to a power above one?",
            "what is the status of the erdosguess?",
            "state the theorem-main rule",
        ],
    },
}

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

#: the seven S7 lesson phrases (frozen) must appear IN the script,
#: byte-exact (the literal script turns are the canonical bytes)
for _phrase in S7_LESSONS:
    assert any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"the S7 lesson phrase is not verbatim in the frozen script: {_phrase[:60]}..."
    )

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict
#: (the sentinels are replaced by control #1, evidence in /tmp).
_UNFROZEN = (
    (FROZEN["domain_sequence"].get(3) or "").startswith("##FREEZE")
    or (FROZEN["domain_sequence"].get(4) or "").startswith("##FREEZE")
    or str(FROZEN["final_total"]).startswith("##FREEZE")
    or str(FROZEN["new_events"]).startswith("##FREEZE")
    or str(FROZEN["mastery_expected"]).startswith("##FREEZE")
    or str(FROZEN["expected_prereq_gaps"]).startswith("##FREEZE")
    or str(FROZEN["pre_s7_states"]).startswith("##FREEZE")
)


def _line_end(store) -> int:
    """The current line end = the largest successor fact v+1 in the
    store (the e6.8 machinery, unchanged by S7)."""

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
    """Every ACTIVE successor object num(n) in the store (P8: the line
    must be EXACTLY 0..84 — zero new successor facts, zero kills)."""

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
    failure, T derive-success, Ff conjecture-flip success, C
    conditional-derivation answer, H honest needs_info wall, S
    derived. Pure function of the turn record."""

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
    if mode == "conj-flip":
        return "Ff"
    if ir.get("uncertainty_state") == "needs_info":
        return "H"
    if ir.get("uncertainty_state") == "conditional":
        return "C"
    return "S"


def _run_once(root: Path) -> list[dict]:
    """Run S2–S4 once under `root` (the seed must already be at
    codeX-S01.json of `root`)."""

    reset_concepts()
    rt = InfantRuntime(root, concepts=CONCEPTS_E611)
    out: list[dict] = []
    for s in (2, 3, 4):
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.10 S6 store, id-for-id."""

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


def _reports(runs: dict) -> dict:
    """The machine-readable run report (per-turn, per-session)."""

    turns: dict[str, dict] = {}
    for srow in runs["e6.11-run1"]:
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
        "seam_facts": {slug: {"statement": meta["statement"]} for slug, meta in S7_SEAM_FROZEN.items()},
        "theorem_facts": {slug: {"statement": meta["statement"]} for slug, meta in S7_THEOREM_FROZEN.items()},
    }


def run_e6_11(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.10 S6 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {"error": "S7 frozen constants are not yet frozen (control #1 must replace the ##FREEZE## sentinels; see the E6.11 pre-reg open points)"}
    runs: dict[str, list[dict]] = {}
    for name in ("e6.11-run1", "e6.11-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.10 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — with the S7
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E611}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.11-run1", "e6.11-run2"):
        (out_dir / name / "e6.11-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.11.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict[str, list[dict]], report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.11-run1"
    final = _fresh_store(run1_root, 4)

    # P0 — the paper NEVER reached the student: the S7 denylist (34
    # terms) over EVERY script turn, every turn's actual response
    # (the new grammar articulations included), the forty-three
    # declared seam statements, and the twelve theorem statements.
    p0_bad: list[str] = []
    surfaces: list[str] = []
    for s, script in sorted(FROZEN["script"].items()):
        surfaces.extend(script)
    for ref, t in sorted(turns.items()):
        surfaces.append(str(t.get("response_text") or ""))
        ir = t.get("response_ir") or {}
        surfaces.append(str(ir.get("answer") or ""))
    for lessons in (S4_LESSONS, S5_LESSONS, S6_LESSONS, S7_LESSONS):
        for _phrase in lessons:
            surfaces.append(_phrase)  # noqa: PERF402  # _phrase is a str key, not a list
    for theorems in (S6_THEOREMS, S7_THEOREMS):
        for meta in theorems.values():
            surfaces.append(meta["statement"])
    for term in S7_DENYLIST:
        for surface in surfaces:
            if term in surface:
                p0_bad.append(f"banned paper text in a surface: {term!r}")
                break
    for slug, meta in S7_SEAM_FROZEN.items():
        if not meta["source_lines"]:
            p0_bad.append(f"{slug}: the canonical statement has no line crosswalk")
    checks["p0_no_paper_text"] = {"pass": not p0_bad, "bad": p0_bad}

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
    # failures (F), derive-success (T), the flip (Ff), and the
    # frozen interleave
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
    t = turns.get(FROZEN["flip_turn"])
    if t is None:
        p2_bad.append("missing the flip turn")
    else:
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p2_bad.append(f"{FROZEN['flip_turn']}: the flip is not a derived state change ({ir.get('uncertainty_state')})")
        if not any("conjecture:erdosguess" in str(x) for x in ir.get("evidence") or []):
            p2_bad.append(f"{FROZEN['flip_turn']}: the conjecture is not in the flip's evidence")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S7 adds ZERO successor facts)")
    checks["p2_typed_honesty_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — the SEAM + the THEOREMS: 55 seam-family facts (43 declared
    # + 12 derived), ALL S7 statements byte-equal to the frozen
    # canonical statements, ALL pre-S7 seam facts byte-unchanged,
    # the S7 theorems DERIVED with evidence exactly the sanctioned
    # parts, the prereq edges established, every derived answer
    # exact + grounded, the why-split mechanical
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
    # the seven S7 seam facts
    for slug, meta in sorted(S7_SEAM_FROZEN.items()):
        found = False
        for a in final.query():
            if a.id != f"{meta['kind']}:{slug}":
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
    # the six S7 theorem facts (DERIVED provenance, exact parts)
    for slug, meta in sorted(S7_THEOREM_FROZEN.items()):
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
    # every pre-S7 seam fact: byte-exact (no drift)
    for _lessons, _label in ((S4_LESSONS, "S4"), (S5_LESSONS, "S5"), (S6_LESSONS, "S6")):
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
    # the WHY-SPLIT, mechanically: declared-lemma whydeep = the wall
    # (W-S7-6); theorem whydeep = the chain articulation
    for ref, slug in FROZEN["why_walls"].items():
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing {ref}")
            continue
        ans = str(_ir_answer(t) or "")
        if "the proof of" not in ans or "not in my store" not in ans:
            p3_bad.append(f"{ref}: the declared-lemma why-wall articulation is missing")
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

    # P4 — the beds + the walls + the flip + the third-state power
    # probe, EXACT
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
    t = turns.get("S03:12")  # W-S7-1: the gsslack off-line wall
    if t is None:
        p4_bad.append("missing the W-S7-1 wall")
    else:
        ans = str((t["response_ir"] or {}).get("answer", ""))
        if "100" not in ans or "84" not in ans:
            p4_bad.append("S03:12: the W-S7-1 wall must name 100 and the line end 84")
    for ref in FROZEN["conj_status_open"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        if _ir_answer(t) != FROZEN["derived_table"][ref]:
            p4_bad.append(f"{ref}: the pre-flip status probe must still say open")
    for ref in FROZEN["conj_status_falsified"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        if _ir_answer(t) != FROZEN["derived_table"][ref]:
            p4_bad.append(f"{ref}: the post-flip status probe is not exact")
    for ref in FROZEN["conj_status_falsified_proven"]:
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        if _ir_answer(t) != FROZEN["derived_table"][ref]:
            p4_bad.append(f"{ref}: the post-flip proven probe is not exact")
    # the flip: theorem:main in the evidence, grounded EMPTY
    t = turns.get(FROZEN["flip_turn"])
    if t is None:
        p4_bad.append("missing the flip")
    else:
        ir = t["response_ir"] or {}
        if not any("theorem:theorem-main" in str(x) for x in ir.get("evidence") or []):
            p4_bad.append(f"{FROZEN['flip_turn']}: the flip's evidence must carry theorem:theorem-main")
        if t["grounded"]:
            p4_bad.append(f"{FROZEN['flip_turn']}: the flip cited grounded premises (a status change is derived, never a premise)")
    # the third-state power probe (the visible-learning arc)
    t = turns.get(FROZEN["power_third_turn"])
    if t is None:
        p4_bad.append("missing the third-state power probe")
    else:
        ir = t["response_ir"] or {}
        if _ir_answer(t) != FROZEN["band_end_probes"][FROZEN["power_third_turn"]]:
            p4_bad.append(f"{FROZEN['power_third_turn']}: the third-state power probe is not exact")
        if ir.get("uncertainty_state") != "derived":
            p4_bad.append(f"{FROZEN['power_third_turn']}: the third state is not an unconditional derivation")
        if tuple(str(x) for x in t["grounded"]) != FROZEN["power_third_grounded"]:
            p4_bad.append(f"{FROZEN['power_third_turn']}: the power probe must ground on theorem-main + tower-feeds exactly")
    checks["p4_beds_walls_flip"] = {"pass": not p4_bad, "bad": p4_bad, "bed_refs": len(FROZEN["beds_exact"])}

    # P5 — the SEAM invariance + the conjecture: the erdosguess fact
    # id in ZERO `grounded` lists (a status surface, never a premise);
    # the line beds ground ONLY on line facts + their owning seam
    # fact; the Stage B turn grounds on the cited theorem ids ONLY;
    # no theorem is a premise of an independent line derivation
    p5_bad: list[str] = []
    CONJ = "conjecture:erdosguess"
    for ref, t in sorted(turns.items()):
        if any(CONJ in str(x) for x in t["grounded"]):
            p5_bad.append(f"{ref}: the conjecture was cited as a derivation premise")
    for ref in FROZEN["conj_evidence_refs"]:
        if t := turns.get(ref):
            ev = (t["response_ir"] or {}).get("evidence") or []
            if not any(CONJ in str(x) for x in ev):
                p5_bad.append(f"{ref}: the status/flip probe lost its conjecture evidence")
    for ref, owner in FROZEN["bed_owners"].items():
        t = turns.get(ref)
        if t is None:
            p5_bad.append(f"missing bed {ref}")
            continue
        for g in t["grounded"]:
            g = str(g)
            if not (g.startswith("cs-") or g == owner):
                p5_bad.append(f"{ref}: the line bed cited a non-line fact {g} (allowed: line facts + the owning seam fact)")
        if owner not in [str(x) for x in t["grounded"]]:
            p5_bad.append(f"{ref}: the line bed did not cite its owning seam fact")
    t = turns.get(FROZEN["showdisproof_ref"])
    if t is None:
        p5_bad.append("missing the Stage B reconstruction")
    else:
        if tuple(str(x) for x in t["grounded"]) != FROZEN["showdisproof_evidence"]:
            p5_bad.append(f"{FROZEN['showdisproof_ref']}: the Stage B turn must ground on the cited theorem ids ONLY, ordered")
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

    # P6 — the band-end table (Stage A/B + confounders + the flip +
    # the third-state power probe), exact
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

    # P7 — the cross-checks + the inspectable DAG: the Stage B
    # evidence reproduces the M-chain; re-computing the derivation
    # DAG from ALL twelve theorem facts (S6 + S7) reproduces the
    # sanctioned composition DAG exactly; every theorem's evidence
    # list ⊆ store ids; the one-line-two-beds check (gsslack (9,3)
    # and gsay (9,6) share the 81 cs fact — d² = 81: 4·6 = 24 ≤ 81;
    # 81 − 4·9 − 12·3 = 9)
    p7_bad: list[str] = []
    t = turns.get(FROZEN["showdisproof_ref"])
    if t is None:
        p7_bad.append("missing the Stage B ref")
    else:
        ev = tuple(str(x) for x in (t["response_ir"] or {}).get("evidence") or [])
        if ev != FROZEN["showdisproof_evidence"]:
            p7_bad.append(f"{FROZEN['showdisproof_ref']}: the Stage B EVIDENCE {ev} != the frozen M-chain")
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
    fact81 = None
    for a in final.query(context_match={"kind": "fact", "concept": "count-successor"}):
        if a.object_id == f"count-successor:num({bc['num']})":
            fact81 = a
            break
    ts = turns.get(bc["slack_ref"])
    tg = turns.get(bc["gsay_ref"])
    if fact81 is None:
        p7_bad.append(f"count-successor:num({bc['num']}): the shared successor fact is not in the final store")
    elif ts is None or tg is None:
        p7_bad.append("missing a bed ref in the cross-check")
    else:
        if fact81.id not in [str(x) for x in ts["grounded"]]:
            p7_bad.append(f"{bc['slack_ref']}: the gs-slack bed did not cite the shared {bc['num']} successor fact")
        if fact81.id not in [str(x) for x in tg["grounded"]]:
            p7_bad.append(f"{bc['gsay_ref']}: the gsay bed did not cite the shared {bc['num']} successor fact")
    checks["p7_crosscheck_dag"] = {"pass": not p7_bad, "bad": p7_bad}

    # P8 — mastery, store integrity, determinism
    p8_bad: list[str] = []
    seed = _seed_check(run1_root)
    if seed["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed['seed_total']} != {FROZEN['seed_total']}")
    if seed["reproduced_in_s2_pre"] != FROZEN["seed_total"] or seed["missing"]:
        p8_bad.append(f"seed continuity: {seed}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']} (S7 adds ZERO successor facts)")
    # the line is EXACTLY 0..84: zero new successor objects of any kind
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
    # the ONE conjecture upsert (net zero new assertions, a content
    # change on the existing id)
    try:
        conj = final.get(CONJ)
    except KeyError:
        conj = None
    if conj is None:
        p8_bad.append("the erdosguess fact is gone from the final store")
    else:
        if conj.context.data.get("conjecture_status") != "falsified":
            p8_bad.append(f"the erdosguess status {conj.context.data.get('conjecture_status')!r} != falsified")
        if conj.context.data.get("by") != "theorem:theorem-main":
            p8_bad.append(f"the erdosguess by {conj.context.data.get('by')!r} != theorem:theorem-main")
        if conj.provenance is None or conj.provenance.derived is not True or conj.provenance.observer != "infant":
            p8_bad.append("the flipped conjecture is not a derived infant assertion")
        ev = [str(x) for x in (conj.provenance.evidence if conj.provenance else [])]
        if ev != ["theorem:theorem-main", CONJ]:
            p8_bad.append(f"the flipped conjecture evidence {ev} != [theorem:theorem-main, the conj id]")
    mv = mastery_view(final, [c.id for c in CONCEPTS_E611])
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
    for cid, exp in FROZEN["pre_s7_states"].items():
        v = mv.get(cid)
        if v is None:
            p8_bad.append(f"{cid}: a pre-S7 concept left the mastery view")
            continue
        if v.state != exp["state"]:
            p8_bad.append(f"{cid}: pre-S7 state CHANGED ({v.state} != {exp['state']}) — W-S7-8 measures this")
        if v.correct_derivations != exp["correct"]:
            p8_bad.append(f"{cid}: pre-S7 correct derivations {v.correct_derivations} != frozen {exp['correct']}")
    # determinism
    r1 = runs["e6.11-run1"]
    r2 = runs["e6.11-run2"]
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
            for cid in S7_CONCEPT_IDS
            if cid in mv
        },
        "seed": seed,
        "line_end": _line_end(final),
        "successor_objects": sorted(_successor_objects(final)),
        "final_total": len(all_final),
        "new_facts": [a2.id for a2 in new_facts],
        "new_events": len(new_events),
        "run_identity": hashlib.sha256(a.encode("utf-8")).hexdigest()[:16],
    }
    passed = sum(1 for c in checks.values() if c["pass"])
    value = f"PASS e6.11: {passed}/{len(checks)}" if passed == len(checks) else f"FAIL e6.11: {passed}/{len(checks)}"
    return {"checks": checks, "passed": passed, "value": value}


class E6_11Experiment:
    """E6.11 — S7 of the SAVANT-TRACK: the arithmetical half
    "tower ⇒ disproof" (the savant test proper)."""

    name = "e6.11"
    hypothesis = (
        "The arithmetical half band (S7) stores the tower construction NOT as "
        "lessons about the conclusion but as DERIVATIONS from taught parts: the "
        "seven tower seam lemmas are ESTABLISHED declared-source facts (43 "
        "declared seam facts with S4's ten, S5's sixteen, and S6's ten); the "
        "SIX scaffolded derive turns store the S6 theorems' chain APPLIED: "
        "gen-lower, gs-infinite, splitting, gamma-achieved, tower-feeds, and "
        "theorem-main (the paper's Theorem 1.1), each citing exactly its "
        "sanctioned parts (machine-inspectable in the store); the erdosguess "
        "flips open → falsified (by theorem:theorem-main) by an in-store "
        "derivation ALONE (the M8 upsert on the same id, derived provenance, "
        "zero new conjecture assertions); the same power probe that was the "
        "S4/S5 wall and the S6 conditional answers UNCONDITIONALLY here "
        "(grounded on theorem-main + the chain); no concrete violating n, "
        "delta value, or distinct-distance bound is in the store (honest "
        "beyond-store walls); the line stays 0..84 (zero new successor "
        "facts); the paper never reaches the student (P0); two runs "
        "byte-identical."
    )
    metric = "S7 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_11()
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
                Path("results/phase-6/e6.11-run1/session-S02.json"),
                Path("results/phase-6/e6.11-run1/session-S03.json"),
                Path("results/phase-6/e6.11-run1/session-S04.json"),
                Path("results/phase-6/e6.11-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
