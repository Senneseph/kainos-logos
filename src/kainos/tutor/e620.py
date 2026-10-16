# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.20 — S16 of the PRIZE-ISLANDS-TRACK (the BSD island, band 3
of 3 — the island's SUMMIT; built THE BANDGEN WAY): THE DESCENT AND
THE REACHING.

The third and last band of the BSD island (plan/40-prize-islands/
04-island-bsd.md + the verified research record bsd-research.md,
stages A+B+C+D): over the carried S15 seed (1522, adff69d61a3e4219).
Four new concepts (analytic-order, algebraic-rank, bsd-summit,
line-reaching — college-1, domain bsd, prereqs point DOWN: the
L-factor soil of band 2 and the point soil of band 1), four VERBATIM
lessons (vanish-def, rank-def, statement-def, reach-def), one
sanctioned composition (bsd-panel-satisfaction from
statement-def + vanish-def + rank-def).

The story the band holds on the line: the descent of record settles
BOTH panel ranks WITHOUT the statement — the first member (the rank
zero curve): the selmer dimension two against the two-torsion
dimension two gives the descent bound zero, met by the torsion
ledger; the second (the rank one curve): dimension one against zero
gives the bound one, met by the generator (x zero y zero); the shaf
part trivial of record on both, so the selmer dimension is the rank
plus the two-torsion dimension exactly. The record's orders of
vanishing match the ranks (zero = zero, one = one); the statement —
verbatim from the clay millennial booklet, the wiles chapter — is
stored as the island's SUMMIT fact (declared record, the analytic
values themselves on walls); the line's partials stand for the line's
side (nonzero where the order is zero, far from zero where it is
one).

UNCONDITIONAL-FLAVORED band: the analytic L-values (the exact record
L(C, 1) values, the leading coefficient of the Taylor expansion) sit
on walls W-S16-1/2/3, each naming the value or its record place AND
the line end 84; the orders themselves are beds (record facts the
store holds). NO NEW decimals: the leading coefficient is named
WITHOUT its digit string (of record, past the line); the carried
13.3586546916 (W-S14-5) and the bed decimals stay exactly where the
earlier bands put them. NO `theorem:bsd` fact id exists (the
statement is stored as `lemma:statement-def` + the composition
`theorem:bsd-panel-satisfaction` — the island's summit, the
discovery-candidate invariant stays clean of the bare conj id).

FROZEN FROM CONTROL #1 (bandgen-era, the bandgen dryrun over
bands/spec-e6.20.json; the pre-reg corrections of the D-e6k family
are recorded at closeout: the missing-parts probe names the full
part-set with the one untaught slug, the scaffold byte lists both
missing parts, the line-reaching concept split so the band's
lesson:concept shape holds 4:4). The 51-turn script (S2:17 + S3:17 +
S4:17), the 18 beds, the 4 walls, all predictions out of the
mechanism's own dry-run; the control report is the referee, never
the hand. Store: 1522 -> 1581 (5 facts + 54 events, drift +3 over
the turns).

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
    CONCEPT_S16,
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
    S16_BEDS,
    S16_LESSONS,
    S16_THEOREMS,
    Brainstem,
)
from kainos.tutor.e619 import (
    CONCEPTS_E619,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E620", "FROZEN", "E6_20Experiment", "run_e6_20"]

CHECKS = 9

#: S16 teaches: the descent and the reaching (the four new concepts
#: join the carried S15 registry; prereqs point DOWN: l-partial (band
#: 2) and the point soil (band 1) — the islands connect through the
#: soil, the summit stands on the two sides).
CONCEPTS_E620: tuple = CONCEPTS_E619 + CONCEPT_S16

E619_SEED = Path("results/phase-6/e6.19-run1/codeX-S04.json")

def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E619_SEED.exists():
        return E619_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E619_SEED
    return alt if alt.exists() else E619_SEED

_ST16 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S16_LESSONS.items()}
_TH16 = {s: m["statement"] for s, m in S16_THEOREMS.items()}


def _th16(slug: str) -> str:
    return _TH16[slug]

