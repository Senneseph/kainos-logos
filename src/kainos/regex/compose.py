"""Compositional set generator (P1.10) — novel combinations of known operators.

E1.2's input: descriptions built from a cross-product of operator fragments
*harvested from the seed corpus*, such that no generated description duplicates
the seed corpus (asserted, normalized) and each combination draws on at least
two different seed records ("never appeared together"). Ground truth is not
assumed: every candidate example set is verified with the Perl judge
(ADR-0009) before a record is admitted, and the admitted set is materialized
to `data/regex/compositional_set.jsonl` (deterministic under seed 42) as a
committed, auditable artifact (G2).

Fragments and their placement rules follow the grammar's binding (pinned in
test_corpus.py): alternative/group fragments extend through their alternative
branch, so they may only close a composition; `start of string` only opens
one. Everything else composes freely in the sequence.
"""

from __future__ import annotations

import random

from kainos.lang.deterministic import (
    _CLASS_SURFACES,
    _NUMBER_SURFACES,
    _REFERENCE_SURFACES,
    DeterministicKernel,
    _is_connector,
    _skip_connector,
    parse_regex_text,
    tokenize,
)
from kainos.regex.emitter import emit
from kainos.regex.ir import (
    Alternative,
    Anchor,
    Flag,
    Group,
    Node,
    Repeat,
    Sequence,
)
from kainos.regex.judge import judge
from kainos.regex.testgen import generate

__all__ = ["Fragment", "build_fragment_pool", "generate_compositional_set"]

_CONNECTIVE = ", then "

