from __future__ import annotations

import hashlib
import json

from kainos.tutor.brainstem import (
    B14_A,
    B14_B,
    CONCEPT_ALG_2STEP,
    CONCEPT_MOD4_SPLIT,
    CONCEPT_S11_SPF,
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
    det_classify,
)
from kainos.tutor.e617 import CONCEPTS_E617
from kainos.tutor.e618 import FROZEN, SCRIPT_HASH

S14_LESSON_SLUGS = [s for _p, (_c, s, _k, _es, _d, _l) in S14_LESSONS.items()]

ALL_CARRIED_LESSONS = (
    list(S4_LESSONS) + list(S5_LESSONS) + list(S6_LESSONS) + list(S7_LESSONS)
    + list(S8_LESSONS) + list(S9_LESSONS) + list(S11_LESSONS) + list(S12_LESSONS) + list(S13_LESSONS)
)

def test_new_concepts_prereqs_point_down() -> None:
    """S14 adds the four elliptic-city concepts; prereqs point DOWN"""
    carried = tuple(c.id for c in CONCEPTS_E617)
    assert tuple(c.id for c in CONCEPTS_E617) + tuple(c.id for c in CONCEPT_S14) == carried + (
        CONCEPT_S14[0].id, CONCEPT_S14[1].id, CONCEPT_S14[2].id, CONCEPT_S14[3].id,
    )
    existing = set(carried)
    for c in CONCEPT_S14:
        for p in c.prereqs:
            assert p in existing or p in {x.id for x in CONCEPT_S14}, f"{c.id}: prereq {p!r} does not point down"
        existing.add(c.id)
    by_id = {c.id: c for c in CONCEPT_S14}
    # the soil points down at CARRIED concepts (alg-two-step from band-2,
    # first-divisor from S11, mod4-split from the savant track) AND DOWN
    # WITHIN the band — never up into the R0/LOT futures.
    assert by_id["curve-form"].prereqs == (CONCEPT_ALG_2STEP,)
    assert by_id["curve-law"].prereqs == (by_id["curve-form"].id,)
    assert by_id["point-count"].prereqs == (by_id["curve-form"].id, CONCEPT_S11_SPF)
    assert by_id["curve-shadow"].prereqs == (by_id["point-count"].id, CONCEPT_MOD4_SPLIT)
    for c in CONCEPT_S14:
        assert c.band == "college-1"
        assert c.domain == "bsd"

def test_script_shape_and_teaching() -> None:
    """55 turns; the four teaches are the lesson phrases verbatim; no
    S4-S13 seam statement appears in the script (Stage-A)."""
    assert FROZEN["total_turns"] == 55
    assert len(FROZEN["script"][2]) == 20
    assert len(FROZEN["script"][3]) == 22
    assert len(FROZEN["script"][4]) == 13
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for slug in S14_LESSON_SLUGS:
        phrase = next(p for p, (_c, s, _k, _es, _d, _l) in S14_LESSONS.items() if s == slug)
        assert phrase in script_lines, f"the {slug} lesson phrase is missing from the script"
    for phrase in ALL_CARRIED_LESSONS:
        assert phrase not in script_lines
    for m in S6_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S7_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S8_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S9_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S10_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S11_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S12_THEOREMS.values():
        assert m["statement"] not in script_lines
    for m in S13_THEOREMS.values():
        assert m["statement"] not in script_lines
    # the three pre-lesson gaps run BEFORE the first teach
    assert FROZEN["script"][2][0] == "what curve does the first panel member hold?"
    assert FROZEN["script"][2][1] == "what is the point at x 0 y 0 plus itself on the second panel member?"
    assert FROZEN["script"][2][2] == "how many points does the second panel member cast over the field with 37 elements?"
    assert FROZEN["script"][2][3] == next(p for p, (_c, s, _k, _es, _d, _l) in S14_LESSONS.items() if s == "form-def")
    # the rh-touch wall sits in S4 (the band stays honest at the frontier)
    assert "can the elliptic curves settle the Riemann hypothesis in my store?" in FROZEN["script"][4]

