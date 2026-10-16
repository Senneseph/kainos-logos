"""The 20 Questions game loop (step 14).

State machine: ``ask -> answer -> update -> guess/end`` with budget
``max_questions=20`` (configurable). Win/loss + full trace are recorded.

The *agent* (this module) asks questions through the info-gain selector and
receives oracle answers about the *target* concept (the "player"). The game
ends when the agent guesses (``guess``), or when the budget exhausts (loss).
Stopping rule: guess immediately when |H| == 1, or when the best remaining
question's expected IG drops below ``stop_threshold`` (guess the top of H).
Top-of-H is the deterministic fallback ``min(H)`` — later experiments
(E2.x) replace the guess/parse sides with the LLM kernel.
"""

from __future__ import annotations

from kainos.q20.baselines import GreedyIGPolicy
from kainos.q20.hypothesis import HypothesisSpace
from kainos.q20.selector import best_question

__all__ = ["PLAY_BUDGET", "Game"]

PLAY_BUDGET = 20


class Game:
    """One game against a scripted/real oracle about ``target``."""

    STATE_PLAYING = "playing"
    STATE_WON = "won"
    STATE_LOST = "lost"

    def __init__(
        self,
        oracle,
        questions: list[dict],
        target: str,
        corpus: list[dict] | None = None,
        max_questions: int = PLAY_BUDGET,
        stop_threshold: float = 0.0,
        cost: dict[str, float] | None = None,
        policy=None,
    ) -> None:
        if corpus is None:
            corpus = oracle.corpus
        self.oracle = oracle
        self.questions = questions
        self.target = target
        self.space = HypothesisSpace.from_corpus(corpus)
        self.max_questions = max_questions
        self.stop_threshold = stop_threshold
        self.cost = cost
        self._policy = policy if policy is not None else GreedyIGPolicy(questions, cost)
        if target not in self.space.concepts:
            raise KeyError(f"target {target!r} is not in the corpus")
        self.state = self.STATE_PLAYING
        self.questions_used = 0
        self.trace: list[dict] = []

    # -- the loop ----------------------------------------------------------
    def next_question(self) -> dict:
        """The selected next question (per the game's question policy)."""

        if len(self.space) <= 1:
            raise ValueError("|H| <= 1 — nothing left to ask; call guess()")
        question = self._policy.choose(self.space, self.oracle)
        if question is None:
            raise ValueError("question policy exhausted — call guess()")
        return question

    def receive(self, question: dict | str, answer: str | int | None = None) -> str | int:
        """One answer step: ``ask -> answer -> update``. Records the trace row."""

        if self.state != self.STATE_PLAYING:
            raise RuntimeError(f"game already over ({self.state})")
        if self.questions_used >= self.max_questions:
            raise RuntimeError("budget exhausted — call guess()")
        qid = question if isinstance(question, str) else question["id"]
        if answer is None:
            answer = self.oracle.answer(self.target, question)
        h_before = len(self.space)
        h_after = self.space.apply(self.oracle, question, answer)
        self.questions_used += 1
        self.trace.append(
            {
                "question": qid,
                "answer": answer,
                "h_before": h_before,
                "h_after": h_after,
                "entropy_after": self.space.entropy(),
            }
        )
        if h_after == 0:
            # the observed answer is consistent with no concept in H — the
            # oracle lied / the target is outside H: unrecoverable, loss.
            self.state = self.STATE_LOST
        return answer

    def make_guess(self, guess_id: str | None = None) -> dict:
        """Commit a guess (defaults per module docstring). Ends the game."""

        if self.state != self.STATE_PLAYING:
            raise RuntimeError(f"game already over ({self.state})")
        guess = guess_id if guess_id is not None else (min(self.space.concepts) if self.space.concepts else None)
        won = guess == self.target
        self.state = self.STATE_WON if won else self.STATE_LOST
        return self.result(guess)

    def result(self, guess_id: str | None) -> dict:
        return {
            "won": guess_id == self.target,
            "target": self.target,
            "guess": guess_id,
            "questions_used": self.questions_used,
            "budget": self.max_questions,
            "final_H": sorted(self.space.concepts),
            "final_entropy": self.space.entropy(),
            "trace": self.trace,
            "state": self.state,
        }

    def play(self) -> dict:
        """Deterministic play-to-completion: ask/answer until the stop rule."""

        while self.state == self.STATE_PLAYING:
            if len(self.space) <= 1:
                return self.make_guess()
            if self.questions_used >= self.max_questions:
                return self.make_guess()  # exhaustion -> recorded loss unless it was the last
            try:
                question = self.next_question()
            except ValueError:
                return self.make_guess()  # policy exhausted (e.g. random deck empty)
            if self.stop_threshold > 0.0:
                _, ig = best_question(self.space, self.questions, self.oracle, self.cost)
                if ig < self.stop_threshold:
                    return self.make_guess()
            self.receive(question)
        return self.result(None)  # contradiction loss (an answer consistent with no concept)