# Words the grammar consumes structurally (not content words, not class
# surfaces): the complement of these + the class/number/reference surfaces +
# numerals marks the words only a CODEX lookup can resolve.
_STRUCTURAL_WORDS = frozenset(
    {
        "one", "or", "more", "zero", "optional", "optionally", "maybe", "exactly",
        "at", "least", "most", "between", "from", "to", "and", "then", "by",
        "start", "beginning", "end", "of", "string", "ignoring", "case",
        "literal", "group",
        "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    }
)


def _split_clauses(tokens: list[str]) -> list[list[str]]:
    """Split a description's token stream into clauses (connector-separated).
    Connectors themselves belong to no clause."""

    clauses: list[list[str]] = []
    start = 0
    i = 0
    while i < len(tokens):
        if _is_connector(tokens, i):
            start_of_connector_run = i
            i = _skip_connector(tokens, i)
            while i < len(tokens) and _is_connector(tokens, i):
                i = _skip_connector(tokens, i)
            if start_of_connector_run > start:
                clauses.append(tokens[start:start_of_connector_run])
            start = i
        else:
            i += 1
    if i > start:
        clauses.append(tokens[start:])
    return clauses


def _contains(node: Node, factories: type | tuple[type, ...]) -> bool:
    if isinstance(node, factories):
        return True
    if isinstance(node, Sequence):
        return any(_contains(el, factories) for el in node.elements)
    if isinstance(node, Alternative):
        return any(_contains(b, factories) for b in node.branches)
    if isinstance(node, (Repeat, Group)):
        return _contains(node.node, factories)
    return False


def _needs_lexicon(tokens: list[str]) -> bool:
    """True when the clause contains a word the grammar cannot resolve itself
    (neither structural, class/number/reference surface, numeral, nor part of
    a `the literal …` capture) — i.e. only a CODEX lookup can resolve it."""

    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "literal":
            break  # the rest of the clause is captured literal text
        if t in ("a", "an", "the", "either", "or", ","):
            i += 1
            continue
        if (
            t in _CLASS_SURFACES
            or t in _NUMBER_SURFACES
            or t in _REFERENCE_SURFACES
            or t in _STRUCTURAL_WORDS
            or t.isdigit()
        ):
            i += 1
            continue
        return True
    return False


class Fragment:
    """One operator fragment: a clause of a seed description plus the dialect
    node (and emitted PCRE) it parses to.

    `first_only`/`last_only` encode the grammar's placement rules; `source_id`
    is the seed record the fragment came from (novelty bookkeeping);
    `content_word` marks fragments whose surface needs the CODEX lexicon (the
    hyphen) — the ones that isolate the CODEX's contribution in E1.2.
    """

    def __init__(self, text: str, node: Node, source_id: str, clause_tokens: list[str]) -> None:
        self.text = text
        self.node = node
        self.pcre = emit(node)
        self.source_id = source_id
        self.first_only = _contains(node, Anchor) and emit(node) == "^"
        self.last_only = (_contains(node, Anchor) and emit(node) == "$") or _contains(
            node, (Alternative, Group)
        )
        self.content_word = _needs_lexicon(clause_tokens)
        positive, negative = generate(node, seed=seed_of(node))
        self.positives = [s for s in positive[:2]] or [""]
        self.negatives = [s for s in negative[:2]]

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Fragment({self.text!r} -> {self.pcre!r}, src={self.source_id})"


def seed_of(node: Node) -> int:
    """A stable, per-fragment testgen seed (deterministic; keeps fragments
    independent of the set seed)."""

    return sum(ord(c) for c in emit(node)) % 10_000


def build_fragment_pool(seed_corpus: list[dict]) -> list[Fragment]:
    """Harvest one Fragment per clause of every seed record.

    A clause is admitted only when it parses to exactly the corresponding
    element of the record's full tree (byte-checked by emission) — so every
    fragment is known-true by construction. Records whose clauses cannot be
    paired 1:1 are skipped.
    """

    from kainos.codex.memory import InMemoryCodexStore
    from kainos.regex.lexicon import seed

    store = InMemoryCodexStore()
    seed(store)
    kernel = DeterministicKernel(store)

    pool: list[Fragment] = []
    for rec in seed_corpus:
        tokens = tokenize(rec["description"])
        clauses = _split_clauses(tokens)
        try:
            tree = kernel.parse(rec["description"])[0].ir
        except ValueError:
            continue
        if not isinstance(tree, Node):
            continue
        elements = list(tree.elements) if isinstance(tree, Sequence) else [tree]
        if len(clauses) != len(elements):
            continue
        for clause, element in zip(clauses, elements):
            try:
                clause_node = parse_regex_text(" ".join(clause), kernel._lookup)
            except ValueError:
                continue
            if emit(clause_node) != emit(element):
                continue
            frag = Fragment(" ".join(clause), element, rec["id"], clause)
            if not frag.positives:
                continue
            pool.append(frag)
    return pool


def _first_flag(pool: list[Fragment]) -> Fragment:
    flags = [f for f in pool if isinstance(f.node, Flag)]
    if not flags:
        raise ValueError("no flag fragment in pool")
    return flags[0]


def generate_compositional_set(
    seed_corpus: list[dict], n: int = 40, set_seed: int = 42, judge_enabled: bool = True
) -> list[dict]:
    """Build `n` novel, judge-grounded compositions of seed-corpus fragments.

    Deterministic for a fixed set_seed (and the fixed per-fragment seeds):
    the materialized data/regex/compositional_set.jsonl is reproducible.
    """

    rng = random.Random(set_seed)
    pool = build_fragment_pool(seed_corpus)
    if not pool:
        raise ValueError("no fragments harvested from the seed corpus")

    first_pool = [f for f in pool if f.first_only]
    last_pool = [f for f in pool if f.last_only]
    content_pool = [f for f in pool if f.content_word and not f.first_only and not f.last_only]
    mid_pool = [f for f in pool if not f.first_only and not f.last_only]
    if not mid_pool:
        raise ValueError("no mid-position fragments available")

    seed_token_sets = {" ".join(tokenize(r["description"])).lower() for r in seed_corpus}
    records: list[dict] = []
    seen_token_sets: set[str] = set()

    for _attempt in range(n * 200):
        if len(records) >= n:
            break
        k = rng.choice([2, 3, 3])

        chosen = list(rng.sample(mid_pool, min(k, len(mid_pool))))
        if content_pool and rng.random() < 0.7 and not any(f.content_word for f in chosen):
            chosen.insert(rng.randint(0, len(chosen) - 1), rng.choice(content_pool))
        if last_pool and rng.random() < 0.3:  # a closing alternative/group
            chosen.append(rng.choice(last_pool))
        if first_pool and rng.random() < 0.2:  # an opening anchor
            chosen.insert(0, rng.choice(first_pool))
        if rng.random() < 0.3:  # optional case-insensitivity
            chosen.insert(rng.randint(0, len(chosen) - 1), _first_flag(pool))
        if len(chosen) < 2:
            continue

        # Placement: ^ first; $ / alternatives / groups last (grammar binding).
        first_frags = [f for f in chosen if f.first_only][:1]
        last_frags = [f for f in chosen if f.last_only][:1]
        mid_frags = [f for f in chosen if not f.first_only and not f.last_only]
        budget = 3 if (first_frags or last_frags) else k
        seq = first_frags + mid_frags[: max(budget - len(first_frags) - len(last_frags), 0)] + last_frags
        if len(seq) < 2:
            continue
        if len({f.text for f in seq}) != len(seq):
            continue  # repeated fragment (even from another seed record) — retry

        # Novelty: at least two distinct source records, and the joined
        # description duplicates no seed description (token-stream equality).
        if len({f.source_id for f in seq}) < 2:
            continue
        description = _CONNECTIVE.join(f.text for f in seq)
        token_set = " ".join(tokenize(description)).lower()
        if token_set in seed_token_sets or token_set in seen_token_sets:
            continue

        pcre = "".join(f.pcre for f in seq)
        positives = ["".join(combo) for combo in _cartesian([f.positives[:2] for f in seq], limit=6)]
        negatives: list[str] = []
        for frag in seq:
            for neg in frag.negatives:
                parts = [f.positives[0] for f in seq]
                parts[seq.index(frag)] = neg
                negatives.append("".join(parts))
        if not positives or not negatives:
            continue

        if judge_enabled:
            verdict = judge(pcre, positives, negatives)
            bad_texts = {m["text"] for m in verdict.mismatches}
            positives = [p for p in positives if p not in bad_texts]
            negatives = [g for g in negatives if g not in bad_texts]
            if not positives or not negatives:
                continue  # the judge rejected the candidate set → new combination

        seen_token_sets.add(token_set)
        records.append(
            {
                "id": "",  # assigned after the final order is fixed
                "description": description,
                "expected_pcre": pcre,
                "positive": positives[:3],
                "negative": negatives[:3],
            }
        )

    if len(records) < n:
        raise ValueError(f"could not generate {n} compositions (got {len(records)})")
    for i, rec in enumerate(records):
        rec["id"] = f"comp_{i:03d}"
    return records


def _cartesian(items: list[list[str]], limit: int) -> list[list[str]]:
    out: list[list[str]] = [[]]
    for options in items:
        out = [prefix + [opt] for prefix in out for opt in options]
        out = out[:limit]
    return out
