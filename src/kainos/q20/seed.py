"""Seed the 20Q corpus into the CODEX (step 13).

Every concept/property/category becomes an assertion with mandatory
provenance (ADR-0008): the corpus is knowledge the reasoner can see, not a
parallel data structure.

Shape (per concept C in category K with property p=v):
    C --has_property--> "p=v"          (object as the literal value string)
    C --is_a--> K                       (category term)

Properties ABSENT from the corpus are NOT written as assertions — absence
stays the ``unknown`` signal (the deliberate EXCEPTION seeds).
"""

from __future__ import annotations

from kainos.codex.models import (
    Assertion,
    EpistemicState,
    Provenance,
    Source,
    TermRef,
)

__all__ = ["HAS_PROPERTY", "IS_A", "SOURCE_URI", "SOURCE_VERSION", "seed"]

SOURCE_URI = "q20_corpus"
SOURCE_VERSION = "1"
HAS_PROPERTY = "has_property"
IS_A = "is_a"


def _provenance() -> Provenance:
    return Provenance(
        source=Source(uri=SOURCE_URI, version=SOURCE_VERSION),
        observer=SOURCE_URI,
        verified=True,
    )


def seed(codex, corpus: list[dict] | None = None) -> dict:
    """Add the corpus as established, provenance-marked assertions.

    Returns stats: {"concepts", "property_assertions", "category_assertions",
    "total"}. Idempotent-safe (assertion ids are deterministic upserts).
    """

    from kainos.q20.oracle import load_corpus

    if corpus is None:
        corpus = load_corpus()
    stats = {"concepts": 0, "property_assertions": 0, "category_assertions": 0, "total": 0}
    for c in corpus:
        term = TermRef(id=c["id"], labels=[c["label"]])
        for prop, value in sorted(c["properties"].items()):
            codex.add(
                Assertion(
                    id=f"as_{c['id']}_hp_{prop}",
                    subject=term,
                    relation=TermRef(id=HAS_PROPERTY),
                    object=f"{prop}={value}",
                    status=EpistemicState.established,
                    provenance=_provenance(),
                )
            )
            stats["property_assertions"] += 1
        for category in c["categories"]:
            codex.add(
                Assertion(
                    id=f"as_{c['id']}_isa_{category}",
                    subject=term,
                    relation=TermRef(id=IS_A),
                    object=TermRef(id=category, labels=[category]),
                    status=EpistemicState.established,
                    provenance=_provenance(),
                )
            )
            stats["category_assertions"] += 1
        stats["concepts"] += 1
    stats["total"] = stats["property_assertions"] + stats["category_assertions"]
    return stats
