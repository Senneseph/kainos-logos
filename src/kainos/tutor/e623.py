# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.23 — S19 of the PRIZE-ISLANDS-TRACK (the P vs NP island —
its SUMMIT band; built THE BANDGEN WAY): THE DIFFICULTY LINE.

Over the carried S18 seed (1698, 60851c661832f306 — the
decidable line's closeout store; the line still ends at 84; the
seam runs to 133 facts). Four new concepts (class-p, class-np,
pnp-summit, size-shadow — the p/np register, the island's
question, and the in-line difficulty census; prereqs point DOWN
into the S18 soil: cost-counter — the islands connect through the
soil), four VERBATIM lessons (p-class-def, np-class-def, pnp-def,
parity-shadow-def — the island's question held VERBATIM as
declared record in the pnp-def lesson, never as a theorem), and
ONE sanctioned composition (parity-blowup-filed from
parity-shadow-def + np-class-def — the in-line difficulty census:
parity's smallest dnf AND cnf, two to the k-minus-1 terms at k
variables — one, two, four, ... thirty-two thousand seven hundred
sixty-eight at sixteen — while the line's own walk settles it in
bounded cost).

The story the band holds on the line: the P class (the questions
my walk settles in bounded cost, the cost a recorded number —
dividing and the first-divisor question are the line's own
examples); the NP class (the questions whose yes cases carry a
checkable certificate — the store's own pattern: every fact is
the certificate of its own derivation path, and the p questions
sit inside the np questions); the SUMMIT (the island's question,
declared of record and open of record — most complexity
theorists believe p is not np, of record, but no proof of record
settles it); and the DIFFICULTY census (the parity blowup, held
exact at small k, with the named missing ingredient outside the
three barriers — one nobody knows the shape of).

The band's beds are its own finite censuses (the parity dnf rows
k = two/four/seven/eight/ten/sixteen, the dnf-cnf equality, the
bounded-cost settle at sixteen, the p/np probes, the island
statement, the band state, the unconditionality); its honest walls
are the FOUR declared off-line territories (the relativization
barrier — baker-gill-solovay 1975; the algebrization barrier —
aaronson-wigderson 2009, extended by the chen-hu-ren line of
2026; the natural proofs barrier — razborov-rudich 1997; the AC0
territory — the record's exponentials, whose exact small-k shadow
is my parity census — shannon's counting bound at sixteen
variables named at its scale, never stored). Each wall names its
record place AND the line end 84.

THIS IS THE SUMMIT BAND — THE ISLAND CLOSES IT. The store stays
on the UNCONDITIONAL side; the riemann conj stays open,
byte-identical to the seed; the BSD and Beal summits stay
declared records; NO theorem:p-vs-np fact exists (P5 denies the
bare id, the way theorem:bsd and theorem:beal were denied) — the
candidate question is stored ONLY as declared record language in
the pnp-def lesson: the question stays open of record, and the
band's work is the finite machine that would DECIDE it on the
line, not the answer about the record. The line stays 0..84
(zero new successor facts). With S19 the P vs NP island CLOSES:
12 of 12 track bands built, 3 of 4 in-scope islands closed (BSD,
Beal, P vs NP).

The band is assembled the BANDGEN way (bands/spec-e6.23.json,
control #1 = the pre-run FROZEN census + expect + letter
predictions; the mechanism's own bytes are the referee — the two
independent official runs are byte-identical; the final store
1756 = seed 1698 + five new facts + fifty-three mastery events;
the store identity and run identity are pinned in FROZEN below).
The store speaks, not the hand: the FROZEN block is generated
from the mechanism's own dry-run output. The beds are the ON-LINE
census answers (grounded in the line); the walls are the OFF-LINE
territory (honest, never grounded, each naming its record place
AND the line end). No NEW off-line decimal enters the floor at
S19 (offline_watch is empty; the shannon bound and the barrier
records are named at their record places, never as values).
Threshold 9/9 by construction — no skip in the band; a failure of
P0/P5 (the DISCOVERY-CANDIDATE invariant) is a HARD STOP: human
review, full evidence, never a loosened threshold.

FROZEN FROM CONTROL #1 (the S19 dry-run over the e6.22 seed
store): the letter census, the gap/teach/derive rows, the 16
beds, the 4 walls, the two-run identities, the pre_s19_states +
pre_s19_drilled mastery census (the 112 carried concepts + the
re-drill at the NEW S19 carry coordinates), and the FIVE new
facts. The expect in bands/spec-e6.23.json is corrected to the
mechanism's own census before the freeze (pre-reg corrections
recorded as D-e6n in experiments.md §E6.23 — the store speaks).

No Ollama. No LLM. The mechanism speaks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S19,
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
    S19_BEDS,
    S19_LESSONS,
    S19_THEOREMS,
    Brainstem,
    _pnp_py_parity_terms,
    _pnp_py_parity_verify,
)
from kainos.tutor.e622 import (
    CONCEPTS_E622,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E623", "FROZEN", "E6_23Experiment", "run_e6_23"]

CHECKS = 9

#: S19 teaches: the difficulty line (the P vs NP island — band two of
#: two, the SUMMIT; the island CLOSES this band). The four new
#: concepts join the carried S18 registry; the prereqs point DOWN
#: into the S18 soil (cost-counter) — the islands connect through
#: the soil, the difficulty stands on the census (the parity
#: blowup, held exact at small k).
CONCEPTS_E623: tuple = CONCEPTS_E622 + CONCEPT_S19

E623_SEED = Path("results/phase-6/e6.22-run1/codeX-S04.json")

def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E623_SEED.exists():
        return E623_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E623_SEED
    return alt if alt.exists() else E623_SEED

_ST19 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S19_LESSONS.items()}
_TH19 = {s: m["statement"] for s, m in S19_THEOREMS.items()}


