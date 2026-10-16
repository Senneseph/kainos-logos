"""Declared capabilities as first-class CODEX terms (P11, ADR-0011, P3.12).

A capability is *declared, not implied*: the planner may only use capabilities
present in the store as established assertions. Adding or removing a
capability is a **store operation** (assertion add / status -> ``obsolete``),
never a code change — this module's seed set is data, mirrored from the
design doc's four simulated capabilities.

Storage shape (one capability = one term + three ``has_property`` assertions):

    SEARCH_CODEX --has_property--> preconditions=<comma list or empty>
    SEARCH_CODEX --has_property--> effect=<comma list>
    SEARCH_CODEX --has_property--> cost=<float>

The seed set deliberately has **no image capability**: E3.6's unachievable
goal test depends on that absence (honest refusal, not fabrication).
"""

from __future__ import annotations

from dataclasses import dataclass

from kainos.codex.models import Assertion, EpistemicState, Provenance, Source, TermRef
from kainos.codex.store import CodexStore

__all__ = [
    "CAPABILITY_KIND",
    "DEFAULT_CAPABILITIES",
    "Capability",
    "capability_id",
    "load_capabilities",
    "obsoletize_capability",
    "seed_capabilities",
]

CAPABILITY_KIND = "capability"
_HAS_PROPERTY = "has_property"

@dataclass(frozen=True)
class Capability:
    """A declared capability: preconditions that must hold + effect facts
    added when applied + a search cost. Frozen data — the CODEX is the
    system of record; this is its in-memory view."""

    name: str
    preconditions: tuple[str, ...]
    effect: tuple[str, ...]
    cost: float

    def to_assertions(self) -> list[Assertion]:
        """The capability's store rows (term + preconditions/effect/cost
        properties), all ``established`` with seed provenance."""

        subject = TermRef(id=self.name, labels=[self.name.lower().replace("_", " ")], kind=CAPABILITY_KIND)
        prov = Provenance(source=Source(uri="capability_seed", version="1"), observer="capability_seed", verified=True)
        rows = [
            f"preconditions={','.join(self.preconditions)}",
            f"effect={','.join(self.effect)}",
            f"cost={self.cost!r}",
        ]
        return [
            Assertion(
                id=f"as_cap_{self.name}_{tag}",
                subject=subject,
                relation=TermRef(id=_HAS_PROPERTY, labels=["has property"]),
                object=obj,
                status=EpistemicState.established,
                provenance=prov,
            )
            for tag, obj in zip(("pre", "effect", "cost"), rows)
        ]


def capability_id(name: str) -> str:
    return name  # capability term id == its name (declared term, ADR-0011)


def seed_capabilities(codex: CodexStore, names: list[str] | None = None) -> None:
    """Add (idempotently) the named capabilities (default: the four seeds) as
    established assertions. Calling this with a NEW name is itself the
    store-operation way to grant a capability — no code change (P11)."""

    chosen = {c.name: c for c in DEFAULT_CAPABILITIES}
    for n in names or [c.name for c in DEFAULT_CAPABILITIES]:
        if n not in chosen:
            raise ValueError(f"unknown capability name: {n} (declare it as a Capability first)")
        for a in chosen[n].to_assertions():
            codex.add(a)


def load_capabilities(codex: CodexStore) -> dict[str, Capability]:
    """Every capability in the store with an ESTABLISHED preconditions row
    (plus its established effect/cost rows) — i.e. declared and not
    obsoletized. This is the planner's only legal move set (P11)."""

    raw: dict[str, dict[str, str]] = {}
    for a in codex.query(relation=_HAS_PROPERTY):
        if a.status != EpistemicState.established or not isinstance(a.object, str):
            continue
        key = a.object.split("=", 1)
        if len(key) != 2 or key[0] not in ("preconditions", "effect", "cost"):
            continue
        raw.setdefault(a.subject.id, {}).setdefault(key[0], key[1])
    caps: dict[str, Capability] = {}
    for name, d in raw.items():
        if "preconditions" not in d:
            continue  # not a declared capability row
        pre = tuple(x for x in d["preconditions"].split(",") if x)
        effect = tuple(x for x in d.get("effect", "").split(",") if x)
        cost = float(d["cost"]) if d.get("cost") else 1.0
        caps[name] = Capability(name=name, preconditions=pre, effect=effect, cost=cost)
    return caps


def obsoletize_capability(codex: CodexStore, name: str) -> int:
    """Remove a capability the store way: every one of its assertions goes
    ``obsolete``. Returns the number of assertions retired."""

    n = 0
    for a in codex.query(subject=name, relation=_HAS_PROPERTY):
        if a.status != EpistemicState.obsolete:
            codex.update_status(a.id, EpistemicState.obsolete, evidence=[f"obsoletize:{name}"])
            n += 1
    return n

#: The four simulated capabilities (design doc / directive 21). Fact names are
#: the projection's state vocabulary; effects are pure label additions — no
#: side effects of any kind are executed (scope guard: simulated).
DEFAULT_CAPABILITIES: tuple[Capability, ...] = (
    Capability(name="SEARCH_CODEX", preconditions=(), effect=("knowledge_located",), cost=1.0),
    Capability(name="WRITE_TEXT", preconditions=("knowledge_located",), effect=("artifact_available",), cost=1.0),
    Capability(name="ASK_USER", preconditions=(), effect=("user_clarification",), cost=1.0),
    Capability(name="READ_SOURCE", preconditions=("source_referenced",), effect=("source_content",), cost=1.0),
)


