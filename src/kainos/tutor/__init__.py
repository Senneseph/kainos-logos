"""kainos.tutor — the Interactive Tutor horizon (epic #150; registry phase 6).

An "infant" that speaks the OpenAI protocol and runs the stack: CODEX as
durable knowledge (provenance-mandatory), WORKSPACE as session memory, the 7
interaction contracts as the dialogue discipline, and a BRAINSTEM turn loop
(perceive -> classify -> policy -> grounded response -> memory write).
Mastery and curriculum are STORE DATA (P11): recomputed from the CODEX,
auditable, never a hidden state.
"""

from __future__ import annotations

from kainos.tutor.brainstem import Brainstem, TurnResult, det_classify, fixed_epoch
from kainos.tutor.facade import MODEL_ID, InfantServer, make_server
from kainos.tutor.mastery import BANDS, Concept, MasteryState, MasteryView, mastery_view
from kainos.tutor.sequencer import REEXPOSE_INTERVAL, due_concepts, next_drill
from kainos.tutor.session import InfantRuntime, SessionReport

__all__ = [
    "BANDS",
    "MODEL_ID",
    "REEXPOSE_INTERVAL",
    "Brainstem",
    "Concept",
    "InfantRuntime",
    "InfantServer",
    "MasteryState",
    "MasteryView",
    "SessionReport",
    "TurnResult",
    "det_classify",
    "due_concepts",
    "fixed_epoch",
    "make_server",
    "mastery_view",
    "next_drill",
]
