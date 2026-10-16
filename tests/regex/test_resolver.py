"""Resolver tests (P1.05) — resolution via CODEX, rotation, and honest
REQUIRES_CONTEXT / UNSEEN statuses (spec §4).
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, Provenance, Source, TermRef
from kainos.lang.deterministic import DeterministicKernel
from kainos.regex.ir import (
    Alternative,
    Anchor,
    Class,
    ClassKind,
    Literal,
    Quantifier,
    Repeat,
    Sequence,
    UnresolvedRef,
)
from kainos.regex.lexicon import RELATES_SURFACES_TO, seed
from kainos.regex.resolver import node_from_realization, resolve


@pytest.fixture()
def codex() -> InMemoryCodexStore:
    store = InMemoryCodexStore()
    seed(store)
    return store


def _add_realization(store: InMemoryCodexStore, term_id: str, value: str, aid: str) -> None:
    store.add(
        Assertion(
            id=aid,
            subject=TermRef(id=term_id, kind="entity", labels=[term_id]),
            relation=TermRef(id=RELATES_SURFACES_TO, kind="relation", labels=["realizes as"]),
            object=value,
            polarity=True,
            confidence=0.9,
            provenance=Provenance(source=Source(uri="test"), observer="test"),
        )
    )


# ── Class verification (trace entries) ──────────────────────────────────────


def test_class_verification_lands_in_trace(codex):
    node, trace = resolve(Class(ClassKind.digit), codex)
    assert node == Class(ClassKind.digit)  # classes keep semantic identity
    assert trace == [
        {"kind": "class", "term": "digit", "realized_as": r"\d", "assertion_id": "lexicon-digit"}
    ]


def test_unseeded_codex_records_missing_not_fails():
    _, trace = resolve(Class(ClassKind.digit), InMemoryCodexStore())
    assert trace == [
        {"kind": "class", "term": "digit", "realized_as": None, "assertion_id": None}
    ]


# ── reference rotation ──────────────────────────────────────────────────────


def test_hyphen_resolves_to_hyphen_via_codex(codex):
    node, trace = resolve(UnresolvedRef(surface="hyphen", candidates=[]), codex)
    assert node == Literal("-", raw=True)
    assert trace[0]["kind"] == "ref"
    assert trace[0]["status"] == "resolved"
    assert trace[0]["realization"] == "-"
    assert trace[0]["via"] == "hyphen"
    assert trace[0]["assertion_ids"] == ["lexicon-hyphen"]


def test_the_dash_thing_parses_to_candidate_ref(codex):
    kernel = DeterministicKernel(codex)
    interp = kernel.parse("the dash thing")[0]
    assert isinstance(interp.ir, UnresolvedRef)
    assert interp.ir.surface == "dash thing"
    assert interp.ir.candidates == ["dash"]
    assert interp.unresolved == ["dash thing"]


def test_single_reachable_realization_resolves(codex):
    _add_realization(codex, "dash", "-", "dash-one")
    node, trace = resolve(UnresolvedRef(surface="dash thing", candidates=["dash"]), codex)
    assert node == Literal("-", raw=True)  # 'dash' shares its only realization with 'hyphen'
    assert trace[0]["status"] == "resolved"
    assert trace[0]["via"] == "dash"


def test_ambiguous_realizations_keep_ref_with_status(codex):
    _add_realization(codex, "dash", "-", "dash-one")
    _add_realization(codex, "dash", "–", "dash-two")
    node, trace = resolve(UnresolvedRef(surface="dash thing", candidates=["dash"]), codex)
    assert isinstance(node, UnresolvedRef)
    assert node.candidates == ["-", "–"]  # competing realizations
    assert trace[0]["status"] == "REQUIRES_CONTEXT"
    assert trace[0]["candidates"] == ["-", "–"]


def test_unseen_candidate_records_unseen(codex):
    node, trace = resolve(UnresolvedRef(surface="dash thing", candidates=["dash"]), codex)
    assert isinstance(node, UnresolvedRef)
    assert trace[0]["status"] == "UNSEEN"


def test_rotation_reaches_neighbor_realizations(codex):
    # 'glyph' realizes nothing itself, but it is related to 'hyphen', whose
    # realization is one hop away — rotation must find it.
    codex.add(
        Assertion(
            id="g-glyph-rel",
            subject=TermRef(id="glyph", kind="entity", labels=["glyph"]),
            relation=TermRef(id="see_also", kind="relation", labels=["see also"]),
            object="hyphen",  # str object carrying the term id of the partner
            polarity=True,
            provenance=Provenance(source=Source(uri="test"), observer="test"),
        )
    )
    node, trace = resolve(UnresolvedRef(surface="glyph", candidates=[]), codex)
    assert node == Literal("-", raw=True)  # one-hop rotation lands on a CODEX-taught fragment
    assert trace[0]["status"] == "resolved"


def test_node_from_realization_shapes():
    assert node_from_realization(r"\d") == Class(ClassKind.digit)
    assert isinstance(node_from_realization("^"), Anchor)
    assert isinstance(node_from_realization("-"), Literal)
    assert isinstance(node_from_realization("zz"), Literal)


# ── structural passthrough ──────────────────────────────────────────────────


def test_resolve_walks_the_whole_tree(codex):
    tree = Sequence(
        [
            Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.exactly(2)),
            UnresolvedRef(surface="hyphen", candidates=[]),
            Alternative([Class(ClassKind.letter), Literal("z")]),
        ]
    )
    out, trace = resolve(tree, codex)
    assert isinstance(out, Sequence)
    assert out.elements[1] == Literal("-", raw=True)
    assert isinstance(out.elements[2], Alternative)
    # Trace: class (digit), ref (hyphen), class (letter).
    assert [e["kind"] for e in trace] == ["class", "ref", "class"]
    assert [e["status"] for e in trace if e["kind"] == "ref"] == ["resolved"]
