"""Oracle tests (step 13): determinism, unknown, sometimes, categories, numbers."""

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion
from kainos.q20 import Oracle, load_corpus, load_questions, seed
from kainos.q20.oracle import ANSWERS


@pytest.fixture(scope="module")
def oracle() -> Oracle:
    return Oracle.load()


def test_corpus_artifact_shape():
    corpus = load_corpus()
    questions = load_questions()
    assert 100 <= len(corpus) <= 300
    ids = [c["id"] for c in corpus]
    assert len(ids) == len(set(ids))
    for c in corpus:
        assert c["categories"]  # at least one category
        for v in c["properties"].values():
            assert v in ("yes", "no", "sometimes") or isinstance(v, int)
    kinds = {q["kind"] for q in questions}
    assert kinds == {"property_probe", "category_probe"}
    # intentional seeds exist: the EXCEPTION pressure has something to press
    some = sum(isinstance(v, str) and v == "sometimes" for c in corpus for v in c["properties"].values())
    assert some >= 10


def test_deterministic(oracle: Oracle):
    a = oracle.answer("dog", "q_alive")
    b = oracle.answer("dog", "q_alive")
    assert a == b == "yes"
    # full transcript stable across two freshly loaded oracles
    assert oracle.answers("car") == Oracle.load().answers("car")
    assert all(a in ANSWERS or isinstance(a, int) for a in oracle.answers("car").values())


def test_missing_property_is_unknown(oracle: Oracle):
    # dog has no has_wheels cell -> unknown (absence is the signal)
    assert oracle.answer("dog", "q_wheels") == "unknown"
    assert oracle.answer("dog", "q_wheel_count") == "unknown"
    assert oracle.answer("bread", "q_doors") == "unknown"
    # train: has_wheels is "sometimes" but NO wheel_count cell -> still unknown
    assert oracle.answer("train", "q_wheels") == "sometimes"
    assert oracle.answer("train", "q_wheel_count") == "unknown"


def test_sometimes(oracle: Oracle):
    assert oracle.answer("elephant", "q_carry") == "sometimes"
    assert oracle.answer("adult_man", "q_carry") == "sometimes"
    assert oracle.answer("sailboat", "q_engine") == "sometimes"
    assert oracle.answer("train", "q_wheels") == "sometimes"
    assert oracle.answer("mountain", "q_green") == "sometimes"


def test_numbered_values(oracle: Oracle):
    assert oracle.answer("car", "q_wheel_count") == 4
    assert oracle.answer("bicycle", "q_wheel_count") == 2
    assert oracle.answer("truck", "q_wheel_count") == 6


def test_category_probes(oracle: Oracle):
    assert oracle.answer("dog", "q_cat_animals") == "yes"
    assert oracle.answer("dog", "q_cat_vehicles") == "no"
    assert oracle.answer("pizza", "q_cat_foods") == "yes"
    assert oracle.answer("oak_tree", "q_cat_plants") == "yes"
    assert oracle.answer("house", "q_cat_places") == "yes"
    assert oracle.answer("adult_man", "q_cat_people") == "yes"
    assert oracle.answer("table", "q_cat_objects") == "yes"


def test_question_by_dict_or_id(oracle: Oracle):
    by_id = oracle.answer("horse", "q_carry")
    by_dict = oracle.answer("horse", {"id": "q_carry", "surface": "?", "kind": "property_probe", "property": "can_carry_person"})
    assert by_id == by_dict == "yes"


def test_unknown_concept_and_question_raise(oracle: Oracle):
    with pytest.raises(KeyError):
        oracle.answer("unicorn", "q_alive")
    with pytest.raises(KeyError):
        oracle.answer("dog", "q_nonexistent")


def test_corpus_seeded_into_codex():
    """The seed is the bridge: corpus -> CODEX assertions (step 13.4)."""

    store = InMemoryCodexStore()
    stats = seed(store)
    corpus = load_corpus()
    expected_props = sum(len(c["properties"]) for c in corpus)
    assert stats["concepts"] == len(corpus)
    assert stats["property_assertions"] == expected_props
    assert stats["category_assertions"] == len(corpus)
    # every seeded assertion is a real Assertion object (provenance enforced)
    assert all(isinstance(a, Assertion) for a in store.query())
    # spot check: car's wheel count is in the CODEX
    car = [a for a in store.query(subject="car") if isinstance(a.object, str) and a.object.startswith("wheel_count=")]
    assert [a.object for a in car] == ["wheel_count=4"]
