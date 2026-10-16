# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.10 — S6 of the SAVANT-TRACK (pre-REGISTERED, frozen): the
geometric criterion band — scaffolded generation (THE LEAP).

The student is TAUGHT THE PARTS (ten more declared `lemma:{slug}`
seam facts: the norm-one count, the margins gamma-positive /
b-positive, the overlap / averaging / projection / packing facts, the
slack composition rule, the growing-degrees hypothesis) and then
SCAFFOLDED: frozen `derive` questions ask it to put the SIX
sanctioned compositions together into `theorem:{slug}` facts with
DERIVED provenance (evidence = the part fact ids; never
declared-source). The scaffold failures are honest and typed
(missing parts / no rule — zero fabrication); the beds ride the
extended 0..84 line (a declared substrate operation: 12 successor
facts, closing the S4 7×7 = 84 wall and putting the tower degrees
3, 9, 27, 81 on-line); the why-split is measured (declared lemmas
keep the S5 proof wall; derived theorems answer with the in-store
chain); and the SAME power-probe surface changes its honest answer
as the store learns (H before the chain, the conditional C
articulation after it — the erdosguess stays open; the flip is
S7's). The paper never reaches the student (P0 denylist scan).
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT6,
    S4_LESSONS,
    S5_LESSONS,
    S6_DENYLIST,
    S6_LESSONS,
    S6_THEOREMS,
)
from kainos.tutor.e69 import CONCEPTS_E69
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E610", "FROZEN", "E6_10Experiment", "run_e6_10"]

CHECKS = 9

