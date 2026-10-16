"""E6.14 (S10 — the attempt) — the pre-registered frozen-table tests."""

from __future__ import annotations

from kainos.tutor.bands import BAND_MAP, band_by_name
from kainos.tutor.brainstem import (
    S4_LESSONS,
    S7_LESSONS,
    S8_LESSONS,
    S9_DENYLIST,
    S9_LESSONS,
    S10_THEOREMS,
    det_classify,
)
from kainos.tutor.e612 import _ANSWER_ as E612_ANSWER
from kainos.tutor.e612 import FROZEN as E612_FROZEN
from kainos.tutor.e613 import (
    CONCEPTS_E613,
)
from kainos.tutor.e613 import (
    FROZEN as E613_FROZEN,
)
from kainos.tutor.e614 import (
    _ANSWER_,
    CONCEPTS_E614,
    FROZEN,
    SCRIPT_HASH,
    WALL_ARTICULATIONS,
)

ALL_LESSONS = {**S4_LESSONS, **S7_LESSONS, **S8_LESSONS, **S9_LESSONS}

GAP_FRAGMENT = "not a capability i have been taught"


def test_no_new_concepts() -> None:
    # S10 is a measurement band: the concept registry is unchanged.
    assert CONCEPTS_E614 == CONCEPTS_E613


def test_script_shape_and_no_teaching() -> None:
    assert FROZEN["total_turns"] == 75
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 20
    assert len(FROZEN["script"][4]) == 30
    # S10 teaches NOTHING: no seam statement appears in the script
    # (the corpus is reproduced by PROBE, never by re-assertion).
    script_lines = [t for s in FROZEN["script"].values() for t in s]
    for phrase in ALL_LESSONS:
        assert phrase not in script_lines


def test_frozen_shape() -> None:
    assert FROZEN["seed_total"] == 1037
    assert FROZEN["line_end_final"] == 84
    assert FROZEN["new_facts"] == 1  # only the assembly theorem
    assert FROZEN["new_fact_ids"] == ["theorem:rh-reach"]
    assert FROZEN["total_seam_facts"] == 81  # 80 at seed + 1 (the assembly); the D-e6k(e) census
    assert len(FROZEN["theorem_dag"]) == 17  # S6 + S7 + S8 + S9 + S10
    assert FROZEN["pre_teach_gaps"] == {}
    assert FROZEN["prereq_edges"] == []
    # FROZEN FROM CONTROL #1 (written once to /tmp/rh-s10-control1.txt,
    # read back): the mechanism's own numbers.
    assert FROZEN["final_total"] == 1101  # 1037 + 1 fact + 63 events
    assert FROZEN["new_events"] == 63
    assert isinstance(FROZEN["mastery_expected"], dict) and len(FROZEN["mastery_expected"]) == 10
    assert FROZEN["mastery_expected"]["psi-eq"] == {"state": "stable", "correct": 11}
    assert FROZEN["mastery_expected"]["zero-free"] == {"state": "practicing", "correct": 12}
    assert isinstance(FROZEN["expected_prereq_gaps"], dict) and len(FROZEN["expected_prereq_gaps"]) == 10
    assert isinstance(FROZEN["pre_s10_drilled"], dict) and len(FROZEN["pre_s10_drilled"]) == 19
    assert FROZEN["domain_sequence"] == {
        2: "SSSSSSSSSSSSSSSSSSSSSSHHH",
        3: "SSSSSHSHSHSSSSSSSFTH",
        4: "SSSSSSSSSSSSSSSSSSHHHHHHHSHSSS",
    }
    # the typed part-set names the missing part (the W-S6-2 family)
    from kainos.tutor.e614 import PARTSET_FAIL_ARTICULATION

    assert "short the mirror-region" in PARTSET_FAIL_ARTICULATION
    assert "not a capability" not in PARTSET_FAIL_ARTICULATION


def test_pre_s10_states_carry_e613_final() -> None:
    # 80 = 70 carried + 10 S9.
    assert len(FROZEN["pre_s10_states"]) == len(E613_FROZEN["pre_s9_states"]) + 10
    # the ten S9 concepts at their S9-final (measured) values
    for cid, exp in E613_FROZEN["mastery_expected"].items():
        assert FROZEN["pre_s10_states"][cid] == exp
    # the 70 carried concepts at their S9-final values (base + S9 drilled)
    for cid, base in E613_FROZEN["pre_s9_states"].items():
        want = base["correct"] + E613_FROZEN["pre_s9_drilled"].get(cid, 0)
        assert FROZEN["pre_s10_states"][cid] == {"state": base["state"], "correct": want}, cid


def test_denylist_is_the_s9_44() -> None:
    from kainos.tutor.brainstem import S8_DENYLIST

    assert S9_DENYLIST == S8_DENYLIST
    assert len(S9_DENYLIST) == 44


