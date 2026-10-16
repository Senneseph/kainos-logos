"""E3.4 runner — multi-modal abstraction (the "one algebra" claim, modality level).

Scripted per `phase-3-generalization/experiments.md` → E3.4:

- Text port: ``"John moved the box"`` → IR (entity john/box + moved edge).
- Synthetic vision port: box at ``[0,0,0]`` at t1, ``[4,4,4]`` at t2 → IR
  (located_at edges with context).
- The SAME modality-blind ``abstract_pattern`` step reduces both IRs to the
  same abstract TRANSFER pattern (object=box) — the cross-modal match.
- The shared entity ``box`` is corroborated into a real CODEX store from
  BOTH modalities (provenance names the modality) — one entity, ≥2
  modalities.

Both IRs are validated against ``kainos/ir/1`` at the boundary. Deterministic
(fixed script, no RNG). Exit 0 iff the E3.4 threshold is met.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState, Provenance, Source, TermRef
from kainos.harness.paths import default_results_dir
from kainos.ir.codec import validate
from kainos.multimodal.port import TextPort, abstract_pattern
from kainos.multimodal.synthetic_vision import SyntheticVisionPort

__all__ = ["E3_4Experiment", "run_e3_4"]

_TEXT = "John moved the box"
_SCENE: dict[str, Any] = {"t": ["t1", "t2"], "objects": [{"id": "box", "positions": [[0.0, 0.0, 0.0], [4.0, 4.0, 4.0]]}]}


def _consolidate_entity(term_id: str, modalities: list[str], codex, observer: str) -> list[str]:
    """Corroborate one entity into the CODEX from every modality that saw it.
    One assertion per modality, provenance naming the modality — idempotent
    (deterministic ids; the step-19 discipline)."""

    ids: list[str] = []
    for m in modalities:
        aid = f"as_cons_e34_{term_id}_{m}"
        try:
            codex.get(aid)
            ids.append(aid)
            continue
        except KeyError:
            pass
        codex.add(
            Assertion(
                id=aid,
                subject=TermRef(id=term_id, labels=[term_id]),
                relation=TermRef(id="cited_by", labels=[]),
                object=m,
                status=EpistemicState.candidate,
                provenance=Provenance(
                    source=Source(uri=f"modality_{m}", version="1"),
                    observer=observer,
                ),
            )
        )
        ids.append(aid)
    return ids


def _entity_ids(ir: dict) -> set[str]:
    return {str(e["id"]) for e in ir.get("entities", [])}


def _sources_of(codex, ids: list[str]) -> set[str]:
    """Provenance source URIs behind a set of assertion ids (narrowed for mypy)."""

    out: set[str] = set()
    for aid in ids:
        prov = codex.get(aid).provenance
        assert prov is not None, "corroborations carry provenance"
        src = prov.source
        assert src is not None, "corroborations name a source"
        out.add(src.uri)
    return out


def run_e3_4(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = Path(out_dir) if out_dir is not None else default_results_dir()  # results hygiene
    text_ir = TextPort().perceive(_TEXT)
    vision_ir = SyntheticVisionPort().perceive(_SCENE)
    # boundary validation — every IR that enters the algebra must be ir/1:
    validate(text_ir)
    validate(vision_ir)

    p_text = abstract_pattern(text_ir)
    p_vision = abstract_pattern(vision_ir)
    pattern_matched = (
        p_text is not None and p_vision is not None and p_text.compatible(p_vision)
    )

    shared = _entity_ids(text_ir) & _entity_ids(vision_ir)
    codex = InMemoryCodexStore()
    corroboration: dict[str, list[str]] = {}
    for term in sorted(shared):
        corroboration[term] = _consolidate_entity(
            term,
            ["synthetic_vision", "text"],  # sorted modality order — deterministic
            codex,
            observer="e3.4",
        )

    consolidated = [
        term
        for term, ids in sorted(corroboration.items())
        if len(_sources_of(codex, ids)) >= 2
    ]
    entity_consolidated = bool(consolidated)
    passed = bool(pattern_matched and entity_consolidated)

    report: dict[str, Any] = {
        "config": {
            "commit": os.environ.get("KAINOS_GIT_COMMIT", "unknown"),
            "text": _TEXT,
            "scene": _SCENE,
            "ports": ["text", "synthetic_vision"],
        },
        "text_ir": text_ir,
        "vision_ir": vision_ir,
        "patterns": {
            "text": p_text.to_dict() if p_text else None,
            "vision": p_vision.to_dict() if p_vision else None,
        },
        "pattern_matched_cross_modal": bool(pattern_matched),
        "shared_entities": sorted(shared),
        "consolidation": {
            term: {
                "assertion_ids": ids,
                "modalities": sorted(_sources_of(codex, ids)),
            }
            for term, ids in sorted(corroboration.items())
        },
        "entity_consolidated": entity_consolidated,
        "consolidated_entities": consolidated,
        "passed": bool(passed),
    }
    (out_dir / "phase-3").mkdir(parents=True, exist_ok=True)
    (out_dir / "phase-3" / "e3.4.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


class E3_4Experiment:
    """Phase-2-harness Experiment for E3.4 (multi-modal abstraction)."""

    name = "e3.4"
    hypothesis = (
        "a synthetic 'vision' modality and text produce the SAME abstract CODEX "
        "pattern (TRANSFER) and corroborate a shared entity — the one-algebra "
        "claim at the modality level"
    )
    metric = (
        "cross-modal corroboration (one entity consolidated from >=2 modalities, "
        "provenance names the modality) + pattern-match success (one abstract "
        "pattern recognized across modalities)"
    )
    threshold = (
        "one entity consolidated from >=2 modalities; one abstract pattern "
        "recognized across modalities"
    )

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e3_4()
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=1.0 if report["passed"] else 0.0,
            evidence=[Path("results/phase-3/e3.4.json")],
            config={
                "pattern_matched": report["pattern_matched_cross_modal"],
                "entity_consolidated": report["entity_consolidated"],
                "consolidated_entities": report["consolidated_entities"],
                "patterns": report["patterns"],
            },
        )
