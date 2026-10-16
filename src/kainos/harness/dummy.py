"""The dummy experiment (P0.09) — an end-to-end canary for the harness.

Proves registration, execution, reproducibility config, persistence, and report
rendering work, before any real science is attempted. It is deliberately
intelligence-free: passing is deterministic by construction.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from kainos.harness.paths import default_results_dir

if TYPE_CHECKING:
    from kainos.harness.runner import Result

__all__ = ["DummyExperiment"]


class DummyExperiment:
    name = "dummy"
    hypothesis = "the harness executes a registered experiment end-to-end and persists an auditable result (config with seed/commit/dataset_hash + evidence file)"
    metric = "dummy_success (1.0 = runner + persistence + report all worked)"
    threshold = "== 1.0"

    def __init__(self, results_dir: Path | None = None) -> None:
        self._results_dir = results_dir if results_dir is not None else default_results_dir()

    def run(self) -> Result:
        # Local import breaks the runner <-> dummy import cycle (Result is only
        # needed to construct the return value).
        from kainos.harness.runner import Result

        evidence = self._results_dir / "dummy.evidence.json"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(
            json.dumps({"ok": True, "note": "harness canary — evidence is a file path, not prose"}, indent=2)
            + "\n",
            encoding="utf-8",
        )
        return Result(
            name=self.name,
            passed=True,
            value=1.0,
            evidence=[evidence],
            config={"seed": 0, "dataset_hash": None},
        )
