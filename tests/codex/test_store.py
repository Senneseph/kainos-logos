"""Store tests (action-step 02 §6) — run against BOTH implementations.

The parametrized fixtures cover the directive's required scenarios (relation
query, the disputed pair surviving in both stores); the scenario-diff at the
bottom enforces the Phase 0 exit criterion "store parity": the same operation
script must produce identical results on SQLite and in memory.
"""

from __future__ import annotations

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    ExceptionState,
    Interval,
)
from kainos.codex.sqlite import SqliteCodexStore
from tests.codex.helpers import (
    make_assertion,
    make_provenance,
    make_term,
)

STORE_IMPLS = [SqliteCodexStore, InMemoryCodexStore]
STORE_IDS = ["sqlite", "memory"]


@pytest.fixture(params=STORE_IMPLS, ids=STORE_IDS)
def store(request) -> SqliteCodexStore | InMemoryCodexStore:
    impl = request.param
    s: SqliteCodexStore | InMemoryCodexStore = (
        SqliteCodexStore(":memory:") if impl is SqliteCodexStore else InMemoryCodexStore()
    )
    yield s
    if isinstance(s, SqliteCodexStore):
        s.close()


# ── the directive's required scenarios ─────────────────────────────────────


def test_add_and_query_by_relation(store):
    store.add(make_assertion("a1", "France", "CAPITAL_OF", "Paris"))
    store.add(make_assertion("a2", "Germany", "CAPITAL_OF", "Berlin"))
    got = store.query(relation="CAPITAL_OF")
    assert {a.id for a in got} == {"a1", "a2"}
    assert len(got) == 2


def test_disputed_pair_survives_in_both_stores(store):
    """Invariant #6: contradictions are preserved, never averaged."""

    store.add(
        make_assertion(
            "cap-paris",
            "France",
            "CAPITAL_OF",
            "Paris",
            status=EpistemicState.established,
        )
    )
    store.add(
        make_assertion(
            "cap-lyon",
            "France",
            "CAPITAL_OF",
            "Lyon",
            status=EpistemicState.disputed,
            exception=ExceptionState.conflicting,
        )
    )
    got = store.query(subject="France", relation="CAPITAL_OF")
    assert len(got) == 2
    assert {a.object_id for a in got} == {"Paris", "Lyon"}
    # Both original statuses are intact.
    by_id = {a.id: a for a in got}
    assert by_id["cap-paris"].status is EpistemicState.established
    assert by_id["cap-lyon"].status is EpistemicState.disputed
    assert by_id["cap-lyon"].exception is ExceptionState.conflicting


# ── query filters ──────────────────────────────────────────────────────────


def _seeded() -> dict[str, Assertion]:
    return {
        "a1": make_assertion(
            "a1",
            "France",
            "CAPITAL_OF",
            make_term("Paris", kind="entity"),
            context={"country_code": "FR", "domain": "geography"},
            validity=Interval(from_="2024-01-01", to="2025-01-01"),
            status=EpistemicState.established,
            provenance=make_provenance(verified=True),
        ),
        "a2": make_assertion(
            "a2",
            "France",
            "CAPITAL_OF",
            "Lyon",
            validity=Interval(from_="2020-01-01", to="2020-12-31"),
            status=EpistemicState.disputed,
        ),
        "a3": make_assertion(
            "a3",
            "Government",
            "SEAT_OF",
            make_term("Paris", kind="entity"),
            context={"domain": "politics"},
        ),
    }


@pytest.fixture()
def seeded(store) -> dict[str, Assertion]:
    for a in _seeded().values():
        store.add(a)
    return _seeded()


def test_query_object_matches_str_and_termref_by_id(store, seeded):
    # "Lyon" is stored as a raw string, "Paris" as a TermRef — one filter for both.
    got = store.query(object="Paris")
    assert {a.id for a in got} == {"a1", "a3"}
    assert {a.id for a in store.query(object="Lyon")} == {"a2"}


def test_query_status_filter(store, seeded):
    assert {a.id for a in store.query(status=EpistemicState.disputed)} == {"a2"}
    assert {a.id for a in store.query(status="established")} == {"a1"}


