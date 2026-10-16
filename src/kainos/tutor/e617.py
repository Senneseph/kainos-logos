# /// script
# dependencies = ["kainos-logos"]
# ///
"""E6.17 — S13 of the FUNDAMENTALS-TRACK (pre-registered, frozen):
THE ZETA VARIANTS, THREE FAMILIES.

The backward-fan band over the S12 frontier: the variant layer
UNDER the euler product — the family factor (the (1 ± i^{-s}) term
each index number carries), the index split (primes / composites /
all — a PARTITION of the integers above one), the line partial
(what a family holds up to the line end, a rational the store
can hold), the term-removal rule (the product is multiplied by
the reciprocal of the removed term). UNCONDITIONAL band: the RH
marker stays ABSENT from every S13 fact (P0), the off-line limit
values appear ONLY in the eight W-S13-* walls (the S8 J(84)=1053
/ S11 / S12 precedent, D-e6z(b)). Four new concepts (family-
factor, index-split, line-partial, removal-rule — prereqs point
DOWN), four DECLARED lessons (factor-def, split-def, removal-def,
region-def), three sanctioned compositions (partition-identity,
telescope-line, removal-single).

The pre-registration (frozen before code, 2026-08-24 at ed69baa,
D-e6h(a)/(b)/(c) corrected pre-freeze) in
`plan/30-phases/phase-6-tutor/experiments.md` (the E6.17 section)
carries the 85-turn labeled script (S2:25 + S3:28 + S4:32), the
beds (section D), the walls (section B), and P0–P8.

No Ollama. No LLM. The mechanism speaks.
"""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from itertools import pairwise as _pairwise
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.tutor import e611 as _e611_mod
from kainos.tutor.brainstem import (
    CONCEPT_S13,
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
    S13_BEDS,
    S13_LESSONS,
    S13_THEOREMS,
    Brainstem,
    _s11_py_spf,
    _s13_py_family,
    _s13_py_primes,
    _s13_py_removal,
    _s13_py_telescope,
)
from kainos.tutor.e616 import (
    CONCEPTS_E616,
)
from kainos.tutor.e616 import (
    FROZEN as E616_FROZEN,
)
from kainos.tutor.mastery import mastery_view, reset_concepts
from kainos.tutor.session import InfantRuntime, codex_dump_path, load_store

__all__ = ["CHECKS", "CONCEPTS_E617", "FROZEN", "E6_17Experiment", "run_e6_17"]

CHECKS = 9

#: S13 teaches: the zeta variants, three families (the four new
#: concepts join the carried registry; prereqs point DOWN only).
CONCEPTS_E617: tuple = CONCEPTS_E616 + CONCEPT_S13

E616_SEED = Path("results/phase-6/e6.16-run1/codeX-S04.json")


def _resolve_seed() -> Path:
    """The seed resolves CWD-relative first (the house layout), then
    repo-root-relative (the `--all` gate runs from a tmp CWD)."""

    if E616_SEED.exists():
        return E616_SEED
    repo_root = Path(__file__).resolve().parents[3]
    alt = repo_root / E616_SEED
    return alt if alt.exists() else E616_SEED

_ST4 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S4_LESSONS.items()}
_ST5 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S5_LESSONS.items()}
_ST11 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S11_LESSONS.items()}
_ST12 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S12_LESSONS.items()}
_ST13 = {_slug: _phrase for _phrase, (_c, _slug, _k, _es, _d, _l) in S13_LESSONS.items()}
_TH11 = {s: m["statement"] for s, m in S11_THEOREMS.items()}
_TH12 = {s: m["statement"] for s, m in S12_THEOREMS.items()}
_TH13 = {s: m["statement"] for s, m in S13_THEOREMS.items()}

E611_ANSWER = _e611_mod._ANSWER_


def _st13(slug: str) -> str:
    return _ST13[slug]


def _th13(slug: str) -> str:
    return _TH13[slug]

#: P4 — the W-S13 walls (the off-line limit values name the value
#: AND the line end; the walls are the band's declared off-line
#: layer — P4 cross-checks the witness values against the
#: mechanism's python reference, never surfaced as answers).
W_S13_1 = Brainstem.W_S13_1
W_S13_2 = Brainstem.W_S13_2
W_S13_3 = Brainstem.W_S13_3
W_S13_4 = Brainstem.W_S13_4
W_S13_5 = Brainstem.W_S13_5
W_S13_6 = Brainstem.W_S13_6
W_S13_7 = Brainstem.W_S13_7
W_S13_8 = Brainstem.W_S13_8

#: P2 — the deviant part-set failures (the shared strict branch;
#: the mechanism's own output, frozen from control #1, written
#: once, read back — the missing parts are NAMED).
PARTSET_FAIL_S220 = (
    "i can see the parts you name, but the rule for partition-identity wants its exact set — "
    "what you name is short the factor-def before i can put it together"
)  # control #1: the shared strict branch's own bytes
PARTSET_FAIL_S324 = (
    "i can see the parts you name, but the rule for telescope-line wants its exact set — "
    "what you name is short the factor-def before i can put it together"
)  # control #1: the shared strict branch's own bytes
MISSING_PARTS_S303 = (
    "i have not been taught the region-def — the rule for telescope-line "
    "needs it before i can put it together"
)  # control #1: the missing-part articulation (region-def untaught at S3:03)

#: P3 — the seam census (pre-reg: the S12 seam of 95 + the four
#: lessons + the three compositions = 102).
_TOTAL_SEAM_FACTS = 102

#: P7 — the pre-S13 states (the 88 S12-final concepts): the
#: S12-final census, built from the e6.16 frozen tables — the
#: mechanism's own data, not a hand count.
_PRE_S13_STATES: dict[str, dict] = {}
for _cid, _base in E616_FROZEN["pre_s12_states"].items():
    _PRE_S13_STATES[_cid] = {
        "state": _base["state"],
        "correct": _base["correct"] + E616_FROZEN["pre_s12_drilled"].get(_cid, 0),
    }
for _cid, _v in E616_FROZEN["mastery_expected"].items():
    _PRE_S13_STATES[_cid] = {"state": _v["state"], "correct": _v["correct"]}