#: The official e6.9 S5 store (the S6 seed: 636 assertions, line 72),
#: repo-relative.
E69_SEED = Path("results/phase-6/e6.9-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E69_SEED.exists():
        return E69_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E69_SEED
    return alt if alt.exists() else E69_SEED


#: E6.10 — the concept registry the band ends carrying: everything
#: the e6.9 band ends with, plus the six savant S6 concepts.
CONCEPTS_E610: tuple = CONCEPTS_E69 + CONCEPT_SAVANT6

#: The ten S6 seam facts, derived from the frozen S6_LESSONS in the
#: brainstem (slug -> kind + the exact canonical statement + essence
#: + the line crosswalk). P0/P3 read these.
_LESSON_META_S6 = {
    _slug: {"kind": _k, "statement": _phrase, "essence": _es, "source_lines": _l}
    for _phrase, (_c, _slug, _k, _es, _d, _l) in S6_LESSONS.items()
}

#: The six theorem facts (slug -> the exact canonical statement +
#: the sanctioned parts + the owning concept), derived from the
#: frozen S6_THEOREMS in the brainstem.
_THEOREM_META_S6 = {
    _slug: {
        "statement": _meta["statement"],
        "parts": tuple(_meta["parts"]),
        "concept": _meta["concept"],
    }
    for _slug, _meta in S6_THEOREMS.items()
}


_ANSWER_ = {
    "CONJ_OPEN": "open — believed, not known",
    "CONJ_PROVEN_NO": "no — the erdosguess is believed, not known; its status is open",
    "GRID_7_7": "84",
    "GRID_6_6": "60",
    "GRID_4_4": "24",
    "SQ_YES_2_5": "yes — 2 squared plus one is 1 times 5",
    "GS_YES_3_2": "yes — four times r is 8, at most d squared, 9, so the test says infinite",
    "TWOSQ_50": "3",
    "PACK_1": "16",
    "PACK_2": "64",
    "TRIPOW_4": "81",
}

GAP_ARTICULATION = "not a capability i have been taught"
CONDITIONAL_ARTICULATION = "conditionally i can"


def _st6(slug: str) -> str:
    return _LESSON_META_S6[slug]["statement"]


def _th(slug: str) -> str:
    return _THEOREM_META_S6[slug]["statement"]


def _whychain(slug: str) -> str:
    meta = _THEOREM_META_S6[slug]
    return f"i derived it from {', '.join(meta['parts'])}: {meta['statement']}"


FROZEN: dict[str, Any] = {
    "seed": str(E69_SEED),
    "seed_total": 636,
    "total_turns": 70,
    "line_end_final": 84,  # the declared substrate operation: 0..84
    # P8 — the frozen store decomposition (final = seed + new facts
    # + new mastery events). FROZEN FROM CONTROL #2 (D-e6w):
    # 45 new facts = 12 successor facts (73..84) + 10 S6 seam facts
    # + 6 concept registries + 11 prereq edges + 6 theorem facts;
    # 53 NEW events = 32 derivation-correct + 12 drill-unable ... no:
    # 32 derivation-correct + 11 drill-unable + 10 seam lesson
    # markers. D-e6w: the preg predicted 66 (12 line-lesson markers
    # + 12 drill-unable + 32 + 10); the event-id coordinates
    # (concept, session, turn, kind) COLLIDE with the seed's own
    # events (the seed carries a previous run's sessions 2-4 at the
    # same coordinates, 13 of them on the S6 (concept, turn)
    # coordinates) and the store dedupes by id — 12 line-lesson
    # markers + 1 drill-unable land on existing ids (the seed's
    # continuity still holds; the labels ride the coordinates, the
    # house event design).
    "final_total": 734,  # 636 seed + 45 new facts + 53 new events
    "new_facts": 45,
    "new_events": 53,  # 32 derivation-correct + 11 drill-unable + 10 seam-lesson markers
    #: the ten S6 seam facts, frozen statements (byte-frozen)
    "seam_facts": _LESSON_META_S6,
    #: the six theorem facts, frozen statements (byte-frozen)
    "theorem_facts": _THEOREM_META_S6,
    # D-e6t (recorded after control #1): the pre-reg prose said
    # "24 S5 + 10 S6 = 34 declared + 6 = 40 seam-family facts"; the
    # mechanism writes 26 declared (S4's ten + S5's sixteen) + 10
    # (S6) = 36 declared + 6 theorems = 42 seam-family facts.
    "total_seam_facts": 42,  # lesson/conjecture/theorem top-level kinds
    # P2 — the pre-lesson honest gaps (frozen refs -> concepts).
    "pre_teach_gaps": {
        "S02:22": "averaging",  # the torus-average fact is untaught
        "S03:07": "packing",  # the pack-bound theorem does not exist yet
    },
    # P2 — the typed SCAFFOLD FAILURES (frozen refs -> notes).
    "scaffold_failures": {
        "S02:15": "window-rich: overlap-ratio + torus-average untaught",
        "S03:01": "proj-inj: one-embed-zero untaught",
        "S03:11": "pack-bound: b-positive missing from the parts",
        "S04:12": "b-positive: not a sanctioned derivation (no rule)",
    },
    # P2 — the DERIVE SUCCESS turns (frozen refs -> theorem slugs).
    "derive_successes": {
        "S02:25": "window-rich",
        "S03:04": "proj-inj",
        "S03:14": "pack-bound",
        "S04:03": "delta-positive",
        "S04:05": "growth-compare",
        "S04:08": "infinity-end",
    },
    # P2/P4 — the CONDITIONAL turn (the store-mediated power probe).
    "conditional_turn": "S04:22",
    # P3 — the exact derived answers (frozen; every one must be
    # `derived` with non-empty grounded evidence citing the owning
    # fact).
    "derived_table": {
        "S02:14": _st6("normonecount"),
        "S02:18": _ANSWER_["GRID_7_7"],
        "S02:21": _st6("overlap-ratio"),
        "S02:24": _st6("torus-average"),
        "S02:25": _th("window-rich"),
        "S03:03": _st6("one-embed-zero"),
        "S03:04": _th("proj-inj"),
        "S03:05": _th("proj-inj"),
        "S03:06": _whychain("proj-inj"),
        "S03:10": _st6("vol-compare"),
        "S03:14": _th("pack-bound"),
        "S03:15": _th("pack-bound"),
        "S03:16": _whychain("pack-bound"),
        "S03:17": _ANSWER_["PACK_1"],
        "S03:18": _ANSWER_["PACK_2"],
        "S04:02": _st6("slack-compose-rule"),
        "S04:03": _th("delta-positive"),
        "S04:04": _th("delta-positive"),
        "S04:05": _th("growth-compare"),
        "S04:06": _th("growth-compare"),
        "S04:08": _th("infinity-end"),
        "S04:09": _th("infinity-end"),
        "S04:10": _whychain("infinity-end"),
        "S04:11": _whychain("window-rich"),
        "S04:13": _ANSWER_["CONJ_OPEN"],
        "S04:14": _ANSWER_["GRID_4_4"],
        "S04:15": _ANSWER_["SQ_YES_2_5"],
        "S04:16": _ANSWER_["TWOSQ_50"],
        "S04:17": _ANSWER_["GS_YES_3_2"],
        "S04:19": _ANSWER_["TRIPOW_4"],
        "S04:25": _ANSWER_["GRID_7_7"],
        "S04:26": _th("infinity-end"),
    },
    # P4 — the measured walls (frozen refs).
    "why_walls": {
        "S02:17": "the gamma-positive proof is not a store object (S7's P6)",
        "S03:13": "the b-positive proof is not a store object",
        "S04:24": "the gamma-positive proof is not a store object (band-stable)",
    },
    "magnitude_walls": {
        "S03:19": "packcount 3: 144 is off the 0..84 line",
        "S04:18": "duopow 7: 128 is off the 0..84 line (the S5 wall persists)",
        "S04:20": "tripow 5: 243 is off the 0..84 line (the tower wall)",
    },
    "power_wall_pre_chain": {
        "S02:19": "the power probe while the chain is incomplete (the S4/S5 articulation)"
    },
    "show_one_wall": {
        "S04:21": "no concrete violating n is in the store (limit #3 stays a wall)"
    },
    # P4 also — the beds EXACT (all grounded on the 0..84 line).
    "beds_exact": {
        "S02:18": _ANSWER_["GRID_7_7"],
        "S03:17": _ANSWER_["PACK_1"],
        "S03:18": _ANSWER_["PACK_2"],
        "S04:14": _ANSWER_["GRID_4_4"],
        "S04:15": _ANSWER_["SQ_YES_2_5"],
        "S04:16": _ANSWER_["TWOSQ_50"],
        "S04:17": _ANSWER_["GS_YES_3_2"],
        "S04:19": _ANSWER_["TRIPOW_4"],
        "S04:25": _ANSWER_["GRID_7_7"],
    },
    # P5 — the SEAM invariance: the erdosguess is a status surface
    # (never a premise; the flip is S7's). A theorem id may appear in
    # `grounded` ONLY within the frozen per-turn allow-set below:
    # its own state turn, the derive/whydeep turns that take it as a
    # sanctioned part, and the bed turns its owning concept runs.
    # NO theorem is ever a premise of an independent line
    # (arithmetic) derivation — the line arithmetic beds (grid /
    # sqmod / twosq / gsay / duopow / tripow) are NOT in the map,
    # so any theorem citation there is a P5 failure. (The owning
    # concept's own bed citing its theorem mirrors the S5 house
    # pattern where a seam bed cites its owning seam fact — the
    # pre-reg P7's "cites only line facts + its owning seam fact".)
    "conj_status_evidence": ["S04:13", "S04:23"],
    "theorem_allowed": {
        "S03:04": ("window-rich",),
        "S03:05": ("proj-inj",),
        "S03:06": ("window-rich",),
        "S03:15": ("pack-bound",),
        "S03:17": ("pack-bound",),
        "S03:18": ("pack-bound",),
        "S04:04": ("delta-positive",),
        "S04:05": ("proj-inj", "pack-bound"),
        "S04:06": ("growth-compare",),
        "S04:08": ("delta-positive", "growth-compare"),
        "S04:09": ("infinity-end",),
        "S04:10": ("delta-positive", "growth-compare"),
        "S04:26": ("infinity-end",),
    },
    # P6 — the band-end table (S04:13-17, 19, 21, 22, 23, 25, 26).
    "band_end_probes": {
        "S04:13": _ANSWER_["CONJ_OPEN"],
        "S04:14": _ANSWER_["GRID_4_4"],
        "S04:15": _ANSWER_["SQ_YES_2_5"],
        "S04:16": _ANSWER_["TWOSQ_50"],
        "S04:17": _ANSWER_["GS_YES_3_2"],
        "S04:19": _ANSWER_["TRIPOW_4"],
        "S04:23": _ANSWER_["CONJ_PROVEN_NO"],
        "S04:25": _ANSWER_["GRID_7_7"],
        "S04:26": _th("infinity-end"),
    },
    # P7 — the cross-checks + the inspectable DAG.
    "bed_crosscheck": {
        "pack_ref": "S03:18",  # (4*2)^2 = 64 = duopow 6 (one number, two beds)
        "pack_answer": _ANSWER_["PACK_2"],
        "tripow_ref": "S04:19",  # 3^4 = 81: a successor fact of the extension
        "tripow_answer": _ANSWER_["TRIPOW_4"],
    },
    "theorem_dag": {
        "window-rich": ("normonecount", "overlap-ratio", "torus-average"),
        "proj-inj": ("minkembed", "one-embed-zero", "window-rich"),
        "pack-bound": ("numberfields", "denom-d", "vol-compare", "b-positive"),
        "growth-compare": ("proj-inj", "pack-bound"),
        "delta-positive": ("gamma-positive", "b-positive", "slack-compose-rule"),
        "infinity-end": ("delta-positive", "growth-compare", "hypo-infinity"),
    },
    # P8 — mastery of the SIX S6 concepts (FROZEN FROM CONTROL #1).
    # HONEST PREG READ: the S5 gap cascade spans into S6 (number-field
    # 2/practicing still gates minkowski-embed / cm-conj, which gate
    # window-setup, which gates the whole S6 chain) — ALL six new
    # concepts end PRACTICING, averaging (4) and packing (6) and
    # criterion-chain (10) clear the K=4 evidence bar but are
    # prereq-GATED. The state of every pre-S6 concept is UNCHANGED
    # (re-drills only touch them through the band-end joint probes).
    "mastery_expected": {
        "window-setup": {"state": "practicing", "correct": 1},
        "averaging": {"state": "practicing", "correct": 4},
        "projection": {"state": "practicing", "correct": 4},  # S03:03,04,05,06 (state/derive/state/whydeep)
        "packing": {"state": "practicing", "correct": 6},
        "slack-margins": {"state": "practicing", "correct": 1},
        "criterion-chain": {"state": "practicing", "correct": 9},  # the C turn rides unit-distance, not this concept
    },
    # P8 — the prereq-gap structure (frozen from control #1).
    "expected_prereq_gaps": {
        "window-setup": ("cm-conj", "minkowski-embed"),
        "averaging": ("window-setup",),
        "projection": ("window-setup",),
        "packing": ("number-field", "window-setup"),
        "slack-margins": ("packing",),
        "criterion-chain": ("averaging", "packing", "projection", "slack-margins"),
    },
    # P8 — the pre-S6 states that must NOT change (from the frozen
    # e6.9 FROZEN table + the stable S4/seed concepts).
    "pre_s6_states": {
        "number-field": "practicing",
        "prime-split": "practicing",
        "mod4-split": "practicing",
        "disc-rd": "practicing",
        "adjoin-i": "practicing",
        "cyclotomic-cubic": "practicing",
        "char-cutout": "practicing",
        "class-bound": "practicing",
        "chebotarev": "practicing",
        "pnt-ap": "practicing",
        "frattini": "practicing",
        "golod-shaf": "practicing",
        "shafarevich": "practicing",
        "cm-conj": "practicing",
        "minkowski-embed": "practicing",
        "hajir-maire": "practicing",
    },
    # P3 — the eleven prereq edges that must be ESTABLISHED.
    "prereq_edges": [
        "curriculum:prereq:window-setup>minkowski-embed",
        "curriculum:prereq:window-setup>cm-conj",
        "curriculum:prereq:averaging>window-setup",
        "curriculum:prereq:projection>window-setup",
        "curriculum:prereq:packing>window-setup",
        "curriculum:prereq:packing>number-field",
        "curriculum:prereq:slack-margins>packing",
        "curriculum:prereq:criterion-chain>averaging",
        "curriculum:prereq:criterion-chain>projection",
        "curriculum:prereq:criterion-chain>packing",
        "curriculum:prereq:criterion-chain>slack-margins",
    ],
    "script": {
        2: [
            "after 72 comes 73",
            "after 73 comes 74",
            "after 74 comes 75",
            "after 75 comes 76",
            "after 76 comes 77",
            "after 77 comes 78",
            "after 78 comes 79",
            "after 79 comes 80",
            "after 80 comes 81",
            "after 81 comes 82",
            "after 82 comes 83",
            "after 83 comes 84",
            _st6("normonecount"),
            "state the normonecount rule",
            "derive window-rich from normonecount, overlap-ratio and torus-average",
            _st6("gamma-positive"),
            "explain why the gamma-positive holds",
            "how many unit pairs does the 7 by 7 grid have?",
            "can you prove that for infinitely many n the unit pairs grow to a power above one?",
            _st6("overlap-ratio"),
            "state the overlap-ratio rule",
            "state the torus-average rule",
            _st6("torus-average"),
            "state the torus-average rule",
            "derive window-rich from normonecount, overlap-ratio and torus-average",
        ],
        3: [
            "derive proj-inj from minkembed, one-embed-zero and window-rich",
            _st6("one-embed-zero"),
            "state the one-embed-zero rule",
            "derive proj-inj from minkembed, one-embed-zero and window-rich",
            "state the proj-inj rule",
            "explain why the proj-inj holds",
            "how many points does the packing bound allow when the outer radius is 1 times the inner?",
            _st6("denom-d"),
            _st6("vol-compare"),
            "state the vol-compare rule",
            "derive pack-bound from numberfields, denom-d and vol-compare",
            _st6("b-positive"),
            "explain why the b-positive holds",
            "derive pack-bound from numberfields, denom-d, vol-compare and b-positive",
            "state the pack-bound rule",
            "explain why the pack-bound holds",
            "how many points does the packing bound allow when the outer radius is 1 times the inner?",
            "how many points does the packing bound allow when the outer radius is 2 times the inner?",
            "how many points does the packing bound allow when the outer radius is 3 times the inner?",
        ],
        4: [
            _st6("slack-compose-rule"),
            "state the slack-compose-rule rule",
            "derive delta-positive from gamma-positive, b-positive and slack-compose-rule",
            "state the delta-positive rule",
            "derive growth-compare from proj-inj and pack-bound",
            "state the growth-compare rule",
            _st6("hypo-infinity"),
            "derive infinity-end from delta-positive, growth-compare and hypo-infinity",
            "state the infinity-end rule",
            "explain why the infinity-end holds",
            "explain why the window-rich holds",
            "derive b-positive from slack-compose-rule and window-rich",
            "what is the status of the erdosguess?",
            "how many unit pairs does the 4 by 4 grid have?",
            "does 2 squared plus one vanish modulo 5?",
            "in how many ways is 50 a sum of two squares?",
            "does the gs test say infinite for 3 generators and 2 relations?",
            "how large is two raised to the 7?",
            "how large is three raised to the 4?",
            "how large is three raised to the 5?",
            "name a concrete n for which the unit pairs exceed n to the 1 plus delta",
            "can you prove that for infinitely many n the unit pairs grow to a power above one?",
            "is the erdosguess proven?",
            "explain why the gamma-positive holds",
            "how many unit pairs does the 7 by 7 grid have?",
            "state the infinity-end rule",
        ],
    },
    # P2 — the frozen domain sequence per session (L lesson, U
    # pre-lesson gap, F scaffold-failure, T derive-success, S
    # derived, H honest wall, C conditional). S2/S3 match the
    # pre-reg letter-for-letter; S4 is derived turn-for-turn from the
    # authoritative per-turn script by control #1 (the D-e6q lesson).
    # D-e6v (control #1, letter-for-letter): the pre-reg's hand-derived
    # S2 string carried a single-letter slip at position 19 (it read
    # S; the pre-reg's OWN per-turn script — declared authoritative —
    # makes S02:19 the pre-chain power probe, which is the H wall).
    # The per-turn script wins (the D-e6q lesson, third application);
    # S3 and S4 match the pre-reg letter-for-letter.
    "domain_sequence": {
        2: "SSSSSSSSSSSSLSFLHSHLSULST",
        3: "FLSTSSULLSFLHTSSSSH",
        4: "LSTSTSLTSSSFSSSSSHSHHCSHSS",
    },
}

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

#: the ten lesson phrases + the twelve line lessons (frozen) must
#: appear IN the script, byte-exact (the literal script turns are
#: the canonical bytes)
_lesson_phrases = list(S6_LESSONS)
for _phrase in _lesson_phrases:
    assert any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"the S6 lesson phrase is not verbatim in the frozen script: {_phrase[:60]}..."
    )