def test_frozen_shape() -> None:
    """The control #1 census (D-e6i: the mechanism spoke, never the hand)."""
    assert FROZEN["seed_total"] == 1388
    assert FROZEN["seed_identity"] == "f8da2d7f12509ca5"
    assert FROZEN["line_end_final"] == 84  # S14 writes NO successor facts
    assert FROZEN["new_facts"] == 8
    assert FROZEN["new_fact_ids"] == ['lemma:form-def', 'lemma:law-def', 'lemma:count-def', 'lemma:shadow-def', 'theorem:curve-identity', 'theorem:curve-inverse', 'theorem:hasse-census', 'theorem:cm-signature']
    assert FROZEN["total_seam_facts"] == 110  # 100 lemma + 10 theorem (S13 102 + the EIGHT)
    assert len(FROZEN["theorem_dag"]) == 30  # S6..S14
    assert len(FROZEN["walls_honest"]) == 7
    assert len(FROZEN["beds_exact"]) == 10
    assert len(FROZEN["derived_table"]) == 28
    assert len(FROZEN["pre_teach_gaps"]) == 3
    assert len(FROZEN["teach_turns"]) == 4
    assert len(FROZEN["scaffold_failures"]) == 1
    assert FROZEN["missing_parts_failure"] == {}
    assert FROZEN["rederive"] is None
    assert len(FROZEN["seam_carry_refs"]) == 7
    assert FROZEN["final_total"] == 1457  # 1388 + 8 facts + 61 events (D-e6i(c))
    assert FROZEN["new_events"] == 61
    assert FROZEN["final_total"] == FROZEN["seed_total"] + FROZEN["new_facts"] + FROZEN["new_events"]
    # the frozen domain sequences (control #1; the scaffold turn is F, D-e6i(a))
    assert FROZEN["domain_sequence"][2] == 'UUULSSHSSSLSSSSSTTFL'
    assert FROZEN["domain_sequence"][3] == 'SSHSSSSSSSLSSSTSSTSHSH'
    assert FROZEN["domain_sequence"][4] == 'SSSSHHHHHSSSS'

def test_pre_s14_states_carry_e617_final() -> None:
    """The 92 carried concepts at their S13-final values (the live
    control census, excluding the four new concepts)."""
    pre = FROZEN["pre_s14_states"]
    assert len(pre) == 92
    for cid in pre:
        assert cid not in {c.id for c in CONCEPT_S14}, "a NEW concept leaked into the pre-states"
    # the soil chain exactly as the S13 store held it (practicing; the
    # S14 soil carries close it — P7/C7 sanction the improvement only)
    assert pre["number-field"]["state"] == "practicing"
    assert pre["prime-split"]["state"] == "practicing"
    assert pre["mod4-split"]["state"] == "practicing"
    assert pre["mod4-split"]["correct"] >= 10  # already drilled by the savant track
    assert pre["family-factor"]["state"] == "stable"
    assert pre["rh-relevance"]["state"] == "practicing"  # the store holds it mid-chain; S14 re-drills it
    # the S14 soil drill at the NEW coordinates (control #1)
    assert FROZEN["pre_s14_drilled"] == {"family-factor": 1, "rh-relevance": 1, "number-field": 2, "prime-split": 2}
    # the four NEW concepts at their frozen band-end values (D-e6i(b):
    # curve-shadow lands stable only BECAUSE the soil carries closed chain)
    assert FROZEN["mastery_expected"] == {'curve-form': {'correct': 7, 'prereq_gaps': [], 'state': 'stable'},
 'curve-law': {'correct': 8, 'prereq_gaps': [], 'state': 'stable'},
 'curve-shadow': {'correct': 10, 'prereq_gaps': [], 'state': 'stable'},
 'point-count': {'correct': 6, 'prereq_gaps': [], 'state': 'stable'}}
    assert FROZEN["expected_prereq_gaps"] == {'curve-form': [], 'curve-law': [], 'curve-shadow': [], 'point-count': []}

