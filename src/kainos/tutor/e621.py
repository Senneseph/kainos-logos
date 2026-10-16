# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.21 — S17 of the PRIZE-ISLANDS-TRACK (the Beal island — its
single band; built THE BANDGEN WAY): THE VALUATION LINE.

Over the carried S16 seed (1581, e21eaaf32b475930 — the BSD island's
closeout store). Four new concepts (valuation, lte-form,
beal-summit, beal-census — college-1, domain beal, prereqs point DOWN
into the S11 soil: first-divisor, divides, scan-ledger), four VERBATIM
lessons (valuation-def, lte-def, beal-def, census-def), two
sanctioned compositions (lte-ledger from lte-def + valuation-def;
beal-line-satisfaction from beal-def + census-def).

The story the band holds on the line: the valuation — the p-adic
depth of a number, read off the p-rung of the first-divisor
factorization chain (the S11 soil); the lift-the-exponent identity,
the classical odd-p form (v_p(x^n - y^n) = v_p(x-y) + v_p(n) for
p | (x-y), p ∤ x·y) — the ledger of 249,280 instances in the line's
box verifies every one of them, zero deviations; the STATEMENT —
verbatim per the ams beal prize record (if A^x + B^y = C^z with
positive integers and x, y, z > 2, then A, B, C share a common prime
factor) — stored as the island's summit fact (declared record); and
the VERIFICATION CENSUS — in the box (bases at or below the line end
84, exponents three through ten of record) exactly 83 triples solve
the equation and every one carries its common prime factor: zero
primitive triples on the line.

UNCONDITIONAL-FLAVORED band: the primitive territory, the
fermat-catalan boundary, and the fermat closed anchor sit on walls
W-S17-1/2/3, each naming its record place AND the line end 84; the
census rows and the ledger count are beds (record facts the store
holds). NO NEW decimals: the 3-powerful counterexample scale is named
at its order (seventeen digits) without its digit string. NO
`theorem:beal` fact id exists (the statement is stored as
`lemma:beal-def` + the composition `theorem:beal-line-satisfaction`
— the bare conj id is the island's wall, not its store fact; the
discovery-candidate invariant extends: P5 stops on theorem:beal
exactly as on theorem:bsd).

FROZEN FROM CONTROL #1 (bandgen-era, the bandgen dryrun over
bands/spec-e6.21.json: c0–c9 CLEAN — ready to freeze; the
pre-reg corrections of the D-e6l family are recorded at closeout:
the missing-parts probe names BOTH untaught parts — 'the beal-def or
the census-def ... needs them'; the mastery census lands at
valuation 6, lte-form 7, beal-summit 4, beal-census 10 (the re-
probes drill the concepts); 54 events for the 51 turns, drift +3).
The 51-turn script (S2:17 + S3:17 + S4:17), the 15 beds, the 3 walls,
all predictions out of the mechanism's own dry-run; the control
report is the referee, never the hand. Store: 1581 -> 1641
(6 facts + 54 events, drift +3). No NEW successor facts (the line
stays 0..84); the riemann conj stays open, byte-identical to the
seed.

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
    CONCEPT_S17,
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
    S17_BEDS,
    S17_LESSONS,
    S17_THEOREMS,
    Brainstem,
    _beal_py_census,
    _beal_py_lte_box,
)
from kainos.tutor.e620 import (
    CONCEPTS_E620,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E621", "FROZEN", "E6_21Experiment", "run_e6_21"]

CHECKS = 9

#: S17 teaches: the valuation line (the Beal island — its single band).
#: The four new concepts join the carried S16 registry; prereqs point
#: DOWN into the S11 soil (first-divisor, divides, scan-ledger) — the
#: islands connect through the soil, the summit stands on the census.
CONCEPTS_E621: tuple = CONCEPTS_E620 + CONCEPT_S17

E620_SEED = Path("results/phase-6/e6.20-run1/codeX-S04.json")

def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E620_SEED.exists():
        return E620_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E620_SEED
    return alt if alt.exists() else E620_SEED

_ST17 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S17_LESSONS.items()}
_TH17 = {s: m["statement"] for s, m in S17_THEOREMS.items()}


def _th17(slug: str) -> str:
    return _TH17[slug]

