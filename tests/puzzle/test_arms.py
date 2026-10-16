"""The E4.1 arms, end to end (frozen choices — see phase-4 experiments.md)."""

from __future__ import annotations

from kainos.puzzle.bench import (
    ARM_C_DROPPED_CLUE,
    EINSTEIN_TRUTH,
    TRANSFER_TRUTH,
    _replay_proof,
)
from kainos.puzzle.core import minimal_certificate, resolving_facts, solve
from kainos.puzzle.puzzles import (
    EINSTEIN,
    EINSTEIN_CONTRADICTION_CLUE,
    EINSTEIN_FISH_TERM,
    EINSTEIN_HIDDEN_ARM,
    TRANSFER_4x4,
)


def test_arm_a_unique_solution_and_truth() -> None:
    rep = solve(EINSTEIN, cap=2)
    assert rep.status == "solved" and rep.unique
    sol = rep.solutions[0]
    assert sol.as_grid(EINSTEIN) == [dict(r) for r in EINSTEIN_TRUTH]
    fish = sol.pos("pet", EINSTEIN_FISH_TERM)
    assert fish == 4
    assert sol.cell(fish, EINSTEIN)["nationality"] == "german"
    ok, why = _replay_proof(EINSTEIN, sol)
    assert ok, why


def test_arm_b_hidden_term_exact_gap_no_hallucination() -> None:
    spec = EINSTEIN.with_hidden("pet", EINSTEIN_HIDDEN_ARM)
    rep = solve(spec, cap=2)
    assert rep.status == "solved" and rep.unique
    sol = rep.solutions[0]
    grid = sol.as_grid(spec)
    assert [row["pet"] for row in grid] == ["cats", "horses", "birds", "pet:u1", "dogs"]
    gaps = sol.gaps(spec)
    assert len(gaps) == 1
    g = gaps[0]
    assert (g.dim, g.placeholder, g.pos) == ("pet", "pet:u1", 4)
    assert "position 4" in g.statement and "I will not invent one" in g.statement
    # no hallucination: nothing named outside the visible vocabulary
    vocab = {t for d in spec.dimensions for t in d.visible()}
    for row in grid:
        assert all(val in vocab for val in row.values())


def test_arm_c_missing_clue_exactly_two_solutions() -> None:
    red = EINSTEIN.with_clues(tuple(c for i, c in enumerate(EINSTEIN.clues) if i != ARM_C_DROPPED_CLUE))
    rep = solve(red, cap=400)
    assert rep.status == "underdetermined"
    assert len(rep.solutions) == 2
    assert not rep.capped
    # the two solutions differ only in the horse/fish swap
    s0, s1 = rep.solutions
    diff = [
        (k)
        for k in red.variable_keys()
        if s0.pos(k[0], k[1]) != s1.pos(k[0], k[1])
    ]
    assert sorted(diff) == [("pet", "fish"), ("pet", "horses")]
    facts = resolving_facts(red)
    assert len(facts) == 4
    assert all(r.status == "solved" and r.unique for _, r in facts)
    assert any(f.text == "fish (pet) is at position 4" for f, _ in facts)


def test_arm_d_contradiction_certificate() -> None:
    spec_d = EINSTEIN.with_clues(EINSTEIN.clues + (EINSTEIN_CONTRADICTION_CLUE,))
    rep = solve(spec_d, cap=1)
    assert rep.status == "no_solution"
    assert rep.contradiction is not None
    cert = minimal_certificate(spec_d, rep.contradiction.clue_ids)
    # exactly the two Norwegian-at-fixed-position clues (9th and the added 16th)
    assert cert == [8, 15]
    for cid in cert:
        without = spec_d.with_clues(tuple(c for i, c in enumerate(spec_d.clues) if i != cid))
        assert solve(without, cap=1).status in ("solved", "underdetermined")


def test_arm_e_transfer_unique() -> None:
    rep = solve(TRANSFER_4x4, cap=2)
    assert rep.status == "solved" and rep.unique
    assert rep.solutions[0].as_grid(TRANSFER_4x4) == [dict(r) for r in TRANSFER_TRUTH]
    ok, why = _replay_proof(TRANSFER_4x4, rep.solutions[0])
    assert ok, why
