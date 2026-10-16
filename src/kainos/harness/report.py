"""Markdown reporting for experiment results (plan 40-testing/harness.md)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # runtime-free import: runner -> report (one-way at runtime)
    from collections.abc import Iterable

    from kainos.harness.runner import Result

__all__ = ["render"]


def render(results: Iterable[Result]) -> str:
    """Render results as a markdown table (name / passed / value / threshold / evidence)."""

    lines = [
        "# Experiment results",
        "",
        "| name | passed | value | threshold | evidence |",
        "|------|--------|-------|-----------|----------|",
    ]
    for r in results:
        passed = "PASS" if r.passed else "FAIL"
        threshold = r.threshold or "—"
        evidence = ", ".join(f"`{p}`" for p in r.evidence) or "—"
        lines.append(f"| {r.name} | {passed} | {r.value} | {threshold} | {evidence} |")
    return "\n".join(lines)
