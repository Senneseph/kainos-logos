"""bandgen — the band compiler (v0.1: validate / compute / control).

The per-band source of truth is a SPEC file (``bands/spec-*.json``,
schema ``specs/band_spec.schema.json``). bandgen never edits the
mechanism: it validates the spec, COMPUTES the frozen tables (beds
from reference functions, carry bytes from the seed store,
pre-states from a runtime boot), and DRY-RUNS the labeled script in a
scratch root to capture the mechanism's own letters, answers, and
mastery census — reporting the diff between the spec's predictions
and the mechanism. The official gate (pinned image, twin, P0–P8)
is unchanged: the compiler automates production, never the referee.

The store speaks, not the hand — including here: every captured
byte in the dry-run is the mechanism's, the compiler only reports.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
