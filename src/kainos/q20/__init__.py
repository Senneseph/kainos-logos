"""The 20 Questions world (Phase 2).

Corpus + deterministic oracle + CODEX seed (step 13); question parser,
hypothesis space, info-gain selector and game loop (step 14).
"""

from kainos.q20.game import Game
from kainos.q20.hypothesis import HypothesisSpace
from kainos.q20.oracle import Oracle, load_corpus, load_questions
from kainos.q20.question_parse import ParsedQuestion, Query, parse_question
from kainos.q20.seed import seed
from kainos.q20.selector import best_question

__all__ = [
    "Game",
    "HypothesisSpace",
    "Oracle",
    "ParsedQuestion",
    "Query",
    "best_question",
    "load_corpus",
    "load_questions",
    "parse_question",
    "seed",
]