def test_query_context_match(store, seeded):
    assert {a.id for a in store.query(context_match={"country_code": "FR"})} == {"a1"}
    assert {a.id for a in store.query(context_match={"domain": "politics"})} == {"a3"}
    # Non-matching context.
    assert store.query(context_match={"country_code": "DE"}) == []


def test_query_time_at_inclusive_open_ended(store, seeded):
    # a1: 2024-01-01..2025-01-01, a2: 2020 window, a3: open-ended (no validity).
    got = [a.id for a in store.query(time_at="2024-06-01")]
    assert set(got) == {"a1", "a3"}
    # Inclusive bounds.
    assert {a.id for a in store.query(time_at="2024-01-01", subject="France")} == {"a1"}
    assert {a.id for a in store.query(time_at="2025-01-01", subject="France")} == {"a1"}
    assert store.query(time_at="2025-01-02", subject="France") == []


def test_query_combines_filters_and_orders_by_id(store, seeded):
    assert [a.id for a in store.query(subject="France", relation="CAPITAL_OF")] == ["a1", "a2"]


# ── update_status ──────────────────────────────────────────────────────────


def test_update_status_and_evidence(store, seeded):
    store.update_status("a2", EpistemicState.contradicted, evidence=["e-ext-42"])
    a2 = next(a for a in store.query() if a.id == "a2")
    assert a2.status is EpistemicState.contradicted
    assert a2.provenance.evidence == ["e-ext-42"]
    # Appending dedupes and preserves order.
    store.update_status("a2", EpistemicState.contradicted, evidence=["e-ext-42", "e-ext-43"])
    a2 = next(a for a in store.query() if a.id == "a2")
    assert a2.provenance.evidence == ["e-ext-42", "e-ext-43"]
    # Without evidence arg the list is untouched.
    store.update_status("a2", EpistemicState.disputed)
    a2 = next(a for a in store.query() if a.id == "a2")
    assert a2.provenance.evidence == ["e-ext-42", "e-ext-43"]


def test_update_status_unknown_id_raises(store, seeded):
    with pytest.raises(KeyError):
        store.update_status("nope", EpistemicState.established)


# ── graph primitives ───────────────────────────────────────────────────────


def test_neighbors_depth(store, seeded):
    # Direct: France touches a1, a2.
    assert {a.id for a in store.neighbors("France", 1)} == {"a1", "a2"}
    # Two hops from Paris: a1, a3 (direct) + a2 (via France).
    assert {a.id for a in store.neighbors("Paris", 2)} == {"a1", "a2", "a3"}
    # Depth bounds the search.
    assert {a.id for a in store.neighbors("Paris", 1)} == {"a1", "a3"}
    assert store.neighbors("Nowhere", 5) == []


def test_rotate_returns_partner_terms(store, seeded):
    partners = {t.id for t in store.rotate("France")}
    assert partners == {"Paris", "Lyon"}


def test_coverage_verified_over_encountered(store, seeded):
    # France: (CAPITAL_OF, Paris) verified + (CAPITAL_OF, Lyon) unverified -> 0.5
    assert store.coverage("France") == 0.5
    # Government: only (SEAT_OF, Paris), unverified -> 0.0
    assert store.coverage("Government") == 0.0
    # Paris: (CAPITAL_OF, France) verified + (SEAT_OF, Government) not -> 0.5
    assert store.coverage("Paris") == 0.5
    # Empty store analogue: unknown term -> 0.0
    assert store.coverage("Nowhere") == 0.0
    # Context filter: only the geography assertions count.
    assert store.coverage("France", context=Context(data={"country_code": "FR"})) == 1.0


def test_dump_deterministic(store, seeded):
    d1, d2 = store.dump(), store.dump()
    assert d1 == d2
    assert [t["id"] for t in d1["terms"]] == sorted(t["id"] for t in d1["terms"])
    assert [a["id"] for a in d1["assertions"]] == ["a1", "a2", "a3"]


# ── explain (inspectability spine, invariant #9) ───────────────────────────


