"""E5.4 — the LLM-surface messaging arm (T6 #166, M4 stretch).

The message SURFACE of the game channel: a delta's CLAIM travels as a
plain-English sentence; the deterministic parser reconstructs the exact
delta before anything is delivered or merged. Pre-registered in
``plan/30-phases/phase-5-multi-agent/experiments.md`` — E5.4 (frozen
before implementation):

- One surface, two consumers (ticket design decision): the seam shares
  ``lang.llm.Backend`` (the same backend object E3.1's ``LLMKernel``
  drives), the E3.1 SKIP semantics, and the bounded-retry-then-drop
  discipline. The game grammar is game-local frozen data.
- The LLM renders only. The DETERMINISTIC parser is the only authority
  (D-e6b generalized): a render that does not round-trip to the exact
  original assertion id is DROPPED and logged — never rescued, never
  silently accepted (invariant #6).
- SKIP: no backend => the canonical-codec arm is the official run; no
  codec at all => the structured arm (the E5.1 baseline).

Transport sideband: the sentence carries the claim (class, subject,
value); sender-attribution, scope, round/game-kind/order timestamp
travel as structured metadata, restored verbatim. The transcript
records the surface's own audit log per delta (renderer, text,
delivered|dropped).
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from kainos.exchange.protocol import AssertionDelta
from kainos.game.agent import VALUE_KEY

__all__ = [
    "GRAMMAR_SHA",
    "LLM_SYSTEM_PROMPT",
    "CanonicalRenderer",
    "ClaimSpec",
    "LlmRenderer",
    "ScriptedDropRenderer",
    "SurfaceCodec",
    "claim_from_delta",
    "parse_sentence",
    "render_sentence",
]

#: The frozen grammar (exactly the pre-registered forms).
_CELL_RE = re.compile(
    r"^(?P<sender>a|b) says: (?P<cell>r[1-5]c[1-4]) is (?P<value>empty|wall|goal|key|door)\.$"
)
_ANCHOR_RE = re.compile(
    r"^(?P<sender>a|b) says: my door in row 3 is at column c(?P<col>[1-4])\.$"
)
_CORRECT_RE = re.compile(
    r"^(?P<sender>a|b) says: (?P<target>a|b), your door reading is c(?P<other>[1-4]), mine is c(?P<mine>[1-4])\.$"
)

GRAMMAR_FORMS: dict[str, str] = {
    "cell": "{s} says: {cell} is {value}.",
    "anchor": "{s} says: my door in row 3 is at column c{col}.",
    "correct": "{s} says: {target}, your door reading is c{other}, mine is c{mine}.",
}
GRAMMAR_SHA: str = (
    "sha256:"
    + hashlib.sha256(
        json.dumps(
            {
                "forms": GRAMMAR_FORMS,
                "patterns": [_CELL_RE.pattern, _ANCHOR_RE.pattern, _CORRECT_RE.pattern],
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
)

DOOR_SUBJECT = "row3:door"
CELL_VALUES: tuple[str, ...] = ("empty", "wall", "goal", "key", "door")

LLM_SYSTEM_PROMPT = (
    "You are the plain-language message channel of a two-agent grid game. "
    "There are two senders, 'a' and 'b'. Transmit exactly one English "
    "sentence, using EXACTLY one of these three forms (substitute the "
    "bracketed parts; keep the wording and punctuation):\n"
    "1) Cell claim: '<sender> says: <cell> is <value>.' where <cell> looks "
    "like r1c2 (rows 1-5, columns 1-4) and <value> is one of: empty, wall, "
    "goal, key, door.\n"
    "2) Door anchor: '<sender> says: my door in row 3 is at column "
    "c<column>.' where <column> is 1-4.\n"
    "3) Door correction: '<sender> says: <other>, your door reading is "
    "c<your_column>, mine is c<my_column>.' where the columns are 1-4.\n"
    "Write only the sentence. No quotes, no extra words."
)


@dataclass(frozen=True)
class ClaimSpec:
    """The claim a delta makes, in surface terms (the sentence's
    content — attribution/scope/timestamp are sideband metadata)."""

    form: str  # "cell" | "anchor" | "correct"
    sender: str  # "a" | "b"
    parts: dict[str, str]

    def subject(self) -> str:
        if self.form == "cell":
            return self.parts["cell"]
        if self.form == "anchor":
            return DOOR_SUBJECT
        return f"agent:{self.parts['target']}"

    def relation(self) -> str:
        return "corrects" if self.form == "correct" else "is"

    def object_id(self) -> str:
        if self.form == "cell":
            return f"{VALUE_KEY}={self.parts['value']}"
        if self.form == "anchor":
            return f"{VALUE_KEY}=c{self.parts['col']}"
        return f"{DOOR_SUBJECT} mine=c{self.parts['mine']} other=c{self.parts['other']}"


def claim_from_delta(d: AssertionDelta) -> ClaimSpec | None:
    """Classify one channel delta into its surface claim; None = not a
    grammatical surface claim (nothing this surface can say)."""

    a = d.assertion
    subj, rel, obj = a.subject.id, a.relation.id, a.object_id
    sender = d.node_id
    if sender not in ("a", "b"):
        return None
    if rel == "is":
        if (
            re.fullmatch(r"r[1-5]c[1-4]", subj)
            and obj.startswith(f"{VALUE_KEY}=")
            and obj[len(f"{VALUE_KEY}=") :] in CELL_VALUES
        ):
            return ClaimSpec(
                "cell", sender, {"cell": subj, "value": obj[len(f"{VALUE_KEY}=") :]}
            )
        if (
            subj == DOOR_SUBJECT
            and obj.startswith(f"{VALUE_KEY}=")
            and re.fullmatch(r"c[1-4]", obj[len(f"{VALUE_KEY}=") :])
        ):
            return ClaimSpec("anchor", sender, {"col": obj[len(f"{VALUE_KEY}=") :][1:]})
        return None
    if (
        rel == "corrects"
        and subj.startswith("agent:")
        and subj[len("agent:") :] in ("a", "b")
    ):
        m = re.fullmatch(r"row3:door mine=c([1-4]) other=c([1-4])", obj)
        if m:
            return ClaimSpec(
                "correct",
                sender,
                {
                    "target": subj[len("agent:") :],
                    "mine": m.group(1),
                    "other": m.group(2),
                },
            )
    return None


def render_sentence(claim: ClaimSpec) -> str:
    """The canonical (deterministic) rendering of a claim."""

    p = {**claim.parts}
    if claim.form == "cell":
        return f"{claim.sender} says: {p['cell']} is {p['value']}."
    if claim.form == "anchor":
        return f"{claim.sender} says: my door in row 3 is at column c{p['col']}."
    return f"{claim.sender} says: {p['target']}, your door reading is c{p['other']}, mine is c{p['mine']}."


def parse_sentence(text: str) -> ClaimSpec | None:
    """The deterministic parser: the only authority. A text matching
    none of the three frozen forms is ambiguous-for-the-surface and
    parses to None (drop — no rescue)."""

    text = (text or "").strip()
    m = _CELL_RE.match(text)
    if m:
        return ClaimSpec(
            "cell",
            m.group("sender"),
            {"cell": m.group("cell"), "value": m.group("value")},
        )
    m = _ANCHOR_RE.match(text)
    if m:
        return ClaimSpec("anchor", m.group("sender"), {"col": m.group("col")})
    m = _CORRECT_RE.match(text)
    if m and m.group("target") != m.group("sender"):
        return ClaimSpec(
            "correct",
            m.group("sender"),
            {
                "target": m.group("target"),
                "other": m.group("other"),
                "mine": m.group("mine"),
            },
        )
    return None


@runtime_checkable
class SurfaceRenderer(Protocol):
    """A message renderer: claim -> one sentence. The bounded retry is
    driven by the CODEC (it alone parses): `rerender` is called once
    with the failed text when the first render does not round-trip."""

    name: str

    def render(self, claim: ClaimSpec) -> str: ...

    def rerender(
        self, claim: ClaimSpec, failed_text: str
    ) -> str: ...  # pragma: no cover - protocol


class CanonicalRenderer:
    """The official (SKIP) arm renderer: the frozen forms verbatim."""

    name = "canonical"

    def render(self, claim: ClaimSpec) -> str:
        return render_sentence(claim)

    def rerender(self, claim: ClaimSpec, failed_text: str) -> str:
        return render_sentence(claim)


class LlmRenderer:
    """LLM-rendered natural-language messages (the M4 surface). The
    backend is the shared ``lang.llm.Backend`` seam (one surface, two
    consumers). The backend's own output is untrusted text: only the
    deterministic parser's round-trip admits it."""

    name: str

    def __init__(self, backend: Any, model: str) -> None:
        self._backend = backend
        self.model = model
        self.name = f"llm:{model}"

    def _user_prompt(self, claim: ClaimSpec) -> str:
        p = claim.parts
        if claim.form == "cell":
            spec = f"Form 1. Sender: {claim.sender}. Cell: {p['cell']}. Value: {p['value']}."
        elif claim.form == "anchor":
            spec = f"Form 2. Sender: {claim.sender}. Column: {p['col']}."
        else:
            spec = f"Form 3. Sender: {claim.sender}. Other: {p['target']}. Their reading: c{p['other']}. My reading: c{p['mine']}."
        return spec

    def _complete(self, claim: ClaimSpec, extra: str | None) -> str:
        messages = [
            {"role": "system", "content": LLM_SYSTEM_PROMPT},
            {"role": "user", "content": self._user_prompt(claim) + (extra or "")},
        ]
        return self._backend.complete(messages).strip()

    def render(self, claim: ClaimSpec) -> str:
        return self._complete(claim, None)

    def rerender(self, claim: ClaimSpec, failed_text: str) -> str:
        return self._complete(
            claim,
            f"\n\nYour last sentence was not machine-legible:\n{failed_text}\nRewrite it in exactly one of the three forms.",
        )


