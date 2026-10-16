"""Synthetic vision port (P3.09) — the cheapest honest second modality.

Input: a SCENE — objects with (x, y, z) positions at two or more named
timestamps. Output: a Semantic IR with one entity per object and one
``located_at`` relationship per (object, timestamp) — exactly the shape the
modality-blind ``abstract_pattern`` step turns into a TRANSFER pattern.

No pixels, no model: the claim under test is the algebra above the port, so
the honest move is to make the port trivially inspectable.
"""

from __future__ import annotations

from typing import Any

__all__ = ["SyntheticVisionPort"]


def _point_label(xyz: list[float]) -> str:
    """Deterministic location id: ``(x,y,z)`` — the spec's own notation."""

    return "(" + ",".join(str(v) for v in xyz) + ")"


class SyntheticVisionPort:
    """Scene (objects × timestamps) -> IR.

    Scene shape::

        {
          "t": ["t1", "t2"],
          "objects": [{"id": "box", "positions": [[0, 0, 0], [4, 4, 4]]}],
        }

    ``len(positions)`` must equal ``len(t)`` for every object, and each
    position is a triple of numbers — anything else is outside the port's
    declared input grammar and rejected outright."""

    name = "synthetic_vision"

    def perceive(self, raw: dict) -> dict:
        t = list(raw.get("t", []))
        objects = list(raw.get("objects", []))
        if not t or not objects:
            raise ValueError("scene needs timestamps and at least one object")
        entities: list[dict[str, Any]] = []
        relationships: list[dict[str, Any]] = []
        for o in objects:
            oid = str(o.get("id", ""))
            if not oid:
                raise ValueError("every scene object needs an id")
            positions = list(o.get("positions", []))
            if len(positions) != len(t):
                raise ValueError(
                    f"scene object {oid!r}: {len(positions)} positions for {len(t)} timestamps"
                )
            entities.append({"id": oid, "type": "object", "labels": [oid]})
            for ti, xyz in enumerate(positions):
                xyz = [float(v) for v in xyz]
                if len(xyz) != 3:
                    raise ValueError(f"scene object {oid!r}: position must be (x, y, z): {xyz}")
                relationships.append(
                    {
                        "subject": oid,
                        "relation": "located_at",
                        "object": _point_label(xyz),
                        "context": {"t": t[ti], "xyz": xyz},
                    }
                )
        return {"kind": "state", "entities": entities, "relationships": relationships}