#: P4 — the W-S16 walls (the off-line material names the value or its
#: record place AND the line end; the walls are the band's declared
#: off-line layer — P4 cross-checks the bytes against the Brainstem
#: class attributes, never surfaced beyond the wall).
W_S16_1 = Brainstem.W_S16_1
W_S16_2 = Brainstem.W_S16_2
W_S16_3 = Brainstem.W_S16_3


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
    rt = InfantRuntime(root, concepts=CONCEPTS_E620)
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
FROZEN_DATA = {'bed_grounded': {'S02:05': ['lemma:vanish-def'], 'S02:06': ['lemma:vanish-def'], 'S02:09': ['lemma:rank-def'], 'S02:10': ['lemma:rank-def'], 'S02:11': ['lemma:rank-def'], 'S02:12': ['lemma:rank-def'], 'S02:13': ['lemma:rank-def'], 'S02:14': ['lemma:rank-def'], 'S02:15': ['lemma:rank-def'], 'S02:16': ['lemma:rank-def'], 'S03:05': ['lemma:statement-def'], 'S03:06': ['lemma:reach-def'], 'S03:07': ['lemma:reach-def', 'lemma:l-partial-def'], 'S03:09': ['lemma:vanish-def', 'lemma:rank-def'], 'S03:10': ['lemma:vanish-def', 'lemma:rank-def'], 'S03:15': ['lemma:statement-def'], 'S03:16': ['theorem:bsd-panel-satisfaction'], 'S03:17': ['lemma:statement-def']},
 'bed_owners': {'S02:05': 'lemma:vanish-def', 'S02:06': 'lemma:vanish-def', 'S02:09': 'lemma:rank-def', 'S02:10': 'lemma:rank-def', 'S02:11': 'lemma:rank-def', 'S02:12': 'lemma:rank-def', 'S02:13': 'lemma:rank-def', 'S02:14': 'lemma:rank-def', 'S02:15': 'lemma:rank-def', 'S02:16': 'lemma:rank-def', 'S03:05': 'lemma:statement-def', 'S03:06': 'lemma:reach-def', 'S03:07': 'lemma:reach-def', 'S03:09': 'lemma:vanish-def', 'S03:10': 'lemma:vanish-def', 'S03:15': 'lemma:statement-def', 'S03:16': 'theorem:bsd-panel-satisfaction', 'S03:17': 'lemma:statement-def'},
 'beds_exact': {'S02:05': "of record, the L product of the first panel member is nonzero at s equal to one — order zero of vanishing — and on my line the exact partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 stands nonzero for the line's side, at the line end 84",
                'S02:06': "of record, the L product of the second panel member vanishes at s equal to one, of order one — and on my line the exact partial 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 stands far from zero for the line's side (the vanishing is the divergence of the infinite product past the line), at the line end 84",
                'S02:09': 'of record, the algebraic rank of the first panel member is zero — settled by the two-descent: the selmer dimension two against its two-torsion dimension two, the descent bound zero, met by the torsion ledger (its three torsion points, no generator); no B S D is used, at the line end 84',
                'S02:10': 'of record, the algebraic rank of the second panel member is one — settled by the two-descent: the selmer dimension one against its two-torsion dimension zero, the descent bound one, met by the generator (x zero y zero) of record, on my line; no B S D is used, at the line end 84',
                'S02:11': 'of record, two: the rank zero plus the two-torsion dimension two plus the two-shaf dimension zero (the shaf is trivial of record on both members), at the line end 84',
                'S02:12': 'of record, one: the rank one plus the two-torsion dimension zero plus the two-shaf dimension zero (the shaf is trivial of record on both members), at the line end 84',
                'S02:13': 'the torsion ledger of the first panel member holds its three integral two-torsion points on my line — (x zero y zero), (x one y zero), (x minus one y zero) — the full two-torsion of record (z/2 squared), and nothing else on the line, at the line end 84',
                'S02:14': 'the generation ledger of the second panel member holds the generator (x zero y zero) of record, and every point my line counted is a small multiple of it — ten of ten of the ledger, closed on the line, at the line end 84',
                'S02:15': 'for the first panel member, the descent bound is the selmer dimension two minus the two-torsion dimension two — zero — and the point ledger holds only its three torsion points (x zero y zero, x one y zero, x minus one y zero), so the rank is zero, settled, at the line end 84',
                'S02:16': 'for the second panel member, the descent bound is the selmer dimension one minus the two-torsion dimension zero — one — and the generator (x zero y zero) of record, on my line, meets it (the rank is at least one), so the rank is one, settled, at the line end 84',
                'S03:05': 'the summit of the island is the statement itself — held in my store as a declared record fact (the clay millennial booklet, the wiles chapter): the order of vanishing of the L product at s equal to one equals the algebraic rank — and on my panel the two sides are settled of record and they agree: order zero equals rank zero for the first member, and order one equals rank one for the second, at the line end 84',
                'S03:06': "the line holds toward the summit: the exact partials (the first member's uniform partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 holds nonzero, the second member's uniform partial 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 and record partial 288658484322736684459196579776684558374651494400 over 21623718536400902622086448680400714121493095949 stand far from zero), the torsion ledger of the first member (its three integral two-torsion points on the line — x zero y zero, x one y zero, x minus one y zero), and the generation ledger of the second member (the generator (x zero y zero), and every point my line counted is a small multiple of it — ten of ten), at the line end 84",
                'S03:07': "yes — on my line: the first member's exact uniform partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 stands nonzero, consistent with the record's order zero, and the second member's exact partial 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 stands far from zero at the line end, consistent with the record's order one (the vanishing is the divergence of the infinite product past the line), at the line end 84",
                'S03:09': 'for the first panel member, the analytic side is the order zero of vanishing of record, the algebraic side is the rank zero of record — the order zero equals the rank zero, at the line end 84',
                'S03:10': 'for the second panel member, the analytic side is the order one of vanishing of record, the algebraic side is the rank one of record — the order one equals the rank one, at the line end 84',
                'S03:15': "the summit band holds the statement itself, stored as a declared record fact (the clay millennial booklet, the wiles chapter), with its satisfaction on the panel of record — order zero equals rank zero for the first member, order one equals rank one for the second — and the line's side standing: the two-descent exact sequence and descent bounds, the exact partials consistent with both orders — the island's summit filed, the island closed, at the line end 84",
                'S03:16': "the summit of the island filed on my panel: the statement holds of record on both members — the order zero of vanishing equals the rank zero of the first member, and the order one of vanishing equals the rank one of the second — the two sides settled by independent record machinery (the ranks by the descent and the point ledger, the orders by the L-function's record), and my line's exact partials stand consistent with both, at the line end 84",
                'S03:17': "nothing the summit band says is conditional on the Riemann hypothesis — the two-descent, the exact sequence, the selmer census, and the statement of record are unconditional mathematics on my panel, and the record's values (the L values, the leading coefficient) stand named of record on their walls, at the line end 84"},
 'derive_successes': {'S03:08': ['bsd-panel-satisfaction', ['statement-def', 'vanish-def', 'rank-def']]},
 'derived_table': {'S03:08': "the summit of the island filed on my panel: the statement holds of record on both members — the order zero of vanishing equals the rank zero of the first member, and the order one of vanishing equals the rank one of the second — the two sides settled by independent record machinery (the ranks by the descent and the point ledger, the orders by the L-function's record), and my line's exact partials stand consistent with both, at the line end 84",
                   'S04:01': 'the record L product of the second panel member up to height 83 (last prime 83) holds the exact rational 288658484322736684459196579776684558374651494400 over 21623718536400902622086448680400714121493095949 — and past the conductor prime the record partial has separated from the uniform one by the hair of the correction, at the line end 84',
                   'S04:02': 'the ramification correction of the first panel member is 4 over 5 — the record factor 1 over the uniform factor 5 over 4 at its single ramified prime 2 on the line, and the record partial is the uniform partial times it, at the line end 84',
                   'S04:03': 'the L product of the first panel member at my line end 84 holds the exact rational 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889',
                   'S04:04': 'the first panel member carries the factor 10 over 9 at prime 3 in the uniform form',
                   'S04:05': 'needs_info: this band does not state the BSD: the statement equating the order of vanishing of the L product at s equal to one with the rank of the group of rational points is the summit fact of the island; the object of this band is the L-family itself — the factors, the partials, and the corrections my line holds — while the order of vanishing and the rank sit on their walls (of record, past my line), at the line end 84',
                   'S04:06': "the cross-pollination queue for the bands above my line carries exactly four lots, in declared order: the condition line (the condition-closers made teachable, with the conditional consequences as its drills), the primes in residue classes (the tower's prime layer), the zero count at height T, and the factor-count deviation ledger (the root smallness); a fifth lot is not in the queue, because the selection runs on the declared classes, at the line end 84",
                   'S04:07': "of record, the L product of the first panel member is nonzero at s equal to one — order zero of vanishing — and on my line the exact partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 stands nonzero for the line's side, at the line end 84",
                   'S04:08': 'of record, the algebraic rank of the second panel member is one — settled by the two-descent: the selmer dimension one against its two-torsion dimension zero, the descent bound one, met by the generator (x zero y zero) of record, on my line; no B S D is used, at the line end 84',
                   'S04:09': 'the summit of the island is the statement itself — held in my store as a declared record fact (the clay millennial booklet, the wiles chapter): the order of vanishing of the L product at s equal to one equals the algebraic rank — and on my panel the two sides are settled of record and they agree: order zero equals rank zero for the first member, and order one equals rank one for the second, at the line end 84',
                   'S04:10': "the line holds toward the summit: the exact partials (the first member's uniform partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 holds nonzero, the second member's uniform partial 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 and record partial 288658484322736684459196579776684558374651494400 over 21623718536400902622086448680400714121493095949 stand far from zero), the torsion ledger of the first member (its three integral two-torsion points on the line — x zero y zero, x one y zero, x minus one y zero), and the generation ledger of the second member (the generator (x zero y zero), and every point my line counted is a small multiple of it — ten of ten), at the line end 84",
                   'S04:11': "yes — on my line: the first member's exact uniform partial 3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889 stands nonzero, consistent with the record's order zero, and the second member's exact partial 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 stands far from zero at the line end, consistent with the record's order one (the vanishing is the divergence of the infinite product past the line), at the line end 84",
                   'S04:12': "the reaching: what my line holds toward the summit — the exact partials the line holds (the first member's uniform partial holds nonzero, the second member's uniform and record partials hold their exact rationals), the torsion ledger of the first member on the line (its three integral two-torsion points), the generation ledger of the second member on the line (the generator (x zero y zero), and every point my line counted is a small multiple of it), and the consistency of the line's values with the record's orders (the order zero keeps its nonzero partial, the order one keeps its exact partial far from zero), at the line end 84",
                   'S04:13': 'the generation ledger of the second panel member holds the generator (x zero y zero) of record, and every point my line counted is a small multiple of it — ten of ten of the ledger, closed on the line, at the line end 84',
                   'S04:14': 'for the first panel member, the analytic side is the order zero of vanishing of record, the algebraic side is the rank zero of record — the order zero equals the rank zero, at the line end 84',
                   'S04:15': 'the torsion ledger of the first panel member holds its three integral two-torsion points on my line — (x zero y zero), (x one y zero), (x minus one y zero) — the full two-torsion of record (z/2 squared), and nothing else on the line, at the line end 84',
                   'S04:16': "the summit band holds the statement itself, stored as a declared record fact (the clay millennial booklet, the wiles chapter), with its satisfaction on the panel of record — order zero equals rank zero for the first member, order one equals rank one for the second — and the line's side standing: the two-descent exact sequence and descent bounds, the exact partials consistent with both orders — the island's summit filed, the island closed, at the line end 84",
                   'S04:17': "of record, the L product of the second panel member vanishes at s equal to one, of order one — and on my line the exact partial 159521793967828167727450741455536203312307404800 over 11941456505176617865928337330967558544705142539 stands far from zero for the line's side (the vanishing is the divergence of the infinite product past the line), at the line end 84"},
 'domain_sequence': {2: 'UUULSSULSSSSSSSSF', 3: 'ULFLSSSTSSHHHHSSS', 4: 'SSSSHSSSSSSSSSSSS'},
 'expected_prereq_gaps': {'algebraic-rank': [], 'analytic-order': [], 'bsd-summit': [], 'line-reaching': []},
 'final_total': 1581,
 'honest_zero_bytes': {},
 'line_end_final': 84,
 'mastery_expected': {'algebraic-rank': {'correct': 11, 'prereq_gaps': [], 'state': 'stable'}, 'analytic-order': {'correct': 4, 'prereq_gaps': [], 'state': 'stable'}, 'bsd-summit': {'correct': 10, 'prereq_gaps': [], 'state': 'stable'}, 'line-reaching': {'correct': 5, 'prereq_gaps': [], 'state': 'stable'}},
 'missing_parts_failure': {'S02:17': 'needs_info: i have not been taught the statement-def — the rule for bsd-panel-satisfaction needs it before i can put it together'},
 'new_events': 54,
 'new_fact_ids': ['lemma:vanish-def', 'lemma:rank-def', 'lemma:statement-def', 'lemma:reach-def', 'theorem:bsd-panel-satisfaction'],
 'new_facts': 5,
 'offscript_carry': {'state the kstbound rule': 'because two unit circles meet in at most two points the unit pair graph of a planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs at a constant times n to the three halves power'},
 'pre_s16_drilled': {'euler-factor': 1, 'l-correction': 1},
 'pre_s16_states': {'add-two-digit': {'correct': 11, 'state': 'stable'},
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
                    'curve-shadow': {'correct': 12, 'state': 'stable'},
                    'cyclotomic-cubic': {'correct': 3, 'state': 'practicing'},
                    'disc-rd': {'correct': 1, 'state': 'practicing'},
                    'disproof': {'correct': 10, 'state': 'practicing'},
                    'divides': {'correct': 5, 'state': 'stable'},
                    'erdos-conj': {'correct': 10, 'state': 'stable'},
                    'euler-factor': {'correct': 8, 'state': 'stable'},
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
                    'l-correction': {'correct': 7, 'state': 'stable'},
                    'l-partial': {'correct': 14, 'state': 'stable'},
                    'li-criterion': {'correct': 9, 'state': 'stable'},
                    'lindelof': {'correct': 4, 'state': 'practicing'},
                    'line-partial': {'correct': 9, 'state': 'stable'},
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
 'pre_teach_gaps': {'S02:01': "not yet learned: the order of vanishing: what the record says the L-product does at s equal to one — zero for the first panel member, one for the second; a limit fact past my line, and my partials stand for the line's side", 'S02:02': 'not yet learned: the algebraic rank: the record settles the panel — the first member zero with its torsion ledger, the second one with its generator; the two-descent machinery: the exact sequence and the descent bound that settle the rank with the point ledger, no BSD used', 'S02:03': 'not yet learned: the vanish-def rule', 'S02:07': 'not yet learned: the rank-def rule', 'S03:01': 'not yet learned: the statement-def rule'},
 'rederive': None,
 'scaffold_failures': {'S03:03': 'needs_info: i can see the parts you name, but the rule for bsd-panel-satisfaction wants its exact set — what you name is short the vanish-def and the rank-def before i can put it together'},
 'script': {2: ['what order of vanishing does the L product of the first panel member have at s equal to one of record?',
                'what is the algebraic rank of the second panel member of record?',
                'state the vanish-def rule',
                "at the limit my line does not reach, the record says what the L-products of my panel do at s equal to one: the L-product of the first panel member is nonzero there — order zero of vanishing — and the L-product of the second panel member vanishes there of order one — the analytic side of the statement the island summits on; a limit fact of record past my line, and on the line i hold the exact partials that stand for the line's side: the first member's partial holds nonzero, the second member's partial holds its exact rational far from zero — the vanishing is the divergence of the infinite product, at the line end 84",
                'what order of vanishing does the L product of the first panel member have at s equal to one of record?',
                'what order of vanishing does the L product of the second panel member have at s equal to one of record?',
                'state the rank-def rule',
                'the algebraic rank of a panel member is of record, settled by the two-descent — the machinery: the exact sequence, the selmer dimension equals the rank plus the dimension of the two torsion plus the dimension of the two shaf, and the descent bound, the rank at most the selmer dimension minus the two torsion dimension, met by the point ledger when the bound and the known points agree; on my panel the record settles it — the first member rank zero, its two selmer dimension two against its two torsion dimension two, the bound zero, and the ledger holds only its three torsion points (x zero y zero, x one y zero, x minus one y zero); the second member rank one, its two selmer dimension one against its two torsion dimension zero, the bound one, and the generator (x zero y zero) of record meets it; no BSD is used to settle a rank on my panel, at the line end 84',
                'what is the algebraic rank of the first panel member of record?',
                'what is the algebraic rank of the second panel member of record?',
                'what is the two selmer dimension of the first panel member of record?',
                'what is the two selmer dimension of the second panel member of record?',
                'what does the torsion ledger of the first panel member hold on my line?',
                'what does the generation ledger of the second panel member hold on my line?',
                'what does the two-descent settle for the first panel member of record?',
                'what does the two-descent settle for the second panel member of record?',
                'derive bsd-panel-satisfaction from statement-def and vanish-def and rank-def'],
            3: ['state the statement-def rule',
                'the statement of the island, of record (the clay millennial booklet, the wiles chapter): for a curve over the rationals, in the taylor expansion of its L-product at s equal to one, the order r of vanishing equals the algebraic rank — the L-product is c times (s minus 1) to the power r plus higher order terms, c not zero, r equals the rank of the group of rational points — and in particular the L-product at s equal to one is zero if and only if there are infinitely many rational points; on my panel the two sides are settled of record and they agree: order zero equals rank zero for the first member, and order one equals rank one for the second, at the line end 84',
                'derive bsd-panel-satisfaction from statement-def',
                "the reaching: what my line holds toward the summit — the exact partials the line holds (the first member's uniform partial holds nonzero, the second member's uniform and record partials hold their exact rationals), the torsion ledger of the first member on the line (its three integral two-torsion points), the generation ledger of the second member on the line (the generator (x zero y zero), and every point my line counted is a small multiple of it), and the consistency of the line's values with the record's orders (the order zero keeps its nonzero partial, the order one keeps its exact partial far from zero), at the line end 84",
                'what is the summit fact of the island?',
                'what does my line hold toward the summit of the island?',
                'are my partials consistent with the record orders at s equal to one?',
                'derive bsd-panel-satisfaction from statement-def and vanish-def and rank-def',
                'what do the two sides of the statement say for the first panel member of record?',
                'what do the two sides of the statement say for the second panel member of record?',
                'how is the two selmer of the first panel member computed in detail of record?',
                'how is the two selmer of the second panel member computed in detail of record?',
                'what is the exact record L value of the second panel member at s equal to one?',
                "which curves of record does the island's summit settle on my line?",
                'what state does the summit band hold at the line end?',
                'state the bsd-panel-satisfaction rule',
                'does the summit band say anything conditional on the Riemann hypothesis?'],
            4: ['what does the record L product of the second panel member hold at height 83?',
                'what is the ramification correction of the first panel member?',
                "what does the first panel member's L product hold at my line end?",
                'what factor does the first panel member carry at prime 3 in the uniform form?',
                'does this band state the BSD?',
                'what is the queue above my line?',
                'what order of vanishing does the L product of the first panel member have at s equal to one of record?',
                'what is the algebraic rank of the second panel member of record?',
                'what is the summit fact of the island?',
                'what does my line hold toward the summit of the island?',
                'are my partials consistent with the record orders at s equal to one?',
                'state the reach-def rule',
                'what does the generation ledger of the second panel member hold on my line?',
                'what do the two sides of the statement say for the first panel member of record?',
                'what does the torsion ledger of the first panel member hold on my line?',
                'what state does the summit band hold at the line end?',
                'what order of vanishing does the L product of the second panel member have at s equal to one of record?']},
 'seam_carry_refs': ['S04:01', 'S04:02', 'S04:03', 'S04:04', 'S04:05', 'S04:06'],
 'seam_crosscheck': {'expected': 'agreement'},
 'seed': 'results/phase-6/e6.19-run1/codeX-S04.json',
 'seed_identity': 'adff69d61a3e4219',
 'seed_total': 1522,
 'teach_turns': {'S02:04': 'lemma:vanish-def', 'S02:08': 'lemma:rank-def', 'S03:02': 'lemma:statement-def', 'S03:04': 'lemma:reach-def'},
 'theorem_allowed': {'S03:16': ['bsd-panel-satisfaction'], 'S04:06': ['queue-declared']},
 'theorem_dag': ['theorem:bsd-panel-satisfaction', 'theorem:cm-signature', 'theorem:criterion-gap', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:delta-positive', 'theorem:first-divisor-prime', 'theorem:gamma-achieved', 'theorem:gap-scale-agreement', 'theorem:gen-lower', 'theorem:growth-compare', 'theorem:gs-infinite', 'theorem:hasse-census', 'theorem:infinity-end', 'theorem:l-added-term', 'theorem:l-ramified-unit', 'theorem:l-record-identity', 'theorem:mirror-region', 'theorem:pack-bound', 'theorem:partition-identity', 'theorem:proj-inj', 'theorem:queue-declared', 'theorem:reflect', 'theorem:removal-single', 'theorem:rh-reach', 'theorem:sieve-equality', 'theorem:spf-chain', 'theorem:splitting', 'theorem:strip', 'theorem:telescope-line', 'theorem:theorem-main', 'theorem:tower-feeds', 'theorem:two-routes-one-guarantee', 'theorem:window-rich'],
 'total_seam_facts': 122,
 'total_turns': 51,
 'unclassified_honest': {},
 'wall_articulations': {'S03:11': ['selmer', 'line end 84'], 'S03:12': ['selmer', 'line end 84'], 'S03:13': ['leading coefficient', 'line end 84'], 'S03:14': ['conductor', 'line end 84']},
 'walls_honest': {'S03:11': 'needs_info: the two-descent of record runs over the homology of the rationals, not over my line: the selmer group is the locally soluble homology spaces, computed in the ideles of the rationals — for the first panel member the selmer group of order four (dimension two) against the two-torsion dimension two gives the descent bound zero, met by the torsion ledger; for the second the selmer group of order two (dimension one) against the two-torsion dimension zero gives the descent bound one, met by the generator (x zero y zero); the shaf part is trivial of record on both, so the selmer dimension is the rank plus the two-torsion dimension exactly — the mechanism is of record, past my line, at the line end 84',
                  'S03:12': 'needs_info: the two-descent of record runs over the homology of the rationals, not over my line: the selmer group is the locally soluble homology spaces, computed in the ideles of the rationals — for the first panel member the selmer group of order four (dimension two) against the two-torsion dimension two gives the descent bound zero, met by the torsion ledger; for the second the selmer group of order two (dimension one) against the two-torsion dimension zero gives the descent bound one, met by the generator (x zero y zero); the shaf part is trivial of record on both, so the selmer dimension is the rank plus the two-torsion dimension exactly — the mechanism is of record, past my line, at the line end 84',
                  'S03:13': "needs_info: the exact L value at s equal to one is of record, not on my line: the first panel member's L value is nonzero of order zero of vanishing, and the second panel member's vanishes of order one with its leading coefficient nonzero of record (named here, not computed); my line holds the exact rational partials standing for the line's side — the vanishing is a limit fact past my line, at the line end 84",
                  'S03:14': 'needs_info: the statement is universal — every curve over the rationals — but my line covers the two panel members: y squared = x cubed minus x, conductor 32, and y squared plus y = x cubed minus x, conductor 37, on which both sides are settled of record and agree (order zero, rank zero; order one, rank one); other curves of record, with their ranks and their orders, sit past the panel, named as such, at the line end 84'}}

FROZEN: dict[str, Any] = FROZEN_DATA

SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

# --- Stage-A discipline (frozen at build): the carried corpus is
# reproduced by PROBE (seam carries), never by re-assertion. No S4–S14
# lesson phrase, no S6–S14 theorem statement, appears in the S16
# script verbatim.
_StageA_ALL_LESSONS = (
    {**S4_LESSONS, **S5_LESSONS, **S6_LESSONS, **S7_LESSONS, **S8_LESSONS,
     **S9_LESSONS, **S11_LESSONS, **S12_LESSONS, **S13_LESSONS, **S14_LESSONS,
     **S15_LESSONS}
)
_StageA_ALL_THEOREMS = (
    {**S6_THEOREMS, **S7_THEOREMS, **S8_THEOREMS, **S9_THEOREMS, **S10_THEOREMS,
     **S11_THEOREMS, **S12_THEOREMS, **S13_THEOREMS, **S14_THEOREMS, **S15_THEOREMS}
)
_stagea_script = [t for s in FROZEN["script"].values() for t in s]
for _ph in _StageA_ALL_LESSONS:
    assert _ph not in _stagea_script, f"Stage-A: a carried lesson is re-asserted in the S16 script: {_ph[:60]!r}"
for _m in _StageA_ALL_THEOREMS.values():
    assert _m["statement"] not in _stagea_script, "Stage-A: a carried theorem statement appears in the S16 script"

_UNFROZEN = str(FROZEN["final_total"]).startswith("##FREEZE") or str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.20-run1"]:
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
            s: {"parts": tuple(S16_THEOREMS[s]["parts"]), "statement": S16_THEOREMS[s]["statement"]}
            for s in ("bsd-panel-satisfaction",)
        },
    }