class ScriptedDropRenderer:
    """The frozen X3 perturbation: canonical except a designated
    (sender, form) renders an unparseable sentence (the honest-drop
    probe)."""

    name = "scripted-drop"

    def __init__(self, drop: tuple[str, str] | None = None) -> None:
        self.drop = drop

    def render(self, claim: ClaimSpec) -> str:
        if self.drop is not None and (claim.sender, claim.form) == self.drop:
            return f"{claim.sender} says: the door one, is, r3 column {claim.parts.get('col', claim.parts.get('cell', '?'))} i think"
        return render_sentence(claim)

    def rerender(self, claim: ClaimSpec, failed_text: str) -> str:
        return (
            render_sentence(claim)
            if self.drop is None or (claim.sender, claim.form) != self.drop
            else f"{claim.sender} says: um, the door at {claim.parts.get('col', '?')}, roughly"
        )


def _reconstruct(original: AssertionDelta, claim: ClaimSpec) -> AssertionDelta | None:
    """Round-trip integrity: the parsed claim must denote EXACTLY the
    claim the delta makes (subject/relation/object triple equal) — the
    delta itself is then the reconstructed message. A text that parses
    to anything else denotes a different claim than the one sent
    (corrupted channel = drop, never a silent acceptance; invariant #6).
    The delta's own id is the deterministic fingerprint of that triple
    under its scope, so triple equality implies id equality."""

    a = original.assertion
    if (claim.subject(), claim.relation(), claim.object_id()) != (
        a.subject.id,
        a.relation.id,
        a.object_id,
    ):
        return None
    return original


