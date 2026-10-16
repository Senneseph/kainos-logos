"""Default output-root resolution (results hygiene — see the handoff).

``KAINOS_RESULTS_DIR`` redirects the default output root. The test suite
sets it to a session tmpdir (``tests/conftest.py``) so that test runs
NEVER touch the repo's tracked ``results/`` artifacts — the 2026-08-21
root cause of the recurring "reports kept disappearing" (experiments with
a default ``out_dir`` rewrote the official evidence with test-time data:
commit=unknown, fast-sample env). Official runs leave the variable unset
(→ ``results/``) and are unaffected.

Imported from leaf modules (bench, benchmarks) — it must stay dependency-free
(no imports from ``kainos.harness.runner``; that module imports the benches).
"""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["default_phase_dir", "default_results_dir"]


def default_results_dir() -> Path:
    """Flat record root (``results/`` by default)."""

    return Path(os.environ.get("KAINOS_RESULTS_DIR", "results"))


def default_phase_dir(phase: int = 3) -> Path:
    """Full-report root (``results/phase-<n>`` by default)."""

    return default_results_dir() / f"phase-{phase}"
