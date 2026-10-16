"""Baselines: random (seeded) + stateless greedy (step 15.2)."""

import pytest

from kainos.q20 import Oracle, load_corpus, load_questions
from kainos.q20.baselines import GreedyIGPolicy, RandomQuestioner, StatelessGreedy
from kainos.q20.game import Game
from kainos.q20.hypothesis import HypothesisSpace
from kainos.q20.selector import best_question


@pytest.fixture(scope="module")
def oracle() -> Oracle:
    return Oracle.load()


@pytest.fixture(scope="module")
def questions() -> list[dict]:
    return load_questions()


def test_random_is_seeded_reproducible(questions):
    a, b = RandomQuestioner(questions, seed=7), RandomQuestioner(questions, seed=7)
    assert a.order == b.order
    c = RandomQuestioner(questions, seed=8)
    assert a.order != c.order  # different seed, different order (17 questions: overwhelming odds)


def test_random_asks_each_question_exactly_once(oracle, questions):
    rq = RandomQuestioner(questions, seed=3)
    space = HypothesisSpace.from_corpus(load_corpus())
    asked: list[str] = []
    while (q := rq.choose(space, oracle)) is not None:
        asked.append(q["id"])
    assert sorted(asked) == sorted(q["id"] for q in questions)  # a full shuffle, no repeats, then stop
    assert rq.choose(space, oracle) is None


def test_random_policy_plays_a_complete_game(oracle, questions):
    game = Game(oracle, questions, "frog", load_corpus(), policy=RandomQuestioner(questions, seed=11))
    r = game.play()
    # random over 17 questions, budget 20: 'frog' (5 informative cells) is usually winnable,
    # but the contract is a COMPLETE recorded game, not necessarily a win
    assert r["state"] in (Game.STATE_WON, Game.STATE_LOST)
    assert 1 <= r["questions_used"] <= min(20, len(questions))
    assert all(row["h_after"] <= row["h_before"] for row in r["trace"])


def test_stateless_order_is_the_frozen_ig_order(oracle, questions):
    all_ids = {c["id"] for c in load_corpus()}
    sg = StatelessGreedy(questions, oracle, all_ids)
    # first question = the max-IG question on the FULL frozen space
    full = HypothesisSpace(all_ids)
    expected_first, _ = best_question(full, questions, oracle)
    assert sg.order[0] == expected_first["id"]
    assert len(sg.order) == len(questions)


def test_stateless_ignores_codex_history(oracle, questions):
    """The whole point: the frozen order is identical no matter what games
    (and learning) happened in between — the A1/A3 falsifier."""

    all_ids = {c["id"] for c in load_corpus()}
    before = StatelessGreedy(questions, oracle, all_ids)
    # one full game plays out against the world, using a stateless policy
    Game(oracle, questions, "shrimp", load_corpus(), policy=StatelessGreedy(questions, oracle, all_ids)).play()
    after = StatelessGreedy(questions, oracle, all_ids)
    assert before.order == after.order  # nothing learned, nothing changes


def test_adaptive_reads_h_while_stateless_advances_a_deck(oracle, questions):
    """Adaptive IG re-selects on the filtered space; stateless advances a
    frozen deck. Same first question (both max-IG on the full space), then
    the stateless one is exactly its precomputed order[1]."""

    all_ids = {c["id"] for c in load_corpus()}
    space = HypothesisSpace(all_ids)
    sg = StatelessGreedy(questions, oracle, all_ids)
    ig = GreedyIGPolicy(questions)
    first_s, first_i = sg.choose(space, oracle), ig.choose(space, oracle)
    assert first_s["id"] == first_i["id"]
    # answer the first question for a target, filter H, re-select
    target = "shrimp"
    space.apply(oracle, first_i, oracle.answer(target, first_i))
    second_i = ig.choose(space, oracle)
    second_s = sg.choose(space, oracle)
    assert second_s["id"] == StatelessGreedy(questions, oracle, all_ids).order[1]  # frozen deck
    valid = {q["id"] for q in questions}
    assert second_i["id"] in valid and second_s["id"] in valid
