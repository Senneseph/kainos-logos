"""C2 (P1.12) — persistent memory.

A CODEX entry survives a full restart of the pipeline and is reused with the
kernel unchanged ("frozen weights": the deterministic kernel has no weights at
all — everything that changes across the restart is CODEX state, invariant #2).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion
from kainos.regex.bench import (
    PHONE_DESCRIPTION,
    PHONE_PATTERN,
    _describe_digest,
    run_e1_3,
    teach_phone_number,
)
from kainos.regex.judge import judge
from kainos.regex.lexicon import seed
from kainos.regex.pipeline import describe


@pytest.fixture(scope="module")
def seeded() -> InMemoryCodexStore:
    store = InMemoryCodexStore()
    seed(store)
    return store


def test_phone_number_unknown_before_teaching(seeded):
    digest = _describe_digest(PHONE_DESCRIPTION, seeded)
    assert digest["pcre"] is None
    assert digest["escalation"] is not None
    assert digest["escalation"]["recommended_action"] == "ask_human"


def test_teaching_makes_describe_succeed_and_traces_provenance(seeded):
    teach_phone_number(seeded)
    digest = _describe_digest(PHONE_DESCRIPTION, seeded)
    assert digest["pcre"] == PHONE_PATTERN
    # The trace names the exact CODEX assertion that supplied the pattern.
    ref_entries = [t for t in digest["trace"] if t.get("kind") == "ref"]
    assert any(
        t.get("status") == "resolved" and "taught-us-phone-number" in t.get("assertion_ids", [])
        for t in ref_entries
    )


def test_restart_preserves_the_taught_fact():
    """dump -> fresh store (rebuilt from plain dicts) -> fresh pipeline -> same pcre."""

    store = InMemoryCodexStore()
    seed(store)
    teach_phone_number(store)

    dump = store.dump()
    assert "assertions" in dump and "terms" in dump  # plain dicts, serializable
    json.dumps(dump)  # must survive JSON round-trip (disk-shaped)

    fresh = InMemoryCodexStore()
    for record in dump["assertions"]:
        fresh.add(Assertion.from_dict(record))

    result = describe(PHONE_DESCRIPTION, fresh)
    assert result.pcre == PHONE_PATTERN
    assert result.escalation is None


def test_learned_pattern_is_a_real_regex_not_escaped_text():
    """The taught realization is a raw regex fragment: it must MATCH phone
    numbers (a wrongly escaped literal would not)."""

    store = InMemoryCodexStore()
    seed(store)
    teach_phone_number(store)
    result = describe(PHONE_DESCRIPTION, store)
    assert result.pcre is not None
    verdict = judge(result.pcre, ["555-123-4567"], ["555-123-456", "5551234567"])
    assert verdict.ok, verdict.summary()


def test_explain_shows_user_instruction_provenance(seeded):
    explain = seeded.explain("taught-us-phone-number")
    text = explain if isinstance(explain, str) else json.dumps(explain, default=str)
    assert "user_instruction" in text
    # the JSON dump escapes the backslashes — unescape before comparing
    assert PHONE_PATTERN in text.replace("\\\\", "\\")


def test_run_e1_3_end_to_end(tmp_path: Path):
    report = run_e1_3(out_dir=tmp_path)
    assert report["passed"] is True
    assert report["before"]["pcre"] is None
    assert report["after"]["pcre"] == PHONE_PATTERN
    assert report["after_restart"]["pcre"] == PHONE_PATTERN
    assert report["assertion_present"] is True
    assert (tmp_path / "e1.3.json").is_file()