def test_explain_chain_with_missing_and_circular(store, seeded):
    """Wiring check: store.explain delegates to the shared module (tests/codex/test_explain.py)."""
    # Missing evidence renders as {"id": ..., "missing": true} — never raises.
    store.update_status("a2", EpistemicState.contradicted, evidence=["e-missing-42"])
    ex = store.explain("a2")
    assert ex["id"] == "a2"
    assert ex["assertion"]["id"] == "a2"
    assert ex["provenance"]["evidence"] == ["e-missing-42"]
    assert ex["chain"] == [{"id": "e-missing-42", "missing": True}]

    # Nested chain: a derived assertion citing a1 (which cites nothing).
    store.add(
        make_assertion(
            "a4",
            "Paris",
            "IS_IN",
            "France",
            status=EpistemicState.hypothesis,
            provenance=make_provenance(derived=True, evidence=["a1"]),
        )
    )
    ex4 = store.explain("a4")
    assert ex4["chain"][0]["id"] == "a1"
    assert ex4["chain"][0]["assertion"]["id"] == "a1"
    assert ex4["chain"][0]["chain"] == []

    # Cycle: a5 <-> a6 terminates with a circular marker.
    store.add(
        make_assertion(
            "a5",
            "S5",
            "LINK",
            "T5",
            provenance=make_provenance(evidence=["a6"]),
        )
    )
    store.add(
        make_assertion(
            "a6",
            "S6",
            "LINK",
            "T6",
            provenance=make_provenance(evidence=["a5"]),
        )
    )
    ex5 = store.explain("a5")
    assert ex5["chain"][0]["id"] == "a6"
    assert ex5["chain"][0]["chain"][0] == {"id": "a5", "circular": True}

    # Unknown top-level id also renders, never raises.
    assert store.explain("nope") == {"id": "nope", "missing": True}


# ── store parity (Phase 0 exit criterion) ──────────────────────────────────


def _run_scenario(impl) -> dict:
    """Run one fixed operation script; return its full observable behavior."""

    s: SqliteCodexStore | InMemoryCodexStore = (
        SqliteCodexStore(":memory:") if impl is SqliteCodexStore else InMemoryCodexStore()
    )
    results: dict = {}
    for a in _seeded().values():
        s.add(a)
    assert s.add(_seeded()["a1"]) == "a1"  # upsert idempotent
    s.update_status("a2", EpistemicState.contradicted, evidence=["e1", "e2"])
    s.update_status("a3", EpistemicState.established, evidence=["e2"])
    s.add(
        make_assertion(
            "a7",
            "Paris",
            "BOUNDED_BY",
            "Seine",
            provenance=make_provenance(evidence=["a1", "missing-x"]),
        )
    )
    results["query_all"] = [a.to_dict() for a in s.query()]
    results["query_relation"] = [a.to_dict() for a in s.query(relation="CAPITAL_OF")]
    results["query_object_paris"] = [a.id for a in s.query(object="Paris")]
    results["query_ctx"] = [a.id for a in s.query(context_match={"domain": "geography"})]
    results["query_time"] = [a.id for a in s.query(time_at="2024-06-01")]
    results["neighbors_paris_2"] = [a.to_dict() for a in s.neighbors("Paris", 2)]
    results["neighbors_france_1"] = [a.id for a in s.neighbors("France", 1)]
    results["rotate_france"] = [t.to_dict() for t in s.rotate("France")]
    results["coverage"] = {t: s.coverage(t) for t in ("France", "Paris", "Government", "Seine", "Nowhere")}
    results["coverage_ctx"] = s.coverage("France", context=Context(data={"country_code": "FR"}))
    results["dump"] = s.dump()
    results["explain_a2"] = s.explain("a2")
    results["explain_a7"] = s.explain("a7")
    results["explain_missing"] = s.explain("never-existed")
    if isinstance(s, SqliteCodexStore):
        s.close()
    return results


def test_store_parity_sqlite_matches_memory():
    by_impl = {k.__name__: _run_scenario(k) for k in STORE_IMPLS}
    sqlite_r, memory_r = by_impl["SqliteCodexStore"], by_impl["InMemoryCodexStore"]
    assert list(sqlite_r.keys()) == list(memory_r.keys())
    for key in sqlite_r:
        assert sqlite_r[key] == memory_r[key], f"store parity violation: {key}"
