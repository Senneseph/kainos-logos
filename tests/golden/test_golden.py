"""Golden serialization tests (P0.06) — byte-stable; fail if a field drifts.

The CODEX golden (``tests/codex/golden/dump.json``) is the exact
``store.dump()`` of the pinned fixture below (generated in-container via
``tests.golden.test_golden.golden_assertions``); comparison is exact JSON string
equality over ``sort_keys=True`` serialization, on BOTH store implementations
(a golden drift in either impl fails here).
"""

from __future__ import annotations

import json
from pathlib import Path

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
from kainos.ir.codec import dump, load
from tests.codex.helpers import make_provenance, make_term

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DUMP = REPO_ROOT / "tests" / "codex" / "golden" / "dump.json"
GOLDEN_IR = REPO_ROOT / "tests" / "ir" / "golden" / "minimal.json"


def golden_assertions() -> list[Assertion]:
    """The pinned fixture the dump.json golden was generated from.

    Covers the shapes a drift must catch: TermRef vs raw-str object, two
    epistemic statuses, context, validity interval, exception state, verified
    provenance.
    """
    return [
        Assertion(
            id="france-capital-paris",
            subject=make_term("France", kind="entity", labels=["France"]),
            relation=make_term("CAPITAL_OF", kind="relation", labels=["capital of"]),
            object=make_term("Paris", kind="entity", labels=["Paris"]),
            polarity=True,
            context=Context(data={"country_code": "FR", "domain": "geography"}),
            validity=Interval(from_="2024-01-01", to="2025-01-01"),
            confidence=0.95,
            status=EpistemicState.established,
            provenance=make_provenance(
                uri="https://example.org/geography/v1", observer="golden", verified=True
            ),
            exception=None,
        ),
        Assertion(
            id="france-capital-lyon",
            subject=make_term("France", kind="entity", labels=["France"]),
            relation=make_term("CAPITAL_OF", kind="relation", labels=["capital of"]),
            object="Lyon",  # raw string object — not a term row
            polarity=True,
            context=Context(data={"domain": "geography"}),
            validity=None,
            confidence=0.4,
            status=EpistemicState.disputed,
            provenance=make_provenance(uri="https://example.org/geography/v1", observer="golden"),
            exception=ExceptionState.conflicting,
        ),
    ]


STORE_IMPLS = [SqliteCodexStore, InMemoryCodexStore]
STORE_IDS = ["sqlite", "memory"]


def _normalized(data: object) -> str:
    return json.dumps(data, sort_keys=True)


@pytest.fixture(params=STORE_IMPLS, ids=STORE_IDS)
def store(request) -> SqliteCodexStore | InMemoryCodexStore:
    impl = request.param
    s: SqliteCodexStore | InMemoryCodexStore = (
        SqliteCodexStore(":memory:") if impl is SqliteCodexStore else InMemoryCodexStore()
    )
    yield s
    if isinstance(s, SqliteCodexStore):
        s.close()


def test_codex_dump_matches_golden(store):
    for a in golden_assertions():
        store.add(a)
    got = _normalized(store.dump())
    want = _normalized(json.loads(GOLDEN_DUMP.read_text(encoding="utf-8")))
    assert got == want, "CODEX golden drift: a model/store field changed — update the golden deliberately"


def test_ir_golden_round_trip_is_byte_stable():
    raw_text = GOLDEN_IR.read_text(encoding="utf-8")
    raw = json.loads(raw_text)
    assert _normalized(dump(load(raw))) == _normalized(raw)


def test_golden_dump_file_is_itself_canonical():
    """The committed file must be stable under its own normalization (no reformat churn)."""

    text = GOLDEN_DUMP.read_text(encoding="utf-8")
    assert text == json.dumps(json.loads(text), indent=2, sort_keys=True) + "\n"
