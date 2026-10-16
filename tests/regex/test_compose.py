"""Compositional set tests (P1.10) — the E1.2 input is novel, deterministic,
and judge-grounded; the committed artifact is reproducible.
"""

from __future__ import annotations

import json

import pytest

from kainos.lang.deterministic import tokenize
from kainos.regex.bench import (
    default_compositional_path,
    default_corpus_path,
    materialize_compositional_set,
)
from kainos.regex.compose import build_fragment_pool, generate_compositional_set
from kainos.regex.data import load_corpus
from kainos.regex.judge import judge


@pytest.fixture(scope="module")
def seed_records() -> list[dict]:
    return load_corpus(default_corpus_path())


@pytest.fixture(scope="module")
def committed() -> list[dict]:
    return load_corpus(default_compositional_path())


# ── committed artifact ──────────────────────────────────────────────────────


def test_committed_set_shape(committed):
    assert len(committed) == 40
    for rec in committed:
        assert rec["id"].startswith("comp_")
        assert rec["positive"] and rec["negative"]


def test_committed_set_is_novel_against_seed(seed_records, committed):
    seed_tokens = {" ".join(tokenize(r["description"])).lower() for r in seed_records}
    for rec in committed:
        tokens = " ".join(tokenize(rec["description"])).lower()
        assert tokens not in seed_tokens, rec["id"]
        assert tokens.count("then") >= 1 or "," in tokens  # genuinely a combination


def test_every_committed_record_ground_truth_by_judge(committed):
    for rec in committed:
        verdict = judge(rec["expected_pcre"], rec["positive"], rec["negative"])
        assert verdict.ok, f"{rec['id']}: {verdict.summary()}"


# ── determinism: regeneration reproduces the committed artifact ─────────────


def test_regeneration_is_deterministic_and_matches_artifact(seed_records, tmp_path):
    # judge_enabled=True is how the committed artifact was built (the judge
    # filters rejected candidate sets, which shifts the acceptance stream), so
    # the comparison must regenerate with the judge on, like materialization.
    a = generate_compositional_set(seed_records, n=40, set_seed=42)
    b = generate_compositional_set(seed_records, n=40, set_seed=42)
    assert a == b
    committed = load_corpus(default_compositional_path())
    assert [json.dumps(r, sort_keys=True) for r in a] == [
        json.dumps(r, sort_keys=True) for r in committed
    ]


def test_different_seed_changes_the_set(seed_records, tmp_path):
    a = generate_compositional_set(seed_records, n=40, set_seed=42, judge_enabled=False)
    b = generate_compositional_set(seed_records, n=40, set_seed=7, judge_enabled=False)
    desc_a = {r["description"] for r in a}
    desc_b = {r["description"] for r in b}
    assert desc_a != desc_b


def test_materialize_writes_jsonl(seed_records, tmp_path):
    p = materialize_compositional_set(path=tmp_path / "cs.jsonl")
    lines = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) == 40
    assert all(json.loads(l) for l in lines)


# ── generator invariants (fresh random runs) ────────────────────────────────


def test_generated_records_satisfy_novelty_constraints(seed_records, tmp_path):
    recs = generate_compositional_set(seed_records, n=40, set_seed=1234, judge_enabled=False)
    seed_tokens = {" ".join(tokenize(r["description"])).lower() for r in seed_records}
    pool = build_fragment_pool(seed_records)
    text_to_sources = {}
    for frag in pool:
        text_to_sources.setdefault(frag.text, set()).add(frag.source_id)
    for rec in recs:
        tokens = " ".join(tokenize(rec["description"])).lower()
        assert tokens not in seed_tokens
        # Every generated description combines fragments; the combined text
        # must trace back to >= 2 distinct seed records (novelty requirement).
        clauses = []
        current: list[str] = []
        for t in tokenize(rec["description"]):
            if t in (",", "then", "and"):
                if current:
                    clauses.append(" ".join(current))
                    current = []
            else:
                current.append(t)
        if current:
            clauses.append(" ".join(current))
        sources: set[str] = set()
        for c in clauses:
            sources |= text_to_sources.get(c, set())
        assert len(sources) >= 2, f"{rec['id']}: combination not traceable to >= 2 seed records"


def test_content_word_fragments_exist_for_e1_2_isolation(seed_records):
    pool = build_fragment_pool(seed_records)
    content = [f for f in pool if f.content_word and not f.first_only and not f.last_only]
    assert any(f.text == "a hyphen" for f in content)
    assert not any(f.content_word for f in content if "literal" in f.text)
    # Class-surface phrases (quantifier + numeral words) are NOT lexicon words:
    assert not any(f.content_word for f in pool if f.text in (
        "exactly two letters", "three digits", "four digits",
    ))
