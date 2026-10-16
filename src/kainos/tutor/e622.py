# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.22 — S18 of the PRIZE-ISLANDS-TRACK (the P vs NP island —
its FIRST band; built THE BANDGEN WAY): THE DECIDABLE LINE.

Over the carried S17 seed (1641, e092ef1261ef7210 — the Beal
island's closeout store; the line still ends at 84; the seam runs
to 128 facts). Four new concepts (decision-question,
tamable-machine, reduction, cost-counter — the computability/
complexity register; prereqs point DOWN into the S11 soil:
divides, scan-ledger), four VERBATIM lessons (question-def,
tamable-def, reduction-def, cost-def — the tamability of the
line's machines is a DESIGN FACT of the finite line, walled inside
the lesson against the infinite-tape machines of record), and ONE
sanctioned composition (line-pi-reduction from question-def +
reduction-def — the pi census re-derived through the teaching
register: the first-divisor census of the line counts twenty-three
primes; the SP-factorization scan over the line costs one hundred
ninety-two candidate steps).

The story the band holds on the line: the DECISION question (a
yes/no question on the line, decided by a finite walk); the
TAMABLE machine (a design fact — the line's machines halt, named
as a design property of the finite line, never a theorem about the
machines of record which carry an infinite tape); the REDUCTION
(another question's yes/no re-expressed as a decision question on
the line — the reduction that makes the pi census a decision
question); and the COST counter (the finite ledger of the decision
walks — the scan cost, the heaviest single query, the kill-trials,
the pigeonhole zero-violation rows).

The band's beds are its own finite censuses (the decision probes
seven/thirteen/two/three/seventeen at the line end; the pi census
twenty-three; the scan cost one hundred ninety-two; the heaviest
query eight trials at eighty-three; the cost spot rows; the
kill-trials; the pigeonhole rows n = 1..10 with zero violations);
its honest walls are the COMPUTABILITY WALL (the halting problem —
the machine that decides whether machines halt, walled at its
record place, off-line material naming the record place AND the
line end) and the MACHINE-UNIVERSE WALL (the machines of record
carry an infinite tape; the line's tamability is a design fact of
the finite line, never a theorem about the record).

The P vs NP island (the prize target: $1,000,000 per the CMI
record) — its SUMMIT band is S19, which carries the two classes
(the p class, the np class of record), the island statement
VERBATIM (the CMI/Cook statement, declared record), the island's
genuine in-store difficulty census (the parity DNF blowup, the
line's own finite row), and the three barriers as honest walls
(relativization, algebrization — including the 2026 ITCS
strengthening, natural proofs, and the AC0 barrier territory).
This band (S18) is the island's FOUNDATION: it builds the register
the summit stands on. The store stays on the UNCONDITIONAL side;
the riemann conj stays open, byte-identical to the seed; the BSD
and Beal summits stay declared records. The line stays 0..84
(zero new successor facts). The candidate question (does p equal
np) is stored ONLY as declared record language in the S19 summit
lesson — NO theorem:p-vs-np fact exists (P5 denies the bare id),
the way theorem:bsd and theorem:beal were denied. This is the
island's discovery-candidate discipline: the question stays open
of record, and the band's work is the finite machine that would
DECIDE it on the line, not the answer about the record.

The band is assembled the BANDGEN way (bands/spec-e6.22.json,
control #1 = the pre-run FROZEN census + expect + letter
predictions; the mechanism's own bytes are the referee — the two
independent official runs are byte-identical; the final store
1698 = seed 1641 + five new facts + fifty-two mastery events; the
store identity and run identity are pinned in FROZEN below). The
store speaks, not the hand: the FROZEN block is generated from the
mechanism's own dry-run output. The beds are the ON-LINE census
answers (grounded in the line); the walls are the OFF-LINE
territory (honest, never grounded, each naming its record place
AND the line end). No NEW off-line decimal enters the floor at
S18 (offline_watch is empty). Threshold 9/9 by construction — no
skip in the band; a failure of P0/P5 (the DISCOVERY-CANDIDATE
invariant) is a HARD STOP: human review, full evidence, never a
loosened threshold.

FROZEN FROM CONTROL #1 (the S18 dry-run over the e6.21 seed
store): the letter census, the gap/teach/derive rows, the 18 beds,
the 2 walls, the two-run identities, the pre_s18_states +
pre_s18_drilled mastery census (the 108 carried concepts + the
drill at the NEW S18 coordinates), and the FIVE new facts. The
expect in bands/spec-e6.22.json is corrected to the mechanism's
own census before the freeze (pre-reg corrections recorded as
D-e6m in experiments.md §E6.22 — the store speaks).

