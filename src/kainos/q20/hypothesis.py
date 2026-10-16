"""Hypothesis space over concept ids (step 14).

The learner is rewarded for ELIMINATING possibilities, not for generating
text: ``H`` starts as all concepts, each (question, answer) filters it, and
progress is measured in bits of entropy ``log2(|H|)``.
"""

from __future__ import annotations

import math

__all__ = ["BUCKET_KEYS", "HypothesisSpace"]

BUCKET_KEYS = ("yes", "no", "unknown", "sometimes")


def bucket_key(answer: str | int) -> str:
    """``yes|no|unknown|sometimes`` pass through; ints become ``n:<int>``."""

    return answer if isinstance(answer, str) else f"n:{answer}"


class HypothesisSpace:
    """``H`` = frozenset of consistent concept ids + (question, answer) history."""

    def __init__(self, concept_ids) -> None:
        if concept_ids is None:
            raise ValueError("HypothesisSpace(None) is not a concept set")
        self.concepts: frozenset[str] = frozenset(concept_ids)
        self.history: list[tuple[str, str | int]] = []

    def __len__(self) -> int:
        return len(self.concepts)

    @staticmethod
    def from_corpus(corpus: list[dict]) -> HypothesisSpace:
        return HypothesisSpace({c["id"] for c in corpus})

    def apply(self, oracle, question, answer: str | int) -> int:
        """Filter H in place to the concepts consistent with this answer.

        Returns the new |H|. The filtered bucket is exactly the oracle
        partition cell for ``answer`` (see :meth:`split`).
        """

        qid = question if isinstance(question, str) else question["id"]
        key = bucket_key(answer)
        kept = {c for c in self.concepts if bucket_key(oracle.answer(c, question)) == key}
        self.concepts = frozenset(kept)
        self.history.append((qid, answer))
        return len(self.concepts)

    def entropy(self) -> float:
        """log2(|H|); 0.0 for |H| <= 1 (a singleton is already 'known')."""

        n = len(self.concepts)
        return math.log2(n) if n > 1 else 0.0

    def split(self, oracle, question) -> dict[str, set[str]]:
        """H partitioned by the oracle's answer to ``question``.

        Keys: ``yes|no|unknown|sometimes`` and ``n:<int>`` for numbered
        answers. The buckets always partition H (disjoint, union = H).
        """

        buckets: dict[str, set[str]] = {}
        for c in self.concepts:
            key = bucket_key(oracle.answer(c, question))
            buckets.setdefault(key, set()).add(c)
        return buckets
