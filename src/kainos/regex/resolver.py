"""Resolver (P1.05) — resolve the dialect AST against the CODEX; never guess.

For every `Class`, its `realizes_as` is verified against the CODEX lexicon and
recorded in the trace (`{term, realized_as, assertion_id}`) — the Class node
itself keeps semantic identity (invariant #2). For every `UnresolvedRef`,
**rotation**: each candidate's CODEX neighborhood (direct `realizes_as` hits plus
hits of the neighbors' direct partners) is collected. Exactly one reachable
realization → the ref is replaced by the corresponding node (`{^, $}` become
Anchors, class-realization values become Classes, everything else a Literal);
several → the ref stays, recorded as `REQUIRES_CONTEXT` with the competing
candidates; none → `UNSEEN`. Anything left unresolved after the walk makes the
pipeline escalate instead of emitting (spec §4).

M1 (Morpho pattern transfer, SCAVENGE_MORPHO.md — benchmark-gated, ADR-0013):
`SpecializationCache` memoizes the per-term CODEX facts
(`(term, store-generation) → TermFacts`) so repeated resolution against an
unchanged CODEX re-derives nothing. It is **operational, not knowledge**:
the cache is re-derivable, dies with the process, and cannot change a result —
any store mutation bumps `generation` and the cache invalidates itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from kainos.codex.store import CodexStore
from kainos.regex.emitter import emit
from kainos.regex.ir import (
    Alternative,
    Anchor,
    AnchorKind,
    Class,
    ClassKind,
    Group,
    Literal,
    Node,
    Repeat,
    Sequence,
    UnresolvedRef,
)

__all__ = [
    "SpecializationCache",
    "TermFacts",
    "node_from_realization",
    "resolve",
]


@dataclass(frozen=True)
class TermFacts:
    """A term's direct CODEX facts as of one store generation.

    `direct_realizations` are (object value, assertion id) pairs in query
    (assertion-id) order with NO dedup — dedup semantics live in the consumer,
    exactly as in the uncached code path, so cached and uncached results are
    identical by construction.`partner_terms are the term's direct neighbor term
    ids (self excluded) in first-seen order.
    """

    direct_realizations: tuple[tuple[str, str], ...] = ()
    partner_terms: tuple[str, ...] = ()


class SpecializationCache:
    """M1: memoized partial evaluation of `(term, codex-generation) → TermFacts`.

    Morpho analogy: the `jit_runner` materialization registry — compute a
    sub-result once per concrete context signature, cache it, never re-derive.
    Here the "concrete context signature" is the store generation: the CODEX is
    the only input the facts depend on, and `generation` says whether the facts
    are still the facts.
    """

    __slots__ = ("_codex", "_facts", "_generation", "hits", "misses")

    def __init__(self, codex: CodexStore) -> None:
        self._codex = codex
        self._generation: int | None = None
        self._facts: dict[str, TermFacts] = {}
        self.hits = 0
        self.misses = 0

    def term_facts(self, term: str) -> TermFacts:
        generation = self._codex.generation
        if generation != self._generation:  # store mutated (or first use) → re-derive
            self._facts.clear()
            self._generation = generation
        cached = self._facts.get(term)
        if cached is not None:
            self.hits += 1
            return cached
        self.misses += 1
        facts = _compute_facts(self._codex, term)
        self._facts[term] = facts
        return facts

    def stats(self) -> dict:
        return {"hits": self.hits, "misses": self.misses, "terms": len(self._facts)}


def _compute_facts(codex: CodexStore, term: str) -> TermFacts:
    """One term's direct facts, computed the same way the uncached resolver
    always computed them (query + neighbors, no logic change)."""

    realizations: tuple[tuple[str, str], ...] = tuple(
        (a.object_id, a.id) for a in codex.query(subject=term, relation="realizes_as")
    )
    partners: list[str] = []
    for a in codex.neighbors(term, depth=1):
        partner = a.object_id if a.subject.id == term else a.subject.id
        if partner != term and partner not in partners:
            partners.append(partner)
    return TermFacts(direct_realizations=realizations, partner_terms=tuple(partners))


def _facts_for(codex: CodexStore, term: str, cache: SpecializationCache | None) -> TermFacts:
    if cache is not None:
        return cache.term_facts(term)
    return _compute_facts(codex, term)


def node_from_realization(value: str) -> Node:
    """The dialect node whose emission equals a CODEX realization value."""

    if value == emit(Anchor(kind=AnchorKind.start)):
        return Anchor(kind=AnchorKind.start)
    if value == emit(Anchor(kind=AnchorKind.end)):
        return Anchor(kind=AnchorKind.end)
    for kind in ClassKind:
        if emit(Class(kind=kind)) == value:
            return Class(kind=kind)
    # Everything else the CODEX realizes is a regex fragment it TAUGHT (never
    # literal text): it must be emitted verbatim, not escaped.
    return Literal(text=value, raw=True)


def _reachable_realizations(
    codex: CodexStore, candidate: str, cache: SpecializationCache | None
) -> tuple[list[str], list[str]]:
    """(distinct realization values, assertion ids) reachable from a candidate:
    its direct `realizes_as` hits, plus those of its direct neighbors' terms
    (one hop of rotation)."""

    realizations: list[str] = []
    assertion_ids: list[str] = []

    def _absorb(pair: tuple[str, str]) -> None:
        value, aid = pair
        if value not in realizations:
            realizations.append(value)
        if aid not in assertion_ids:
            assertion_ids.append(aid)

    for pair in _facts_for(codex, candidate, cache).direct_realizations:
        _absorb(pair)
    for partner in _facts_for(codex, candidate, cache).partner_terms:
        for pair in _facts_for(codex, partner, cache).direct_realizations:
            _absorb(pair)
    return realizations, assertion_ids


def resolve(
    node: Node, codex: CodexStore, cache: SpecializationCache | None = None
) -> tuple[Node, list[dict]]:
    """Resolve a dialect tree against the CODEX. Returns (resolved_tree, trace) —
    the trace is the audit record: one entry per Class verification and per
    reference rotation (its status: resolved / REQUIRES_CONTEXT / UNSEEN).

    `cache` (M1) is an optional specialization cache shared across resolves on
    the same (unchanged) CODEX; `None` (default) resolves exactly as before.
    """

    trace: list[dict] = []
    return _resolve_node(node, codex, trace, cache), trace


def _resolve_node(
    node: Node, codex: CodexStore, trace: list[dict], cache: SpecializationCache | None
) -> Node:
    if isinstance(node, Class):
        facts = _facts_for(codex, node.kind.value, cache)
        first = facts.direct_realizations[0] if facts.direct_realizations else None
        trace.append(
            {
                "kind": "class",
                "term": node.kind.value,
                "realized_as": first[0] if first else None,
                "assertion_id": first[1] if first else None,
            }
        )
        return node  # a class keeps its semantic identity
    if isinstance(node, UnresolvedRef):
        return _resolve_ref(node, codex, trace, cache)
    if isinstance(node, Sequence):
        return Sequence(
            elements=[_resolve_node(el, codex, trace, cache) for el in node.elements], id=node.id
        )
    if isinstance(node, Alternative):
        return Alternative(
            branches=[_resolve_node(b, codex, trace, cache) for b in node.branches], id=node.id
        )
    if isinstance(node, Repeat):
        return Repeat(node=_resolve_node(node.node, codex, trace, cache), quantifier=node.quantifier, id=node.id)
    if isinstance(node, Group):
        return Group(node=_resolve_node(node.node, codex, trace, cache), id=node.id)
    return node  # Literal / Anchor / Flag: nothing to resolve


def _resolve_ref(
    ref: UnresolvedRef, codex: CodexStore, trace: list[dict], cache: SpecializationCache | None
) -> Node:
    candidates = list(ref.candidates) or [ref.surface]
    realizations: list[str] = []
    assertion_ids: list[str] = []
    via: dict[str, str] = {}
    for cand in candidates:
        reals, ids = _reachable_realizations(codex, cand, cache)
        for r in reals:
            if r not in realizations:
                realizations.append(r)
                via[r] = cand
        assertion_ids.extend(i for i in ids if i not in assertion_ids)

    if len(realizations) == 1:
        value = realizations[0]
        node = node_from_realization(value)
        trace.append(
            {
                "kind": "ref",
                "surface": ref.surface,
                "status": "resolved",
                "resolved_to": f"{type(node).__name__}({value!r})",
                "realization": value,
                "via": via[value],
                "assertion_ids": assertion_ids,
            }
        )
        return node
    if len(realizations) > 1:
        trace.append(
            {
                "kind": "ref",
                "surface": ref.surface,
                "status": "REQUIRES_CONTEXT",
                "candidates": realizations,
                "assertion_ids": assertion_ids,
            }
        )
        return UnresolvedRef(surface=ref.surface, candidates=realizations, id=ref.id)
    trace.append(
        {
            "kind": "ref",
            "surface": ref.surface,
            "status": "UNSEEN",
            "candidates": candidates,
            "assertion_ids": assertion_ids,
        }
    )
    return UnresolvedRef(surface=ref.surface, candidates=list(ref.candidates) or [ref.surface], id=ref.id)
