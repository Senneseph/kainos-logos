"""Perception ports (P3.09) — modality -> Semantic IR, then IR -> abstract pattern.

A ``PerceptionPort`` is anything that turns a RAW modality input into a
Semantic IR dict (``kainos/ir/1``): text, a synthetic vision scene, (later)
audio, … The algebra under the port is modality-blind — the same
``abstract_pattern`` step runs on every port's IR, which is exactly the "one
algebra" claim this step exists to test.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol

__all__ = ["TEXT_MOVE_RE", "AbstractPattern", "PerceptionPort", "TextPort", "abstract_pattern"]

#: The text port's declared, honest grammar: "<actor> moved [the|a] <object>".
#: It is intentionally tiny — a perception port declares what it can see.
#: The point is the IR it emits, not the size of its grammar.
TEXT_MOVE_RE = re.compile(r"^(\w+) moved (?:the |a |)(\w+)$", re.IGNORECASE)

_TRANSFER_RELATIONS = {"moved", "move", "transferred"}


@dataclass(frozen=True)
class AbstractPattern:
    """A modality-abstract pattern: ``TRANSFER(object, …)`` — the object that
    moved, who/what moved it, and where it moved (A -> B). ``actor`` is
    unknown from a pure scene (motion without a visible agent); the from/to
    locations are unknown from a bare "moved" sentence. Compatibility is the
    cross-modal match: same pattern type, same object."""

    pattern: str
    object: str
    actor: str | None = None
    from_loc: str | None = None
    to_loc: str | None = None

    def compatible(self, other: AbstractPattern) -> bool:
        return self.pattern == other.pattern and self.object == other.object

    def to_dict(self) -> dict[str, str | None]:
        return {
            "pattern": self.pattern,
            "object": self.object,
            "actor": self.actor,
            "from": self.from_loc,
            "to": self.to_loc,
        }


class PerceptionPort(Protocol):
    """Modality -> Semantic IR. ``name`` is the modality label used in
    provenance when the IR's content is corroborated into the CODEX."""

    name: str

    def perceive(self, raw: Any) -> dict:
        """Return a Semantic IR dict (kainos/ir/1). Raise on input outside the
        port's declared grammar — a port names what it can see."""
        ...


class TextPort:
    """English -> IR. Declared grammar: TEXT_MOVE_RE. Emits the moving event
    as a relationship so the same abstraction step that reads a vision scene
    can read this sentence (one algebra, two modalities)."""

    name = "text"

    def perceive(self, raw: str) -> dict:
        m = TEXT_MOVE_RE.match(raw.strip())
        if m is None:
            raise ValueError(f"text outside the port's declared grammar: {raw!r}")
        actor, obj = m.group(1).lower(), m.group(2).lower()
        return {
            "kind": "state",
            "entities": [
                {"id": actor, "type": "agent", "labels": [m.group(1)]},
                {"id": obj, "type": "object", "labels": [m.group(2)]},
            ],
            "relationships": [{"subject": actor, "relation": "moved", "object": obj}],
        }


def abstract_pattern(ir: dict) -> AbstractPattern | None:
    """The modality-blind reduction step. Two declared routes into the same
    abstract TRANSFER pattern:

    - an explicit move event: ``actor --moved/…--> object`` (text);
    - observed motion: ``object --located_at--> A`` at t1 and
      ``object --located_at--> B ≠ A`` at a later t (vision). Location
      order = context ``t`` order, then list order (deterministic).

    Returns None when the IR shows no transfer — the honest negative,
    mirroring the planner's NoValidPlan discipline."""

    rels = ir.get("relationships", [])

    for rel in rels:
        if str(rel.get("relation", "")).lower() in _TRANSFER_RELATIONS:
            return AbstractPattern(
                pattern="TRANSFER",
                object=str(rel.get("object")),
                actor=str(rel.get("subject")),
            )

    located: dict[str, list[tuple[float, int, str]]] = {}
    for i, rel in enumerate(rels):
        if rel.get("relation") != "located_at":
            continue
        ctx = rel.get("context") or {}
        t = ctx.get("t", 0)
        try:
            key = (float(t), i, str(rel.get("object")))
        except (TypeError, ValueError):
            key = (float("inf"), i, str(rel.get("object")))
        located.setdefault(str(rel.get("subject")), []).append(key)

    for subject in sorted(located):
        entries = located[subject]
        locs = [obj for _, _, obj in sorted(entries)]
        if len(dict.fromkeys(locs)) >= 2:
            return AbstractPattern(
                pattern="TRANSFER",
                object=subject,
                from_loc=locs[0],
                to_loc=locs[-1],
            )
    return None