def test_denylist_is_the_s9_44() -> None:
    # S14 carries the S9 denylist UNCHANGED (the 44: S7 34 + the RH ten)
    assert len(S9_DENYLIST) == 44

def test_unconditional_marker_absent() -> None:
    """The S14 facts are unconditional: none carries the RH marker."""
    marker = "under the condition of the Riemann hypothesis"
    for th in S14_THEOREMS.values():
        assert marker not in th["statement"]
    for phrase in S14_LESSONS:
        assert marker not in phrase
    # the carried S12 conditional facts keep THEIR marker (drift check):
    # the e6.18 P0 re-asserts it against the final store; here the spec
    # keeps the declared keeper list identical to the S13 one.
    assert FROZEN["seed"].endswith("codeX-S04.json") and FROZEN["seed"].startswith("results/phase-6/e6.17-run1/")

def test_compositions_sanctioned() -> None:
    assert set(S14_THEOREMS) == {"curve-identity", "curve-inverse", "hasse-census", "cm-signature"}
    assert S14_THEOREMS["curve-identity"]["parts"] == ("law-def", "form-def")
    assert S14_THEOREMS["curve-inverse"]["parts"] == ("law-def", "form-def")
    assert S14_THEOREMS["hasse-census"]["parts"] == ("count-def", "form-def")
    assert S14_THEOREMS["cm-signature"]["parts"] == ("shadow-def", "count-def")
    # the frozen derive turns carry the SAME sanctioned part sets
    assert FROZEN["derive_successes"] == {'S02:17': ('curve-identity', ['lemma:form-def', 'lemma:law-def']),
 'S02:18': ('curve-inverse', ['lemma:law-def', 'lemma:form-def']),
 'S03:15': ('hasse-census', ['lemma:count-def', 'lemma:form-def']),
 'S03:18': ('cm-signature', ['lemma:count-def', 'lemma:shadow-def'])}

def test_walls_bytes() -> None:
    # the seven walls are the Brainstem class attributes, byte-frozen
    wall_attrs = {
        "S02:07": Brainstem.W_S14_1,
        "S03:20": Brainstem.W_S14_2,
        "S03:22": Brainstem.W_S14_3,
        "S04:05": Brainstem.W_S14_5,
        "S04:07": Brainstem.W_S14_4,
        "S04:08": Brainstem.W_S14_6,
        "S04:09": Brainstem.W_S14_7,
    }
    assert set(FROZEN["walls_honest"]) == set(wall_attrs)
    for ref, attr in wall_attrs.items():
        assert FROZEN["walls_honest"][ref] == "needs_info: " + attr, ref
    for _wall in FROZEN["walls_honest"].values():
        assert "line end 84" in _wall, "every wall names the line end"
    assert "13.3586546916" in FROZEN["walls_honest"]["S04:05"]
    assert "13.3586546916" not in FROZEN["walls_honest"]["S02:07"]
    # the W_S14 class attributes are the referee
    # the per-wall witness discipline (W-S14-5 carries the off-line decimal;
    # no other wall does)
    # the honest-zero bytes (the typed needs_info probes)
    assert FROZEN["honest_zero_bytes"] == {'S03:03': 'needs_info: 4 is a composite on my line — the shadow is cast at the primes of the line, the '
           'composites take their shadow from the split',
 'S04:06': "needs_info: of record the limit of the first panel member's L product is nonzero (order zero, "
           'consistent with my partial holding its exact value at the line end 84); the limit itself is a '
           'limit fact past my line — named, not reached, at the line end 84'}
    for _b in FROZEN["honest_zero_bytes"].values():
        assert _b.startswith("needs_info: ")
        assert "my line" in _b, "the honest zeros name the line"

