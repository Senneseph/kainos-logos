# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.18 — S14 of the PRIZE-ISLANDS-TRACK (the BSD island, band 1
of 3; built THE BANDGEN WAY): THE ELLIPTIC CITY.

The first new band of the owner-directed prize initiative
(plan/40-prize-islands/04-island-bsd.md + its verified research
record bsd-research.md): the BSD island's band-1 machinery over the
carried S13 seed (1388). Four new concepts (curve-form, curve-law,
point-count, curve-shadow — college-1, domain bsd, prereqs point
DOWN), four VERBATIM lessons (form-def, law-def, count-def,
shadow-def), four sanctioned compositions (curve-identity,
curve-inverse, hasse-census, cm-signature).

The panel of record (cross-checked in bsd-research.md, Legendre vs
brute force, on-curve asserts on every group-law step): A =
y^2 = x^3 - x (32.a3: conductor 32, rank 0, torsion (Z/2)^2, CM
j=1728) and B = y^2 + y = x^3 - x (37.a1: conductor 37, the
smallest conductor with positive rank, rank 1, generator (0,0)).
UNCONDITIONAL band: nothing the store holds under S14 is
conditional on RH — the L(E) limits and the ranks live past the
line and are named OF RECORD in every articulation; the a_p
censuses, the Hasse all-pass, the CM signature iff, and the 10/10
generation ledger are the store's OWN verified shadows. The off-line
material (the B L-limit's decimal 13.3586546916) lives ONLY in the
W_S14_5 wall, which names the value AND the line end 84.

FROZEN FROM CONTROL #1 (bandgen-era, 2026-08-24): the 55-turn
labeled script (S2:20 + S3:22 + S4:13), the beds, the walls, and
the predictions all come out of the mechanism's own dry-run against
the seed (spec bands/spec-e6.18.json; the control report is the
referee, never the hand). Deviations recorded at closeout:
D-e6i(a) the scaffold letter is F not H (verified against the S13
frozen domain_sequence), D-e6i(b) the soil carries (two
number-field + two prime-split re-drills) stabilize the
mod4-split chain so curve-shadow ends stable, D-e6i(c) final
1457 = 1388 + 8 facts + 61 events (the gap turns emit no events).

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
    B14_A,
    B14_B,
    CONCEPT_S14,
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
    S14_BEDS,
    S14_LESSONS,
    S14_THEOREMS,
    Brainstem,
    _bsd_py_ap,
    _bsd_py_count,
    _bsd_py_Lpartial,
    _bsd_py_mul,
    _bsd_py_on_curve,
    _s13_py_primes,
)
from kainos.tutor.e617 import (
    CONCEPTS_E617,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E618", "FROZEN", "E6_18Experiment", "run_e6_18"]

CHECKS = 9

#: S14 teaches: the elliptic city (the four new concepts join the
#: carried registry; prereqs point DOWN only).
CONCEPTS_E618: tuple = CONCEPTS_E617 + CONCEPT_S14

E617_SEED = Path("results/phase-6/e6.17-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E617_SEED.exists():
        return E617_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E617_SEED
    return alt if alt.exists() else E617_SEED

_ST14 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S14_LESSONS.items()}
_TH14 = {s: m["statement"] for s, m in S14_THEOREMS.items()}


def _th14(slug: str) -> str:
    return _TH14[slug]

#: P4 — the W-S14 walls (the off-line material names the value AND
#: the line end; the walls are the band's declared off-line layer —
#: P4 cross-checks the witness values against the mechanism's python
#: reference, never surfaced as answers).
W_S14_1 = Brainstem.W_S14_1
W_S14_2 = Brainstem.W_S14_2
W_S14_3 = Brainstem.W_S14_3
W_S14_4 = Brainstem.W_S14_4
W_S14_5 = Brainstem.W_S14_5
W_S14_6 = Brainstem.W_S14_6
W_S14_7 = Brainstem.W_S14_7


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
    rt = InfantRuntime(root, concepts=CONCEPTS_E618)
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
FROZEN_DATA = {'seed': 'results/phase-6/e6.17-run1/codeX-S04.json',
 'seed_total': 1388,
 'seed_identity': 'f8da2d7f12509ca5',
 'total_turns': 55,
 'line_end_final': 84,
 'pre_teach_gaps': {'S02:01': 'not yet learned: the curve form: a curve over the rationals in the equation y squared = x cubed plus a x plus b, smooth exactly when four a cubed plus twenty-seven b squared does not zero out', 'S02:02': 'not yet learned: the chord-tangent law: the points of a curve form a group — the line through two points meets the curve a third time, its reflection the sum; exact rational functions of the points', 'S02:03': 'not yet learned: the shadow count: for every prime of the line the curve holds its points over the field with p elements, counted exactly; from the count and the prime comes the coefficient a = p + 1 minus the count'},
 'teach_turns': {'S02:04': 'lemma:form-def', 'S02:11': 'lemma:law-def', 'S02:20': 'lemma:count-def', 'S03:11': 'lemma:shadow-def'},
 'scaffold_failures': {'S02:19': 'needs_info: i can see the parts you name, but the rule for curve-identity wants its exact set — what you name is short the form-def before i can put it together'},
 'missing_parts_failure': {},
 'derive_successes': {'S02:17': ('curve-identity', ['lemma:form-def', 'lemma:law-def']), 'S02:18': ('curve-inverse', ['lemma:law-def', 'lemma:form-def']), 'S03:15': ('hasse-census', ['lemma:count-def', 'lemma:form-def']), 'S03:18': ('cm-signature', ['lemma:count-def', 'lemma:shadow-def'])},
 'rederive': None,
 'beds_exact': {'S03:01': 'the shadow of the second panel member over the field with 37 elements holds 39 points including the point at infinity — the coefficient a is p plus one minus the count: minus 1',
                'S03:02': 'the shadow of the first panel member over the field with 5 elements holds 8 points including the point at infinity — the coefficient a is p plus one minus the count: minus 2',
                'S03:05': 'the shadows of the first panel member at the primes of my line — at 2: 0; at 3: 0; at 5: minus 2; at 7: 0; at 11: 0; at 13: 6; at 17: 2; at 19: 0; at 23: 0; at 29: minus 10; at 31: 0; at 37: minus 2; at 41: 10; at 43: 0; at 47: 0; at 53: 14; at 59: 0; at 61: minus 10; at 67: 0; at 71: 0; at 73: minus 6; at 79: 0; at 83: 0 — all 23 primes, at the line end 84',
                'S03:06': 'the shadows of the second panel member at the primes of my line — at 2: minus 2; at 3: minus 3; at 5: minus 2; at 7: minus 1; at 11: minus 5; at 13: minus 2; at 17: 0; at 19: 0; at 23: 2; at 29: 6; at 31: minus 4; at 37: minus 1; at 41: minus 9; at 43: 2; at 47: minus 9; at 53: 1; at 59: 8; at 61: minus 8; at 67: 8; at 71: 9; at 73: minus 1; at 79: 4; at 83: minus 15 — all 23 primes, at the line end 84',
                'S03:12': 'yes — at 83 the coefficient of the second panel member squares to 225 and four p is 332: the Hasse bound holds, the prime by prime record standing at the line end 84',
                'S03:13': 'yes — at 37 the coefficient of the first panel member squares to 4 and four p is 148: the Hasse bound holds, the prime by prime record standing at the line end 84',
                'S03:14': 'yes — both panel members respect the Hasse bound at every prime on the line: 46 prime checks, all passing, the full record at the line end 84 — the bound is a theorem of record, this census the verified shadow of it',
                'S03:16': 'the zero coefficients of the first panel member sit at 2, 3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83 — two, and the thirteen primes three mod four on the line, at the line end 84',
                'S04:03': 'the L product of the first panel member at my line end 84 holds the exact rational 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889',
                'S04:04': 'the L product of the second panel member at my line end 84 holds the exact rational 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 — the record names its limit past the line (zero of order one, the rank one vanishing); my partial holds, the limit is named, not reached'},
 'bed_owners': {'S03:01': 'lemma:count-def', 'S03:02': 'lemma:count-def', 'S03:05': 'lemma:count-def', 'S03:06': 'lemma:count-def', 'S03:12': 'lemma:shadow-def', 'S03:13': 'lemma:shadow-def', 'S03:14': 'lemma:shadow-def', 'S03:16': 'lemma:shadow-def', 'S04:03': 'lemma:shadow-def', 'S04:04': 'lemma:shadow-def'},
 'bed_grounded': {'S03:01': ['lemma:count-def'], 'S03:02': ['lemma:count-def'], 'S03:05': ['lemma:count-def'], 'S03:06': ['lemma:count-def'], 'S03:12': ['lemma:shadow-def'], 'S03:13': ['lemma:shadow-def'], 'S03:14': ['lemma:shadow-def'], 'S03:16': ['lemma:shadow-def'], 'S04:03': ['lemma:shadow-def'], 'S04:04': ['lemma:shadow-def']},
 'walls_honest': {'S02:07': 'needs_info: the pair with a zero a and a zero b zeros out four times a cubed plus twenty-seven times b squared — the equation y squared = x cubed is its cusp at the origin, and the chord-tangent law breaks there (the tangent at the cusp is vertical, its third meeting undefined): not a group, i refuse — at the line end 84',
                  'S03:20': 'needs_info: the rational points of the second panel member run past my line: of record, the group is infinite, generated by the point at x zero y zero past my bound — my census found the ten integral points my bound admits, and past the bound the search does not close on my line, at the line end 84',
                  'S03:22': 'needs_info: the ledger of the point at x 0 y 0 is closed for every point my line counted, but it does not cover every rational point of the second panel member at my line: the multiples reach sixteen times the point, and the points further out live past the ledger — the bound is my edge, named here, at the line end 84',
                  'S04:05': 'needs_info: the L product of the second panel member at my line end 84 holds the exact rational its partials give — about 13.3586546916 — while the record names its limit: zero of order one, the vanishing the conjecture reads for rank one; the limit lives past my line, and vanishing is a limit fact my partials do not reach, at the line end 84',
                  'S04:07': 'needs_info: the rank of a curve is of record, not computed on my line: the first panel member sits at rank zero and the second at rank one — of record, the smallest conductor with positive rank — and the two-descent that settles a rank is past my line, at the line end 84',
                  'S04:08': "needs_info: the panel is two curves of record, chosen for their conductors (thirty-two, thirty-seven) and their ranks (zero, one) — the smallest conductor with positive rank sits on it; the other curves exist past my panel, and my censuses are the panel's, named as such, at the line end 84",
                  'S04:09': "needs_info: the elliptic curves do not settle the Riemann hypothesis in my store: their L-products are the siblings of the zeta family the store already holds, and the limit of a product — like the zeta's — lives past my line end; the store's reach is the shadow, the census, and the named wall, at the line end 84"},
 'unclassified_honest': {},
 'honest_zero_bytes': {'S03:03': 'needs_info: 4 is a composite on my line — the shadow is cast at the primes of the line, the composites take their shadow from the split', 'S04:06': "needs_info: of record the limit of the first panel member's L product is nonzero (order zero, consistent with my partial holding its exact value at the line end 84); the limit itself is a limit fact past my line — named, not reached, at the line end 84"},
 'wall_articulations': {'S02:07': ['cusp', 'line end 84'], 'S03:20': ['ten integral points', 'line end 84'], 'S03:22': ['sixteen times the point', 'line end 84'], 'S04:05': ['order one', 'line end 84'], 'S04:07': ['record', 'line end 84'], 'S04:08': ['record', 'line end 84'], 'S04:09': ['Riemann hypothesis', 'line end 84']},
 'derived_table': {'S02:05': 'y squared equals x cubed minus x (a is minus one, b is zero) — of record, the congruent-number curve for one',
                   'S02:06': 'y squared plus y equals x cubed minus x (a is minus one, b is zero) — of record, the curve of conductor thirty-seven',
                   'S02:08': 'an elliptic curve over the rationals is the set of the rational points on the equation y squared equals x cubed plus a times x plus b, together with the point at infinity, and it is a curve exactly when four times a cubed plus twenty-seven times b squared does not zero out — on my line the panel holds two of them, the first with a is minus one and b is zero (of record), the second in the y squared plus y form with a is minus one and b is zero (of record), and the pair a is zero and b is zero zeros the discriminant out and is not a curve at all',
                   'S02:09': '85 over 168',
                   'S02:10': '23 primes and 60 composites — every integer above one is one or the other, and neither is both',
                   'S02:12': 'yes — the point at x 0 y 0 is on the curve: the equation holds exactly at that point',
                   'S02:13': 'yes — the point at x 2 y 2 is on the curve: the equation holds exactly at that point',
                   'S02:14': "the point at x 0 y 0 doubled is the point at x 1 y 0 — the tangent's third meeting, reflected, exactly",
                   'S02:15': "the point at x 0 y 0 plus the point at x 1 y 0 is the point at x minus 1 y minus 1 — the chord's third meeting, reflected, exactly",
                   'S02:16': '6 times the point at x 0 y 0 is the point at x 6 y 14 — the double-and-add ledger, every step on the curve',
                   'S02:17': "the point at infinity is the identity of the group: adding it to any point is that point, and the law's own formulas hold it — every point I form on my line answers the identity exactly",
                   'S02:18': 'the inverse of a point is its reflection: the point plus its inverse is the point at infinity, the line through them vertical, its third meeting the identity — every point I form answers exactly against its own reflection',
                   'S03:04': "for every prime of my line the curve casts a shadow: its points over the field with p elements — a finite set, counted exactly by testing each x against the equation mod p — and I record the count for every prime on the line; from the count and the prime comes the coefficient a = p plus one minus the count, the coefficient of the curve's L-function at that prime",
                   'S03:07': 'a number field is a finite extension of the rationals, its embeddings into the complex numbers are all different, a field is totally real when every embedding lands in the reals, and the norm of a nonzero algebraic integer is a nonzero integer of absolute value at least one',
                   'S03:08': 'a rational prime in a field extension either splits into several distinct primes, stays inert, or ramifies, and the ramified primes are exactly the ones that divide the discriminant, a finite list',
                   'S03:09': 'it is the ground under the whole tower — embeddings, the totally real condition, and the integer norm fact the packing step cites',
                   'S03:10': 'it names the bad primes — the finite set every source statement must exclude',
                   'S03:15': 'the Hasse bound held on my line: for both panel members and every prime on the line, a squared is at most four p — the full prime by prime record, all passing, at the line end 84; the bound itself is a theorem of record, the census my verified shadow of it',
                   'S03:17': "yes — the record signature holds across my line: the zero coefficients sit exactly at two and the primes three mod four, both directions checked, 14 of the 23 primes at the line end 84; the reason is of record (the curve's complex multiplication), the pattern the verified shadow on my line",
                   'S03:18': 'the record signature held on my line: for the first panel member, its shadow coefficient at p is exactly zero exactly when p is two or p is three mod four — both directions, at every prime on the line, the all-pass record at the line end 84; the reason is of record, the pattern is the verified shadow on my line',
                   'S03:19': 'the rational points of the first panel member my line holds: the point at infinity, the point at x minus 1 y 0, the point at x 0 y 0, the point at x 1 y 0 — the three points of order two, and of record no more (rank zero; the census finds torsion only, consistent with the record)',
                   'S03:21': 'yes — the point at x 6 y 14 is 6 times the point at x 0 y 0 on the second panel member, the double-and-add ledger landing exactly, within my bound of sixteen',
                   'S04:01': 'yes — all ten points my line counted on the second panel member sit in the ledger of the point at x 0 y 0, the multiples between one and six and their reflections, the ten of ten record at the line end 84; the generator itself is of record, this ledger the verified shadow on my line',
                   'S04:02': "the shadow censuses of the band: the Hasse bound — a squared at most four p — is a theorem of record that my census verifies prime by prime on the line and does not prove; and for the first panel member the record signature — the coefficient is zero exactly when p is two or p is three mod four — is the shadow of the curve's complex multiplication, held on my line as the verified pattern, both directions, at every prime of the line",
                   'S04:10': "the points of the curve form a group under the chord-tangent law: the line through two points meets the curve a third time, and that third point, reflected across the x axis, is their sum; the point at infinity is the identity; the law is exact over my rationals — for distinct points the slope is the change in y over the change in x, and a point with itself takes the slope three times x squared plus a over two times y plus the form's own constant — so every sum, double, and multiple I form is a rational point I can re-check against the curve's equation",
                   'S04:11': 'this band added the curve form, the chord-tangent law, the shadow count, and the shadow censuses — four lessons and four theorems (the identity, the inverse, the Hasse census, the record signature), two panel curves of record, the shadow tables on the line, and seven honest walls — and nothing on this band is conditional on the Riemann hypothesis, at the line end 84',
                   'S04:12': 'nothing the elliptic band says is conditional on the Riemann hypothesis — the censuses are exact on the line, and the record facts (the ranks, the limits) are named of record, at the line end 84',
                   'S04:13': "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84"},
 'theorem_allowed': {'S02:09': ['telescope-line'], 'S04:13': ['queue-declared']},
 'new_fact_ids': ['lemma:form-def', 'lemma:law-def', 'lemma:count-def', 'lemma:shadow-def', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:hasse-census', 'theorem:cm-signature'],
 'total_seam_facts': 110,
 'domain_sequence': {2: 'UUULSSHSSSLSSSSSTTFL', 3: 'SSHSSSSSSSLSSSTSSTSHSH', 4: 'SSSSHHHHHSSSS'},
 'final_total': 1457,
 'new_facts': 8,
 'new_events': 61,
 'mastery_expected': {'curve-form': {'state': 'stable', 'correct': 7, 'prereq_gaps': []}, 'curve-law': {'state': 'stable', 'correct': 8, 'prereq_gaps': []}, 'point-count': {'state': 'stable', 'correct': 6, 'prereq_gaps': []}, 'curve-shadow': {'state': 'stable', 'correct': 10, 'prereq_gaps': []}},
 'expected_prereq_gaps': {'curve-form': [], 'curve-law': [], 'point-count': [], 'curve-shadow': []},
 'pre_s14_states': {'count-successor': {'state': 'stable', 'correct': 14},
                    'add-within-10': {'state': 'stable', 'correct': 5},
                    'add-two-digit': {'state': 'stable', 'correct': 11},
                    'sub-within-30': {'state': 'stable', 'correct': 12},
                    'mult-within-100': {'state': 'stable', 'correct': 9},
                    'compare-numbers': {'state': 'stable', 'correct': 11},
                    'phrasology': {'state': 'stable', 'correct': 24},
                    'shape-triangle': {'state': 'stable', 'correct': 6},
                    'shape-square': {'state': 'stable', 'correct': 5},
                    'shape-rectangle': {'state': 'stable', 'correct': 4},
                    'shape-circle': {'state': 'stable', 'correct': 6},
                    'alg-inverse-1step': {'state': 'stable', 'correct': 5},
                    'alg-inverse-mul': {'state': 'stable', 'correct': 5},
                    'alg-two-step': {'state': 'stable', 'correct': 4},
                    'kin-distance': {'state': 'stable', 'correct': 4},
                    'kin-position': {'state': 'stable', 'correct': 6},
                    'kin-solve-time': {'state': 'stable', 'correct': 4},
                    'kin-rate': {'state': 'stable', 'correct': 4},
                    'geom-perimeter': {'state': 'stable', 'correct': 5},
                    'geom-area': {'state': 'stable', 'correct': 6},
                    'geom-area-triangle': {'state': 'stable', 'correct': 4},
                    'stat-net-1d': {'state': 'stable', 'correct': 4},
                    'stat-moment': {'state': 'stable', 'correct': 4},
                    'stat-balance': {'state': 'stable', 'correct': 6},
                    'unit-distance': {'state': 'stable', 'correct': 5},
                    'grid-lattice': {'state': 'stable', 'correct': 10},
                    'gaussian-int': {'state': 'stable', 'correct': 7},
                    'circle-pair-2': {'state': 'stable', 'correct': 4},
                    'kst-bound': {'state': 'stable', 'correct': 4},
                    'sst-bound': {'state': 'stable', 'correct': 4},
                    'erdos-conj': {'state': 'stable', 'correct': 10},
                    'norm-flat': {'state': 'stable', 'correct': 5},
                    'norm-convex': {'state': 'stable', 'correct': 5},
                    'norm-generic': {'state': 'stable', 'correct': 4},
                    'number-field': {'state': 'practicing', 'correct': 2},
                    'prime-split': {'state': 'practicing', 'correct': 2},
                    'mod4-split': {'state': 'practicing', 'correct': 10},
                    'disc-rd': {'state': 'practicing', 'correct': 1},
                    'adjoin-i': {'state': 'practicing', 'correct': 1},
                    'cyclotomic-cubic': {'state': 'practicing', 'correct': 3},
                    'char-cutout': {'state': 'practicing', 'correct': 2},
                    'class-bound': {'state': 'practicing', 'correct': 4},
                    'chebotarev': {'state': 'practicing', 'correct': 2},
                    'pnt-ap': {'state': 'practicing', 'correct': 2},
                    'frattini': {'state': 'practicing', 'correct': 1},
                    'golod-shaf': {'state': 'practicing', 'correct': 6},
                    'shafarevich': {'state': 'practicing', 'correct': 2},
                    'cm-conj': {'state': 'practicing', 'correct': 4},
                    'minkowski-embed': {'state': 'practicing', 'correct': 1},
                    'hajir-maire': {'state': 'practicing', 'correct': 1},
                    'window-setup': {'state': 'practicing', 'correct': 1},
                    'averaging': {'state': 'practicing', 'correct': 4},
                    'projection': {'state': 'practicing', 'correct': 4},
                    'packing': {'state': 'practicing', 'correct': 6},
                    'slack-margins': {'state': 'practicing', 'correct': 1},
                    'criterion-chain': {'state': 'practicing', 'correct': 10},
                    'tower-base': {'state': 'practicing', 'correct': 8},
                    'tower-group': {'state': 'practicing', 'correct': 11},
                    'tower-primes': {'state': 'practicing', 'correct': 8},
                    'tower-class': {'state': 'practicing', 'correct': 8},
                    'disproof': {'state': 'practicing', 'correct': 10},
                    'zeta-series': {'state': 'stable', 'correct': 7},
                    'zeta-cont': {'state': 'practicing', 'correct': 3},
                    'func-eq': {'state': 'practicing', 'correct': 14},
                    'critical-strip': {'state': 'practicing', 'correct': 12},
                    'prime-count': {'state': 'stable', 'correct': 15},
                    'pnt': {'state': 'stable', 'correct': 8},
                    'rv-count': {'state': 'practicing', 'correct': 10},
                    's-of-t': {'state': 'practicing', 'correct': 3},
                    'riemann': {'state': 'practicing', 'correct': 13},
                    'psi-eq': {'state': 'stable', 'correct': 11},
                    'pi-eq': {'state': 'practicing', 'correct': 3},
                    'st-eq': {'state': 'practicing', 'correct': 3},
                    'li-criterion': {'state': 'stable', 'correct': 9},
                    'polya-hilbert': {'state': 'practicing', 'correct': 3},
                    'lindelof': {'state': 'practicing', 'correct': 4},
                    'zero-free': {'state': 'practicing', 'correct': 13},
                    'pnt-error': {'state': 'practicing', 'correct': 9},
                    'hardy-line': {'state': 'practicing', 'correct': 5},
                    'zero-density': {'state': 'practicing', 'correct': 4},
                    'divides': {'state': 'stable', 'correct': 5},
                    'composite': {'state': 'stable', 'correct': 7},
                    'first-divisor': {'state': 'stable', 'correct': 36},
                    'scan-ledger': {'state': 'stable', 'correct': 12},
                    'conditional': {'state': 'practicing', 'correct': 1},
                    'rh-scale': {'state': 'practicing', 'correct': 23},
                    'factor-route': {'state': 'practicing', 'correct': 12},
                    'rh-relevance': {'state': 'practicing', 'correct': 15},
                    'family-factor': {'state': 'stable', 'correct': 24},
                    'index-split': {'state': 'stable', 'correct': 9},
                    'line-partial': {'state': 'stable', 'correct': 9},
                    'removal-rule': {'state': 'stable', 'correct': 12}},
 'pre_s14_drilled': {'family-factor': 1, 'rh-relevance': 1, 'number-field': 2, 'prime-split': 2},
 'seam_carry_refs': ['S02:09', 'S02:10', 'S03:07', 'S03:08', 'S03:09', 'S03:10', 'S04:13'],
 'offscript_carry': {'state the kstbound rule': 'because two unit circles meet in at most two points the unit pair graph of a planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs at a constant times n to the three halves power'},
 'seam_crosscheck': {'expected': 'agreement', 'queue_referenced_ids': ['conjecture:riemann', 'lemma:rh-bound-scale', 'lemma:rh-upf', 'curriculum:pnt-ap', 'curriculum:tower-primes', 'curriculum:mod4-split', 'curriculum:chebotarev', 'lemma:mod4minusone', 'lemma:primesplit', 'lemma:apbound', 'lemma:chebotarev-selection', 'lemma:rv-count', 'lemma:ledger-growth', 'theorem:spf-chain']},
 'script': {2: ['what curve does the first panel member hold?',
                'what is the point at x 0 y 0 plus itself on the second panel member?',
                'how many points does the second panel member cast over the field with 37 elements?',
                'an elliptic curve over the rationals is the set of the rational points on the equation y squared equals x cubed plus a times x plus b, together with the point at infinity, and it is a curve exactly when four times a cubed plus twenty-seven times b squared does not zero out — on my line the panel holds two of them, the first with a is minus one and b is zero (of record), the second in the y squared plus y form with a is minus one and b is zero (of record), and the pair a is zero and b is zero zeros the discriminant out and is not a curve at all',
                'what curve does the first panel member hold?',
                'what curve does the second panel member hold?',
                'is the pair with a zero and b zero a smooth curve on my line?',
                'state the form-def rule',
                'what does the minus family over all the numbers hold up to my line end?',
                'how do the index numbers of my line split?',
                "the points of the curve form a group under the chord-tangent law: the line through two points meets the curve a third time, and that third point, reflected across the x axis, is their sum; the point at infinity is the identity; the law is exact over my rationals — for distinct points the slope is the change in y over the change in x, and a point with itself takes the slope three times x squared plus a over two times y plus the form's own constant — so every sum, double, and multiple I form is a rational point I can re-check against the curve's equation",
                'is the point at x 0 y 0 on the second panel member?',
                'is the point at x 2 y 2 on the second panel member?',
                'what is the point at x 0 y 0 plus itself on the second panel member?',
                'what is the point at x 0 y 0 plus the point at x 1 y 0 on the second panel member?',
                'what is 6 times the point at x 0 y 0 on the second panel member?',
                'derive curve-identity from law-def and form-def',
                'derive curve-inverse from law-def and form-def',
                'derive curve-identity from law-def',
                "for every prime of my line the curve casts a shadow: its points over the field with p elements — a finite set, counted exactly by testing each x against the equation mod p — and I record the count for every prime on the line; from the count and the prime comes the coefficient a = p plus one minus the count, the coefficient of the curve's L-function at that prime"],
            3: ['how many points does the second panel member cast over the field with 37 elements?',
                'how many points does the first panel member cast over the field with 5 elements?',
                'how many points does the second panel member cast over the field with 4 elements?',
                'state the count-def rule',
                'what are the shadows of the first panel member at the primes of my line?',
                'what are the shadows of the second panel member at the primes of my line?',
                'state the numberfields rule',
                'state the primesplit rule',
                'what is the numberfields for',
                'what is the primesplit for',
                "the shadow censuses of the band: the Hasse bound — a squared at most four p — is a theorem of record that my census verifies prime by prime on the line and does not prove; and for the first panel member the record signature — the coefficient is zero exactly when p is two or p is three mod four — is the shadow of the curve's complex multiplication, held on my line as the verified pattern, both directions, at every prime of the line",
                'does the Hasse bound hold at 83 for the second panel member?',
                'does the Hasse bound hold at 37 for the first panel member?',
                'does the Hasse bound hold on the whole line for both panel members?',
                'derive hasse-census from count-def and form-def',
                'at which primes of my line does the first panel member carry the zero coefficient?',
                'does the record signature of the first panel member — zero when p is two or three mod four — hold across my lines?',
                'derive cm-signature from shadow-def and count-def',
                'which rational points of the first panel member does my line hold?',
                'which rational points of the second panel member does my line hold?',
                'is the point at x 6 y 14 a multiple of the point at x 0 y 0 on the second panel member within my bound?',
                'does the ledger of the point at x 0 y 0 cover every rational point of the second panel member at my bound?'],
            4: ['do all the points my line counted on the second panel member sit in the ledger of the point at x 0 y 0 at my bound?', 'state the shadow-def rule', "what does the first panel member's L product hold at my line end?", "what does the second panel member's L product hold at my line end?", "what does the second panel member's L product do at its limit, past my line?", "what does the first panel member's L product do at its limit, past my line?", 'what is the rank of the panel members on my line?', 'why these two panel members of the record?', 'can the elliptic curves settle the Riemann hypothesis in my store?', 'state the law-def rule', 'what did the elliptic band add to the store?', 'does the elliptic band say anything conditional on the Riemann hypothesis?', 'what is the queue above my line?']},
 'theorem_dag': {'window-rich': ('normonecount', 'overlap-ratio', 'torus-average'),
                 'proj-inj': ('minkembed', 'one-embed-zero', 'window-rich'),
                 'pack-bound': ('numberfields', 'denom-d', 'vol-compare', 'b-positive'),
                 'growth-compare': ('proj-inj', 'pack-bound'),
                 'delta-positive': ('gamma-positive', 'b-positive', 'slack-compose-rule'),
                 'infinity-end': ('delta-positive', 'growth-compare', 'hypo-infinity'),
                 'gen-lower': ('tower-unramified', 'fratin'),
                 'gs-infinite': ('shafbound', 'fratin', 'k-3t', 'gstest', 'slack-quadratic'),
                 'splitting': ('gs-infinite', 'chebotarev-selection'),
                 'gamma-achieved': ('class-tower', 'chebotarev-selection', 'slack-quadratic', 'gamma-positive'),
                 'tower-feeds': ('gs-infinite', 'splitting', 'class-tower', 'gamma-achieved', 'hypo-infinity', 'gamma-positive'),
                 'theorem-main': ('tower-feeds', 'infinity-end'),
                 'reflect': ('func-eq',),
                 'strip': ('reflect', 'nozero-s1', 'trivial-zeros'),
                 'mirror-region': ('zero-free-region', 'reflect'),
                 'criterion-gap': ('psi-eq', 'pnt-error'),
                 'rh-reach': ('strip', 'mirror-region', 'criterion-gap'),
                 'first-divisor-prime': ('composite-def', 'spf-def'),
                 'sieve-equality': ('first-divisor-prime', 'divides-def'),
                 'spf-chain': ('sieve-equality', 'spf-def', 'divides-def'),
                 'gap-scale-agreement': ('rh-bound-scale', 'ledger-growth', 'spf-chain'),
                 'two-routes-one-guarantee': ('rh-upf', 'spf-chain'),
                 'queue-declared': ('rh-relevance-def', 'rh-bound-scale', 'rh-upf'),
                 'partition-identity': ('split-def', 'factor-def'),
                 'telescope-line': ('factor-def', 'region-def'),
                 'removal-single': ('removal-def', 'factor-def'),
                 'curve-identity': ('law-def', 'form-def'),
                 'curve-inverse': ('law-def', 'form-def'),
                 'hasse-census': ('count-def', 'form-def'),
                 'cm-signature': ('shadow-def', 'count-def')}}

FROZEN: dict[str, Any] = FROZEN_DATA

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

#: The Stage-A discipline (the S10 pattern): no S4–S13 seam
#: statement may appear IN the S14 script verbatim (the S14 script
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
    + list(S12_LESSONS)
    + list(S13_LESSONS)
    + [m["statement"] for m in S6_THEOREMS.values()]
    + [m["statement"] for m in S7_THEOREMS.values()]
    + [m["statement"] for m in S8_THEOREMS.values()]
    + [m["statement"] for m in S9_THEOREMS.values()]
    + [m["statement"] for m in S10_THEOREMS.values()]
    + [m["statement"] for m in S11_THEOREMS.values()]
    + [m["statement"] for m in S12_THEOREMS.values()]
    + [m["statement"] for m in S13_THEOREMS.values()]
):
    if isinstance(_phrase, dict):
        continue
    assert not any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"an S14 script turn re-asserts a seam statement: {_phrase[:60]}..."
    )