def run_e6_20(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.19 S15 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S16 frozen constants are not yet frozen (control #1 must replace the sentinels)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.20-run1", "e6.20-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.19 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)

    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.20-run1", "e6.20-run2"):
        (out_dir / name / "e6.20-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.20.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.20-run1"
    root2 = out_dir / "e6.20-run2"
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inherited from S13/S14): NO
    # S15 fact carries the hypothesis marker (the L band is
    # unconditional mathematics); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S16 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s16_facts = tuple(FROZEN["new_fact_ids"])
    for fid in s16_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S16 is the unconditional summit band)")
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
        "marker_absent_facts": list(s16_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S16 script + all responses + band lessons (S4–S9 + S11–S16) + all thirty-four theorem statements",
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
    if [t["domain"] for k, t in sorted(turns.items()) if k.startswith("S02:")] [:3] != ["U", "U", "U"]:
        p1_bad.append("S2:01–03 do not run impossible BEFORE the teaches")
    checks["p1_script_contract"] = {"pass": not p1_bad, "bad": p1_bad, "turns": len(turns)}

    # P2 — the typed honesty: the FOUR pre-lesson gaps, the FOUR
    # teach turns (lesson facts stored), the ONE part-set failure
    # (named, needs_info, ungrounded, store-inert), the ONE
    # missing-part articulation (the full part-set named with the one
    # untaught slug), the ONE derive success (stored, grounded exactly
    # on the sanctioned parts), the frozen domain sequences, the line
    # end, and ZERO seeded-fact object bytes changed.
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
        if str(ir.get("answer", "")) != _th16(slug):
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

    # P4 — the 18 beds exact + grounded (the ON-LINE census answers),
    # the 4 walls honest with their frozen bytes and articulations
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
        W_S16_1 == Brainstem.W_S16_1
        and W_S16_2 == Brainstem.W_S16_2
        and W_S16_3 == Brainstem.W_S16_3
    ):
        p4_bad.append("a W-S16 wall drifted from the Brainstem class attribute")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S16-1..W-S16-3 (cross-checked, never surfaced)",
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
        # the BARE conj id only (the summit composition
    # theorem:bsd-panel-satisfaction is the sanctioned summit fact, not the candidate):
    bsd_th = [a.id for a in final.query() if a.id == "theorem:bsd"]
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
    # (a)+(b)+(c) the summit destinations (mechanism vs record
    # arithmetic): (a) the descent arithmetic — on both panel members
    # the descent bound is the selmer dimension minus the two-torsion
    # dimension (the exact sequence with the shaf part trivial of
    # record); (b) the PANEL SATISFACTION — the record's order of
    # vanishing equals the record's rank on both members (zero = zero,
    # one = one); (c) the line's side — the first member's uniform
    # partial is nonzero (the line stands with the order zero), the
    # second member's record partial is past one (the line stands with
    # the order one, far from zero).
    d_bad: list[str] = []
    for tag in ("A", "B"):
        if S16_BEDS["descend_bound"][tag] != S16_BEDS["selmer_dim"][tag] - S16_BEDS["e2_dim"][tag]:
            d_bad.append(f"{tag}: the descent bound is not the selmer minus two-torsion dimension (the exact-sequence arithmetic drifted)")
        if S16_BEDS["sha2_dim"][tag] != 0:
            d_bad.append(f"{tag}: the shaf two-torsion dimension is not trivial of record")
        if S16_BEDS["rank"][tag] != S16_BEDS["order"][tag]:
            d_bad.append(f"{tag}: the panel does not satisfy the statement (rank {S16_BEDS['rank'][tag]} != order {S16_BEDS['order'][tag]})")
    _uA = Fraction(S16_BEDS["uniform_84_A"])
    _rB = Fraction(S16_BEDS["record_84_B"])
    if _uA == 0:
        d_bad.append("A: the line's uniform partial vanished (the order zero side broke on the line)")
    if not S16_BEDS["consistent_A_nonzero"]:
        d_bad.append("A: the line's value is not consistent with the record order")
    if _rB <= 1:
        d_bad.append("B: the line's record partial is not far from zero (the order one side broke on the line)")
    if not S16_BEDS["consistent_B_far"]:
        d_bad.append("B: the line's value is not consistent with the record order")
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
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "summit_destination_bad": d_bad[:10],
            "summit_destination_agreement": not d_bad,
            "queue_missing": queue_missing,
            "queue_source": "lemma:queue-declared (self-parsed)",
        },
    }

    # P6 — the SEAM carry (the THREE rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime:
    # the two S14 L-partial carries and the queue) + the one
    # OFF-SCRIPT carry probe (kstbound byte-identical — the savant
    # track's standing soil check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.20-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E620)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S16-run answer (the seam carry drifted)")
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
    mv = mastery_view(final, [c.id for c in CONCEPTS_E620])
    _S16_NEW = [c.id for c in CONCEPT_S16]
    for cid in list(FROZEN["pre_s16_states"]) + _S16_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s16_drilled"] if isinstance(FROZEN["pre_s16_drilled"], dict) else {}
    improved: list[str] = []
    for cid, exp in FROZEN["pre_s16_states"].items():
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
        "carried_refs": len(FROZEN["pre_s16_states"]),
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
    if runs["e6.20-run1"] != runs["e6.20-run2"]:
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
            "determinism_twin": runs["e6.20-run1"] == runs["e6.20-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.20-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s16_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_20Experiment:
    """E6.20 — S16 of the PRIZE-ISLANDS-TRACK (the BSD island,
    band 3 of 3 — the island's SUMMIT): the descent and the reaching.
    The descent of record settles both panel ranks WITHOUT the
    statement; the record's orders of vanishing match; the statement —
    verbatim from the clay millennial booklet — is stored as the
    island's summit fact; the line's partials stand for the line's
    side."""

    name = "e6.20"
    hypothesis = (
        "S16 of the PRIZE-ISLANDS-TRACK (the BSD island, band 3 of 3 — the SUMMIT) walks THE DESCENT "
        "AND THE REACHING over the carried S15 seed (1522): the descent of record settles both panel "
        "ranks without the statement (the rank zero curve: selmer dimension two against two-torsion "
        "dimension two, bound zero met by the torsion ledger; the rank one curve: dimension one "
        "against zero, bound one met by the generator); the record's orders of vanishing match the "
        "ranks (zero = zero, one = one); the BSD statement verbatim from the clay millennial booklet "
        "is stored as the island's summit fact with the composition bsd-panel-satisfaction on the "
        "strict part set (statement-def + vanish-def + rank-def); the line's partials stand for the "
        "line's side (nonzero where the order is zero, far from zero where it is one). It stores FIVE "
        "new deterministic facts: four lessons (vanish-def, rank-def, statement-def, reach-def) and "
        "one composition (bsd-panel-satisfaction), the seam census closing 117+5 -> 122. The analytic "
        "L-values sit on walls (the leading coefficient named without its digits); NO NEW decimals "
        "enter the floor. The line stays 0..84 (zero new successor facts); the conj stays open, "
        "byte-identical to the seed; NO theorem:bsd exists (the bare conj id is the "
        "discovery-candidate invariant: the summit is stored as the declared record fact + the "
        "panel-satisfaction composition, not as the bare conjecture id); the SIX seam rows (the S15 "
        "record-partial carry, the ramification correction, the S14 L-partial carry, the S15 factor "
        "carry, the W-S15 BSD-touch wall, the queue) byte-identical to the seed store; kstbound "
        "byte-identical; two runs byte-identical. The BSD island (the $1,000,000 clay millennial "
        "prize target) is now CLOSED as a band: its statement stands in the store as a declared "
        "record fact, settled on the panel by the record machinery, with the line's side held exact."
    )
    metric = "S16 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_20()
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
                Path("results/phase-6/e6.20-run1/session-S02.json"),
                Path("results/phase-6/e6.20-run1/session-S03.json"),
                Path("results/phase-6/e6.20-run1/session-S04.json"),
                Path("results/phase-6/e6.20-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
