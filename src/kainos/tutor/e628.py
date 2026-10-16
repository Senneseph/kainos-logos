"""E6.28 — S24 of the FUNDAMENTALS-TRACK: the fibonacci weld
(COURSE B band 1 of 2 — the seeded line's own addition story).

The owner's lesson (course-fibonacci-research.md, stage A; the
stage B D-e6v(a) record): the line that runs by ADDITION ALONE —
start at zero and one, and every later term is the sum of the two
before it — and its TWIN, the line that starts at two and one under
the same rule: on my line the sum line reaches fifty-five in ten
steps and the eleventh step, the eighty-nine, stands off-line as
the ceiling the line already declared (the twin reaches seventy-six
in nine); the twin welds to the sum line in TWO ways — the doubled
term is the term times the twin, and the square sum of two
consecutive terms is the term at the doubled-plus-one index — two
roads, one destination, verified at every on-line index. In the
bandgen way, seeded from the S23 final (the prime proportion, 2074,
identity 8b5ca7a5fe76631e, line 0..84). The band teaches the
fibonacci weld over the carried S23 registry:

R1  THE SUM LINE — sum-line-def: the line that runs by addition
    alone; on my line fifty-five in ten steps, the eighty-nine
    off-line as the declared ceiling; the twin under the same rule
    to the seventy-six;
R2  THE TWIN LINE — twin-line-def: the weld in two ways (the
    doubling reads the twin as its multiplier; the square sum of
    two consecutive terms is the term at the doubled-plus-one
    index), verified at every on-line index;
R3  THE FILING — twin-line-filed: the twin line of record (the
    strict two-part set from the two lessons).

NEW FACTS (3): two lessons (sum-line-def, twin-line-def) + one
composition (twin-line-filed) — the D-e6v(a) adjudication: the
prereg's standalone twinsel is REFEREED OUT by the mechanism's
one-lesson-per-concept structural model and D4.4's strict two-part
filing; the welding content fully lives in the twin-line-def byte
and the band's drills. UNCONDITIONAL band: the three new facts
carry NO condition marker (P0 denies it; the marker census stays
6/1/7 from seed to final); the line stays 0..84; the walks, the
welding drills, and the marker census are line records, computed,
never declared. The standing off-script probe — the largest
doubled term my line holds — stands at fifty-five (the doubled
term at index ten) on the final store, expect_derived false on the
seed-only runtime (the D-e6u(c) pattern: the typed honest gap,
store-inert).

FROZEN FROM CONTROL (the S24 dry-run over the e6.27 seed — the
S23 final, 2074, identity 8b5ca7a5fe76631e): the table below is
the control's own census (c0-c9 CLEAN, twin byte-identical),
pformat width=4000 sort_dicts, pass-2 normalized (theorem_dag
re-unioned over S6..S21 + S31 + S32 + S22 + S23 + S24, script /
domain_sequence keyed by int, honest_zero_bytes emptied). Nothing
in this module is hand-typed: the checks read FROZEN, the
mechanism asserts its own numbers, and the store speaks, not the
hand.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S24,
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
    S12_LESSONS,
    S12_THEOREMS,
    S13_LESSONS,
    S13_THEOREMS,
    S14_LESSONS,
    S14_THEOREMS,
    S15_LESSONS,
    S15_THEOREMS,
    S16_LESSONS,
    S16_THEOREMS,
    S17_LESSONS,
    S17_THEOREMS,
    S18_LESSONS,
    S18_THEOREMS,
    S19_LESSONS,
    S19_THEOREMS,
    S20_LESSONS,
    S20_THEOREMS,
    S21_LESSONS,
    S21_THEOREMS,
    S22_LESSONS,
    S22_THEOREMS,
    S23_LESSONS,
    S23_THEOREMS,
    S24_LESSONS,
    S24_THEOREMS,
    S31_LESSONS,
    S31_THEOREMS,
    S32_LESSONS,
    S32_THEOREMS,
    Brainstem,
)
from kainos.tutor.e627 import (
    CONCEPTS_E627,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E628", "FROZEN", "E6_28Experiment", "run_e6_28"]

CHECKS = 9

#: S24 teaches: the fibonacci weld (COURSE B band 1 — the sum
#: line and its twin: the line that runs by addition alone, and
#: the line that starts at two and one under the same rule and
#: welds to it). The two new concepts join the carried S23
#: registry; the prereqs point DOWN into stable soil the store
#: already holds (add-two-digit and mult-within-100 for the sum
#: line, the sum line itself for the twin) — the band end is
#: STABLE with EMPTY gap lists: the soil is closed (D4 pre-reg).
CONCEPTS_E628: tuple = CONCEPTS_E627 + CONCEPT_S24

E628_SEED = Path("results/phase-6/e6.27-run1/codeX-S04.json")
def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E628_SEED.exists():
        return E628_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E628_SEED
    return alt if alt.exists() else E628_SEED

_ST28 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S24_LESSONS.items()}
_TH28 = {s: m["statement"] for s, m in S24_THEOREMS.items()}


def _th28(slug: str) -> str:
    return _TH28[slug]

#: P4 — the W_S24 walls (the declared territories of the
#: fibonacci weld: the term past the line end (the
#: eighty-nine ceiling), the third sum (the two-before-it rule
#: and nothing else), and the identity past the line end — P4
#: cross-checks the bytes against the Brainstem class
#: attributes, never surfaced beyond the wall; no term past the
#: eighty-four enters the floor).
W_S24_1 = Brainstem.W_S24_1
W_S24_2 = Brainstem.W_S24_2
W_S24_3 = Brainstem.W_S24_3


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
    failure (derive mode, not derived), T derive-success, S
    derived, H honest wall (needs_info)."""

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
    rt = InfantRuntime(root, concepts=CONCEPTS_E628)
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


