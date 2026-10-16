"""The deterministic 20Q oracle (step 13).

Answers are ``yes | no | unknown | sometimes | <int>``. ``unknown``
(property absent for the concept) and ``sometimes`` (conditional property)
are the intentional EXCEPTION seeds — absence, not a stored value, is the
unknown. The oracle is a pure function of (corpus, question, concept):
same inputs, same answer, no RNG involved (the ``seed`` parameter exists
for the signature contract and is intentionally unused).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

__all__ = ["Oracle", "default_corpus_path", "default_questions_path", "load_corpus", "load_questions"]

ANSWERS = ("yes", "no", "unknown", "sometimes")


def _q20_data(name: str) -> Path:
    """CWD-relative ``data/q20/<name>``, falling back to the package-anchored
    repo root (the Phase-1 regex-bench convention) so experiments can run from
    any CWD (e.g. harness tmp dirs)."""

    direct = Path("data/q20") / name
    if direct.exists():
        return direct
    return Path(__file__).resolve().parents[3] / "data/q20" / name


def default_corpus_path() -> Path:
    return _q20_data("concepts.json")


def default_questions_path() -> Path:
    return _q20_data("questions.json")


def load_corpus(path: str | Path | None = None) -> list[dict]:
    """[{"id", "label", "categories": [...], "properties": {...}}, ...]"""

    records = json.loads((Path(path) if path is not None else default_corpus_path()).read_text())
    for r in records:
        for key in ("id", "label", "categories", "properties"):
            if key not in r:
                raise ValueError(f"corpus record missing {key!r}: {r!r}")
    return records


def load_questions(path: str | Path | None = None) -> list[dict]:
    """[{"id", "surface", "kind", "property"|"category"}, ...]"""

    records = json.loads((Path(path) if path is not None else default_questions_path()).read_text())
    for r in records:
        for key in ("id", "surface", "kind"):
            if key not in r:
                raise ValueError(f"question missing {key!r}: {r!r}")
        if r["kind"] == "property_probe" and "property" not in r:
            raise ValueError(f"property_probe missing 'property': {r!r}")
        if r["kind"] == "category_probe" and "category" not in r:
            raise ValueError(f"category_probe missing 'category': {r!r}")
    return records


@dataclass(frozen=True)
class Oracle:
    """Deterministic Q/A against the corpus: ``answer(concept_id, question)``."""

    corpus: list[dict]
    questions: list[dict]

    def __post_init__(self) -> None:
        if any(not isinstance(v, str) and not isinstance(v, int) for c in self.corpus for v in c["properties"].values()):
            raise ValueError("property values must be 'yes'|'no'|'sometimes'|int")

    @classmethod
    def load(cls, corpus: str | Path | None = None, questions: str | Path | None = None) -> Oracle:
        return cls(load_corpus(corpus), load_questions(questions))

    def concept(self, concept_id: str) -> dict:
        for c in self.corpus:
            if c["id"] == concept_id:
                return c
        raise KeyError(f"unknown concept: {concept_id!r}")

    def question(self, question: dict | str) -> dict:
        if isinstance(question, dict):
            return question
        for q in self.questions:
            if q["id"] == question:
                return q
        raise KeyError(f"unknown question: {question!r}")

    def answer(self, concept_id: str, question: dict | str, seed: int = 0) -> str | int:
        """``yes | no | unknown | sometimes | <int>``. ``seed`` is accepted for
        the signature contract and never used — determinism is total."""

        q = self.question(question)
        c = self.concept(concept_id)
        if q["kind"] == "property_probe":
            value = c["properties"].get(q["property"])
            if value is None:
                return "unknown"  # absence is the signal
            return value  # yes | no | sometimes | int
        if q["kind"] == "category_probe":
            return "yes" if q["category"] in c["categories"] else "no"
        raise ValueError(f"unknown question kind: {q['kind']!r}")

    def answers(self, concept_id: str) -> dict[str, str | int]:
        """All questions keyed by question id (the full oracle transcript)."""

        return {q["id"]: self.answer(concept_id, q) for q in self.questions}