class SurfaceCodec:
    """The codec a Game can carry: render each delta's claim, parse it
    back, reconstruct (or drop + log), hand the surviving deltas to
    the channel. The per-entry audit log goes on the transcript entry
    (the report's `surface` blocks — the only added machine content,
    see E5.4 X2)."""

    def __init__(self, renderer: SurfaceRenderer) -> None:
        self.renderer = renderer
        self.name = renderer.name

    def pass_deltas(
        self, deltas: tuple[AssertionDelta, ...]
    ) -> tuple[tuple[AssertionDelta, ...], list[dict[str, Any]]]:
        out: list[AssertionDelta] = []
        log: list[dict[str, Any]] = []
        for d in deltas:
            claim = claim_from_delta(d)
            if claim is None:
                out.append(
                    d
                )  # not a surface claim: structured sideband path (never said in NL)
                log.append(
                    {
                        "subject": d.assertion.subject.id,
                        "text": None,
                        "status": "structured",
                        "reason": "not a surface-grammar claim",
                    }
                )
                continue
            text = self.renderer.render(claim)
            parsed = parse_sentence(text)
            if parsed is None:  # one bounded retry (E3.1 discipline: no rescue loops)
                text = self.renderer.rerender(claim, text)
                parsed = parse_sentence(text)
            if parsed is None:
                log.append(
                    {
                        "subject": d.assertion.subject.id,
                        "text": text,
                        "status": "dropped",
                        "reason": "render did not round-trip through the deterministic parser (one bounded retry used; never rescued)",
                    }
                )
                continue
            rebuilt = _reconstruct(d, parsed)
            if rebuilt is None:
                log.append(
                    {
                        "subject": d.assertion.subject.id,
                        "text": text,
                        "status": "dropped",
                        "reason": "round-trip denotes a different claim than the one sent (id mismatch) — corrupted channel, not accepted",
                    }
                )
                continue
            out.append(rebuilt)
            log.append(
                {
                    "subject": d.assertion.subject.id,
                    "text": text,
                    "status": "delivered",
                    "reason": None,
                }
            )
        return tuple(out), log