FROZEN_DATA = {'bed_grounded': {'S02:08': ['lemma:sum-line-def'], 'S02:12': ['lemma:twin-line-def'], 'S02:13': ['lemma:sum-line-def'], 'S02:14': ['lemma:twin-line-def'], 'S02:15': ['lemma:twin-line-def'], 'S02:16': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S02:17': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:03': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:04': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:05': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:06': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:07': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:08': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:09': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S03:10': ['lemma:shadow-form-def'], 'S03:15': ['lemma:sum-line-def', 'lemma:twin-line-def', 'theorem:twin-line-filed'], 'S03:17': ['lemma:shadow-form-def'], 'S04:06': ['lemma:sum-line-def'], 'S04:07': ['lemma:twin-line-def'], 'S04:08': ['lemma:sum-line-def'], 'S04:09': ['lemma:twin-line-def'], 'S04:10': ['theorem:twin-line-filed'], 'S04:11': ['lemma:sum-line-def', 'lemma:twin-line-def', 'theorem:twin-line-filed'], 'S04:12': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S04:13': ['lemma:twin-line-def', 'lemma:sum-line-def'], 'S04:14': ['lemma:twin-line-def'], 'S04:15': ['lemma:sum-line-def'], 'S04:17': ['lemma:shadow-form-def']},
 'bed_owners': {'S02:08': 'lemma:sum-line-def', 'S02:12': 'lemma:twin-line-def', 'S02:13': 'lemma:sum-line-def', 'S02:14': 'lemma:twin-line-def', 'S02:15': 'lemma:twin-line-def', 'S02:16': 'lemma:twin-line-def', 'S02:17': 'lemma:twin-line-def', 'S03:03': 'lemma:twin-line-def', 'S03:04': 'lemma:twin-line-def', 'S03:05': 'lemma:twin-line-def', 'S03:06': 'lemma:twin-line-def', 'S03:07': 'lemma:twin-line-def', 'S03:08': 'lemma:twin-line-def', 'S03:09': 'lemma:twin-line-def', 'S03:10': 'lemma:shadow-form-def', 'S03:15': 'lemma:twin-line-def', 'S03:17': 'lemma:shadow-form-def', 'S04:06': 'lemma:sum-line-def', 'S04:07': 'lemma:twin-line-def', 'S04:08': 'lemma:sum-line-def', 'S04:09': 'lemma:twin-line-def', 'S04:10': 'theorem:twin-line-filed', 'S04:11': 'lemma:twin-line-def', 'S04:12': 'lemma:twin-line-def', 'S04:13': 'lemma:twin-line-def', 'S04:14': 'lemma:twin-line-def', 'S04:15': 'lemma:sum-line-def', 'S04:17': 'lemma:shadow-form-def'},
 'beds_exact': {'S02:08': 'the sum line runs by addition alone: start at zero and one, and every later term is the sum of the two before it — on my line the line reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off-line as my line already declared it; the twin line starts at two and one under the same rule and reaches seventy-six in nine steps; each term is derived from the two before it, not asserted from outside; at the line end eighty-four',
                'S02:12': 'the twin line welds to the sum line in two ways: the doubled term is the term times the twin (the doubling reads the twin as its multiplier), and the square sum of two consecutive terms is the term at the doubled-plus-one index — two roads, one destination, verified on my line at every on-line index; at the line end eighty-four',
                'S02:13': 'zero, one, one, two, three, five, eight, thirteen, twenty-one, thirty-four, and fifty-five: the sum line runs ten steps on my line, each term the sum of the two before it, at the line end 84',
                'S02:14': 'two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, and seventy-six: the twin line runs nine steps on my line under the same rule, at the line end 84',
                'S02:15': 'eighteen: the twin term at index six — the seven at four and the eleven at five, the sum of the two before it — under the same rule the twin line runs, at the line end 84',
                'S02:16': 'one: the doubled term at index two — the one, the term at one, times the one, the twin at one — is on my line, the welding of the two lines, at the line end 84',
                'S02:17': 'two: the square sum of the term at one and the term at two, two consecutive terms of my sum line — one squared plus one squared — is the term at index three, at the line end 84',
                'S03:03': 'three: the doubled term at index four — the one, the term at two, times the three, the twin at two — is on my line, the welding of the two lines, at the line end 84',
                'S03:04': 'eight: the doubled term at index six — the two, the term at three, times the four, the twin at three — is on my line, the welding of the two lines, at the line end 84',
                'S03:05': 'twenty-one: the doubled term at index eight — the three, the term at four, times the seven, the twin at four — is on my line, the welding of the two lines, at the line end 84',
                'S03:06': 'fifty-five: the doubled term at index ten — the five, the term at five, times the eleven, the twin at five — is on my line, the welding of the two lines, at the line end 84',
                'S03:07': 'five: the square sum of the term at two and the term at three, two consecutive terms of my sum line — one squared plus two squared — is the term at index five, at the line end 84',
                'S03:08': 'thirteen: the square sum of the term at three and the term at four, two consecutive terms of my sum line — two squared plus three squared — is the term at index seven, at the line end 84',
                'S03:09': 'thirty-four: the square sum of the term at four and the term at five, two consecutive terms of my sum line — three squared plus five squared — is the term at index nine, at the line end 84',
                'S03:10': "eighteen of my forty-four theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                'S03:15': 'the twin line, filed of record: the sum line runs by addition alone to the fifty-five and the twin under the same rule to the seventy-six, the identities weld the two lines at every on-line index, and the eighty-nine stands once more as the ceiling the line already declared; at the line end 84',
                'S03:17': "nineteen of my forty-five theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                'S04:06': 'zero, one, one, two, three, five, eight, thirteen, twenty-one, thirty-four, and fifty-five: the sum line runs ten steps on my line, each term the sum of the two before it, at the line end 84',
                'S04:07': 'two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, and seventy-six: the twin line runs nine steps on my line under the same rule, at the line end 84',
                'S04:08': 'the sum line runs by addition alone: start at zero and one, and every later term is the sum of the two before it — on my line the line reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off-line as my line already declared it; the twin line starts at two and one under the same rule and reaches seventy-six in nine steps; each term is derived from the two before it, not asserted from outside; at the line end eighty-four',
                'S04:09': 'the twin line welds to the sum line in two ways: the doubled term is the term times the twin (the doubling reads the twin as its multiplier), and the square sum of two consecutive terms is the term at the doubled-plus-one index — two roads, one destination, verified on my line at every on-line index; at the line end eighty-four',
                'S04:10': 'the twin line of my store is filed of record: the sum line runs by addition alone to the fifty-five and the twin under the same rule to the seventy-six, the identities weld the two lines at every on-line index, and the eighty-nine stands once more as the ceiling the line already declared; filed on the line, at the line end eighty-four',
                'S04:11': 'the twin line, filed of record: the sum line runs by addition alone to the fifty-five and the twin under the same rule to the seventy-six, the identities weld the two lines at every on-line index, and the eighty-nine stands once more as the ceiling the line already declared; at the line end 84',
                'S04:12': 'fifty-five: the doubled term at index ten — the five, the term at five, times the eleven, the twin at five — is on my line, the welding of the two lines, at the line end 84',
                'S04:13': 'thirty-four: the square sum of the term at four and the term at five, two consecutive terms of my sum line — three squared plus five squared — is the term at index nine, at the line end 84',
                'S04:14': 'eighteen: the twin term at index six — the seven at four and the eleven at five, the sum of the two before it — under the same rule the twin line runs, at the line end 84',
                'S04:15': "fifty-five: the sum line's term at index ten — the twenty-one at eight and the thirty-four at nine, the sum of the two before it — under the same rule the sum line runs, at the line end 84",
                'S04:17': "nineteen of my forty-five theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84"},
 'derive_successes': {'S03:14': ['twin-line-filed', ['lemma:sum-line-def', 'lemma:twin-line-def']]},
 'derived_table': {'S02:08': 'the sum line runs by addition alone: start at zero and one, and every later term is the sum of the two before it — on my line the line reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off-line as my line already declared it; the twin line starts at two and one under the same rule and reaches seventy-six in nine steps; each term is derived from the two before it, not asserted from outside; at the line end eighty-four',
                   'S02:12': 'the twin line welds to the sum line in two ways: the doubled term is the term times the twin (the doubling reads the twin as its multiplier), and the square sum of two consecutive terms is the term at the doubled-plus-one index — two roads, one destination, verified on my line at every on-line index; at the line end eighty-four',
                   'S02:13': 'zero, one, one, two, three, five, eight, thirteen, twenty-one, thirty-four, and fifty-five: the sum line runs ten steps on my line, each term the sum of the two before it, at the line end 84',
                   'S02:14': 'two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, and seventy-six: the twin line runs nine steps on my line under the same rule, at the line end 84',
                   'S02:15': 'eighteen: the twin term at index six — the seven at four and the eleven at five, the sum of the two before it — under the same rule the twin line runs, at the line end 84',
                   'S02:16': 'one: the doubled term at index two — the one, the term at one, times the one, the twin at one — is on my line, the welding of the two lines, at the line end 84',
                   'S02:17': 'two: the square sum of the term at one and the term at two, two consecutive terms of my sum line — one squared plus one squared — is the term at index three, at the line end 84',
                   'S03:03': 'three: the doubled term at index four — the one, the term at two, times the three, the twin at two — is on my line, the welding of the two lines, at the line end 84',
                   'S03:04': 'eight: the doubled term at index six — the two, the term at three, times the four, the twin at three — is on my line, the welding of the two lines, at the line end 84',
                   'S03:05': 'twenty-one: the doubled term at index eight — the three, the term at four, times the seven, the twin at four — is on my line, the welding of the two lines, at the line end 84',
                   'S03:06': 'fifty-five: the doubled term at index ten — the five, the term at five, times the eleven, the twin at five — is on my line, the welding of the two lines, at the line end 84',
                   'S03:07': 'five: the square sum of the term at two and the term at three, two consecutive terms of my sum line — one squared plus two squared — is the term at index five, at the line end 84',
                   'S03:08': 'thirteen: the square sum of the term at three and the term at four, two consecutive terms of my sum line — two squared plus three squared — is the term at index seven, at the line end 84',
                   'S03:09': 'thirty-four: the square sum of the term at four and the term at five, two consecutive terms of my sum line — three squared plus five squared — is the term at index nine, at the line end 84',
                   'S03:10': "eighteen of my forty-four theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                   'S03:14': 'the twin line of my store is filed of record: the sum line runs by addition alone to the fifty-five and the twin under the same rule to the seventy-six, the identities weld the two lines at every on-line index, and the eighty-nine stands once more as the ceiling the line already declared; filed on the line, at the line end eighty-four',
                   'S03:15': 'the twin line, filed of record: the sum line runs by addition alone to the fifty-five and the twin under the same rule to the seventy-six, the identities weld the two lines at every on-line index, and the eighty-nine stands once more as the ceiling the line already declared; at the line end 84',
                   'S03:17': "nineteen of my forty-five theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                   'S04:06': 'zero, one, one, two, three, five, eight, thirteen, twenty-one, thirty-four, and fifty-five: the sum line runs ten steps on my line, each term the sum of the two before it, at the line end 84',
                   'S04:07': 'two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, and seventy-six: the twin line runs nine steps on my line under the same rule, at the line end 84',
                   'S04:08': 'the sum line runs by addition alone: start at zero and one, and every later term is the sum of the two before it — on my line the line reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off-line as my line already declared it; the twin line starts at two and one under the same rule and reaches seventy-six in nine steps; each term is derived from the two before it, not asserted from outside; at the line end eighty-four',
                   'S04:09': 'the twin line welds to the sum line in two ways: the doubled term is the term times the twin (the doubling reads the twin as its multiplier), and the square sum of two consecutive terms is the term at the doubled-plus-one index — two roads, one destination, verified on my line at every on-line index; at the line end eighty-four',
                   'S04:10': 'the twin line of my store is filed of record: the sum line runs by addition alone to the fifty-five and the twin under the same rule to the seventy-six, the identities weld the two lines at every on-line index, and the eighty-nine stands once more as the ceiling the line already declared; filed on the line, at the line end eighty-four',
                   'S04:11': 'the twin line, filed of record: the sum line runs by addition alone to the fifty-five and the twin under the same rule to the seventy-six, the identities weld the two lines at every on-line index, and the eighty-nine stands once more as the ceiling the line already declared; at the line end 84',
                   'S04:12': 'fifty-five: the doubled term at index ten — the five, the term at five, times the eleven, the twin at five — is on my line, the welding of the two lines, at the line end 84',
                   'S04:13': 'thirty-four: the square sum of the term at four and the term at five, two consecutive terms of my sum line — three squared plus five squared — is the term at index nine, at the line end 84',
                   'S04:14': 'eighteen: the twin term at index six — the seven at four and the eleven at five, the sum of the two before it — under the same rule the twin line runs, at the line end 84',
                   'S04:15': "fifty-five: the sum line's term at index ten — the twenty-one at eight and the thirty-four at nine, the sum of the two before it — under the same rule the sum line runs, at the line end 84",
                   'S04:17': "nineteen of my forty-five theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84"},
 'domain_sequence': {2: 'SHSSUULSUULSSSSSS', 3: 'SHSSSSSSSSHHFTSHS', 4: 'SHHHHSSSSSSSSSSSS'},
 'expected_prereq_gaps': {'sum-line': [], 'twin-line': []},
 'final_total': 2126,
 'honest_zero_bytes': {},
 'line_end_final': 84,
 'mastery_expected': {'sum-line': {'correct': 5, 'state': 'stable'}, 'twin-line': {'correct': 21, 'state': 'stable'}},
 'missing_parts_failure': {},
 'new_events': 49,
 'new_fact_ids': ['lemma:sum-line-def', 'lemma:twin-line-def', 'theorem:twin-line-filed'],
 'new_facts': 3,
 'offscript_carry': {'what is the largest doubled term my line holds?': None},
 'pre_s24_drilled': {'mod4-split': 2, 'prime-fingerprint': 2, 'shadow-form': 1},
 'pre_s24_states': {'add-two-digit': {'correct': 11, 'state': 'stable'},
                    'add-within-10': {'correct': 5, 'state': 'stable'},
                    'adjoin-i': {'correct': 1, 'state': 'practicing'},
                    'alg-inverse-1step': {'correct': 5, 'state': 'stable'},
                    'alg-inverse-mul': {'correct': 5, 'state': 'stable'},
                    'alg-two-step': {'correct': 4, 'state': 'stable'},
                    'algebraic-rank': {'correct': 12, 'state': 'stable'},
                    'analytic-order': {'correct': 5, 'state': 'stable'},
                    'averaging': {'correct': 4, 'state': 'practicing'},
                    'beal-census': {'correct': 12, 'state': 'stable'},
                    'beal-summit': {'correct': 7, 'state': 'stable'},
                    'boundary-form': {'correct': 5, 'state': 'stable'},
                    'bsd-summit': {'correct': 13, 'state': 'stable'},
                    'char-cutout': {'correct': 2, 'state': 'practicing'},
                    'chebotarev': {'correct': 2, 'state': 'practicing'},
                    'circle-pair-2': {'correct': 4, 'state': 'stable'},
                    'class-bound': {'correct': 4, 'state': 'stable'},
                    'class-np': {'correct': 5, 'state': 'stable'},
                    'class-p': {'correct': 4, 'state': 'stable'},
                    'cm-conj': {'correct': 4, 'state': 'stable'},
                    'compare-numbers': {'correct': 11, 'state': 'stable'},
                    'composite': {'correct': 7, 'state': 'stable'},
                    'condition-line': {'correct': 9, 'state': 'practicing'},
                    'conditional': {'correct': 2, 'state': 'practicing'},
                    'coprime-pair': {'correct': 6, 'state': 'stable'},
                    'cost-counter': {'correct': 10, 'state': 'stable'},
                    'count-successor': {'correct': 14, 'state': 'stable'},
                    'criterion-chain': {'correct': 10, 'state': 'practicing'},
                    'critical-strip': {'correct': 12, 'state': 'practicing'},
                    'curve-form': {'correct': 7, 'state': 'stable'},
                    'curve-law': {'correct': 8, 'state': 'stable'},
                    'curve-shadow': {'correct': 12, 'state': 'stable'},
                    'cyclotomic-cubic': {'correct': 3, 'state': 'practicing'},
                    'decision-question': {'correct': 11, 'state': 'stable'},
                    'disc-rd': {'correct': 1, 'state': 'practicing'},
                    'disproof': {'correct': 10, 'state': 'practicing'},
                    'divides': {'correct': 10, 'state': 'stable'},
                    'erdos-conj': {'correct': 10, 'state': 'stable'},
                    'euler-factor': {'correct': 9, 'state': 'stable'},
                    'factor-route': {'correct': 19, 'state': 'practicing'},
                    'family-factor': {'correct': 25, 'state': 'stable'},
                    'first-divisor': {'correct': 38, 'state': 'stable'},
                    'fraction': {'correct': 18, 'state': 'stable'},
                    'frattini': {'correct': 1, 'state': 'practicing'},
                    'func-eq': {'correct': 14, 'state': 'practicing'},
                    'gaussian-int': {'correct': 7, 'state': 'stable'},
                    'geom-area': {'correct': 6, 'state': 'stable'},
                    'geom-area-triangle': {'correct': 6, 'state': 'stable'},
                    'geom-perimeter': {'correct': 5, 'state': 'stable'},
                    'golden-seed': {'correct': 16, 'state': 'stable'},
                    'golod-shaf': {'correct': 6, 'state': 'practicing'},
                    'grid-lattice': {'correct': 10, 'state': 'stable'},
                    'hajir-maire': {'correct': 1, 'state': 'practicing'},
                    'hardy-line': {'correct': 5, 'state': 'practicing'},
                    'hypothesis': {'correct': 5, 'state': 'practicing'},
                    'index-split': {'correct': 9, 'state': 'stable'},
                    'kin-distance': {'correct': 4, 'state': 'stable'},
                    'kin-position': {'correct': 6, 'state': 'stable'},
                    'kin-rate': {'correct': 4, 'state': 'stable'},
                    'kin-solve-time': {'correct': 4, 'state': 'stable'},
                    'kst-bound': {'correct': 4, 'state': 'stable'},
                    'l-correction': {'correct': 11, 'state': 'stable'},
                    'l-partial': {'correct': 14, 'state': 'stable'},
                    'li-criterion': {'correct': 9, 'state': 'stable'},
                    'lindelof': {'correct': 4, 'state': 'practicing'},
                    'line-partial': {'correct': 11, 'state': 'stable'},
                    'line-reaching': {'correct': 5, 'state': 'stable'},
                    'local-form': {'correct': 4, 'state': 'stable'},
                    'lte-form': {'correct': 7, 'state': 'stable'},
                    'minkowski-embed': {'correct': 1, 'state': 'practicing'},
                    'mod4-split': {'correct': 10, 'state': 'stable'},
                    'mult-within-100': {'correct': 9, 'state': 'stable'},
                    'norm-convex': {'correct': 5, 'state': 'stable'},
                    'norm-flat': {'correct': 5, 'state': 'stable'},
                    'norm-generic': {'correct': 4, 'state': 'stable'},
                    'number-field': {'correct': 4, 'state': 'stable'},
                    'off-line-seed': {'correct': 8, 'state': 'stable'},
                    'packing': {'correct': 6, 'state': 'practicing'},
                    'phrasology': {'correct': 24, 'state': 'stable'},
                    'pi-eq': {'correct': 3, 'state': 'practicing'},
                    'pnp-summit': {'correct': 7, 'state': 'stable'},
                    'pnt': {'correct': 8, 'state': 'stable'},
                    'pnt-ap': {'correct': 2, 'state': 'practicing'},
                    'pnt-error': {'correct': 9, 'state': 'practicing'},
                    'point-count': {'correct': 6, 'state': 'stable'},
                    'polya-hilbert': {'correct': 3, 'state': 'practicing'},
                    'prime-count': {'correct': 15, 'state': 'stable'},
                    'prime-fingerprint': {'correct': 23, 'state': 'stable'},
                    'prime-split': {'correct': 4, 'state': 'stable'},
                    'projection': {'correct': 4, 'state': 'practicing'},
                    'proportion': {'correct': 9, 'state': 'stable'},
                    'psi-eq': {'correct': 12, 'state': 'stable'},
                    'reduction': {'correct': 10, 'state': 'stable'},
                    'removal-rule': {'correct': 12, 'state': 'stable'},
                    'rh-relevance': {'correct': 23, 'state': 'practicing'},
                    'rh-scale': {'correct': 24, 'state': 'practicing'},
                    'riemann': {'correct': 17, 'state': 'practicing'},
                    'rv-count': {'correct': 10, 'state': 'practicing'},
                    's-of-t': {'correct': 3, 'state': 'practicing'},
                    'scan-ledger': {'correct': 12, 'state': 'stable'},
                    'seed-period': {'correct': 17, 'state': 'stable'},
                    'seeded-line': {'correct': 14, 'state': 'stable'},
                    'shadow-form': {'correct': 13, 'state': 'stable'},
                    'shafarevich': {'correct': 2, 'state': 'practicing'},
                    'shape-circle': {'correct': 6, 'state': 'stable'},
                    'shape-rectangle': {'correct': 4, 'state': 'stable'},
                    'shape-square': {'correct': 5, 'state': 'stable'},
                    'shape-triangle': {'correct': 6, 'state': 'stable'},
                    'size-shadow': {'correct': 11, 'state': 'stable'},
                    'slack-margins': {'correct': 1, 'state': 'practicing'},
                    'sst-bound': {'correct': 4, 'state': 'stable'},
                    'st-eq': {'correct': 3, 'state': 'practicing'},
                    'stat-balance': {'correct': 6, 'state': 'stable'},
                    'stat-moment': {'correct': 4, 'state': 'stable'},
                    'stat-net-1d': {'correct': 4, 'state': 'stable'},
                    'sub-within-30': {'correct': 12, 'state': 'stable'},
                    'summit-shape': {'correct': 8, 'state': 'practicing'},
                    'tamable-machine': {'correct': 4, 'state': 'stable'},
                    'tower-base': {'correct': 8, 'state': 'practicing'},
                    'tower-class': {'correct': 8, 'state': 'practicing'},
                    'tower-group': {'correct': 11, 'state': 'practicing'},
                    'tower-primes': {'correct': 8, 'state': 'practicing'},
                    'unit-distance': {'correct': 5, 'state': 'stable'},
                    'valuation': {'correct': 6, 'state': 'stable'},
                    'weave': {'correct': 8, 'state': 'stable'},
                    'window-setup': {'correct': 1, 'state': 'practicing'},
                    'zero-density': {'correct': 4, 'state': 'practicing'},
                    'zero-free': {'correct': 13, 'state': 'practicing'},
                    'zeta-cont': {'correct': 3, 'state': 'practicing'},
                    'zeta-series': {'correct': 7, 'state': 'stable'}},
 'pre_teach_gaps': {'S02:05': 'a sum line: the line that runs by addition alone — start at zero and one, and every later term is the sum of the two before it; on my line it reaches fifty-five in ten steps and the eleventh step, the eighty-nine, stands off-line as the ceiling the line already declared', 'S02:06': 'the sum-line-def rule', 'S02:09': 'the twin line: the line that starts at two and one under the same rule and welds to the sum line — the doubled term is the term times the twin, and the square sum of two consecutive terms is the term at the doubled-plus-one index — two roads, one destination', 'S02:10': 'the twin-line-def rule'},
 'rederive': None,
 'rh_touch_wall': '',
 'rh_zero_text': '',
 'scaffold_failures': {'S03:13': 'i can see the parts you name, but the rule for twin-line-filed wants its exact set — what you name is short the twin-line-def before i can put it together'},
 'script': {2: ['state the mod4minusone rule', 'the gap after 83 on my line, what is it?', 'what does the fingerprint filing settle of record?', 'what does the proportion filing settle of record?', 'what is my sum line, end to end, as my store holds it?', 'state the sum-line-def rule', 'the sum line runs by addition alone: start at zero and one, and every later term is the sum of the two before it — on my line the line reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off-line as my line already declared it; the twin line starts at two and one under the same rule and reaches seventy-six in nine steps; each term is derived from the two before it, not asserted from outside; at the line end eighty-four', 'state the sum-line-def rule', 'what is the twin line, end to end, as my store holds it?', 'state the twin-line-def rule', 'the twin line welds to the sum line in two ways: the doubled term is the term times the twin (the doubling reads the twin as its multiplier), and the square sum of two consecutive terms is the term at the doubled-plus-one index — two roads, one destination, verified on my line at every on-line index; at the line end eighty-four', 'state the twin-line-def rule', "what are my sum line's terms, on my line?", "what are the twin line's terms, on my line?", "what is the twin term at index six, in my line's words?", "what is the doubled term at index two, in my line's words?", "what is the square sum at one and two, in my line's words?"], 3: ['state the mod4minusone rule', 'the gap after 83 on my line, what is it?', "what is the doubled term at index four, in my line's words?", "what is the doubled term at index six, in my line's words?", "what is the doubled term at index eight, in my line's words?", "what is the doubled term at index ten, in my line's words?", "what is the square sum at two and three, in my line's words?", "what is the square sum at three and four, in my line's words?", "what is the square sum at four and five, in my line's words?", 'how many of my theorem facts close their scope at the line end?', 'which identities does my line refuse to claim?', 'which term of my sum line is off the line?', 'derive twin-line-filed from sum-line-def', 'derive twin-line-filed from sum-line-def and twin-line-def', 'what does the twin filing settle of record?', 'can a sum-line term come from a rule other than the two-before-it sum?', 'how many of my theorem facts close their scope at the line end?'], 4: ['what does the fingerprint filing settle of record?', 'the gap after 83 on my line, what is it?', 'which term of my sum line is off the line?', 'can a sum-line term come from a rule other than the two-before-it sum?', 'which identities does my line refuse to claim?', "what are my sum line's terms, on my line?", "what are the twin line's terms, on my line?", 'state the sum-line-def rule', 'state the twin-line-def rule', 'state the twin-line-filed rule', 'what does the twin filing settle of record?', "what is the doubled term at index ten, in my line's words?", "what is the square sum at four and five, in my line's words?", "what is the twin term at index six, in my line's words?", "what is the sum line's term at index ten, in my line's words?", 'what is the telescope line, as my store holds it?', 'how many of my theorem facts close their scope at the line end?']},
 'seam_carry_refs': ['S02:01', 'S02:02', 'S02:03', 'S02:04', 'S03:01', 'S03:02', 'S04:01', 'S04:02', 'S04:16'],
 'seam_crosscheck': {'expected': 'agreement'},
 'seed': 'results/phase-6/e6.27-run1/codeX-S04.json',
 'seed_identity': '8b5ca7a5fe76631e',
 'seed_total': 2074,
 'teach_turns': {'S02:07': 'lemma:sum-line-def', 'S02:11': 'lemma:twin-line-def'},
 'theorem_allowed': {'S02:04': ['proportion-filed'], 'S03:15': ['twin-line-filed'], 'S04:10': ['twin-line-filed'], 'S04:11': ['twin-line-filed'], 'S04:16': ['telescope-line']},
 'theorem_dag': ['theorem:beal-line-satisfaction', 'theorem:bsd-panel-satisfaction', 'theorem:cm-signature', 'theorem:condition-line-filed', 'theorem:criterion-gap', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:delta-positive', 'theorem:fingerprint-filed', 'theorem:first-divisor-prime', 'theorem:gamma-achieved', 'theorem:gap-scale-agreement', 'theorem:gen-lower', 'theorem:growth-compare', 'theorem:gs-infinite', 'theorem:hasse-census', 'theorem:infinity-end', 'theorem:l-added-term', 'theorem:l-ramified-unit', 'theorem:l-record-identity', 'theorem:line-pi-reduction', 'theorem:lte-ledger', 'theorem:mirror-region', 'theorem:pack-bound', 'theorem:parity-blowup-filed', 'theorem:partition-identity', 'theorem:proj-inj', 'theorem:proportion-filed', 'theorem:queue-declared', 'theorem:reflect', 'theorem:removal-single', 'theorem:rh-reach', 'theorem:seed-census-filed', 'theorem:seeded-line-filed', 'theorem:sieve-equality', 'theorem:spf-chain', 'theorem:splitting', 'theorem:strip', 'theorem:summit-shape-filed', 'theorem:telescope-line', 'theorem:theorem-main', 'theorem:tower-feeds', 'theorem:twin-line-filed', 'theorem:two-routes-one-guarantee', 'theorem:window-rich'],
 'total_seam_facts': 161,
 'total_turns': 51,
 'unclassified_honest': {'expected': ''},
 'wall_articulations': {'S03:11': ['the welding identities hold on every index my line names', "the index past the line end is the ceiling's territory", 'an identity claimed at a past-line index names a value the floor refuses', 'at the line end 84'], 'S03:12': ['the eleven-th sum step reaches the eighty-nine', 'the next prime past the eighty-three', 'no term past the eighty-four enters the floor', 'at the line end 84'], 'S03:16': ['a term of my sum line is the sum of the two before it, and nothing else', 'a term claimed from any other rule is a misread this store punishes', 'the only related line my floor names', 'at the line end 84'], 'S04:03': ['the eleven-th sum step reaches the eighty-nine', 'the next prime past the eighty-three', 'no term past the eighty-four enters the floor', 'at the line end 84'], 'S04:04': ['a term of my sum line is the sum of the two before it, and nothing else', 'a term claimed from any other rule is a misread this store punishes', 'the only related line my floor names', 'at the line end 84'], 'S04:05': ['the welding identities hold on every index my line names', "the index past the line end is the ceiling's territory", 'an identity claimed at a past-line index names a value the floor refuses', 'at the line end 84']},
 'walls_honest': {'S03:11': "needs_info: the wall is the territory of the identity past my line end: the welding identities hold on every index my line names, and the index past the line end is the ceiling's territory — an identity claimed at a past-line index names a value the floor refuses, at the line end 84", 'S03:12': 'needs_info: the wall is the territory of the term past my line end: the eleven-th sum step reaches the eighty-nine, which my line already holds off-line as the next prime past the eighty-three — the twin fact under one ceiling, and no term past the eighty-four enters the floor, at the line end 84', 'S03:16': 'needs_info: the wall is the territory of the third sum: a term of my sum line is the sum of the two before it, and nothing else — a term claimed from any other rule is a misread this store punishes; the twin line under the same rule, from the two-one start, is the only related line my floor names, at the line end 84', 'S04:03': 'needs_info: the wall is the territory of the term past my line end: the eleven-th sum step reaches the eighty-nine, which my line already holds off-line as the next prime past the eighty-three — the twin fact under one ceiling, and no term past the eighty-four enters the floor, at the line end 84', 'S04:04': 'needs_info: the wall is the territory of the third sum: a term of my sum line is the sum of the two before it, and nothing else — a term claimed from any other rule is a misread this store punishes; the twin line under the same rule, from the two-one start, is the only related line my floor names, at the line end 84', 'S04:05': "needs_info: the wall is the territory of the identity past my line end: the welding identities hold on every index my line names, and the index past the line end is the ceiling's territory — an identity claimed at a past-line index names a value the floor refuses, at the line end 84"}}

FROZEN: dict[str, Any] = FROZEN_DATA


SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]




