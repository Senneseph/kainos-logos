"""CODEX lexicon seed tests (P1.04) — the meaning of words lives in the CODEX
with provenance (invariant #1), and the emitter stays consistent with it
(invariant #2 / spec §5 parity).
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.sqlite import SqliteCodexStore
from kainos.regex.emitter import emit
from kainos.regex.ir import Anchor, AnchorKind, Class, ClassKind, Literal
from kainos.regex.lexicon import LEXICON, RELATES_SURFACES_TO, seed

STORE_IMPLS = [SqliteCodexStore, InMemoryCodexStore]


@pytest.fixture(params=STORE_IMPLS, ids=["sqlite", "memory"])
def codex(request) -> SqliteCodexStore | InMemoryCodexStore:
    impl = request.param
    store: SqliteCodexStore | InMemoryCodexStore = (
        SqliteCodexStore(":memory:") if impl is SqliteCodexStore else InMemoryCodexStore()
    )
    seed(store)
    yield store
    if isinstance(store, SqliteCodexStore):
        store.close()


def test_seed_ids_on_fresh_store():
    store = InMemoryCodexStore()
    ids = seed(store)
    assert ids == [f"lexicon-{s}" for s in LEXICON]


@pytest.mark.parametrize("surface", list(LEXICON))
def test_each_surface_realizes_to_its_target(codex, surface):
    hits = codex.query(subject=surface, relation=RELATES_SURFACES_TO)
    assert len(hits) == 1
    assert hits[0].object_id == LEXICON[surface]
    assert hits[0].status.value == "established"


def test_dump_shows_provenance_on_every_seeded_assertion(codex):
    """Invariant #1: every seeded assertion carries source=seed_corpus,
    status=established, verified provenance."""

    dumped = codex.dump()
    seeded = {a["id"]: a for a in dumped["assertions"] if a["id"].startswith("lexicon-")}
    assert len(seeded) == len(LEXICON)
    for a in seeded.values():
        assert a["status"] == "established"
        assert a["provenance"]["source"]["uri"] == "seed_corpus"
        assert a["provenance"]["source"]["version"] == "1"
        assert a["provenance"]["verified"] is True
        assert a["provenance"]["observer"] == "seed"


def test_terms_are_upserted_not_duplicated(codex):
    dumped = codex.dump()
    term_ids = [t["id"] for t in dumped["terms"]]
    assert len(term_ids) == len(set(term_ids))
    assert RELATES_SURFACES_TO in term_ids
    for surface in LEXICON:
        assert surface in term_ids


# ── lexicon <-> emitter parity (spec §5): the CODEX is the single source of
# truth for what a term means; the emitter's built-in tables stay consistent. ──


def test_emitter_matches_codex_for_every_seeded_surface(codex):
    """For every seeded surface, the emitter's output for the corresponding node
    shape EQUALS the CODEX realization (the parser never invents these values;
    the CODEX is the single source of truth — spec §5)."""

    emitter_shapes: dict[str, object] = {
        "digit": Class(ClassKind.digit),
        "letter": Class(ClassKind.letter),
        "word": Class(ClassKind.word),
        "whitespace": Class(ClassKind.whitespace),
        "any": Class(ClassKind.any),
        # The parser builds Anchors structurally; the CODEX still records what
        # "start"/"end" mean for explain/inspection.
        "start": Anchor(kind=AnchorKind.start),
        "end": Anchor(kind=AnchorKind.end),
        "hyphen": None,  # Literal, built from the CODEX value at parse time
    }
    for surface, node in emitter_shapes.items():
        hits = codex.query(subject=surface, relation=RELATES_SURFACES_TO)
        assert len(hits) == 1
        realization = hits[0].object_id
        assert LEXICON[surface] == realization
        if node is None:  # hyphen: the seed value IS the literal text the parser builds
            node = Literal(text=realization)
        assert emit(node) == realization, (
            f"emitter/CODEX drift on {surface!r}: emitter says {emit(node)!r}, "
            f"CODEX says {realization!r}"
        )