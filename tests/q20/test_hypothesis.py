"""Hypothesis space: filtering, entropy, partition (step 14.2)."""

import math

import pytest

from kainos.q20 import Oracle, load_corpus, load_questions
from kainos.q20.hypothesis import HypothesisSpace


@pytest.fixture(scope="module")
def oracle() -> Oracle:
    return Oracle.load()


@pytest.fixture(scope="module")
def questions() -> list[dict]:
    return load_questions()


@pytest.fixture()
def space(oracle) -> HypothesisSpace:
    return HypothesisSpace.from_corpus(load_corpus())


def test_init_and_len(space):
    assert len(space) == 149
    with pytest.raises(ValueError):
        HypothesisSpace(None)


def test_apply_removes_inconsistent(oracle, space, questions):
    q = next(q for q in questions if q["kind"] == "property_probe" and q["property"] == "alive")
    before = len(space)
    after = space.apply(oracle, q, "no")
    expected = sum(1 for c in load_corpus() if c["properties"].get("alive") == "no")
    assert after == expected == len(space)
    assert before > after  # every alive concept is gone
    # concepts without an alive cell stayed out too (unknown != no)
    unknown = [c["id"] for c in load_corpus() if "alive" not in c["properties"]]
    assert not (set(unknown) & set(space.concepts))
    assert space.history[-1] == (q["id"], "no")


def test_numbered_answer_filter(oracle):
    s = HypothesisSpace.from_corpus(load_corpus())
    s.apply(oracle, "q_wheel_count", 4)
    expected = {c["id"] for c in load_corpus() if c["properties"].get("wheel_count") == 4}
    assert s.concepts == frozenset(expected)
    assert len(expected) > 5  # wheel_count=4 is the common vehicle count


def test_entropy(oracle):
    full = HypothesisSpace.from_corpus(load_corpus())
    assert abs(full.entropy() - math.log2(149)) < 1e-12
    single = HypothesisSpace({"mushroom"})
    assert single.entropy() == 0.0
    empty = HypothesisSpace(set())
    assert empty.entropy() == 0.0


def test_split_partitions_h(oracle, space):
    q = "q_wheels"
    buckets = space.split(oracle, q)
    flat = [c for cell in buckets.values() for c in cell]
    assert len(flat) == len(set(flat)) == 149  # disjoint, union = H
    assert set(buckets) <= {"yes", "no", "unknown", "sometimes"} | {f"n:{i}" for i in range(20)}
    # wheels: most concepts have no cell at all -> unknown is the big bucket
    assert buckets["unknown"] and len(buckets["unknown"]) > 100
    assert "car" in buckets["yes"]


def test_split_numbered_buckets(oracle):
    s = HypothesisSpace.from_corpus(load_corpus())
    buckets = s.split(oracle, "q_wheel_count")
    assert "n:4" in buckets and "n:2" in buckets
    assert "car" in buckets["n:4"] and "bicycle" in buckets["n:2"]
    assert "train" not in buckets.get("n:4", set())  # sometimes-wheels, no count


def test_history_accumulates(oracle):
    s = HypothesisSpace.from_corpus(load_corpus())
    s.apply(oracle, "q_alive", "yes")
    s.apply(oracle, "q_wheels", "yes")
    assert [h[0] for h in s.history] == ["q_alive", "q_wheels"]
    assert len(s) <= len(HypothesisSpace.from_corpus(load_corpus()))
