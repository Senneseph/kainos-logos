"""E5.1 The Shared Grid — unit tests (the 12 official checks live in
``run_e5_1`` / the e5.1 experiment; these pin the pieces underneath)."""

from __future__ import annotations

from pathlib import Path

import pytest

from kainos.codex.models import EpistemicState
from kainos.game.actions import Correct, Pass
from kainos.game.agent import Agent
from kainos.game.scheduler import Game
from kainos.game.shared_grid import (
    CAPS,
    CELLS,
    DOOR_FACT,
    build_game,
    correct_delta,
    gen_grid,
    make_episode,
    run_e5_1,
    score_run,
)
from kainos.game.spec import GameSpec

# ── world generation ─────────────────────────────────────────────────────


def test_gen_grid_shape_and_unique_specials() -> None:
    grid, door_col = gen_grid(5101)
    assert set(grid) == set(CELLS)
    specials = [c for c in CELLS if grid[c] in ("door", "key", "goal")]
    assert len(specials) == 3
    assert grid[f"r3c{door_col}"] == "door"
    key_row = int(next(c for c in specials if grid[c] == "key")[1])
    goal_row = int(next(c for c in specials if grid[c] == "goal")[1])
    assert key_row in (1, 2)
    assert goal_row in (4, 5)


def test_gen_grid_true_door_corridor_is_open() -> None:
    for seed in (1, 7, 5101, 99991):
        grid, door_col = gen_grid(seed)
        assert grid[f"r2c{door_col}"] == "empty"
        assert grid[f"r4c{door_col}"] == "empty"


def test_planted_row3_differs_at_exactly_two_cells() -> None:
    grid, door_col = gen_grid(5101)
    from kainos.game.shared_grid import planted_row3

    row_w, planted_col = planted_row3(grid, door_col)
    assert planted_col != door_col
    diff = [c for c in row_w if grid[c] != row_w[c]]
    assert len(diff) == 2
    assert row_w[f"r3c{planted_col}"] == "door"
    assert row_w[f"r3c{door_col}"] == "empty"


def test_false_episode_planted_corridor_is_blocked() -> None:
    ep = make_episode("false")
    planted = ep["planted_col"]
    assert ep["truth"][f"r2c{planted}"] == "wall" or ep["truth"][f"r4c{planted}"] == "wall"


def test_perception_override_is_view_scoped_data() -> None:
    ep = make_episode("false")
    spec = ep["spec"]
    # the override names only facts inside a's view
    assert set(spec.perception_overrides["a"]) <= spec.views["a"]
    # and a perceives the planted row, b perceives truth
    from kainos.game.shared_grid import _perceptions

    perms = _perceptions(spec)
    truth3 = [ep["truth"][c] for c in ("r3c1", "r3c2", "r3c3", "r3c4")]
    assert [perms["a"][c] for c in ("r3c1", "r3c2", "r3c3", "r3c4")] != truth3
    assert [perms["b"][c] for c in ("r3c1", "r3c2", "r3c3", "r3c4")] == truth3


def test_override_reaching_outside_view_is_rejected() -> None:
    with pytest.raises(ValueError, match="OUTSIDE its view"):
        GameSpec(
            "t", ("a", "b"), {"f1": "x", "f2": "y"},
            {"a": frozenset({"f1"}), "b": frozenset({"f2"})},
            perception_overrides={"a": {"f2": "z"}},
        )


# ── the kernel gate (structural cleanness of the probe) ─────────────────


def test_v0_cannot_emit_correct() -> None:
    ep = make_episode("clean")
    spec = ep["spec"]

    def rogue(view, round_no, transcript):
        if round_no != 1:
            return Pass()
        return Correct("b", DOOR_FACT, (correct_delta("a", "b", "c1", "c2", 1, spec.name, ()),))

    a = Agent("a", spec, rogue, capabilities=CAPS["V0"])
    b = Agent("b", spec, lambda view, r, t: Pass(), capabilities=CAPS["V0"])
    report = Game(spec, {"a": a, "b": b}, seed=1).run(write=False)
    assert any("assert_about_other" in r["reason"] for r in report["agents"]["a"]["rejections"])
    assert not any(e["action"]["kind"] == "correct" for e in report["transcript"])


def test_v1_can_emit_correct() -> None:
    rep = build_game("false", "V1").run(write=False)
    assert any(e["action"]["kind"] == "correct" for e in rep["transcript"])


# ── behavior: the pre-registered exact values ───────────────────────────


def test_clean_redundancy_exact_fractions() -> None:
    ep = make_episode("clean")
    report = build_game("clean", "V1").run(write=False)
    sc = score_run(report, ep["spec"])
    for p in ("a", "b"):
        d = sc["redundancy"][p]
        assert (d["redundant"], d["sent"]) == (1, 9)
    assert sc["recovery"] is True

    ep0 = make_episode("clean")
    report0 = build_game("clean", "V0").run(write=False)
    sc0 = score_run(report0, ep0["spec"])
    for p in ("a", "b"):
        d = sc0["redundancy"][p]
        assert (d["redundant"], d["sent"]) == (5, 13)


def test_false_belief_probe_timeline() -> None:
    ep = make_episode("false")
    report = build_game("false", "V1").run(write=False)
    sc = score_run(report, ep["spec"])
    fc = sc["first_correct"]
    assert fc["round"] == 4 and fc["by"] == "a" and fc["target"] == "b"
    assert sc["recovery"] is True

    report0 = build_game("false", "V0").run(write=False)
    sc0 = score_run(report0, ep["spec"])
    assert sc0["first_correct"] is None
    assert sc0["correct_cells"]["b"] == len(CELLS)
    wrong = [c for c in CELLS if report0["commits"]["a"]["grid"].get(c) != ep["truth"][c]]
    assert len(wrong) == 2 and all(c.startswith("r3c") for c in wrong)


def test_disputed_anchor_pair_survives_in_both_stores() -> None:
    game = build_game("false", "V1")
    report = game.run(write=False)
    # the report carries per-agent audits; both must show the preserved pair
    for p in ("a", "b"):
        audit = report["audit"][p]
        assert audit["n_disputes_preserved"] >= 2
        assert audit["violations"] == []
    # and the raw stores: two door-anchor assertions, both disputed
    for p in ("a", "b"):
        anchors = game.agents[p].codex.query(subject=DOOR_FACT)
        disputed = [x for x in anchors if x.status == EpistemicState.disputed]
        assert len(disputed) == 2, f"{p}: both door-anchor sides must survive as disputed"


# ── determinism at the game level ───────────────────────────────────────


def test_e5_1_rerun_is_bit_identical(tmp_path: Path) -> None:
    r1 = run_e5_1(out_dir=tmp_path)
    assert r1["checks_passed"] == 12
    for key, run in r1["runs"].items():
        r2 = build_game(run["episode"], run["variant"]).run(write=False)
        assert r2["determinism_hash"] == run["determinism_hash"], key
