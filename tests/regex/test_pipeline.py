"""Pipeline tests (P1.07) — end-to-end describe: parse → resolve → emit →
generate → judge. Canonical examples pass with a non-empty audit trace; vague
descriptions escalate instead of emitting a guessed regex.
"""

from __future__ import annotations

import json

import pytest

from kainos.cli import main
from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, Provenance, Source, TermRef
from kainos.regex.emitter import emit
from kainos.regex.ir import UnresolvedRef
from kainos.regex.lexicon import seed
from kainos.regex.pipeline import PipelineResult, describe


@pytest.fixture()
def codex() -> InMemoryCodexStore:
    store = InMemoryCodexStore()
    seed(store)
    return store


# ── canonical / clean descriptions ──────────────────────────────────────────


def test_canonical_example_round_trips(codex):
    result = describe("three digits, then a hyphen", codex)
    assert isinstance(result, PipelineResult)
    assert result.pcre == r"\d{3}-"
    assert result.verdict is not None
    assert result.verdict.ok, result.verdict.summary()
    assert result.escalation is None
    # Audit trace: the digit class was verified against the CODEX. (The hyphen
    # was already resolved at parse time by the kernel's DIRECT lexicon lookup —
    # see tests/lang/test_deterministic.py::test_hyphen_comes_from_the_codex_not_the_parser.)
    kinds = [e["kind"] for e in result.resolved_trace]
    assert kinds == ["class"]
    assert result.resolved_trace[0]["assertion_id"] == "lexicon-digit"
    # The resolved tree is what emits.
    assert emit(result.ir) == result.pcre
    assert result.confidence == 1.0


def test_nl_form_of_canonical_example_2(codex):
    result = describe(
        "ignoring case, three digits, a hyphen, either the literal foo or the literal bar",
        codex,
    )
    assert result.pcre == r"(?i)\d{3}-(?:foo|bar)"
    assert result.verdict is not None and result.verdict.ok, result.verdict.summary()
    assert result.confidence == 1.0


def test_anchored_pattern(codex):
    result = describe("beginning of string, word, end of string", codex)
    assert result.pcre == r"^\w$"
    assert result.verdict is not None and result.verdict.ok, result.verdict.summary()


def test_result_to_dict_is_serializable(codex):
    result = describe("a digit, then a hyphen", codex)
    d = result.to_dict()
    # Round-trips through JSON (it is the CLI wire form).
    assert json.loads(json.dumps(d))["pcre"] == r"\d-"


# ── escalation: never emit what you can't justify ───────────────────────────


def test_vague_description_escalates(codex):
    result = describe("a digit, then the dash thing", codex)
    assert result.pcre is None  # NO guessed regex
    assert result.verdict is None
    assert result.confidence == 0.0
    # The unresolved ref survives in the returned IR (inspectable, not hidden).
    assert result.to_dict()["ir"].get("unresolved", [])[0]["surface"] == "dash thing"
    assert result.escalation is not None
    assert result.escalation["status"] == "requires_context"
    assert result.escalation["recommended_action"] == "ask_human"
    assert "dash" in result.escalation["candidates"]
    statuses = [e["status"] for e in result.resolved_trace if e["kind"] == "ref"]
    assert statuses == ["UNSEEN"]


def test_ambiguous_description_escalates_with_candidates(codex):
    codex.add(
        Assertion(
            id="dash-a",
            subject=TermRef(id="dash", kind="entity", labels=["dash"]),
            relation=TermRef(id="realizes_as", kind="relation", labels=["realizes as"]),
            object="-",
            provenance=Provenance(source=Source(uri="t"), observer="t"),
        )
    )
    codex.add(
        Assertion(
            id="dash-b",
            subject=TermRef(id="dash", kind="entity", labels=["dash"]),
            relation=TermRef(id="realizes_as", kind="relation", labels=["realizes as"]),
            object="–",
            provenance=Provenance(source=Source(uri="t"), observer="t"),
        )
    )
    result = describe("a digit, then the dash thing", codex)
    assert result.pcre is None
    assert result.escalation["status"] == "requires_context"
    assert result.escalation["candidates"] == ["-", "–"]
    statuses = [e["status"] for e in result.resolved_trace if e["kind"] == "ref"]
    assert statuses == ["REQUIRES_CONTEXT"]


def test_ambiguity_resolves_when_one_candidate_survives(codex):
    # Only '-' for dash (no competitor) → resolves, emits, passes.
    codex.add(
        Assertion(
            id="dash-a",
            subject=TermRef(id="dash", kind="entity", labels=["dash"]),
            relation=TermRef(id="realizes_as", kind="relation", labels=["realizes as"]),
            object="-",
            provenance=Provenance(source=Source(uri="t"), observer="t"),
        )
    )
    result = describe("a digit, then the dash thing", codex)
    assert result.pcre == r"\d-"
    assert result.verdict is not None and result.verdict.ok, result.verdict.summary()


# ── unparseable text surfaces as an error, not a guess ──────────────────────


def test_unparseable_text_raises():
    with pytest.raises(ValueError):
        describe("or", codex)


# ── CLI: describe / explain ─────────────────────────────────────────────────


def test_cli_describe_prints_json_result(capsys):
    rc = main(["regex", "describe", "three digits, then a hyphen"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["pcre"] == r"\d{3}-"
    assert out["verdict"]["ok"] is True
    assert out["escalation"] is None
    assert out["confidence"] == 1.0
    assert out["ir"]["meta"]["dialect"] == "kainos/regex/1"


def test_cli_describe_escation_is_a_zero_exit_result(capsys):
    """Escalation is a valid RESULT (ask-human), not a CLI error."""

    rc = main(["regex", "describe", "a digit, then the dash thing"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["pcre"] is None
    assert out["escalation"]["recommended_action"] == "ask_human"


def test_cli_describe_bad_text_is_exit_1(capsys):
    assert main(["regex", "describe", "or"]) == 1
    assert "could not parse" in capsys.readouterr().err


def test_cli_explain_prints_ir_trace_pcre_verdict(capsys):
    rc = main(["regex", "explain", "beginning of string, word, end of string"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "IR (resolved dialect tree" in out
    assert "Resolved trace:" in out
    assert "PCRE: ^\\w$" in out
    assert "Verdict: PASS" in out
    assert "Confidence: 1.00" in out


def test_cli_sqlite_codex_flag(tmp_path, capsys):
    """--codex uses the given (seeded) sqlite CODEX and persists nothing else."""

    from kainos.codex.sqlite import SqliteCodexStore

    db = str(tmp_path / "codex.sqlite")
    store = SqliteCodexStore(db)
    seed(store)
    store.close()
    rc = main(["regex", "describe", "a digit, then a hyphen", "--codex", db])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["pcre"] == r"\d-"
    assert out["verdict"]["ok"] is True


def test_pipeline_uses_passed_codex_not_default():
    """An explicit codex is authoritative: an unseeded store ⇒ no hyphen, ⇒ escalation."""

    result = describe("a hyphen", InMemoryCodexStore())
    assert result.pcre is None
    assert result.escalation is not None
    assert isinstance(result.ir, UnresolvedRef)
