"""Seed corpus tests (P1.08) — shape validation, operator coverage (every
operator must be present), and pure-data semantics: every authored
expected_pcre must already be a correct PCRE for its own examples."""

from __future__ import annotations

import json
import re

import pytest

from kainos.regex.bench import default_corpus_path
from kainos.regex.data import load_corpus
from kainos.regex.judge import judge

CORPUS = default_corpus_path()


@pytest.fixture(scope="module")
def records() -> list[dict]:
    return load_corpus(CORPUS)


# ── shape ───────────────────────────────────────────────────────────────────


def test_corpus_loads_and_is_nontrivial(records):
    assert 40 <= len(records) <= 80, f"corpus size {len(records)} outside the 40-80 directive band"


def test_corpus_records_have_nonempty_examples(records):
    for rec in records:
        assert rec["positive"], rec["id"]
        assert rec["negative"], rec["id"]


def test_canonical_examples_present(records):
    by_id = {r["id"]: r for r in records}
    assert by_id["canon_1"]["expected_pcre"] == r"\d{3}-"
    assert by_id["canon_2"]["expected_pcre"] == r"(?i)\d{3}-(?:foo|bar)"


# ── operator coverage (directive DoD: "all operators present") ─────────────

# Detection over the authored expected_pcres (Python regex on PCRE text — the
# corpus is what is under test, not the pipeline).
_COVERAGE: dict[str, str] = {
    "quantifier_one_or_more": r"(?<!\\)\+",
    "quantifier_zero_or_more": r"(?<!\\)\*",
    "quantifier_optional": r"(?<!\\)\?",
    "quantifier_exactly": r"\{[1-9]\d*\}",
    "quantifier_at_least": r"\{\d+,\}",
    "quantifier_at_most": r"\{0,[1-9]\d*\}",
    "quantifier_between": r"\{[1-9]\d*,\d+\}",
    "class_digit": r"\\d",
    "class_letter": r"\[A-Za-z\]",
    "class_word": r"\\w",
    "class_whitespace": r"\\s",
    "class_any": r"(?<!\\)\.",
    "anchor_start": r"(?<!\\)\^",
    "anchor_end": r"(?<!\\)\$",
    "literal_escaped_metachar": r"\\[\.\^\$\*\+\?\(\)\[\]\{\}\\\\\|]",
    "alternative": r"\|",
    "flag_case_insensitive": r"\(\?i\)",
}


def test_every_operator_is_covered(records):
    found = {
        name
        for name, pat in _COVERAGE.items()
        if any(re.search(pat, r["expected_pcre"]) for r in records)
    }
    missing = set(_COVERAGE) - found
    assert not missing, f"corpus lacks operator coverage: {sorted(missing)}"


def test_group_operator_is_covered(records):
    # Group has no PCRE signature distinct from alternative wrapping, so it is
    # asserted on the description form the parser accepts.
    assert any("group of" in r["description"] for r in records)


def test_corpus_respects_the_group_scope_ambiguity():
    """The grammar's documented binding: 'group of' extends through the rest of
    the current alternative branch, so 'either a group of X or Y' lets the group
    swallow the 'or' and the text is rejected rather than guessed. The corpus
    must never rely on the other grouping — pin the rejection."""

    from kainos.lang.deterministic import parse_regex_text

    with pytest.raises(ValueError):
        parse_regex_text("either a group of a digit or a letter")
    # The unambiguous variant (branch before the group) parses and emits cleanly.
    from kainos.regex.emitter import emit

    node = parse_regex_text("either a letter or a group of a letter and a space")
    assert emit(node) == r"(?:[A-Za-z]|(?:[A-Za-z]\s))"


def test_every_record_passes_its_own_judge(records):
    """Pure-data check (no pipeline involved): the authored expected PCRE must
    already be a correct pattern for the authored examples under Perl."""

    for rec in records:
        verdict = judge(rec["expected_pcre"], rec["positive"], rec["negative"])
        assert verdict.ok, f"{rec['id']}: {verdict.summary()}"


# ── load_corpus validation ──────────────────────────────────────────────────


def _write(tmp_path, lines: list[dict]) -> str:
    p = tmp_path / "corpus.jsonl"
    p.write_text("\n".join(json.dumps(l) for l in lines) + "\n", encoding="utf-8")
    return str(p)


def _rec(**over) -> dict:
    base = {
        "id": "x",
        "description": "a digit",
        "expected_pcre": r"\d",
        "positive": ["1"],
        "negative": ["a"],
    }
    base.update(over)
    return base


def test_load_corpus_rejects_missing_key(tmp_path):
    rec = _rec()
    del rec["negative"]
    with pytest.raises(ValueError, match="missing"):
        load_corpus(_write(tmp_path, [rec]))


def test_load_corpus_rejects_empty_examples(tmp_path):
    with pytest.raises(ValueError, match="non-empty"):
        load_corpus(_write(tmp_path, [_rec(negative= [])]))
    with pytest.raises(ValueError, match="non-empty"):
        load_corpus(_write(tmp_path, [_rec(positive= [])]))


def test_load_corpus_rejects_duplicate_ids(tmp_path):
    with pytest.raises(ValueError, match="duplicate"):
        load_corpus(_write(tmp_path, [_rec(), _rec()]))


def test_load_corpus_rejects_bad_json(tmp_path):
    p = tmp_path / "bad.jsonl"
    p.write_text('{"id": "oops"\n', encoding="utf-8")
    with pytest.raises(ValueError, match="valid JSON"):
        load_corpus(str(p))
