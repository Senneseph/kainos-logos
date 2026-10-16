"""E6.13 — the RH-TRACK S9 experiment (the criterion gallery)."""

from __future__ import annotations

from kainos.tutor.bands import BAND_MAP
from kainos.tutor.brainstem import (
    CONCEPT_SAVANT9,
    S9_DENYLIST,
    S9_LESSONS,
    S9_THEOREMS,
    det_classify,
)
from kainos.tutor.e612 import CONCEPTS_E612
from kainos.tutor.e612 import FROZEN as E612_FROZEN
from kainos.tutor.e613 import (
    CONCEPTS_E613,
    FROZEN,
    S9_NEW_FACT_IDS,
    S9_SEAM_FROZEN,
    SCRIPT_HASH,
    WALL_ARTICULATIONS,
)


def test_concepts_extend_e612() -> None:
    assert CONCEPTS_E613 == CONCEPTS_E612 + CONCEPT_SAVANT9
    assert len(CONCEPT_SAVANT9) == 10


def test_frozen_shape() -> None:
    assert FROZEN["total_turns"] == 75
    assert len(FROZEN["script"][2]) == 25
    assert len(FROZEN["script"][3]) == 20
    assert len(FROZEN["script"][4]) == 30
    assert FROZEN["seed_total"] == 944
    assert FROZEN["line_end_final"] == 84
    assert FROZEN["new_facts"] == 36
    assert len(S9_NEW_FACT_IDS) == 36
    assert FROZEN["final_total"] == 1037  # control #1: 944 + 36 facts + 57 events
    assert FROZEN["new_events"] == 57
    assert isinstance(FROZEN["mastery_expected"], dict) and len(FROZEN["mastery_expected"]) == 10
    assert isinstance(FROZEN["pre_s9_drilled"], dict) and FROZEN["pre_s9_drilled"] == {
        "critical-strip": 1,
        "prime-count": 1,
        "riemann": 1,
    }
    assert FROZEN["domain_sequence"] == {
        2: "ULSLSFLSTSSSLSLSTSSLSSLSU",
        3: "LSHULSLULSSHHSHSSSSH",
        4: "SSSSSSSSSSSSSSSSSSSSSHHHHHHSSS",
    }
    assert len(FROZEN["theorem_dag"]) == 16  # S6 + S7 + S8 + S9


def test_eleven_lessons_verbatim() -> None:
    for phrase in S9_LESSONS:
        assert any(t == phrase for s in FROZEN["script"].values() for t in s)


def test_lessons_are_byte_canonical() -> None:
    # every S9_LESSONS key round-trips to its seam entry
    assert set(S9_SEAM_FROZEN.keys()) == {
        "psi-eq", "pi-eq", "st-eq", "li-criterion", "polya-hilbert", "lindelof",
        "zero-free-region", "pnt-error", "hardy", "mean-square", "zero-density",
    }
    for meta in S9_SEAM_FROZEN.values():
        assert meta["kind"] == "lemma"
        assert meta["source_lines"]


def test_theorems_sanctioned() -> None:
    assert S9_THEOREMS["criterion-gap"]["parts"] == ("psi-eq", "pnt-error")
    assert S9_THEOREMS["mirror-region"]["parts"] == ("zero-free-region", "reflect")


def test_denylist_is_the_s8_44() -> None:
    from kainos.tutor.brainstem import S8_DENYLIST

    assert S9_DENYLIST == S8_DENYLIST
    assert len(S9_DENYLIST) == 44


def test_pre_teach_gaps_are_honest_gaps() -> None:
    assert set(FROZEN["pre_teach_gaps"].keys()) == {"S02:01", "S02:25", "S03:04", "S03:08"}
    for ref in FROZEN["pre_teach_gaps"]:
        ses, n = int(ref[1:3]), int(ref[4:6])
        assert det_classify(FROZEN["script"][ses][n - 1]) is not None


def test_scaffold_and_derives() -> None:
    assert FROZEN["scaffold_failures"] == {"S02:06": "criterion-gap: missing psi-eq"}
    assert FROZEN["derive_successes"] == {"S02:09": "criterion-gap", "S02:17": "mirror-region"}


def test_attempt_turns_are_the_probe_line() -> None:
    assert FROZEN["attempt_turns"] == ("S03:20", "S04:27")
    for ref in FROZEN["attempt_turns"]:
        ses, n = int(ref[1:3]), int(ref[4:6])
        assert FROZEN["script"][ses][n - 1] == "can you derive the riemann hypothesis from the store?"


def test_theorem_allowed_covers_grounded() -> None:
    # the attempt turns ground on the derived gap; the states/whys on
    # the theorems
    assert FROZEN["theorem_allowed"]["S03:20"] == ("criterion-gap",)
    assert FROZEN["theorem_allowed"]["S04:27"] == ("criterion-gap",)
    assert FROZEN["theorem_allowed"]["S03:19"] == ("strip",)
    assert FROZEN["theorem_allowed"]["S04:30"] == ("theorem-main",)


def test_pre_s9_states_carry_e612_final() -> None:
    # the 9 S8 concepts at their e6.12-final (state, correct)
    for cid, exp in E612_FROZEN["mastery_expected"].items():
        assert FROZEN["pre_s9_states"][cid] == exp
    # the five S7 concepts at their e6.12-final (post-S8 drills)
    assert FROZEN["pre_s9_states"]["tower-base"]["correct"] == E612_FROZEN["pre_s8_states"]["tower-base"]["correct"] + E612_FROZEN["pre_s8_drilled"]["tower-base"]
    assert FROZEN["pre_s9_states"]["disproof"]["correct"] == E612_FROZEN["pre_s8_states"]["disproof"]["correct"]
    # the carried census
    assert len(FROZEN["pre_s9_states"]) == len(E612_FROZEN["pre_s8_states"]) + 9


def test_band_end_probes_cover_session4() -> None:
    assert len(FROZEN["band_end_probes"]) == 30
    assert set(FROZEN["band_end_probes"]) == {f"S04:{i:02d}" for i in range(1, 31)}


def test_script_hash_is_stable() -> None:
    assert len(SCRIPT_HASH) == 16


def test_crosscheck_legs() -> None:
    bc = FROZEN["bed_crosscheck"]
    assert bc["pi_ref"] == "S03:17"
    assert bc["jfunc_ref"] == "S03:18"
    assert bc["shared"] == E612_FROZEN["bed_crosscheck"]["shared"]
    assert len(bc["shared"]) == 36


def test_wall_articulations_match_walls() -> None:
    assert set(WALL_ARTICULATIONS) == set(FROZEN["walls_honest"])


def test_band_map_still_validates() -> None:

    assert any(b.name == "rh-2" for b in BAND_MAP)
