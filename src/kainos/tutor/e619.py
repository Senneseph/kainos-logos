# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.19 — S15 of the PRIZE-ISLANDS-TRACK (the BSD island, band 2
of 3; built THE BANDGEN WAY): THE L-FUNCTION OF THE CITY.

The second band of the BSD island (plan/40-prize-islands/
04-island-bsd.md + the verified research record bsd-research.md,
stages A+B+C): the LOCAL-FACTOR layer of the two panel curves over
the carried S14 seed (1457). Four new concepts (euler-factor,
local-form, l-partial, l-correction — college-1, domain bsd,
prereqs point DOWN, cross-track at family-factor / line-partial —
the Riemann-island machinery IS the pattern: the islands connect),
four VERBATIM lessons (l-factor-def, l-local-def, l-partial-def,
l-corr-def), three sanctioned compositions (l-added-term,
l-record-identity, l-ramified-unit).

The story band 2 holds on the line: the factor each prime carries
(the uniform two-term form 1 - a_p/p + 1/p^2 at every prime; the
record's ONE-term form 1 - a_p/p at the ramified conductor primes —
the additive prime 2 for panel A where the coefficient is zero so
the record factor is the unit ONE, the multiplicative prime 37 for
panel B where the coefficient is minus one so the record factor is
one plus one over p), the L-partial as the exact rational product
the line holds (the added-term rule: the S13 removal rule inverted),
and the ramification correction (the record partial is the uniform
partial times the corrections, 4/5 and 1406/1407, both sides exact
at the line end 84). The separation is the lesson: panel B's record
and uniform partials agree through height 23 and separate exactly
at the conductor 37 by the hair 1406/1407; panel A's record partial
never moves at the ramified prime 2 (the unit factor), uniform
inflating by 5/4.

