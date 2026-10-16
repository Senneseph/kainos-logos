"""T1 game kernel — the scheduler: a deterministic round driver.

Round semantics (fixed, seeded, synchronous):

    for each round:  channel.new_round()
        for each player in turn order:
            inbox <- channel.take_inbox(player); agent.merge_inbox(round)
            action, rejection = agent.act_on(round, transcript)
            execute: Say -> channel.deliver (budget+corruption),
                     Reveal -> broadcast fact deltas (same channel),
                     Commit -> recorded (last wins), Pass -> recorded
            view-isolation invariant re-checked EVERY turn
            (recorded in the report: a "leaky view" fails the suite,
             E3.7 style)

Messages delivered during a player's turn arrive in its INBOX and are
merged at that player's next turn — so an EARLIER actor's same-round
speech is visible to a later actor within the same round, while the
first actor of the turn order sees the previous round's tail. All of
it is fully deterministic given the spec (no wall clock, seeded
channel), and the transcript records every delivery. Everything derives from
``(spec, policies, seed)`` — two runs of the same game are
bit-identical (the determinism hash in the report proves it).
"""

from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kainos.exchange.protocol import AssertionDelta
from kainos.game.actions import Action, Commit, Correct, Pass, Reveal, Say
from kainos.game.agent import VALUE_KEY, Agent, fact_delta_for
from kainos.game.audit import tom_audit
from kainos.game.channel import Channel
from kainos.game.spec import GameSpec
from kainos.game.surface import SurfaceCodec

__all__ = ["Game", "ScorerFn"]


def _deltas_view(deltas: tuple[AssertionDelta, ...]) -> list[dict[str, Any]]:
    out = []
    for d in deltas:
        a = d.assertion
        out.append(
            {
                "id": a.id,
                "subject": a.subject.id,
                "relation": a.relation.id,
                "object": a.object_id,
                "source": a.provenance.source.uri
                if a.provenance and a.provenance.source
                else None,
                "timestamp": d.timestamp,
            }
        )
    return out


def _serialize_action(action: Action) -> dict[str, Any]:
    if isinstance(action, Say):
        return {
            "kind": "say",
            "receiver": action.receiver,
            "deltas": _deltas_view(action.deltas),
        }
    if isinstance(action, Reveal):
        return {"kind": "reveal", "fact_ids": list(action.fact_ids)}
    if isinstance(action, Correct):
        return {
            "kind": "correct",
            "target": action.target,
            "fact_id": action.fact_id,
            "deltas": _deltas_view(action.deltas),
        }
    if isinstance(action, Commit):
        return {"kind": "commit", "payload": dict(action.payload)}
    if isinstance(action, Pass):
        return {"kind": "pass"}
    raise TypeError(f"unknown action {action!r}")


