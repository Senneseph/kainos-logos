"""Testgen + judge tests (P1.06-P1.07) — every operator covered, deterministic
output, useful diffs, and the judge as objective arbiter (Perl, ADR-0009).
"""

from __future__ import annotations

import pytest

from kainos.regex.emitter import emit
from kainos.regex.ir import (
    Alternative,
    Anchor,
    AnchorKind,
    Class,
    ClassKind,
    Flag,
    Group,
    Literal,
    Quantifier,
    Repeat,
    Sequence,
    UnresolvedRef,
)
from kainos.regex.judge import Verdict, judge
from kainos.regex.testgen import generate


def _pcre(tree) -> str:
    return emit(tree)


# ── determinism ─────────────────────────────────────────────────────────────


def test_generate_is_deterministic_under_seed():
    tree = Sequence(
        [
            Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.between(2, 4)),
            Literal("-"),
            Alternative([Class(ClassKind.letter), Literal("z")]),
        ]
    )
    for seed in (0, 7, 42):
        a = generate(tree, seed=seed)
        b = generate(tree, seed=seed)
        assert a == b, f"seed {seed} is not deterministic"
    # Different seeds may (not must) differ — same seed always agrees (above).


def test_generate_covers_every_operator():
    """One tree using every node kind: both example lists are non-empty, and the
    JUDGE agrees with the intended language (all positives match, no negative
    matches). The judge is the proof that the examples mean anything."""

    tree = Sequence(
        [
            Anchor(kind=AnchorKind.start),
            Flag("case_insensitive"),
            Literal("ab"),
            Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.exactly(2)),
            Repeat(node=Class(ClassKind.whitespace), quantifier=Quantifier.optional()),
            Alternative([Group(node=Class(ClassKind.letter)), Literal("Z")]),
            Anchor(kind=AnchorKind.end),
        ]
    )
    pos, neg = generate(tree, seed=1)
    assert len(pos) >= 1 and all(isinstance(s, str) for s in pos)
    assert len(neg) >= 1
    # Every example string is distinct.
    assert len(set(pos)) == len(pos)
    verdict = judge(_pcre(tree), pos, neg)
    assert verdict.ok, verdict.summary()


@pytest.mark.parametrize(
    "quant",
    [
        Quantifier.one_or_more(),
        Quantifier.zero_or_more(),
        Quantifier.optional(),
        Quantifier.exactly(3),
        Quantifier.at_least(2),
        Quantifier.at_most(4),
        Quantifier.between(1, 3),
    ],
    ids=["one_or_more", "zero_or_more", "optional", "exactly", "at_least", "at_most", "between"],
)
def test_every_quantifier_passes_its_own_judge(quant):
    tree = Repeat(node=Class(ClassKind.digit), quantifier=quant)
    pos, neg = generate(tree, seed=0)
    assert len(pos) >= 1 and len(neg) >= 1
    verdict = judge(_pcre(tree), pos, neg)
    assert verdict.ok, f"{quant.kind.value}: {verdict.summary()}"


# ── the judge: objective arbiter ────────────────────────────────────────────


def test_judge_accepts_a_correct_pattern():
    tree = Sequence([Literal("cat"), Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.one_or_more())])
    pos, neg = generate(tree, seed=0)
    verdict = judge(_pcre(tree), pos, neg)
    assert verdict.ok
    assert verdict.summary().startswith("PASS")


def test_judge_rejects_a_wrong_regex_with_useful_diff():
    """Deliberate sabotage: 'cat\\D+' where the language is 'cat\\d+'."""

    tree = Sequence([Literal("cat"), Repeat(node=Class(ClassKind.digit), quantifier=Quantifier.one_or_more())])
    pos, neg = generate(tree, seed=0)
    verdict = judge("cat\\D+", pos, neg)
    assert not verdict.ok
    assert verdict.mismatches, "a mismatching example must be reported"
    m = verdict.mismatches[0]
    assert set(m) == {"text", "expected", "got", "note"}
    assert "match" in m["note"]  # human-readable
    assert verdict.summary().startswith("FAIL")


def test_judge_reports_compile_error():
    verdict = judge("(unclosed", ["a"], ["b"])
    assert not verdict.ok
    assert verdict.compile_error
    assert all("compile" in m["note"] for m in verdict.mismatches)


def test_judge_uses_full_match_semantics():
    # Full match, not substring: "ba" contains "a", so a substring engine would
    # wrongly judge it as a match and flag the negative. The Perl judge must
    # call it correctly (no mismatches).
    verdict = judge("a", positive=["a"], negative=["ba", "ab", "aab"])
    assert verdict.ok, verdict.summary()


def test_judge_handles_empty_example_strings():
    verdict = judge("^$", positive=[""], negative=["x"])
    assert verdict.ok, verdict.summary()


def test_verdict_dataclass_shape():
    v = Verdict(ok=True)
    assert v.mismatches == []
    assert v.compile_error is None


# ── unresolved guard ─────────────────────────────────────────────────────────


def test_generate_refuses_unresolved_trees():
    with pytest.raises(ValueError, match="unresolved"):
        generate(Sequence([Literal("a"), UnresolvedRef(surface="x")]), seed=0)