for _n in range(72, 84):
    _line_turn = f"after {_n} comes {_n + 1}"
    assert any(t == _line_turn for s in FROZEN["script"].values() for t in s), (
        f"the S6 line-extension turn is missing: {_line_turn}"
    )


def _line_end(store) -> int:
    """The current line end = the largest successor fact v+1 in the
    store (the e6.8 machinery, unchanged by S6)."""

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
    L savant lesson, U pre-lesson capability gap, F typed scaffold
    failure, T derive-success, C conditional-derivation answer, H
    honest needs_info wall, S derived. Pure function of the turn
    record."""

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
    rt = InfantRuntime(root, concepts=CONCEPTS_E610)
    out: list[dict] = []
    for s in (2, 3, 4):
        rt.boot(s)
        for text in FROZEN["script"][s]:
            rt.turn(text)
        out.append(rt.lapse().to_dict())
    return out


def _seed_check(root: Path) -> dict:
    """P8: the seed dump is the official e6.9 S5 store, id-for-id."""

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
    for srow in runs["e6.10-run1"]:
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
        "theorem_facts": {slug: {"statement": meta["statement"]} for slug, meta in _THEOREM_META_S6.items()},
    }


def run_e6_10(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.9 S5 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: dict[str, list[dict]] = {}
    for name in ("e6.10-run1", "e6.10-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.9 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)
    # the declared curriculum map (the T7 artifact) — with the S6
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E610}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.10-run1", "e6.10-run2"):
        (out_dir / name / "e6.10-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.10.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict[str, list[dict]], report: dict, out_dir: Path) -> dict:
    checks: dict[str, Any] = {}
    turns = report["turns"]
    run1_root = out_dir / "e6.10-run1"
    final = _fresh_store(run1_root, 4)

    # P0 — the paper NEVER reached the student (the S6 frozen
    # denylist over EVERY script turn, the ten seam statements, and
    # the six theorem statements; the statements carry their line
    # crosswalks)
    p0_bad: list[str] = []
    for s, script in sorted(FROZEN["script"].items()):
        for surface in script:
            for term in S6_DENYLIST:
                if term in surface:
                    p0_bad.append(f"S{s:02d}: banned paper text in the script: {term!r}")
    for slug, meta in sorted(FROZEN["seam_facts"].items()):
        if not meta["source_lines"]:
            p0_bad.append(f"{slug}: the canonical statement has no line crosswalk")
        for term in S6_DENYLIST:
            if term in meta["statement"]:
                p0_bad.append(f"{slug}: banned paper text in the seam statement: {term!r}")
    for slug, meta in sorted(FROZEN["theorem_facts"].items()):
        for term in S6_DENYLIST:
            if term in meta["statement"]:
                p0_bad.append(f"{slug}: banned paper text in the theorem statement: {term!r}")
    checks["p0_no_paper_text"] = {"pass": not p0_bad, "bad": p0_bad}

    # P1 — script & contract (70 turns, contract-valid, det arm)
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
    # failures (F), derive-success (T), the conditional (C), and the
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
    t = turns.get(FROZEN["conditional_turn"])
    if t is None:
        p2_bad.append("missing the conditional turn")
    else:
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "conditional":
            p2_bad.append(f"{FROZEN['conditional_turn']}: not the conditional state ({ir.get('uncertainty_state')})")
        if not any("theorem:" in str(x) for x in ir.get("evidence") or []):
            p2_bad.append(f"{FROZEN['conditional_turn']}: the chain is not in the evidence")
        if t["grounded"]:
            p2_bad.append(f"{FROZEN['conditional_turn']}: the conditional answer cited established premises (it must not)")
    for s, frozen_seq in sorted(FROZEN["domain_sequence"].items()):
        actual = "".join(turns[f"S{s:02d}:{tn:02d}"]["domain"] for tn, _ in enumerate(FROZEN["script"][s], 1))
        if actual != frozen_seq:
            p2_bad.append(f"S{s:02d}: the domain sequence {actual} != frozen {frozen_seq}")
    checks["p2_typed_honesty_interleave"] = {"pass": not p2_bad, "bad": p2_bad}

    # P3 — the SEAM + the THEOREMS: 42 seam-family facts (36 declared
    # + 6 derived), all S6 statements byte-equal to the frozen
    # canonical statements, ALL pre-S6 seam facts byte-unchanged,
    # the theorems DERIVED with evidence exactly the sanctioned
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
        if not t["grounded"] and ref not in FROZEN["conj_status_evidence"]:
            p3_bad.append(f"{ref}: zero grounded evidence")
    # the ten S6 seam facts
    for slug, meta in sorted(FROZEN["seam_facts"].items()):
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
    # the six theorem facts (DERIVED provenance, exact parts)
    for slug, meta in sorted(FROZEN["theorem_facts"].items()):
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
        # the evidence must BE the part fact ids, all in the store
        for pid in a.provenance.evidence if a.provenance else []:
            try:
                pf = final.get(pid)
            except KeyError:
                p3_bad.append(f"{slug}: the theorem evidence {pid} is not in the store")
                continue
            if pf is None:
                p3_bad.append(f"{slug}: the theorem evidence {pid} is not active")
    # every pre-S6 seam fact: byte-exact (no drift)
    for _lessons, _label in ((S4_LESSONS, "S4"), (S5_LESSONS, "S5")):
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
    # the WHY-SPLIT, mechanically: declared-lemma whydeep = the S5
    # wall (W-S6-6); theorem whydeep = the chain articulation
    for ref, slug in (("S02:17", "gamma-positive"), ("S03:13", "b-positive"), ("S04:24", "gamma-positive")):
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing {ref}")
            continue
        ans = str(_ir_answer(t) or "")
        if "the proof of" not in ans or "not in my store" not in ans:
            p3_bad.append(f"{ref}: the declared-lemma why-wall articulation is missing")
    for ref, slug in (("S03:06", "proj-inj"), ("S03:16", "pack-bound"), ("S04:10", "infinity-end"), ("S04:11", "window-rich")):
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

    # P4 — the measured walls + the beds exact
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
        ans = str(ir.get("answer", ""))
        if "past my line which ends at 84" not in ans:
            p4_bad.append(f"{ref}: the magnitude wall must name the off-line value and the line end 84")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited evidence")
    for ref, expected_val in (("S03:19", "144"), ("S04:18", "128"), ("S04:20", "243")):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing {ref}")
            continue
        if expected_val not in str((t["response_ir"] or {}).get("answer", "")):
            p4_bad.append(f"{ref}: the wall must name {expected_val}")
    t = turns.get(FROZEN["power_wall_pre_chain"] and "S02:19")
    if t is None:
        p4_bad.append("missing the pre-chain power probe")
    else:
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append("S02:19: the pre-chain power probe is not an honest gap")
        if GAP_ARTICULATION not in str(ir.get("answer", "")):
            p4_bad.append("S02:19: the not-yet-taught articulation is missing")
        if t["grounded"]:
            p4_bad.append("S02:19: a wall cited evidence")
    t = turns.get("S04:21")
    if t is None:
        p4_bad.append("missing the show-one probe")
    else:
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p4_bad.append("S04:21: the show-one probe is not an honest gap")
        if "not one instance number" not in str(ir.get("answer", "")):
            p4_bad.append("S04:21: the show-one articulation is missing")
        if t["grounded"]:
            p4_bad.append("S04:21: a wall cited evidence")
    t = turns.get(FROZEN["conditional_turn"])
    if t is None:
        p4_bad.append("missing the conditional turn")
    else:
        ans = str((t["response_ir"] or {}).get("answer", ""))
        if not ans.startswith(CONDITIONAL_ARTICULATION):
            p4_bad.append(f"{FROZEN['conditional_turn']}: the conditional articulation is missing")
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

    # P5 — the SEAM invariance: the erdosguess is a status surface
    # (never a premise; the flip is S7's); the theorem ids appear in
    # `grounded` ONLY on their own state turns
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

    # P6 — the band-end table (one store, the criterion, the walls)
    p6_bad: list[str] = []
    for ref, expected in sorted(FROZEN["band_end_probes"].items()):
        t = turns.get(ref)
        if t is None:
            p6_bad.append(f"missing {ref}")
            continue
        got = _ir_answer(t)
        if got != expected:
            p6_bad.append(f"{ref}: band-end answer {got!r} != {expected!r}")
    checks["p6_band_end"] = {"pass": not p6_bad, "bad": p6_bad}

    # P7 — the cross-checks + the inspectable DAG: packcount k=2 =
    # 64 = duopow 6 (one number, two beds) grounded on the line;
    # tripow 4 = 81 cites the EXTENDED successor fact; every theorem
    # fact's derived_from reproduces the sanctioned DAG exactly and
    # every part fact exists in the store
    p7_bad: list[str] = []
    bc = FROZEN["bed_crosscheck"]
    tp = turns.get(bc["pack_ref"])
    if tp is None:
        p7_bad.append("missing the pack cross-check ref")
    else:
        if _ir_answer(tp) != bc["pack_answer"]:
            p7_bad.append(f"{bc['pack_ref']}: the pack bed is not {bc['pack_answer']}")
        for x in tp["grounded"]:
            x = str(x)
            if not (x.startswith("cs-") or x == "theorem:pack-bound"):
                p7_bad.append(f"{bc['pack_ref']}: the pack bed cited a non-line fact {x}")
        if not any(str(x) == "theorem:pack-bound" for x in tp["grounded"]):
            p7_bad.append(f"{bc['pack_ref']}: the pack bed did not cite its owning theorem")
    tt = turns.get(bc["tripow_ref"])
    if tt is None:
        p7_bad.append("missing the tripow cross-check ref")
    else:
        if _ir_answer(tt) != bc["tripow_answer"]:
            p7_bad.append(f"{bc['tripow_ref']}: the tripow bed is not {bc['tripow_answer']}")
        # the bed must cite the EXTENDED successor fact (81 > the S5 line
        # end 72): resolve its assertion id via the object id
        fact81 = None
        for a in final.query(context_match={"kind": "fact", "concept": "count-successor"}):
            if a.object_id == "count-successor:num(81)":
                fact81 = a
                break
        if fact81 is None:
            p7_bad.append("count-successor:num(81): the extended successor fact is not in the final store")
        elif fact81.id not in [str(x) for x in tt["grounded"]]:
            p7_bad.append(f"{bc['tripow_ref']}: the tripow bed did not cite the extended successor fact 81")
    for slug, parts in FROZEN["theorem_dag"].items():
        try:
            a = final.get(f"theorem:{slug}")
        except KeyError:
            p7_bad.append(f"{slug}: absent from the final store (DAG)")
            continue
        got_parts = tuple(a.context.data.get("derived_from") or ())
        if got_parts != tuple(parts):
            p7_bad.append(f"{slug}: the stored DAG edge {got_parts} != sanctioned {tuple(parts)}")
    checks["p7_crosscheck_dag"] = {"pass": not p7_bad, "bad": p7_bad}

    # P8 — mastery, store integrity, determinism
    p8_bad: list[str] = []
    seed = _seed_check(run1_root)
    if seed["seed_total"] != FROZEN["seed_total"]:
        p8_bad.append(f"seed total {seed['seed_total']} != {FROZEN['seed_total']}")
    if seed["reproduced_in_s2_pre"] != FROZEN["seed_total"] or seed["missing"]:
        p8_bad.append(f"seed continuity: {seed}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p8_bad.append(
            f"line end {_line_end(final)} != {FROZEN['line_end_final']} (the declared extension is exactly 0..84)"
        )
    # the TWELVE extension facts, exactly (resolved by object id —
    # the assertion ids are the cs-f... write stamps)
    ext_obj = set()
    for a in final.query(context_match={"kind": "fact", "concept": "count-successor"}):
        oid = a.object_id
        if not (isinstance(oid, str) and oid.startswith("count-successor:num(")):
            continue
        n = int(oid[len("count-successor:num(") : -1])
        if n > 72:
            ext_obj.add(n)
            if a.validity is not None and a.validity.to is not None:
                p8_bad.append(f"count-successor:num({n}): inactive in the final store")
    if ext_obj != set(range(73, 85)):
        p8_bad.append(f"line extension wrote the successor objects {sorted(ext_obj)} != exactly 73..84 (the declared operation)")
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
    mv = mastery_view(final, [c.id for c in CONCEPTS_E610])
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
    for cid, state in FROZEN["pre_s6_states"].items():
        v = mv.get(cid)
        if v is None or v.state != state:
            p8_bad.append(f"{cid}: pre-S6 state regressed ({v.state if v else 'absent'} != {state})")
    # determinism
    r1 = runs["e6.10-run1"]
    r2 = runs["e6.10-run2"]
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
        f"PASS e6.10: {passed}/{len(checks)}"
        if passed == len(checks)
        else f"FAIL e6.10: {passed}/{len(checks)}"
    )
    return {"checks": checks, "passed": passed, "value": value}


class E6_10Experiment:
    """E6.10 — S6 of the SAVANT-TRACK: the geometric criterion band
    (scaffolded generation — THE LEAP)."""

    name = "e6.10"
    hypothesis = (
        "The geometric criterion band (S6) stores the paper's theorem NOT as "
        "lessons about the conclusion but as DERIVATIONS from taught parts: the "
        "ten part facts are ESTABLISHED declared-source seam facts (36 declared "
        "seam facts with S4/S5's twenty-six); the SIX scaffolded derive turns "
        "store SIX theorem facts with derived (infant-observed) provenance, each "
        "citing exactly its sanctioned parts (window-rich, proj-inj, pack-bound, "
        "growth-compare, delta-positive, infinity-end — the chain (7)-(11) of "
        "the criterion, machine-inspectable in the store); the scaffold failures "
        "are honest and typed (3 missing-parts, 1 no-rule — zero writes, zero "
        "fabrication); the why-split holds (declared lemmas keep the proof wall, "
        "derived theorems answer with the in-store chain); the beds ride the "
        "declared 0..84 line extension (7x7 = 84 finally derives; the packing "
        "beds 16/64 with 144 off-line; the tower beds 3, 9, 27, 81 with 243 "
        "off-line; 128 still off-line); the SAME power probe is the S4/S5 wall "
        "while the chain is incomplete and the CONDITIONAL articulation once it "
        "is (hypotheses flagged, erdosguess still open — the flip is S7's); no "
        "concrete violating n can be named (limit #3 stays a wall by design); "
        "the paper never reaches the student (P0); two runs byte-identical."
    )
    metric = "S6 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_10()
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
                Path("results/phase-6/e6.10-run1/session-S02.json"),
                Path("results/phase-6/e6.10-run1/session-S03.json"),
                Path("results/phase-6/e6.10-run1/session-S04.json"),
                Path("results/phase-6/e6.10-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
            },
        )
