"""Comparison baselines for the E2 experiments (step 15).

Both expose the policy interface the Game plays through:
``choose(space, oracle) -> question | None``.

- :class:`GreedyIGPolicy` — the pipeline's policy: adaptive info gain
  (step 14). Kept here so policies are comparable in one place.
- :class:`RandomQuestioner` — uniform random valid questions, seeded and
  reproducible, asks each question at most once, then stops (``None``).
- :class:`StatelessGreedy` — IG computed ONCE over the frozen full corpus,
  turning into a fixed question order: it never adapts to the answers it
  receives and ignores everything the CODEX has learned (A1/A3 falsifiers).
"""

from __future__ import annotations

import random

from kainos.q20.hypothesis import HypothesisSpace
from kainos.q20.selector import best_question, expected_information_gain

__all__ = ["GreedyIGPolicy", "RandomQuestioner", "StatelessGreedy"]


class GreedyIGPolicy:
    """Adaptive maximum-information-gain selection (the pipeline's policy).

    Asks each question at most once (a repeated question has the same
    answer and leaves H unchanged — the 20Q rule :class:`RandomQuestioner`
    documents too); when every question has been asked it returns ``None``
    so the game commits its guess (fallback ``min(H)``).
    """

    def __init__(self, questions: list[dict], cost: dict[str, float] | None = None) -> None:
        self.questions = questions
        self.cost = cost

    def choose(self, space: HypothesisSpace, oracle) -> dict | None:
        if len(space) <= 1:
            return None
        asked = {qid for qid, _ in space.history}
        remaining = [q for q in self.questions if q["id"] not in asked]
        if not remaining:
            return None
        question, _ = best_question(space, remaining, oracle, self.cost)
        return question


class RandomQuestioner:
    """Uniformly random VALID questions, seeded: reproducible per seed.

    Each question is asked at most once (shuffled deck); ``choose`` returns
    ``None`` when the deck is exhausted — the game then guesses.
    """

    def __init__(self, questions: list[dict], seed: int = 0) -> None:
        self.seed = seed
        self._deck = list(questions)
        random.Random(seed).shuffle(self._deck)
        self._i = 0

    def choose(self, space: HypothesisSpace, oracle) -> dict | None:
        if self._i >= len(self._deck):
            return None
        q = self._deck[self._i]
        self._i += 1
        return q

    @property
    def order(self) -> list[str]:
        return [q["id"] for q in self._deck]


class StatelessGreedy:
    """IG selection over the FROZEN corpus: a fixed questionnaire.

    IGs are computed once on the full (unfiltered) space, so every game
    plays the same question order regardless of the answers observed or
    what the CODEX has since learned. The meaningful A1/A3 baseline:
    'smart questions, no learning'.
    """

    def __init__(self, questions: list[dict], oracle, all_ids: set[str] | list[str], cost: dict[str, float] | None = None) -> None:
        space = HypothesisSpace(set(all_ids))
        stats = {q["id"]: expected_information_gain(space, oracle, q, cost) for q in questions}
        self._order = sorted(questions, key=lambda q: (-stats[q["id"]]["ig"], stats[q["id"]]["unknown"], stats[q["id"]]["cost"]))
        self._i = 0

    def choose(self, space: HypothesisSpace, oracle) -> dict | None:
        if self._i >= len(self._order):
            return None
        q = self._order[self._i]
        self._i += 1
        return q

    @property
    def order(self) -> list[str]:
        return [q["id"] for q in self._order]