#: P4 — the W-S17 walls (the off-line material names the record place
#: AND the line end; the walls are the band's declared off-line layer
#: — P4 cross-checks the bytes against the Brainstem class
#: attributes, never surfaced beyond the wall).
W_S17_1 = Brainstem.W_S17_1
W_S17_2 = Brainstem.W_S17_2
W_S17_3 = Brainstem.W_S17_3


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
    rt = InfantRuntime(root, concepts=CONCEPTS_E621)
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
FROZEN_DATA = {'bed_grounded': {'S02:04': ['lemma:valuation-def'], 'S02:05': ['lemma:valuation-def'], 'S02:06': ['lemma:valuation-def'], 'S02:10': ['lemma:lte-def'], 'S02:11': ['lemma:lte-def'], 'S02:12': ['lemma:lte-def'], 'S02:16': ['lemma:valuation-def'], 'S02:17': ['lemma:lte-def'], 'S03:06': ['lemma:census-def'], 'S03:07': ['lemma:census-def'], 'S03:08': ['lemma:census-def'], 'S03:14': ['lemma:census-def'], 'S03:15': ['lemma:census-def'], 'S03:16': ['theorem:beal-line-satisfaction'], 'S03:17': ['lemma:beal-def']},
 'bed_owners': {'S02:04': 'lemma:valuation-def', 'S02:05': 'lemma:valuation-def', 'S02:06': 'lemma:valuation-def', 'S02:10': 'lemma:lte-def', 'S02:11': 'lemma:lte-def', 'S02:12': 'lemma:lte-def', 'S02:16': 'lemma:valuation-def', 'S02:17': 'lemma:lte-def', 'S03:06': 'lemma:census-def', 'S03:07': 'lemma:census-def', 'S03:08': 'lemma:census-def', 'S03:14': 'lemma:census-def', 'S03:15': 'lemma:census-def', 'S03:16': 'theorem:beal-line-satisfaction', 'S03:17': 'lemma:beal-def'},
 'beds_exact': {'S02:04': 'the p-adic depth of sixty-four at the prime two of record is six — read off the two-rung of the first-divisor factorization chain of sixty-four, at the line end 84',
                'S02:05': 'the p-adic depth of seventy-two at the prime three of record is two — read off the three-rung of the first-divisor factorization chain of seventy-two, at the line end 84',
                'S02:06': 'the p-adic depth of eighty-four at the prime two of record is two — read off the two-rung of the first-divisor factorization chain of eighty-four, at the line end 84',
                'S02:10': 'it holds: four cubed minus one cubed — sixty-three — holds two of the three-rung, while the difference 3 holds one of the three-rung and the exponent three holds one of it — one plus one is two — the depth of the difference plus the depth of the exponent, at the line end 84',
                'S02:11': 'it holds: ten cubed minus one cubed — nine hundred and ninety-nine — holds three of the three-rung, while the difference 9 holds two of the three-rung and the exponent three holds one of it — two plus one is three — the depth of the difference plus the depth of the exponent, at the line end 84',
                'S02:12': 'two hundred forty-nine thousand two hundred eighty of record: the odd primes at or below my line end, the difference a multiple of the prime with neither term divisible by it, the exponents three through the line end — every one holds: zero deviations, at the line end 84',
                'S02:16': 'the p-adic depth of thirty-six at the prime two of record is two — read off the two-rung of the first-divisor factorization chain of thirty-six, at the line end 84',
                'S02:17': 'two hundred forty-nine thousand two hundred eighty of record: the odd primes at or below my line end, the difference a multiple of the prime with neither term divisible by it, the exponents three through the line end — every one holds: zero deviations, at the line end 84',
                'S03:06': 'eighty-three triples in the box — a, b, c at or below my line end, the exponents between three and ten of record — and every one of the eighty-three carries its common prime factor: no primitive triple in the box, at the line end 84',
                'S03:07': 'zero — no primitive triple lives on my line; the line ends where the primitive triples would live, and that territory is a wall, at the line end 84',
                'S03:08': 'the two-power twins (two to the n plus two to the n equals two to the n plus one), the three-family (three cubed plus six cubed equals three to the fifth), the seven-family (seven cubed plus seven to the fourth equals fourteen cubed), the fifteen-family (fifteen to the fourth plus fifteen to the fifth equals thirty to the fourth), and the seventeen, nineteen, twenty-six, twenty-eight, thirty-one, thirty-three families with their common factors — 61 of the eighty-three carry the two, the other 22 their odd primes, at the line end 84',
                'S03:14': 'eighty-three triples in the box — a, b, c at or below my line end, the exponents between three and ten of record — and every one of the eighty-three carries its common prime factor: no primitive triple in the box, at the line end 84',
                'S03:15': 'the beal band holds the statement of the island, stored as a declared record fact (the ams beal prize), its satisfaction filed on my line — the verification census of the box: eighty-three triples, every one carrying its common prime factor, zero primitive — with the valuation read off the first-divisor chain and the lift-the-exponent ledger holding in all its instances, the primitive territory, the fermat catalan boundary, and the fermat anchor named on their walls, at the line end 84',
                'S03:16': 'the summit of the island filed on my line: the statement holds of record across the whole census box — the eighty-three triples of the box each carry their common prime factor, no primitive triple lives in the box, and the primitive territory is a wall, at the line end 84',
                'S03:17': 'nothing the beal band says is conditional on an unproved hypothesis — the valuation, the lift-the-exponent ledger, and the verification census are record on the line, and the primitive territory, the fermat catalan boundary, and the fermat anchor stand named of record on their walls, at the line end 84'},
 'derive_successes': {'S02:15': ['lte-ledger', ['lte-def', 'valuation-def']], 'S03:10': ['beal-line-satisfaction', ['beal-def', 'census-def']]},
 'derived_table': {'S02:15': "the ledger filed on the line: the lift-the-exponent identity, the classical odd-p form, verified in every instance of the ledger's box — the odd primes at or below my line end, the difference a multiple of the prime with neither term divisible by it, the exponents three through the line end — two hundred forty-nine thousand two hundred eighty instances, zero deviations, at the line end 84",
                   'S03:10': 'the summit of the island filed on my line: the statement holds of record across the whole census box — the eighty-three triples of the box each carry their common prime factor, no primitive triple lives in the box, and the primitive territory is a wall, at the line end 84',
                   'S04:01': 'the summit of the island is the statement itself — held in my store as a declared record fact (the clay millennial booklet, the wiles chapter): the order of vanishing of the L product at s equal to one equals the algebraic rank — and on my panel the two sides are settled of record and they agree: order zero equals rank zero for the first member, and order one equals rank one for the second, at the line end 84',
                   'S04:02': "of record, the L product of the first panel member is nonzero at s equal to one — order zero of vanishing — and on my line the exact partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 stands nonzero for the line's side, at the line end 84",
                   'S04:03': 'the torsion ledger of the first panel member holds its three integral two-torsion points on my line — (x zero y zero), (x one y zero), (x minus one y zero) — the full two-torsion of record (z/2 squared), and nothing else on the line, at the line end 84',
                   'S04:04': "needs_info: the exact L value at s equal to one is of record, not on my line: the first panel member's L value is nonzero of order zero of vanishing, and the second panel member's vanishes of order one with its leading coefficient nonzero of record (named here, not computed); my line holds the exact rational partials standing for the line's side — the vanishing is a limit fact past my line, at the line end 84",
                   'S04:05': 'the ramification correction of the first panel member is 4 over 5 — the record factor 1 over the uniform factor 5 over 4 at its single ramified prime 2 on the line, and the record partial is the uniform partial times it, at the line end 84',
                   'S04:06': "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84",
                   'S04:07': 'the p-adic depth of sixty-four at the prime two of record is six — read off the two-rung of the first-divisor factorization chain of sixty-four, at the line end 84',
                   'S04:08': 'the p-adic depth of seventy-two at the prime three of record is two — read off the three-rung of the first-divisor factorization chain of seventy-two, at the line end 84',
                   'S04:09': 'it holds: four cubed minus one cubed — sixty-three — holds two of the three-rung, while the difference 3 holds one of the three-rung and the exponent three holds one of it — one plus one is two — the depth of the difference plus the depth of the exponent, at the line end 84',
                   'S04:10': 'two hundred forty-nine thousand two hundred eighty of record: the odd primes at or below my line end, the difference a multiple of the prime with neither term divisible by it, the exponents three through the line end — every one holds: zero deviations, at the line end 84',
                   'S04:11': 'the statement of record, as the ams beal prize holds it: if a to the x power plus b to the y power equals c to the z power, with a, b, c, x, y and z positive and x, y and z each above two, then a, b and c have a common prime factor — no pairwise coprime solution exists once every exponent is above two, at the line end 84',
                   'S04:12': 'eighty-three triples in the box — a, b, c at or below my line end, the exponents between three and ten of record — and every one of the eighty-three carries its common prime factor: no primitive triple in the box, at the line end 84',
                   'S04:13': 'zero — no primitive triple lives on my line; the line ends where the primitive triples would live, and that territory is a wall, at the line end 84',
                   'S04:14': 'the two-power twins (two to the n plus two to the n equals two to the n plus one), the three-family (three cubed plus six cubed equals three to the fifth), the seven-family (seven cubed plus seven to the fourth equals fourteen cubed), the fifteen-family (fifteen to the fourth plus fifteen to the fifth equals thirty to the fourth), and the seventeen, nineteen, twenty-six, twenty-eight, thirty-one, thirty-three families with their common factors — 61 of the eighty-three carry the two, the other 22 their odd primes, at the line end 84',
                   'S04:15': "the verification census on my line: in the box where a, b, c lie at or below my line end and the exponents x, y, z stand between three and ten of record, exactly eighty-three triples solve the island's equation, and every one of the eighty-three carries its common prime factor — the two-power twin family, the three-family, the seven-family, the fifteen-family, and the seventeen, nineteen, twenty-six, twenty-eight, thirty-one, thirty-three families — while zero primitive triples live on my line; the line ends where the primitive triples would live, and that territory is a wall, at the line end 84",
                   'S04:16': 'the beal band holds the statement of the island, stored as a declared record fact (the ams beal prize), its satisfaction filed on my line — the verification census of the box: eighty-three triples, every one carrying its common prime factor, zero primitive — with the valuation read off the first-divisor chain and the lift-the-exponent ledger holding in all its instances, the primitive territory, the fermat catalan boundary, and the fermat anchor named on their walls, at the line end 84',
                   'S04:17': 'needs_info: the wall is the primitive territory itself: the conjecture asserts that no pairwise coprime solution survives once all three exponents are above 2; my census box (the line end at eighty-four, the exponent depth ten of record) holds eighty-three triples and none of them is primitive, and any counterexample would carry three terms each 3-powerful — the smallest known coprime sum of 3-powerfuls sits at the scale of seventeen digits, far past my line — that territory is declared, never reached, at the line end 84'},
 'domain_sequence': {2: 'UULSSSUULSSSFFTSS', 3: 'UULULSSSFTHHHSSSS', 4: 'SSSHSSSSSSSSSSSSH'},
 'expected_prereq_gaps': {'beal-census': [], 'beal-summit': [], 'lte-form': [], 'valuation': []},
 'final_total': 1641,
 'honest_zero_bytes': {},
 'line_end_final': 84,
 'mastery_expected': {'beal-census': {'correct': 10, 'prereq_gaps': [], 'state': 'stable'}, 'beal-summit': {'correct': 4, 'prereq_gaps': [], 'state': 'stable'}, 'lte-form': {'correct': 7, 'prereq_gaps': [], 'state': 'stable'}, 'valuation': {'correct': 6, 'prereq_gaps': [], 'state': 'stable'}},
 'missing_parts_failure': {'S02:13': 'needs_info: i have not been taught the beal-def or the census-def — the rule for beal-line-satisfaction needs them before i can put it together'},
 'new_events': 54,
 'new_fact_ids': ['lemma:valuation-def', 'lemma:lte-def', 'lemma:beal-def', 'lemma:census-def', 'theorem:lte-ledger', 'theorem:beal-line-satisfaction'],
 'new_facts': 6,
 'offscript_carry': {'state the bsd-panel-satisfaction rule': "the summit of the island filed on my panel: the statement holds of record on both members — the order zero of vanishing equals the rank zero of the first member, and the order one of vanishing equals the rank one of the second — the two sides settled by independent record machinery (the ranks by the descent and the point ledger, the orders by the L-function's record), and my line's exact partials stand consistent with both, at the line end 84"},
 'pre_s17_drilled': {'algebraic-rank': 1, 'analytic-order': 1, 'bsd-summit': 1, 'l-correction': 1},
 'pre_s17_states': {'add-two-digit': {'correct': 11, 'state': 'stable'},
                    'add-within-10': {'correct': 5, 'state': 'stable'},
                    'adjoin-i': {'correct': 1, 'state': 'practicing'},
                    'alg-inverse-1step': {'correct': 5, 'state': 'stable'},
                    'alg-inverse-mul': {'correct': 5, 'state': 'stable'},
                    'alg-two-step': {'correct': 4, 'state': 'stable'},
                    'algebraic-rank': {'correct': 11, 'state': 'stable'},
                    'analytic-order': {'correct': 4, 'state': 'stable'},
                    'averaging': {'correct': 4, 'state': 'practicing'},
                    'bsd-summit': {'correct': 10, 'state': 'stable'},
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
                    'curve-shadow': {'correct': 12, 'state': 'stable'},
                    'cyclotomic-cubic': {'correct': 3, 'state': 'practicing'},
                    'disc-rd': {'correct': 1, 'state': 'practicing'},
                    'disproof': {'correct': 10, 'state': 'practicing'},
                    'divides': {'correct': 5, 'state': 'stable'},
                    'erdos-conj': {'correct': 10, 'state': 'stable'},
                    'euler-factor': {'correct': 9, 'state': 'stable'},
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
                    'l-correction': {'correct': 8, 'state': 'stable'},
                    'l-partial': {'correct': 14, 'state': 'stable'},
                    'li-criterion': {'correct': 9, 'state': 'stable'},
                    'lindelof': {'correct': 4, 'state': 'practicing'},
                    'line-partial': {'correct': 9, 'state': 'stable'},
                    'line-reaching': {'correct': 5, 'state': 'stable'},
                    'local-form': {'correct': 4, 'state': 'stable'},
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
                    'rh-relevance': {'correct': 17, 'state': 'practicing'},
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
 'pre_teach_gaps': {'S02:01': 'not yet learned: the valuation: for a prime and a number on my line, the p-adic depth — the p-rung of the first-divisor factorization chain, counting how many times the prime divides before the stop; every recorded number carries its depths as facts',
                    'S02:02': 'not yet learned: the valuation-def rule',
                    'S02:07': "not yet learned: the lift-the-exponent form: for an odd prime p dividing the difference x minus y and dividing neither term, the p-adic depth of x to the n power minus y to the n power is the p-adic depth of the difference plus the p-adic depth of the exponent — verified in every instance of the line's ledger box",
                    'S02:08': 'not yet learned: the lte-def rule',
                    'S03:01': 'not yet learned: the summit of the island: the statement itself, a declared record fact (the ams beal prize) — with all three exponents above two, a to the x power plus b to the y power equal to c to the z power forces a common prime factor of a, b and c; on my line the verification census carries it and the primitive territory is a wall',
                    'S03:02': 'not yet learned: the beal-def rule',
                    'S03:04': "not yet learned: the verification census: in the box where a, b, c lie at or below the line end and the exponents stand between three and ten of record, exactly 83 triples solve the island's equation and every one carries its common prime factor — zero primitive triples on the line; the line ends where the primitive triples would live"},
 'rederive': None,
 'scaffold_failures': {'S02:14': 'needs_info: i can see the parts you name, but the rule for lte-ledger wants its exact set — what you name is short the valuation-def before i can put it together', 'S03:09': 'needs_info: i can see the parts you name, but the rule for beal-line-satisfaction wants its exact set — what you name is short the census-def before i can put it together'},
 'script': {2: ['what is the p-adic depth of sixty-four at the prime two of record?',
                'state the valuation-def rule',
                'the valuation, the p-adic depth, read off the first-divisor factorization chain: for a prime p and a number on my line, it is the number of times the p-rung of the chain divides the number before the stop — the highest power of p that divides it — and every recorded number carries each of its depths as a fact, at the line end 84',
                'what is the p-adic depth of sixty-four at the prime two of record?',
                'what is the p-adic depth of seventy-two at the prime three of record?',
                'what is the p-adic depth of eighty-four at the prime two of record?',
                'what does the lift-the-exponent identity hold for four cubed minus one cubed at the prime three of record?',
                'state the lte-def rule',
                "the lift-the-exponent identity, the classical odd-p form, as the rule i was given: when an odd prime p divides the difference x minus y and divides neither x nor y, the p-adic depth of x to the n power minus y to the n power is the p-adic depth of the difference x minus y plus the p-adic depth of the exponent n — my ledger in the line's box (the odd primes at or below the line end, the difference a multiple of the prime with neither term divisible by it, the exponents three through the line end) verifies every instance of it, at the line end 84",
                'what does the lift-the-exponent identity hold for four cubed minus one cubed at the prime three of record?',
                'what does the lift-the-exponent identity hold for ten cubed minus one cubed at the prime three of record?',
                "how many instances does the lift-the-exponent ledger cover in the line's box of record?",
                'derive beal-line-satisfaction from beal-def and census-def',
                'derive lte-ledger from lte-def',
                'derive lte-ledger from lte-def and valuation-def',
                'what is the p-adic depth of thirty-six at the prime two of record?',
                "how many instances does the lift-the-exponent ledger cover in the line's box of record?"],
            3: ['what is the statement of the beal island of record?',
                'state the beal-def rule',
                'the statement of the island, of record, as the ams beal prize holds it: if a to the x power plus b to the y power equals c to the z power, and a, b, c, x, y and z are positive integers with x, y and z each above two, then a, b and c have a common prime factor — that is, the equation has no solution in pairwise coprime a, b and c once every exponent is above two, at the line end 84',
                "how many triples does the verification census of the beal island hold in the line's box?",
                "the verification census on my line: in the box where a, b, c lie at or below my line end and the exponents x, y, z stand between three and ten of record, exactly eighty-three triples solve the island's equation, and every one of the eighty-three carries its common prime factor — the two-power twin family, the three-family, the seven-family, the fifteen-family, and the seventeen, nineteen, twenty-six, twenty-eight, thirty-one, thirty-three families — while zero primitive triples live on my line; the line ends where the primitive triples would live, and that territory is a wall, at the line end 84",
                "how many triples does the verification census of the beal island hold in the line's box?",
                'how many primitive triples live on my line?',
                'which families does the verification census of the beal island hold on my line?',
                'derive beal-line-satisfaction from beal-def',
                'derive beal-line-satisfaction from beal-def and census-def',
                'what lives in the primitive territory of the beal island?',
                'what lives at the fermat catalan boundary of the beal island?',
                'what is the closed anchor of the beal island?',
                "how many triples does the verification census of the beal island hold in the line's box?",
                'what state does the beal band hold at the line end?',
                'state the beal-line-satisfaction rule',
                'does the beal band say anything conditional on an unproved hypothesis?'],
            4: ['what is the summit fact of the island?',
                'what order of vanishing does the L product of the first panel member have at s equal to one of record?',
                'what does the torsion ledger of the first panel member hold on my line?',
                'what is the exact record L value of the second panel member at s equal to one?',
                'what is the ramification correction of the first panel member?',
                'what is the queue above my line?',
                'what is the p-adic depth of sixty-four at the prime two of record?',
                'what is the p-adic depth of seventy-two at the prime three of record?',
                'what does the lift-the-exponent identity hold for four cubed minus one cubed at the prime three of record?',
                "how many instances does the lift-the-exponent ledger cover in the line's box of record?",
                'what is the statement of the beal island of record?',
                "how many triples does the verification census of the beal island hold in the line's box?",
                'how many primitive triples live on my line?',
                'which families does the verification census of the beal island hold on my line?',
                'state the census-def rule',
                'what state does the beal band hold at the line end?',
                'what lives in the primitive territory of the beal island?']},
 'seam_carry_refs': ['S04:01', 'S04:02', 'S04:03', 'S04:04', 'S04:05', 'S04:06'],
 'seam_crosscheck': {'expected': 'agreement'},
 'seed': 'results/phase-6/e6.20-run1/codeX-S04.json',
 'seed_identity': 'e21eaaf32b475930',
 'seed_total': 1581,
 'teach_turns': {'S02:03': 'lemma:valuation-def', 'S02:09': 'lemma:lte-def', 'S03:03': 'lemma:beal-def', 'S03:05': 'lemma:census-def'},
 'theorem_allowed': {'S03:16': ['beal-line-satisfaction'], 'S04:06': ['queue-declared']},
 'theorem_dag': ['theorem:beal-line-satisfaction', 'theorem:bsd-panel-satisfaction', 'theorem:cm-signature', 'theorem:criterion-gap', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:delta-positive', 'theorem:first-divisor-prime', 'theorem:gamma-achieved', 'theorem:gap-scale-agreement', 'theorem:gen-lower', 'theorem:growth-compare', 'theorem:gs-infinite', 'theorem:hasse-census', 'theorem:infinity-end', 'theorem:l-added-term', 'theorem:l-ramified-unit', 'theorem:l-record-identity', 'theorem:lte-ledger', 'theorem:mirror-region', 'theorem:pack-bound', 'theorem:partition-identity', 'theorem:proj-inj', 'theorem:queue-declared', 'theorem:reflect', 'theorem:removal-single', 'theorem:rh-reach', 'theorem:sieve-equality', 'theorem:spf-chain', 'theorem:splitting', 'theorem:strip', 'theorem:telescope-line', 'theorem:theorem-main', 'theorem:tower-feeds', 'theorem:two-routes-one-guarantee', 'theorem:window-rich'],
 'total_seam_facts': 128,
 'total_turns': 51,
 'unclassified_honest': {},
 'wall_articulations': {'S03:11': ['primitive', 'line end 84'], 'S03:12': ['fermat-catalan', 'line end 84'], 'S03:13': ['wiles', 'line end 84']},
 'walls_honest': {'S03:11': 'needs_info: the wall is the primitive territory itself: the conjecture asserts that no pairwise coprime solution survives once all three exponents are above 2; my census box (the line end at eighty-four, the exponent depth ten of record) holds eighty-three triples and none of them is primitive, and any counterexample would carry three terms each 3-powerful — the smallest known coprime sum of 3-powerfuls sits at the scale of seventeen digits, far past my line — that territory is declared, never reached, at the line end 84',
                  'S03:12': "needs_info: the wall of the fermat-catalan boundary: the primitive solutions with reciprocal exponents under 1 are finite by the darmon-granville record (an ineffective finiteness), and their known forms all use 2 as an exponent — exactly the solutions my band's own 'all exponents above two' condition excludes (seven cubed plus thirteen squared equals two to the ninth, three to the fifth plus ten squared equals seven cubed, two to the fifth plus seven squared equals three to the fourth); they live just outside my line's box, named of record, never as values, at the line end 84",
                  'S03:13': 'needs_info: the anchor of the closed case: the equal-exponent corner where all three exponents stand above 2 is the fermat last theorem itself — no positive-integer solutions (the wiles record of 1994): a closed anchor named, not computed, never a value of mine, at the line end 84'}}

FROZEN: dict[str, Any] = FROZEN_DATA

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

# --- Stage-A discipline (frozen at build): the carried corpus is
# reproduced by PROBE (seam carries), never by re-assertion. No S4–S16
# lesson phrase, no S6–S16 theorem statement, appears in the S17
# script verbatim.
_StageA_ALL_LESSONS = (
    {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS,
     **S9_LESSONS, **S11_LESSONS, **S12_LESSONS, **S13_LESSONS, **S14_LESSONS,
     **S15_LESSONS, **S16_LESSONS}
)
_StageA_ALL_THEOREMS = (
    {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS,
     **S11_THEOREMS, **S12_THEOREMS, **S13_THEOREMS, **S14_THEOREMS, **S15_THEOREMS,
     **S16_THEOREMS}
)
_stagea_script = [t for s in FROZEN["script"].values() for t in s]
for _ph in _StageA_ALL_LESSONS:
    assert _ph not in _stagea_script, f"Stage-A: a carried lesson is re-asserted in the S17 script: {_ph[:60]!r}"
for _m in _StageA_ALL_THEOREMS.values():
    assert _m["statement"] not in _stagea_script, "Stage-A: a carried theorem statement appears in the S17 script"


_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.21-run1"]:
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
            s: {"parts": tuple(S17_THEOREMS[s]["parts"]), "statement": S17_THEOREMS[s]["statement"]}
            for s in ("lte-ledger", "beal-line-satisfaction")
        },
    }