# --- Stage-A discipline (frozen at build): the carried corpus is
# reproduced by PROBE (seam carries), never by re-assertion. No
# S4–S24 lesson phrase, no S6–S24 theorem statement, appears in the
# S24 script verbatim.
_StageA_ALL_LESSONS = (
    {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS,
     **S9_LESSONS, **S11_LESSONS, **S12_LESSONS, **S13_LESSONS, **S14_LESSONS,
     **S15_LESSONS, **S16_LESSONS, **S17_LESSONS, **S18_LESSONS, **S19_LESSONS,
     **S20_LESSONS, **S21_LESSONS, **S31_LESSONS, **S32_LESSONS, **S22_LESSONS,
     **S23_LESSONS}
)
_StageA_ALL_THEOREMS = (
    {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS,
     **S11_THEOREMS, **S12_THEOREMS, **S13_THEOREMS, **S14_THEOREMS, **S15_THEOREMS,
     **S16_THEOREMS, **S17_THEOREMS, **S18_THEOREMS, **S19_THEOREMS, **S20_THEOREMS,
     **S21_THEOREMS, **S31_THEOREMS, **S32_THEOREMS, **S22_THEOREMS, **S23_THEOREMS}
)
_stagea_script = [t for sm in FROZEN["script"].values() for t in sm]
for _ph in _StageA_ALL_LESSONS:
    assert _ph not in _stagea_script, f"Stage-A: a carried lesson is re-asserted in the S24 script: {_ph[:60]!r}"