No Ollama. No LLM. The mechanism speaks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor.brainstem import (
    CONCEPT_S18,
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
    S18_BEDS,
    S18_LESSONS,
    S18_THEOREMS,
    Brainstem,
    _pnp_py_heaviest,
    _pnp_py_kill_trials,
    _pnp_py_pi_count,
    _pnp_py_pi_list,
    _pnp_py_pigeonhole,
    _pnp_py_scan_cost,
    _pnp_py_spf_cost,
)
from kainos.tutor.e621 import (
    CONCEPTS_E621,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E622", "FROZEN", "E6_22Experiment", "run_e6_22"]

CHECKS = 9

#: S18 teaches: the decidable line (the P vs NP island — band one of
#: two). The four new concepts join the carried S17 registry; the
#: prereqs point DOWN into the S11 soil (divides, scan-ledger) — the
#: islands connect through the soil, the difficulty stands on the
#: census (S19).
CONCEPTS_E622: tuple = CONCEPTS_E621 + CONCEPT_S18

E621_SEED = Path("results/phase-6/e6.21-run1/codeX-S04.json")

def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E621_SEED.exists():
        return E621_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E621_SEED
    return alt if alt.exists() else E621_SEED

_ST18 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S18_LESSONS.items()}
_TH18 = {s: m["statement"] for s, m in S18_THEOREMS.items()}


def _th18(slug: str) -> str:
    return _TH18[slug]