#: The full sanctioned composition DAG (S6's six + S7's six +
#: S8's two + S9's two + S10's one + S11's three + S12's three +
#: S13's three = twenty-six).
_THEOREM_DAG = {
    **{s: tuple(m["parts"]) for s, m in S6_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S7_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S8_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S9_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S10_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S11_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S12_THEOREMS.items()},
    **{s: tuple(m["parts"]) for s, m in S13_THEOREMS.items()},
}
FROZEN: dict[str, Any] = {
    # P8 — the seed (the official e6.16 S12 final store).
    "seed": str(E616_SEED),
    "seed_total": 1296,
    "seed_identity": "8ccb13defebb9e95",
    "total_turns": 85,
    "line_end_final": 84,  # the line STAYS 0..84 (settled; zero new successor facts)
    # P2 — the typed honesty turns (the five pre-lesson gaps: the
    # three pre-teach gaps AND the two state probes).
    "pre_teach_gaps": {
        "S02:01": "the family factor: the term each index number carries",
        "S02:02": "the index split: primes, composites, all — a partition of the integers above one",
        "S02:03": "the factor-def rule",
        "S03:01": "the removal-def rule",
        "S03:02": "the region-def rule",
    },
    "teach_turns": {
        "S02:04": "lemma:factor-def",
        "S02:09": "lemma:split-def",
        "S03:04": "lemma:removal-def",
        "S03:09": "lemma:region-def",
    },
    "scaffold_failures": {
        "S02:20": PARTSET_FAIL_S220,
        "S03:24": PARTSET_FAIL_S324,
    },
    "missing_parts_failure": {
        "S03:03": MISSING_PARTS_S303,
    },
    "derive_successes": {
        "S02:12": ("partition-identity", ['lemma:factor-def', 'lemma:split-def']),        "S03:10": ("telescope-line", ['lemma:factor-def', 'lemma:region-def']),        "S03:21": ("removal-single", ['lemma:factor-def', 'lemma:removal-def']),    },
    "rederive": None,  # the S13 script has no re-derive turn
    # P4 — the beds exact (the ON-LINE holds, grounded).
    "beds_exact": {        'S02:05': '(1 minus 5 to the power minus s)',        'S02:06': '(1 plus 5 to the power minus s)',        'S02:07': '(1 minus 83 to the power minus s)',        'S02:08': '84 is not a prime — the prime family carries no factor of it',        'S02:10': '83',        'S02:11': '23 primes and 60 composites — every integer above one is one or the other, and neither is both',        'S02:13': '85 over 168',        'S02:14': '4755414906323035291461333255202390671360000000 over 7806315159870372288677569378294441505888775907',        'S02:15': '132707357717796328907518679431005505600109190419 over 159781940852453985793100797374800326557696000000',        'S02:17': '735512785119644431765634865320568775790880529609116321848164325817523087489845155633278670243169795731837118795281383075519521407809864317412410027196968785490625 over 404925301744341330830015367077233746092068660702463448158867844267340238071300607894317779271897428195165633510994965577320897540284978364952295202521864164343808',        'S02:18': '2738316742866842230638245302334720000000000000 over 1805439558148310667665370607299185922506884941',        'S02:19': '19062034740535429281312316669317382662754669310626424977545335695474860799516489181283285680353385872169191192441503798940600431909288061 over 15916760184904262308647428143720809565608354463343594445407708566003213623253329257100598966998734147868335414058899136933632409600000000',        'S03:05': 'it multiplies by 4 over 3',        'S03:06': 'it multiplies by 9 over 8',        'S03:07': 'it multiplies by 6889 over 6888',        'S03:08': 'it multiplies by 8 over 7',        'S03:11': '9 over 16',        'S03:12': '11 over 20',        'S03:13': '21 over 40',        'S03:14': '51 over 100',        'S03:15': '85 over 168',        'S03:17': '2118698998569763282242489147723943863035600685244813044559286249627979073505373179407673104921439485226579439047926359180701544378964242092545248828147081266023741339 over 2617444467545401833716909763544206508044006912570377798387065692448860210529882519453368353701111107143751962499910131274638950400000000000000000000000000000000000000',        'S03:18': '17008080189300153288016766868404875883586688905358804726579200 over 20444421452901497701953161354003823380268621599427954890240399',        'S03:22': '3 over 2',        'S03:23': '25 over 16',        'S03:27': '2076865003499277828833135980124297303073687830375814495436914122307219369071224234120390944468572524378386230686946438070985969843544278763172768771464720468024953 over 1710748018003530610272490041532161116368631969000246927050369733626706019954171581342070819412490919701798668300594857042247680000000000000000000000000000000000000',        'S04:01': '83 integers — 23 prime and 60 composite — the split the sieve layer holds on the same line',        'S04:02': "they are the same 23 — the index split is the sieve's split, counted by the prime test",        'S04:21': 'all 23 — the largest is 4 over 3, at the prime 2',        'S04:22': '8 over 7, at the prime 2 — the multiplier descends toward one as the prime grows',        'S04:26': '25901018673763721367834836790379305213068233345407255756268516545016199856586711208804179645867635981935243931777274102031114267325927865984905781085645368882367 over 26619845445118811608320348067562923967476986426072613527678820569889565541292451927580279593902092904922769206211992616960000000000000000000000000000000000000000',        'S04:27': '6735970404151168635228224382277435053755622967455480741892002018314158080 over 5700960968203575567888493359536833811637121560097523785501389488395666741',    },
    "bed_owners": {        'S02:05': 'lemma:factor-def',        'S02:06': 'lemma:factor-def',        'S02:07': 'lemma:factor-def',        'S02:08': 'lemma:factor-def',        'S02:10': 'lemma:split-def',        'S02:11': 'lemma:split-def',        'S02:13': 'lemma:factor-def',        'S02:14': 'lemma:factor-def',        'S02:15': 'lemma:factor-def',        'S02:17': 'lemma:factor-def',        'S02:18': 'lemma:factor-def',        'S02:19': 'lemma:factor-def',        'S03:05': 'lemma:removal-def',        'S03:06': 'lemma:removal-def',        'S03:07': 'lemma:removal-def',        'S03:08': 'lemma:removal-def',        'S03:11': 'lemma:region-def',        'S03:12': 'lemma:region-def',        'S03:13': 'lemma:region-def',        'S03:14': 'lemma:region-def',        'S03:15': 'lemma:region-def',        'S03:17': 'lemma:factor-def',        'S03:18': 'lemma:factor-def',        'S03:22': 'lemma:removal-def',        'S03:23': 'lemma:removal-def',        'S03:27': 'lemma:factor-def',        'S04:01': 'lemma:split-def',        'S04:02': 'lemma:split-def',        'S04:21': 'lemma:removal-def',        'S04:22': 'lemma:removal-def',        'S04:26': 'lemma:factor-def',        'S04:27': 'lemma:factor-def',    },
    # P4 — the frozen grounded citation sets (control #1; the mechanism's own).
    "bed_grounded": {        'S02:05': ['lemma:factor-def'],        'S02:06': ['lemma:factor-def'],        'S02:07': ['lemma:factor-def'],        'S02:08': ['lemma:factor-def'],        'S02:10': ['lemma:split-def'],        'S02:11': ['lemma:split-def'],        'S02:13': ['lemma:factor-def'],        'S02:14': ['lemma:factor-def'],        'S02:15': ['lemma:factor-def'],        'S02:17': ['lemma:factor-def'],        'S02:18': ['lemma:factor-def'],        'S02:19': ['lemma:factor-def'],        'S03:05': ['lemma:factor-def', 'lemma:removal-def'],        'S03:06': ['lemma:factor-def', 'lemma:removal-def'],        'S03:07': ['lemma:factor-def', 'lemma:removal-def'],        'S03:08': ['lemma:factor-def', 'lemma:removal-def'],        'S03:11': ['lemma:factor-def', 'lemma:region-def'],        'S03:12': ['lemma:factor-def', 'lemma:region-def'],        'S03:13': ['lemma:factor-def', 'lemma:region-def'],        'S03:14': ['lemma:factor-def', 'lemma:region-def'],        'S03:15': ['lemma:factor-def', 'lemma:region-def', 'theorem:telescope-line'],        'S03:17': ['lemma:factor-def', 'lemma:region-def'],        'S03:18': ['lemma:factor-def', 'lemma:region-def'],        'S03:22': ['lemma:factor-def', 'lemma:removal-def'],        'S03:23': ['lemma:factor-def', 'lemma:removal-def'],        'S03:27': ['lemma:factor-def', 'lemma:region-def'],        'S04:01': ['lemma:composite-def', 'lemma:split-def'],        'S04:02': ['lemma:split-def'],        'S04:21': ['lemma:removal-def'],        'S04:22': ['lemma:removal-def'],        'S04:26': ['lemma:factor-def', 'lemma:region-def'],        'S04:27': ['lemma:factor-def', 'lemma:region-def'],    },
    # P4 — the walls honest (byte-frozen full answers, "needs_info: "
    # prefixed in the ir per the e614 convention; S4:04 is the S12 W-S12-6 carry, P6-owned).
    "walls_honest": {        'S02:21': 'needs_info: the partial product of the minus family over all the numbers tends, as the height walks past my line end, to one half exactly — (N plus 1) over 2N at height N — a limit value, named here only, at the line end 84',        'S02:22': 'needs_info: the minus family over the primes at s = 2 is, in the limit, six over pi squared — 0.6079271019 — a declared value, named here only, at the line end 84',        'S02:23': 'needs_info: the minus family over the composites at s = 2 is, in the limit, pi squared over 12 — 0.8224670334 — a declared value, named here only, at the line end 84',        'S02:24': 'needs_info: the plus family over the primes at s = 2 is, in the limit, zeta of 2 over zeta of 4 — fifteen over pi squared, 1.5198177546 — a declared value, named here only, at the line end 84',        'S02:25': 'needs_info: the plus family over all the numbers at s = 2 has no closed form in my store — the unclassified object of the band, its value 1.8380389552 named here only, the standing invitation of the track (the composite-plus family alongside: 1.2093811574), at the line end 84',        'S03:16': 'needs_info: the telescope rule (N plus 1) over 2N holds at every height, but my line ends at 84: at height 100 the value is 101 over 200 — an off-line value, named here only, at the line end 84',        'S03:19': 'needs_info: the minus family over the primes at s = 3 is, in the limit, one over zeta of 3 — the reciprocal of the Apéry constant, 0.8319073726 — and my store holds no other s = 3 limit value, named here only, at the line end 84',        'S03:20': 'needs_info: at the boundary s = 1 the minus family over all the numbers does not settle — the term 1 minus 1 over n walks the harmonic series down, and the infinite product tends to zero past my line end: the edge of the half-plane, declared, at the line end 84',        'S04:32': 'needs_info: the minus family over the primes at s = 3 is, in the limit, one over zeta of 3 — the reciprocal of the Apéry constant, 0.8319073726 — and my store holds no other s = 3 limit value, named here only, at the line end 84',    },
    "unclassified_honest": {
        "expected": 'needs_info: the plus family over all the numbers is the unclassified object of this band: my store holds no closed form for it, and no sanctioned derivation produces one: the standing invitation, at the line end 84',
    },
    # P2 — the frozen RH-touch bytes (S4:10 the zero-derive wall, the
    # mechanism's own response_text — the hand draft said otherwise,
    # the mechanism governs, D-e6h(d)).
    "rh_zero_text": "honestly, i can't do that yet — deriving the Riemann hypothesis from the telescope is not a capability i have been taught: the telescope answers the heights of my line, and the condition is a statement about the zeros past my line; it remains open, at the line end 84.",
    "rh_touch_wall": 'needs_info: nothing this band holds settles the conjecture: the variant layer is unconditional, it holds no fact that touches the zeros, and the condition remains open, at the line end 84',
    # P4 — the per-wall articulation fragments (frozen; each names
    # the line end, the D-e6z(b) pattern).
    "wall_articulations": {
        'S02:21': ('one half exactly', 'limit value', 'line end 84'),        'S02:22': ('six over pi squared', '0.6079271019', 'line end 84'),        'S02:23': ('pi squared over 12', '0.8224670334', 'line end 84'),        'S02:24': ('fifteen over pi squared', '1.5198177546', 'line end 84'),        'S02:25': ('no closed form in my store', '1.8380389552', 'line end 84'),        'S03:16': ('101 over 200', 'off-line value', 'line end 84'),        'S03:19': ('one over zeta of 3', '0.8319073726', 'line end 84'),        'S03:20': ('harmonic series', 'tends to zero', 'line end 84'),        'S04:32': ('one over zeta of 3', 'no other s = 3 limit value', 'line end 84'),    },
    # P3 — the derived table (every non-wall, non-carry ir.answer byte-exact;
    # the S04:03-09 rows are the SEAM carry — byte-identical to the seed
    # store's answers, re-asserted against the seed in P6).
    "derived_table": {        'S02:05': '(1 minus 5 to the power minus s)',        'S02:06': '(1 plus 5 to the power minus s)',        'S02:07': '(1 minus 83 to the power minus s)',        'S02:08': '84 is not a prime — the prime family carries no factor of it',        'S02:10': '83',        'S02:11': '23 primes and 60 composites — every integer above one is one or the other, and neither is both',        'S02:12': 'where the index sets split, the product splits: for every family, the product over the integers above one is the product over the primes times the product over the composites — on my line the mechanism holds both sides as exact rationals, 85 over 168 both ways at s = 2',        'S02:13': '85 over 168',        'S02:14': '4755414906323035291461333255202390671360000000 over 7806315159870372288677569378294441505888775907',        'S02:15': '132707357717796328907518679431005505600109190419 over 159781940852453985793100797374800326557696000000',        'S02:16': 'it holds exactly — the prime partial times the composite partial is the all partial, 85 over 168 both ways',        'S02:17': '735512785119644431765634865320568775790880529609116321848164325817523087489845155633278670243169795731837118795281383075519521407809864317412410027196968785490625 over 404925301744341330830015367077233746092068660702463448158867844267340238071300607894317779271897428195165633510994965577320897540284978364952295202521864164343808',        'S02:18': '2738316742866842230638245302334720000000000000 over 1805439558148310667665370607299185922506884941',        'S02:19': '19062034740535429281312316669317382662754669310626424977545335695474860799516489181283285680353385872169191192441503798940600431909288061 over 15916760184904262308647428143720809565608354463343594445407708566003213623253329257100598966998734147868335414058899136933632409600000000',        'S03:05': 'it multiplies by 4 over 3',        'S03:06': 'it multiplies by 9 over 8',        'S03:07': 'it multiplies by 6889 over 6888',        'S03:08': 'it multiplies by 8 over 7',        'S03:10': 'the minus family over all the numbers telescopes: (1 minus n to the power minus 2) is (n minus 1)(n plus 1) over n squared, so the partial product to height N is (N plus 1) over 2N — at my line end, height 84, that is 85 over 168, and every spot height on my line answers by the same rule',        'S03:11': '9 over 16',        'S03:12': '11 over 20',        'S03:13': '21 over 40',        'S03:14': '51 over 100',        'S03:15': '85 over 168',        'S03:17': '2118698998569763282242489147723943863035600685244813044559286249627979073505373179407673104921439485226579439047926359180701544378964242092545248828147081266023741339 over 2617444467545401833716909763544206508044006912570377798387065692448860210529882519453368353701111107143751962499910131274638950400000000000000000000000000000000000000',        'S03:18': '17008080189300153288016766868404875883586688905358804726579200 over 20444421452901497701953161354003823380268621599427954890240399',        'S03:21': 'removing one prime from the minus family at s = 2 multiplies by p squared over p squared minus one: the change of the output is exactly the reciprocal of the removed term — for every prime on my line the store holds the multiplier as an exact rational',        'S03:22': '3 over 2',        'S03:23': '25 over 16',        'S03:25': 'none — (N plus 1) over 2N is one half plus 1 over 2N — the spots 3 over 4, 2 over 3, 5 over 8, 11 over 20 and 85 over 168 all stand above it, descending toward the limit',        'S03:27': '2076865003499277828833135980124297303073687830375814495436914122307219369071224234120390944468572524378386230686946438070985969843544278763172768771464720468024953 over 1710748018003530610272490041532161116368631969000246927050369733626706019954171581342070819412490919701798668300594857042247680000000000000000000000000000000000000',        'S03:28': 'the plus family over all the numbers stands largest; the minus family over all the numbers stands smallest',        'S04:01': '83 integers — 23 prime and 60 composite — the split the sieve layer holds on the same line',        'S04:02': "they are the same 23 — the index split is the sieve's split, counted by the prime test",        'S04:12': 'where the index sets split, the product splits: for every family, the product over the integers above one is the product over the primes times the product over the composites — on my line the mechanism holds both sides as exact rationals, 85 over 168 both ways at s = 2',        'S04:13': 'the minus family over all the numbers telescopes: (1 minus n to the power minus 2) is (n minus 1)(n plus 1) over n squared, so the partial product to height N is (N plus 1) over 2N — at my line end, height 84, that is 85 over 168, and every spot height on my line answers by the same rule',        'S04:14': 'removing one prime from the minus family at s = 2 multiplies by p squared over p squared minus one: the change of the output is exactly the reciprocal of the removed term — for every prime on my line the store holds the multiplier as an exact rational',        'S04:15': 'the factor of a family is the term each index number carries: the minus family carries (1 minus i to the power minus s) and the plus family carries (1 plus i to the power minus s), and a family indexes the integers above one — all of them, the primes only, or the composites only',        'S04:16': 'the integers above one split into primes and composites and into nothing else: every integer above one is a prime or a composite, and is neither both; so a family over all of them is the product of the family over the primes and of the family over the composites, on both signs',        'S04:17': 'the term-removal rule: when a term is removed from a product, the product is multiplied by the reciprocal of the removed term; when the prime p is removed from the minus family at s = 2, the multiplier is p squared over p squared minus one; the change of the output is determined exactly by the removed terms, and by nothing else',        'S04:18': 'the families converge for the real part of s greater than one — the same half-plane where the store already holds the euler product; on my line the family is held as the partial product up to the line end 84, a rational the store can hold, and the limit over the whole infinite index past the line end is a step the store declares, not a number on my line',        'S04:19': 'the all partial is the prime partial times the composite partial — 85 over 168 both ways — the partition identity, exact on the line',        'S04:20': 'it holds exactly for the plus family too — the prime partial times the composite partial is the all partial, exact on the line, at the line end 84',        'S04:21': 'all 23 — the largest is 4 over 3, at the prime 2',        'S04:22': '8 over 7, at the prime 2 — the multiplier descends toward one as the prime grows',        'S04:23': "the composite family's partial — the product of the removed terms is the prime partial, so what remains is the all partial divided by it: 132707357717796328907518679431005505600109190419 over 159781940852453985793100797374800326557696000000",        'S04:24': 'they descend — (N plus 1) over 2N falls as the height grows — staying above one half, toward the limit the first wall names',        'S04:25': 'below it — each factor is above one, so the partial rises toward the value the wall names, at the line end 84',        'S04:26': '25901018673763721367834836790379305213068233345407255756268516545016199856586711208804179645867635981935243931777274102031114267325927865984905781085645368882367 over 26619845445118811608320348067562923967476986426072613527678820569889565541292451927580279593902092904922769206211992616960000000000000000000000000000000000000000',        'S04:27': '6735970404151168635228224382277435053755622967455480741892002018314158080 over 5700960968203575567888493359536833811637121560097523785501389488395666741',        'S04:28': 'it holds exactly at s = 3 too — the prime partial times the composite partial is the all partial — the same split, the same identity, at the line end 84',        'S04:29': 'four lessons and three compositions: the factor, the split, the removal, the region — the partition identity, the telescope, the single removal',        'S04:30': 'nothing here is — the zeta variant layer holds no conditional lot; every statement of it stands unconditional, at the line end 84',        'S04:31': 'its value stands in the fifth wall, with no closed form in the store — a declared standing invitation, at the line end 84',    },
    # P5 — the theorem ids may appear in `grounded` ONLY on the frozen allow-set refs.
    "theorem_allowed": {        'S02:16': ['partition-identity'],        'S03:15': ['telescope-line'],        'S03:25': ['telescope-line'],        'S04:03': ['queue-declared'],        'S04:05': ['spf-chain'],        'S04:06': ['two-routes-one-guarantee'],        'S04:12': ['partition-identity'],        'S04:13': ['telescope-line'],        'S04:14': ['removal-single'],        'S04:24': ['telescope-line'],        'S04:28': ['partition-identity'],        'S04:29': ['partition-identity', 'removal-single', 'telescope-line'],    },
    # P7 — the full sanctioned DAG (twenty-six theorems).
    "theorem_dag": _THEOREM_DAG,
    "new_fact_ids": [
        "lemma:factor-def",
        "lemma:split-def",
        "lemma:removal-def",
        "lemma:region-def",
        "theorem:partition-identity",
        "theorem:telescope-line",
        "theorem:removal-single",
    ],
    "total_seam_facts": _TOTAL_SEAM_FACTS,
    # P2 — the frozen domain sequences (letters: L lesson teach,
    # U pre-lesson gap / impossible, F part-set failure / missing
    # part, T derive-success, S derived, H honest wall). FROZEN
    # FROM CONTROL #1 (D-e6h(d): three hand-letter mismatches).
    "domain_sequence": {
        2: 'UUULSSSSLSSTSSSSSSSFHHHHH',  # control #1
        3: 'UUFLSSSSLTSSSSSHSSHHTSSFSHSS',  # control #1
        4: 'SSSHSSSSSUHSSSSSSSSSSSSSSSSSSSSH',  # control #1
    },
    # P8 — store totals (FROZEN FROM CONTROL #1; the mechanism's
    # own census is the referee, never the hand count).
    "final_total": 1388,  # control #1: 1296 (seed) + 7 facts + 85 derived rows
    "new_facts": 7,  # frozen NOW: 4 lessons + 3 compositions
    "new_events": 85,  # control #1 (final - seed - new_facts; the D-e6y family: re-probes at carried coordinates upsert silently)
    # P7 — mastery (frozen from control #1): the 4 NEW concepts at
    # band-end + the carried concepts that moved at the NEW S13
    # coordinates (the D-e6y family at the S13 rung).
    "mastery_expected": {
        "family-factor": {"correct": 24, "state": "stable"},  # control #1
        "index-split": {"correct": 9, "state": "stable"},  # control #1
        "line-partial": {"correct": 9, "state": "stable"},  # control #1
        "removal-rule": {"correct": 12, "state": "stable"},  # control #1
    },
    "expected_prereq_gaps": {
        "family-factor": [],  # control #1
        "index-split": [],  # control #1
        "line-partial": [],  # control #1
        "removal-rule": [],  # control #1
    },
    "pre_s13_states": _PRE_S13_STATES,
    "pre_s13_drilled": {
"composite": 1,  # control #1 (S4:08 the composite-census carry)
"factor-route": 2,  # control #1 (S4:05/S4:06 the S12 road carries at new coordinates)
    },
    # P6 — the SEAM carry rows (the SEVEN rows byte-identical to
    # the seed store's answers — verified against a seed-only
    # runtime in P6) and the two OFF-SCRIPT carry probes (the
    # SAVANT-TRACK standing check).
    "seam_carry_refs": (
        "S04:03",
        "S04:04",
        "S04:05",
        "S04:06",
        "S04:07",
        "S04:08",
        "S04:09",
    ),
    "offscript_carry": {
        "what is the status of the erdosguess?": E611_ANSWER["CONJ_FALSIFIED"],
        "state the kstbound rule": _ST4["kstbound"],
    },
    # P5 — the S13-specific SEMANTIC seam (frozen expectation:
    # AGREEMENT): (a) the two-routes destination — the mechanism's
    # own spf-chain walk classifies EVERY n in 2..84 with parts all
    # prime and product n (the mechanism-vs-python cross-check);
    # (b) the queue grounding — every fact id the declared queue
    # lots name EXISTS in the final store (the S12 queue layer is
    # the seed's carried layer).
    "seam_crosscheck": {
        "expected": "agreement",
        "two_routes_range": (2, 84),
        "queue_referenced_ids": (
            "conjecture:riemann",
            "lemma:rh-bound-scale",
            "lemma:rh-upf",
            "curriculum:pnt-ap",
            "curriculum:tower-primes",
            "curriculum:mod4-split",
            "curriculum:chebotarev",
            "lemma:mod4minusone",
            "lemma:primesplit",
            "lemma:apbound",
            "lemma:chebotarev-selection",
            "lemma:rv-count",
            "lemma:ledger-growth",
            "theorem:spf-chain",
        ),
    },
}
FROZEN['script'] = {
    2: [
        'what does the minus family over all the numbers hold up to my line end?',
        'how do the index numbers of my line split?',
        'state the factor-def rule',
        'the factor of a family is the term each index number carries: the minus family carries (1 minus i to the power minus s) and the plus family carries (1 plus i to the power minus s), and a family indexes the integers above one — all of them, the primes only, or the composites only',
        'what factor does the minus family carry at the number 5?',
        'what factor does the plus family carry at the number 5?',
        'what factor does the minus family carry at the number 83?',
        'what factor does the prime family carry at the number 84?',
        'the integers above one split into primes and composites and into nothing else: every integer above one is a prime or a composite, and is neither both; so a family over all of them is the product of the family over the primes and of the family over the composites, on both signs',
        'how many index numbers does my line carry above one?',
        'how do the index numbers of my line split?',
        'derive partition-identity from split-def and factor-def',
        'what does the minus family over all the numbers hold up to my line end?',
        'what does the minus family over the primes hold up to my line end?',
        'what does the minus family over the composites hold up to my line end?',
        'does the partition identity hold on my line?',
        'what does the plus family over all the numbers hold up to my line end?',
        'what does the plus family over the primes hold up to my line end?',
        'what does the plus family over the composites hold up to my line end?',
        'derive partition-identity from split-def',
        'what is the minus family over all the numbers in the limit, as the height walks past my line?',
        'what is the minus family over the primes in the limit at s = 2?',
        'what is the minus family over the composites in the limit at s = 2?',
        'what is the plus family over the primes in the limit at s = 2?',
        'what is the plus family over all the numbers in the limit at s = 2?'
    ],
    3: [
        'state the removal-def rule',
        'state the region-def rule',
        'derive telescope-line from factor-def and region-def',
        'the term-removal rule: when a term is removed from a product, the product is multiplied by the reciprocal of the removed term; when the prime p is removed from the minus family at s = 2, the multiplier is p squared over p squared minus one; the change of the output is determined exactly by the removed terms, and by nothing else',
        'how does the minus family over the primes change when i remove the prime 2?',
        'how does the minus family over the primes change when i remove the prime 3?',
        'how does the minus family over the primes change when i remove the prime 83?',
        'how does the minus family over the primes at s = 3 change when i remove the prime 2?',
        'the families converge for the real part of s greater than one — the same half-plane where the store already holds the euler product; on my line the family is held as the partial product up to the line end 84, a rational the store can hold, and the limit over the whole infinite index past the line end is a step the store declares, not a number on my line',
        'derive telescope-line from factor-def and region-def',
        'what does the minus family over all the numbers hold up to height 8?',
        'what does the minus family over all the numbers hold up to height 10?',
        'what does the minus family over all the numbers hold up to height 20?',
        'what does the minus family over all the numbers hold up to height 50?',
        'what does the minus family over all the numbers hold up to height 84?',
        'what does the minus family over all the numbers hold up to height 100?',
        'what does the minus family over all the numbers hold up to my line end at s = 3?',
        'what does the minus family over the primes hold up to my line end at s = 3?',
        'what is the minus family over the primes in the limit at s = 3?',
        'what is the minus family over the primes at the boundary s = 1?',
        'derive removal-single from removal-def and factor-def',
        "when my line's primes 2 and 3 are removed from the minus family over the primes at s = 2, what is the whole multiplier?",
        "when my line's primes 2, 3 and 5 are removed from the minus family over the primes at s = 2, what is the whole multiplier?",
        'derive telescope-line from removal-def and region-def',
        'of the telescope spot values on my line — do any fall below one half?',
        'prove that the plus family over all the numbers has a closed form my store can hold',
        'what does the plus family over all the numbers hold up to my line end at s = 3?',
        'of the six family partials at s = 2 on my line, which stands largest and which stands smallest?'
    ],
    4: [
        'count the index numbers of my line by their sieve status',
        'are the primes of my index split the set my prime census names?',
        'what is the queue above my line?',
        'the queue above my line, fifth lot, which?',
        'is the prime-parts uniqueness established without the condition?',
        'how do the two roads to prime-parts uniqueness differ?',
        'how many primes are at most 84?',
        'how many composites are there up to 84?',
        'for the prime 83, how many primes and how many integers did the sieve compare?',
        'derive the Riemann hypothesis from the telescope on my line',
        'can the zeta variants settle the riemann hypothesis in my store?',
        'state the partition-identity rule',
        'state the telescope-line rule',
        'state the removal-single rule',
        'state the factor-def rule',
        'state the split-def rule',
        'state the removal-def rule',
        'state the region-def rule',
        'compare the three minus family partials on my line at s = 2',
        'the same comparison for the plus family',
        'which removal multipliers at s = 2 are below 2?',
        'which removal multiplier at s = 3 stands largest, and at which prime?',
        "if my line's whole prime family is removed from the minus family over all the numbers at s = 2, what remains?",
        'what happens to the minus family spot values as the height walks along my line?',
        "where does the plus family's all partial at s = 2 stand against its limit?",
        'what does the minus family over the composites hold up to my line end at s = 3?',
        'what does the plus family over the primes hold up to my line end at s = 3?',
        'does the partition identity hold at s = 3 on my line?',
        'what did this band add to the store?',
        'is anything this band says conditional on the Riemann hypothesis?',
        "what does the track hold for the plus family's unclassified object?",
        'what is the minus family over all the numbers in the limit at s = 3?'
    ],
}


