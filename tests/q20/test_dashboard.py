"""Growth dashboard: coverage + exception accounting (step 15.3)."""

from pathlib import Path

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import (
    Assertion,
    EpistemicState,
    ExceptionState,
    Provenance,
    Source,
    TermRef,
)
from kainos.q20 import load_corpus, load_questions, seed
from kainos.q20.dashboard import render, sample_growth, write_growth


def _prov() -> Provenance:
    return Provenance(source=Source(uri="test", version="1"), observer="t", verified=True)


@pytest.fixture()
def tiny() -> InMemoryCodexStore:
    """Two concepts with known coverage:
    a: 2 assertions, both verified, distinct partners  -> 1.0
    b: 1 verified + 1 candidate, distinct partners     -> 0.5
    plus one disputed pair on c and a 'sometimes' cell on a.
    """

    store = InMemoryCodexStore()

    def _unverified() -> Provenance:
        return Provenance(source=Source(uri="test", version="1"), observer="t", verified=False)

    a_term = TermRef(id="a", labels=["a"])
    b_term = TermRef(id="b", labels=["b"])
    c_term = TermRef(id="c", labels=["c"])
    hp = TermRef(id="has_property")
    store.add(Assertion(id="s1", subject=a_term, relation=hp, object="p1=x", status=EpistemicState.established, provenance=_prov()))
    store.add(Assertion(id="s2", subject=a_term, relation=hp, object="p2=y", status=EpistemicState.established, provenance=_prov()))
    store.add(Assertion(id="s3", subject=a_term, relation=hp, object="p3=sometimes", status=EpistemicState.established, provenance=_prov()))
    store.add(Assertion(id="s4", subject=b_term, relation=hp, object="p1=x", status=EpistemicState.established, provenance=_prov()))
    store.add(Assertion(id="s5", subject=b_term, relation=hp, object="p2=z", status=EpistemicState.candidate, provenance=_unverified()))
    store.add(Assertion(id="s6", subject=c_term, relation=hp, object="p4=yes", status=EpistemicState.disputed, exception=ExceptionState.conflicting, provenance=_unverified()))
    store.add(Assertion(id="s7", subject=c_term, relation=hp, object="p4=no", status=EpistemicState.disputed, exception=ExceptionState.conflicting, provenance=_unverified()))
    return store


def test_coverage_on_tiny_fixture(tiny: InMemoryCodexStore):
    corpus = [
        {"id": "a", "label": "a", "categories": [], "properties": {}},
        {"id": "b", "label": "b", "categories": [], "properties": {}},
        {"id": "c", "label": "c", "categories": [], "properties": {}},
        {"id": "z", "label": "z", "categories": [], "properties": {}},  # no assertions at all
    ]
    s = sample_growth(tiny, corpus, [])
    assert s["n_assertions"] == 7
    assert s["coverage"]["a"] == 1.0  # all 3 assertions verified
    assert s["coverage"]["b"] == 0.5  # s5's combination is unverified (candidate)
    assert s["coverage"]["c"] == 0.0  # disputed != verified
    assert s["coverage"]["z"] == 0.0
    assert s["coverage_zero_concepts"] == ["c", "z"]
    assert s["sometimes_cells"] == 1
    assert s["by_exception"] == {"conflicting": 2}
    assert s["disputed_terms"] == ["c"]
    assert s["by_status"] == {"candidate": 1, "disputed": 2, "established": 4}


def test_render_contains_the_key_numbers(tiny: InMemoryCodexStore):
    corpus = [{"id": "a", "label": "a", "categories": [], "properties": {}}]
    md = render(sample_growth(tiny, corpus, []))
    assert "Assertions: **7**" in md
    assert "| a | 1.0000 |" in md
    assert "conflicting: 2" in md
    assert "'sometimes' cells: **1**" in md


def test_write_growth_creates_file(tiny: InMemoryCodexStore, tmp_path: Path):
    out = tmp_path / "growth.md"
    written = write_growth(tiny, [{"id": "a", "label": "a", "categories": [], "properties": {}}], [], out)
    assert written == out
    assert out.exists()
    text = out.read_text()
    assert text.startswith("# 20Q growth dashboard")


def test_full_corpus_sample_is_sane():
    store = InMemoryCodexStore()
    seed(store)
    corpus = load_corpus()
    s = sample_growth(store, corpus, load_questions())
    assert s["n_assertions"] > 0
    # a freshly seeded corpus is fully established & verified -> mean coverage 1.0
    assert s["by_status"] == {"established": s["n_assertions"]}
    assert s["coverage_mean"] == 1.0
    assert s["dimensions"] == []
    md = render(s)
    assert f"of {len(corpus)}" in md
