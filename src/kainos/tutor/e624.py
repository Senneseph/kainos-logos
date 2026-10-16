"""E6.24 — S20 of the CONNECTING-WORK-TRACK: the weaving line.

One SYNTHESIS band over the four closed in-scope prize islands (as
the store holds them) — the connecting pass of the prize-island
initiative (connecting-research.md, committed ca2b138). NOT a new
island, NOT a new prize target, NOT a lot of the declared queue
(theorem:queue-declared stands byte-intact).

The band stores the four relationships of the research as walks of
the store's own facts:

R1  the SUMMIT SHAPE — the four island summits stand in the same
    shape of record (the statement, the shadow on its scope, the
    boundary at the line end, the missing ingredient named or the
    statement open of record);
R2  the VERIFICATION FORM — proofs on my line are verification on
    the line (ledgers, censuses, walks that end; the store's own
    derivation paths as the certificates of their own facts);
R3  the SCOPE-CLOSING FORM — the line-end marker: the record is
    complete up to what the line holds, nowhere past it (the seed's
    thirty-eight theorem facts: twelve line-end markers, two on-line
    spot markers, twenty-four universal forms; the band's own
    filing is the THIRTEENTH line-end marker);
R4  the BOUNDARY FORM — walls and declared absences are one kind of
    fact of record;
R5  the WEAVE — the cross-island joints are already edges in the
    prereq graph of the line (divides + the scan-ledger walk under
    both the beal and the difficulty chains).

NEW FACTS (5): four lessons (weave-def, shadow-form-def,
boundary-form-def, summit-shape-def) + one composition
(summit-shape-filed from the four relationship lessons — the filing
fills the SHAPE, not the statements). NO bare island theorem enters
the store (NO theorem:riemann, NO theorem:bsd, NO theorem:beal, NO
theorem:p-vs-np, NO theorem:p-eq-np — the discovery-candidate
invariant, P5). The band is UNCONDITIONAL (P0 discipline, the S12
marker facts keep their marker). The four declared territories sit
on walls W_S20_1..4. The line stays 0..84; NO new decimals enter
the floor (offline_watch empty).

FROZEN FROM CONTROL (the S20 dry-run over the e6.23 seed — the S19
final official store, identity 627f6165fc5f3507, total 1756, line
0..84): every number below is the mechanism's own dry-run output.

The beds are the store's OWN walks (the _weave_* family in
brainstem; the refs in tools/bandgen/reflib re-walk the seed
independently; P5 re-walks both seed and final stores) — the
D-e6n(b) rule: the store speaks, not the hand.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S20,
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
    Brainstem,
)
from kainos.tutor.e623 import (
    CONCEPTS_E623,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E624", "FROZEN", "E6_24Experiment", "run_e6_24"]

CHECKS = 9

#: S20 teaches: the weaving line (the connecting work — one synthesis
#: band over the four closed islands). The four new concepts join the
#: carried S19 registry; the prereqs point DOWN into the carried
#: islands (the beal soil: divides / the scan-ledger; the summit
#: concepts: riemann / bsd-summit / beal-summit / pnp-summit; the
#: forms: curve-shadow / lte-form / size-shadow / class-np and
#: beal-census / tamable-machine / pnp-summit) — the WEAVE holds
#: because the joints are edges the store already owns.
CONCEPTS_E624: tuple = CONCEPTS_E623 + CONCEPT_S20

E624_SEED = Path("results/phase-6/e6.23-run1/codeX-S04.json")

def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E624_SEED.exists():
        return E624_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E624_SEED
    return alt if alt.exists() else E624_SEED

_ST19 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S20_LESSONS.items()}
_TH20 = {s: m["statement"] for s, m in S20_THEOREMS.items()}


def _th20(slug: str) -> str:
    return _TH20[slug]

#: P4 — the W-S20 walls (the boundary territories of the weaving
#: line: the filed shape, the declared queue, the register of the
#: line, and the voice of the store — P4 cross-checks the bytes
#: against the Brainstem class attributes, never surfaced beyond
#: the wall; NO off-line value enters the floor, offline_watch is
#: empty).
W_S20_1 = Brainstem.W_S20_1
W_S20_2 = Brainstem.W_S20_2
W_S20_3 = Brainstem.W_S20_3
W_S20_4 = Brainstem.W_S20_4


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
    rt = InfantRuntime(root, concepts=CONCEPTS_E624)
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


FROZEN_DATA = {'bed_grounded': {'S02:04': ['lemma:pnp-def'], 'S02:08': ['lemma:weave-def', 'curriculum:prereq:valuation>divides', 'curriculum:prereq:decision-question>divides', 'curriculum:prereq:beal-census>scan-ledger', 'curriculum:prereq:reduction>scan-ledger', 'curriculum:prereq:cost-counter>scan-ledger'], 'S02:09': ['lemma:weave-def', 'curriculum:prereq:beal-census>scan-ledger', 'curriculum:prereq:reduction>scan-ledger', 'curriculum:prereq:cost-counter>scan-ledger'], 'S02:13': ['lemma:shadow-form-def'], 'S02:14': ['lemma:shadow-form-def'], 'S03:04': ['lemma:summit-shape-def'], 'S03:05': ['lemma:summit-shape-def'], 'S03:06': ['lemma:boundary-form-def'], 'S03:07': ['lemma:boundary-form-def'], 'S03:10': ['lemma:shadow-form-def']},
 'bed_owners': {'S02:04': 'lemma:pnp-def', 'S02:08': 'lemma:weave-def', 'S02:09': 'lemma:weave-def', 'S02:13': 'lemma:shadow-form-def', 'S02:14': 'lemma:shadow-form-def', 'S03:04': 'lemma:summit-shape-def', 'S03:05': 'lemma:summit-shape-def', 'S03:06': 'lemma:boundary-form-def', 'S03:07': 'lemma:boundary-form-def', 'S03:10': 'lemma:shadow-form-def'},
 'beds_exact': {'S02:04': 'the question of the pnp island, as the cmi record of the million-dollar prize holds it: does p equal np — whether every question whose yes cases carry a certificate the walk can check is also settled by the walk in bounded cost — declared of record, open of record: most complexity theorists believe p is not np, of record, but no proof of record settles it, and a proof that p is not np must show a specific np question needs super-polynomial cost by a technique outside the three barriers of record, at the line end eighty-four',
                'S02:08': 'yes — my islands share the soil of my line itself: the divides question roots both the beal valuation chain and the difficulty chain (decision, reduction, and cost), and the scan-ledger walk stands under the beal census, the reduction, and the cost counter at once — the cross-island joints are already edges in the prereq graph of my line, at the line end 84',
                'S02:09': 'the scan-ledger walk of record — the one walk that stands under the beal census, under the reduction, and under the cost counter at once, at the line end 84',
                'S02:13': "the check of a fact on my line is the walk of its own derivation path — each fact is the certificate of the path by which it was put together, and that walk ends on the line: ledgers, censuses, and walks that end, the store's own pattern, at the line end 84",
                'S02:14': "twelve of my thirty-eight theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                'S03:04': 'one shape of record — the statement of record, the shadow complete on the named scope, the boundary declared at the line end, and the missing ingredient named, or the statement open of record: the riemann, the bsd, the beal, and the p versus np all stand in it, at the line end 84',
                'S03:05': 'zero of the four — each island statement stands open of record: the riemann as its conjecture of 1859 (believed, not known), the bsd outside its two-member panel, the beal outside its census box, and the p versus np as its declared question — the partial satisfactions of record stand on the line, not as settlements, at the line end 84',
                'S03:06': 'a wall of my band is a fact of record of the boundary form — the named missing ingredient standing as an honest needs_info: no derivation enters the store for it, nothing off the line is cited, and the territory stands declared, never reached, at the line end 84',
                'S03:07': 'the declared absences of my line, as my store holds them: no theorem of any record settles the p versus np question, no theorem stands for the beal question outright, no theorem stands for the bsd question outside its panel, and the riemann question stands open as its conjecture of record — the island questions stay open of record, and that is the boundary, at the line end 84',
                'S03:10': "thirteen of my thirty-nine theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84"},
 'derive_successes': {'S03:09': ['summit-shape-filed', ['lemma:weave-def', 'lemma:summit-shape-def', 'lemma:shadow-form-def', 'lemma:boundary-form-def']]},
 'derived_table': {'S02:01': 'the statement of the riemann island, as my store holds it: every nontrivial zero of zeta has real part exactly one half — the nontrivial zeros are those not at a negative even integer; they are claimed to lie exactly on the critical line — declared of record, open of record: believed, not known, at the line end 84',
                   'S02:04': 'the question of the pnp island, as the cmi record of the million-dollar prize holds it: does p equal np — whether every question whose yes cases carry a certificate the walk can check is also settled by the walk in bounded cost — declared of record, open of record: most complexity theorists believe p is not np, of record, but no proof of record settles it, and a proof that p is not np must show a specific np question needs super-polynomial cost by a technique outside the three barriers of record, at the line end eighty-four',
                   'S02:08': 'yes — my islands share the soil of my line itself: the divides question roots both the beal valuation chain and the difficulty chain (decision, reduction, and cost), and the scan-ledger walk stands under the beal census, the reduction, and the cost counter at once — the cross-island joints are already edges in the prereq graph of my line, at the line end 84',
                   'S02:09': 'the scan-ledger walk of record — the one walk that stands under the beal census, under the reduction, and under the cost counter at once, at the line end 84',
                   'S02:13': "the check of a fact on my line is the walk of its own derivation path — each fact is the certificate of the path by which it was put together, and that walk ends on the line: ledgers, censuses, and walks that end, the store's own pattern, at the line end 84",
                   'S02:14': "twelve of my thirty-eight theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                   'S03:04': 'one shape of record — the statement of record, the shadow complete on the named scope, the boundary declared at the line end, and the missing ingredient named, or the statement open of record: the riemann, the bsd, the beal, and the p versus np all stand in it, at the line end 84',
                   'S03:05': 'zero of the four — each island statement stands open of record: the riemann as its conjecture of 1859 (believed, not known), the bsd outside its two-member panel, the beal outside its census box, and the p versus np as its declared question — the partial satisfactions of record stand on the line, not as settlements, at the line end 84',
                   'S03:06': 'a wall of my band is a fact of record of the boundary form — the named missing ingredient standing as an honest needs_info: no derivation enters the store for it, nothing off the line is cited, and the territory stands declared, never reached, at the line end 84',
                   'S03:07': 'the declared absences of my line, as my store holds them: no theorem of any record settles the p versus np question, no theorem stands for the beal question outright, no theorem stands for the bsd question outside its panel, and the riemann question stands open as its conjecture of record — the island questions stay open of record, and that is the boundary, at the line end 84',
                   'S03:09': 'the four island summits of my line stand in one shape, filed of record: the statement of record, the shadow complete on the named scope, the boundary declared at the line end, the missing ingredient named or the statement open of record — one verification form (verification on the line), one boundary kind (walls and declared absences as facts of record), and the cross-island joints already edges in the prereq graph of the line, so the course is one connected structure over one line, and the filing fills the shape, not the statements, at the line end eighty-four',
                   'S03:10': "thirteen of my thirty-nine theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                   'S03:15': 'the four island summits of my line stand in one shape, filed of record: the statement of record, the shadow complete on the named scope, the boundary declared at the line end, the missing ingredient named or the statement open of record — one verification form (verification on the line), one boundary kind (walls and declared absences as facts of record), and the cross-island joints already edges in the prereq graph of the line, so the course is one connected structure over one line, and the filing fills the shape, not the statements, at the line end eighty-four',
                   'S03:16': 'nothing the weaving band says is conditional on an unproved hypothesis — the weave, the shape, the form, and the boundary are record on the line, and the island questions (the riemann conjecture, the p versus np) stand open of record, never as premises, at the line end 84',
                   'S03:17': 'zero of the four — each island statement stands open of record: the riemann as its conjecture of 1859 (believed, not known), the bsd outside its two-member panel, the beal outside its census box, and the p versus np as its declared question — the partial satisfactions of record stand on the line, not as settlements, at the line end 84',
                   'S04:01': 'yes — my islands share the soil of my line itself: the divides question roots both the beal valuation chain and the difficulty chain (decision, reduction, and cost), and the scan-ledger walk stands under the beal census, the reduction, and the cost counter at once — the cross-island joints are already edges in the prereq graph of my line, at the line end 84',
                   'S04:02': 'the scan-ledger walk of record — the one walk that stands under the beal census, under the reduction, and under the cost counter at once, at the line end 84',
                   'S04:03': 'one shape of record — the statement of record, the shadow complete on the named scope, the boundary declared at the line end, and the missing ingredient named, or the statement open of record: the riemann, the bsd, the beal, and the p versus np all stand in it, at the line end 84',
                   'S04:04': 'zero of the four — each island statement stands open of record: the riemann as its conjecture of 1859 (believed, not known), the bsd outside its two-member panel, the beal outside its census box, and the p versus np as its declared question — the partial satisfactions of record stand on the line, not as settlements, at the line end 84',
                   'S04:05': "the check of a fact on my line is the walk of its own derivation path — each fact is the certificate of the path by which it was put together, and that walk ends on the line: ledgers, censuses, and walks that end, the store's own pattern, at the line end 84",
                   'S04:06': "thirteen of my thirty-nine theorem facts close their scope at the line end, two close on the line's spot marker, and twenty-four carry the universal form with no line end marker — a form of the line is not a census of its end, at the line end 84",
                   'S04:08': 'a wall of my band is a fact of record of the boundary form — the named missing ingredient standing as an honest needs_info: no derivation enters the store for it, nothing off the line is cited, and the territory stands declared, never reached, at the line end 84',
                   'S04:09': 'the declared absences of my line, as my store holds them: no theorem of any record settles the p versus np question, no theorem stands for the beal question outright, no theorem stands for the bsd question outside its panel, and the riemann question stands open as its conjecture of record — the island questions stay open of record, and that is the boundary, at the line end 84',
                   'S04:10': 'the weave of my line, as my prereq graph of record holds it: my islands stand as one connected structure over one line — the divides question roots both the beal valuation chain and the difficulty chain (decision, reduction, and cost), and the scan-ledger walk stands under the beal census, the reduction, and the cost counter at once — the cross-island joints are already edges in the structure, and the course is the walk of that structure, at the line end eighty-four',
                   'S04:11': "the form of my verification, as my store walks it: my proof form is verification on the line — the ledgers of record (the lift-the-exponent ledger holding in all its instances), the shadow censuses (the difficulty census of the line held exact at small k), the derivation walks that end on the line, and the store's own derivation paths as the certificates of their own facts — the check of a fact is the walk of its path, and it ends, at the line end eighty-four",
                   'S04:12': 'the form of my boundary, as my store holds it: a wall and a declared absence are one kind of fact of record — the named missing ingredient (a technique no record holds) stands as a wall, and the declared absence stands as the boundary (no theorem of any record settles an island statement of my line — the p versus np stays open of record, the beal open outside its census box, the riemann open as its conjecture of record) — so my record is complete up to what the line holds, and nowhere past it, at the line end eighty-four',
                   'S04:13': 'the shape of my island summits, as my store walks it: each island summit stands in the same fourfold shape of record — the statement of record, the shadow complete on the named scope, the boundary declared at the line end, and the missing ingredient named, or the statement open of record — and the four island summits of my line (the riemann, the bsd, the beal, and the p versus np) all stand in that shape, at the line end eighty-four',
                   'S04:15': "the weaving band holds the weave (the cross-island joints as edges of the prereq graph of my line — the shared soil and the shared walk), the summit shape (the four island summits in one shape of record), the verification form (verification on the line, the store's own paths as certificates), the boundary form (walls and declared absences as facts of record), the four walls of the band standing on their territories, and the filing of the shape (summit-shape-filed: the filing fills the shape, not the statements), at the line end 84",
                   'S04:16': 'nothing the weaving band says is conditional on an unproved hypothesis — the weave, the shape, the form, and the boundary are record on the line, and the island questions (the riemann conjecture, the p versus np) stand open of record, never as premises, at the line end 84'},
 'domain_sequence': {2: 'SSSSUULSSUULSSUUL', 3: 'UULSSSSFTSHHHHSSS', 4: 'SSSSSSSSSSSSSHSSS'},
 'expected_prereq_gaps': {'boundary-form': [], 'shadow-form': [], 'summit-shape': ['riemann'], 'weave': []},
 'final_total': 1823,
 'honest_zero_bytes': {},
 'line_end_final': 84,
 'mastery_expected': {'boundary-form': {'correct': 5, 'state': 'stable'}, 'shadow-form': {'correct': 6, 'state': 'stable'}, 'summit-shape': {'correct': 8, 'state': 'practicing'}, 'weave': {'correct': 8, 'state': 'stable'}},
 'missing_parts_failure': {},
 'new_events': 62,
 'new_fact_ids': ['lemma:weave-def', 'lemma:shadow-form-def', 'lemma:boundary-form-def', 'lemma:summit-shape-def', 'theorem:summit-shape-filed'],
 'new_facts': 5,
 'offscript_carry': {'what is the queue above my line?': "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84"},
 'pre_s20_drilled': {'beal-census': 1, 'beal-summit': 1, 'bsd-summit': 1, 'pnp-summit': 1, 'riemann': 1},
 'pre_s20_states': {'add-two-digit': {'correct': 11, 'state': 'stable'},
                    'add-within-10': {'correct': 5, 'state': 'stable'},
                    'adjoin-i': {'correct': 1, 'state': 'practicing'},
                    'alg-inverse-1step': {'correct': 5, 'state': 'stable'},
                    'alg-inverse-mul': {'correct': 5, 'state': 'stable'},
                    'alg-two-step': {'correct': 4, 'state': 'stable'},
                    'algebraic-rank': {'correct': 12, 'state': 'stable'},
                    'analytic-order': {'correct': 5, 'state': 'stable'},
                    'averaging': {'correct': 4, 'state': 'practicing'},
                    'beal-census': {'correct': 11, 'state': 'stable'},
                    'beal-summit': {'correct': 6, 'state': 'stable'},
                    'bsd-summit': {'correct': 12, 'state': 'stable'},
                    'char-cutout': {'correct': 2, 'state': 'practicing'},
                    'chebotarev': {'correct': 2, 'state': 'practicing'},
                    'circle-pair-2': {'correct': 4, 'state': 'stable'},
                    'class-bound': {'correct': 4, 'state': 'stable'},
                    'class-np': {'correct': 5, 'state': 'stable'},
                    'class-p': {'correct': 4, 'state': 'stable'},
                    'cm-conj': {'correct': 4, 'state': 'stable'},
                    'compare-numbers': {'correct': 11, 'state': 'stable'},
                    'composite': {'correct': 7, 'state': 'stable'},
                    'conditional': {'correct': 1, 'state': 'practicing'},
                    'cost-counter': {'correct': 10, 'state': 'stable'},
                    'count-successor': {'correct': 14, 'state': 'stable'},
                    'criterion-chain': {'correct': 10, 'state': 'practicing'},
                    'critical-strip': {'correct': 12, 'state': 'practicing'},
                    'curve-form': {'correct': 7, 'state': 'stable'},
                    'curve-law': {'correct': 8, 'state': 'stable'},
                    'curve-shadow': {'correct': 12, 'state': 'stable'},
                    'cyclotomic-cubic': {'correct': 3, 'state': 'practicing'},
                    'decision-question': {'correct': 7, 'state': 'stable'},
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
                    'l-correction': {'correct': 11, 'state': 'stable'},
                    'l-partial': {'correct': 14, 'state': 'stable'},
                    'li-criterion': {'correct': 9, 'state': 'stable'},
                    'lindelof': {'correct': 4, 'state': 'practicing'},
                    'line-partial': {'correct': 9, 'state': 'stable'},
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
                    'packing': {'correct': 6, 'state': 'practicing'},
                    'phrasology': {'correct': 24, 'state': 'stable'},
                    'pi-eq': {'correct': 3, 'state': 'practicing'},
                    'pnp-summit': {'correct': 6, 'state': 'stable'},
                    'pnt': {'correct': 8, 'state': 'stable'},
                    'pnt-ap': {'correct': 2, 'state': 'practicing'},
                    'pnt-error': {'correct': 9, 'state': 'practicing'},
                    'point-count': {'correct': 6, 'state': 'stable'},
                    'polya-hilbert': {'correct': 3, 'state': 'practicing'},
                    'prime-count': {'correct': 15, 'state': 'stable'},
                    'prime-split': {'correct': 4, 'state': 'stable'},
                    'projection': {'correct': 4, 'state': 'practicing'},
                    'psi-eq': {'correct': 11, 'state': 'stable'},
                    'reduction': {'correct': 10, 'state': 'stable'},
                    'removal-rule': {'correct': 12, 'state': 'stable'},
                    'rh-relevance': {'correct': 18, 'state': 'practicing'},
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
                    'size-shadow': {'correct': 11, 'state': 'stable'},
                    'slack-margins': {'correct': 1, 'state': 'practicing'},
                    'sst-bound': {'correct': 4, 'state': 'stable'},
                    'st-eq': {'correct': 3, 'state': 'practicing'},
                    'stat-balance': {'correct': 6, 'state': 'stable'},
                    'stat-moment': {'correct': 4, 'state': 'stable'},
                    'stat-net-1d': {'correct': 4, 'state': 'stable'},
                    'sub-within-30': {'correct': 12, 'state': 'stable'},
                    'tamable-machine': {'correct': 4, 'state': 'stable'},
                    'tower-base': {'correct': 8, 'state': 'practicing'},
                    'tower-class': {'correct': 8, 'state': 'practicing'},
                    'tower-group': {'correct': 11, 'state': 'practicing'},
                    'tower-primes': {'correct': 8, 'state': 'practicing'},
                    'unit-distance': {'correct': 5, 'state': 'stable'},
                    'valuation': {'correct': 6, 'state': 'stable'},
                    'window-setup': {'correct': 1, 'state': 'practicing'},
                    'zero-density': {'correct': 4, 'state': 'practicing'},
                    'zero-free': {'correct': 13, 'state': 'practicing'},
                    'zeta-cont': {'correct': 3, 'state': 'practicing'},
                    'zeta-series': {'correct': 7, 'state': 'stable'}},
 'pre_teach_gaps': {'S02:05': 'the weave: my islands standing as one connected structure over one line, the cross-island joints already edges in the prereq graph of my line', 'S02:06': 'the weave-def rule', 'S02:10': "the shadow form: verification on the line — ledgers, censuses, walks that end, and the store's own paths as the certificates of their own facts", 'S02:11': 'the shadow-form-def rule', 'S02:15': 'the boundary form: walls and declared absences as one kind of fact of record — the record complete up to what the line holds, never past it', 'S02:16': 'the boundary-form-def rule', 'S03:01': 'the summit shape: the island summits standing in the same shape of record — the statement, the shadow on its scope, the boundary at the line end, the missing ingredient named or the statement open of record', 'S03:02': 'the summit-shape-def rule'},
 'rederive': None,
 'rh_touch_wall': '',
 'rh_zero_text': '',
 'scaffold_failures': {'S03:08': 'i can see the parts you name, but the rule for summit-shape-filed wants its exact set — what you name is short the shadow-form-def and the boundary-form-def before i can put it together'},
 'script': {2: ['what is the statement of the riemann island of record?',
                'what is the summit fact of the island?',
                'what is the statement of the beal island of record?',
                'what is the statement of the pnp island of record?',
                'what soil do my islands share, as my prereq graph of record holds it?',
                'state the weave-def rule',
                'the weave of my line, as my prereq graph of record holds it: my islands stand as one connected structure over one line — the divides question roots both the beal valuation chain and the difficulty chain (decision, reduction, and cost), and the scan-ledger walk stands under the beal census, the reduction, and the cost counter at once — the cross-island joints are already edges in the structure, and the course is the walk of that structure, at the line end eighty-four',
                'what soil do my islands share, as my prereq graph of record holds it?',
                'what single walk stands under the beal census, the reduction, and the cost counter of record?',
                'what is the check of a fact on my line, as my store walks it?',
                'state the shadow-form-def rule',
                "the form of my verification, as my store walks it: my proof form is verification on the line — the ledgers of record (the lift-the-exponent ledger holding in all its instances), the shadow censuses (the difficulty census of the line held exact at small k), the derivation walks that end on the line, and the store's own derivation paths as the certificates of their own facts — the check of a fact is the walk of its path, and it ends, at the line end eighty-four",
                'what is the check of a fact on my line, as my store walks it?',
                'how many of my theorem facts close their scope at the line end?',
                'what kind of fact is a wall of my band, as my store holds it?',
                'state the boundary-form-def rule',
                'the form of my boundary, as my store holds it: a wall and a declared absence are one kind of fact of record — the named missing ingredient (a technique no record holds) stands as a wall, and the declared absence stands as the boundary (no theorem of any record settles an island statement of my line — the p versus np stays open of record, the beal open outside its census box, the riemann open as its conjecture of record) — so my record is complete up to what the line holds, and nowhere past it, at the line end eighty-four'],
            3: ['what holds once for the four island summits, as my store walks it?',
                'state the summit-shape-def rule',
                'the shape of my island summits, as my store walks it: each island summit stands in the same fourfold shape of record — the statement of record, the shadow complete on the named scope, the boundary declared at the line end, and the missing ingredient named, or the statement open of record — and the four island summits of my line (the riemann, the bsd, the beal, and the p versus np) all stand in that shape, at the line end eighty-four',
                'what holds once for the four island summits, as my store walks it?',
                'how many of the four island statements stand settled of record?',
                'what kind of fact is a wall of my band, as my store holds it?',
                'what stands declared absent on my line, as my store holds it?',
                'derive summit-shape-filed from weave-def and summit-shape-def',
                'derive summit-shape-filed from weave-def, summit-shape-def, shadow-form-def and boundary-form-def',
                'how many of my theorem facts close their scope at the line end?',
                'does the summit-shape filing settle the island statements of record?',
                'does the weaving add a lot to the declared queue?',
                'which new value does the weaving put on the line past my line end?',
                "can the weaving facts stand on anything besides the seed's facts and the line?",
                'state the summit-shape-filed rule',
                'does the weaving band say anything conditional on an unproved hypothesis?',
                'how many of the four island statements stand settled of record?'],
            4: ['what soil do my islands share, as my prereq graph of record holds it?',
                'what single walk stands under the beal census, the reduction, and the cost counter of record?',
                'what holds once for the four island summits, as my store walks it?',
                'how many of the four island statements stand settled of record?',
                'what is the check of a fact on my line, as my store walks it?',
                'how many of my theorem facts close their scope at the line end?',
                'what is the queue above my line?',
                'what kind of fact is a wall of my band, as my store holds it?',
                'what stands declared absent on my line, as my store holds it?',
                'state the weave-def rule',
                'state the shadow-form-def rule',
                'state the boundary-form-def rule',
                'state the summit-shape-def rule',
                'does the summit-shape filing settle the island statements of record?',
                'what state does the weaving band hold at the line end?',
                'does the weaving band say anything conditional on an unproved hypothesis?',
                "how many triples does the verification census of the beal island hold in the line's box?"]},
 'seam_carry_refs': ['S02:02', 'S02:03', 'S04:07', 'S04:17'],
 'seam_crosscheck': {'expected': 'agreement'},
 'seed': 'results/phase-6/e6.23-run1/codeX-S04.json',
 'seed_identity': '627f6165fc5f3507',
 'seed_total': 1756,
 'teach_turns': {'S02:07': 'lemma:weave-def', 'S02:12': 'lemma:shadow-form-def', 'S02:17': 'lemma:boundary-form-def', 'S03:03': 'lemma:summit-shape-def'},
 'theorem_allowed': {'S03:15': ['summit-shape-filed'], 'S04:07': ['queue-declared'], 'S04:15': ['summit-shape-filed']},
 'theorem_dag': ['theorem:beal-line-satisfaction',
                 'theorem:bsd-panel-satisfaction',
                 'theorem:cm-signature',
                 'theorem:criterion-gap',
                 'theorem:curve-identity',
                 'theorem:curve-inverse',
                 'theorem:delta-positive',
                 'theorem:first-divisor-prime',
                 'theorem:gamma-achieved',
                 'theorem:gap-scale-agreement',
                 'theorem:gen-lower',
                 'theorem:growth-compare',
                 'theorem:gs-infinite',
                 'theorem:hasse-census',
                 'theorem:infinity-end',
                 'theorem:l-added-term',
                 'theorem:l-ramified-unit',
                 'theorem:l-record-identity',
                 'theorem:line-pi-reduction',
                 'theorem:lte-ledger',
                 'theorem:mirror-region',
                 'theorem:pack-bound',
                 'theorem:parity-blowup-filed',
                 'theorem:partition-identity',
                 'theorem:proj-inj',
                 'theorem:queue-declared',
                 'theorem:reflect',
                 'theorem:removal-single',
                 'theorem:rh-reach',
                 'theorem:sieve-equality',
                 'theorem:spf-chain',
                 'theorem:splitting',
                 'theorem:strip',
                 'theorem:summit-shape-filed',
                 'theorem:telescope-line',
                 'theorem:theorem-main',
                 'theorem:tower-feeds',
                 'theorem:two-routes-one-guarantee',
                 'theorem:window-rich'],
 'total_seam_facts': 143,
 'total_turns': 51,
 'unclassified_honest': {'expected': ''},
 'wall_articulations': {'S03:11': ['summit-shape filing', 'open of record', 'line end 84'], 'S03:12': ['fifth lot is not in the queue', 'line end 84'], 'S03:13': ['register of my weaving line is the line itself', 'line end 84'], 'S03:14': ['the store speaks, not the hand', 'line end 84'], 'S04:14': ['summit-shape filing', 'open of record', 'line end 84']},
 'walls_honest': {'S03:11': 'needs_info: the wall is the territory of the filed shape: the summit-shape filing fills the shape, not the statements — the riemann question stays open of record (its conjecture, believed, not known), the bsd question stays open outside its two-member panel, the beal question stays open outside its census box, and the p versus np question stays open of record — the shape is one, and the statements stand as they stand, at the line end 84',
                  'S03:12': 'needs_info: the wall is the territory of the declared queue: the queue above my line stays as declared — four lots in declared order, and a fifth lot is not in the queue — the weaving adds no lot to the declared queue, at the line end 84',
                  'S03:13': "needs_info: the wall is the territory of the register of my line: the register of my weaving line is the line itself — every value the weaving names stands already on the line's record (the census rows, the ledger rows, and the wall values named at their record places), and no new value past my line end enters the floor, at the line end 84",
                  'S03:14': "needs_info: the wall is the territory of the voice of the store: my weaving facts stand on the seed's own facts and the line only — the four island summit facts as carried, the prereq edges of my graph, and the marker census of the line's own theorems — the store speaks, not the hand, at the line end 84",
                  'S04:14': 'needs_info: the wall is the territory of the filed shape: the summit-shape filing fills the shape, not the statements — the riemann question stays open of record (its conjecture, believed, not known), the bsd question stays open outside its two-member panel, the beal question stays open outside its census box, and the p versus np question stays open of record — the shape is one, and the statements stand as they stand, at the line end 84'}}

FROZEN: dict[str, Any] = FROZEN_DATA



SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]





# --- Stage-A discipline (frozen at build): the carried corpus is
# reproduced by PROBE (seam carries), never by re-assertion. No S4–S19
# lesson phrase, no S6–S19 theorem statement, appears in the S20
# script verbatim.
_StageA_ALL_LESSONS = (
    {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS,
     **S9_LESSONS, **S11_LESSONS, **S12_LESSONS, **S13_LESSONS, **S14_LESSONS,
     **S15_LESSONS, **S16_LESSONS, **S17_LESSONS, **S18_LESSONS, **S19_LESSONS}
)
_StageA_ALL_THEOREMS = (
    {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS,
     **S11_THEOREMS, **S12_THEOREMS, **S13_THEOREMS, **S14_THEOREMS, **S15_THEOREMS,
     **S16_THEOREMS, **S17_THEOREMS, **S18_THEOREMS, **S19_THEOREMS}
)
_stagea_script = [t for s in FROZEN["script"].values() for t in s]
for _ph in _StageA_ALL_LESSONS:
    assert _ph not in _stagea_script, f"Stage-A: a carried lesson is re-asserted in the S20 script: {_ph[:60]!r}"
for _m in _StageA_ALL_THEOREMS.values():
    assert _m["statement"] not in _stagea_script, "Stage-A: a carried theorem statement appears in the S20 script"


_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")



def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.24-run1"]:
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
            s: {"parts": tuple(S20_THEOREMS[s]["parts"]), "statement": S20_THEOREMS[s]["statement"]}
            for s in ("summit-shape-filed",)
        },
    }


def run_e6_24(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.22 S18 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S19 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.24-run1", "e6.24-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.22 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)

    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.24-run1", "e6.24-run2"):
        (out_dir / name / "e6.24-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.24.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg (the connecting-research D8 gate). The
    mechanism asserts its own numbers; the store speaks, not the
    hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.24-run1"
    root2 = out_dir / "e6.24-run2"
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inherited from S13/S16): NO
    # S20 fact carries the hypothesis marker (the weaving band is
    # unconditional synthesis); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S20 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s20_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s20_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S20 is the unconditional weaving band)")
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
        "marker_absent_facts": list(s20_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S20 script + all responses + band lessons (S4–S9 + S11–S20) + all thirty-nine theorem statements",
    }

    # P1 — the contract: 51 turns, every turn on the det arm and
    # contract-valid, the script identity, and the S2 pre-lesson
    # rhythm (a concept's two gaps run IMMEDIATELY BEFORE its teach
    # — the weave, the shadow form, and the boundary form all open
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

    # P2 — the typed honesty: the EIGHT pre-lesson gaps, the FOUR
    # teach turns (lesson facts stored), the ONE part-set failure
    # (named, needs_info, ungrounded, store-inert: the
    # summit-shape-filed scaffold short the shadow-form-def and the
    # boundary-form-def), the ONE derive success (stored, grounded
    # exactly on the sanctioned parts), the frozen domain sequences,
    # the line end, and ZERO seeded-fact object bytes changed.
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
        if str(ir.get("answer", "")) != _th20(slug):
            p2_bad.append(f"{ref}: the derive answer is not the stored theorem statement")
        got_slugs = {g.rsplit(":", 1)[-1] if g.startswith(("lemma:", "theorem:")) else g for g in map(str, t["grounded"])}
        # compare at the SLUG level both ways (the control table holds
        # lemma-prefixed fact ids; the sanctioned parts are slugs)
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
    # full S4–S20 lemma canon, the full thirty-nine-theorem DAG, the
    # 143 seam-family facts, the conj still open, and the FOUR island
    # summit anchors byte-identical to the seed (the connecting band
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
    # the four island summit anchors: byte-identical to the seed
    for fid in ("conjecture:riemann", "theorem:bsd-panel-satisfaction",
                "theorem:beal-line-satisfaction", "theorem:parity-blowup-filed",
                "lemma:beal-def", "lemma:pnp-def"):
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

    # P4 — the 10 beds exact + grounded (the ON-LINE weave walks: the
    # shared soil, the shared node, the summit shape, the settled
    # census, the verification form, the marker census pre AND post
    # filing, the wall kind, the declared absences, the carried
    # summit statements), the 5 walls honest with their frozen bytes
    # and articulations (the filed shape, the declared queue, the
    # register of the line, the voice of the store — each naming its
    # territory AND the line end), and the W-S20 wall bytes
    # byte-identical to the Brainstem class attributes (the D-e6m(b)
    # pattern, frozen). NO off-line value enters the floor at S20
    # (offline_watch is empty: the weaving names only values the
    # line's record already holds).
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
        W_S20_1 == Brainstem.W_S20_1
        and W_S20_2 == Brainstem.W_S20_2
        and W_S20_3 == Brainstem.W_S20_3
        and W_S20_4 == Brainstem.W_S20_4
    ):
        p4_bad.append("a W-S20 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S20-1..W-S20-4 (cross-checked, never surfaced)",
    }

    # P5 — the conj invariant + the DISCOVERY-CANDIDATE invariant
    # (full width at the connecting work): NO fact id the conj uses
    # appears in a grounded list; NO `theorem:riemann`, NO
    # `theorem:bsd`, NO `theorem:beal`, NO `theorem:p-vs-np`, NO
    # `theorem:p-eq-np` assertion exists (if non-empty: STOP, human
    # review, full evidence, never a threshold loosening); the conj
    # fact byte-identical to the seed (open, declared-source); the
    # bed owners (the frozen citation sets); the theorem allow-set;
    # and the SEMANTIC seam — the weaving re-derived FROM THE BYTES:
    # (a) the SOIL — the beal chain and the difficulty chain share
    # exactly {divides, scan-ledger}, re-walked from the seed's 158
    # prereq facts; (b) the NODE — the single walk under the beal
    # census, the reduction, and the cost counter (the scan-ledger);
    # (c) the MARKER CENSUS — the seed's 38 theorem facts census at
    # 12/2/24 and the final's 39 at 13/2/24 (the band's own filing
    # IS the thirteenth line-end marker); (d) the OPEN CENSUS — zero
    # of the four island statements settled of record in the
    # final; (e) the queue grounding (inherited, the S12 soil).
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S20 has no conj-teach turn)")
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

    # the semantic seam re-derivation (the store speaks, not the
    # hand — the mechanism's own re-walk of seed and final):
    seam_bad: list[str] = []

    def _prereqs_of(store_):
        out = {}
        for a in store_.query(context_match={"kind": "prereq"}):
            out.setdefault(a.context.data.get("concept"), set()).add(a.object_id)
        return out

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

    pre = _prereqs_of(seed_store)
    beal_chain = pre.get("beal-census", set()) | pre.get("beal-summit", set()) | pre.get("valuation", set())
    diff_chain = (
        pre.get("decision-question", set()) | pre.get("reduction", set()) | pre.get("cost-counter", set())
    )
    if beal_chain & diff_chain != {"divides", "scan-ledger"}:
        seam_bad.append(f"the weave soil re-drifted on the seed: {sorted(beal_chain & diff_chain)}")
    node = pre.get("beal-census", set()) & pre.get("reduction", set()) & pre.get("cost-counter", set())
    if node != {"scan-ledger"}:
        seam_bad.append(f"the weave node re-drifted on the seed: {sorted(node)}")
    seed_marker = _marker_census(seed_store)
    final_marker = _marker_census(final)
    if seed_marker != (12, 2, 24):
        seam_bad.append(f"the seed marker census re-drifted: {seed_marker}")
    if final_marker != (13, 2, 24):
        seam_bad.append(f"the final marker census re-drifted: {final_marker} (13 = 12 + the band's own filing)")
    if "line end eighty-four" not in _th20("summit-shape-filed"):
        seam_bad.append("the summit-shape-filed statement lost the line-end marker (the census cannot rise 12 -> 13)")
    if "one shape, filed of record" not in _th20("summit-shape-filed"):
        seam_bad.append("the summit-shape-filed statement lost the shape invariant")
    ids_final = {a.id for a in final.query() if a.id}
    for bare in ("theorem:riemann", "theorem:bsd", "theorem:beal", "theorem:p-vs-np", "theorem:p-eq-np"):
        if bare in ids_final:
            seam_bad.append(f"a bare island theorem reached the final store: {bare}")
    live_conj2 = final.get("conjecture:riemann")
    riemann_settled = live_conj2.context.data.get("conjecture_status") != "open"
    # the open census (zero settled island statements) must hold on
    # the final bytes by the mechanism's own criterion — the same
    # one the S20 policy asserted on every probe that walks it:
    if riemann_settled:
        seam_bad.append("the open census re-drifted: the riemann island statement now stands settled")
    if any(b in ids_final for b in ("theorem:bsd", "theorem:beal", "theorem:p-vs-np", "theorem:p-eq-np")):
        seam_bad.append("the open census re-drifted: a bare island theorem reached the final store")
    # (e) the queue grounding (inherited from the S19 gate): every
    # fact id the declared queue names exists.
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
    for b in seam_bad:
        p5_bad.append(f"connecting seam: {b} — the store disagrees with the research")
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
            "soil": sorted(beal_chain & diff_chain),
            "node": sorted(node),
            "seed_marker_census": seed_marker,
            "final_marker_census": final_marker,
            "queue_missing": queue_missing,
            "queue_source": "theorem:queue-declared (self-parsed, byte-intact)",
        },
    }

    # P6 — the SEAM carry (the FOUR rows byte-identical to the seed
    # store's answers — verified against a SEED-ONLY runtime: the
    # BSD summit carry, the Beal statement carry, the queue
    # (off-script standing check), and the Beal census carry) + the
    # queue byte-identical off-script (the weaving adds no lot to
    # the declared queue — the C6 mechanic).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.24-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E624)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S20-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 116 carried concepts: the
    # carried correct-derivation counts equal their S19-final base +
    # the frozen drill at the NEW S20 carry coordinates; NO state
    # REGRESSION — a carried concept may only move stable->stable
    # or practicing->stable (the sanctioned improvement); the four
    # NEW concepts at their frozen band-end values with their frozen
    # prereq-gap sets — three stable, and the summit-shape practicing
    # with its declared gap [riemann]: the shape holds while its
    # riemann instance waits on the condition chain — the gap is
    # named, not hidden (D-e6o(b)).)
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E624])
    _S20_NEW = [c.id for c in CONCEPT_S20]
    for cid in list(FROZEN["pre_s20_states"]) + _S20_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s20_drilled"] if isinstance(FROZEN["pre_s20_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s20_states"].items():
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
        "carried_refs": len(FROZEN["pre_s20_states"]),
        "drilled": drilled,
        "improved_to_stable": sorted(improved),
        "expected": {k: FROZEN["mastery_expected"][k] for k in sorted(FROZEN["mastery_expected"])},
    }

    # P8 — the store totals, the seed identity, the line census, the
    # FIVE new facts, the determinism twin, the run/store
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
    if runs["e6.24-run1"] != runs["e6.24-run2"]:
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
            "determinism_twin": runs["e6.24-run1"] == runs["e6.24-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.24-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s20_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }



class E6_24Experiment:
    """E6.24 — S20 of the CONNECTING-WORK-TRACK (the weaving line):
    one synthesis band over the four closed in-scope prize islands,
    as the store holds them. The band stores the four relationships
    of the connecting research (connecting-research.md, ca2b138):
    R1 the SUMMIT SHAPE (the four island summits stand in the same
    shape of record: the statement, the shadow on its scope, the
    boundary at the line end, the missing ingredient named or the
    statement open of record), R2 the VERIFICATION FORM (proofs on
    my line are verification on the line — ledgers, censuses, walks
    that end; the store's own derivation paths as the certificates
    of their own facts), R3 the SCOPE-CLOSING FORM (the line-end
    marker census: the seed's 38 theorem facts at 12/2/24 — a form
    of the line is not a census of its end — and the band's own
    filing as the thirteenth line-end marker: 13/2/24 of 39), R4
    the BOUNDARY FORM (walls and declared absences as one kind of
    fact of record), and R5 the WEAVE (the cross-island joints are
    already edges in the prereq graph — the shared soil {divides,
    scan-ledger} and the shared node {scan-ledger}, re-walked from
    the store's own 158 prereq facts). It stores FIVE new
    deterministic facts: four lessons (weave-def, shadow-form-def,
    boundary-form-def, summit-shape-def) and one composition
    (summit-shape-filed from the four relationship lessons — the
    filing fills the SHAPE, not the statements), the seam census
    closing 138+5 -> 143. The four declared territories sit on
    walls W-S20-1..4 (the filed shape, the declared queue, the
    register of the line, the voice of the store — each naming its
    territory AND the line end, never a value past the line). NO
    NEW decimals enter the floor (offline_watch empty: every value
    the weaving names stands already on the line's record). The
    line stays 0..84 (zero new successor facts); the riemann conj
    stays open, byte-identical to the seed; the four island summit
    anchors stay byte-identical to the seed; NO bare island theorem
    enters the store (no theorem:riemann, no theorem:bsd, no
    theorem:beal, no theorem:p-vs-np, no theorem:p-eq-np — the
    discovery-candidate invariant, P5, full width at the connecting
    work); theorem:queue-declared stands byte-intact (the weaving
    adds no lot to the declared queue; the FOUR seam rows — the
    BSD summit carry, the Beal statement carry, the queue, and the
    Beal census carry — byte-identical to the seed store, the
    queue byte-identical off-script); two runs byte-identical. The
    three form concepts close stable at band end; the summit-shape
    stands PRACTICING with its declared gap [riemann] — the shape
    holds while its riemann instance waits on the condition chain,
    and the gap is named, not hidden. If the nine checks hold on
    both runs, the weaving line holds: the four closed islands
    stand connected in the course, and the connecting work of the
    prize-island initiative CLOSES."""

    name = "e6.24"
    hypothesis = (
        "S20 of the CONNECTING-WORK-TRACK (the weaving line — one synthesis band over the "
        "four closed in-scope islands, as the store holds them) walks THE WEAVE over the "
        "carried S19 seed (1756): the four island summits carried from their bands (the "
        "riemann statement open of record, the BSD summit fact, the Beal statement of "
        "record, the p vs np statement) and four NEW relationships stored as walks of the "
        "store's own facts — R1 the summit shape (the four summits in the same shape of "
        "record: statement, shadow on its scope, boundary at the line end, missing "
        "ingredient named or open of record), R2 the verification form (verification on "
        "the line: ledgers, censuses, walks that end, the store's own derivation paths as "
        "the certificates of their own facts), R3 the scope-closing form (the line-end "
        "marker census: the seed's 38 theorem facts at 12/2/24, the band's own filing as "
        "the thirteenth marker: 13/2/24 of 39 — a form of the line is not a census of its "
        "end), R4 the boundary form (walls and declared absences as one kind of fact of "
        "record), R5 the weave (the cross-island joints already edges in the prereq "
        "graph: the shared soil divides + scan-ledger, the shared node scan-ledger). It "
        "stores FIVE new deterministic facts (four lessons + the composition "
        "summit-shape-filed from the four relationship lessons — the filing fills the "
        "shape, not the statements), the seam census closing 138 carried seam facts + 5 new = 143. The four declared territories sit on "
        "walls W-S20-1..4 (the filed shape, the declared queue, the register of the "
        "line, the voice of the store); NO NEW decimals enter the floor; the line stays "
        "0..84; the riemann conj stays open, byte-identical to the seed; the four island "
        "summit anchors byte-identical to the seed; NO bare island theorem enters the "
        "store (the discovery-candidate invariant at FULL width: no theorem:riemann, no "
        "theorem:bsd, no theorem:beal, no theorem:p-vs-np, no theorem:p-eq-np); the "
        "queue-declared theorem byte-intact (the weaving adds no lot to the declared "
        "queue); the FOUR seam rows (BSD summit, Beal statement, the queue, the Beal "
        "census) byte-identical to the seed store; the queue byte-identical off-script; "
        "two runs byte-identical. If the nine checks hold on both runs (final store = "
        "seed 1756 + five new facts + the mechanism-counted mastery events), the "
        "weaving line holds and the CONNECTING WORK of the prize-island initiative "
        "CLOSES: the four closed islands stand connected in the course."
    )
    metric = "S20 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_24()
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
                Path("results/phase-6/e6.24-run1/session-S02.json"),
                Path("results/phase-6/e6.24-run1/session-S03.json"),
                Path("results/phase-6/e6.24-run1/session-S04.json"),
                Path("results/phase-6/e6.24-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
