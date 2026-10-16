"""Question parser: 20Q grammar -> Query IR (step 14).

Reuses the Phase-1 kernel PATTERN (template match -> typed IR node; unknown
phrasing -> ``UnresolvedRef`` so the game can ask a clarifying question —
ADR/plan: the parser never invents meaning), applied to the 20Q question
grammar from ``plan/30-phases/phase-2-20questions/game-spec.md``:

    "Is it <property>?"        -> CONSTRAINT  (property = yes/no to be learned)
    "Does it have <property>?" -> CONSTRAINT  (has_<property>)
    "How many <part>?"         -> CONSTRAINT  (<part> = <number>)
    "Is it a <category>?"      -> HYPOTHESIS  (is_a = category)

Unknown wording (a word that is neither a property nor a category) yields
``query=None`` + ``unresolved=[<word>]`` — the game loop turns that into a
clarifying question (C3, honest uncertainty, now at 20Q scale).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

__all__ = ["ParsedQuestion", "Query", "load_questions_index", "parse_question"]

# word -> property for the question grammar (underscore names also accepted)
PROPERTY_WORDS = {
    "alive": "alive",
    "edible": "edible",
    "green": "is_green",
    "wheels": "has_wheels",
    "engine": "has_engine",
    "doors": "has_doors",
    "person": "can_carry_person",
    "water": "lives_in_water",
}
# part -> property for "How many <part>?"
PART_WORDS = {"wheel": "wheel_count", "wheels": "wheel_count"}


@dataclass(frozen=True)
class Query:
    """One parsed 20Q question: a constraint probe or a category hypothesis."""

    kind: str  # "CONSTRAINT" | "HYPOTHESIS"
    property: str | None = None  # CONSTRAINT: property name
    category: str | None = None  # HYPOTHESIS: category name
    question_id: str | None = None  # when it matches a known question


@dataclass(frozen=True)
class ParsedQuestion:
    surface: str
    query: Query | None
    unresolved: tuple[str, ...] = ()


def load_questions_index(path: str | Path | None = None) -> dict[str, dict]:
    """{surface (lower, '?'-stripped, whitespace-normalized) -> question dict}."""

    if path is None:
        path = Path("data/q20/questions.json")
    records = json.loads(Path(path).read_text())
    return {_norm_surface(r["surface"]): r for r in records}


def _norm_surface(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower()).rstrip("?").strip()


def _word(s: str) -> str:
    return re.sub(r"[^a-z]+", " ", s.lower()).strip()


def parse_question(surface: str, questions: dict[str, dict] | None = None) -> ParsedQuestion:
    """Template-match one surface form. Canonical known surfaces win first."""

    text = surface.strip()
    low = _norm_surface(text)

    if questions is None:
        questions = load_questions_index()
    known = questions.get(low)
    if known is not None:
        kind = "HYPOTHESIS" if known["kind"] == "category_probe" else "CONSTRAINT"
        if kind == "HYPOTHESIS":
            return ParsedQuestion(text, Query(kind, category=known["category"], question_id=known["id"]), ())
        return ParsedQuestion(text, Query(kind, property=known["property"], question_id=known["id"]), ())

    # "How many <part>?"
    m = re.fullmatch(r"how many (.+)", low)
    if m:
        part = _word(m.group(1))
        if part in PART_WORDS:
            return ParsedQuestion(
                text, Query("CONSTRAINT", property=PART_WORDS[part], question_id=f"q_{PART_WORDS[part]}"), ()
            )
        return ParsedQuestion(text, None, (part,))

    # "Does it have <...>?"
    m = re.fullmatch(r"does it have (?:an |a |the )?(.+)", low)
    if m:
        word = _word(m.group(1))
        if word in PROPERTY_WORDS:
            prop = PROPERTY_WORDS[word]
            if not prop.startswith("has_"):
                prop = f"has_{prop}"
            return ParsedQuestion(text, Query("CONSTRAINT", property=prop, question_id=f"q_{prop}"), ())
        return ParsedQuestion(text, None, (word,))

    # "Can it carry <...>?"
    m = re.fullmatch(r"can it (?:carry|hold) (.+)", low)
    if m:
        word = _word(m.group(1))
        if word in PROPERTY_WORDS:
            prop = PROPERTY_WORDS[word]
            return ParsedQuestion(text, Query("CONSTRAINT", property=prop, question_id=f"q_{prop}"), ())
        return ParsedQuestion(text, None, (word,))

    # "Is it (a|an|the)? <word>?" — category first, then property
    m = re.fullmatch(r"is it (?:(?:a|an|the) )?(.+)", low)
    if m:
        word = _word(m.group(1))
        categories = {q["category"] for q in questions.values() if q["kind"] == "category_probe"}
        if word in categories or (word + "s") in categories:
            cat = word if word in categories else f"{word}s"
            return ParsedQuestion(text, Query("HYPOTHESIS", category=cat, question_id=f"q_cat_{cat}"), ())
        if word in PROPERTY_WORDS:
            prop = PROPERTY_WORDS[word]
            return ParsedQuestion(text, Query("CONSTRAINT", property=prop, question_id=f"q_{prop}"), ())
        # multi-word property surfaces, e.g. "was it made by humans"/"made by humans"
        made = "made by humans" in word or "man made" in word or "man-made" in word
        if made:
            return ParsedQuestion(text, Query("CONSTRAINT", property="manufactured", question_id="q_made"), ())
        return ParsedQuestion(text, None, (word,))

    # no template matched at all
    return ParsedQuestion(text, None, (low,))
