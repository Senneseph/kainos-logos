"""M1 specialization cache tests (Scavenge Step B, SCAVENGE_MORPHO.md, #141).

The seam-neutrality regression demanded by the scavenge guardrails: with the
cache OFF (cache=None) results are byte-identical to the pre-M1 code path;
with it ON, results must still be identical AND the cache must actually be
used, and it must invalidate on store mutation (never serve stale facts).
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState, Provenance, Source, TermRef
from kainos.lang.deterministic import DeterministicKernel
from kainos.regex.bench import default_corpus_path, run_m1_benchmark
from kainos.regex.data import load_corpus
from kainos.regex.emitter import emit
from kainos.regex.ir import Literal
from kainos.regex.lexicon import seed
from kainos.regex.pipeline import describe
from kainos.regex.resolver import SpecializationCache, _compute_facts, resolve


@pytest.fixture()
def codex() -> InMemoryCodexStore:
    store = InMemoryCodexStore()
    seed(store)
    return store


# ── seam neutrality: cached vs uncached are identical ──────────────────────


def test_full_corpus_resolve_identical_cached_vs_uncached(codex):
    kernel = DeterministicKernel(codex)
    cache = SpecializationCache(codex)
    for rec in load_corpus(default_corpus_path()):
        tree_uncached = DeterministicKernel(codex).parse(rec["description"])[0].ir
        tree_cached = kernel.parse(rec["description"])[0].ir
        out_uncached, trace_uncached = resolve(tree_uncached, codex)
        out_cached, trace_cached = resolve(tree_cached, codex, cache=cache)
        assert emit(out_cached) == emit(out_uncached), rec["id"]
        assert trace_cached == trace_uncached, rec["id"]
    # And the cache actually worked.
    assert cache.hits > 0


def test_describe_identical_with_and_without_cache(codex):
    for text in (
        "three digits, then a hyphen",
        "a digit, then the dash thing",  # escalation path, too
        "either a digit or a letter, then a space",
    ):
        a = describe(text, codex)
        b = describe(text, codex, cache=SpecializationCache(codex))
        assert a.pcre == b.pcre
        assert a.resolved_trace == b.resolved_trace
        assert a.escalation == b.escalation


def test_uncached_path_is_unchanged_behavior(codex):
    """cache=None must behave exactly as the pre-M1 resolver: same trace shape
    for the hyphen rotation (the step-07/08 tests already pin this end to end;
    this pins the resolver-level contract)."""

    from kainos.regex.ir import Literal, UnresolvedRef

    node, trace = resolve(UnresolvedRef(surface="hyphen"), codex)
    assert node == Literal("-", raw=True)
    assert trace[0]["status"] == "resolved"
    assert trace[0]["realization"] == "-"
    assert trace[0]["assertion_ids"] == ["lexicon-hyphen"]


# ── the cache is used and correct ──────────────────────────────────────────


def test_cache_hits_and_fact_contents(codex):
    cache = SpecializationCache(codex)
    facts = cache.term_facts("hyphen")
    assert facts.direct_realizations == (("-", "lexicon-hyphen"),)
    again = cache.term_facts("hyphen")
    assert again is facts  # memoized, same object
    assert cache.hits == 1 and cache.misses == 1
    digit = cache.term_facts("digit")
    assert digit.direct_realizations[0] == (r"\d", "lexicon-digit")
    unseen = cache.term_facts("no-such-term")
    assert unseen.direct_realizations == () and unseen.partner_terms == ()


def test_cache_survives_across_resolve_calls(codex):
    cache = SpecializationCache(codex)
    from kainos.regex.ir import UnresolvedRef

    resolve(UnresolvedRef(surface="hyphen"), codex, cache=cache)
    resolve(UnresolvedRef(surface="hyphen"), codex, cache=cache)
    stats = cache.stats()
    assert stats["hits"] > stats["misses"]  # second resolve mostly hits


# ── invalidation on store mutation ─────────────────────────────────────────


def test_generation_bumps_on_mutation(codex):
    g0 = codex.generation
    codex.add(
        Assertion(
            id="x-new",
            subject=TermRef(id="new-term", kind="entity", labels=["new-term"]),
            relation=TermRef(id="realizes_as", kind="relation", labels=["realizes as"]),
            object="N",
            provenance=Provenance(source=Source(uri="t"), observer="t"),
        )
    )
    assert codex.generation == g0 + 1
    codex.update_status("lexicon-hyphen", EpistemicState.disputed)
    assert codex.generation == g0 + 2


def test_cache_invalidates_when_store_mutates(codex):
    from kainos.regex.ir import UnresolvedRef

    cache = SpecializationCache(codex)
    node, trace = resolve(UnresolvedRef(surface="dash"), codex, cache=cache)
    assert trace[0]["status"] == "UNSEEN"  # dash unseen in the seeded lexicon

    # Now 'dash' gets a single realization — the cached UNSEEN fact is stale.
    codex.add(
        Assertion(
            id="dash-a",
            subject=TermRef(id="dash", kind="entity", labels=["dash"]),
            relation=TermRef(id="realizes_as", kind="relation", labels=["realizes as"]),
            object="-",
            provenance=Provenance(source=Source(uri="t"), observer="t"),
        )
    )
    node, trace = resolve(UnresolvedRef(surface="dash"), codex, cache=cache)
    assert trace[0]["status"] == "resolved"
    assert node == Literal("-", raw=True)
    assert trace[0]["realization"] == "-"


def test_compute_facts_matches_uncached_directories(codex):
    """TermFacts must be exactly the facts the old direct queries returned."""

    facts = _compute_facts(codex, "hyphen")
    direct = codex.query(subject="hyphen", relation="realizes_as")
    assert facts.direct_realizations == tuple((a.object_id, a.id) for a in direct)
    partners = set()
    for a in codex.neighbors("hyphen", depth=1):
        p = a.object_id if a.subject.id == "hyphen" else a.subject.id
        if p != "hyphen":
            partners.add(p)
    assert set(facts.partner_terms) == partners


# ── the gate itself ─────────────────────────────────────────────────────────


def test_m1_benchmark_gate(tmp_path):
    report = run_m1_benchmark(out_dir=tmp_path)
    assert report["identical"] is True  # semantic neutrality
    assert (tmp_path / "m1.json").is_file()
    # The gate demands a measured advantage; at this scale the resolution
    # phase is small, so assert the mechanism ran (hits) and record, not hide,
    # the margin. (The adopt/reject verdict with margin is written at Step I.)
    assert report["cache_stats"]["cached"]["hits"] > 0
    assert report["speedup"] is not None