#: P4 — the W-S18 walls (the off-line material names the record place
#: AND the line end; the walls are the band's declared off-line layer
#: — P4 cross-checks the bytes against the Brainstem class
#: attributes, never surfaced beyond the wall).
W_S18_1 = Brainstem.W_S18_1
W_S18_2 = Brainstem.W_S18_2


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
    rt = InfantRuntime(root, concepts=CONCEPTS_E622)
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
FROZEN_DATA = {'bed_grounded': {'S02:04': ['lemma:question-def'], 'S02:05': ['lemma:question-def'], 'S02:06': ['lemma:question-def'], 'S02:12': ['lemma:tamable-def'], 'S02:16': ['lemma:cost-def'], 'S02:17': ['lemma:cost-def'], 'S03:04': ['lemma:reduction-def'], 'S03:05': ['lemma:cost-def'], 'S03:06': ['lemma:cost-def'], 'S03:09': ['lemma:cost-def'], 'S03:10': ['lemma:cost-def'], 'S03:11': ['lemma:cost-def'], 'S03:12': ['lemma:reduction-def'], 'S03:13': ['theorem:line-pi-reduction'], 'S03:14': ['lemma:reduction-def'], 'S03:15': ['lemma:question-def'], 'S03:16': ['lemma:question-def'], 'S03:17': ['lemma:question-def']},
 'bed_owners': {'S02:04': 'lemma:question-def', 'S02:05': 'lemma:question-def', 'S02:06': 'lemma:question-def', 'S02:12': 'lemma:tamable-def', 'S02:16': 'lemma:cost-def', 'S02:17': 'lemma:cost-def', 'S03:04': 'lemma:reduction-def', 'S03:05': 'lemma:cost-def', 'S03:06': 'lemma:cost-def', 'S03:09': 'lemma:cost-def', 'S03:10': 'lemma:cost-def', 'S03:11': 'lemma:cost-def', 'S03:12': 'lemma:reduction-def', 'S03:13': 'theorem:line-pi-reduction', 'S03:14': 'lemma:reduction-def', 'S03:15': 'lemma:question-def', 'S03:16': 'lemma:question-def', 'S03:17': 'lemma:question-def'},
 'beds_exact': {'S02:04': 'yes — the seven divides the eighty-four: twelve of them, at the line end 84',
                'S02:05': 'no — the thirteen does not divide the eighty-four: the walk leaves a remainder of six (thirteen times six is seventy-eight), at the line end 84',
                'S02:06': 'zero violations of record — the seven thousand seven hundred seventy-six maps of five plus one objects into five boxes all carry a shared box (one more object than box forces the share), at the line end 84',
                'S02:12': 'yes — every query i run on my line ends on the line: a finite question on a finite line, a design fact of the line i hold, not a theorem about the machines of record, at the line end 84',
                'S02:16': 'one hundred ninety-two candidate steps of record — the walk over every number from two to my line end, each to its first divisor, at the line end 84',
                'S02:17': 'the number eighty-three — the largest prime below my line end — its walk tries the candidates up to the floor of the square root: eight candidate steps of record, at the line end 84',
                'S03:04': 'twenty-three of record — the numbers from two to my line end whose first divisor is themselves: two, three, five, seven, eleven, thirteen, seventeen, nineteen, twenty-three, twenty-nine, thirty-one, thirty-seven, forty-one, forty-three, forty-seven, fifty-three, fifty-nine, sixty-one, sixty-seven, seventy-one, seventy-three, seventy-nine, eighty-three — the first-divisor census is a walk that ends in one hundred ninety-two candidate steps, at the line end 84',
                'S03:05': 'ninety-five candidate steps over the composites with all candidates, eighty-seven with the prime candidates alone — the kill-trials ledger my first-divisor soil already holds, at the line end 84',
                'S03:06': 'six — the walk tries two, three, four, five, six, and the seven before it stops (seven squared is forty-nine), at the line end 84',
                'S03:09': 'one — the two divides on the first try of the walk, at the line end 84',
                'S03:10': "zero — the walk's loop never runs over the two, at the line end 84",
                'S03:11': 'one — the two divides on the first try of the walk, at the line end 84',
                'S03:12': "the decidable band holds the decision question (the yes/no on my line's objects, ending on the line), the tamability stated as a design fact of my finite line, the reduction (the prime-count question answered by the first-divisor census — twenty-three), the cost counter (one hundred ninety-two candidate steps over the whole line, the heaviest single query eight at eighty-three), the pigeonhole's zero violations, and the halting territory and the machine universe named on their walls, at the line end 84",
                'S03:13': 'the count question ends on the line: how many primes lie at or below my line end — the first-divisor census answers it: the numbers whose first divisor is themselves, twenty-three of them — and the census itself is a walk that ends on my line, in one hundred ninety-two candidate steps, at the line end eighty-four',
                'S03:14': 'nothing the decidable band says is conditional on an unproved hypothesis — the decision table, the first-divisor census, and the cost counter are of record on the line, and the halting territory and the machine universe stand named of record on their walls, at the line end 84',
                'S03:15': 'yes — the two divides the eighty-four: forty-two of them, at the line end 84',
                'S03:16': 'yes — the three divides the eighty-four: twenty-eight of them, at the line end 84',
                'S03:17': 'zero violations of record — the sixty-four maps of three plus one objects into three boxes all carry a shared box (one more object than box forces the share), at the line end 84'},
 'derive_successes': {'S03:08': ['line-pi-reduction', ['question-def', 'reduction-def']]},
 'derived_table': {'S03:08': 'the count question ends on the line: how many primes lie at or below my line end — the first-divisor census answers it: the numbers whose first divisor is themselves, twenty-three of them — and the census itself is a walk that ends on my line, in one hundred ninety-two candidate steps, at the line end eighty-four',
                   'S04:01': 'the statement of record, as the ams beal prize holds it: if a to the x power plus b to the y power equals c to the z power, with a, b, c, x, y and z positive and x, y and z each above two, then a, b and c have a common prime factor — no pairwise coprime solution exists once every exponent is above two, at the line end 84',
                   'S04:02': 'eighty-three triples in the box — a, b, c at or below my line end, the exponents between three and ten of record — and every one of the eighty-three carries its common prime factor: no primitive triple in the box, at the line end 84',
                   'S04:03': 'needs_info: the wall is the primitive territory itself: the conjecture asserts that no pairwise coprime solution survives once all three exponents are above 2; my census box (the line end at eighty-four, the exponent depth ten of record) holds eighty-three triples and none of them is primitive, and any counterexample would carry three terms each 3-powerful — the smallest known coprime sum of 3-powerfuls sits at the scale of seventeen digits, far past my line — that territory is declared, never reached, at the line end 84',
                   'S04:04': 'the ramification correction of the first panel member is 4 over 5 — the record factor 1 over the uniform factor 5 over 4 at its single ramified prime 2 on the line, and the record partial is the uniform partial times it, at the line end 84',
                   'S04:05': "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84",
                   'S04:06': 'yes — every query i run on my line ends on the line: a finite question on a finite line, a design fact of the line i hold, not a theorem about the machines of record, at the line end 84',
                   'S04:07': 'yes — every query i run on my line ends on the line: a finite question on a finite line, a design fact of the line i hold, not a theorem about the machines of record, at the line end 84',
                   'S04:08': 'yes — every query i run on my line ends on the line: a finite question on a finite line, a design fact of the line i hold, not a theorem about the machines of record, at the line end 84',
                   'S04:09': 'twenty-three of record — the numbers from two to my line end whose first divisor is themselves: two, three, five, seven, eleven, thirteen, seventeen, nineteen, twenty-three, twenty-nine, thirty-one, thirty-seven, forty-one, forty-three, forty-seven, fifty-three, fifty-nine, sixty-one, sixty-seven, seventy-one, seventy-three, seventy-nine, eighty-three — the first-divisor census is a walk that ends in one hundred ninety-two candidate steps, at the line end 84',
                   'S04:10': 'one hundred ninety-two candidate steps of record — the walk over every number from two to my line end, each to its first divisor, at the line end 84',
                   'S04:11': 'the number eighty-three — the largest prime below my line end — its walk tries the candidates up to the floor of the square root: eight candidate steps of record, at the line end 84',
                   'S04:12': 'ninety-five candidate steps over the composites with all candidates, eighty-seven with the prime candidates alone — the kill-trials ledger my first-divisor soil already holds, at the line end 84',
                   'S04:13': 'zero violations of record — the twenty-five billion nine hundred thirty-seven million four hundred twenty-four thousand six hundred one maps of ten plus one objects into ten boxes all carry a shared box (one more object than box forces the share), at the line end 84',
                   'S04:14': "needs_info: the wall is the halting territory of the machines: turing's diagonal argument of record (1936) shows that no machine decides, for every machine and every input, whether that machine halts — the halting problem is not decidable, of record; yes/no questions about the machines in general are, in general, unanswered questions; my line is finite by construction — a design fact of the line, not a theorem about the machines — every question about my line's objects ends on the line, and the non-terminating territory lies past my line, at the line end 84",
                   'S04:15': 'the count question ends on the line: how many primes lie at or below my line end — the first-divisor census answers it: the numbers whose first divisor is themselves, twenty-three of them — and the census itself is a walk that ends on my line, in one hundred ninety-two candidate steps, at the line end eighty-four',
                   'S04:16': "the decidable band holds the decision question (the yes/no on my line's objects, ending on the line), the tamability stated as a design fact of my finite line, the reduction (the prime-count question answered by the first-divisor census — twenty-three), the cost counter (one hundred ninety-two candidate steps over the whole line, the heaviest single query eight at eighty-three), the pigeonhole's zero violations, and the halting territory and the machine universe named on their walls, at the line end 84",
                   'S04:17': 'nothing the decidable band says is conditional on an unproved hypothesis — the decision table, the first-divisor census, and the cost counter are of record on the line, and the halting territory and the machine universe stand named of record on their walls, at the line end 84'},
 'domain_sequence': {2: 'UULSSSUULHHSUULSS', 3: 'UULSSSFTSSSSSSSSS', 4: 'SSHSSSSSSSSSSHSSS'},
 'expected_prereq_gaps': {'cost-counter': [], 'decision-question': [], 'reduction': [], 'tamable-machine': []},
 'final_total': 1698,
 'honest_zero_bytes': {},
 'line_end_final': 84,
 'mastery_expected': {'cost-counter': {'correct': 10, 'prereq_gaps': [], 'state': 'stable'}, 'decision-question': {'correct': 7, 'prereq_gaps': [], 'state': 'stable'}, 'reduction': {'correct': 9, 'prereq_gaps': [], 'state': 'stable'}, 'tamable-machine': {'correct': 4, 'prereq_gaps': [], 'state': 'stable'}},
 'missing_parts_failure': {},
 'new_events': 52,
 'new_fact_ids': ['lemma:question-def', 'lemma:tamable-def', 'lemma:reduction-def', 'lemma:cost-def', 'theorem:line-pi-reduction'],
 'new_facts': 5,
 'offscript_carry': {'state the beal-line-satisfaction rule': 'the summit of the island filed on my line: the statement holds of record across the whole census box — the eighty-three triples of the box each carry their common prime factor, no primitive triple lives in the box, and the primitive territory is a wall, at the line end 84'},
 'pre_s18_drilled': {'beal-census': 1, 'beal-summit': 1, 'l-correction': 1},
 'pre_s18_states': {'add-two-digit': {'correct': 11, 'state': 'stable'},
                    'add-within-10': {'correct': 5, 'state': 'stable'},
                    'adjoin-i': {'correct': 1, 'state': 'practicing'},
                    'alg-inverse-1step': {'correct': 5, 'state': 'stable'},
                    'alg-inverse-mul': {'correct': 5, 'state': 'stable'},
                    'alg-two-step': {'correct': 4, 'state': 'stable'},
                    'algebraic-rank': {'correct': 12, 'state': 'stable'},
                    'analytic-order': {'correct': 5, 'state': 'stable'},
                    'averaging': {'correct': 4, 'state': 'practicing'},
                    'beal-census': {'correct': 10, 'state': 'stable'},
                    'beal-summit': {'correct': 4, 'state': 'stable'},
                    'bsd-summit': {'correct': 11, 'state': 'stable'},
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
                    'l-correction': {'correct': 9, 'state': 'stable'},
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
                    'valuation': {'correct': 6, 'state': 'stable'},
                    'window-setup': {'correct': 1, 'state': 'practicing'},
                    'zero-density': {'correct': 4, 'state': 'practicing'},
                    'zero-free': {'correct': 13, 'state': 'practicing'},
                    'zeta-cont': {'correct': 3, 'state': 'practicing'},
                    'zeta-series': {'correct': 7, 'state': 'stable'}},
 'pre_teach_gaps': {'S02:01': "not yet learned: the decision question: a yes/no question about objects on my line — does the seven divide the eighty-four? — every decision question about my line's objects that i run ends on the line with a yes or a no; that is the pattern of the line",
                    'S02:02': 'not yet learned: the question-def rule',
                    'S02:07': "not yet learned: the tamable machine: i am a walk on a finite line, and a finite question on a finite line ends — every query i run about my line's objects ends on the line, stated as a DESIGN FACT of the line, not a theorem about the machines of the record (which carry an infinite tape); my safe region is my line",
                    'S02:08': 'not yet learned: the tamable-def rule',
                    'S02:13': 'not yet learned: the cost counter: cost on the line is a counter — the cost of a query is the number of line-steps its walk takes; the scan over the whole line takes one hundred ninety-two candidate steps, and my ledger records each cost as a number on the line',
                    'S02:14': 'not yet learned: the cost-def rule',
                    'S03:01': 'not yet learned: the reduction: a mapping of question A to question B so that an answer to B answers A — my own reduction on my line: the prime-count question is answered by the first-divisor census (walk the first divisors and count the numbers whose first divisor is themselves)',
                    'S03:02': 'not yet learned: the reduction-def rule'},
 'rederive': None,
 'scaffold_failures': {'S03:07': 'needs_info: i can see the parts you name, but the rule for line-pi-reduction wants its exact set — what you name is short the reduction-def before i can put it together'},
 'script': {2: ['does the seven divide the eighty-four of record?',
                'state the question-def rule',
                "the decision question, as the question my line asks: a yes/no question about objects on my line — does the seven divide the eighty-four? — and every decision question about my line's objects that i run ends on the line with a yes or a no; that is the pattern of the line, at the line end eighty-four",
                'does the seven divide the eighty-four of record?',
                'does the thirteen divide the eighty-four of record?',
                'how many violations live in the pigeonhole at five boxes?',
                'what lives in the halting territory of the machines?',
                'state the tamable-def rule',
                "the tamability of my walk, as the fact i hold: i am a walk on a finite line, and a finite question on a finite line ends — every query i run about my line's objects ends on the line; this is stated as a design fact of the line, not a theorem about the machines of the record (which carry an infinite tape of record), and the questions of those machines about their own halting live past my line, at the line end eighty-four",
                'what lives in the halting territory of the machines?',
                'what lives past my line in the machine universe?',
                'does my walk end on the line, always?',
                'how many candidate steps does the whole-line first-divisor census take?',
                'state the cost-def rule',
                'the cost counter, as the counter i keep: the cost of a query is the number of line-steps its walk takes — the scan over the whole line (the first-divisor walk of every number from two to the line end) takes one hundred ninety-two candidate steps, the heaviest single query on the line takes eight (the walk over the largest prime below the line end), and my ledger records each cost as a number on the line, at the line end eighty-four',
                'how many candidate steps does the whole-line first-divisor census take?',
                'on which number is the heaviest single first-divisor query on my line, and how many steps?'],
            3: ['how many primes lie at or below my line end of record?',
                'state the reduction-def rule',
                "the reduction, as the pattern i execute: a mapping of question a to question b so that an answer to b answers a — on my line the prime-count question is answered by the first-divisor census: to count the primes at or below the line end, walk the first-divisor chains and count the numbers whose first divisor is themselves; my line's own reduction, at the line end eighty-four",
                'how many primes lie at or below my line end of record?',
                'how many candidate steps do the composite walks take, over all candidates and over prime candidates alone?',
                'how many candidate steps does the first-divisor query on forty-nine take?',
                'derive line-pi-reduction from question-def',
                'derive line-pi-reduction from question-def and reduction-def',
                'how many candidate steps does the first-divisor query on sixty-four take?',
                'how many candidate steps does the first-divisor query on two take?',
                'how many candidate steps does the first-divisor query on eighty-four take?',
                'what state does the decidable band hold at the line end?',
                'state the line-pi-reduction rule',
                'does the decidable band say anything conditional on an unproved hypothesis?',
                'does the two divide the eighty-four of record?',
                'does the three divide the eighty-four of record?',
                'how many violations live in the pigeonhole at three boxes?'],
            4: ['what is the statement of the beal island of record?',
                "how many triples does the verification census of the beal island hold in the line's box?",
                'what lives in the primitive territory of the beal island?',
                'what is the ramification correction of the first panel member?',
                'what is the queue above my line?',
                'does my walk end on the line, always?',
                'does my walk end on the line, always?',
                'does my walk end on the line, always?',
                'how many primes lie at or below my line end of record?',
                'how many candidate steps does the whole-line first-divisor census take?',
                'on which number is the heaviest single first-divisor query on my line, and how many steps?',
                'how many candidate steps do the composite walks take, over all candidates and over prime candidates alone?',
                'how many violations live in the pigeonhole at ten boxes?',
                'what lives in the halting territory of the machines?',
                'state the line-pi-reduction rule',
                'what state does the decidable band hold at the line end?',
                'does the decidable band say anything conditional on an unproved hypothesis?']},
 'seam_carry_refs': ['S04:01', 'S04:02', 'S04:03', 'S04:04', 'S04:05'],
 'seam_crosscheck': {'expected': 'agreement'},
 'seed': 'results/phase-6/e6.21-run1/codeX-S04.json',
 'seed_identity': 'e092ef1261ef7210',
 'seed_total': 1641,
 'teach_turns': {'S02:03': 'lemma:question-def', 'S02:09': 'lemma:tamable-def', 'S02:15': 'lemma:cost-def', 'S03:03': 'lemma:reduction-def'},
 'theorem_allowed': {'S03:13': ['line-pi-reduction'], 'S04:05': ['queue-declared'], 'S04:15': ['line-pi-reduction']},
 'theorem_dag': ['theorem:beal-line-satisfaction', 'theorem:bsd-panel-satisfaction', 'theorem:cm-signature', 'theorem:criterion-gap', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:delta-positive', 'theorem:first-divisor-prime', 'theorem:gamma-achieved', 'theorem:gap-scale-agreement', 'theorem:gen-lower', 'theorem:growth-compare', 'theorem:gs-infinite', 'theorem:hasse-census', 'theorem:infinity-end', 'theorem:l-added-term', 'theorem:l-ramified-unit', 'theorem:l-record-identity', 'theorem:line-pi-reduction', 'theorem:lte-ledger', 'theorem:mirror-region', 'theorem:pack-bound', 'theorem:partition-identity', 'theorem:proj-inj', 'theorem:queue-declared', 'theorem:reflect', 'theorem:removal-single', 'theorem:rh-reach', 'theorem:sieve-equality', 'theorem:spf-chain', 'theorem:splitting', 'theorem:strip', 'theorem:telescope-line', 'theorem:theorem-main', 'theorem:tower-feeds', 'theorem:two-routes-one-guarantee', 'theorem:window-rich'],
 'total_seam_facts': 133,
 'total_turns': 51,
 'unclassified_honest': {},
 'wall_articulations': {'S02:10': ['turing', 'line end 84'], 'S02:11': ['machine universe', 'line end 84']},
 'walls_honest': {'S02:10': "needs_info: the wall is the halting territory of the machines: turing's diagonal argument of record (1936) shows that no machine decides, for every machine and every input, whether that machine halts — the halting problem is not decidable, of record; yes/no questions about the machines in general are, in general, unanswered questions; my line is finite by construction — a design fact of the line, not a theorem about the machines — every question about my line's objects ends on the line, and the non-terminating territory lies past my line, at the line end 84",
                  'S02:11': "needs_info: the wall past my line in the machine universe: the machines of record carry an infinite tape (the cmi document's own machine clause) — an unbounded machine runs as long as its question runs; i am one bounded inhabitant of that universe: my ledger holds what my walk computes, and a machine's questions about its own halting are declared territory, not my answers, at the line end 84"}}

FROZEN: dict[str, Any] = FROZEN_DATA

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

# --- Stage-A discipline (frozen at build): the carried corpus is
# reproduced by PROBE (seam carries), never by re-assertion. No S4–S17
# lesson phrase, no S6–S17 theorem statement, appears in the S18
# script verbatim.
_StageA_ALL_LESSONS = (
    {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS,
     **S9_LESSONS, **S11_LESSONS, **S12_LESSONS, **S13_LESSONS, **S14_LESSONS,
     **S15_LESSONS, **S16_LESSONS, **S17_LESSONS}
)
_StageA_ALL_THEOREMS = (
    {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS,
     **S11_THEOREMS, **S12_THEOREMS, **S13_THEOREMS, **S14_THEOREMS, **S15_THEOREMS,
     **S16_THEOREMS, **S17_THEOREMS}
)
_stagea_script = [t for s in FROZEN["script"].values() for t in s]
for _ph in _StageA_ALL_LESSONS:
    assert _ph not in _stagea_script, f"Stage-A: a carried lesson is re-asserted in the S18 script: {_ph[:60]!r}"
for _m in _StageA_ALL_THEOREMS.values():
    assert _m["statement"] not in _stagea_script, "Stage-A: a carried theorem statement appears in the S18 script"


_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.22-run1"]:
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
            s: {"parts": tuple(S18_THEOREMS[s]["parts"]), "statement": S18_THEOREMS[s]["statement"]}
            for s in ("line-pi-reduction",)
        },
    }


