"""CODEX seed tests (step 13): provenance on every edge, no bare edges, round-trip."""

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState
from kainos.q20 import load_corpus, seed
from kainos.q20.seed import HAS_PROPERTY, IS_A, SOURCE_URI, SOURCE_VERSION


@pytest.fixture()
def seeded() -> InMemoryCodexStore:
    store = InMemoryCodexStore()
    seed(store)
    return store


def test_every_assertion_has_provenance(seeded: InMemoryCodexStore):
    dump = seeded.dump()
    assertions = dump["assertions"]
    assert len(assertions) > 400
    for a in assertions:
        prov = a["provenance"]
        assert prov is not None, f"bare edge: {a['id']}"
        assert prov["source"]["uri"] == SOURCE_URI
        assert prov["source"]["version"] == SOURCE_VERSION
        assert a["status"] == EpistemicState.established.value


def test_relation_counts_seeded_store(seeded: InMemoryCodexStore):
    corpus = load_corpus()
    n_props = sum(len(c["properties"]) for c in corpus)
    hp = seeded.query(relation=HAS_PROPERTY)
    isa = seeded.query(relation=IS_A)
    assert len(hp) == n_props
    assert len(isa) == len(corpus)


def test_no_bare_edges_and_upserts_are_deterministic(seeded: InMemoryCodexStore):
    # re-seeding is idempotent (deterministic ids => upserts, no duplicates)
    before = len(seeded.dump()["assertions"])
    seed(seeded)
    assert len(seeded.dump()["assertions"]) == before


def test_concept_neighborhood(seeded: InMemoryCodexStore):
    car = [a for a in seeded.query(subject="car")]
    objects = {a.object if isinstance(a.object, str) else a.object.id for a in car}
    assert "alive=no" in objects
    assert "has_wheels=yes" in objects
    assert "vehicles" in objects
    # the 'animals' category term is linked to exactly the animal concepts
    animals = seeded.query(relation=IS_A, object="animals")
    assert len(animals) == 30
    assert {a.subject.id for a in animals} == {a["id"] for a in load_corpus() if "animals" in a["categories"]}


def test_dump_reload_roundtrip(seeded: InMemoryCodexStore):
    dump = seeded.dump()
    fresh = InMemoryCodexStore()
    for a in dump["assertions"]:
        fresh.add(Assertion.from_dict(a))
    assert fresh.dump() == dump
    # queries survive the round-trip (the reasoner sees the same graph)
    assert fresh.query(subject="oak_tree") == seeded.query(subject="oak_tree")


def test_absence_stays_absent(seeded: InMemoryCodexStore):
    # the unknown SEEDS must not have been written as assertions

    def objects(term: str) -> set[str]:
        return {a.object if isinstance(a.object, str) else a.object.id for a in seeded.query(subject=term)}

    dog = objects("dog")
    assert not any(o.startswith("has_wheels=") for o in dog if isinstance(o, str))
    assert not any(o.startswith("wheel_count=") for o in dog if isinstance(o, str))
    train = {o for o in objects("train") if isinstance(o, str)}
    assert "has_wheels=sometimes" in train
    assert "wheel_count=4" not in train