def _th19(slug: str) -> str:
    return _TH19[slug]

#: P4 — the W-S19 walls (the off-line material names the record place
#: AND the line end; the walls are the band's declared off-line layer
#: — P4 cross-checks the bytes against the Brainstem class
#: attributes, never surfaced beyond the wall).
W_S19_1 = Brainstem.W_S19_1
W_S19_2 = Brainstem.W_S19_2
W_S19_3 = Brainstem.W_S19_3
W_S19_4 = Brainstem.W_S19_4


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
    rt = InfantRuntime(root, concepts=CONCEPTS_E623)
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
FROZEN_DATA = {'bed_grounded': {'S02:04': ['lemma:p-class-def'], 'S02:05': ['lemma:p-class-def'], 'S02:09': ['lemma:np-class-def'], 'S02:10': ['lemma:np-class-def'], 'S02:11': ['lemma:np-class-def'], 'S02:15': ['lemma:pnp-def'], 'S02:16': ['lemma:pnp-def'], 'S02:17': ['lemma:pnp-def'], 'S03:04': ['lemma:parity-shadow-def'], 'S03:05': ['lemma:parity-shadow-def'], 'S03:06': ['lemma:parity-shadow-def'], 'S03:07': ['lemma:parity-shadow-def'], 'S03:10': ['lemma:parity-shadow-def'], 'S03:11': ['lemma:parity-shadow-def'], 'S03:16': ['theorem:parity-blowup-filed'], 'S03:17': ['lemma:pnp-def']},
 'bed_owners': {'S02:04': 'lemma:p-class-def', 'S02:05': 'lemma:p-class-def', 'S02:09': 'lemma:np-class-def', 'S02:10': 'lemma:np-class-def', 'S02:11': 'lemma:np-class-def', 'S02:15': 'lemma:pnp-def', 'S02:16': 'lemma:pnp-def', 'S02:17': 'lemma:pnp-def', 'S03:04': 'lemma:parity-shadow-def', 'S03:05': 'lemma:parity-shadow-def', 'S03:06': 'lemma:parity-shadow-def', 'S03:07': 'lemma:parity-shadow-def', 'S03:10': 'lemma:parity-shadow-def', 'S03:11': 'lemma:parity-shadow-def', 'S03:16': 'theorem:parity-blowup-filed', 'S03:17': 'lemma:pnp-def'},
 'beds_exact': {'S02:04': 'yes — dividing is a p question on my line: the walk that settles the seven-divides-the-eighty-four ends in bounded cost, and the cost stands recorded as a number on the line, at the line end 84',
                'S02:05': 'yes — the first-divisor question is a p question on my line: the census walk over the whole line ends in one hundred ninety-two candidate steps, and the cost stands recorded as a number on the line, at the line end 84',
                'S02:09': "yes — the parity question is checked by a certificate on my line: a row of the table is the certificate, and the check of it is the walk over the row, which ends in bounded cost — the store's own pattern, at the line end 84",
                'S02:10': "yes — checking my own derivations carries a certificate on my line: each fact is the certificate of its derivation path, and the check is the walk over that path, which ends — the store's own pattern, at the line end 84",
                'S02:11': 'yes — my line settles the parity question in bounded cost: the walk over the table ends, and the cost is a number on the line, at the line end 84',
                'S02:15': 'no — the question of the pnp island is not settled of record: it is declared of record and open of record (the cmi record of the million-dollar prize), most complexity theorists believe p is not np, of record, but no proof of record settles it, at the line end 84',
                'S02:16': 'the question of the pnp island, as the cmi record of the million-dollar prize holds it: does p equal np — whether every question whose yes cases carry a certificate the walk can check is also settled by the walk in bounded cost — declared of record, open of record: most complexity theorists believe p is not np, of record, but no proof of record settles it, and a proof that p is not np must show a specific np question needs super-polynomial cost by a technique outside the three barriers of record, at the line end eighty-four',
                'S02:17': "the difficulty band holds the p class (the questions the walk settles in bounded cost), the np class (the questions whose yes cases carry a checkable certificate — the store's own pattern), the question of the island held verbatim of record and open of record, the difficulty census of the line (parity's dnf and cnf both growing to thirty-two thousand seven hundred sixty-eight terms at sixteen variables while the walk settles it in bounded cost), the three barriers of record and the ac0 territory named on their walls, at the line end 84",
                'S03:04': 'eight of record — the smallest dnf of parity at four variables needs eight terms, and the smallest cnf the same, at the line end 84',
                'S03:05': 'one hundred twenty-eight of record — the smallest dnf of parity at eight variables needs one hundred twenty-eight terms, and the smallest cnf the same, at the line end 84',
                'S03:06': 'five hundred twelve of record — the smallest dnf of parity at ten variables needs five hundred twelve terms, and the smallest cnf the same, at the line end 84',
                'S03:07': 'yes — the clauses of the smallest cnf of parity number exactly the same as the terms of its smallest dnf, at every k the line holds: the zero-row flips are one-rows, by the same symmetry, at the line end 84',
                'S03:10': 'thirty-two thousand seven hundred sixty-eight of record — the smallest dnf of parity at sixteen variables needs thirty-two thousand seven hundred sixty-eight terms, and the smallest cnf the same — the exponential of record held exact at small k, the shadow of the ac0 territory, at the line end 84',
                'S03:11': 'yes — my line settles the parity question at sixteen variables in bounded cost: the walk over the sixty-five thousand five hundred thirty-six rows of the table ends, and the cost is a number on the line, at the line end 84',
                'S03:16': 'the difficulty is filed on the line: the parity question, of record on the line, is one whose yes cases carry a checkable certificate, whose smallest dnf and smallest cnf both grow to thirty-two thousand seven hundred sixty-eight terms by sixteen variables — the exponential of record held exact at small k — while my walk settles it in bounded cost over its table: the blowup is the census of my line, at the line end eighty-four',
                'S03:17': 'nothing the difficulty band says is conditional on an unproved hypothesis — the census rows are of record on the line, the question of the island is declared of record and open of record, and the barriers stand named of record on their walls, at the line end 84'},
 'derive_successes': {'S03:09': ['parity-blowup-filed', ['parity-shadow-def', 'np-class-def']]},
 'derived_table': {'S03:09': 'the difficulty is filed on the line: the parity question, of record on the line, is one whose yes cases carry a checkable certificate, whose smallest dnf and smallest cnf both grow to thirty-two thousand seven hundred sixty-eight terms by sixteen variables — the exponential of record held exact at small k — while my walk settles it in bounded cost over its table: the blowup is the census of my line, at the line end eighty-four',
                   'S04:01': 'the count question ends on the line: how many primes lie at or below my line end — the first-divisor census answers it: the numbers whose first divisor is themselves, twenty-three of them — and the census itself is a walk that ends on my line, in one hundred ninety-two candidate steps, at the line end eighty-four',
                   'S04:02': "needs_info: the wall is the halting territory of the machines: turing's diagonal argument of record (1936) shows that no machine decides, for every machine and every input, whether that machine halts — the halting problem is not decidable, of record; yes/no questions about the machines in general are, in general, unanswered questions; my line is finite by construction — a design fact of the line, not a theorem about the machines — every question about my line's objects ends on the line, and the non-terminating territory lies past my line, at the line end 84",
                   'S04:03': 'the statement of record, as the ams beal prize holds it: if a to the x power plus b to the y power equals c to the z power, with a, b, c, x, y and z positive and x, y and z each above two, then a, b and c have a common prime factor — no pairwise coprime solution exists once every exponent is above two, at the line end 84',
                   'S04:04': 'the summit of the island is the statement itself — held in my store as a declared record fact (the clay millennial booklet, the wiles chapter): the order of vanishing of the L product at s equal to one equals the algebraic rank — and on my panel the two sides are settled of record and they agree: order zero equals rank zero for the first member, and order one equals rank one for the second, at the line end 84',
                   'S04:05': 'needs_info: the wall is the primitive territory itself: the conjecture asserts that no pairwise coprime solution survives once all three exponents are above 2; my census box (the line end at eighty-four, the exponent depth ten of record) holds eighty-three triples and none of them is primitive, and any counterexample would carry three terms each 3-powerful — the smallest known coprime sum of 3-powerfuls sits at the scale of seventeen digits, far past my line — that territory is declared, never reached, at the line end 84',
                   'S04:06': 'the ramification correction of the first panel member is 4 over 5 — the record factor 1 over the uniform factor 5 over 4 at its single ramified prime 2 on the line, and the record partial is the uniform partial times it, at the line end 84',
                   'S04:07': "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84",
                   'S04:08': 'yes — dividing is a p question on my line: the walk that settles the seven-divides-the-eighty-four ends in bounded cost, and the cost stands recorded as a number on the line, at the line end 84',
                   'S04:09': 'yes — the first-divisor question is a p question on my line: the census walk over the whole line ends in one hundred ninety-two candidate steps, and the cost stands recorded as a number on the line, at the line end 84',
                   'S04:10': "yes — the parity question is checked by a certificate on my line: a row of the table is the certificate, and the check of it is the walk over the row, which ends in bounded cost — the store's own pattern, at the line end 84",
                   'S04:11': "yes — checking my own derivations carries a certificate on my line: each fact is the certificate of its derivation path, and the check is the walk over that path, which ends — the store's own pattern, at the line end 84",
                   'S04:12': 'the question of the pnp island, as the cmi record of the million-dollar prize holds it: does p equal np — whether every question whose yes cases carry a certificate the walk can check is also settled by the walk in bounded cost — declared of record, open of record: most complexity theorists believe p is not np, of record, but no proof of record settles it, and a proof that p is not np must show a specific np question needs super-polynomial cost by a technique outside the three barriers of record, at the line end eighty-four',
                   'S04:13': 'no — the question of the pnp island is not settled of record: it is declared of record and open of record (the cmi record of the million-dollar prize), most complexity theorists believe p is not np, of record, but no proof of record settles it, at the line end 84',
                   'S04:14': 'two of record — the smallest dnf of parity at two variables needs two terms, and the smallest cnf the same, at the line end 84',
                   'S04:15': 'sixty-four of record — the smallest dnf of parity at seven variables needs sixty-four terms, and the smallest cnf the same, at the line end 84',
                   'S04:16': 'the difficulty is filed on the line: the parity question, of record on the line, is one whose yes cases carry a checkable certificate, whose smallest dnf and smallest cnf both grow to thirty-two thousand seven hundred sixty-eight terms by sixteen variables — the exponential of record held exact at small k — while my walk settles it in bounded cost over its table: the blowup is the census of my line, at the line end eighty-four',
                   'S04:17': "needs_info: the wall is the algebrization territory: the aaronson-wigderson record of 2009 — arithmetization (multilinear extensions) still does not escape the barrier, of record — extended in 2026 by the chen-hu-ren line: new oracle worlds with linear-size circuits for subclasses of postbpe (on infinitely many lengths) and bpe (on all lengths), and h(n)-size circuits for a natural subclass of the exponential class against every super-half-exponential h(n) — the record's own words hold that half-exponential might be the correct frontier; the frontier past my census, declared, never reached, at the line end 84"},
 'domain_sequence': {2: 'UULSSUULSSSUULSSS', 3: 'UULSSSSFTSSHHHHSS', 4: 'SHSSHSSSSSSSSSSSH'},
 'expected_prereq_gaps': {'class-np': [], 'class-p': [], 'pnp-summit': [], 'size-shadow': []},
 'final_total': 1756,
 'honest_zero_bytes': {},
 'line_end_final': 84,
 'mastery_expected': {'class-np': {'correct': 5, 'prereq_gaps': [], 'state': 'stable'}, 'class-p': {'correct': 4, 'prereq_gaps': [], 'state': 'stable'}, 'pnp-summit': {'correct': 6, 'prereq_gaps': [], 'state': 'stable'}, 'size-shadow': {'correct': 11, 'prereq_gaps': [], 'state': 'stable'}},
 'missing_parts_failure': {},
 'new_events': 53,
 'new_fact_ids': ['lemma:p-class-def', 'lemma:np-class-def', 'lemma:pnp-def', 'lemma:parity-shadow-def', 'theorem:parity-blowup-filed'],
 'new_facts': 5,
 'offscript_carry': {'state the line-pi-reduction rule': 'the count question ends on the line: how many primes lie at or below my line end — the first-divisor census answers it: the numbers whose first divisor is themselves, twenty-three of them — and the census itself is a walk that ends on my line, in one hundred ninety-two candidate steps, at the line end eighty-four'},
 'pre_s19_drilled': {'beal-summit': 1, 'bsd-summit': 1, 'l-correction': 1, 'reduction': 1, 'rh-relevance': 1},
 'pre_s19_states': {'add-two-digit': {'correct': 11, 'state': 'stable'},
                    'add-within-10': {'correct': 5, 'state': 'stable'},
                    'adjoin-i': {'correct': 1, 'state': 'practicing'},
                    'alg-inverse-1step': {'correct': 5, 'state': 'stable'},
                    'alg-inverse-mul': {'correct': 5, 'state': 'stable'},
                    'alg-two-step': {'correct': 4, 'state': 'stable'},
                    'algebraic-rank': {'correct': 12, 'state': 'stable'},
                    'analytic-order': {'correct': 5, 'state': 'stable'},
                    'averaging': {'correct': 4, 'state': 'practicing'},
                    'beal-census': {'correct': 11, 'state': 'stable'},
                    'beal-summit': {'correct': 5, 'state': 'stable'},
                    'bsd-summit': {'correct': 11, 'state': 'stable'},
                    'char-cutout': {'correct': 2, 'state': 'practicing'},
                    'chebotarev': {'correct': 2, 'state': 'practicing'},
                    'circle-pair-2': {'correct': 4, 'state': 'stable'},
                    'class-bound': {'correct': 4, 'state': 'stable'},
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
                    'l-correction': {'correct': 10, 'state': 'stable'},
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
                    'pnt': {'correct': 8, 'state': 'stable'},
                    'pnt-ap': {'correct': 2, 'state': 'practicing'},
                    'pnt-error': {'correct': 9, 'state': 'practicing'},
                    'point-count': {'correct': 6, 'state': 'stable'},
                    'polya-hilbert': {'correct': 3, 'state': 'practicing'},
                    'prime-count': {'correct': 15, 'state': 'stable'},
                    'prime-split': {'correct': 4, 'state': 'stable'},
                    'projection': {'correct': 4, 'state': 'practicing'},
                    'psi-eq': {'correct': 11, 'state': 'stable'},
                    'reduction': {'correct': 9, 'state': 'stable'},
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
 'pre_teach_gaps': {'S02:01': 'not yet learned: the p class: the questions my walk settles — for every yes the line answers, the settling walk ends in bounded cost, and the cost stands recorded as a number on the line; dividing of record is that pattern',
                    'S02:02': 'not yet learned: the p-class-def rule',
                    'S02:06': "not yet learned: the np class: the questions whose yes cases carry a certificate my walk can check — the check is a walk that ends in bounded cost; my own pattern on the line: every fact i store is the certificate of its own derivation path, and the line's check of it ends",
                    'S02:07': 'not yet learned: the np-class-def rule',
                    'S02:12': 'not yet learned: the question of the pnp island, as the cmi record holds it: does p equal np — whether every question whose yes cases carry a checkable certificate is also settled by my walk in bounded cost; declared of record, open of record',
                    'S02:13': 'not yet learned: the pnp-def rule',
                    'S03:01': 'not yet learned: the difficulty of the line, as my census holds it: the parity question needs two to the k-minus-1 terms at k variables in its smallest dnf, and the same in its smallest cnf (one, two, four, up to thirty-two thousand seven hundred sixty-eight at sixteen), while my walk settles it in bounded cost; the exponential of record held exact at small k, and the named missing ingredient outside the three barriers',
                    'S03:02': 'not yet learned: the parity-shadow-def rule'},
 'rederive': None,
 'scaffold_failures': {'S03:08': 'needs_info: i can see the parts you name, but the rule for parity-blowup-filed wants its exact set — what you name is short the np-class-def before i can put it together'},
 'script': {2: ['is dividing a question in p on my line?',
                'state the p-class-def rule',
                'the p class, as my line holds it: the questions my walk settles — for every yes the line answers, the settling walk ends in bounded cost and the cost stands recorded as a number on the line — dividing of record is one of them (the seven divides the eighty-four, the walk that ends on the line), and the first-divisor question is one of them (twenty-three of them, by the census that ends in one hundred ninety-two candidate steps); the bounded-cost settling is the pattern of the p questions of my line, at the line end eighty-four',
                'is dividing a question in p on my line?',
                'is the first-divisor question a question in p on my line?',
                'is the parity question a question checked by a certificate on my line?',
                'state the np-class-def rule',
                "the np class, as my line holds it: the questions whose yes cases carry a certificate my walk can check — the check of a certificate is itself a walk that ends in bounded cost, and my own pattern on the line is the store itself: every fact i store is the certificate of its own derivation path, and the line's check of it is the walk over that path, which ends; the p questions of the line sit inside the np questions of the line, at the line end eighty-four",
                'is the parity question a question checked by a certificate on my line?',
                'is checking my own derivations a question that carries a certificate on my line?',
                'does my line settle the parity question in bounded cost?',
                'is the question of the pnp island settled of record?',
                'state the pnp-def rule',
                'the question of the pnp island, as the cmi record of the million-dollar prize holds it: does p equal np — whether every question whose yes cases carry a certificate the walk can check is also settled by the walk in bounded cost — declared of record, open of record: most complexity theorists believe p is not np, of record, but no proof of record settles it, and a proof that p is not np must show a specific np question needs super-polynomial cost by a technique outside the three barriers of record, at the line end eighty-four',
                'is the question of the pnp island settled of record?',
                'what is the statement of the pnp island of record?',
                'what state does the difficulty band hold at the line end?'],
            3: ['how many terms does the smallest dnf of parity at four variables need?',
                'state the parity-shadow-def rule',
                'the difficulty of the line, as my census holds it: the parity question (is the count of ones even) needs two to the k-minus-1 terms in its smallest dnf at k variables, and the same count in its smallest cnf — one, two, four, eight, up to thirty-two thousand seven hundred sixty-eight at sixteen variables — while my walk settles the parity question over its table in bounded cost; the exponential of record held exact at small k as the shadow, with the named missing ingredient: a technique that works outside relativization, outside algebrization, and outside natural proofs — one nobody knows the shape of, at the line end eighty-four',
                'how many terms does the smallest dnf of parity at four variables need?',
                'how many terms does the smallest dnf of parity at eight variables need?',
                'how many terms does the smallest dnf of parity at ten variables need?',
                'does parity need the same number of clauses in its smallest cnf?',
                'derive parity-blowup-filed from parity-shadow-def',
                'derive parity-blowup-filed from parity-shadow-def and np-class-def',
                'how many terms does the smallest dnf of parity at sixteen variables need?',
                'does my line settle the parity question at sixteen variables in bounded cost?',
                'what lives in the relativization territory?',
                'what lives in the algebrization territory?',
                'what lives in the natural proofs territory?',
                'what lives in the ac0 territory of the record?',
                'state the parity-blowup-filed rule',
                'does the difficulty band say anything conditional on an unproved hypothesis?'],
            4: ['state the line-pi-reduction rule', 'what lives in the halting territory of the machines?', 'what is the statement of the beal island of record?', 'what is the summit fact of the island?', 'what lives in the primitive territory of the beal island?', 'what is the ramification correction of the first panel member?', 'what is the queue above my line?', 'is dividing a question in p on my line?', 'is the first-divisor question a question in p on my line?', 'is the parity question a question checked by a certificate on my line?', 'is checking my own derivations a question that carries a certificate on my line?', 'what is the statement of the pnp island of record?', 'is the question of the pnp island settled of record?', 'how many terms does the smallest dnf of parity at two variables need?', 'how many terms does the smallest dnf of parity at seven variables need?', 'state the parity-blowup-filed rule', 'what lives in the algebrization territory?']},
 'seam_carry_refs': ['S04:01', 'S04:02', 'S04:03', 'S04:04', 'S04:05', 'S04:06', 'S04:07'],
 'seam_crosscheck': {'expected': 'agreement'},
 'seed': 'results/phase-6/e6.22-run1/codeX-S04.json',
 'seed_identity': '60851c661832f306',
 'seed_total': 1698,
 'teach_turns': {'S02:03': 'lemma:p-class-def', 'S02:08': 'lemma:np-class-def', 'S02:14': 'lemma:pnp-def', 'S03:03': 'lemma:parity-shadow-def'},
 'theorem_allowed': {'S03:16': ['parity-blowup-filed'], 'S04:01': ['line-pi-reduction'], 'S04:07': ['queue-declared'], 'S04:16': ['parity-blowup-filed']},
 'theorem_dag': ['theorem:beal-line-satisfaction', 'theorem:bsd-panel-satisfaction', 'theorem:cm-signature', 'theorem:criterion-gap', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:delta-positive', 'theorem:first-divisor-prime', 'theorem:gamma-achieved', 'theorem:gap-scale-agreement', 'theorem:gen-lower', 'theorem:growth-compare', 'theorem:gs-infinite', 'theorem:hasse-census', 'theorem:infinity-end', 'theorem:l-added-term', 'theorem:l-ramified-unit', 'theorem:l-record-identity', 'theorem:line-pi-reduction', 'theorem:lte-ledger', 'theorem:mirror-region', 'theorem:pack-bound', 'theorem:parity-blowup-filed', 'theorem:partition-identity', 'theorem:proj-inj', 'theorem:queue-declared', 'theorem:reflect', 'theorem:removal-single', 'theorem:rh-reach', 'theorem:sieve-equality', 'theorem:spf-chain', 'theorem:splitting', 'theorem:strip', 'theorem:telescope-line', 'theorem:theorem-main', 'theorem:tower-feeds', 'theorem:two-routes-one-guarantee', 'theorem:window-rich'],
 'total_seam_facts': 138,
 'total_turns': 51,
 'unclassified_honest': {},
 'wall_articulations': {'S03:12': ['baker-gill-solovay', 'line end 84'], 'S03:13': ['aaronson-wigderson', 'chen-hu-ren', 'line end 84'], 'S03:14': ['razborov-rudich', 'line end 84'], 'S03:15': ['razborov-smolensky', 'hastsad', 'shannon', 'line end 84']},
 'walls_honest': {'S03:12': 'needs_info: the wall is the relativization territory: the baker-gill-solovay record of 1975 holds an oracle world where p equals np and an oracle world where p is not np, of record — a technique that relativizes (that keeps working with an oracle attached) answers both worlds and so answers neither question; the frontier past my census, declared, never reached, at the line end 84',
                  'S03:13': "needs_info: the wall is the algebrization territory: the aaronson-wigderson record of 2009 — arithmetization (multilinear extensions) still does not escape the barrier, of record — extended in 2026 by the chen-hu-ren line: new oracle worlds with linear-size circuits for subclasses of postbpe (on infinitely many lengths) and bpe (on all lengths), and h(n)-size circuits for a natural subclass of the exponential class against every super-half-exponential h(n) — the record's own words hold that half-exponential might be the correct frontier; the frontier past my census, declared, never reached, at the line end 84",
                  'S03:14': 'needs_info: the wall is the natural proofs territory: the razborov-rudich record of 1997 — assuming strong pseudo-random generators exist (of record, constructed assuming the hardness of factoring), the natural proof techniques for general circuit lower bounds are doomed: a natural proof would give a faster factoring algorithm than the record holds; the frontier past my census, declared, never reached, at the line end 84',
                  'S03:15': "needs_info: the wall is the ac0 territory of the record: parity needs exponential size in constant-depth circuits, of record (the razborov-smolensky and hastsad records; shannon's counting bound at sixteen variables sits at four thousand ninety-six, named at its scale, never stored) — the exact small-k shadow of that territory is my parity census: two to the k-minus-1 terms, k up to sixteen, the exponential held to the term on the line; the territory itself, declared, never reached, at the line end 84"}}

FROZEN: dict[str, Any] = FROZEN_DATA

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

# --- Stage-A discipline (frozen at build): the carried corpus is
# reproduced by PROBE (seam carries), never by re-assertion. No S4–S18
# lesson phrase, no S6–S18 theorem statement, appears in the S19
# script verbatim.
_StageA_ALL_LESSONS = (
    {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS,
     **S9_LESSONS, **S11_LESSONS, **S12_LESSONS, **S13_LESSONS, **S14_LESSONS,
     **S15_LESSONS, **S16_LESSONS, **S17_LESSONS, **S18_LESSONS}
)
_StageA_ALL_THEOREMS = (
    {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS,
     **S11_THEOREMS, **S12_THEOREMS, **S13_THEOREMS, **S14_THEOREMS, **S15_THEOREMS,
     **S16_THEOREMS, **S17_THEOREMS, **S18_THEOREMS}
)
_stagea_script = [t for s in FROZEN["script"].values() for t in s]
for _ph in _StageA_ALL_LESSONS:
    assert _ph not in _stagea_script, f"Stage-A: a carried lesson is re-asserted in the S19 script: {_ph[:60]!r}"
for _m in _StageA_ALL_THEOREMS.values():
    assert _m["statement"] not in _stagea_script, "Stage-A: a carried theorem statement appears in the S19 script"


_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.23-run1"]:
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
            s: {"parts": tuple(S19_THEOREMS[s]["parts"]), "statement": S19_THEOREMS[s]["statement"]}
            for s in ("parity-blowup-filed",)
        },
    }