UNCONDITIONAL band: the order of vanishing at s = 1 (order zero for
A, order one for B — the analytic side of BSD's equation), the
convergence region, and the ranks live past the line and are named
OF RECORD on the five W-S15 walls, each naming the value and the
line end 84. NO `theorem:bsd` exists (the discovery-candidate
invariant, P5): the statement equating the order of vanishing to
the rank is the island's SUMMIT fact (band 3), not this band's.

FROZEN FROM CONTROL #1 (bandgen-era, 2026-08-24): the 54-turn
labeled script (S2:20 + S3:21 + S4:13), the 23 beds, the 5 walls,
and the predictions all come out of the mechanism's own dry-run
against the seed (spec bands/spec-e6.19.json; the control report
is the referee, never the hand). Deviations recorded at closeout:
D-e6j family (the pre-reg corrections this band forced: the
state-style gap bytes, the s15-form grounding on l-local-def so
the l-correction prereq lands stable, final 1522 = 1457 + 7 facts
+ 58 events).

No Ollama. No LLM. The mechanism speaks.
"""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    B14_A,
    B14_B,
    CONCEPT_S15,
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
    Brainstem,
    _bsd_py_lcorr,
    _bsd_py_lfactor,
    _bsd_py_Lpartial,
    _bsd_py_lpartial_record,
    _bsd_py_lpartial_uniform,
    _bsd_py_lspots,
    _s13_py_primes,
)
from kainos.tutor.e618 import (
    CONCEPTS_E618,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E619", "FROZEN", "E6_19Experiment", "run_e6_19"]

CHECKS = 9

#: S15 teaches: the L-function of the city (the four new concepts
#: join the carried registry; prereqs point DOWN only — the
#: cross-track edges at family-factor (S13) and line-partial (S13)
#: are the Riemann-island soil, where the islands connect).
CONCEPTS_E619: tuple = CONCEPTS_E618 + CONCEPT_S15

E618_SEED = Path("results/phase-6/e6.18-run1/codeX-S04.json")

def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E618_SEED.exists():
        return E618_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E618_SEED
    return alt if alt.exists() else E618_SEED

_ST15 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S15_LESSONS.items()}
_TH15 = {s: m["statement"] for s, m in S15_THEOREMS.items()}


def _th15(slug: str) -> str:
    return _TH15[slug]

#: P4 — the W-S15 walls (the off-line material names the value AND
#: the line end; the walls are the band's declared off-line layer —
#: P4 cross-checks the witness values against the mechanism's python
#: reference, never surfaced as answers).
W_S15_1 = Brainstem.W_S15_1
W_S15_2 = Brainstem.W_S15_2
W_S15_3 = Brainstem.W_S15_3
W_S15_4 = Brainstem.W_S15_4
W_S15_5 = Brainstem.W_S15_5


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
    rt = InfantRuntime(root, concepts=CONCEPTS_E619)
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
FROZEN_DATA = {'bed_grounded': {'S02:05': ['lemma:l-factor-def'], 'S02:06': ['lemma:l-factor-def'], 'S02:07': ['lemma:l-factor-def'], 'S02:08': ['lemma:l-factor-def'], 'S02:09': ['lemma:l-factor-def'], 'S02:14': ['lemma:l-partial-def'], 'S02:15': ['lemma:l-partial-def'], 'S02:16': ['lemma:l-partial-def'], 'S02:17': ['lemma:l-partial-def'], 'S03:04': ['lemma:l-local-def'], 'S03:05': ['lemma:l-local-def'], 'S03:09': ['lemma:l-corr-def'], 'S03:10': ['lemma:l-corr-def'], 'S03:11': ['lemma:l-corr-def'], 'S03:12': ['lemma:l-corr-def'], 'S03:15': ['lemma:l-partial-def'], 'S03:16': ['lemma:l-partial-def'], 'S03:17': ['lemma:l-partial-def'], 'S04:01': ['lemma:l-partial-def'], 'S04:02': ['lemma:l-partial-def'], 'S04:03': ['lemma:l-partial-def'], 'S04:04': ['lemma:l-partial-def'], 'S04:05': ['lemma:l-partial-def']},
 'bed_owners': {'S02:05': 'lemma:l-factor-def', 'S02:06': 'lemma:l-factor-def', 'S02:07': 'lemma:l-factor-def', 'S02:08': 'lemma:l-factor-def', 'S02:09': 'lemma:l-factor-def', 'S02:14': 'lemma:l-partial-def', 'S02:15': 'lemma:l-partial-def', 'S02:16': 'lemma:l-partial-def', 'S02:17': 'lemma:l-partial-def', 'S03:04': 'lemma:l-local-def', 'S03:05': 'lemma:l-local-def', 'S03:09': 'lemma:l-corr-def', 'S03:10': 'lemma:l-corr-def', 'S03:11': 'lemma:l-corr-def', 'S03:12': 'lemma:l-corr-def', 'S03:15': 'lemma:l-partial-def', 'S03:16': 'lemma:l-partial-def', 'S03:17': 'lemma:l-partial-def', 'S04:01': 'lemma:l-partial-def', 'S04:02': 'lemma:l-partial-def', 'S04:03': 'lemma:l-partial-def', 'S04:04': 'lemma:l-partial-def', 'S04:05': 'lemma:l-partial-def'},
 'beds_exact': {'S02:05': 'the first panel member carries the factor 10 over 9 at prime 3 in the uniform form',
                'S02:06': 'the second panel member carries the factor 9 over 4 at prime 2 in the uniform form',
                'S02:07': 'the first panel member carries the factor 1 at prime 2 in the record form — the ramified form, against the uniform factor 5 over 4',
                'S02:08': 'the second panel member carries the factor 38 over 37 at prime 37 in the record form — the ramified form, against the uniform factor 1407 over 1369',
                'S02:09': 'the first panel member carries the factor 36 over 25 at prime 5 in the record form — here the record and uniform forms agree (the prime is not ramified)',
                'S02:14': 'the uniform L product of the second panel member up to height 11 (last prime 11) holds the exact rational 1725219 over 148225',
                'S02:15': 'the uniform L product of the first panel member up to height 23 (last prime 23) holds the exact rational 2396868608000 over 2404368533567',
                'S02:16': 'the uniform L product of the second panel member up to height 59 (last prime 59) holds the exact rational 352146888129939261952985247744 over 26085591493411460613950839453',
                'S02:17': 'it is multiplied by the factor at 5: the uniform partial of the second panel member at 19/4 times the factor 36 over 25 is the partial 171 over 25 — the change is exactly the added factor, at the line end 84',
                'S03:04': 'at its ramified prime 2 the record form of the first panel member carries the single term 1 — against the uniform factor 5 over 4, the unit: the additive prime carries nothing, the coefficient is zero, at the line end 84',
                'S03:05': 'at its ramified prime 37 the record form of the second panel member carries the single term 38 over 37 — against the uniform factor 1407 over 1369, the multiplicative factor with its sign of record: the coefficient is minus one, at the line end 84',
                'S03:09': 'the ramification correction of the first panel member is 4 over 5 — the record factor 1 over the uniform factor 5 over 4 at its single ramified prime 2 on the line, and the record partial is the uniform partial times it, at the line end 84',
                'S03:10': 'the ramification correction of the second panel member is 1406 over 1407 — the record factor 38 over 37 over the uniform factor 1407 over 1369 at its single ramified prime 37 on the line, and the record partial is the uniform partial times it, at the line end 84',
                'S03:11': 'yes — for the first panel member the record partial 3119914956498144080343838710992732160000000 over 3913322115699829528290507876874142617812889 is the uniform partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 times the correction 4 over 5, both sides held as exact rationals, at the line end 84',
                'S03:12': 'yes — for the second panel member the record partial 288658484322736684459196579776684558374651494400 over 21623718536400902622086448680400714121493095949 is the uniform partial 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 times the correction 1406 over 1407, both sides held as exact rationals, at the line end 84',
                'S03:15': 'the record L product of the first panel member up to height 23 (last prime 23) holds the exact rational 1917494886400 over 2404368533567',
                'S03:16': 'the record L product of the second panel member up to height 23 (last prime 23) holds the exact rational 1605438144 over 129184445',
                'S03:17': 'the record L product of the second panel member up to height 41 (last prime 41) holds the exact rational 3130048911602801664 over 223924207993357885 — and past the conductor prime the record partial has separated from the uniform one by the hair of the correction, at the line end 84',
                'S04:01': 'the uniform L product of the first panel member up to height 83 (last prime 83) holds the exact rational 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889',
                'S04:02': 'the record L product of the second panel member up to height 83 (last prime 83) holds the exact rational 288658484322736684459196579776684558374651494400 over 21623718536400902622086448680400714121493095949 — and past the conductor prime the record partial has separated from the uniform one by the hair of the correction, at the line end 84',
                'S04:03': 'the record L product of the first panel member up to height 83 (last prime 83) holds the exact rational 3119914956498144080343838710992732160000000 over 3913322115699829528290507876874142617812889',
                'S04:04': 'it is multiplied by the factor at 2: the record partial of the first panel member at 1 times the factor 1 is the partial 1 — the change is exactly the added factor, at the line end 84',
                'S04:05': 'it is multiplied by the factor at 2: the uniform partial of the first panel member at 1 times the factor 5 over 4 is the partial 5 over 4 — the change is exactly the added factor, at the line end 84'},
 'derive_successes': {'S02:18': ['l-added-term', ['l-partial-def', 'l-factor-def']], 'S03:06': ['l-ramified-unit', ['l-local-def', 'l-factor-def']], 'S03:14': ['l-record-identity', ['l-corr-def', 'l-factor-def']]},
 'derived_table': {'S02:11': 'the L product of the first panel member at my line end 84 holds the exact rational 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889',
                   'S02:18': 'the added-term rule held on my line: for both panel members and every prime of the line, the partial product up to the prime is the partial product up to the previous prime times the factor the prime carries — in the uniform form and in the record form, the exact rationals agreeing prime by prime, the full record at the line end 84',
                   'S02:19': "in the L-product of a curve, each prime of my line carries a factor: in the uniform form, one minus a over p plus one over p squared, the two-term form the panel's shadow coefficient gives at every prime of the line; and in the record form the same two terms, which at the primes where the curve ramifies — the primes dividing the conductor — the record's local factor drops to a single term, one minus a over p; on my panel the ramified primes are two for the first member and thirty-seven for the second",
                   'S02:20': 'the L product of the second panel member at my line end 84 holds the exact rational 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 — the record names its limit past the line (zero of order one, the rank one vanishing); my partial holds, the limit is named, not reached',
                   'S03:06': "the ramified factors of my panel held on the line: at two for the first member the record's factor is the unit one against the uniform factor five over four, and at thirty-seven for the second member the record's factor is one plus one over thirty-seven against the uniform factor fourteen hundred and seven over thirteen hundred and sixty-nine — the two-term form replaced by the one-term, exactly, at the line end 84",
                   'S03:14': 'the record identity held on my line: the record partial to the line end is the uniform partial times the ramification corrections — four-fifths for the first panel member, fourteen hundred and six over fourteen hundred and seven for the second — and the store holds both sides as exact rationals, at the line end 84',
                   'S04:06': "this band added the L-family of the city: the factor each prime carries (the uniform two-term form, the record's one-term form at the ramified primes), the partial the line holds as an exact rational, the added-term rule, the ramification corrections, three theorems (the added term, the record identity, the ramified unit), and five honest walls — and nothing on this band is conditional on the Riemann hypothesis, at the line end 84",
                   'S04:07': "at the primes where the curve ramifies, the record's factor is the single term one minus a over p: for the first panel member the shadow coefficient is zero at two, so the record's factor is literally one — the unit, the additive prime carries nothing — and for the second panel member the shadow coefficient is minus one at thirty-seven, so the record's factor is one plus one over thirty-seven, the multiplicative factor with its sign of record; and on both members of my panel every ramified prime of record sits on the line, so the correction the line holds is the record's full correction, not a partial one",
                   'S04:08': 'the L-family of a panel member is held on my line as the product of the factors it holds: a partial product up to a height on the line, an exact rational the store holds; when a prime is added, the partial is multiplied by the factor that prime carries — the change of the partial is determined exactly by the added factor, and by nothing else; and the limit of the product over all primes past my line end is a step the store declares, not a number on my line',
                   'S04:09': "the ramification correction of a prime is the ratio of the record's factor to the uniform factor: on my panel it is four-fifths at two for the first member and fourteen hundred and six over fourteen hundred and seven at thirty-seven for the second; the record partial is the uniform partial times the product of the corrections, and at my line end both sides are exact rationals the store holds",
                   'S04:11': 'nothing the L band says is conditional on the Riemann hypothesis — the factors, the partials, and the corrections are exact on the line, and the record facts (the order of vanishing, the ranks) are named of record on their walls, at the line end 84',
                   'S04:12': "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84",
                   'S04:13': "in the L-product of a curve, each prime of my line carries a factor: in the uniform form, one minus a over p plus one over p squared, the two-term form the panel's shadow coefficient gives at every prime of the line; and in the record form the same two terms, which at the primes where the curve ramifies — the primes dividing the conductor — the record's local factor drops to a single term, one minus a over p; on my panel the ramified primes are two for the first member and thirty-seven for the second"},
 'domain_sequence': {2: 'UUULSSSSSHSULSSSSTSS', 3: 'UFLSSTULSSSSFTSSSHHHH', 4: 'SSSSSSSSSHSSS'},
 'expected_prereq_gaps': {'euler-factor': [], 'l-correction': [], 'l-partial': [], 'local-form': []},
 'final_total': 1522,
 'honest_zero_bytes': {'S02:10': 'needs_info: 4 is a composite on my line — the factor of the L product is carried at the primes of the line, the composites take their factors from the split'},
 'line_end_final': 84,
 'mastery_expected': {'euler-factor': {'correct': 8, 'prereq_gaps': [], 'state': 'stable'}, 'l-correction': {'correct': 7, 'prereq_gaps': [], 'state': 'stable'}, 'l-partial': {'correct': 14, 'prereq_gaps': [], 'state': 'stable'}, 'local-form': {'correct': 4, 'prereq_gaps': [], 'state': 'stable'}},
 'missing_parts_failure': {'S03:02': 'needs_info: i have not been taught the l-local-def — the rule for l-ramified-unit needs it before i can put it together'},
 'new_events': 58,
 'new_fact_ids': ['lemma:l-factor-def', 'lemma:l-local-def', 'lemma:l-partial-def', 'lemma:l-corr-def', 'theorem:l-added-term', 'theorem:l-record-identity', 'theorem:l-ramified-unit'],
 'new_facts': 7,
 'offscript_carry': {'state the kstbound rule': 'because two unit circles meet in at most two points the unit pair graph of a planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs at a constant times n to the three halves power'},
 'pre_s15_drilled': {'curve-shadow': 2, 'rh-relevance': 1},
 'pre_s15_states': {'add-two-digit': {'correct': 11, 'state': 'stable'},
                    'add-within-10': {'correct': 5, 'state': 'stable'},
                    'adjoin-i': {'correct': 1, 'state': 'practicing'},
                    'alg-inverse-1step': {'correct': 5, 'state': 'stable'},
                    'alg-inverse-mul': {'correct': 5, 'state': 'stable'},
                    'alg-two-step': {'correct': 4, 'state': 'stable'},
                    'averaging': {'correct': 4, 'state': 'practicing'},
                    'char-cutout': {'correct': 2, 'state': 'practicing'},
                    'chebotarev': {'correct': 2, 'state': 'practicing'},
                    'circle-pair-2': {'correct': 4, 'state': 'stable'},
                    'class-bound': {'correct': 4, 'state': 'stable'},
                    'cm-conj': {'correct': 4, 'state': 'stable'},
                    'compare-numbers': {'correct': 11, 'state': 'stable'},
                    'composite': {'correct': 7, 'state': 'stable'},
                    'conditional': {'correct': 1, 'state': 'practicing'},
                    'count-successor': {'correct': 14, 'state': 'stable'},
                    'criterion-chain': {'correct': 10, 'state': 'practicing'},
                    'critical-strip': {'correct': 12, 'state': 'practicing'},
                    'curve-form': {'correct': 7, 'state': 'stable'},
                    'curve-law': {'correct': 8, 'state': 'stable'},
                    'curve-shadow': {'correct': 10, 'state': 'stable'},
                    'cyclotomic-cubic': {'correct': 3, 'state': 'practicing'},
                    'disc-rd': {'correct': 1, 'state': 'practicing'},
                    'disproof': {'correct': 10, 'state': 'practicing'},
                    'divides': {'correct': 5, 'state': 'stable'},
                    'erdos-conj': {'correct': 10, 'state': 'stable'},
                    'factor-route': {'correct': 12, 'state': 'practicing'},
                    'family-factor': {'correct': 25, 'state': 'stable'},
                    'first-divisor': {'correct': 36, 'state': 'stable'},
                    'frattini': {'correct': 1, 'state': 'practicing'},
                    'func-eq': {'correct': 14, 'state': 'practicing'},
                    'gaussian-int': {'correct': 7, 'state': 'stable'},
                    'geom-area': {'correct': 6, 'state': 'stable'},
                    'geom-area-triangle': {'correct': 4, 'state': 'stable'},
                    'geom-perimeter': {'correct': 5, 'state': 'stable'},
                    'golod-shaf': {'correct': 6, 'state': 'practicing'},
                    'grid-lattice': {'correct': 10, 'state': 'stable'},
                    'hajir-maire': {'correct': 1, 'state': 'practicing'},
                    'hardy-line': {'correct': 5, 'state': 'practicing'},
                    'index-split': {'correct': 9, 'state': 'stable'},
                    'kin-distance': {'correct': 4, 'state': 'stable'},
                    'kin-position': {'correct': 6, 'state': 'stable'},
                    'kin-rate': {'correct': 4, 'state': 'stable'},
                    'kin-solve-time': {'correct': 4, 'state': 'stable'},
                    'kst-bound': {'correct': 4, 'state': 'stable'},
                    'li-criterion': {'correct': 9, 'state': 'stable'},
                    'lindelof': {'correct': 4, 'state': 'practicing'},
                    'line-partial': {'correct': 9, 'state': 'stable'},
                    'minkowski-embed': {'correct': 1, 'state': 'practicing'},
                    'mod4-split': {'correct': 10, 'state': 'stable'},
                    'mult-within-100': {'correct': 9, 'state': 'stable'},
                    'norm-convex': {'correct': 5, 'state': 'stable'},
                    'norm-flat': {'correct': 5, 'state': 'stable'},
                    'norm-generic': {'correct': 4, 'state': 'stable'},
                    'number-field': {'correct': 4, 'state': 'stable'},
                    'packing': {'correct': 6, 'state': 'practicing'},
                    'phrasology': {'correct': 24, 'state': 'stable'},
                    'pi-eq': {'correct': 3, 'state': 'practicing'},
                    'pnt': {'correct': 8, 'state': 'stable'},
                    'pnt-ap': {'correct': 2, 'state': 'practicing'},
                    'pnt-error': {'correct': 9, 'state': 'practicing'},
                    'point-count': {'correct': 6, 'state': 'stable'},
                    'polya-hilbert': {'correct': 3, 'state': 'practicing'},
                    'prime-count': {'correct': 15, 'state': 'stable'},
                    'prime-split': {'correct': 4, 'state': 'stable'},
                    'projection': {'correct': 4, 'state': 'practicing'},
                    'psi-eq': {'correct': 11, 'state': 'stable'},
                    'removal-rule': {'correct': 12, 'state': 'stable'},
                    'rh-relevance': {'correct': 16, 'state': 'practicing'},
                    'rh-scale': {'correct': 23, 'state': 'practicing'},
                    'riemann': {'correct': 13, 'state': 'practicing'},
                    'rv-count': {'correct': 10, 'state': 'practicing'},
                    's-of-t': {'correct': 3, 'state': 'practicing'},
                    'scan-ledger': {'correct': 12, 'state': 'stable'},
                    'shafarevich': {'correct': 2, 'state': 'practicing'},
                    'shape-circle': {'correct': 6, 'state': 'stable'},
                    'shape-rectangle': {'correct': 4, 'state': 'stable'},
                    'shape-square': {'correct': 5, 'state': 'stable'},
                    'shape-triangle': {'correct': 6, 'state': 'stable'},
                    'slack-margins': {'correct': 1, 'state': 'practicing'},
                    'sst-bound': {'correct': 4, 'state': 'stable'},
                    'st-eq': {'correct': 3, 'state': 'practicing'},
                    'stat-balance': {'correct': 6, 'state': 'stable'},
                    'stat-moment': {'correct': 4, 'state': 'stable'},
                    'stat-net-1d': {'correct': 4, 'state': 'stable'},
                    'sub-within-30': {'correct': 12, 'state': 'stable'},
                    'tower-base': {'correct': 8, 'state': 'practicing'},
                    'tower-class': {'correct': 8, 'state': 'practicing'},
                    'tower-group': {'correct': 11, 'state': 'practicing'},
                    'tower-primes': {'correct': 8, 'state': 'practicing'},
                    'unit-distance': {'correct': 5, 'state': 'stable'},
                    'window-setup': {'correct': 1, 'state': 'practicing'},
                    'zero-density': {'correct': 4, 'state': 'practicing'},
                    'zero-free': {'correct': 13, 'state': 'practicing'},
                    'zeta-cont': {'correct': 3, 'state': 'practicing'},
                    'zeta-series': {'correct': 7, 'state': 'stable'}},
 'pre_teach_gaps': {'S02:01': "not yet learned: the euler factor: the term each prime of the line carries into the L-product — the uniform two-term form at every prime, and the record's one-term form at the primes where the curve ramifies", 'S02:02': 'not yet learned: the line partial of the L-family: the product of the factors the line holds, an exact rational; adding a prime multiplies the partial by the factor it carries, and the limit past the line end is declared, not computed', 'S02:03': 'not yet learned: the l-factor-def rule', 'S02:12': 'not yet learned: the l-partial-def rule', 'S03:01': 'not yet learned: the l-local-def rule', 'S03:07': 'not yet learned: the l-corr-def rule'},
 'rederive': None,
 'scaffold_failures': {'S03:13': 'needs_info: i can see the parts you name, but the rule for l-record-identity wants its exact set — what you name is short the l-factor-def before i can put it together'},
 'script': {2: ['what factor does the first panel member carry at prime 3 in the uniform form?',
                'what does the uniform L product of the second panel member hold at height 11?',
                'state the l-factor-def rule',
                "in the L-product of a curve, each prime of my line carries a factor: in the uniform form, one minus a over p plus one over p squared, the two-term form the panel's shadow coefficient gives at every prime of the line; and in the record form the same two terms, which at the primes where the curve ramifies — the primes dividing the conductor — the record's local factor drops to a single term, one minus a over p; on my panel the ramified primes are two for the first member and thirty-seven for the second",
                'what factor does the first panel member carry at prime 3 in the uniform form?',
                'what factor does the second panel member carry at prime 2 in the uniform form?',
                'what factor does the first panel member carry at prime 2 in the record form?',
                'what factor does the second panel member carry at prime 37 in the record form?',
                'what factor does the first panel member carry at prime 5 in the record form?',
                'what factor does the second panel member carry at prime 4 in the record form?',
                "what does the first panel member's L product hold at my line end?",
                'state the l-partial-def rule',
                'the L-family of a panel member is held on my line as the product of the factors it holds: a partial product up to a height on the line, an exact rational the store holds; when a prime is added, the partial is multiplied by the factor that prime carries — the change of the partial is determined exactly by the added factor, and by nothing else; and the limit of the product over all primes past my line end is a step the store declares, not a number on my line',
                'what does the uniform L product of the second panel member hold at height 11?',
                'what does the uniform L product of the first panel member hold at height 23?',
                'what does the uniform L product of the second panel member hold at height 59?',
                'how does the uniform partial of the second panel member change when i add the prime 5?',
                'derive l-added-term from l-partial-def and l-factor-def',
                'state the l-factor-def rule',
                "what does the second panel member's L product hold at my line end?"],
            3: ['state the l-local-def rule',
                'derive l-ramified-unit from l-local-def and l-factor-def',
                "at the primes where the curve ramifies, the record's factor is the single term one minus a over p: for the first panel member the shadow coefficient is zero at two, so the record's factor is literally one — the unit, the additive prime carries nothing — and for the second panel member the shadow coefficient is minus one at thirty-seven, so the record's factor is one plus one over thirty-seven, the multiplicative factor with its sign of record; and on both members of my panel every ramified prime of record sits on the line, so the correction the line holds is the record's full correction, not a partial one",
                'in the record form what factor does the first panel member carry at its ramified prime?',
                'in the record form what factor does the second panel member carry at its ramified prime?',
                'derive l-ramified-unit from l-local-def and l-factor-def',
                'state the l-corr-def rule',
                "the ramification correction of a prime is the ratio of the record's factor to the uniform factor: on my panel it is four-fifths at two for the first member and fourteen hundred and six over fourteen hundred and seven at thirty-seven for the second; the record partial is the uniform partial times the product of the corrections, and at my line end both sides are exact rationals the store holds",
                'what is the ramification correction of the first panel member?',
                'what is the ramification correction of the second panel member?',
                'does the record partial equal the uniform partial times the ramification correction of the first panel member at my line end?',
                'does the record partial equal the uniform partial times the ramification correction of the second panel member at my line end?',
                'derive l-record-identity from l-corr-def',
                'derive l-record-identity from l-corr-def and l-factor-def',
                'what does the record L product of the first panel member hold at height 23?',
                'what does the record L product of the second panel member hold at height 23?',
                'what does the record L product of the second panel member hold at height 41?',
                'are all the ramified primes of record of the panel on my line?',
                'what does the record say the L product of the second panel member does at s equal to one?',
                'what does the record say the L product of the first panel member does at s equal to one?',
                'where in the half-plane do the L products of the panel converge?'],
            4: ['what does the uniform L product of the first panel member hold at height 83?', 'what does the record L product of the second panel member hold at height 83?', 'what does the record L product of the first panel member hold at height 83?', 'how does the record partial of the first panel member change when i add the prime 2?', 'how does the uniform partial of the first panel member change when i add the prime 2?', 'what did the L band add to the store?', 'state the l-local-def rule', 'state the l-partial-def rule', 'state the l-corr-def rule', 'does this band state the BSD?', 'does the L band say anything conditional on the Riemann hypothesis?', 'what is the queue above my line?', 'state the l-factor-def rule']},
 'seam_carry_refs': ['S02:11', 'S02:20', 'S04:12'],
 'seam_crosscheck': {'expected': 'agreement', 'queue_referenced_ids': ['conjecture:riemann', 'lemma:rh-bound-scale', 'lemma:rh-upf', 'curriculum:pnt-ap', 'curriculum:tower-primes', 'curriculum:mod4-split', 'curriculum:chebotarev', 'lemma:mod4minusone', 'lemma:primesplit', 'lemma:apbound', 'lemma:chebotarev-selection', 'lemma:rv-count', 'lemma:ledger-growth', 'theorem:spf-chain']},
 'seed': 'results/phase-6/e6.18-run1/codeX-S04.json',
 'seed_identity': 'f923ab40fbdff7d2',
 'seed_total': 1457,
 'teach_turns': {'S02:04': 'lemma:l-factor-def', 'S02:13': 'lemma:l-partial-def', 'S03:03': 'lemma:l-local-def', 'S03:08': 'lemma:l-corr-def'},
 'theorem_allowed': {'S04:12': ['queue-declared']},
 'theorem_dag': ['theorem:cm-signature', 'theorem:criterion-gap', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:delta-positive', 'theorem:first-divisor-prime', 'theorem:gamma-achieved', 'theorem:gap-scale-agreement', 'theorem:gen-lower', 'theorem:growth-compare', 'theorem:gs-infinite', 'theorem:hasse-census', 'theorem:infinity-end', 'theorem:l-added-term', 'theorem:l-ramified-unit', 'theorem:l-record-identity', 'theorem:mirror-region', 'theorem:pack-bound', 'theorem:partition-identity', 'theorem:proj-inj', 'theorem:queue-declared', 'theorem:reflect', 'theorem:removal-single', 'theorem:rh-reach', 'theorem:sieve-equality', 'theorem:spf-chain', 'theorem:splitting', 'theorem:strip', 'theorem:telescope-line', 'theorem:theorem-main', 'theorem:tower-feeds', 'theorem:two-routes-one-guarantee', 'theorem:window-rich'],
 'total_seam_facts': 117,
 'total_turns': 54,
 'unclassified_honest': {},
 'wall_articulations': {'S03:18': ['both members', 'line end 84'], 'S03:19': ['order one', 'line end 84'], 'S03:20': ['nonzero', 'line end 84'], 'S03:21': ['real part of s is above one', 'line end 84'], 'S04:10': ['summit fact of the island', 'line end 84']},
 'walls_honest': {'S03:18': 'needs_info: on both members of my panel every ramified prime of record sits on the line — two for the first, thirty-seven for the second — so the correction my line holds is the full correction of record; other curves of record have ramified primes past my line, and for them the correction the line would hold is only a part, named as such, at the line end 84',
                  'S03:19': 'needs_info: the record says the L product of the second panel member vanishes at s equal to one, of order one — the analytic side of the statement that the conjecture reads as the rank one my censuses name for the curve; my record partial at the line end holds its exact rational, far from zero — the vanishing is a limit fact past my line, named here of record, not reached, at the line end 84',
                  'S03:20': 'needs_info: the record says the L product of the first panel member at s equal to one is nonzero, order zero of vanishing — the analytic side that reads the rank zero my censuses name for the curve; my uniform partial holds its exact rational at the line end, consistent with nonzero, but nonzero at the limit is a limit fact past my line — named, not reached, at the line end 84',
                  'S03:21': 'needs_info: the L products of the panel converge only where the real part of s is above one — the same half-plane my store already holds for the zeta family; at s equal to one the product sits at its boundary, and its value and order of vanishing are limit facts past my line; the line holds the partials, the walls name the limits, at the line end 84',
                  'S04:10': 'needs_info: this band does not state the BSD: the statement equating the order of vanishing of the L product at s equal to one with the rank of the group of rational points is the summit fact of the island; the object of this band is the L-family itself — the factors, the partials, and the corrections my line holds — while the order of vanishing and the rank sit on their walls (of record, past my line), at the line end 84'}}

FROZEN: dict[str, Any] = FROZEN_DATA

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

# --- Stage-A discipline (frozen at build): the carried corpus is
# reproduced by PROBE (seam carries), never by re-assertion. No S4–S14
# lesson phrase, no S6–S14 theorem statement, appears in the S15
# script verbatim.
_StageA_ALL_LESSONS = (
    {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS,
     **S9_LESSONS, **S11_LESSONS, **S12_LESSONS, **S13_LESSONS, **S14_LESSONS}
)
_StageA_ALL_THEOREMS = (
    {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS,
     **S11_THEOREMS, **S12_THEOREMS, **S13_THEOREMS, **S14_THEOREMS}
)
_stagea_script = [t for s in FROZEN["script"].values() for t in s]
for _ph in _StageA_ALL_LESSONS:
    assert _ph not in _stagea_script, f"Stage-A: a carried lesson is re-asserted in the S15 script: {_ph[:60]!r}"
for _m in _StageA_ALL_THEOREMS.values():
    assert _m["statement"] not in _stagea_script, "Stage-A: a carried theorem statement appears in the S15 script"

#: P4 — the S15 bed budget (the mechanism's own python reference
#: re-derives every bed value the store articulates; the store's run
#: is the referee, the reference computes).
_PRIMES_ = list(_s13_py_primes(84))


def _l_budget() -> dict[str, Any]:
    """The S15 bed values re-derived from the python reference:
    the uniform/record factor tables, the spot partials, the
    corrections, the line-end partials (both forms), and the record
    identity at the line end (uniform times the corrections)."""
    out: dict[str, Any] = {}
    for tag, cv in (("A", B14_A), ("B", B14_B)):
        uni_spots = _bsd_py_lspots(*cv, form="uniform")
        rec_spots = _bsd_py_lspots(*cv, form="record")
        out[f"uni_spots_{tag}"] = {str(p): v for p, v in uni_spots.items()}
        out[f"rec_spots_{tag}"] = {str(p): v for p, v in rec_spots.items()}
        out[f"uni_84_{tag}"] = _bsd_py_lpartial_uniform(*cv)
        out[f"rec_84_{tag}"] = _bsd_py_lpartial_record(*cv)
        out[f"corr_{tag}"] = _bsd_py_lcorr(*cv)
        out[f"identity_{tag}"] = (
            _bsd_py_lpartial_uniform(*cv) * _bsd_py_lcorr(*cv) == _bsd_py_lpartial_record(*cv)
        )
    return out


_BED_BUD = _l_budget()
for _t in (2, 3, 5, 7, 37, 83):
    for _cv in (B14_A, B14_B):
        for _form in ("uniform", "record"):
            _f = _bsd_py_lfactor(_t, *_cv, _form)
            _bud = (
                _BED_BUD["uni_spots_A" if _cv == B14_A else "uni_spots_B"]
                if _form == "uniform"
                else _BED_BUD["rec_spots_A" if _cv == B14_A else "rec_spots_B"]
            )
            # the factor is exactly the ratio of consecutive spot partials
            _prev = [q for q in _PRIMES_ if q < _t]
            _before = _bud[str(_prev[-1])] if _prev else Fraction(1)
            assert _bud[str(_t)] == _before * _f, f"bed budget: the factor at {_t} ({_form}) does not chain the spot partials"
for _t in _BED_BUD:
    if _t.startswith("identity_"):
        assert _BED_BUD[_t] is True, f"bed budget: the record identity fails on the reference ({_t})"
assert _BED_BUD["uni_84_A"] == _bsd_py_Lpartial(*B14_A), "the uniform A partial drifted from the S14 beds"
assert _BED_BUD["uni_84_B"] == _bsd_py_Lpartial(*B14_B), "the uniform B partial drifted from the S14 beds"
_BSD_UNIT_A = _bsd_py_lfactor(2, *B14_A, "record")
assert _BSD_UNIT_A == Fraction(1), "panel A's ramified record factor is the unit"
assert _bsd_py_lfactor(37, *B14_B, "record") == 1 + Fraction(1, 37), "panel B's ramified record factor is one plus one over p"

_BED_BUD = {k: (v if not isinstance(v, Fraction) else str(v)) for k, v in _BED_BUD.items()}
for _k in ("uni_spots_A", "rec_spots_A", "uni_spots_B", "rec_spots_B"):
    _BED_BUD[_k] = {k: str(v) for k, v in _BED_BUD[_k].items()}


_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.19-run1"]:
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
            s: {"parts": tuple(S15_THEOREMS[s]["parts"]), "statement": S15_THEOREMS[s]["statement"]}
            for s in ("l-added-term", "l-record-identity", "l-ramified-unit")
        },
    }


def run_e6_19(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.18 S14 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S15 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.19-run1", "e6.19-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.18 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)

    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.19-run1", "e6.19-run2"):
        (out_dir / name / "e6.19-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.19.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.19-run1"
    root2 = out_dir / "e6.19-run2"
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
        **S13_LESSONS,
        **S14_LESSONS,
        **S15_LESSONS,
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inherited from S13/S14): NO
    # S15 fact carries the hypothesis marker (the L band is
    # unconditional mathematics); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S15 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s15_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s15_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S15 is unconditional)")
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
        if not ("under the condition of the Riemann hypothesis" in obj or "under the condition that" in obj):
            p0_bad.append(f"P0: {fid} lost the condition marker (drift)")
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
    checks["p0_unconditional_denying"] = {
        "pass": not p0_bad,
        "bad": p0_bad,
        "marker_absent_facts": list(s15_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S15 script + all responses + band lessons (S4–S9 + S11–S15) + all thirty-three theorem statements",
    }

    # P1 — the contract: 54 turns, every turn on the det arm and
    # contract-valid, the script identity, and the S2:01–03
    # impossible-runs BEFORE the teaches (the pre-lesson gaps come
    # first, then the teach turns).
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

    # P2 — the typed honesty: the FOUR pre-lesson gaps, the FOUR
    # teach turns (lesson facts stored), the ONE part-set failure
    # (named, needs_info, ungrounded, store-inert), the ONE
    # missing-part articulation, the THREE derive successes (stored,
    # grounded exactly on the sanctioned parts), the frozen domain
    # sequences, the line end, the ONE frozen honest-zero byte
    # (S02:10 the composite-prime probe), and ZERO seeded-fact
    # object bytes changed.
    p2_bad: list[str] = []
    impossible = [k for k, t in turns.items() if t["kind"] == "impossible"]
    if sorted(impossible) != sorted(FROZEN["pre_teach_gaps"]):
        p2_bad.append(f"impossible turns {sorted(impossible)} != frozen {sorted(FROZEN['pre_teach_gaps'])}")
    for ref, frozen_byte in sorted(FROZEN["pre_teach_gaps"].items()):
        ir = (turns.get(ref) or {}).get("response_ir") or {}
        if str(ir.get("gap", "")) != frozen_byte:
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
            p2_bad.append(f"{ref}: the frozen part-set articulation is missing (the missing part must be named)")
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
        if str(ir.get("answer", "")) != _th15(slug):
            p2_bad.append(f"{ref}: the derive answer is not the stored theorem statement")
        # the store grounds FACT ids (lemma:<slug>); the sanctioned
        # parts are SLUGS — compare at the slug level (the S14
        # check's own comparison, read at the layer the store
        # actually writes)
        got_slugs = {g.rsplit(":", 1)[-1] if g.startswith(("lemma:", "theorem:")) else g for g in map(str, t["grounded"])}
        if got_slugs != set(prem_ids):
            p2_bad.append(f"{ref}: the grounded part set {sorted(got_slugs)} != sanctioned {sorted(prem_ids)}")
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
    # the seed drift census: ZERO seeded facts changed (the touch
    # set is exactly the new facts + the mastery events).
    seed_path = _resolve_seed()
    seed_store = load_store(seed_path)
    if not seed_path.exists():
        p2_bad.append("the seed store is missing")
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
    # full S4–S15 lemma canon, the full thirty-three-theorem DAG,
    # the 117 seam-family facts, the conj still open).
    p3_bad: list[str] = []
    for ref, expected in sorted(FROZEN["derived_table"].items()):
        t = turns.get(ref)
        if t is None:
            p3_bad.append(f"missing derived turn {ref}")
            continue
        ans = _ir_answer(t)
        if ans != expected:
            p3_bad.append(f"{ref}: derived answer {str(ans)[:60]!r} != frozen {str(expected)[:60]!r}")
        ir = t["response_ir"] or {}
        if ir.get("uncertainty_state") != "derived":
            p3_bad.append(f"{ref}: not a grounded derivation ({ir.get('uncertainty_state')})")
    for a in final.query():
        if a.id is None or not a.id.startswith("lemma:"):
            continue
        if isinstance(a.object, str) is False:
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
        p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S15 must not flip)")
    checks["p3_seam_and_theorems"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_lessons": len(seam_facts),
        "seam_theorems": len(th_facts),
        "total_seam_facts": len(seam_facts) + len(th_facts),
    }

    # P4 — the 23 beds exact + grounded (the ON-LINE census answers),
    # the 5 walls honest with their frozen bytes and articulations
    # (each wall names the value AND the line end), and the W-S15
    # wall bytes byte-identical to the Brainstem class attributes
    # (the D-e6z(b) pattern, frozen). No NEW off-line decimal enters
    # the floor at S15 (offline_watch is empty; the carried
    # 13.3586546916 stays exactly where W-S14-5 left it).
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
        W_S15_1 == Brainstem.W_S15_1
        and W_S15_2 == Brainstem.W_S15_2
        and W_S15_3 == Brainstem.W_S15_3
        and W_S15_4 == Brainstem.W_S15_4
        and W_S15_5 == Brainstem.W_S15_5
    ):
        p4_bad.append("a W-S15 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S15-1..W-S15-5 (cross-checked, never surfaced)",
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant (BSD-flavored, strengthened at the L band): NO fact
    # id the conj uses appears in a grounded list; NO `theorem:bsd`
    # assertion exists (if non-empty: STOP, human review, full
    # evidence, never a threshold loosening); the conj fact
    # byte-identical to the seed (open, declared-source); the bed
    # owners (the frozen citation sets); the theorem allow-set; and
    # the SEMANTIC seam (the AGREEMENT, measured by the mechanism's
    # own python reference at every prime of the line): (a) the
    # added-term rule — each spot partial is the previous times the
    # factor, both forms, both panels; (b) the record identity — at
    # the line end, the record partial is the uniform times the
    # corrections, exact; (c) the ramified unit — panel A's record
    # factor at 2 is the literal unit 1, panel B's at 37 is
    # 1 + 1/37; (d) the queue grounding — every fact id the
    # declared queue lots name exists.
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S15 has no conj-teach turn)")
    bsd_th = [a.id for a in final.query() if a.id and a.id.startswith("theorem:bsd")]
    if bsd_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {bsd_th} — the sanctioned corpus now produces theorem:bsd")
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
    # (a)+(b)+(c) the L-family destinations (mechanism vs reference):
    l_bad: list[str] = []
    for tag, cv in (("A", B14_A), ("B", B14_B)):
        for form in ("uniform", "record"):
            spots = _BED_BUD[f"{'uni' if form == 'uniform' else 'rec'}_spots_{tag}"]
            for i, p in enumerate(_PRIMES_):
                fac = _bsd_py_lfactor(p, *cv, form)
                before_str = spots[str(_PRIMES_[i - 1])] if i else "1/1"
                before = Fraction(before_str)
                after = Fraction(spots[str(p)])
                if after != before * fac:
                    l_bad.append(f"{tag} {form} @ {p}: the added-term rule drifted on the reference")
        if not _BED_BUD[f"identity_{tag}"]:
            l_bad.append(f"{tag}: the record identity (uniform x corrections) fails on the reference")
    if _bsd_py_lfactor(2, *B14_A, "record") != Fraction(1):
        l_bad.append("A@2: the ramified record factor is not the unit")
    if _bsd_py_lfactor(37, *B14_B, "record") != 1 + Fraction(1, 37):
        l_bad.append("B@37: the ramified record factor is not one plus one over p")
    for b in l_bad:
        p5_bad.append(f"L-identity destination: {b} — TIER-2 breakthrough candidate (PENDING owner)")
    # (d) the queue grounding (carried, unchanged from S14/S13):
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
        "discovery_candidate_bsd_theorem_facts": bsd_th,
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "l_identity_bad": l_bad[:10],
            "l_identity_agreement": not l_bad,
            "queue_referenced_ids": list(FROZEN["seam_crosscheck"]["queue_referenced_ids"]),
            "queue_missing": queue_missing,
        },
    }

    # P6 — the SEAM carry (the THREE rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime:
    # the two S14 L-partial carries and the queue) + the one
    # OFF-SCRIPT carry probe (kstbound byte-identical — the savant
    # track's standing soil check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.19-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E619)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S15-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 100 seed concepts: the carried
    # correct-derivation counts equal their S14-final base + the
    # frozen drill at the NEW S15 coordinates; NO state REGRESSION —
    # a carried concept may only move stable->stable or
    # practicing->stable (the sanctioned improvement, the S14
    # D-e6i(b) rule); the four NEW concepts at their frozen band-end
    # values with their frozen prereq-gap sets — local-form landing
    # stable via the s15-form grounding (D-e6j(b)) clears the
    # l-correction prereq).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E619])
    _S15_NEW = [c.id for c in CONCEPT_S15]
    for cid in list(FROZEN["pre_s15_states"]) + _S15_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s15_drilled"] if isinstance(FROZEN["pre_s15_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s15_states"].items():
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
        "carried_refs": len(FROZEN["pre_s15_states"]),
        "drilled": drilled,
        "improved_to_stable": sorted(improved),
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
    if runs["e6.19-run1"] != runs["e6.19-run2"]:
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
            "determinism_twin": runs["e6.19-run1"] == runs["e6.19-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.19-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s15_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_19Experiment:
    """E6.19 — S15 of the PRIZE-ISLANDS-TRACK (the BSD island,
    band 2 of 3): the L-function of the city (the local factors,
    the exact-rational partials, the ramification corrections)."""

    name = "e6.19"
    hypothesis = (
        "S15 of the PRIZE-ISLANDS-TRACK (the BSD island, band 2 of 3) walks the L-FUNCTION OF THE CITY "
        "over the carried S14 seed (1457): the factor each prime of the line carries in the panel's "
        "L-product — the uniform two-term form 1 - a_p/p + 1/p^2 at every prime, and the record's one-term "
        "form at the ramified conductor primes, where panel A's factor at 2 is the literal unit 1 (the "
        "additive prime with the zero coefficient carries nothing) and panel B's factor at 37 is one "
        "plus one over p (the multiplicative sign of the minus-one coefficient); the L-partial held as "
        "the exact rational product the line holds, with the added-term rule (the S13 removal rule "
        "inverted) verified prime by prime in both forms; and the ramification correction, under which "
        "the record partial to the line end is the uniform partial times 4/5 (panel A) or 1406/1407 "
        "(panel B) — both sides exact rationals the store holds, the separation standing at the "
        "conductor: panel B's record and uniform partials agree through height 23 and separate exactly "
        "at 37 by the hair 1406/1407, while panel A's record partial never moves at 2. The band is "
        "UNCONDITIONAL: the order of vanishing at s = 1 (order zero for A, order one for B — the "
        "analytic side of the BSD equation), the convergence region, and the ranks are named OF RECORD "
        "on the five W-S15 walls, each naming the value and the line end 84. It stores SEVEN new "
        "deterministic facts: four lessons (l-factor-def, l-local-def, l-partial-def, l-corr-def) and "
        "three compositions (l-added-term, l-record-identity, l-ramified-unit) with the strict part "
        "sets, the seam census closing 110+7 -> 117. The line stays 0..84 (zero new successor facts); "
        "the conj stays open, byte-identical to the seed; NO theorem:bsd exists (the BSD statement — "
        "order of vanishing equals rank — is the island's SUMMIT fact, band 3's object: the "
        "discovery-candidate invariant, BSD-flavored); the THREE seam rows (the two S14 L-partial "
        "carries, the queue) are byte-identical to the seed store; kstbound byte-identical; two runs "
        "byte-identical. The store holds, verified and honestly bounded: it can re-derive every "
        "census from its own premises — or refuse the record claims it has not been taught."
    )
    metric = "S15 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_19()
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
                Path("results/phase-6/e6.19-run1/session-S02.json"),
                Path("results/phase-6/e6.19-run1/session-S03.json"),
                Path("results/phase-6/e6.19-run1/session-S04.json"),
                Path("results/phase-6/e6.19-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
