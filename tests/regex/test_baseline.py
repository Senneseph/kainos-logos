"""DirectBaseline tests (P1.11) — the no-CODEX stand-in succeeds on what the
grammar natively expresses and fails (honestly, with a note) wherever a CODEX
lookup is required.
"""

from __future__ import annotations

from kainos.regex.baseline import DirectBaseline


def test_baseline_solves_pure_grammar_descriptions():
    b = DirectBaseline()
    assert b.solve("a digit, then a letter").pcre == r"\d[A-Za-z]"
    assert b.solve("either a digit or a letter").pcre == r"(?:\d|[A-Za-z])"
    assert b.solve("start of string, one or more digits, end of string").pcre == r"^\d+$"
    assert b.solve("the literal foo, then a space").pcre == r"foo\s"


def test_baseline_fails_on_codex_content_words_with_note():
    b = DirectBaseline()
    result = b.solve("three digits, then a hyphen")
    assert result.pcre is None
    assert "hyphen" in result.note.lower()


def test_baseline_failure_is_honest_not_guessed():
    """The baseline never emits a PCRE for a description it cannot fully
    resolve — even a prefix that looks resolvable must not be emitted."""

    b = DirectBaseline()
    result = b.solve("a hyphen, then a digit")
    assert result.pcre is None  # not "\-\d", not "-", not anything


def test_baseline_unparseable_text_is_a_failure_not_a_crash():
    b = DirectBaseline()
    result = b.solve("or")
    assert result.pcre is None
    assert "unparseable" in result.note