@dataclass
class Game:
    """A concrete game: spec + agents + seed. ``run`` is pure in its
    inputs apart from the (optionally requested) report file write."""

    spec: GameSpec
    agents: dict[str, Agent]
    seed: int
    scorer: ScorerFn | None = None
    #: E5.4 (T6 #166, M4 stretch): the message-surface codec. None = the
    #: structured arm (bit-identical to the pre-E5.4 kernel); a codec
    #: renders each Say/Correct delta's claim as a sentence and the
    #: deterministic parser must round-trip it before delivery.
    surface: SurfaceCodec | None = None

    def _make_scorer(self) -> ScorerFn:
        if self.scorer is not None:
            return self.scorer

        def default(commits: dict[str, dict[str, Any]], game: Game) -> dict[str, Any]:
            return {"n_commits": len(commits)}

        return default

    def run(
        self, write: bool = True, out_dir: Path | str | None = None
    ) -> dict[str, Any]:
        rng = random.Random(self.seed)
        # corruption operates on raw object strings; the kernel hands it the
        # property-form values so a corrupted fact stays well-formed
        values = tuple(
            sorted(f"{VALUE_KEY}={v}" for v in dict.fromkeys(self.spec.state.values()))
        )
        channel = Channel(
            self.spec.players,
            self.spec.channel.budget_per_round,
            self.spec.channel.corruption,
            rng,
            values,
        )
        transcript: list[dict[str, Any]] = []
        commits: dict[str, dict[str, Any]] = {}
        leaks = 0
        checked_turns = 0
        bad_receiver_events: list[dict[str, Any]] = []

        for round_no in range(1, self.spec.rounds + 1):
            channel.new_round()
            for order, player in enumerate(self.spec.turn()):
                agent = self.agents[player]
                agent.set_inbox(channel.take_inbox(player))
                agent.merge_inbox(round_no)
                action, rejection = agent.act_on(round_no, transcript)

                # structural view-isolation invariant, re-checked every turn
                view = agent.perceive()
                allowed = self.spec.views[player]
                if any(f not in allowed for f in view):
                    leaks += 1
                checked_turns += 1

                entry: dict[str, Any] = {
                    "round": round_no,
                    "actor": player,
                    "action": _serialize_action(action),
                }
                if rejection is not None:
                    entry["rejection"] = {
                        "action": rejection.action,
                        "reason": rejection.reason,
                    }

                if isinstance(action, Say):
                    if (
                        action.receiver != "shared"
                        and action.receiver not in self.spec.players
                    ):
                        bad_receiver_events.append(
                            {
                                "round": round_no,
                                "actor": player,
                                "receiver": action.receiver,
                            }
                        )
                        entry["delivered"] = False
                        entry["error"] = (
                            f"unknown receiver {action.receiver!r} (shared or a player id required)"
                        )
                    elif self.surface is not None:
                        spoken, surface_log = self.surface.pass_deltas(action.deltas)
                        entry["surface"] = {
                            "renderer": self.surface.name,
                            "deltas": surface_log,
                        }
                        entry["delivered"] = channel.deliver(
                            round_no, player, action.receiver, spoken
                        )
                    else:
                        entry["delivered"] = channel.deliver(
                            round_no, player, action.receiver, action.deltas
                        )
                elif isinstance(action, Correct):
                    if self.surface is not None:
                        spoken, surface_log = self.surface.pass_deltas(action.deltas)
                        entry["surface"] = {
                            "renderer": self.surface.name,
                            "deltas": surface_log,
                        }
                        entry["delivered"] = channel.deliver(
                            round_no, player, action.target, spoken
                        )
                    else:
                        entry["delivered"] = channel.deliver(
                            round_no, player, action.target, action.deltas
                        )
                elif isinstance(action, Reveal):
                    deltas = tuple(
                        fact_delta_for(
                            "reveal",
                            player,
                            fid,
                            self.spec.state[fid],
                            round_no,
                            order,
                            self.spec.name,
                        )
                        for fid in action.fact_ids
                    )
                    entry["delivered"] = channel.deliver(
                        round_no, player, "shared", deltas
                    )
                elif isinstance(action, Commit):
                    commits[player] = dict(action.payload)

                transcript.append(entry)

        scores = self._make_scorer()(commits, self)

        audit = {
            p: tom_audit(self.agents[p], self.spec).to_dict() for p in self.spec.players
        }

        report: dict[str, Any] = {
            "game": self.spec.name,
            "seed": self.seed,
            "rounds": self.spec.rounds,
            "players": list(self.spec.players),
            "channel": {
                "budget_per_round": self.spec.channel.budget_per_round,
                "corruption_probability": self.spec.channel.corruption,
                "sent_totals": channel.sent_totals(),
                "events": [e.__dict__ for e in channel.events],
                "bad_receivers": bad_receiver_events,
            },
            "agents": {
                p: {
                    "capabilities": sorted(a.capabilities),
                    "policy_note": a.policy_note,
                    "rejections": [r.__dict__ for r in a.rejections],
                    "observe_reports": a.observe_reports,
                    "codex_assertions": len(a.codex.query()),
                }
                for p, a in self.agents.items()
            },
            "commits": commits,
            "scores": scores,
            "audit": audit,
            "negative_control": {"view_leaks": leaks, "checked_turns": checked_turns},
            "transcript": transcript,
        }
        canonical = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False)
        report["determinism_hash"] = (
            "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        )

        if write:
            out = default_out_dir(out_dir)
            (out / "phase-5").mkdir(parents=True, exist_ok=True)
            (out / "phase-5" / f"{self.spec.name}.json").write_text(
                json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        return report


def default_out_dir(out_dir: Path | str | None) -> Path:
    """Result root per the results-hygiene rule (KAINOS_RESULTS_DIR)."""

    from kainos.harness.paths import default_results_dir

    return Path(out_dir) if out_dir is not None else default_results_dir()


#: ScorerFn: (final commits, game) -> scores block (pure, deterministic).
ScorerFn = Callable[[dict[str, dict[str, Any]], Game], dict[str, Any]]
