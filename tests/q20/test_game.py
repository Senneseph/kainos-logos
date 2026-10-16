"""Game loop: win/loss/budget + trace (step 14.4)."""

from collections import defaultdict

import pytest

from kainos.q20 import Oracle, load_corpus, load_questions
from kainos.q20.game import Game
from tests.q20.test_selector import FakeOracle


@pytest.fixture(scope="module")
def oracle() -> Oracle:
    return Oracle.load()


@pytest.fixture(scope="module")
def questions() -> list[dict]:
    return load_questions()


def _unique_targets(oracle) -> list[str]:
    """Concepts whose 17-answer vector identifies them alone (twins can't win — that is by design)."""

    vectors: dict[tuple, list[str]] = defaultdict(list)
    for c in load_corpus():
        vec = tuple((q["id"], oracle.answer(c["id"], q)) for q in oracle.questions)
        vectors[vec].append(c["id"])
    return [ids[0] for ids in vectors.values() if len(ids) == 1]


def test_corpus_has_identifiable_targets(oracle):
    assert len(_unique_targets(oracle)) >= 10  # the game must be winnable in principle


def test_play_win_within_budget(oracle, questions):
    targets = _unique_targets(oracle)
    for target in targets:
        game = Game(oracle, questions, target)
        r = game.play()
        assert r["won"], f"lost on {target}: {r}"
        assert 1 <= r["questions_used"] <= 20
        assert r["state"] == Game.STATE_WON
        # trace is a consistent record of the elimination
        prev = len(oracle.corpus)
        for row in r["trace"]:
            assert row["h_before"] == prev
            assert 0 < row["h_after"] <= row["h_before"]
            prev = row["h_after"]
        assert r["target"] in r["final_H"]
        assert r["final_entropy"] == 0.0
        # determinism: a fresh game produces the exact same trace
        assert Game(oracle, questions, target).play()["trace"] == r["trace"]


def test_play_determinism_is_full(oracle, questions):
    target = _unique_targets(oracle)[0]
    a = Game(oracle, questions, target).play()
    b = Game(oracle, questions, target).play()
    assert a["trace"] == b["trace"]
    assert a["questions_used"] == b["questions_used"]


def test_budget_exhaustion_is_a_recorded_loss(oracle, questions):
    # with one question the space can never collapse to a singleton for 'cow'
    # (its twin cluster is identical on every 20Q question)
    game = Game(oracle, questions, "cow", max_questions=1)
    r = game.play()
    assert r["state"] == Game.STATE_LOST or r["won"]
    if not r["won"]:
        assert r["questions_used"] == 1
        assert r["guess"] != "cow"
        assert len(r["final_H"]) > 1


def test_wrong_guess_recorded(oracle, questions):
    game = Game(oracle, questions, "mushroom")
    game.receive(game.next_question())
    r = game.make_guess("car")
    assert r["won"] is False
    assert r["guess"] == "car"
    assert game.state == Game.STATE_LOST
    # the game is over: no more questions, no more guesses
    with pytest.raises(RuntimeError):
        game.receive(questions[0])
    with pytest.raises(RuntimeError):
        game.make_guess("dog")


def test_contradiction_answer_terminates_with_loss():
    # an oracle that says "no" to everything, but a scripted "yes" answer:
    # no concept is consistent -> |H| = 0 -> loss, recorded in the trace
    ids = [f"x{i}" for i in range(6)]
    oracle = FakeOracle(ids, {(c, "q1"): "no" for c in ids})
    questions = [{"id": "q1", "surface": "q1?", "kind": "property_probe", "property": "q1"}]
    game = Game(oracle, questions, "x0")
    game.receive(questions[0], answer="yes")
    assert len(game.space) == 0
    assert game.state == Game.STATE_LOST


def test_unknown_target_rejected(oracle, questions):
    with pytest.raises(KeyError):
        Game(oracle, questions, "unicorn")


def test_stop_threshold_triggers_early_guess(oracle, questions):
    target = _unique_targets(oracle)[0]
    game = Game(oracle, questions, target, stop_threshold=99.0)  # any real IG < 99
    r = game.play()
    assert r["questions_used"] == 0  # stopped before asking anything
    assert r["guess"] is not None
    assert r["state"] in (Game.STATE_WON, Game.STATE_LOST)