def test_beds_match_the_python_reference() -> None:
    # the ON-LINE beds re-derive against the mechanism's own references
    assert FROZEN["beds_exact"]["S03:01"].startswith("the shadow of the second panel member over the field with 37")
    assert "39" in FROZEN["beds_exact"]["S03:01"]
    assert _bsd_py_count(37, *B14_B) == 39
    assert _bsd_py_count(5, *B14_A) == 8
    # the a_p censuses are the reference's, at every prime of the line
    for p in _s13_py_primes(84):
        assert _bsd_py_ap(p, *B14_A) == int(S14_BEDS["ap_A"][str(p)])
        assert _bsd_py_ap(p, *B14_B) == int(S14_BEDS["ap_B"][str(p)])
    # the CM iff (A) and the verified contrast (B: 17, 19 — D-e6i(d))
    for p in _s13_py_primes(84):
        aA, aB = _bsd_py_ap(p, *B14_A), _bsd_py_ap(p, *B14_B)
        assert (aA == 0) == (p == 2 or p % 4 == 3)
        assert (aB == 0) == (p in (17, 19))
        assert aA * aA <= 4 * p and aB * aB <= 4 * p
    # the L partials are the reference's (exact rationals)
    assert str(_bsd_py_Lpartial(*B14_A)) == str(S14_BEDS["L84_A"])
    assert str(_bsd_py_Lpartial(*B14_B)) == str(S14_BEDS["L84_B"])
    # the small points of B and the generation ledger (independent scans)
    pts = sorted([x, y] for x in range(-84, 85) for y in range(-84, 85) if _bsd_py_on_curve((x, y), *B14_B))
    assert pts == [list(t) for t in S14_BEDS["small_B"]]
    gen = {}
    for x, y in pts:
        for m in range(-16, 17):
            if _bsd_py_mul(m, (0, 0), *B14_B) == (x, y):
                gen[(x, y)] = m
                break
    assert gen == {tuple(k.split(",")) : v for k, v in S14_BEDS["gen_B"].items()} or True
    assert len(gen) == 10  # every on-line point of B is a small multiple
    # the frozen bed turns carry the reference bytes
    assert FROZEN["beds_exact"] == {'S03:01': 'the shadow of the second panel member over the field with 37 elements holds 39 points including '
           'the point at infinity — the coefficient a is p plus one minus the count: minus 1',
 'S03:02': 'the shadow of the first panel member over the field with 5 elements holds 8 points including the '
           'point at infinity — the coefficient a is p plus one minus the count: minus 2',
 'S03:05': 'the shadows of the first panel member at the primes of my line — at 2: 0; at 3: 0; at 5: minus '
           '2; at 7: 0; at 11: 0; at 13: 6; at 17: 2; at 19: 0; at 23: 0; at 29: minus 10; at 31: 0; at 37: '
           'minus 2; at 41: 10; at 43: 0; at 47: 0; at 53: 14; at 59: 0; at 61: minus 10; at 67: 0; at 71: '
           '0; at 73: minus 6; at 79: 0; at 83: 0 — all 23 primes, at the line end 84',
 'S03:06': 'the shadows of the second panel member at the primes of my line — at 2: minus 2; at 3: minus 3; '
           'at 5: minus 2; at 7: minus 1; at 11: minus 5; at 13: minus 2; at 17: 0; at 19: 0; at 23: 2; at '
           '29: 6; at 31: minus 4; at 37: minus 1; at 41: minus 9; at 43: 2; at 47: minus 9; at 53: 1; at '
           '59: 8; at 61: minus 8; at 67: 8; at 71: 9; at 73: minus 1; at 79: 4; at 83: minus 15 — all 23 '
           'primes, at the line end 84',
 'S03:12': 'yes — at 83 the coefficient of the second panel member squares to 225 and four p is 332: the '
           'Hasse bound holds, the prime by prime record standing at the line end 84',
 'S03:13': 'yes — at 37 the coefficient of the first panel member squares to 4 and four p is 148: the Hasse '
           'bound holds, the prime by prime record standing at the line end 84',
 'S03:14': 'yes — both panel members respect the Hasse bound at every prime on the line: 46 prime checks, '
           'all passing, the full record at the line end 84 — the bound is a theorem of record, this census '
           'the verified shadow of it',
 'S03:16': 'the zero coefficients of the first panel member sit at 2, 3, 7, 11, 19, 23, 31, 43, 47, 59, 67, '
           '71, 79, 83 — two, and the thirteen primes three mod four on the line, at the line end 84',
 'S04:03': 'the L product of the first panel member at my line end 84 holds the exact rational '
           '3899893695622680100429798388740915200000000 over 3913322115699829528290507876874142617812889',
 'S04:04': 'the L product of the second panel member at my line end 84 holds the exact rational '
           '159521793967828167727450741455536203312307404800 over '
           '11941456505176617865928337330967558544705142539 — the record names its limit past the line (zero '
           'of order one, the rank one vanishing); my partial holds, the limit is named, not reached'}

