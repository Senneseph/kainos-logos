"""kainos.puzzle — generic n-dimensional logical-grid constraint core (E4.1).

Pure data + a deterministic forward-chaining/backtracking solver with proof
chains, uniqueness, minimal contradiction certificates, and the degradation
machinery (typed-unknown terms, undetermined facts, resolving facts) that
the E4.1 arms test. No puzzle is built into the core: a puzzle is a
``PuzzleSpec`` (see ``kainos.puzzle.puzzles``).
"""

from __future__ import annotations

from kainos.puzzle.bench import E4_1Experiment, run_e4_1
from kainos.puzzle.core import (
    ENUMERATION_CAP,
    At,
    Clue,
    Contradiction,
    Dimension,
    Gap,
    Left,
    Next,
    Pair,
    ProofStep,
    PuzzleSpec,
    Solution,
    SolveReport,
    minimal_certificate,
    resolving_facts,
    solve,
    undetermined_facts,
)

__all__ = [
    "ENUMERATION_CAP",
    "At",
    "Clue",
    "Contradiction",
    "Dimension",
    "E4_1Experiment",
    "Gap",
    "Left",
    "Next",
    "Pair",
    "ProofStep",
    "PuzzleSpec",
    "Solution",
    "SolveReport",
    "minimal_certificate",
    "resolving_facts",
    "run_e4_1",
    "solve",
    "undetermined_facts",
]
