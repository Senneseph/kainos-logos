"""Growth dashboard: EXCEPTION shrinkage + coverage over time (step 15).

``sample_growth`` measures what has actually changed in the CODEX since
the last sample — coverage per concept (verified/encountered), assertion
status mix, exception states, 'sometimes' cells, and the dimension terms
that contradiction has expanded the ontology with. ``render`` is a pure
dict -> markdown; ``write_growth`` persists ``results/phase-2/growth.md``.
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from kainos.q20.learn import DIM_KIND

__all__ = ["render", "sample_growth", "write_growth"]


def sample_growth(codex, corpus: list[dict], questions: list[dict]) -> dict:
    """One growth sample (dict, JSON-serializable, deterministic order)."""

    by_status: Counter = Counter()
    by_exception: Counter = Counter()
    sometimes = 0
    disputed_terms = set()
    for a in codex.query():
        by_status[a.status.value] += 1
        if a.exception is not None:
            by_exception[a.exception.value] += 1
        if isinstance(a.object, str) and a.object.endswith("=sometimes"):
            sometimes += 1
        if a.status.value == "disputed":
            disputed_terms.add(a.subject.id)
    terms = codex.dump()["terms"]
    dimensions = sorted(t["id"] for t in terms if t.get("kind") == DIM_KIND)
    coverage = {c["id"]: codex.coverage(c["id"]) for c in corpus}
    return {
        "sampled_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "n_assertions": sum(by_status.values()),
        "by_status": dict(sorted(by_status.items())),
        "by_exception": dict(sorted(by_exception.items())),
        "sometimes_cells": sometimes,
        "dimensions": dimensions,
        "disputed_terms": sorted(disputed_terms),
        "coverage_mean": round(sum(coverage.values()) / len(coverage), 4) if coverage else 0.0,
        "coverage_min": round(min(coverage.values()), 4) if coverage else 0.0,
        "coverage_zero_concepts": sorted(t for t, v in coverage.items() if v == 0.0),
        "coverage": {t: round(v, 4) for t, v in sorted(coverage.items())},
    }


def render(sample: dict) -> str:
    """Pure markdown renderer (no I/O)."""

    lines = [
        "# 20Q growth dashboard",
        "",
        f"- Sampled: `{sample['sampled_at']}`",
        f"- Assertions: **{sample['n_assertions']}**",
        "- Status mix: " + ", ".join(f"{k}: {v}" for k, v in sample["by_status"].items()),
        "- Exception states: "
        + (", ".join(f"{k}: {v}" for k, v in sample["by_exception"].items()) or "(none)"),
        f"- 'sometimes' cells: **{sample['sometimes_cells']}**",
        f"- Dimensions expanded by contradiction: **{len(sample['dimensions'])}**"
        + (f" — {', '.join(sample['dimensions'])}" if sample["dimensions"] else ""),
        "",
        "## Coverage per concept (verified / encountered)",
        "",
        f"- Mean: **{sample['coverage_mean']:.4f}** · Min: **{sample['coverage_min']:.4f}**",
        f"- Concepts at 0.0000: {len(sample['coverage_zero_concepts'])} of {len(sample['coverage'])}",
        "",
        "| concept | coverage |",
        "|---------|---------:|",
    ]
    for concept, value in sample["coverage"].items():
        lines.append(f"| {concept} | {value:.4f} |")
    if sample["disputed_terms"]:
        lines += ["", "## Disputed", "", ", ".join(sample["disputed_terms"])]
    return "\n".join(lines) + "\n"


def write_growth(codex, corpus: list[dict], questions: list[dict], out_path: str | Path = "results/phase-2/growth.md") -> Path:
    """Sample + render + persist. Returns the written path."""

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(sample_growth(codex, corpus, questions)))
    return out
