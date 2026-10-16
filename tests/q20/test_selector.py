"""Info-gain selector: median-ish split + documented tie-breaks (step 14.3)."""

from kainos.q20.hypothesis import HypothesisSpace
from kainos.q20.selector import best_question, expected_information_gain


class FakeOracle:
    """Hand-built world: answer(concept, question) from a table."""

    def __init__(self, concepts, answers):
        self.corpus = [{"id": c, "label": c, "categories": [], "properties": {}} for c in concepts]
        self._answers = answers
        self.questions = [
            {"id": qid, "surface": qid, "kind": "property_probe", "property": qid}
            for qid in {a[1] for a in answers}
        ]

    def answer(self, concept_id, question, seed=0):
        qid = question if isinstance(question, str) else question["id"]
        return self._answers.get((concept_id, qid), "unknown")


def fake_world():
    ids = [f"c{i}" for i in range(8)]
    table = {}
    for c in ids:
        table[(c, "q_bal")] = "yes" if c in ("c0", "c1", "c2", "c3") else "no"
        table[(c, "q_lop")] = "yes" if c != "c7" else "no"
        table[(c, "q_eqA")] = "yes" if c in ("c0", "c1", "c2", "c3") else "no"
        table[(c, "q_eqB")] = "unknown" if c in ("c0", "c1", "c2", "c3") else "sometimes"
        table[(c, "q_eqC")] = "yes" if c in ("c0", "c1", "c2", "c3") else "no"
    oracle = FakeOracle(ids, table)
    questions = [
        {"id": qid, "surface": qid, "kind": "property_probe", "property": qid}
        for qid in ("q_bal", "q_lop", "q_eqA", "q_eqB", "q_eqC")
    ]
    return oracle, questions


def test_balanced_split_beats_lopsided():
    oracle, questions = fake_world()
    space = HypothesisSpace.from_corpus(oracle.corpus)
    ig_bal = expected_information_gain(space, oracle, "q_bal")["ig"]
    ig_lop = expected_information_gain(space, oracle, "q_lop")["ig"]
    assert ig_bal > ig_lop  # 1.0 > ~0.54
    q, ig = best_question(space, questions, oracle)
    assert q["id"] in ("q_bal", "q_eqA", "q_eqC")  # all maximal-IG; tie-breaks may reorder
    assert abs(ig - 1.0) < 1e-12


def test_tiebreak_a_prefers_smaller_unknown_bucket():
    oracle, questions = fake_world()
    space = HypothesisSpace.from_corpus(oracle.corpus)
    by_id = {q["id"]: q for q in questions}
    ig_a = expected_information_gain(space, oracle, by_id["q_eqA"])["ig"]
    ig_b = expected_information_gain(space, oracle, by_id["q_eqB"])["ig"]
    assert abs(ig_a - ig_b) < 1e-12  # same expected reduction
    assert expected_information_gain(space, oracle, by_id["q_eqA"])["unknown"] == 0
    assert expected_information_gain(space, oracle, by_id["q_eqB"])["unknown"] == 4
    q, _ = best_question(space, [by_id["q_eqA"], by_id["q_eqB"]], oracle)
    assert q["id"] == "q_eqA"  # shrink EXCEPTION


def test_tiebreak_b_lowest_cost_wins():
    oracle, questions = fake_world()
    space = HypothesisSpace.from_corpus(oracle.corpus)
    # identical IG and identical unknown buckets -> cost decides
    by_id = {q["id"]: q for q in questions}
    cost = {"q_eqC": 2.0, "q_eqA": 1.0}
    q, _ = best_question(space, [by_id["q_eqC"], by_id["q_eqA"]], oracle, cost)
    assert q["id"] == "q_eqA"


def test_total_tie_is_deterministic_first_in_scan_order():
    oracle, questions = fake_world()
    space = HypothesisSpace.from_corpus(oracle.corpus)
    by_id = {q["id"]: q for q in questions}
    first = best_question(space, [by_id["q_eqA"], by_id["q_eqC"], by_id["q_bal"]], oracle)
    second = best_question(space, [by_id["q_eqA"], by_id["q_eqC"], by_id["q_bal"]], oracle)
    assert first == second
    assert first[0]["id"] == "q_eqA"  # first in scan order among exact ties


def test_selector_rejects_singleton():
    oracle, questions = fake_world()
    space = HypothesisSpace({"c0"})
    import pytest

    with pytest.raises(ValueError):
        best_question(space, questions, oracle)