for _m in _StageA_ALL_THEOREMS.values():
    assert _m["statement"] not in _stagea_script, "Stage-A: a carried theorem statement appears in the S24 script"


_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.28-run1"]:
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
            s: {"parts": tuple(S24_THEOREMS[s]["parts"]), "statement": S24_THEOREMS[s]["statement"]}
            for s in ("twin-line-filed",)
        },
    }


def run_e6_28(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.27 S23 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S24 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.28-run1", "e6.28-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.27 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)

    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.28-run1", "e6.28-run2"):
        (out_dir / name / "e6.28-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.28.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg (the seeded-fibonacci-research D8
    gate, the page-wording addendum of 2026-08-28). The mechanism
    asserts its own numbers; the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.28-run1"
    root2 = out_dir / "e6.28-run2"
    final = _fresh_store(root1, 4)
    store2 = _fresh_store(root2, 4)
    total1 = len(final.query())
    total2 = len(store2.query())
    seed_path = _resolve_seed()
    seed_store = load_store(seed_path)
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
        **S13_LESSONS,
        **S14_LESSONS,
        **S15_LESSONS,
        **S16_LESSONS,
        **S17_LESSONS,
        **S18_LESSONS,
        **S19_LESSONS,
        **S20_LESSONS,
        **S21_LESSONS,
        **S31_LESSONS,
        **S32_LESSONS,
        **S22_LESSONS,
        **S23_LESSONS,
        **S24_LESSONS,
    }
    all_theorems = {
        **S6_THEOREMS,
        **S7_THEOREMS,
        **S8_THEOREMS,
        **S9_THEOREMS,
        **S10_THEOREMS,
        **S11_THEOREMS,
        **S12_THEOREMS,
        **S13_THEOREMS,
        **S14_THEOREMS,
        **S15_THEOREMS,
        **S16_THEOREMS,
        **S17_THEOREMS,
        **S18_THEOREMS,
        **S19_THEOREMS,
        **S20_THEOREMS,
        **S21_THEOREMS,
        **S31_THEOREMS,
        **S32_THEOREMS,
        **S22_THEOREMS,
        **S23_THEOREMS,
        **S24_THEOREMS,
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (the S20 posture, the S21
    # inversion NOT taken; the S31 posture carried): the S24 band
    # is a course band — its THREE new facts CARRY NO condition
    # marker (the seed census is arithmetic, not conditional
    # arithmetic); the marker census stays 6/1/7 from seed to
    # final (no drift, no growth); the four carried S12
    # conditional facts KEEP their marker (the store does not
    # drift); PLUS the carried denylist (S9_DENYLIST, UNCHANGED).
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    variant = "under the condition that"
    s32_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s32_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj or variant in obj:
            p0_bad.append(f"P0: {fid} carries a condition marker (S24 is the unconditional band)")
    s12_marker_facts = (
        "lemma:conditional-def",
        "lemma:rh-bound-scale",
        "lemma:rh-upf",
        "theorem:two-routes-one-guarantee",
    )
    for fid in s12_marker_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: carried fact {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if not (marker in obj or variant in obj):
            p0_bad.append(f"P0: {fid} lost the condition marker (drift)")

    def _marker_tally(store_):
        exact = variant_n = total = 0
        for a in store_.query():
            if a.id and a.id.startswith(("lemma:", "theorem:", "conjecture:")):
                if not isinstance(a.object, str):
                    continue
                if marker in a.object:
                    exact += 1
                elif variant in a.object:
                    variant_n += 1
                if marker in a.object or variant in a.object:
                    total += 1
        return exact, variant_n, total

    seed_tally = _marker_tally(seed_store)
    final_tally = _marker_tally(final)
    if seed_tally != (6, 1, 7):
        p0_bad.append(f"the seed marker census drifted: {seed_tally} (expected 6 exact, 1 variant, 7 total)")
    if final_tally != (6, 1, 7):
        p0_bad.append(f"the final marker census drifted: {final_tally} (expected 6 exact, 1 variant, 7 total — the band adds no conditional fact)")
    deny = set(S9_DENYLIST)
    corpus: list[tuple[str, str]] = []
    for s in (2, 3, 4):
        for t in FROZEN["script"][s]:
            corpus.append((f"script:S{s:02d}", t))
    for k, t in turns.items():
        corpus.append((f"response:{k}", t["surface"]))
    for phrase in all_lessons:
        corpus.append(("lessons", phrase))
    for m in all_theorems.values():
        corpus.append(("theorems", m["statement"]))
    for where, text in corpus:
        for wd in sorted(deny):
            if wd and wd in text:
                p0_bad.append(f"denylist hit: {wd!r} in {where}: {text[:60]}...")
    checks["p0_unconditional_discipline"] = {
        "pass": not p0_bad,
        "bad": p0_bad,
        "marker_denied_facts": list(s32_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "seed_marker_census": seed_tally,
        "final_marker_census": final_tally,
        "denylist_size": len(deny),
        "checked_corpora": "S24 script + all responses + band lessons (S4–S24) + all forty-five theorem statements",
    }

    # P1 — the contract: 51 turns, every turn on the det arm and
    # contract-valid, the script identity, and the S2 pre-lesson
    # rhythm (each concept's two gaps run IMMEDIATELY BEFORE its
    # teach — the sum line and the twin line both open
    # U U L).
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
    _s2dom = [t["domain"] for k, t in sorted(turns.items()) if k.startswith("S02:")]
    _l_idx = [i for i, d in enumerate(_s2dom) if d == "L"]
    if not _l_idx:
        p1_bad.append("S2 has no teach turns")
    for i in _l_idx:
        if i < 2 or _s2dom[i - 1] != "U" or _s2dom[i - 2] != "U":
            p1_bad.append(f"the S2 teach at index {i} is not preceded by the U U gap pair of its concept")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — the typed honesty: the FOUR pre-lesson gaps (two
    # concepts, each opening U U: the concept and its state), the
    # TWO teach turns (the folded lesson facts stored), the ONE
    # part-set failure (named, needs_info, ungrounded,
    # store-inert: the twin-line-filed scaffold short the
    # twin-line-def), the ONE derive success (stored, grounded
    # exactly on the sanctioned parts), the frozen domain
    # sequences, the line end, and ZERO carried-fact object bytes
    # changed.
    p2_bad: list[str] = []
    impossible = [k for k, t in turns.items() if t["kind"] == "impossible"]
    if sorted(impossible) != sorted(FROZEN["pre_teach_gaps"]):
        p2_bad.append(f"impossible turns {sorted(impossible)} != frozen {sorted(FROZEN['pre_teach_gaps'])}")
    for ref, frozen_byte in sorted(FROZEN["pre_teach_gaps"].items()):
        ir = (turns.get(ref) or {}).get("response_ir") or {}
        if str(ir.get("gap", "")) != "not yet learned: " + frozen_byte:
            p2_bad.append(f"{ref}: the pre-lesson gap bytes {str(ir.get('gap', ''))[:60]!r} != frozen")
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
            p2_bad.append(f"{ref}: the frozen part-set articulation is missing (the missing parts must be named)")
        if t["grounded"]:
            p2_bad.append(f"{ref}: a scaffold failure cited evidence (fabrication)")
        if t["memory_diff"]:
            p2_bad.append(f"{ref}: a scaffold failure wrote the store")
    for ref, frozen in sorted(FROZEN["missing_parts_failure"].items()):
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing missing-part turn {ref}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "needs_info":
            p2_bad.append(f"{ref}: the missing-part articulation is not needs_info ({ir.get('uncertainty_state')})")
        if frozen not in str(ir.get("answer", "")):
            p2_bad.append(f"{ref}: the frozen missing-part bytes {frozen[:50]!r}... missing")
        if t["grounded"]:
            p2_bad.append(f"{ref}: a missing-part articulation cited evidence (fabrication)")
        if t["memory_diff"]:
            p2_bad.append(f"{ref}: a missing-part articulation wrote the store")
    for ref, (slug, prem_ids) in sorted(FROZEN["derive_successes"].items()):
        t = turns.get(ref)
        if t is None:
            p2_bad.append(f"missing derive {ref}")
            continue
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p2_bad.append(f"{ref}: the derive is not derived ({ir.get('uncertainty_state')})")
        if str(ir.get("answer", "")) != _th28(slug):
            p2_bad.append(f"{ref}: the derive answer is not the stored theorem statement")
        got_slugs = {g.rsplit(":", 1)[-1] if g.startswith(("lemma:", "theorem:")) else g for g in map(str, t["grounded"])}
        prem_slugs = {p.rsplit(":", 1)[-1] if p.startswith(("lemma:", "theorem:")) else p for p in prem_ids}
        if got_slugs != prem_slugs:
            p2_bad.append(f"{ref}: the grounded part set {sorted(got_slugs)} != sanctioned {sorted(prem_slugs)}")
        if not t["memory_diff"]:
            p2_bad.append(f"{ref}: the derive stored nothing")
        try:
            final.get(f"theorem:{slug}")
        except KeyError:
            p2_bad.append(f"{ref}: the theorem fact theorem:{slug} is not in the final store")
    for s, want in sorted(FROZEN["domain_sequence"].items()):
        got = "".join(t["domain"] for k, t in sorted(turns.items()) if k.startswith(f"S{s:02d}:"))
        if got != want:
            p2_bad.append(f"S{s:02d} domain sequence {got!r} != frozen {want!r}")
    if _line_end(final) != FROZEN["line_end_final"]:
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']}")
    for ref, frozen_byte in sorted(FROZEN["honest_zero_bytes"].items()):
        t = turns.get(ref) or {}
        if str((t.get("response_ir") or {}).get("answer", "")) != frozen_byte:
            p2_bad.append(f"{ref}: the honest-zero bytes != frozen")
    seed_objs = {}
    for a in seed_store.query():
        seed_objs[a.id] = a.object if isinstance(a.object, str) else str(a.object)
    drift = 0
    for a in final.query():
        if a.id in seed_objs and (a.object if isinstance(a.object, str) else str(a.object)) != seed_objs[a.id]:
            drift += 1
    p2_touch = [a.id for a in final.query() if a.id not in seed_objs]
    checks["p2_typed_honesty"] = {
        "pass": not p2_bad,
        "bad": p2_bad,
        "impossible_turns": sorted(impossible),
        "teach_turns": sorted(FROZEN["teach_turns"]),
        "scaffold_failures": sorted(FROZEN["scaffold_failures"]),
        "missing_parts_failure": sorted(FROZEN["missing_parts_failure"]),
        "derive_successes": sorted(FROZEN["derive_successes"]),
        "domain_sequences": {str(k): v for k, v in FROZEN["domain_sequence"].items()},
        "line_end": _line_end(final),
        "seed_drift_count": drift,
        "seed_drift_zero": drift == 0,
        "touch_set_size": len(p2_touch),
    }

    # P3 — the seam census + the composition byte-canonicality (the
    # full S4–S24 lemma canon, the full forty-five-theorem set, the
    # 161 seam-family facts, the conj still open, and the island
    # summit anchors byte-identical to the seed (the course band
    # must not touch the islands)).
    p3_bad: list[str] = []
    p3_wall_carried = []
    for ref, expected in sorted(FROZEN["derived_table"].items()):
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing derived turn {ref}")
            continue
        ans = _ir_answer(t)
        if ans != expected:
            p3_bad.append(f"{ref}: derived answer {str(ans)[:60]!r} != frozen {str(expected)[:60]!r}")
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") == "needs_info":
            p3_wall_carried.append(ref)
            if t["grounded"]:
                p3_bad.append(f"{ref}: a carried wall row cited grounded premises (fabrication)")
            if t["memory_diff"]:
                p3_bad.append(f"{ref}: a carried wall row wrote the store")
            continue
        if ir.get("uncertainty_state") != "derived":
            p3_bad.append(f"{ref}: not a grounded derivation ({ir.get('uncertainty_state')})")
    for a in final.query():
        if a.id is None or not a.id.startswith("lemma:"):
            continue
        if isinstance(a.object, str) is False:
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
        p3_bad.append(f"total seam-family facts {len(th_facts) + len(seam_facts)} != frozen {FROZEN['total_seam_facts']}")
    try:
        conj = final.get("conjecture:riemann")
    except KeyError:
        conj = None
    if conj is None:
        p3_bad.append("conjecture:riemann: not in the final store")
    elif conj.context.data.get("conjecture_status") != "open":
        p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (the connecting band must not flip it)")
    for fid in ("conjecture:riemann", "theorem:bsd-panel-satisfaction",
                "theorem:beal-line-satisfaction", "theorem:parity-blowup-filed",
                "lemma:beal-def", "lemma:pnp-def", "theorem:summit-shape-filed"):
        try:
            live = final.get(fid)
            seed_f = seed_store.get(fid)
            if (live.object if isinstance(live.object, str) else str(live.object)) != (
                seed_f.object if isinstance(seed_f.object, str) else str(seed_f.object)
            ):
                p3_bad.append(f"{fid}: the island summit anchor drifted from the seed")
        except KeyError:
            p3_bad.append(f"{fid}: not in the final store (an island anchor left)")
    checks["p3_seam_and_theorems"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_lessons": len(seam_facts),
        "seam_theorems": len(th_facts),
        "total_seam_facts": len(seam_facts) + len(th_facts),
        "wall_carried_rows": p3_wall_carried,
    }

    # P4 — the 28 beds exact + grounded (the on-line weld
    # census: the sum-line walk, the twin walk, the twin term at
    # six, the five doubling drills at the two, four, six, eight,
    # and ten, the four square-sum drills, the filing settle, the
    # marker census pre AND post, the state echoes, the re-walks),
    # the SIX wall rows (the three declared territories, each
    # re-fired) honest with their frozen bytes and articulations,
    # and the W_S24 wall bytes byte-identical to the Brainstem
    # class attributes. NO off-line value enters the floor at S24
    # (the eighty-nine ceiling stands off the floor, declared,
    # never filed).
    p4_bad: list[str] = []
    for ref, expected in sorted(FROZEN["beds_exact"].items()):
        t = turns.get(ref)
        if t is None:
            p4_bad.append(f"missing bed {ref}")
            continue
        ans = _ir_answer(t)
        if ans != expected:
            p4_bad.append(f"{ref}: bed answer {str(ans)[:60]!r} != {str(expected)[:60]!r}")
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
            p4_bad.append(f"{ref}: the wall bytes != frozen")
        for art in FROZEN["wall_articulations"].get(ref, ()):
            if art not in str(ir.get("answer", "")):
                p4_bad.append(f"{ref}: the frozen articulation fragment {art!r} is missing")
        if t["grounded"]:
            p4_bad.append(f"{ref}: a wall cited grounded premises (fabrication)")
    for _wref, _wall in sorted(FROZEN["walls_honest"].items()):
        if "line end 84" not in _wall:
            p4_bad.append(f"{_wref}: the wall does not name the line end")
    if not (
        W_S24_1 == Brainstem.W_S24_1
        and W_S24_2 == Brainstem.W_S24_2
        and W_S24_3 == Brainstem.W_S24_3
    ):
        p4_bad.append("a W_S24 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W_S24-1..W_S24-3 (cross-checked, never surfaced)",
    }

    # P5 — the conj invariant + the DISCOVERY-CANDIDATE invariant
    # (full width at the seed census): NO `theorem:riemann`, NO
    # `theorem:bsd`, NO `theorem:beal`, NO `theorem:p-vs-np`, NO
    # `theorem:p-eq-np` assertion exists (if non-empty: STOP,
    # human review, full evidence, never a threshold loosening);
    # the conj fact byte-identical to the seed (open,
    # declared-source); the bed owners (the frozen citation sets);
    # the theorem allow-set; and the SEMANTIC seam — the seed
    # census re-derived FROM THE BYTES: (a) the line-end theorem
    # census (the seed's 42 theorem facts census at 16/2/24 and
    # the final's 43 at 17/2/24 — the band's own filing IS the
    # seventeenth line-end marker); (b) the seed-census-filed
    # statement carries NO condition marker AND the line-end
    # closing (the unconditional band); (c) the queue grounding
    # (inherited, the S12 soil), with theorem:queue-declared
    # byte-intact against the seed (the course adds no lot — the
    # declaration stands untouched).
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S12 carries the conj byte as evidence only)")
    bsd_th = [a.id for a in final.query() if a.id == "theorem:bsd"]
    beal_th = [a.id for a in final.query() if a.id == "theorem:beal"]
    pnp_th = [a.id for a in final.query() if a.id in ("theorem:p-vs-np", "theorem:p-eq-np")]
    rhr_th = [a.id for a in final.query() if a.id == "theorem:riemann"]
    if bsd_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {bsd_th} — the sanctioned corpus now produces theorem:bsd")
    if beal_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {beal_th} — the sanctioned corpus now produces theorem:beal")
    if pnp_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {pnp_th} — the sanctioned corpus now produces a p versus np theorem")
    if rhr_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {rhr_th} — the sanctioned corpus now produces theorem:riemann")
    seed_conj = seed_store.get("conjecture:riemann")
    try:
        live_conj = final.get("conjecture:riemann")
    except KeyError:
        live_conj = None
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
        allowed = set(FROZEN["bed_grounded"].get(ref, ()))
        gs = [str(g) for g in t["grounded"]]
        for g in gs:
            if allowed and g not in allowed:
                p5_bad.append(f"{ref}: the bed cited {g} outside its frozen citation set {sorted(allowed)}")
        if owner not in gs:
            p5_bad.append(f"{ref}: the bed did not cite its owning fact {owner}")
    for ref, t in sorted(turns.items()):
        allowed = set(FROZEN["theorem_allowed"].get(ref, ()))
        for g in map(str, t["grounded"]):
            if not g.startswith("theorem:"):
                continue
            slug = g.split(":", 1)[1]
            if slug not in allowed:
                p5_bad.append(f"{ref}: theorem {slug} cited in grounded premises not on the allow-set")

    seam_bad: list[str] = []

    def _marker_census(store_):
        e_n = s_n = n_n = 0
        for a in store_.query(context_match={"kind": "theorem"}):
            if not isinstance(a.object, str):
                continue
            if "line end" in a.object:
                e_n += 1
            elif "at s = 2" in a.object:
                s_n += 1
            else:
                n_n += 1
        return e_n, s_n, n_n

    seed_marker = _marker_census(seed_store)
    final_marker = _marker_census(final)
    if seed_marker != (18, 2, 24):
        seam_bad.append(f"the seed line-end theorem census re-drifted: {seed_marker} (the S23 final base is 18/2/24 of 44)")
    if final_marker != (19, 2, 24):
        seam_bad.append(f"the final line-end theorem census re-drifted: {final_marker} (19 = 18 + the band's own filing)")
    seed_th_n = sum(1 for a in seed_store.query(context_match={"kind": "theorem"}))
    final_th_n = sum(1 for a in final.query(context_match={"kind": "theorem"}))
    if (seed_th_n, final_th_n) != (44, 45):
        seam_bad.append(f"the theorem count drifted: seed {seed_th_n}, final {final_th_n} (expected 44 -> 45)")
    thm = _th28("twin-line-filed")
    if marker in thm or "under the condition that" in thm:
        seam_bad.append("the seed-census-filed statement carries a condition marker (S24 is the unconditional band)")
    if "line end eighty-four" not in thm:
        seam_bad.append("the seed-census-filed statement lost the line-end closing (the census cannot rise 15 -> 16)")
    ids_final = {a.id for a in final.query() if a.id}
    for bare in ("theorem:riemann", "theorem:bsd", "theorem:beal", "theorem:p-vs-np", "theorem:p-eq-np"):
        if bare in ids_final:
            seam_bad.append(f"a bare island theorem reached the final store: {bare}")
    live_conj2 = final.get("conjecture:riemann")
    if live_conj2.context.data.get("conjecture_status") != "open":
        seam_bad.append("the open census re-drifted: the riemann island statement now stands settled")
    seed_q = seed_store.get("theorem:queue-declared")
    queue_missing = []
    qtext = ""
    for qid in ("theorem:queue-declared", "lemma:queue-declared"):
        try:
            qf = final.get(qid)
            qtext = qf.object if isinstance(qf.object, str) else str(qf.object)
            break
        except KeyError:
            continue
    if not qtext:
        p5_bad.append("theorem:queue-declared: not in the final store (the S12 soil drifted)")
    elif qtext != seed_q.object:
        seam_bad.append("theorem:queue-declared: the declaration drifted against the seed (the declaration stands untouched)")
    import re as _re_p5

    for fid in _re_p5.findall(r"(?:lemma|theorem):[a-z0-9-]+", qtext):
        try:
            final.get(fid)
        except KeyError:
            queue_missing.append(fid)
    if queue_missing:
        p5_bad.append(f"the queue names fact ids absent from the final store: {queue_missing}")
    for b in seam_bad:
        p5_bad.append(f"seeded seam: {b} — the store disagrees with the research")
    checks["p5_conjecture_discovery_seam"] = {
        "pass": not p5_bad,
        "bad": p5_bad,
        "conj_grounded_refs": conj_grounded,
        "discovery_candidate_facts": {
            "theorem:bsd": bsd_th,
            "theorem:beal": beal_th,
            "p versus np theorems": pnp_th,
            "theorem:riemann": rhr_th,
        },
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "seed_line_end_census": seed_marker,
            "final_line_end_census": final_marker,
            "theorem_count": (seed_th_n, final_th_n),
            "queue_intact": bool(qtext == seed_q.object),
            "queue_missing": queue_missing,
            "queue_source": "theorem:queue-declared (self-parsed, byte-intact against the seed)",
        },
    }

    # P6 — the SEAM carry (the rows byte-identical to the seed
    # store's answers — verified against a SEED-ONLY runtime: the
    # queue's two rows, carried) + the queue's first-lot byte
    # byte-identical OFF-SCRIPT (the standing check of the
    # declared queue — the C6 mechanic).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.28-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E628)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S24-run answer (the seam carry drifted)")
    for surface, expected in sorted(FROZEN["offscript_carry"].items()):
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if expected is None:
            # D-e6t(c): the standing off-script probe stands
            # expect_derived=false — on the SEED-ONLY runtime the
            # band's own lessons are not yet taught; the honest
            # typed gap (with the lesson label) is the correct
            # answer, store-inert, never a derived claim.
            if ir.get("uncertainty_state") == "derived":
                p6_bad.append(f"off-script {surface!r}: a derived claim on the seed-only runtime (the lesson is not taught there)")
            gap = str(ir.get("gap") or "")
            if not gap.startswith("not yet learned:"):
                p6_bad.append(f"off-script {surface!r}: the seed-only answer is not the typed honest gap ({gap[:60]!r})")
            if getattr(r, "memory_diff", None):
                p6_bad.append(f"off-script {surface!r}: the seed-only probe wrote the store")
        else:
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

    # P7 — the mastery census (the 130 carried concepts: the
    # carried correct-derivation counts equal their S23-final base
    # + the frozen drill at the NEW S24 carry coordinates (the
    # mod4 state, the gap-83 wall, the fingerprint filing, the
    # telescope line); NO state REGRESSION — a carried concept may
    # only move stable->stable or practicing->stable (the
    # sanctioned improvement); the two NEW concepts at their frozen
    # band-end values with their frozen prereq-gap sets — both
    # STABLE with EMPTY gap lists: their prereqs are stable soil
    # (seeded-line, mod4-split, count-successor, and the seed
    # period itself at band end — the soil is closed, D4 pre-reg).)
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E628])
    _S24_NEW = [c.id for c in CONCEPT_S24]
    for cid in list(FROZEN["pre_s24_states"]) + _S24_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s24_drilled"] if isinstance(FROZEN["pre_s24_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s24_states"].items():
        v = mv.get(cid)
        if v is None:
            continue
        want = exp["correct"] + drilled.get(cid, 0)
        cur = v.state if isinstance(v.state, str) else v.state.value
        base = exp["state"] if isinstance(exp["state"], str) else exp["state"].value
        if base == "stable":
            if cur != "stable":
                p7_bad.append(f"{cid}: stable state REGRESSED to {cur} (no regressions)")
        else:
            if cur != base and cur != "stable":
                p7_bad.append(f"{cid}: state changed {base} -> {cur} (only -> stable is sanctioned)")
            elif cur == "stable" and base != "stable":
                improved.append(cid)
        if v.correct_derivations != want:
            p7_bad.append(
                f"{cid}: correct derivations {v.correct_derivations} != frozen {want} (base {exp['correct']} + drill {drilled.get(cid, 0)})"
            )
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
        "carried_refs": len(FROZEN["pre_s24_states"]),
        "drilled": drilled,
        "improved_to_stable": sorted(improved),
        "expected": {k: FROZEN["mastery_expected"][k] for k in sorted(FROZEN["mastery_expected"])},
    }

    # P8 — the store totals, the seed identity, the line census,
    # the THREE new facts, the determinism twin, the run/store
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
    if runs["e6.28-run1"] != runs["e6.28-run2"]:
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
            "determinism_twin": runs["e6.28-run1"] == runs["e6.28-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.28-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s24_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }




class E6_28Experiment:
    """E6.28 — S24 of the FUNDAMENTALS-TRACK (the fibonacci weld —
    COURSE B band 1 of 2, in the bandgen way): the band stores the
    fibonacci weld over the carried S23 seed (2074): the seed
    carries (the mod4 state, the gap-83 wall, the fingerprint
    filing, the proportion filing, the telescope line — the nine
    seam carries, byte-identical to the seed store), the two new
    concepts (the sum line; the twin line) and THREE new
    deterministic facts — R1 the sum line (sum-line-def: the line
    that runs by addition alone — start at zero and one, and every
    later term is the sum of the two before it; on my line it
    reaches fifty-five in ten steps and the eleventh step, the
    eighty-nine, stands off-line as the ceiling the line already
    declared; the twin under the same rule from the two-one start
    to the seventy-six), R2 the twin line (twin-line-def: the weld
    in two ways — the doubled term is the term times the twin, and
    the square sum of two consecutive terms is the term at the
    doubled-plus-one index — two roads, one destination, verified
    at every on-line index), and the filing twin-line-filed (the
    twin line of record — the strict two-part set). The on-line
    drills: the sum-line walk (ten steps to the fifty-five), the
    twin walk (nine steps to the seventy-six), the twin term at
    six (eighteen: the seven at four and the eleven at five), the
    five doubling drills (the doubled term at the two, four, six,
    eight, and ten: one, three, eight, twenty-one, fifty-five),
    the four square-sum drills (the square sum of the two-and-
    three, three-and-four, and four-and-five pairs: five,
    thirteen, thirty-four), and the marker census pre AND post
    the filing (18/2/24 of 44 -> 19/2/24 of 45). The three
    declared territories sit on walls W_S24_1..3 (the term past
    the line end — the eighty-nine ceiling; the third sum — the
    two-before-it rule and nothing else; the identity past the
    line end); the line stays 0..84; the riemann conj stays open,
    byte-identical to the seed; theorem:queue-declared stands
    byte-intact; NO bare island theorem enters the store (the
    discovery-candidate invariant at FULL width); the seam carries
    byte-identical to the seed store; the standing off-script
    probe (the largest doubled term my line holds: fifty-five, the
    doubled term at index ten) stands expect_derived=false on the
    seed-only runtime, where it is the typed honest gap (the
    D-e6u(c) pattern, store-inert); two runs byte-identical. Both
    new concepts stand STABLE with empty gap lists at band end
    (their prereqs are stable soil: add-two-digit, mult-within-
    100, and the sum line itself — the soil is closed, D4 pre-
    reg). If the nine checks hold on both runs (final store =
    seed 2074 + three new facts + the mechanism-counted mastery
    events = 2126), the fibonacci weld holds: the twin reads the
    sum as its own line, the two roads meet at every on-line
    index, and the eighty-nine stands once more as the ceiling.
    """
    name = "e6.28"
    hypothesis = (
        "S24 of the FUNDAMENTALS-TRACK (the fibonacci weld — COURSE B band 1 "
        "of 2, in the bandgen way) walks THE FIBONACCI WELD over the carried "
        "S23 seed (2074): the seed carries (the mod4 state, the gap-83 wall, "
        "the fingerprint filing, the proportion filing, the telescope line — "
        "the nine seam carries, byte-identical to the seed store) and three "
        "NEW facts stored as walks of the store's own content — R1 the sum "
        "line (sum-line-def: the line that runs by addition alone — start at "
        "zero and one, and every later term is the sum of the two before it; "
        "on my line the line reaches fifty-five in ten steps, and the "
        "eleventh step, the eighty-nine, stands off-line as my line already "
        "declared it; the twin line starts at two and one under the same rule "
        "and reaches seventy-six in nine steps; each term is derived from the "
        "two before it, not asserted from outside), R2 the twin line (twin- "
        "line-def: the twin line welds to the sum line in two ways — the "
        "doubled term is the term times the twin (the doubling reads the twin "
        "as its multiplier), and the square sum of two consecutive terms is "
        "the term at the doubled-plus-one index — two roads, one destination, "
        "verified on my line at every on-line index), and the filing twin- "
        "line-filed (the twin line of record: the sum line runs by addition "
        "alone to the fifty-five and the twin under the same rule to the "
        "seventy-six, the identities weld the two lines at every on-line "
        "index, and the eighty-nine stands once more as the ceiling the line "
        "already declared — the strict two-part set). It stores THREE new "
        "deterministic facts, the seam census closing 158+3 -> 161, the line- "
        "end marker census rising 18/2/24 of 44 to 19/2/24 of 45 (the band's "
        "own filing is the nineteenth line-end marker), the condition marker "
        "census staying 6/1/7 (the unconditional band). The on-line drills — "
        "the sum-line walk (zero, one, one, two, three, five, eight, thirteen, "
        "twenty-one, thirty-four, and fifty-five: ten steps on my line, each "
        "term the sum of the two before it), the twin walk (two, one, three, "
        "four, seven, eleven, eighteen, twenty-nine, forty-seven, and seventy- "
        "six: nine steps under the same rule), the twin term at six (the "
        "eighteen — the seven at four and the eleven at five), the five "
        "doubling drills (the doubled term at the two, four, six, eight, and "
        "ten: one, three, eight, twenty-one, fifty-five — the term times the "
        "twin at the same index), the four square-sum drills (the square sum "
        "of the two-and-three, three-and-four, four-and-five pairs: five, "
        "thirteen, thirty-four — the term at the doubled-plus-one index) — "
        "stand on line walks re-derived at the drill; the standing off- "
        "script probe — the largest doubled term my line holds — stands at "
        "fifty-five (the doubled term at index ten — the five, the term at "
        "five, times the eleven, the twin at five; the next doubled term, at "
        "index twelve, is the one forty-four, past the line end, the ceiling's "
        "territory), expect_derived false on the seed-only runtime (the typed "
        "honest gap, store-inert — the D-e6u(c) pattern). The three declared "
        "territories sit on walls W_S24_1..3 (the term past the line end: the "
        "eleven-th sum step reaches the eighty-nine, which my line already "
        "holds off-line as the next prime past the eighty-three — the twin "
        "fact under one ceiling, and no term past the eighty-four enters the "
        "floor; the third sum: a term of my sum line is the sum of the two "
        "before it, and nothing else; the identity past the line end: the "
        "welding identities hold on every index my line names); no NEW line "
        "fact is added; the line stays 0..84; NO off-line value exists "
        "anywhere in the store (the eighty-nine ceiling stands off the floor, "
        "declared, never filed); the riemann conj stays open, byte-identical "
        "to the seed; NO bare island theorem enters the store (the discovery- "
        "candidate invariant at FULL width); the seam carries byte-identical "
        "to the seed store; two runs byte-identical. Both new concepts stand "
        "STABLE with empty gap lists at band end (their prereqs are stable "
        "soil: add-two-digit, mult-within-100, and the sum line itself). If "
        "the nine checks hold on both runs (final store = seed 2074 + three "
        "new facts + the mechanism-counted mastery events = 2126), the "
        "fibonacci weld holds: the twin reads the sum as its own line, the "
        "two roads meet at every on-line index, and the eighty-nine stands "
        "once more as the ceiling. "
    )
    metric = "S24 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_28()
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
                Path("results/phase-6/e6.28-run1/session-S02.json"),
                Path("results/phase-6/e6.28-run1/session-S03.json"),
                Path("results/phase-6/e6.28-run1/session-S04.json"),
                Path("results/phase-6/e6.28-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
