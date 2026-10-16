"""T1 game kernel — the agent.

Each agent is an instance of the STACK, not a black box (the white-box
property everything in the multi-agent spec measures against):

- Its world model is an ``InMemoryCodexStore``; incoming messages are
  step-19 assertion deltas merged through ``merge`` (idempotent,
  conflict-preserving, never averaging — A5 at the social scale).
- VIEW ISOLATION: the only path from world facts to the agent is
  ``spec.views[player]``; :meth:`perceive` is the single read surface
  and the agent object exposes no other access to ``spec.state``.
  A "leaky view" is a bug with a failing test, not an assumption.
- SPEECH IS ATTRIBUTED: only assertions sourced ``"agent:<self>"`` may
  leave an agent (kernel-enforced — the channel cannot carry unattributed
  claims).
- BELIEF CONVENTION (what the T5 audit checks): beliefs about another
  agent are stored as assertions with ``subject.id = "agent:<other>"``,
  ``relation.id = "believes"`` and ``object = "fact:<id>=<value>"``.
  Support rule: such an assertion is SUPPORTED iff its
  ``provenance.source.uri`` is ``"agent:<other>"`` (learned from that
  agent) or ``"agent:<self>"`` with ``provenance.evidence`` citing at
  least one assertion sourced ``"agent:<other>"``. Anything else is
  *unbacked mind-reading* — the audit flags it.
- Capability gating: an action requiring an undeclared capability is
  rejected with a NAMED GAP and never executed (E3.6 honesty contract).

Action flow: the policy ``StepFn`` returns an :class:`Action`; the
scheduler validates it against this agent (validation errors surface as
named-gap rejections, not crashes) and executes it.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, Context, Provenance, Source, TermRef
from kainos.exchange.protocol import AssertionDelta, MergeReport, merge
from kainos.game.actions import (
    ALL_CAPABILITIES,
    Action,
    Correct,
    Pass,
    Reveal,
    Say,
    capability_for,
)
from kainos.game.spec import GameSpec

__all__ = [
    "VALUE_KEY",
    "Agent",
    "Rejection",
    "StepFn",
    "belief_assertion",
    "deterministic_id",
    "fact_delta_for",
    "fact_value",
    "game_ts",
]

#: StepFn: policy function — (visible facts, round_no, transcript) -> Action.
StepFn = Callable[[dict[str, str], int, list[dict[str, Any]]], Action]


def deterministic_id(scope: str, sender: str, subject: str, relation: str, obj: str, polarity: bool = True) -> str:
    """Stable assertion id: an identical claim by the same sender gets
    the same id (idempotent re-delivery is a no-op); a different claim on
    the same aspect gets a different id (a conflict, preserved by merge)."""

    h = hashlib.sha256(f"{scope}|{sender}|{subject}|{relation}|{obj}|{int(polarity)}".encode()).hexdigest()[:16]
    return f"game:{scope}:{sender}:{h}"


#: Deterministic game timestamps (D-m5 discipline: reproducible, no wall clock).
def game_ts(round_no: int, order: int = 0) -> str:
    minutes = round_no * 10 + order
    return f"2026-01-01T{minutes // 60:02d}:{minutes % 60:02d}:00+00:00"


#: Game facts ride the CODEX **property form** (string object
#: ``"value=<v>"``) so the step-19 conflict semantics apply verbatim:
#: same subject + relation, aspect ``value``, different full value ⇒
#: disputed pair — never averaged, never overwritten (invariant #6).
VALUE_KEY = "value"


def fact_delta_for(scope: str, sender: str, fact_id: str, value: str, round_no: int, order: int, game: str) -> AssertionDelta:
    """The standard delta for asserting a world fact (say/reveal)."""

    a = Assertion(
        id=deterministic_id(scope, sender, f"fact:{fact_id}", "is", value),
        subject=TermRef(id=f"fact:{fact_id}", kind="fact"),
        relation=TermRef(id="is", kind="relation"),
        object=f"{VALUE_KEY}={value}",
        context=Context(data={"game": game, "round": round_no, "kind": scope}),
        provenance=Provenance(
            source=Source(uri=f"agent:{sender}", authority="game-channel"),
            observer=sender,
        ),
    )
    return AssertionDelta(assertion=a, node_id=sender, timestamp=game_ts(round_no, order))


def fact_value(object_id: str) -> str | None:
    """Decode a property-form fact object (``value=<v>``); None otherwise."""

    if isinstance(object_id, str) and object_id.startswith(f"{VALUE_KEY}="):
        return object_id[len(f"{VALUE_KEY}=") :]
    return None


def belief_assertion(
    self_id: str,
    other: str,
    fact_id: str,
    value: str,
    source_uri: str,
    evidence: tuple[str, ...] = (),
) -> Assertion:
    """The standard shape of a belief assertion about another agent
    (subject ``agent:<other>``, relation ``believes``)."""

    return Assertion(
        id=deterministic_id("belief", self_id, f"agent:{other}", "believes", f"fact:{fact_id}={value}"),
        subject=TermRef(id=f"agent:{other}", kind="agent"),
        relation=TermRef(id="believes", kind="relation"),
        object=f"fact:{fact_id}={value}",
        provenance=Provenance(
            source=Source(uri=source_uri, authority="game-channel"),
            observer=self_id,
            evidence=list(evidence),
        ),
    )


@dataclass(frozen=True)
class Rejection:
    """A named-gap rejection (capability or action validation)."""

    round_no: int
    actor: str
    action: str
    reason: str


class Agent:
    """One player in a game: CODEX world model + inbox + policy + caps."""

    def __init__(
        self,
        player_id: str,
        spec: GameSpec,
        step: StepFn,
        capabilities: frozenset[str] = ALL_CAPABILITIES,
        codex: InMemoryCodexStore | None = None,
        policy_note: str = "scripted",
    ) -> None:
        self.player_id = player_id
        self._spec = spec
        self._step = step
        self._capabilities = capabilities
        self._codex = codex if codex is not None else InMemoryCodexStore()
        self._policy_note = policy_note
        self._inbox: list[AssertionDelta] = []
        self.rejections: list[Rejection] = []
        self.observe_reports: list[dict[str, Any]] = []

    # ── the single read surface (structural view isolation) ─────────────

    def perceive(self) -> dict[str, str]:
        """The visible slice of world facts — and NOTHING else. This is
        the only method that reads ``spec.state``. Declared
        perception overrides (episode data, e.g. the planted-wrong
        shared layer) apply strictly WITHIN the visible slice: scope
        is never a perception issue."""

        visible = self._spec.views[self.player_id]
        overrides = self._spec.perception_overrides.get(self.player_id, {})
        return {f: overrides.get(f, v) for f, v in sorted(self._spec.state.items()) if f in visible}

    # ── communication ────────────────────────────────────────────────────

    def set_inbox(self, deltas: list[AssertionDelta]) -> None:
        """Scheduler-only: hand over the round's delivered messages."""

        self._inbox.extend(deltas)

    def merge_inbox(self, round_no: int) -> MergeReport:
        """Drain the inbox and merge through step-19 semantics:
        idempotent, conflict-preserving (disputed, cross-linked evidence),
        never averaging. Per-round report is kept for the transcript."""

        report = merge(self._codex, self._inbox) if self._inbox else MergeReport()
        self._inbox = []
        self.observe_reports.append(
            {
                "round": round_no,
                "merged": len(report.merged),
                "duplicates": len(report.duplicates),
                "conflicts_preserved": report.conflicts_preserved,
                "disputed_pairs": len(report.disputed),
            }
        )
        return report

    # ── action policy + gating ───────────────────────────────────────────

    def act_on(self, round_no: int, transcript: list[dict[str, Any]]) -> tuple[Action, Rejection | None]:
        """Run the policy on the visible slice; capability-gate the
        result. Returns (action, rejection|None): on rejection the action
        is a Pass and the rejection carries the NAMED GAP reason."""

        view = self.perceive()
        action = self._step(view, round_no, transcript)
        needed = capability_for(action)
        if needed not in self._capabilities:
            rej = Rejection(
                round_no,
                self.player_id,
                type(action).__name__,
                f"capability {needed!r} is not declared — action not executed (named gap, never guessed)",
            )
            self.rejections.append(rej)
            return Pass(), rej

        if isinstance(action, Say):
            err = self._validate_speech(action.deltas)
            if err is not None:
                rej = Rejection(round_no, self.player_id, "Say", err)
                self.rejections.append(rej)
                return Pass(), rej
        elif isinstance(action, Correct):
            if action.target == self.player_id:
                rej = Rejection(
                    round_no,
                    self.player_id,
                    "Correct",
                    "an agent cannot correct itself (the assertion is ABOUT the other)",
                )
                self.rejections.append(rej)
                return Pass(), rej
            if action.target not in self._spec.players:
                rej = Rejection(round_no, self.player_id, "Correct", f"unknown correction target {action.target!r}")
                self.rejections.append(rej)
                return Pass(), rej
            err = self._validate_speech(action.deltas)
            if err is not None:
                rej = Rejection(round_no, self.player_id, "Correct", err)
                self.rejections.append(rej)
                return Pass(), rej
        elif isinstance(action, Reveal):
            priv = self._spec.private_view(self.player_id)
            bad = [f for f in action.fact_ids if f not in priv]
            if bad:
                rej = Rejection(
                    round_no,
                    self.player_id,
                    "Reveal",
                    f"cannot reveal non-private facts {bad} (only the agent's private layer is shareable)",
                )
                self.rejections.append(rej)
                return Pass(), rej
        return action, None

    def _validate_speech(self, deltas: tuple) -> str | None:
        """Speech is attributed: node id + source uri must be the agent
        itself (the kernel enforces this, it does not trust it)."""

        for d in deltas:
            if d.node_id != self.player_id:
                return f"delta claims node {d.node_id!r}, not {self.player_id!r}"
            a = d.assertion
            if a.provenance is None or a.provenance.source is None:  # invariant #1
                return "a delta left provenance-less (invariant #1: no bare edges)"
            if a.provenance.source.uri != f"agent:{self.player_id}":
                return f"delta sourced {a.provenance.source.uri!r}; only self-sourced speech is admitted"
            if a.provenance.observer != self.player_id:
                return "delta observer is not the speaking agent"
        return None

    def remember(self, assertion: Assertion) -> str:
        """Store a SELF-DERIVED candidate assertion (own inference). The
        belief support rule (module docstring) governs beliefs about
        others; source must be self."""

        if assertion.provenance is None or assertion.provenance.source is None:
            raise ValueError("Assertion.provenance.source is mandatory (invariant #1)")
        if assertion.provenance.source.uri != f"agent:{self.player_id}":
            raise ValueError("an agent may only store self-sourced inferences directly")
        return self._codex.add(assertion)

    # ── inspection (the white-box surface the audit layer reads) ────────

    @property
    def codex(self) -> InMemoryCodexStore:
        return self._codex

    @property
    def capabilities(self) -> frozenset[str]:
        return self._capabilities

    @property
    def policy_note(self) -> str:
        return self._policy_note