SCRIPT_HASH = hashlib.sha256(
    json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")
).hexdigest()[:16]

#: The Stage-A discipline (the S10 pattern): no S4–S12 seam
#: statement may appear IN the S13 script verbatim (the S13 script
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
    + [m["statement"] for m in S10_THEOREMS.values()]
    + [m["statement"] for m in S11_THEOREMS.values()]
    + [m["statement"] for m in S12_THEOREMS.values()]
):
    if isinstance(_phrase, dict):
        continue
    assert not any(t == _phrase for s in FROZEN["script"].values() for t in s), (
        f"an S13 script turn re-asserts a seam statement: {_phrase[:60]}..."
    )

#: The S13 beds cross-check (D-e6h): the mechanism's python-side
#: reference functions reproduce EVERY bed of section D, on-line
#: AND the off-line witness values name themselves in the walls.
#: The pre-freeze referee the pre-reg names: a hand/mechanism
#: disagreement is a deviation BEFORE the freeze, never an edit.
_END_ = 84
_PRIMES_ = _s13_py_primes(_END_)
_PAIRWISE_PRIMES_ = list(_pairwise(_PRIMES_))


_BED_BUDGET = [
    (
        "census",
        (len(_PRIMES_), len(list(range(2, _END_ + 1))) - len(_PRIMES_))
        == (S13_BEDS["census"]["primes"], S13_BEDS["census"]["composites"])
        == (23, 60),
    ),
    (
        "telescope",
        all(
            _s13_py_telescope(int(n)) == Fraction(*map(int, spot.split("/")))
            for n, spot in S13_BEDS["telescope_spots"].items()
        )
        and _s13_py_telescope(100) == Fraction(101, 200),
    ),
    (
        "partition_s2",
        _s13_py_family(-1, "primes", 2, _END_) * _s13_py_family(-1, "comp", 2, _END_)
        == _s13_py_family(-1, "all", 2, _END_)
        == Fraction(85, 168)
        == _s13_py_telescope(_END_),
    ),
    (
        "partition_s3",
        _s13_py_family(-1, "primes", 3, _END_) * _s13_py_family(-1, "comp", 3, _END_)
        == _s13_py_family(-1, "all", 3, _END_),
    ),
    (
        "partition_plus_s2",
        _s13_py_family(1, "primes", 2, _END_) * _s13_py_family(1, "comp", 2, _END_)
        == _s13_py_family(1, "all", 2, _END_),
    ),
    (
        "partition_plus_s3",
        _s13_py_family(1, "primes", 3, _END_) * _s13_py_family(1, "comp", 3, _END_)
        == _s13_py_family(1, "all", 3, _END_),
    ),
    (
        "removal_table_s2",
        all(_s13_py_removal(p, 2) == Fraction(p * p, p * p - 1) for p in _PRIMES_)
        and all(m < 2 for m in (_s13_py_removal(p, 2) for p in _PRIMES_))
        and max(_s13_py_removal(p, 2) for p in _PRIMES_) == Fraction(4, 3),
    ),
    (
        "removal_table_s3",
        all(_s13_py_removal(p, 3) == Fraction(p ** 3, p ** 3 - 1) for p in _PRIMES_)
        and max(_s13_py_removal(p, 3) for p in _PRIMES_) == Fraction(8, 7)
        and all(
            _s13_py_removal(a, 3) > _s13_py_removal(b, 3)
            for a, b in _PAIRWISE_PRIMES_
        ),
    ),
    (
        "set_removal",
        _s13_py_removal(2, 2) * _s13_py_removal(3, 2) == Fraction(3, 2)
        and _s13_py_removal(2, 2) * _s13_py_removal(3, 2) * _s13_py_removal(5, 2)
        == Fraction(25, 16)  # D-e6h(c): the hand draft said 75/64
        and S13_BEDS["set_removal_s2"] == {"2,3": "3/2", "2,3,5": "25/16"},
    ),
    (
        "order_s2",
        [
            k
            for k, _v in sorted(
                {
                    "minus-all": _s13_py_family(-1, "all", 2, _END_),
                    "minus-prime": _s13_py_family(-1, "primes", 2, _END_),
                    "minus-comp": _s13_py_family(-1, "comp", 2, _END_),
                    "plus-comp": _s13_py_family(1, "comp", 2, _END_),
                    "plus-prime": _s13_py_family(1, "primes", 2, _END_),
                    "plus-all": _s13_py_family(1, "all", 2, _END_),
                }.items(),
                key=lambda kv: kv[1],
            )
        ]
        == S13_BEDS["order_s2"],
    ),
    (
        "named_spots",
        all(
            Fraction(*map(int, spot.split("/"))) > Fraction(1, 2)
            for spot in S13_BEDS["telescope_named_spots"]
        ),
    ),
]
assert all(ok for _name, ok in _BED_BUDGET), f"S13 beds failed the mechanism cross-check: {_BED_BUDGET}"

