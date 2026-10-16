"""CODEX lexicon seed (P1.04) — what words MEAN lives here, not in the parser.

Phase 1 seeds a tiny lexicon into the CODEX (invariant #2: meaning in the CODEX,
invariant #1: everything with provenance). The parser (step 07 kernel) resolves
bare content words through a **direct lookup** of these assertions; the
emitter's built-in class table is held consistent with this seed by the
lexicon<->emitter parity test (spec §5). Adding a new realization = one more
assertion here — no parser change.
"""

from __future__ import annotations

from kainos.codex.models import (
    Assertion,
    Context,
    EpistemicState,
    Provenance,
    Source,
    TermRef,
)
from kainos.codex.store import CodexStore

__all__ = ["LEXICON", "RELATES_SURFACES_TO", "seed"]

# surface (lexicon term) -> PCRE realization
LEXICON: dict[str, str] = {
    "hyphen": "-",
    "digit": r"\d",
    "letter": "[A-Za-z]",
    "word": r"\w",
    "whitespace": r"\s",
    "any": ".",
    "start": "^",
    "end": "$",
}

RELATES_SURFACES_TO = "realizes_as"


def _term(id: str, kind: str) -> TermRef:
    return TermRef(id=id, kind=kind, labels=[id])


def seed(codex: CodexStore) -> list[str]:
    """Seed the lexicon into a CODEX store; returns the seeded assertion ids.

    Every assertion is `status=established` with `Source(uri="seed_corpus",
    version="1")` provenance and `verified=True` (invariant #1).
    """

    ids: list[str] = []
    for surface, realization in LEXICON.items():
        assertion = Assertion(
            id=f"lexicon-{surface}",
            subject=_term(surface, "entity"),
            relation=_term(RELATES_SURFACES_TO, "relation"),
            object=realization,
            polarity=True,
            context=Context(data={"lexicon": "phase-1-regex"}),
            validity=None,
            confidence=1.0,
            status=EpistemicState.established,
            provenance=Provenance(
                source=Source(uri="seed_corpus", version="1", media_type="text/plain"),
                observer="seed",
                derived=False,
                verified=True,
                evidence=[],
            ),
            exception=None,
        )
        assert codex.add(assertion) == assertion.id
        ids.append(assertion.id)
    return ids