def run_e6_22(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.21 S17 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S18 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.22-run1", "e6.22-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.21 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)

    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.22-run1", "e6.22-run2"):
        (out_dir / name / "e6.22-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.22.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.22-run1"
    root2 = out_dir / "e6.22-run2"
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inherited from S13/S16): NO
    # S18 fact carries the hypothesis marker (the decidable band is
    # unconditional mathematics); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S18 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s18_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s18_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S18 is the unconditional decidable band)")
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
        "marker_absent_facts": list(s18_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S18 script + all responses + band lessons (S4–S9 + S11–S18) + all thirty-seven theorem statements",
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
    # line-pi-reduction scaffold short the reduction-def), the ONE
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
        if str(ir.get("answer", "")) != _th18(slug):
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
    # full S4–S17 lemma canon, the full thirty-six-theorem DAG,
    # the 133 seam-family facts, the conj still open).
    p3_bad: list[str] = []
    # the wall-carried rows (S04:03: the S17 Beal primitive wall
    # carried into S18 and still honest, plus the band's own walls
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

    # P4 — the 18 beds exact + grounded (the ON-LINE census answers:
    # the decision probes, the pi census, the scan cost, the
    # heaviest query, the kill-trials, the pigeonhole
    # zero-violation rows, the band state, the unconditionality),
    # the 2 walls honest with their frozen bytes and
    # articulations (the halting problem, the machine universe —
    # each naming its record place AND the line end), and the W-S18
    # wall bytes byte-identical to the Brainstem class attributes
    # (the D-e6k(b) pattern, frozen). No NEW off-line decimal
    # enters the floor at S18 (offline_watch is empty; the
    # machine-universe territory is named at its record place,
    # never as a value).
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
        W_S18_1 == Brainstem.W_S18_1
        and W_S18_2 == Brainstem.W_S18_2
    ):
        p4_bad.append("a W-S18 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S18-1..W-S18-2 (cross-checked, never surfaced)",
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
    # measured by the mechanism's own python): (a) the PI CENSUS —
    # twenty-three primes at or below the line end by the
    # first-divisor census (the reduction re-derived through the
    # register); (b) the COST CENSUS — the whole-line scan one
    # hundred ninety-two candidate steps, the heaviest single query
    # 8 trials at n=83, the cost spot rows, the kill-trials totals;
    # (c) the PIGEONHOLE — the rows n = 1..10 carry zero violations
    # (the line's own finite rows, never a proof about the record);
    # (d) the STATEMENT — the line-pi-reduction composition's
    # statement carries the census invariant (twenty-three / one
    # hundred ninety-two) and the line end; (e) the queue
    # grounding — every fact id the declared queue lots name exists.
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S18 has no conj-teach turn)")
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
    # arithmetic): (a) the PI CENSUS — twenty-three primes at or
    # below the line end by the first-divisor census (the
    # reduction re-derived); (b) the COST CENSUS — the whole-line
    # scan 192 candidate steps, the heaviest single query 8 trials
    # at n=83, the cost spot rows, the kill-trials totals; (c) the
    # PIGEONHOLE — zero violations on every row n = 1..10.
    d_bad: list[str] = []
    _pi = _pnp_py_pi_count(84)
    _plist = _pnp_py_pi_list(84)
    if _pi != 23 or _plist != S18_BEDS["primes"]:
        d_bad.append(f"the pi census re-drifted: {_pi} primes at or below the line end (expected 23)")
    _scan = _pnp_py_scan_cost(84)
    if _scan != 192 or S18_BEDS["scan_cost"] != 192:
        d_bad.append(f"the scan cost re-drifted: {_scan} candidate steps (expected 192)")
    _hm, _hc = _pnp_py_heaviest(84)
    if (_hm, _hc) != (83, 8) or tuple(S18_BEDS["heaviest"]) != (83, 8):
        d_bad.append(f"the heaviest-query row re-drifted: {(_hm, _hc)} (expected (83, 8))")
    for _n, _c in S18_BEDS["cost_spot"].items():
        if _pnp_py_spf_cost(_n) != _c:
            d_bad.append(f"the cost spot row {_n} re-drifted (expected {_c})")
    _kt_all = _pnp_py_kill_trials(84, False)
    _kt_prime = _pnp_py_kill_trials(84, True)
    if (_kt_all, _kt_prime) != tuple(S18_BEDS["kill_trials"]):
        d_bad.append(f"the kill-trials row re-drifted: {(_kt_all, _kt_prime)} (expected {tuple(S18_BEDS['kill_trials'])})")
    for _n in range(1, 11):
        _tot, _inj = _pnp_py_pigeonhole(_n)
        if _inj != 0 or _tot != (_n + 1) ** _n:
            d_bad.append(f"the pigeonhole row {_n} re-drifted (violations appeared or counts moved)")
    if not ("twenty-three" in _th18("line-pi-reduction") and "one hundred ninety-two" in _th18("line-pi-reduction")
            and "at the line end eighty-four" in _th18("line-pi-reduction")):
        d_bad.append("the line-pi-reduction statement lost the census invariant or the line end")
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

    # P6 — the SEAM carry (the FIVE rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime:
    # the Beal statement carry, the Beal census carry, the S17
    # primitive-wall carry, the S15 ramification correction, and
    # the queue) + the one OFF-SCRIPT carry probe (the
    # beal-line-satisfaction rule stated byte-identical — the S17
    # summit soil check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.22-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E622)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S18-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 108 carried concepts: the
    # carried correct-derivation counts equal their S17-final base +
    # the frozen drill at the NEW S18 coordinates; NO state
    # REGRESSION — a carried concept may only move stable->stable
    # or practicing->stable (the sanctioned improvement); the four
    # NEW concepts at their frozen band-end values with their frozen
    # prereq-gap sets — all four stable, prereq gaps empty: the S11
    # soil (divides, scan-ledger) and the S18 band lessons clear
    # every prereq of record).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E622])
    _S18_NEW = [c.id for c in CONCEPT_S18]
    for cid in list(FROZEN["pre_s18_states"]) + _S18_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s18_drilled"] if isinstance(FROZEN["pre_s18_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s18_states"].items():
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
        "carried_refs": len(FROZEN["pre_s18_states"]),
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
    if runs["e6.22-run1"] != runs["e6.22-run2"]:
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
            "determinism_twin": runs["e6.22-run1"] == runs["e6.22-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.22-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s18_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_22Experiment:
    """E6.22 — S18 of the PRIZE-ISLANDS-TRACK (the P vs NP island —
    band one of two): the decidable line. The decision question, the
    tamable machine (a design fact of the finite line, never a
    theorem about the infinite-tape machines of record), the
    reduction, and the cost counter — the register the P vs NP
    summit (S19) stands on. The pi census (twenty-three primes) is
    re-derived through the teaching register by the composition
    line-pi-reduction (the census invariant and the line end inside
    its statement); the scan cost on the line is one hundred
    ninety-two candidate steps; the heaviest single query stands at
    eight trials at eighty-three; the pigeonhole rows n = 1..10 carry
    zero violations. The halting problem and the machine universe sit
    on walls W-S18-1/2 (the off-line territory names the record place
    AND the line end, never a value). NO NEW decimals enter the floor;
    the line stays 0..84; the riemann conj stays open, byte-identical
    to the seed; no theorem:p-vs-np exists (the island's question is
    carried as declared record language in S19 — the candidate
    invariant, P5)."""

    name = "e6.22"
    hypothesis = (
        "S18 of the PRIZE-ISLANDS-TRACK (the P vs NP island — band one of two) walks THE "
        "DECIDABLE LINE over the carried S17 seed (1641): the decision question (a yes/no "
        "question on the line), the tamable machine (the line's machines halt — a DESIGN "
        "FACT of the finite line, walled against the infinite-tape machines of record), the "
        "reduction (re-expressing a census as a decision question on the line), and the cost "
        "counter (the finite ledger of the decision walks). The band's finite censuses: the "
        "decision probes (seven/thirteen/two/three/seventeen at the line end), the pi census "
        "(twenty-three primes — the first-divisor reduction re-derived through the register "
        "by line-pi-reduction), the scan cost (one hundred ninety-two candidate steps), the "
        "heaviest single query (eight trials at eighty-three), the kill-trials, and the "
        "pigeonhole rows n = 1..10 with zero violations. It stores FIVE new deterministic "
        "facts: four lessons (question-def, tamable-def, reduction-def, cost-def) and one "
        "composition (line-pi-reduction from question-def + reduction-def, the census "
        "invariant and the line end inside its statement), the seam census closing 128+5 -> "
        "133. The halting problem and the machine universe sit on walls W-S18-1/2 (the "
        "off-line territory named at its record place AND the line end, never as a value); "
        "NO NEW decimals enter the floor. The line stays 0..84 (zero new successor facts); "
        "the riemann conj stays open, byte-identical to the seed; the BSD and Beal summits "
        "stay declared records; NO theorem:p-vs-np exists (the island's candidate question "
        "is carried as declared record language in the S19 summit lesson — the "
        "discovery-candidate invariant: the question stays open of record, and the band's "
        "work is the finite machine that would DECIDE it on the line, not the answer about "
        "the record); the FIVE seam rows (the Beal statement + census carries, the S17 "
        "primitive-wall carry, the S15 ramification correction, the queue) byte-identical to "
        "the seed store; the beal-line-satisfaction rule byte-identical off-script; two runs "
        "byte-identical. If the nine checks hold on both runs (final store 1698 = seed 1641 "
        "+ five new facts + fifty-two mastery events), the decidable line holds and the P vs "
        "NP island's summit band (S19) is built on solid ground."
    )
    metric = "S18 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_22()
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
                Path("results/phase-6/e6.22-run1/session-S02.json"),
                Path("results/phase-6/e6.22-run1/session-S03.json"),
                Path("results/phase-6/e6.22-run1/session-S04.json"),
                Path("results/phase-6/e6.22-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