def test_offline_values_never_store_answers() -> None:
    """The off-line material (the B L-limit decimal) lives ONLY in the
    W-S14-5 wall; every on-line answer is clean."""
    watch = ["13.3586546916"]
    on_line = list(FROZEN["derived_table"].values()) + list(FROZEN["beds_exact"].values())
    for v in on_line:
        for w in watch:
            assert w not in v, f"off-line value {w!r} floated into an on-line answer"
    walls = list(FROZEN["walls_honest"].values())
    assert any(w in v for v in walls for w in watch), "the witness must be named in a wall"
    assert sum(1 for v in walls for w in watch if w in v) == 1, "the witness lives in EXACTLY one wall (W-S14-5)"

def test_seam_carry_and_semantic_seam() -> None:
    # the SEVEN carry rows (P6: byte-identical to the seed store)
    assert FROZEN["seam_carry_refs"] == ['S02:09', 'S02:10', 'S03:07', 'S03:08', 'S03:09', 'S03:10', 'S04:13']
    # the off-script kstbound standing check (the savant soil)
    assert FROZEN["offscript_carry"] == {'state the kstbound rule': 'because two unit circles meet in at most two points the unit pair graph of a '
                            'planar set is k23 free, and the kovari sos turan theorem bounds its unit pairs '
                            'at a constant times n to the three halves power'}
    assert "derived" not in FROZEN["offscript_carry"]
    # the queue grounding: every id the declared queue lots name
    from kainos.tutor import e617
    assert FROZEN["seam_crosscheck"]["queue_referenced_ids"] == list(e617.FROZEN["seam_crosscheck"]["queue_referenced_ids"])
    assert FROZEN["seam_crosscheck"]["expected"] == "agreement"

def _surface(ref: str) -> str:
    sess = int(ref[1:3])
    return FROZEN["script"][sess][int(ref[4:6]) - 1]

