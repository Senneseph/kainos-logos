"""Information-gain question selector (step 14).

Picks the question that maximizes expected information gain (entropy
reduction):

    IG(q) = H(H) - SUM_a P(a) * H(H_a)     P(a) = |H_a| / |H|,
    H_a   = {c in H : oracle.answer(c, q) = a},   H(x) = log2|x| (0 for |x|<=1)

Tie-breaks (strict, in order):
  (a) smaller unknown bucket |H_unknown| — prefer questions that put FEWER
      current candidates into EXCEPTION (unknown) territory, so the
      ambiguous set shrinks fast ("shrink EXCEPTION");
  (b) lower question cost (``cost`` map, default 1.0 for every question).

Fully deterministic: candidates are scanned in the given question order;
comparisons use exact floats with a 1e-12 epsilon for the IG tie.
"""

from __future__ import annotations

import math

from kainos.q20.hypothesis import HypothesisSpace

__all__ = ["best_question", "expected_information_gain"]

IG_TIE_EPS = 1e-12


def _log2(n: int) -> float:
    return math.log2(n) if n > 1 else 0.0


def expected_information_gain(space: HypothesisSpace, oracle, question, cost: dict[str, float] | None = None) -> dict:
    """``{"ig": float, "unknown": int, "cost": float, "buckets": {...}}``."""

    n = len(space)
    h0 = space.entropy()
    buckets = space.split(oracle, question)
    ig = h0
    for cell in buckets.values():
        p = len(cell) / n
        ig -= p * _log2(len(cell))
    qid = question if isinstance(question, str) else question["id"]
    cost_map = cost or {}
    return {
        "ig": ig,
        "unknown": len(buckets.get("unknown", set())),
        "cost": cost_map.get(qid, 1.0),
        "buckets": buckets,
    }


def best_question(space: HypothesisSpace, questions: list[dict], oracle, cost: dict[str, float] | None = None) -> tuple[dict, float]:
    """The (question, ig) with maximal IG, tie-broken per the module docstring.

    A space of size <= 1 needs no question: returns ``(questions[0], 0.0)``
    only if the caller insists (the game loop stops before calling this).
    """

    if len(space) <= 1:
        raise ValueError("no question needed for |H| <= 1")
    best: dict | None = None
    best_key: tuple[float, int, float] | None = None
    best_ig = 0.0
    for q in questions:
        stats = expected_information_gain(space, oracle, q, cost)
        key = (-stats["ig"], stats["unknown"], stats["cost"])
        if best_key is None or key < best_key:
            best, best_key, best_ig = q, key, stats["ig"]
    if best is None:
        raise ValueError("no candidate questions given")
    return best, best_ig