def run_e6_21(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.20 S16 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S17 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.21-run1", "e6.21-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.20 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)

    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.21-run1", "e6.21-run2"):
        (out_dir / name / "e6.21-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.21.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.21-run1"
    root2 = out_dir / "e6.21-run2"
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
        **S16_LESSONS,
        **S17_LESSONS,
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inherited from S13/S16): NO
    # S17 fact carries the hypothesis marker (the valuation band is
    # unconditional mathematics); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S17 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s17_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s17_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S17 is the unconditional valuation band)")
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
        "marker_absent_facts": list(s17_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S17 script + all responses + band lessons (S4–S9 + S11–S17) + all thirty-six theorem statements",
    }

    # P1 — the contract: 51 turns, every turn on the det arm and
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
    _s2dom = [t["domain"] for k, t in sorted(turns.items()) if k.startswith("S02:")]
    _first_l = _s2dom.index("L")
    if _first_l < 2 or any(d != "U" for d in _s2dom[:_first_l]):
        p1_bad.append("the S2 pre-lesson gaps do not all run BEFORE the first teach")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — the typed honesty: the SEVEN pre-lesson gaps, the FOUR
    # teach turns (lesson facts stored), the TWO part-set failures
    # (named, needs_info, ungrounded, store-inert: the lte-ledger
    # scaffold short the valuation-def; the beal-line-satisfaction
    # scaffold short the census-def), the ONE missing-part
    # articulation (the full part-set named, both parts untaught:
    # the beal-def or the census-def), the TWO derive successes
    # (stored, grounded exactly on the sanctioned parts), the
    # frozen domain sequences, the line end, and ZERO seeded-fact
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
        if str(ir.get("answer", "")) != _th17(slug):
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
    # full S4–S16 lemma canon, the full thirty-five-theorem DAG,
    # the 128 seam-family facts, the conj still open).
    p3_bad: list[str] = []
    # the wall-carried rows (S04:05: the S15 BSD-touch wall carried into
    # S16 and still honest): the bytes hold, the honesty holds, nothing
    # is cited, nothing is written.
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
        "wall_carried_rows": p3_wall_carried,
    }

    # P4 — the 15 beds exact + grounded (the ON-LINE census answers:
    # the valuation probes, the LTE instances, the ledger count, the
    # statement, the census, the families, the band state, the
    # unconditionality), the 3 walls honest with their frozen bytes
    # and articulations (the primitive territory, the fermat-catalan
    # boundary, the fermat anchor — each naming its record place AND
    # the line end), and the W-S17 wall bytes byte-identical to the
    # Brainstem class attributes (the D-e6k(b) pattern, frozen). No
    # NEW off-line decimal enters the floor at S17 (offline_watch is
    # empty; the 3-powerful counterexample scale is named at its
    # order, never as a digit string).
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
        W_S17_1 == Brainstem.W_S17_1
        and W_S17_2 == Brainstem.W_S17_2
        and W_S17_3 == Brainstem.W_S17_3
    ):
        p4_bad.append("a W-S17 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S17-1..W-S17-3 (cross-checked, never surfaced)",
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant (BSD-flavored at the summit band; here strengthened
    # to the Beal candidate): NO fact id the conj uses appears in a
    # grounded list; NO `theorem:bsd` assertion exists AND NO
    # `theorem:beal` assertion exists (if non-empty: STOP, human
    # review, full evidence, never a threshold loosening); the conj
    # fact byte-identical to the seed (open, declared-source); the
    # bed owners (the frozen citation sets); the theorem allow-set;
    # and the SEMANTIC seam (the AGREEMENT, measured by the
    # mechanism's own python): (a) the CENSUS — every one of the 83
    # box triples is a true equation carrying its common-prime
    # factor, zero primitive; (b) the LEDGER — the lift-the-exponent
    # identity re-derived over the whole box (249,280 instances,
    # zero deviations); (c) the STATEMENT — the beal-line-satisfaction
    # composition stands on its strict parts with the census
    # invariant (83 / 0) inside its statement; (d) the queue
    # grounding — every fact id the declared queue lots name exists.
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S17 has no conj-teach turn)")
        # the BARE conj ids only (the summit compositions
    # theorem:bsd-panel-satisfaction and
    # theorem:beal-line-satisfaction are the sanctioned summit facts,
    # not the candidates):
    bsd_th = [a.id for a in final.query() if a.id == "theorem:bsd"]
    beal_th = [a.id for a in final.query() if a.id == "theorem:beal"]
    if bsd_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {bsd_th} — the sanctioned corpus now produces theorem:bsd")
    if beal_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {beal_th} — the sanctioned corpus now produces theorem:beal")
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
    # (a)+(b)+(c) the summit destinations (mechanism vs record
    # arithmetic): (a) the CENSUS — every one of the 83 box triples
    # is a true equation with the recorded common factor (the spf of
    # the gcd) and zero primitive triples in the box; (b) the
    # LEDGER — the lift-the-exponent identity re-derived over the
    # WHOLE box (the odd primes at or below the line end, the
    # difference a multiple of the prime with neither term divisible
    # by it, the exponents three through the line end): 249,280
    # instances, zero deviations; (c) the STATEMENT — the
    # beal-line-satisfaction composition's statement carries the
    # census invariant (eighty-three / zero) and the line end.
    d_bad: list[str] = []
    _beal_count, _beal_prim, _beal_rows = _beal_py_census()
    if (_beal_count, _beal_prim) != (83, 0):
        d_bad.append(f"the census re-drifted: {_beal_count} triples / {_beal_prim} primitive (expected 83 / 0)")
    if _beal_rows != S17_BEDS["census"]:
        d_bad.append("the census rows drifted off the line")
    for r in _beal_rows:
        if r[0] ** r[3] + r[1] ** r[4] != r[2] ** r[5]:
            d_bad.append(f"triple {r[:6]} is not a true equation (the census wrote a non-solution)")
            break
    _inst, _fail, _dig = _beal_py_lte_box()
    if (_inst, _fail) != (249280, 0):
        d_bad.append(f"the lte ledger re-drifted: {_inst} instances / {_fail} failures (expected 249280 / 0)")
    if S17_BEDS["lte_max_digits"] != _dig:
        d_bad.append("the lte ledger scale drifted")
    if not ("eighty-three" in _th17("beal-line-satisfaction") and "no primitive triple" in _th17("beal-line-satisfaction")
            and "at the line end 84" in _th17("beal-line-satisfaction")):
        d_bad.append("the beal-line-satisfaction statement lost the census invariant or the line end")
    for b in d_bad:
        p5_bad.append(f"summit destination: {b} — TIER-2 breakthrough candidate (PENDING owner)")
    # (d) the queue grounding (the queue-declared lesson names fact
    # ids; every id it names exists in the final store — the S12
    # standing soil check, self-parsed from the store fact itself):
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
    import re as _re_p5
    for fid in _re_p5.findall(r"(?:lemma|theorem):[a-z0-9-]+", qtext):
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
            "discovery_candidate_beal_theorem_facts": beal_th,
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "summit_destination_bad": d_bad[:10],
            "summit_destination_agreement": not d_bad,
            "queue_missing": queue_missing,
            "queue_source": "lemma:queue-declared (self-parsed)",
        },
    }

    # P6 — the SEAM carry (the SIX rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime:
    # the BSD summit carry, the S16 order carry, the S16 torsion
    # carry, the S16 L-value wall carry, the S15 ramification
    # correction, and the queue) + the one OFF-SCRIPT carry probe
    # (the bsd-panel-satisfaction state byte-identical — the S16
    # summit soil check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.21-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E621)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S17-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 104 seed concepts: the carried
    # correct-derivation counts equal their S16-final base + the
    # frozen drill at the NEW S17 coordinates; NO state REGRESSION —
    # a carried concept may only move stable->stable or
    # practicing->stable (the sanctioned improvement); the four NEW
    # concepts at their frozen band-end values with their frozen
    # prereq-gap sets — all four stable, prereq gaps empty: the S11
    # soil (first-divisor, divides, scan-ledger) and the S17 band
    # lessons clear every prereq of record).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E621])
    _S17_NEW = [c.id for c in CONCEPT_S17]
    for cid in list(FROZEN["pre_s17_states"]) + _S17_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s17_drilled"] if isinstance(FROZEN["pre_s17_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s17_states"].items():
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
        "carried_refs": len(FROZEN["pre_s17_states"]),
        "drilled": drilled,
        "improved_to_stable": sorted(improved),
        "expected": {k: FROZEN["mastery_expected"][k] for k in sorted(FROZEN["mastery_expected"])},
    }

    # P8 — the store totals, the seed identity, the line census,
    # the SIX new facts, the determinism twin, the run/store
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
    if runs["e6.21-run1"] != runs["e6.21-run2"]:
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
            "determinism_twin": runs["e6.21-run1"] == runs["e6.21-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.21-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s17_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_21Experiment:
    """E6.21 — S17 of the PRIZE-ISLANDS-TRACK (the Beal island — its
    single band): the valuation line. The valuation reads the p-adic
    depth off the first-divisor chain (the S11 soil); the
    lift-the-exponent ledger verifies the classical odd-p identity in
    every one of its 249,280 box instances; the Beal statement —
    verbatim per the ams beal prize record — is stored as the
    island's summit fact (declared record); the verification census
    holds 83 triples in the box, every one carrying its common prime
    factor, zero primitive on the line; the primitive territory, the
    fermat-catalan boundary, and the fermat anchor are walls."""

    name = "e6.21"
    hypothesis = (
        "S17 of the PRIZE-ISLANDS-TRACK (the Beal island — its single band) walks THE VALUATION LINE "
        "over the carried S16 seed (1581): the valuation — the p-adic depth read off the p-rung of "
        "the first-divisor factorization chain (the S11 soil); the lift-the-exponent identity, the "
        "classical odd-p form, verified in every one of the 249,280 instances of the line's ledger "
        "box (zero deviations); the Beal statement — verbatim per the ams beal prize record (A^x + "
        "B^y = C^z with x, y, z > 2 forces a common prime factor of A, B, C) — stored as the "
        "island's summit fact with the composition beal-line-satisfaction on the strict part set "
        "(beal-def + census-def); the verification census: exactly 83 triples in the box (bases at "
        "or below the line end 84, exponents three through ten of record), every one carrying its "
        "common prime factor, zero primitive on the line. It stores SIX new deterministic facts: "
        "four lessons (valuation-def, lte-def, beal-def, census-def) and two compositions "
        "(lte-ledger, beal-line-satisfaction), the seam census closing 122+6 -> 128. The primitive "
        "territory, the fermat-catalan boundary, and the fermat closed anchor sit on walls W-S17-"
        "1/2/3 (the 3-powerful counterexample scale named at its order, never as a digit string); "
        "NO NEW decimals enter the floor. The line stays 0..84 (zero new successor facts); the "
        "riemann conj stays open, byte-identical to the seed; NO theorem:beal and NO theorem:bsd "
        "exist (the bare conj ids are the discovery-candidate invariants: the summits are stored as "
        "declared record facts + the satisfaction compositions, never as the bare conjecture ids); "
        "the SIX seam rows (the BSD summit carry, the S16 order carry, the S16 torsion carry, the "
        "S16 L-value wall, the S15 ramification correction, the queue) byte-identical to the seed "
        "store; the bsd-panel-satisfaction state byte-identical off-script; two runs byte-identical. "
        "The Beal island's $1,000,000 (the ams beal prize) now stands in the store the way the BSD "
        "island's did: the statement a declared record fact, the line's side held exact, the "
        "candidate a wall."
    )
    metric = "S17 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_21()
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
                Path("results/phase-6/e6.21-run1/session-S02.json"),
                Path("results/phase-6/e6.21-run1/session-S03.json"),
                Path("results/phase-6/e6.21-run1/session-S04.json"),
                Path("results/phase-6/e6.21-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
