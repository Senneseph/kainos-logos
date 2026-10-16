"""Synthetic vision port + text port — both reduce to the shared TRANSFER
pattern (the E3.4 core)."""

from __future__ import annotations

from typing import Any

import pytest

from kainos.ir.codec import validate
from kainos.multimodal.port import (
    AbstractPattern,
    PerceptionPort,
    TextPort,
    abstract_pattern,
)
from kainos.multimodal.synthetic_vision import SyntheticVisionPort


def _scene() -> dict[str, Any]:
    obj = {"id": "box", "positions": [[0, 0, 0], [4, 4, 4]]}
    return {"t": ["t1", "t2"], "objects": [obj]}


def test_synthetic_scene_emits_valid_ir_with_entities_and_relationships() -> None:
    ir = SyntheticVisionPort().perceive(_scene())
    validate(ir)  # must be a legal kainos/ir/1 document
    assert [e["id"] for e in ir["entities"]] == ["box"]
    assert len(ir["relationships"]) == 2
    (r1, r2) = ir["relationships"]
    assert (r1["subject"], r1["relation"], r1["object"]) == ("box", "located_at", "(0.0,0.0,0.0)")
    assert (r2["subject"], r2["relation"], r2["object"]) == ("box", "located_at", "(4.0,4.0,4.0)")
    assert r1["context"]["t"] == "t1" and r2["context"]["t"] == "t2"


def test_ports_satisfy_the_perception_port_protocol() -> None:
    # structural typing: both ports are usable as PerceptionPort
    def use_port(p: PerceptionPort, raw: Any) -> dict:
        return p.perceive(raw)

    assert use_port(TextPort(), "John moved the box")["kind"] == "state"
    assert use_port(SyntheticVisionPort(), _scene())["kind"] == "state"
    assert TextPort().name == "text" and SyntheticVisionPort().name == "synthetic_vision"


def test_shared_transfer_pattern_from_text_and_scene() -> None:
    from_text = abstract_pattern(TextPort().perceive("John moved the box"))
    from_scene = abstract_pattern(SyntheticVisionPort().perceive(_scene()))
    assert isinstance(from_text, AbstractPattern) and isinstance(from_scene, AbstractPattern)
    assert from_text.pattern == "TRANSFER" and from_scene.pattern == "TRANSFER"
    assert from_text.object == "box" and from_scene.object == "box"
    # what each modality can and cannot know:
    assert from_text.actor == "john" and from_text.from_loc is None and from_text.to_loc is None
    assert from_scene.actor is None and from_scene.from_loc == "(0.0,0.0,0.0)" and from_scene.to_loc == "(4.0,4.0,4.0)"
    # THE cross-modal match:
    assert from_text.compatible(from_scene)
    assert AbstractPattern("TRANSFER", "box").compatible(AbstractPattern("TRANSFER", "box", actor="x"))
    assert not from_text.compatible(AbstractPattern("TRANSFER", "crate"))


def test_abstraction_negative_cases() -> None:
    # no transfer in a static scene (same location both times):
    static = {"t": ["t1", "t2"], "objects": [{"id": "b", "positions": [[1, 1, 1], [1, 1, 1]]}]}
    assert abstract_pattern(SyntheticVisionPort().perceive(static)) is None
    # no move event in the text IR:
    plain = {"kind": "state", "relationships": [{"subject": "a", "relation": "knows", "object": "b"}]}
    # (plain is valid IR shape for our purposes; abstract_pattern only reads relationships)
    assert abstract_pattern(plain) is None


def test_port_rejects_input_outside_its_grammar() -> None:
    with pytest.raises(ValueError):
        TextPort().perceive("the weather is fine")
    with pytest.raises(ValueError):
        SyntheticVisionPort().perceive({"t": ["t1", "t2"], "objects": [{"id": "b", "positions": [[1, 2, 3]]}]})
    with pytest.raises(ValueError):
        SyntheticVisionPort().perceive({})
