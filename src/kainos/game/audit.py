"""T5 — the ToM store-audit harness (the white-box belief probe).

Black-box agent studies can only guess whether an agent models its
partner; ours can READ THE STORE. Per the multi-agent spec, every game
report embeds, per agent:

- **formation**: how many assertions the agent holds ABOUT the other
  agent(s) (the belief convention in :mod:`kainos.game.agent`: subject
  ``agent:<other>``, relation ``believes``);
- **correctness**: of those, how many agree with the game's ground
  truth (the audit is white-box: it sees the full state). A belief of
  the form ``fact:<id>=<value>`` is correct iff the world says so.
  (Scope note, recorded in the spec: T1 audits FIRST-ORDER beliefs —
  facts the agent attributes to the other's speech. Beliefs about the
  other's *beliefs* get their dedicated probe in E5.1's false-belief
  arm.)
- **support** (no unbacked mind-reading): a belief about agent X is
  SUPPORTED iff its ``provenance.source.uri`` is ``"agent:<X>"``
  (learned from X) or ``"agent:<self>"`` with ``provenance.evidence``
  citing at least one assertion sourced ``"agent:<X>"``. Anything else
  is a violation — a guess about another mind.
- **dispute discipline** (A5 at the social scale, store-wide): when the
  other agent's talk contradicts itself (or the world model), both sides
  must survive in the store as ``disputed``, cross-linked in
  ``provenance.evidence`` — never averaged, never overwritten.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.models import Assertion, EpistemicState
from kainos.game.agent import Agent, fact_value
from kainos.game.spec import GameSpec

__all__ = ["AuditReport", "beliefs_about", "tom_audit"]


def beliefs_about(store: InMemoryCodexStore, self_id: str) -> list[Assertion]:
    """All of the agent's assertions about OTHER agents (the audited set)."""

    out: list[Assertion] = []
    for a in store.query():
        if a.subject.id.startswith("agent:") and a.subject.id != f"agent:{self_id}":
            out.append(a)
    return out


def _belief_fact(a: Assertion) -> tuple[str, str] | None:
    """Parse ``fact:<id>=<value>`` objects; None for other shapes."""

    obj = a.object_id
    if not obj.startswith("fact:") or "=" not in obj:
        return None
    fid, _, value = obj[len("fact:") :].partition("=")
    return fid, value


def _supported(a: Assertion, self_id: str, all_assertions: list[Assertion]) -> bool:
    assert a.provenance is not None and a.provenance.source is not None  # invariant #1
    other = a.subject.id[len("agent:") :]
    if a.provenance.source.uri == f"agent:{other}":
        return True
    if a.provenance.source.uri == f"agent:{self_id}":
        cited = {
            x.provenance.source.uri for x in all_assertions if x.provenance and x.provenance.source and x.id in a.provenance.evidence
        }
        return f"agent:{other}" in cited
    return False


@dataclass
class AuditReport:
    agent: str
    n_about_other: int = 0
    n_correct: int = 0
    n_supported: int = 0
    n_disputes_preserved: int = 0
    violations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "agent": self.agent,
            "n_about_other": self.n_about_other,
            "n_correct": self.n_correct,
            "n_supported": self.n_supported,
            "correctness": (self.n_correct / self.n_about_other) if self.n_about_other else None,
            "support": (self.n_supported / self.n_about_other) if self.n_about_other else None,
            "n_disputes_preserved": self.n_disputes_preserved,
            "violations": list(self.violations),
        }


def tom_audit(agent: Agent, spec: GameSpec) -> AuditReport:
    """The white-box audit of one agent's store, against ground truth."""

    store = agent.codex
    all_assertions = store.query()
    about = beliefs_about(store, agent.player_id)
    rep = AuditReport(agent=agent.player_id, n_about_other=len(about))

    for a in about:
        # correctness (first-order: fact beliefs vs the world)
        parsed = _belief_fact(a)
        if parsed is not None:
            fid, raw = parsed
            value = fact_value(raw)
            if value is None:
                value = raw
            if fid in spec.state and spec.state[fid] == value:
                rep.n_correct += 1
        # support (no unbacked mind-reading)
        if _supported(a, agent.player_id, all_assertions):
            rep.n_supported += 1
        else:
            rep.violations.append(
                f"unbacked belief {a.id} (subject {a.subject.id}, object {a.object_id}): "
                f"provenance {a.provenance.source.uri if a.provenance and a.provenance.source else None!r} "
                "cites no supported evidence"
            )

    # dispute discipline (A5 at the social scale): EVERY disputed
    # assertion in the store — world-model facts AND mental-model beliefs —
    # must sit alongside its conflicting sibling (both present, both
    # disputed; never averaged, never overwritten).
    for a in all_assertions:
        if a.status == EpistemicState.disputed:
            siblings = store.query(subject=a.subject.id, relation=a.relation.id)
            if any(
                s.id != a.id
                and s.object_id != a.object_id
                and s.status == EpistemicState.disputed
                and bool(s.provenance is not None and s.provenance.evidence and a.id in s.provenance.evidence or a.provenance is not None and a.provenance.evidence and s.id in a.provenance.evidence)
                for s in siblings
            ):
                rep.n_disputes_preserved += 1
            else:
                rep.violations.append(
                    f"disputed assertion {a.id} lost its sibling: the conflict was NOT preserved "
                    "(A5 discipline: both sides stay, cross-linked)"
                )
    return rep