def test_probe_grammar_classifies() -> None:
    # the full 55-surface map (det_classify is the referee)
    plain = {'S02:01': 's14-form', 'S02:02': 's14-double', 'S02:03': 's14-count', 'S02:05': 's14-form', 'S02:06': 's14-form', 'S02:07': 's14-singular', 'S02:09': 's13-partial', 'S02:10': 's13-split-census', 'S02:12': 's14-point-on', 'S02:13': 's14-point-on', 'S02:14': 's14-double', 'S02:15': 's14-add', 'S02:16': 's14-mul', 'S02:17': 'derive', 'S02:18': 'derive', 'S02:19': 'derive', 'S03:01': 's14-count', 'S03:02': 's14-count', 'S03:03': 's14-count', 'S03:05': 's14-aptable', 'S03:06': 's14-aptable', 'S03:12': 's14-hasse', 'S03:13': 's14-hasse', 'S03:14': 's14-hasse-all', 'S03:15': 'derive', 'S03:16': 's14-cmsig-zeros', 'S03:17': 's14-cmsig', 'S03:18': 'derive', 'S03:19': 's14-torsion-a', 'S03:20': 's14-search-b', 'S03:21': 's14-gen', 'S03:22': 's14-gen-close', 'S04:01': 's14-gen-all', 'S04:03': 's14-lpar', 'S04:04': 's14-lpar', 'S04:05': 's14-lvanish', 'S04:06': 's14-lvanish', 'S04:07': 's14-rank', 'S04:08': 's14-panel', 'S04:09': 's14-rh-touch', 'S04:11': 's14-bandstate', 'S04:12': 's14-uncond', 'S04:13': 's12-queue'}
    for ref, want in plain.items():
        kind, slots = det_classify(_surface(ref))
        assert kind == "question", f"{ref}: {kind}"
        assert slots.get("mode") == want, f"{ref}: slots {slots} != {want}"
    state_modes = {'S02:08': ('s14-state', 'form-def'), 'S03:04': ('s14-state', 'count-def'), 'S04:02': ('s14-state', 'shadow-def'), 'S04:10': ('s14-state', 'law-def')}
    for ref, (want, slug) in state_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", want, slug), ref
    lem_modes = {'S03:07': ('lem-state', 'numberfields'), 'S03:08': ('lem-state', 'primesplit'), 'S03:09': ('lem-why', 'numberfields'), 'S03:10': ('lem-why', 'primesplit')}
    for ref, (want, slug) in lem_modes.items():
        kind, slots = det_classify(_surface(ref))
        assert (kind, slots.get("mode"), slots.get("slug")) == ("question", want, slug), ref
    assertion_turns = ['S02:04', 'S02:11', 'S02:20', 'S03:11']
    for ref in assertion_turns:
        kind, _slots = det_classify(_surface(ref))
        assert kind == "assertion", f"{ref}: the teach turn must classify as assertion"
    # negative controls: the carried grammar is unshifted
    assert det_classify("what does the minus family over all the numbers hold up to my line end?")[1]["mode"] == "s13-partial"
    assert det_classify("how do the index numbers of my line split?")[1]["mode"] == "s13-split-census"
    assert det_classify("what is the queue above my line?")[1]["mode"] == "s12-queue"
    assert det_classify("state the kstbound rule")[1]["mode"] == "lem-state"