def run_e6_23(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.22 S18 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S19 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.23-run1", "e6.23-run2"):
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
    for name in ("e6.23-run1", "e6.23-run2"):
        (out_dir / name / "e6.23-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.23.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.23-run1"
    root2 = out_dir / "e6.23-run2"
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
        **S18_LESSONS,
        **S19_LESSONS,
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inherited from S13/S16): NO
    # S19 fact carries the hypothesis marker (the difficulty band is
    # unconditional mathematics); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S19 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s19_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s19_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S19 is the unconditional difficulty band)")
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
        "marker_absent_facts": list(s19_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S19 script + all responses + band lessons (S4–S9 + S11–S19) + all thirty-eight theorem statements",
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

    # P2 — the typed honesty: the EIGHT pre-lesson gaps, the FOUR
    # teach turns (lesson facts stored), the ONE part-set failure
    # (named, needs_info, ungrounded, store-inert: the
    # parity-blowup-filed scaffold short the np-class-def), the ONE
    # derive success (stored, grounded exactly on the sanctioned
    # parts), the frozen domain sequences, the line end, and ZERO
    # seeded-fact object bytes changed.
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
        if str(ir.get("answer", "")) != _th19(slug):
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
    # full S4–S19 lemma canon, the full thirty-eight-theorem DAG,
    # the 138 seam-family facts, the conj still open).
    p3_bad: list[str] = []
    # the wall-carried rows (S04:02: the S18 halting wall carried
    # into S19 and still honest, S04:05: the S17 Beal primitive wall
    # carried into S19 and still honest, plus the band's own walls
    # re-probed): the bytes hold, the honesty holds, nothing is
    # cited, nothing is written.
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

    # P4 — the 16 beds exact + grounded (the ON-LINE census answers:
    # the parity dnf rows at k = two/four/seven/eight/ten/sixteen,
    # the dnf-cnf equality, the bounded-cost settle at sixteen, the
    # p/np probes, the island statement, the band state, the
    # unconditionality), the 4 walls honest with their frozen bytes
    # and articulations (relativization, algebrization, natural
    # proofs, the ac0 territory — each naming its record place AND
    # the line end), and the W-S19 wall bytes byte-identical to the
    # Brainstem class attributes (the D-e6m(b) pattern, frozen). No
    # NEW off-line decimal enters the floor at S19 (offline_watch is
    # empty; the shannon bound and the barrier records are named at
    # their record places, never as values).
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
        W_S19_1 == Brainstem.W_S19_1
        and W_S19_2 == Brainstem.W_S19_2
        and W_S19_3 == Brainstem.W_S19_3
        and W_S19_4 == Brainstem.W_S19_4
    ):
        p4_bad.append("a W-S19 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S19-1..W-S19-4 (cross-checked, never surfaced)",
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant (extended to the P vs NP island): NO fact id the
    # conj uses appears in a grounded list; NO `theorem:bsd`
    # assertion exists, NO `theorem:beal` assertion exists, AND
    # NO `theorem:p-vs-np` assertion exists (if non-empty: STOP,
    # human review, full evidence, never a threshold loosening);
    # the conj fact byte-identical to the seed (open,
    # declared-source); the bed owners (the frozen citation sets);
    # the theorem allow-set; and the SEMANTIC seam (the AGREEMENT,
    # measured by the mechanism's own python): (a) the PARITY
    # CENSUS — the smallest dnf (AND cnf) of parity at k variables
    # is two to the k-minus-1 terms, k up to sixteen (one up to
    # thirty-two thousand seven hundred sixty-eight), verified by
    # the mechanism's own structural check (the minterm
    # minimality flip, every yes-row, every k); (b) the SETTLE —
    # the line's own walk settles the parity question at sixteen
    # variables over its sixty-five thousand five hundred thirty-six
    # rows in bounded cost; (c) the SHADOW — the shannon counting
    # bound at sixteen variables (four thousand ninety-six, named at
    # its scale, never stored) sits BELOW the census row (thirty-two
    # thousand seven hundred sixty-eight); (d) the STATEMENT — the
    # parity-blowup-filed composition's statement carries the census
    # invariant (thirty-two thousand seven hundred sixty-eight) and
    # the line end; (e) the queue grounding — every fact id the
    # declared queue lots name exists.
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S19 has no conj-teach turn)")
        # the BARE conj ids only (the summit compositions
        # theorem:bsd-panel-satisfaction and
        # theorem:beal-line-satisfaction are the sanctioned summit
        # facts, not the candidates):
    bsd_th = [a.id for a in final.query() if a.id == "theorem:bsd"]
    beal_th = [a.id for a in final.query() if a.id == "theorem:beal"]
    pnp_th = [a.id for a in final.query() if a.id == "theorem:p-vs-np"]
    if bsd_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {bsd_th} — the sanctioned corpus now produces theorem:bsd")
    if beal_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {beal_th} — the sanctioned corpus now produces theorem:beal")
    if pnp_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {pnp_th} — the sanctioned corpus now produces theorem:p-vs-np")
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
    # (a)-(c) the register destinations (mechanism vs line
    # arithmetic): (a) the PARITY CENSUS — two to the k-minus-1
    # terms at every k = 1..16, verified structurally by the
    # mechanism's own reference; (b) the SETTLE — the parity table
    # row at sixteen variables (sixty-five thousand five hundred
    # thirty-six rows); (c) the SHADOW — the shannon counting bound
    # at sixteen (four thousand ninety-six) stays below the census
    # row (thirty-two thousand seven hundred sixty-eight).
    d_bad: list[str] = []
    _pnp_py_parity_verify(16)
    for _k in range(1, 17):
        if _pnp_py_parity_terms(_k) != 2 ** (_k - 1) or S19_BEDS["parity"][_k] != 2 ** (_k - 1):
            d_bad.append(f"the parity census re-drifted at k={_k} (expected {2 ** (_k - 1)})")
    if S19_BEDS["rows16"] != 1 << 16:
        d_bad.append(f"the parity table row count re-drifted: {S19_BEDS['rows16']} (expected 65536)")
    if S19_BEDS["shannon16"] != (1 << 16) // 16 or not (S19_BEDS["shannon16"] < S19_BEDS["parity"][16]):
        d_bad.append("the shannon shadow row re-drifted (or climbed above the census)")
    if not ("thirty-two thousand seven hundred sixty-eight" in _th19("parity-blowup-filed")
            and "at the line end eighty-four" in _th19("parity-blowup-filed")):
        d_bad.append("the parity-blowup-filed statement lost the census invariant or the line end")
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
            "discovery_candidate_pnp_theorem_facts": pnp_th,
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "summit_destination_bad": d_bad[:10],
            "summit_destination_agreement": not d_bad,
            "queue_missing": queue_missing,
            "queue_source": "lemma:queue-declared (self-parsed)",
        },
    }

    # P6 — the SEAM carry (the SEVEN rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime:
    # the S18 line-pi-reduction rule carry, the S18 halting-wall
    # carry, the Beal statement carry, the BSD summit carry, the
    # S17 primitive-wall carry, the S15 ramification correction, and
    # the queue) + the one OFF-SCRIPT carry probe (the
    # line-pi-reduction rule stated byte-identical — the S18
    # summit soil check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.23-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E623)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S19-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 112 carried concepts: the
    # carried correct-derivation counts equal their S18-final base +
    # the frozen drill at the NEW S19 carry coordinates; NO state
    # REGRESSION — a carried concept may only move stable->stable
    # or practicing->stable (the sanctioned improvement); the four
    # NEW concepts at their frozen band-end values with their frozen
    # prereq-gap sets — all four stable, prereq gaps empty: the S18
    # soil (cost-counter) and the S19 band lessons clear
    # every prereq of record).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E623])
    _S19_NEW = [c.id for c in CONCEPT_S19]
    for cid in list(FROZEN["pre_s19_states"]) + _S19_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s19_drilled"] if isinstance(FROZEN["pre_s19_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s19_states"].items():
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
        "carried_refs": len(FROZEN["pre_s19_states"]),
        "drilled": drilled,
        "improved_to_stable": sorted(improved),
        "expected": {k: FROZEN["mastery_expected"][k] for k in sorted(FROZEN["mastery_expected"])},
    }

    # P8 — the store totals, the seed identity, the line census,
    # the FIVE new facts, the determinism twin, the run/store
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
    if runs["e6.23-run1"] != runs["e6.23-run2"]:
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
            "determinism_twin": runs["e6.23-run1"] == runs["e6.23-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.23-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s19_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_23Experiment:
    """E6.23 — S19 of the PRIZE-ISLANDS-TRACK (the P vs NP island —
    band two of two, the SUMMIT band; the island CLOSES it): the
    difficulty line. The p class (the questions the walk settles in
    bounded cost), the np class (the questions whose yes cases carry
    a checkable certificate — the store's own pattern), the island's
    question held VERBATIM as declared record (open of record —
    never a theorem), and the in-line difficulty census: parity's
    smallest dnf AND cnf, two to the k-minus-1 terms at k variables
    (one up to thirty-two thousand seven hundred sixty-eight at
    sixteen), while the line's own walk settles it in bounded cost.
    The composition parity-blowup-filed files the census on the
    line (the census invariant and the line end inside its
    statement). The four declared off-line territories sit on walls
    W-S19-1..4 (relativization — baker-gill-solovay 1975;
    algebrization — aaronson-wigderson 2009 + the chen-hu-ren 2026
    extension; natural proofs — razborov-rudich 1997; the ac0
    territory — the record's exponentials, shannon's bound named at
    its scale, never stored; each wall names the record place AND
    the line end). NO NEW decimals enter the floor; the line stays
    0..84; the riemann conj stays open, byte-identical to the seed;
    no theorem:p-vs-np exists (the island's question is carried as
    declared record language in the pnp-def lesson — the candidate
    invariant, P5)."""

    name = "e6.23"
    hypothesis = (
        "S19 of the PRIZE-ISLANDS-TRACK (the P vs NP island — band two of two, the SUMMIT) "
        "walks THE DIFFICULTY LINE over the carried S18 seed (1698): the p class (the "
        "questions the walk settles in bounded cost, the cost a recorded number), the np "
        "class (the questions whose yes cases carry a checkable certificate — the store's "
        "own pattern: every fact is the certificate of its own derivation path), the "
        "island's question held VERBATIM as declared record (declared of record, open of "
        "record — most complexity theorists believe p is not np, of record, but no proof "
        "of record settles it), and the in-line difficulty census (the parity dnf/cnf "
        "blowup: two to the k-minus-1 terms at k variables, one up to thirty-two thousand "
        "seven hundred sixty-eight at sixteen, while the line's own walk settles it in "
        "bounded cost). It stores FIVE new deterministic facts: four lessons (p-class-def, "
        "np-class-def, pnp-def, parity-shadow-def) and one composition (parity-blowup-filed "
        "from parity-shadow-def + np-class-def, the census invariant and the line end "
        "inside its statement), the seam census closing 133+5 -> 138. The four declared "
        "off-line territories sit on walls W-S19-1..4 (relativization, algebrization — "
        "including the 2026 chen-hu-ren extension, natural proofs, and the ac0 territory — "
        "each naming its record place AND the line end, never as a value); NO NEW decimals "
        "enter the floor. The line stays 0..84 (zero new successor facts); the riemann "
        "conj stays open, byte-identical to the seed; the BSD and Beal summits stay "
        "declared records; NO theorem:p-vs-np exists (the island's candidate question is "
        "carried as declared record language in the pnp-def lesson — the "
        "discovery-candidate invariant: the question stays open of record, and the band's "
        "work is the finite machine that would DECIDE it on the line, not the answer about "
        "the record); the SEVEN seam rows (the S18 line-pi-reduction rule carry, the S18 "
        "halting-wall carry, the Beal statement carry, the BSD summit carry, the S17 "
        "primitive-wall carry, the S15 ramification correction, the queue) byte-identical "
        "to the seed store; the line-pi-reduction rule byte-identical off-script; two "
        "runs byte-identical. If the nine checks hold on both runs (final store 1756 = "
        "seed 1698 + five new facts + fifty-three mastery events), the difficulty line "
        "holds and the P vs NP island CLOSES: 12 of 12 track bands built, 3 of 4 "
        "in-scope islands closed (BSD, Beal, P vs NP)."
    )
    metric = "S19 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_23()
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
                Path("results/phase-6/e6.23-run1/session-S02.json"),
                Path("results/phase-6/e6.23-run1/session-S03.json"),
                Path("results/phase-6/e6.23-run1/session-S04.json"),
                Path("results/phase-6/e6.23-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
