"""kainos.lang — the "language organ" (invariant #2): text <-> IR only.

Phase 1 ships the deterministic kernel (`DeterministicKernel`) so the
compositionality experiment is not confounded by an LLM's latent regex knowledge;
the neural kernel arrives in step 17 behind the same `LanguageKernel` protocol.
"""

from __future__ import annotations

from kainos.lang.deterministic import DeterministicKernel, parse_regex_text
from kainos.lang.kernel import Interpretation, LanguageKernel

__all__ = ["DeterministicKernel", "Interpretation", "LanguageKernel", "parse_regex_text"]