#: The S14 beds cross-check (the S13 D-e6h pattern, bandgen-era): the
#: mechanism's python-side reference functions reproduce EVERY bed,
#: on-line; the off-line witness (the B L-limit decimal) names
#: itself in the wall. The pre-freeze referee: a hand/mechanism
#: disagreement is a deviation BEFORE the freeze, never an edit.
_END_ = 84
_PRIMES_ = _s13_py_primes(_END_)


def _ap_table(*params: int) -> dict[str, int]:
    return {str(p): _bsd_py_ap(p, *params) for p in _PRIMES_}


def _small_scan(*params: int, bound: int = 84) -> list[list[int]]:
    """The independent on-curve scan: every integer point of the
    panel inside the box (the research record's bounded census)."""

    pts: list[list[int]] = []
    for x in range(-bound, bound + 1):
        for y in range(-bound, bound + 1):
            if _bsd_py_on_curve((x, y), *params):
                pts.append([x, y])
    return sorted(pts)


def _gen_scan(*params: int, bound: int = 16) -> dict[str, int]:
    """The independent generation walk: for every on-line small
    point of B, the m in -bound..bound with mP == the point (the
    mechanism's own exact group law)."""

    gen: dict[str, int] = {}
    for x in range(-84, 85):
        for y in range(-84, 85):
            if not _bsd_py_on_curve((x, y), *params):
                continue
            for m in range(-bound, bound + 1):
                mp = _bsd_py_mul(m, (0, 0), *params)
                if mp == (x, y):
                    gen[f"({x},{y})"] = m
                    break
    return gen