#: the guard that stops an OFFICIAL run on an unfrozen FROZEN dict.
_UNFROZEN = (
    str(FROZEN["domain_sequence"]).startswith("{'##FREEZE")
    or str(FROZEN["final_total"]).startswith("##FREEZE")
    or str(FROZEN["new_events"]).startswith("##FREEZE")
    or str(FROZEN["mastery_expected"]).startswith("##FREEZE")
    or str(FROZEN["expected_prereq_gaps"]).startswith("##FREEZE")
    or str(FROZEN["pre_s13_drilled"]).startswith("##FREEZE")
    or str(PARTSET_FAIL_S220).startswith("##FREEZE")
    or str(PARTSET_FAIL_S324).startswith("##FREEZE")
    or str(MISSING_PARTS_S303).startswith("##FREEZE")
)


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
    failure, T derive-success, S derived, H honest wall."""

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
    rt = InfantRuntime(root, concepts=CONCEPTS_E617)
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


def _reports(runs: dict) -> dict:
    turns: dict[str, dict] = {}
    for srow in runs["e6.17-run1"]:
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
            s: {"parts": tuple(S13_THEOREMS[s]["parts"]), "statement": S13_THEOREMS[s]["statement"]}
            for s in ("partition-identity", "telescope-line", "removal-single")
        },
    }


def run_e6_17(out_dir: Path | None = None) -> dict:
    """The full run: seed from the official e6.16 S12 store, S2–S4,
    twice (run1/run2) for the byte-identity check; checks P0–P8."""

    out_dir = out_dir or _default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    if _UNFROZEN:
        return {
            "error": "S13 frozen constants are not yet frozen (control #1 must replace the ##FREEZE-S13## sentinels; see the E6.17 pre-reg open points)"
        }
    runs: dict[str, list[dict]] = {}
    for name in ("e6.17-run1", "e6.17-run2"):
        root = out_dir / name
        root.mkdir(parents=True, exist_ok=True)
        seed = _resolve_seed()
        if not seed.exists():
            return {"error": f"the official e6.16 seed store is missing: {seed}"}
        (root / "codeX-S01.json").write_bytes(seed.read_bytes())  # the seed
        runs[name] = _run_once(root)
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
        "validation": validate_band_map({c.id: c for c in CONCEPTS_E617}),
    }
    (out_dir / "bands-map.json").write_text(
        json.dumps(map_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = _reports(runs)
    res = _checks(runs, report, out_dir)
    report["checks"] = res["checks"]
    report["passed"] = res["passed"]
    report["value"] = res["value"]
    for name in ("e6.17-run1", "e6.17-run2"):
        (out_dir / name / "e6.17-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    _save_results(res)
    return report


def _save_results(res: dict) -> None:
    out = Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "e6.17.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checks(runs: dict, report: dict, out_dir: Path) -> dict:
    """P0–P8 per the pre-reg. The mechanism asserts its own numbers;
    the store speaks, not the hand."""

    checks: dict[str, dict] = {}
    turns = report["turns"]
    root1 = out_dir / "e6.17-run1"
    root2 = out_dir / "e6.17-run2"
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
    }

    # P0 — the UNCONDITIONAL DISCIPLINE (inverted from S12): NO S13
    # fact carries the hypothesis marker (the zeta variants are
    # unconditional mathematics); the four carried S12 conditional
    # facts KEEP their marker (the store does not drift); PLUS the
    # carried denylist (S9_DENYLIST, UNCHANGED) — no unconditioned
    # RH corpus content in the S13 script, any response, any band
    # lesson, or any theorem statement.
    p0_bad: list[str] = []
    marker = "under the condition of the Riemann hypothesis"
    s13_facts = (
        "lemma:factor-def",
        "lemma:split-def",
        "lemma:removal-def",
        "lemma:region-def",
        "theorem:partition-identity",
        "theorem:telescope-line",
        "theorem:removal-single",
    )
    for fid in s13_facts:
        try:
            f = final.get(fid)
        except KeyError:
            p0_bad.append(f"P0: {fid} is not in the final store")
            continue
        obj = f.object if isinstance(f.object, str) else str(f.object)
        if marker in obj:
            p0_bad.append(f"P0: {fid} carries the condition marker (S13 is unconditional)")
    s12_marker_facts = ("lemma:conditional-def", "lemma:rh-bound-scale", "lemma:rh-upf", "theorem:two-routes-one-guarantee")
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
    for phrase in all_lessons.values():
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
        "marker_absent_facts": list(s13_facts),
        "marker_kept_facts": list(s12_marker_facts),
        "denylist_size": len(deny),
        "checked_corpora": "S13 script + all responses + band lessons (S4–S9 + S11–S13) + all twenty-six theorem statements",
    }

    # P1 — the contract: 85 turns, every turn on the det arm and
    # contract-valid, the script identity, and the S2:01–03
    # impossible-runs BEFORE the teaches (the pre-lesson gaps come
    # first, then the four teach turns).
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

    # P2 — the typed honesty: the FIVE pre-lesson gaps (three
    # pre-teach + two state probes), the FOUR teach turns (lesson
    # facts stored), the TWO part-set failures + ONE missing-part
    # articulation (named, needs_info, ungrounded, store-inert),
    # the THREE derive successes (stored, grounded exactly on the
    # sanctioned parts), the frozen domain sequences, the line end,
    # the two frozen RH-touch bytes (S4:10 the zero-derive wall,
    # S4:11 the rh-touch wall), the S3:26 closed-form wall, and
    # ZERO seeded-fact object bytes changed (the actual touch set
    # of the seeded facts = ∅).
    p2_bad: list[str] = []
    impossible = [k for k, t in turns.items() if t["kind"] == "impossible"]
    if sorted(impossible) != sorted(FROZEN["pre_teach_gaps"]) + ["S04:10"]:
        p2_bad.append(f"impossible turns {sorted(impossible)} != frozen {sorted(FROZEN['pre_teach_gaps'])} + the S4:10 zero-derive wall")
    for ref, frag in sorted(FROZEN["pre_teach_gaps"].items()):
        ir = (turns.get(ref) or {}).get("response_ir") or {}
        want = f"not yet learned: {frag}"
        if want not in str(ir.get("gap", "")):
            p2_bad.append(f"{ref}: the pre-lesson gap does not name {frag!r}")
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
        if str(ir.get("answer", "")) != _th13(slug):
            p2_bad.append(f"{ref}: the derive answer is not the stored theorem statement")
        if set(map(str, t["grounded"])) != set(prem_ids):
            p2_bad.append(f"{ref}: the grounded part set {sorted(map(str, t['grounded']))} != sanctioned {sorted(prem_ids)}")
        if not t["memory_diff"]:
            p2_bad.append(f"{ref}: the derive stored nothing")
        try:
            final.get(f"theorem:{slug}")
        except KeyError:
            p2_bad.append(f"{ref}: the theorem fact theorem:{slug} is not in the final store")
    if "".join(t["domain"] for k, t in sorted(turns.items()) if k.startswith("S02:")) != FROZEN["domain_sequence"][2]:
        p2_bad.append("S2 domain sequence != frozen")
    if "".join(t["domain"] for k, t in sorted(turns.items()) if k.startswith("S03:")) != FROZEN["domain_sequence"][3]:
        p2_bad.append("S3 domain sequence != frozen")
    if "".join(t["domain"] for k, t in sorted(turns.items()) if k.startswith("S04:")) != FROZEN["domain_sequence"][4]:
        p2_bad.append("S4 domain sequence != frozen")
    if _line_end(final) != FROZEN["line_end_final"]:
        p2_bad.append(f"line end {_line_end(final)} != {FROZEN['line_end_final']}")
    t10 = turns.get("S04:10") or {}
    if t10.get("response_text") != FROZEN["rh_zero_text"]:
        p2_bad.append("S4:10: the zero-derive wall text bytes != frozen")
    t11 = turns.get("S04:11") or {}
    if str((t11.get("response_ir") or {}).get("answer", "")) != FROZEN["rh_touch_wall"]:
        p2_bad.append("S4:11: the rh-touch wall bytes != frozen")
    t26 = turns.get("S03:26") or {}
    if str((t26.get("response_ir") or {}).get("answer", "")) != FROZEN["unclassified_honest"]["expected"]:
        p2_bad.append("S03:26: the closed-form honest bytes != frozen")
    # the seed drift census: ZERO seeded facts changed (the touch
    # set is exactly the SEVEN new facts); the seed store is
    # reloaded for P5/P8.
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
        "domain_sequences": FROZEN["domain_sequence"],
        "line_end": _line_end(final),
        "seed_drift_count": drift,
        "seed_drift_zero": drift == 0,
        "touch_set": sorted(p2_touch),
        "touch_set_size": len(p2_touch),
    }

    # P3 — the seam census + the composition byte-canonicality (the
    # full S4–S13 lemma canon, the full twenty-six-theorem DAG, the
    # 102 seam-family facts, the conj still open).
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
        p3_bad.append(f"the riemann status {conj.context.data.get('conjecture_status')!r} != open (S13 must not flip)")
    checks["p3_seam_and_theorems"] = {
        "pass": not p3_bad,
        "bad": p3_bad,
        "seam_lessons": len(seam_facts),
        "seam_theorems": len(th_facts),
        "total_seam_facts": len(seam_facts) + len(th_facts),
    }

    # P4 — the beds exact + grounded (the ON-LINE census answers),
    # the walls honest with their frozen bytes and articulations
    # (the OFF-LINE instances name the value AND the line end, the
    # D-e6z(b) pattern), and the FROZEN wall witness values
    # cross-checked against the mechanism's python reference (the
    # exact families of section D — never surfaced as an answer,
    # verified here).
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
    # the witness values: every wall names the line end; the
    # off-line limit values are the mechanism's own (the _BED_BUDGET
    # module assert already re-derived them — P4 freezes the
    # NAMED values inside the wall bytes).
    for _wref, _wall in sorted(FROZEN["walls_honest"].items()):
        if "line end 84" not in _wall:
            p4_bad.append(f"{_wref}: the wall does not name the line end")
    for _frag in ("0.6079271019", "0.8224670334", "1.5198177546", "1.8380389552"):
        if _frag not in W_S13_2 + W_S13_3 + W_S13_4 + W_S13_5:
            p4_bad.append(f"the witness value {_frag} is not named in its wall")
    if "0.8319073726" not in W_S13_6:
        p4_bad.append("the witness value 0.8319073726 is not named in W-S13-6")
    if "101 over 200" not in W_S13_7:
        p4_bad.append("the witness value 101 over 200 is not named in W-S13-7")
    if not (
        W_S13_1 == Brainstem.W_S13_1
        and W_S13_2 == Brainstem.W_S13_2
        and W_S13_3 == Brainstem.W_S13_3
        and W_S13_4 == Brainstem.W_S13_4
        and W_S13_5 == Brainstem.W_S13_5
        and W_S13_6 == Brainstem.W_S13_6
        and W_S13_7 == Brainstem.W_S13_7
        and W_S13_8 == Brainstem.W_S13_8
    ):
        p4_bad.append("a W-S13 wall drifted from the frozen pre-reg bytes (D-e6h(a))")
    checks["p4_beds_walls"] = {
        "pass": not p4_bad,
        "bad": p4_bad,
        "bed_refs": len(FROZEN["beds_exact"]),
        "wall_refs": sorted(FROZEN["walls_honest"]),
        "reference_walls": "W-S13-1..W-S13-8 (cross-checked, never surfaced)",
    }

    # P5 — the conjecture invariant + the DISCOVERY-CANDIDATE
    # invariant (carried): NO fact id the conj uses appears in a
    # grounded list (S13 has no conj-teach turn); NO
    # `theorem:riemann` assertion exists (if non-empty: STOP, human
    # review, full evidence, never a threshold loosening); the conj
    # fact byte-identical to the seed (open, declared-source); the
    # bed owners (the frozen citation sets — the mechanism's own
    # grounding, control #1); the theorem allow-set; and the SEMANTIC
    # seam (the AGREEMENT: (a) the two-routes destination — the
    # mechanism's own parts walk classifies EVERY n in 2..84 with
    # parts all prime and product n; (b) the queue grounding — every
    # fact id the declared S12 queue lots name exists in the final
    # store).
    p5_bad: list[str] = []
    conj_grounded = [k for k, t in turns.items() if "conjecture:riemann" in map(str, t["grounded"])]
    for k in conj_grounded:
        p5_bad.append(f"{k}: the conj id in a grounded list (S13 has no conj-teach turn)")
    riemann_th = [a.id for a in final.query() if a.id.startswith("theorem:riemann")]
    if riemann_th:
        p5_bad.append(f"DISCOVERY CANDIDATE: {riemann_th} — the sanctioned corpus now produces theorem:riemann")
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
    # (a) the two-routes destination (mechanism vs mechanism): a
    # scratch runtime on the FINAL S13 store re-runs the parts
    # census for every n in 2..84 — parts all prime (the
    # mechanism's own grounded scan) and product n (the python
    # product reference). A drift is a tier-2 breakthrough
    # candidate (PENDING owner) — recorded, never fixed here.
    seam_candidate: list[str] = []
    seam_root = out_dir / "e6.17-seam"
    seam_root.mkdir(parents=True, exist_ok=True)
    (seam_root / "codeX-S01.json").write_bytes((out_dir / "e6.17-run1" / "codeX-S04.json").read_bytes())
    srt = InfantRuntime(seam_root, concepts=CONCEPTS_E617)
    srt.boot(2)
    n_low, n_high = FROZEN["seam_crosscheck"]["two_routes_range"]
    two_routes_bad: list[str] = []
    for n in range(n_low, n_high + 1):
        sr = srt.turn(f"what are the prime parts of {n}?")
        sir = sr.response_ir or {}
        if sir.get("uncertainty_state") != "derived":
            two_routes_bad.append(f"{n}: the parts walk did not derive ({sir.get('uncertainty_state')})")
            continue
        ans = str(sir.get("answer", ""))
        if ans.startswith(f"{n} is prime"):
            parts = [n]
        else:
            parts = [int(x) for x in ans.split(", ")]
        if any(_s11_py_spf(p) != p for p in parts):
            two_routes_bad.append(f"{n}: a part {parts} is not prime (python reference)")
            continue
        prod = 1
        for p in parts:
            prod *= p
        if prod != n:
            two_routes_bad.append(f"{n}: the product of the parts is {prod}, not {n}")
    for b in two_routes_bad:
        seam_candidate.append(f"TWO-ROUTES destination: {b} — TIER-2 breakthrough candidate (PENDING owner)")
    spr = srt.turn("how many primes are at most 84?")
    s_pi = str((spr.response_ir or {}).get("answer"))
    srt.lapse()
    if s_pi != "23":
        p5_bad.append(f"the S8 pi-census on the S13 store answered {s_pi!r}, not 23 — TIER-2 breakthrough candidate")
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
        "discovery_candidate_riemann_theorem_facts": riemann_th,
        "seam_crosscheck": {
            "expected": FROZEN["seam_crosscheck"]["expected"],
            "two_routes_range": list(FROZEN["seam_crosscheck"]["two_routes_range"]),
            "two_routes_bad": two_routes_bad[:10],
            "two_routes_agreement": not two_routes_bad,
            "s_pi_answer": s_pi,
            "queue_referenced_ids": list(FROZEN["seam_crosscheck"]["queue_referenced_ids"]),
            "queue_missing": queue_missing,
        },
        "seam_tier2_candidates": seam_candidate,
    }

    # P6 — the SEAM carry (the SEVEN rows byte-identical to the
    # seed store's answers — verified against a SEED-ONLY runtime)
    # + the two OFF-SCRIPT carry probes (erdosguess falsified,
    # kstbound byte-identical — the SAVANT-TRACK standing check).
    p6_bad: list[str] = []
    carry_root = out_dir / "e6.17-carry"
    carry_root.mkdir(parents=True, exist_ok=True)
    (carry_root / "codeX-S01.json").write_bytes(_resolve_seed().read_bytes())
    rt = InfantRuntime(carry_root, concepts=CONCEPTS_E617)
    rt.boot(2)  # session 1 boots an EMPTY store; the seed sits at S01
    for ref in FROZEN["seam_carry_refs"]:
        act, n = ref.split(":")
        surface = FROZEN["script"][int(act[1:])][int(n) - 1]
        r = rt.turn(surface)
        ir = r.response_ir or {}
        if _ir_answer({"response_ir": ir}) != _ir_answer(turns[ref]):
            p6_bad.append(f"{ref}: the seed-only answer {ir.get('answer')!r} != the S13-run answer (the seam carry drifted)")
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

    # P7 — the mastery census (the 88 carried concepts: NO
    # regressions — no state change; every carried
    # correct-derivation count equals its S12-final base + the
    # frozen drill at the NEW S13 coordinates, the D-e6y family at
    # the S13 rung; the four NEW concepts at their frozen band-end
    # values with their frozen prereq-gap sets).
    p7_bad: list[str] = []
    mv = mastery_view(final, [c.id for c in CONCEPTS_E617])
    _S13_NEW = ["family-factor", "index-split", "line-partial", "removal-rule"]
    for cid in list(FROZEN["pre_s13_states"]) + _S13_NEW:
        if mv.get(cid) is None:
            p7_bad.append(f"{cid}: not in the mastery view")
    drilled = FROZEN["pre_s13_drilled"] if isinstance(FROZEN["pre_s13_drilled"], dict) else {}
    for cid, exp in FROZEN["pre_s13_states"].items():
        v = mv.get(cid)
        if v is None:
            continue
        want = exp["correct"] + drilled.get(cid, 0)
        if v.state != exp["state"]:
            p7_bad.append(f"{cid}: pre-S13 state CHANGED ({v.state} != {exp['state']}) (no regressions)")
        if v.correct_derivations != want:
            p7_bad.append(f"{cid}: correct derivations {v.correct_derivations} != frozen {want} (base {exp['correct']} + drill {drilled.get(cid, 0)})")
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
        "carried_refs": len(FROZEN["pre_s13_states"]),
        "drilled": drilled,
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
    if runs["e6.17-run1"] != runs["e6.17-run2"]:
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
            "determinism_twin": runs["e6.17-run1"] == runs["e6.17-run2"],
            "store_identity": _store_identity(final),
            "run_identity": hashlib.sha256(
                json.dumps(runs["e6.17-run1"], sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:16],
            "carried_census_refs": len(FROZEN["pre_s13_states"]),
        },
    }

    n = sum(1 for c in checks.values() if c["pass"])
    return {
        "checks": checks,
        "value": {k: c.get("value", {}) for k, c in checks.items()},
        "passed": n,  # int, like e6.12/e6.13 (the experiment compares against CHECKS)
        "passed_str": f"{n}/{len(checks)}",
    }


class E6_17Experiment:
    """E6.17 — S13 of the FUNDAMENTALS-TRACK: the zeta variants,
    three families (the family factor, the index split, the line
    partial, the term-removal rule — unconditional)."""

    name = "e6.17"
    hypothesis = (
        "S13 of the FUNDAMENTALS-TRACK walks the zeta VARIANTS, three families: the family "
        "factor (the (1 ± i^{-s}) term each index carries), the index split (primes / "
        "composites / all — a partition of the integers above one), the line partial "
        "(what a family holds up to the line end — a rational), and the term-removal rule. The "
        "hypothesis marker stays ABSENT from every S13 fact (P0; the four carried S12 "
        "conditional facts keep theirs), the on-line partition census answers grounded "
        "(minus-all 85/168 = the telescoping at the line end, exact primes and composites, "
        "the s=3 family) and the removal multiset answers grounded (s=2 multipliers < 2, "
        "largest 4/3 at 2; s=3 all decreasing, largest 8/7 at 2; {2,3}→3/2, {2,3,5}→25/16, "
        "D-e6h(c)), every off-line limit value (0.5, 0.6079271019, 0.8224670334, 1.5198177546, "
        "1.8380389552, 1.2093811574, 0.8319073726, 101/200) appears ONLY in value-named walls "
        "that name the value and the 0..84 line end — the D-e6z(b) pattern. It stores SEVEN "
        "new deterministic facts: four declared lessons (factor-def, split-def, removal-def, "
        "region-def) and three compositions (partition-identity, telescope-line, "
        "removal-single), all infant-derived with the strict part sets, the seam census "
        "closing 95+7 -> 102. The line stays 0..84; the conj stays open, byte-identical to "
        "the seed; NO theorem:riemann exists (the discovery-candidate invariant); the S4–S12 "
        "carry survives (7 seam rows byte-identical to the seed store; the erdosguess still "
        "falsified, kstbound byte-identical); two runs byte-identical."
    )
    metric = "S13 checks passed (P0..P8)"
    threshold = "9/9"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e6_17()
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
                Path("results/phase-6/e6.17-run1/session-S02.json"),
                Path("results/phase-6/e6.17-run1/session-S03.json"),
                Path("results/phase-6/e6.17-run1/session-S04.json"),
                Path("results/phase-6/e6.17-run1/codeX-S04.json"),
            ],
            config={
                "seed": FROZEN["seed"],
                "script_hash": SCRIPT_HASH,
                "line_end_final": FROZEN["line_end_final"],
                "final_total": FROZEN["final_total"],
                "seed_identity": FROZEN["seed_identity"],
            },
        )