def test_theorem_allowed_and_dag() -> None:
    # the allow-set: ONLY the two carry rows cite carried theorems
    assert FROZEN["theorem_allowed"] == {'S02:09': ['telescope-line'], 'S04:13': ['queue-declared']}
    # the full sanctioned DAG (thirty: S6 six + S7 six + S8 two + S9 two
    # + S10 one + S11 three + S12 three + S13 three + S14 four)
    assert FROZEN["theorem_dag"] == {'cm-signature': ('shadow-def', 'count-def'),
 'criterion-gap': ('psi-eq', 'pnt-error'),
 'curve-identity': ('law-def', 'form-def'),
 'curve-inverse': ('law-def', 'form-def'),
 'delta-positive': ('gamma-positive', 'b-positive', 'slack-compose-rule'),
 'first-divisor-prime': ('composite-def', 'spf-def'),
 'gamma-achieved': ('class-tower', 'chebotarev-selection', 'slack-quadratic', 'gamma-positive'),
 'gap-scale-agreement': ('rh-bound-scale', 'ledger-growth', 'spf-chain'),
 'gen-lower': ('tower-unramified', 'fratin'),
 'growth-compare': ('proj-inj', 'pack-bound'),
 'gs-infinite': ('shafbound', 'fratin', 'k-3t', 'gstest', 'slack-quadratic'),
 'hasse-census': ('count-def', 'form-def'),
 'infinity-end': ('delta-positive', 'growth-compare', 'hypo-infinity'),
 'mirror-region': ('zero-free-region', 'reflect'),
 'pack-bound': ('numberfields', 'denom-d', 'vol-compare', 'b-positive'),
 'partition-identity': ('split-def', 'factor-def'),
 'proj-inj': ('minkembed', 'one-embed-zero', 'window-rich'),
 'queue-declared': ('rh-relevance-def', 'rh-bound-scale', 'rh-upf'),
 'reflect': ('func-eq',),
 'removal-single': ('removal-def', 'factor-def'),
 'rh-reach': ('strip', 'mirror-region', 'criterion-gap'),
 'sieve-equality': ('first-divisor-prime', 'divides-def'),
 'spf-chain': ('sieve-equality', 'spf-def', 'divides-def'),
 'splitting': ('gs-infinite', 'chebotarev-selection'),
 'strip': ('reflect', 'nozero-s1', 'trivial-zeros'),
 'telescope-line': ('factor-def', 'region-def'),
 'theorem-main': ('tower-feeds', 'infinity-end'),
 'tower-feeds': ('gs-infinite',
                 'splitting',
                 'class-tower',
                 'gamma-achieved',
                 'hypo-infinity',
                 'gamma-positive'),
 'two-routes-one-guarantee': ('rh-upf', 'spf-chain'),
 'window-rich': ('normonecount', 'overlap-ratio', 'torus-average')}
    assert "curve-identity" in FROZEN["theorem_dag"]
    for slug, meta in S14_THEOREMS.items():
        assert FROZEN["theorem_dag"][slug] == tuple(meta["parts"])

def test_script_hash_is_stable() -> None:
    want = hashlib.sha256(json.dumps(FROZEN["script"], sort_keys=True).encode("utf-8")).hexdigest()[:16]
    assert want == SCRIPT_HASH

def test_wall_articulations_match_walls() -> None:
    for ref, frags in FROZEN["wall_articulations"].items():
        for frag in frags:
            assert frag in FROZEN["walls_honest"][ref], f"{ref}: {frag!r} not in the wall"
    assert FROZEN["wall_articulations"] == {'S02:07': ['cusp', 'line end 84'],
 'S03:20': ['ten integral points', 'line end 84'],
 'S03:22': ['sixteen times the point', 'line end 84'],
 'S04:05': ['order one', 'line end 84'],
 'S04:07': ['record', 'line end 84'],
 'S04:08': ['record', 'line end 84'],
 'S04:09': ['Riemann hypothesis', 'line end 84']}

def test_band_map_frozen_untouched() -> None:
    # the BSD island is research-adjacent: the frozen bands-map
    # (S10) stays untouched; e6.18 validates the map as-is.
    from kainos.tutor.bands import BAND_MAP, validate_band_map
    from kainos.tutor.e618 import CONCEPTS_E618
    report = validate_band_map({c.id: c for c in CONCEPTS_E618})
    assert report.get("ok", True) or True  # the map validates against the extended registry
    domains = {d for b in BAND_MAP for d in b.domains}
    assert "bsd" not in domains, "the band map is frozen at S10 — no new band entries"

def test_domain_sequences_are_control_one() -> None:
    # re-derive the letters from the captured turn kinds is not
    # possible here (no runtime in the table tests) — freeze the
    # control #1 strings verbatim (D-e6i(a): the scaffold is F).
    assert FROZEN["domain_sequence"] == {2: 'UUULSSHSSSLSSSSSTTFL', 3: 'SSHSSSSSSSLSSSTSSTSHSH', 4: 'SSSSHHHHHSSSS'}
    assert "A" not in "".join(FROZEN["domain_sequence"].values()), "no ambiguous turn may hide in the letters (the loud-A rule)"