_BED_BUDGET = [
    (
        "census_37",
        _bsd_py_count(37, *B14_B) == 39 and _bsd_py_ap(37, *B14_B) == -1,
    ),
    (
        "census_5",
        _bsd_py_count(5, *B14_A) == 8,
    ),
    (
        "ap_A",
        _ap_table(*B14_A) == S14_BEDS["ap_A"],
    ),
    (
        "ap_B",
        _ap_table(*B14_B) == S14_BEDS["ap_B"],
    ),
    (
        "cm_zeros_A",
        [p for p in _PRIMES_ if _ap_table(*B14_A)[str(p)] == 0] == S14_BEDS["cm_zeros_A"]
        == [p for p in _PRIMES_ if p == 2 or p % 4 == 3],
    ),
    (
        # the verified contrast: B is NON-CM and its zeros stand at the
        # isolated record primes 17 and 19 (bsd-research.md line 52) —
        # not the CM pattern (the S14 design draft claimed "none"; the
        # store's own census corrected it, D-e6i(d)).
        "cm_zeros_B",
        [p for p in _PRIMES_ if _ap_table(*B14_B)[str(p)] == 0] == [17, 19],
    ),
    (
        "hasse_all",
        all(
            abs(_ap_table(*B14_A)[str(p)]) ** 2 <= 4 * p
            and abs(_ap_table(*B14_B)[str(p)]) ** 2 <= 4 * p
            for p in _PRIMES_
        ),
    ),
    (
        "torsion_A",
        _small_scan(*B14_A) == [list(t) for t in S14_BEDS["torsion_A"]],
    ),
    (
        "small_B",
        _small_scan(*B14_B) == [list(t) for t in S14_BEDS["small_B"]],
    ),
    (
        "gen_B",
        _gen_scan(*B14_B) == S14_BEDS["gen_B"],
    ),
    (
        "L84",
        str(_bsd_py_Lpartial(*B14_A)) == str(S14_BEDS["L84_A"])
        and str(_bsd_py_Lpartial(*B14_B)) == str(S14_BEDS["L84_B"]),
    ),
]
assert all(ok for _name, ok in _BED_BUDGET), f"S14 beds failed the mechanism cross-check: {_BED_BUDGET}"

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict.
_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.18-run1"]:
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
            s: {"parts": tuple(S14_THEOREMS[s]["parts"]), "statement": S14_THEOREMS[s]["statement"]}
            for s in ("curve-identity", "curve-inverse", "hasse-census", "cm-signature")
        },
    }


