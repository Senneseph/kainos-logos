"""The regex-dialect AST (P1.01) — the Semantic IR's regex specialization.

Every node maps **losslessly** onto the generic IR (kainos/ir/1, spec
`specs/ir.schema.json` — the schema wins): a node is an `entity` whose `type`
carries the dialect node name and whose scalar payload goes in `labels`; the tree
shape is wired by `relationships` (`sequence` / `flag` edges for Sequence,
`repeat` (quantifier in `context`), `alternative_branch`, and `group` for Group —
an additive relation beyond the four the directive inlines, since every container
edge needs one). `UnresolvedRef` maps onto the generic IR's first-class
`unresolved` shape (surface + candidates), not onto an entity — an entity's closed
shape has no room for them.

`to_ir(node)` produces a full generic pattern document with **deterministic**
pre-order ids (`e0..eN`, `u0..uM` for unresolved) and is validated at the
boundary; `from_ir(doc)` reverses it. Structural equality ignores the
serialization identity (`id`, compare=False), so `from_ir(to_ir(x)) == x`.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from kainos.ir.codec import validate

__all__ = [
    "DIALECT",
    "Alternative",
    "Anchor",
    "AnchorKind",
    "Class",
    "ClassKind",
    "Flag",
    "Group",
    "Literal",
    "Node",
    "QuantKind",
    "Quantifier",
    "Repeat",
    "Sequence",
    "UnresolvedRef",
    "from_ir",
    "to_ir",
]

DIALECT = "kainos/regex/1"


class ClassKind(Enum):
    digit = "digit"
    letter = "letter"
    word = "word"
    whitespace = "whitespace"
    any = "any"


class AnchorKind(Enum):
    start = "start"
    end = "end"


class QuantKind(Enum):
    one_or_more = "one_or_more"
    zero_or_more = "zero_or_more"
    optional = "optional"
    exactly = "exactly"
    at_least = "at_least"
    at_most = "at_most"
    between = "between"


@dataclass(frozen=True)
class Quantifier:
    """Quantifier family: the no-arg kinds are constants; parameterized ones carry
    `n` (exactly/at_least/at_most) or `a`/`b` (between)."""

    kind: QuantKind
    n: int | None = None
    a: int | None = None
    b: int | None = None

    @classmethod
    def one_or_more(cls) -> Quantifier:
        return cls(QuantKind.one_or_more)

    @classmethod
    def zero_or_more(cls) -> Quantifier:
        return cls(QuantKind.zero_or_more)

    @classmethod
    def optional(cls) -> Quantifier:
        return cls(QuantKind.optional)

    @classmethod
    def exactly(cls, n: int) -> Quantifier:
        return cls(QuantKind.exactly, n=n)

    @classmethod
    def at_least(cls, n: int) -> Quantifier:
        return cls(QuantKind.at_least, n=n)

    @classmethod
    def at_most(cls, n: int) -> Quantifier:
        return cls(QuantKind.at_most, n=n)

    @classmethod
    def between(cls, a: int, b: int) -> Quantifier:
        return cls(QuantKind.between, a=a, b=b)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"kind": self.kind.value}
        if self.n is not None:
            d["n"] = self.n
        if self.a is not None:
            d["a"] = self.a
        if self.b is not None:
            d["b"] = self.b
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Quantifier:
        return cls(QuantKind(d["kind"]), d.get("n"), d.get("a"), d.get("b"))


@dataclass
class Node:
    """Base for all dialect nodes.

    `id` is the serialization identity — assigned deterministically by `to_ir`
    (or taken from an earlier `from_ir`) and excluded from equality so structural
    round-trips compare clean trees.
    """

    id: str | None = field(default=None, compare=False, kw_only=True)

    def _entity(self, node_id: str | None, type_: str, labels: list[str] | None = None) -> dict[str, Any]:
        nid = node_id or self.id
        if nid is None:
            raise ValueError(
                f"{type_} node has no id — use to_ir(), which assigns deterministic ids, "
                "or pass node_id explicitly"
            )
        e: dict[str, Any] = {"id": nid, "type": type_}
        if labels is not None:
            e["labels"] = labels
        return e

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        """One node as a generic-IR item (an Entity, or the unresolved shape for
        UnresolvedRef). Trees — children wired via relationships — are to_ir(node)."""

        raise NotImplementedError

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Node:
        raise NotImplementedError


@dataclass
class Sequence(Node):
    elements: list[Node] = field(default_factory=list)

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        return self._entity(node_id, "Sequence")

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Node:
        if doc is None:
            raise ValueError("container nodes need the full document to rebuild children; use from_ir()")
        return _build_from_doc(doc, entity["id"])


@dataclass
class Repeat(Node):
    node: Node
    quantifier: Quantifier

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        return self._entity(node_id, "Repeat")

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Node:
        if doc is None:
            raise ValueError("container nodes need the full document to rebuild children; use from_ir()")
        return _build_from_doc(doc, entity["id"])


@dataclass
class Class(Node):
    kind: ClassKind

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        return self._entity(node_id, "Class", [self.kind.value])

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Class:
        return cls(kind=ClassKind(entity["labels"][0]), id=entity["id"])


@dataclass
class Literal(Node):
    """Literal text (emitter escapes regex metacharacters — spec §3).

    `raw=True` marks a value learned from the CODEX — a regex fragment that
    the emitter must pass through un-escaped (e.g. a taught
    `\\d{3}-\\d{3}-\\d{4}`). The marker rides as a namespaced string label
    (`kainos:raw`), so the generic schema needs no change and documents
    without it are byte-identical."""

    text: str
    raw: bool = False

    RAW_MARKER = "kainos:raw"

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        labels = [self.text]
        if self.raw:
            labels.append(self.RAW_MARKER)
        return self._entity(node_id, "Literal", labels)

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Literal:
        labels = list(entity["labels"])
        raw = cls.RAW_MARKER in labels
        return cls(text=labels[0], raw=raw, id=entity["id"])


@dataclass
class Anchor(Node):
    kind: AnchorKind

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        return self._entity(node_id, "Anchor", [self.kind.value])

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Anchor:
        return cls(kind=AnchorKind(entity["labels"][0]), id=entity["id"])


@dataclass
class Alternative(Node):
    branches: list[Node] = field(default_factory=list)

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        return self._entity(node_id, "Alternative")

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Node:
        if doc is None:
            raise ValueError("container nodes need the full document to rebuild children; use from_ir()")
        return _build_from_doc(doc, entity["id"])


@dataclass
class Group(Node):
    node: Node

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        return self._entity(node_id, "Group")

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Node:
        if doc is None:
            raise ValueError("container nodes need the full document to rebuild children; use from_ir()")
        return _build_from_doc(doc, entity["id"])


@dataclass
class Flag(Node):
    name: str  # e.g. "case_insensitive"

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        return self._entity(node_id, "Flag", [self.name])

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> Flag:
        return cls(name=entity["labels"][0], id=entity["id"])


@dataclass
class UnresolvedRef(Node):
    """A surface the parser could not pin to a realization (step 07) — the resolver
    (step 08) rotates its candidates; the emitter refuses to run with one present."""

    surface: str
    candidates: list[str] = field(default_factory=list)

    def to_generic(self, node_id: str | None = None) -> dict[str, Any]:
        nid = node_id or self.id
        if nid is None:
            raise ValueError("UnresolvedRef node has no id — use to_ir() or pass node_id explicitly")
        d: dict[str, Any] = {"id": nid, "surface": self.surface}  # generic `unresolved` shape
        if self.candidates:
            d["candidates"] = list(self.candidates)
        return d

    @classmethod
    def from_generic(cls, entity: dict[str, Any], doc: dict[str, Any] | None = None) -> UnresolvedRef:
        return cls(surface=entity["surface"], candidates=list(entity.get("candidates", [])), id=entity["id"])


# ── document-level mapping (the lossless contract) ─────────────────────────


def to_ir(node: Node) -> dict[str, Any]:
    """Dialect tree → generic pattern document (kainos/ir/1), validated at the
    boundary. Ids are deterministic (pre-order): e0..eN for entities, u0..uM for
    unresolved refs — the same tree always yields the same document."""

    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []

    def walk(n: Node) -> str:
        if isinstance(n, UnresolvedRef):
            nid = f"u{len(unresolved)}"
            unresolved.append(n.to_generic(nid))
        else:
            nid = f"e{len(entities)}"
            entities.append(n.to_generic(nid))
        if isinstance(n, Sequence):
            for i, el in enumerate(n.elements):
                child = walk(el)
                # A Flag element rides a dedicated `flag` edge (order kept in context).
                relation = "flag" if isinstance(el, Flag) else "sequence"
                relationships.append(
                    {"subject": nid, "relation": relation, "object": child, "context": {"position": i}}
                )
        elif isinstance(n, Alternative):
            for i, br in enumerate(n.branches):
                relationships.append(
                    {"subject": nid, "relation": "alternative_branch", "object": walk(br), "context": {"branch": i}}
                )
        elif isinstance(n, Repeat):
            relationships.append(
                {"subject": nid, "relation": "repeat", "object": walk(n.node), "context": n.quantifier.to_dict()}
            )
        elif isinstance(n, Group):
            relationships.append({"subject": nid, "relation": "group", "object": walk(n.node)})
        return nid

    walk(node)
    doc: dict[str, Any] = {
        "kind": "pattern",
        "entities": entities,
        "relationships": relationships,
        "meta": {"dialect": DIALECT},
    }
    if unresolved:
        doc["unresolved"] = unresolved
    validate(doc)  # never emit a dialect document the generic boundary would reject
    return doc


def from_ir(doc: dict[str, Any]) -> Node:
    """Generic pattern document → dialect tree. Raises ValueError on any document
    that is not a well-formed single-root dialect mapping (the codec validates
    the generic shape first)."""

    validate(doc)
    if doc.get("kind") != "pattern":
        raise ValueError(f"not a pattern document (kind={doc.get('kind')!r})")
    _build = _make_builder(doc)
    referenced = {r["object"] for r in doc.get("relationships", [])}
    lookup = _lookup_ids(doc)
    roots = [i for i in lookup if i not in referenced]
    if len(roots) != 1:
        raise ValueError(f"dialect document must have exactly one root, found {len(roots)}: {sorted(roots)}")
    return _build(roots[0], frozenset())


def _lookup_ids(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    ids: dict[str, dict[str, Any]] = {u["id"]: u for u in doc.get("unresolved", [])}
    ids.update({e["id"]: e for e in doc.get("entities", [])})
    return ids


def _make_builder(doc: dict[str, Any]):
    lookup = _lookup_ids(doc)
    children: dict[str, list[tuple[str, str, dict[str, Any]]]] = defaultdict(list)
    for r in doc.get("relationships", []):
        if r["object"] not in lookup:
            raise ValueError(f"dangling relationship object {r['object']!r}")
        children[r["subject"]].append((r["relation"], r["object"], r.get("context", {})))

    def build(node_id: str, path: frozenset[str]) -> Node:
        if node_id in path:
            raise ValueError(f"cyclic dialect document at {node_id!r}")
        path = path | {node_id}
        item = lookup[node_id]
        if "type" not in item:
            return UnresolvedRef(
                surface=item["surface"], candidates=list(item.get("candidates", [])), id=node_id
            )
        labels = list(item.get("labels", []))
        kids = children.get(node_id, [])

        def sub(rel: str) -> list[tuple[str, dict[str, Any]]]:
            return [(o, c) for (r, o, c) in kids if r == rel]

        t = item["type"]
        if t == "Sequence":
            ordered = sorted(sub("sequence") + sub("flag"), key=lambda oc: oc[1].get("position", 0))
            return Sequence(elements=[build(o, path) for o, _ in ordered], id=node_id)
        if t == "Alternative":
            ordered = sorted(sub("alternative_branch"), key=lambda oc: oc[1].get("branch", 0))
            return Alternative(branches=[build(o, path) for o, _ in ordered], id=node_id)
        if t == "Group":
            g = sub("group")
            if len(g) != 1:
                raise ValueError(f"Group node {node_id!r} must have exactly one group edge")
            return Group(node=build(g[0][0], path), id=node_id)
        if t == "Repeat":
            g = sub("repeat")
            if len(g) != 1:
                raise ValueError(f"Repeat node {node_id!r} must have exactly one repeat edge")
            return Repeat(node=build(g[0][0], path), quantifier=Quantifier.from_dict(g[0][1]), id=node_id)
        if t == "Literal":
            return Literal(text=labels[0], raw=Literal.RAW_MARKER in labels, id=node_id)
        if t == "Class":
            return Class(kind=ClassKind(labels[0]), id=node_id)
        if t == "Anchor":
            return Anchor(kind=AnchorKind(labels[0]), id=node_id)
        if t == "Flag":
            return Flag(name=labels[0], id=node_id)
        raise ValueError(f"unknown dialect node type {t!r}")

    return build


def _build_from_doc(doc: dict[str, Any], node_id: str) -> Node:
    """Node.from_generic(entity, doc) for container nodes — rebuild that node's
    subtree from the document."""

    return _make_builder(doc)(node_id, frozenset())