def test_assembly_theorem_sanctioned() -> None:
    meta = S10_THEOREMS["rh-reach"]
    assert meta["parts"] == ("strip", "mirror-region", "criterion-gap")
    assert meta["concept"] == "riemann"
    assert meta["statement"]


def test_partset_failure_and_derive() -> None:
    assert FROZEN["scaffold_failures"] == {
        "S03:18": "rh-reach: the requested part set is not the sanctioned set (short the mirror-region)"
    }
    assert FROZEN["derive_successes"] == {"S03:19": "rh-reach"}
    # the grammar resolves both probes
    c18, _ = det_classify(FROZEN["script"][3][17])
    c19, _ = det_classify(FROZEN["script"][3][18])
    assert c18 == "question" and c19 == "question"
    # the frozen part-set note names the missing part
    assert "mirror-region" in FROZEN["scaffold_failures"]["S03:18"]


def test_attempt_turns_are_the_probe_line() -> None:
    assert FROZEN["attempt_turns"] == ("S03:20", "S04:27")
    for ref in FROZEN["attempt_turns"]:
        ses, n = int(ref[1:3]), int(ref[4:6])
        assert FROZEN["script"][ses][n - 1] == "can you derive the riemann hypothesis from the store?"
    # the S10 attempt form cites the assembly + names the missing capability
    art = _ANSWER_["WALL_ATTEMPT_S10"]
    assert GAP_FRAGMENT in art
    assert "square-root improvement" in art
    assert "it is the conjecture itself" in art


def test_theorem_allowed_covers_grounded() -> None:
    ta = FROZEN["theorem_allowed"]
    assert ta["S03:19"] == ("strip", "mirror-region", "criterion-gap")
    assert ta["S03:20"] == ("rh-reach",)
    assert ta["S04:10"] == ("rh-reach",)
    assert ta["S04:12"] == ("strip", "mirror-region", "criterion-gap")
    assert ta["S04:27"] == ("rh-reach",)
    assert ta["S04:30"] == ("theorem-main",)


def test_pre_s9_wall_strings_carried() -> None:
    # the carried wall phrases are byte-identical to the e6.12 originals
    for key in (
        "SINCYCLE",
        "GROWTH",
        "NUMZERO",
        "WALL_NUMCHECK",
        "WALL_OFFZERO",
        "WALL_PNTCONF",
        "WALL_PRODCONF",
        "WALL_ZETAVAL",
    ):
        assert _ANSWER_[key] == E612_ANSWER[key]


def test_conj_probes_and_attempt_grounding() -> None:
    assert FROZEN["conj_status_open"] == ("S02:15", "S04:26", "S04:28")
    assert FROZEN["conj_evidence_refs"] == ("S02:15", "S04:26", "S04:28")
    for ref in FROZEN["conj_status_open"]:
        ses, n = int(ref[1:3]), int(ref[4:6])
        assert FROZEN["script"][ses][n - 1] == "what is the status of the riemann hypothesis?"
    # S10 has NO conj-teach turn: the M8 exception does not apply
    assert FROZEN["theorem_allowed"].get("S03:16") != ("conjecture-exception",)


def test_deviant_route_walls() -> None:
    c_li, _ = det_classify(FROZEN["script"][4][18])
    c_st, _ = det_classify(FROZEN["script"][4][19])
    assert c_li == "question"
    assert c_st == "question"
    assert "route ends where the conjecture begins" in _ANSWER_["WALL_LICLOSE"]
    assert "route ends where the conjecture begins" in _ANSWER_["WALL_STCLOSE"]


def test_band_end_probes_cover_session4() -> None:
    assert len(FROZEN["band_end_probes"]) == 30
    assert set(FROZEN["band_end_probes"]) == {f"S04:{i:02d}" for i in range(1, 31)}


def test_script_hash_is_stable() -> None:
    assert len(SCRIPT_HASH) == 16


def test_crosscheck_legs() -> None:
    bc = FROZEN["bed_crosscheck"]
    assert bc["pi_ref"] == "S02:16"
    assert bc["jfunc_ref"] == "S02:17"
    assert bc["shared"] == E612_FROZEN["bed_crosscheck"]["shared"]
    assert len(bc["shared"]) == 36


def test_wall_articulations_match_walls() -> None:
    assert set(WALL_ARTICULATIONS) == set(FROZEN["walls_honest"])


def test_band_map_rh3_implemented() -> None:
    # the RH-TRACK is complete: all three RH bands official (e6.12 + e6.13 + e6.14)
    assert any(b.name == "rh-3" and b.status == "implemented" for b in BAND_MAP)
    assert band_by_name("rh-3").evidence == ("e6.14",)