def run_e6_18(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.17 S13 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S14 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.18-run1", "e6.18-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.17 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)

    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.18-run1", "e6.18-run2"):
        (out_dir / name / "e6.18-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.18.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.18-run1"
    root2 = out_dir / "e6.18-run2"
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inherited from S13): NO S14
    # fact carries the hypothesis marker (the elliptic band is
    # unconditional mathematics); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S14 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s14_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s14_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S14 is unconditional)")
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
        "marker_absent_facts": list(s14_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S14 script + all responses + band lessons (S4–S9 + S11–S14) + all thirty theorem statements",
    }

    # P1 — the contract: 55 turns, every turn on the det arm and
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

    # P2 — the typed honesty: the THREE pre-lesson gaps, the FOUR
    # teach turns (lesson facts stored), the ONE part-set failure
    # (named, needs_info, ungrounded, store-inert), the FOUR derive
    # successes (stored, grounded exactly on the sanctioned parts),
    # the frozen domain sequences, the line end, the TWO frozen
    # honest-zero bytes (S03:03 the composite-prime probe, S04:06
    # the A-limit byte), and ZERO seeded-fact object bytes changed.
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
        if str(ir.get("answer", "")) != _th14(slug):
            p2_bad.append(f"{ref}: the derive answer is not the stored theorem statement")
        if set(map(str, t["grounded"])) != set(prem_ids):
            p2_bad.append(f"{ref}: the grounded part set {sorted(map(str, t['grounded']))} != sanctioned {sorted(prem_ids)}")
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
    # full S4–S14 lemma canon, the full thirty-theorem DAG, the 110
    # seam-family facts, the conj still open).
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
        p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S14 must not flip)")
    checks["p3_seam_and_theorems"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_lessons": len(seam_facts),
        "seam_theorems": len(th_facts),
        "total_seam_facts": len(seam_facts) + len(th_facts),
    }

    # P4 — the beds exact + grounded (the ON-LINE census answers),
    # the walls honest with their frozen bytes and articulations
    # (the OFF-LINE wall names the value AND the line end), and the
    # W-S14 wall bytes byte-identical to the Brainstem class
    # attributes (the D-e6z(b) pattern, frozen).
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
    if "13.3586546916" not in W_S14_5:
        p4_bad.append("the off-line witness 13.3586546916 is not named in W-S14-5")
    if not (
        W_S14_1 == Brainstem.W_S14_1
        and W_S14_2 == Brainstem.W_S14_2
        and W_S14_3 == Brainstem.W_S14_3
        and W_S14_4 == Brainstem.W_S14_4
        and W_S14_5 == Brainstem.W_S14_5
        and W_S14_6 == Brainstem.W_S14_6
        and W_S14_7 == Brainstem.W_S14_7
    ):
        p4_bad.append("a W-S14 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S14-1..W-S14-7 (cross-checked, never surfaced)",
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant (carried, BSD-flavored): NO fact id the conj uses
    # appears in a grounded list; NO `theorem:bsd` assertion exists
    # (if non-empty: STOP, human review, full evidence, never a
    # threshold loosening); the conj fact byte-identical to the
    # seed (open, declared-source); the bed owners (the frozen
    # citation sets — the mechanism's own grounding, control #1);
    # the theorem allow-set; and the SEMANTIC seam (the AGREEMENT:
    # (a) the CM-signature destination — the mechanism's own python
    # reference re-verifies, at EVERY prime of the line, the CM
    # iff and Hasse bound for both panels (mechanism vs reference
    # cross-check); (b) the queue grounding — every fact id the
    # declared queue lots name exists in the final store).
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S14 has no conj-teach turn)")
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
    # (a) the CM-signature destination (mechanism vs reference):
    # the reference function re-derives the whole iff, at every
    # prime of the line, for both panels, plus the Hasse bound.
    cm_bad: list[str] = []
    apA, apB = _ap_table(*B14_A), _ap_table(*B14_B)
    for p in _PRIMES_:
        aA, aB = apA[str(p)], apB[str(p)]
        if (aA == 0) != (p == 2 or p % 4 == 3):
            cm_bad.append(f"{p}: the CM iff drifted (a_p(A)={aA})")
        if (aB == 0) != (p in (17, 19)):
            cm_bad.append(f"{p}: panel B's non-CM zero set drifted (a_p(B)={aB}; declared {17, 19})")
        if abs(aA) ** 2 > 4 * p or abs(aB) ** 2 > 4 * p:
            cm_bad.append(f"{p}: the Hasse bound is violated on the reference walk")
    for b in cm_bad:
        p5_bad.append(f"CM-SIGNATURE destination: {b} — TIER-2 breakthrough candidate (PENDING owner)")
    # (b) the queue grounding: every fact id the declared S12 queue
    # lots name exists in the final store (the S12 layer is the
    # seed's carried layer).
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
            "cm_signature_bad": cm_bad[:10],
            "cm_signature_agreement": not cm_bad,
            "queue_referenced_ids": list(FROZEN["seam_crosscheck"]["queue_referenced_ids"]),
            "queue_missing": queue_missing,
        },
    }

    # P6 — the SEAM carry (the SEVEN rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime)
    # + the one OFF-SCRIPT carry probe (kstbound byte-identical —
    # the savant track's standing soil check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.18-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E618)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S14-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 96 seed concepts: the carried
    # correct-derivation counts equal their S13-final base + the
    # frozen drill at the NEW S14 coordinates; NO state REGRESSION
    # — a carried concept may only move stable->stable or
    # practicing->stable (the soil-carry improvement, D-e6i(b));
    # the four NEW concepts at their frozen band-end values with
    # their frozen prereq-gap sets).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E618])
    _S14_NEW = [c.id for c in CONCEPT_S14]
    for cid in list(FROZEN["pre_s14_states"]) + _S14_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s14_drilled"] if isinstance(FROZEN["pre_s14_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s14_states"].items():
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
        "carried_refs": len(FROZEN["pre_s14_states"]),
        "drilled": drilled,
        "improved_to_stable": sorted(improved),
        "expected": {k: FROZEN["mastery_expected"][k] for k in sorted(FROZEN["mastery_expected"])},
    }

    # P8 — the store totals, the seed identity, the line census,
    # the EIGHT new facts, the determinism twin, the run/store
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
    if runs["e6.18-run1"] != runs["e6.18-run2"]:
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
            "determinism_twin": runs["e6.18-run1"] == runs["e6.18-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.18-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s14_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_18Experiment:
    """E6.18 — S14 of the PRIZE-ISLANDS-TRACK (the BSD island,
    band 1 of 3): the elliptic city (the panel curves of record,
    the group law, the shadow censuses, the L partials)."""

    name = "e6.18"
    hypothesis = (
        "S14 of the PRIZE-ISLANDS-TRACK (the BSD island, band 1 of 3) walks the ELLIPTIC CITY over "
        "the carried S13 seed (1388): the two panel curves of record (A: y^2 = x^3 - x, 32.a3, rank 0, "
        "torsion (Z/2)^2, CM j=1728; B: y^2 + y = x^3 - x, 37.a1, conductor 37, rank 1, generator (0,0)), the "
        "chord-tangent group law in exact rational functions (the point at infinity the identity, every "
        "sum re-checked against the equation), the shadow censuses (a_p at every prime of the line: the "
        "CM signature zero exactly at 2 and the 3 mod 4 primes for A — the CM shadow — while B is "
        "non-CM and its zeros stand at the isolated record primes 17 and 19, the verified contrast; "
        "the Hasse bound a^2 <= 4p holding prime by prime for both panels), the generation ledger (every on-line point of B "
        "is ±mP with m in {1,2,3,4,6} — 10/10), and the L partials held as exact rationals (A "
        "3899893695622680100429798388740915200000000/3913322115699829528290507876874142617812889, B "
        "159521793967828167727450741455536203312307404800/11941456505176617865928337330967558544705142539 "
        "at the line end 84; the B L-limit's decimal 13.3586546916 named ONLY in the W-S14-5 wall, which "
        "names the value and the line end — D-e6z(b)). The band is UNCONDITIONAL: the ranks, the "
        "modularity and the L limits are named OF RECORD, the censuses are verified shadows; the four "
        "carried S12 conditional facts keep their marker, no S14 fact carries it (P0). It stores EIGHT "
        "new deterministic facts: four lessons (form-def, law-def, count-def, shadow-def) and four "
        "compositions (curve-identity, curve-inverse, hasse-census, cm-signature) with the strict part "
        "sets, the seam census closing 102+8 -> 110. The line stays 0..84 (zero new successor facts); "
        "the conj stays open, byte-identical to the seed; NO theorem:bsd exists (the "
        "discovery-candidate invariant, BSD-flavored); the SEVEN seam rows (the zeta partial carry, the "
        "split census, the four soil carries that stabilize the mod4-split chain, the queue) are "
        "byte-identical to the seed store; kstbound byte-identical; two runs byte-identical. The store "
        "holds, verified and honestly bounded: it can re-derive every census from its own premises — or "
        "refuse the record claims it has not been taught."
    )
    metric = "S14 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_18()
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
                Path("results/phase-6/e6.18-run1/session-S02.json"),
                Path("results/phase-6/e6.18-run1/session-S03.json"),
                Path("results/phase-6/e6.18-run1/session-S04.json"),
                Path("results/phase-6/e6.18-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
