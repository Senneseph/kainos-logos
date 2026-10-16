"""E5.1 — "The Shared Grid" (T2, #162): cooperative ToM + the embedded
false-belief (Sally-Anne) probe.

Pre-registration (frozen; D-e5a amended pre-run):
``plan/30-phases/phase-5-multi-agent/experiments.md``. Major spec:
``plan/10-architecture/multi-agent-games.md`` — E5.1.

What this file is: the game as DATA (grid, episodes, views, protocol,
ablation capability sets) + the per-variant policies + the pure scorer
(redundancy to the computable minimum, detection latency, recovery) +
the 12 acceptance checks. The kernel (T1) and the ToM audit (T5) are
reused verbatim — including the structural view-isolation negative
control and the step-19 merge's dispute preservation.

The probe in one paragraph: in the false-belief episode A perceives a
planted-wrong shared row (its door anchor differs from the world). B's
anchor (round 3) reports B's perception. Only an agent that MODELS WHAT
B BELIEVES interprets the anchor as "B sees the door elsewhere", forms
the belief, and — in round 4 — emits the explicit ``Correct`` assertion
("your row 3 is wrong"). ``Correct`` requires the ``assert_about_other``
capability, which the ToM ablation (V0) lacks: the kernel rejects a
forced V0 attempt with a NAMED GAP, so V0 is structurally incapable of
the probe assertion, not merely unwilling. Round 6 resolves the shared
row by the door-corridor coherence rule (D-e5a-amended): the planted
door's corridor is blocked in the world (a generator guarantee), the
true one is open — so V1/V2 both end on the correct grid; V0 commits
its planted perception and fails by exactly the two planted cells.

Policy discipline (honesty note): policies read knowledge ONLY from
their own ``perceive()`` slice and their own CODEX store (merged
inbox). The transcript is used solely as PROTOCOL CONTROL (was a
mismatch flagged in this episode?) — it is a game-level record, and the
delivery of private speech still rides the channel's inbox. The kernel
never exposes one agent's inbox to the other.
"""

from __future__ import annotations

import json
import random
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

from kainos.codex.models import Assertion, Context, Provenance, Source, TermRef
from kainos.exchange.protocol import AssertionDelta, merge
from kainos.game.actions import Action, Commit, Correct, Pass, Say
from kainos.game.agent import Agent, belief_assertion, deterministic_id
from kainos.game.scheduler import Game
from kainos.game.spec import ChannelSpec, GameSpec

__all__ = ["CAPS", "E5_1Experiment", "build_game", "gen_grid", "make_episode", "run_e5_1", "score_run"]

ROWS, COLS = 5, 4
CELLS = tuple(f"r{r}c{c}" for r in range(1, ROWS + 1) for c in range(1, COLS + 1))
ROW3_CELLS = tuple(f"r3c{c}" for c in range(1, COLS + 1))
DOOR_FACT = "row3:door"
SEED = 5101
GAMERUN_SEED = 5101

CHECKS = 12

#: Ablation capability sets (P11: capabilities ARE store data — the
#: ablation is a data choice, a one-line store op).
CAPS = {
    "V0": frozenset({"pass", "commit", "send_message"}),
    "V2": frozenset({"pass", "commit", "send_message", "model_other_beliefs", "assert_about_other"}),
    "V1": frozenset({"pass", "commit", "send_message", "model_other_beliefs", "assert_about_other", "model_other_state"}),
}


# ── grid + episodes ──────────────────────────────────────────────────────


def gen_grid(seed: int) -> tuple[dict[str, str], int]:
    """Seeded 5×4 grid: exactly one key (rows 1–2), one goal (rows 4–5),
    one door (row 3); the corridor directly above and below the TRUE
    door is empty (the world is physically consistent); walls land on
    30% of the remaining free cells. Returns (grid, true_door_col)."""

    rng = random.Random(seed)
    grid = {c: "empty" for c in CELLS}
    door_col = rng.choice(range(1, COLS + 1))
    grid[f"r3c{door_col}"] = "door"
    corridor = {f"r2c{door_col}", f"r4c{door_col}"}
    # key/goal placement is protected from the corridor so the physical
    # consistency guarantee (gen rule) actually holds
    key_candidates = [f"r{r}c{c}" for r in (1, 2) for c in range(1, COLS + 1) if f"r{r}c{c}" not in corridor]
    goal_candidates = [f"r{r}c{c}" for r in (4, 5) for c in range(1, COLS + 1) if f"r{r}c{c}" not in corridor]
    grid[rng.choice(key_candidates)] = "key"
    grid[rng.choice(goal_candidates)] = "goal"
    for c in CELLS:
        if grid[c] == "empty" and c not in corridor and rng.random() < 0.30:
            grid[c] = "wall"
    return grid, door_col


def planted_row3(grid: dict[str, str], true_col: int) -> tuple[dict[str, str], int]:
    """The planted row 3 that agent A perceives: the door moves to the
    NEXT column (wrapping; deterministic, != the true column) and the
    vacated cell becomes empty — exactly two cells differ from truth."""

    planted_col = true_col % COLS + 1
    row = {f"r3c{c}": grid[f"r3c{c}"] for c in range(1, COLS + 1)}
    row[f"r3c{planted_col}"] = "door"
    row[f"r3c{true_col}"] = "empty"
    return row, planted_col


def make_episode(episode: str) -> dict[str, Any]:
    """Episode = game spec + metadata. `clean`: both agents perceive the
    true shared row. `false`: A perceives the planted row 3 (declared
    as a perception override — scope is never a perception issue); the
    generator then GUARANTEES the planted door's corridor contains a
    wall (D-e5a-amended generation rule) while the true corridor stays
    open."""

    grid, true_col = gen_grid(SEED)
    overrides: dict[str, dict[str, str]] = {}
    planted_col: int | None = None
    if episode == "false":
        row_w, planted_col = planted_row3(grid, true_col)
        if grid[f"r2c{planted_col}"] != "wall" and grid[f"r4c{planted_col}"] != "wall":
            grid = dict(grid, **{f"r4c{planted_col}": "wall"})
        overrides = {"a": dict(row_w)}
    views = {
        "a": frozenset(f"r{r}c{c}" for r in (1, 2, 3) for c in range(1, COLS + 1)),
        "b": frozenset(f"r{r}c{c}" for r in (3, 4, 5) for c in range(1, COLS + 1)),
    }
    state = dict(grid)
    state[DOOR_FACT] = f"c{true_col}"  # ambient derived fact (in no view)
    spec = GameSpec(
        f"e5.1-{episode}",
        ("a", "b"),
        state,
        views,
        ChannelSpec(budget_per_round=4, corruption=0.0),
        rounds=6,
        perception_overrides=overrides,
    )
    return {"spec": spec, "truth": grid, "true_col": true_col, "planted_col": planted_col}


# ── deltas (step-19 AssertionDeltas, the message medium) ─────────────────


def _ts(round_no: int, order: int) -> str:
    return f"2026-02-{round_no + 10:02d}T00:{order:02d}:00+00:00"


def cell_delta(player: str, subject: str, value: str, round_no: int, order: int, game: str, kind: str) -> AssertionDelta:
    """A cell/anchor/row3 assertion (property form, per D-m9)."""

    a = Assertion(
        id=deterministic_id(kind, player, subject, "is", value),
        subject=TermRef(id=subject, kind="fact"),
        relation=TermRef(id="is", kind="relation"),
        object=f"value={value}",
        context=Context(data={"game": game, "round": round_no, "kind": kind}),
        provenance=Provenance(source=Source(uri=f"agent:{player}", authority="game-channel"), observer=player),
    )
    return AssertionDelta(assertion=a, node_id=player, timestamp=_ts(round_no, order))


def correct_delta(player: str, target: str, mine: str, other: str, round_no: int, game: str, evidence: tuple[str, ...]) -> AssertionDelta:
    """The signature probe assertion (ABOUT the other agent's model)."""

    obj = f"{DOOR_FACT} mine={mine} other={other}"
    a = Assertion(
        id=deterministic_id("correct", player, f"agent:{target}", "corrects", obj),
        subject=TermRef(id=f"agent:{target}", kind="agent"),
        relation=TermRef(id="corrects", kind="relation"),
        object=obj,
        provenance=Provenance(
            source=Source(uri=f"agent:{player}", authority="game-channel"),
            observer=player,
            evidence=list(evidence),
        ),
    )
    return AssertionDelta(assertion=a, node_id=player, timestamp=_ts(round_no, 1))


# ── policies (variant-aware; knowledge only from view + own store) ───────


def _door_col_in(view: dict[str, str]) -> int:
    for c in range(1, COLS + 1):
        if view[f"r3c{c}"] == "door":
            return c
    raise ValueError("no door in perceived row 3")


def _other_latest(store, subject: str, other: str) -> tuple[str, str] | None:
    """The other agent's latest stored claim about a subject.
    Returns (value, assertion_id) or None."""

    vals = [
        (a.object_id, a)
        for a in store.query(subject=subject)
        if a.provenance is not None and a.provenance.source is not None and a.provenance.source.uri == f"agent:{other}"
    ]
    if not vals:
        return None
    obj, a = vals[-1]
    return obj[len("value=") :], a.id


def _mismatch_flagged(transcript: list[dict[str, Any]], player: str) -> bool:
    """Protocol control (not world knowledge): was an explicit
    mismatch flagged in this episode — by me or addressed to me?"""

    return any(
        e["action"]["kind"] == "correct" and (e["actor"] == player or e["action"].get("target") == player)
        for e in transcript
    )


def make_policy(variant: str, player: str, ep: dict[str, Any], holders: dict[str, Agent]) -> Callable:
    other = "b" if player == "a" else "a"
    my_private_rows = (1, 2) if player == "a" else (4, 5)
    game = ep["spec"].name
    to_model = variant != "V0"

    rows = (1, 2, 3) if player == "a" else (3, 4, 5)
    naive_queue = [f"r{r}c{c}" for r in rows for c in range(1, COLS + 1)]
    sent: set[str] = set()

    def step(view: dict[str, str], round_no: int, transcript: list[dict[str, Any]]) -> Action:
        agent = holders[player]
        store = agent.codex

        # ── rounds 1–2: private exchange ───────────────────────────────
        if round_no in (1, 2):
            if to_model:
                row = my_private_rows[round_no - 1]
                cells = [f"r{row}c{c}" for c in range(1, COLS + 1)]
            else:
                cells = [c for c in naive_queue if c not in sent][:4]
                sent.update(cells)
                if not cells:
                    return Pass()
            return Say("shared", tuple(cell_delta(player, c, view[c], round_no, i, game, "cell") for i, c in enumerate(cells)))

        # ── round 3: alignment (anchor) + self-recording ──────────────
        if round_no == 3:
            my_anchor = f"c{_door_col_in(view)}"
            anchor_id = deterministic_id("anchor", player, DOOR_FACT, "is", my_anchor)
            try:
                store.get(anchor_id)
            except KeyError:
                # self-recording goes through merge (NOT a bare add): if
                # the other's anchor already disagrees, the pair must be
                # marked disputed, cross-linked, and preserved — the
                # step-19 invariant applies to own inferences too.
                self_delta = cell_delta(player, DOOR_FACT, my_anchor, 3, 0, game, "anchor-selfrec")
                merge(store, [self_delta])
            return Say("shared", (cell_delta(player, DOOR_FACT, my_anchor, 3, 0, game, "anchor"),))

        # ── round 4: mismatch response (the probe round) ───────────────
        if round_no == 4:
            if to_model:
                latest = _other_latest(store, DOOR_FACT, other)
                if latest is not None:
                    other_anchor, anchor_id = latest
                    belief = belief_assertion(player, other, DOOR_FACT, other_anchor, f"agent:{player}", (anchor_id,))
                    try:
                        store.get(belief.id)
                    except KeyError:
                        agent.remember(belief)
                    my_anchor = f"c{_door_col_in(view)}"
                    if other_anchor != my_anchor:
                        return Correct(
                            other,
                            DOOR_FACT,
                            (correct_delta(player, other, my_anchor, other_anchor, 4, game, (anchor_id,)),),
                        )
            return Pass()

        # ── round 5: re-confirmation (only after a flagged mismatch) ───
        if round_no == 5:
            if to_model:
                if _mismatch_flagged(transcript, player):
                    return Say(
                        "shared",
                        tuple(cell_delta(player, f"r3c{c}", view[f"r3c{c}"], 5, i, game, "row3") for i, c in enumerate(range(1, COLS + 1))),
                    )
                return Pass()
            # V0: its naive row-major queue keeps draining (the protocol
            # gives it as many sharing slots as the schedule has)
            cells = [c for c in naive_queue if c not in sent][:4]
            sent.update(cells)
            if not cells:
                return Pass()
            return Say("shared", tuple(cell_delta(player, c, view[c], 5, i, game, "cell") for i, c in enumerate(cells)))

        # ── round 6: commit the 20-cell reconstruction ─────────────────
        my_row3 = {f"r3c{c}": view[f"r3c{c}"] for c in range(1, COLS + 1)}
        row3 = my_row3
        if to_model and _mismatch_flagged(transcript, player):

            def corridor_known_empty(row3: dict[str, str]) -> bool:
                """The cell directly above AND below the row's door is
                known (view or other's stored claims) to be empty."""

                col = next(n for n in range(1, COLS + 1) if row3[f"r3c{n}"] == "door")
                out: list[str | None] = []
                for sub in (f"r2c{col}", f"r4c{col}"):
                    if sub in view:
                        out.append(view[sub])
                    else:
                        latest = _other_latest(store, sub, other)
                        out.append(latest[0] if latest else None)
                return out == ["empty", "empty"]

            other_row3: dict[str, str] = {}
            ok = True
            for n in range(1, COLS + 1):
                latest = _other_latest(store, f"r3c{n}", other)
                if latest is None:
                    ok = False
                    break
                other_row3[f"r3c{n}"] = latest[0]
            if corridor_known_empty(my_row3):
                row3 = my_row3
            elif ok and corridor_known_empty(other_row3):
                row3 = other_row3
            else:
                row3 = my_row3

        grid_out: dict[str, str] = {}
        for c, v in view.items():
            grid_out[c] = v
        for c in CELLS:
            if c in grid_out or c.startswith("r3c"):
                continue
            latest = _other_latest(store, c, other)
            if latest is not None:
                grid_out[c] = latest[0]
        for c, v in row3.items():
            grid_out[c] = v
        return Commit({"grid": grid_out})

    return step


# ── building a run ────────────────────────────────────────────────────────


def build_game(episode: str, variant: str) -> Game:
    import dataclasses

    ep = make_episode(episode)
    spec = dataclasses.replace(ep["spec"], name=f"e5.1-{episode}-{variant.lower()}")
    holders: dict[str, Agent] = {}

    def mk(player: str) -> Agent:
        p = make_policy(variant, player, ep, holders)
        a = Agent(player, spec, p, capabilities=CAPS[variant], policy_note=f"{variant} {episode}")
        holders[player] = a
        return a

    return Game(spec, {"a": mk("a"), "b": mk("b")}, seed=GAMERUN_SEED)


# ── the pure scorer ───────────────────────────────────────────────────────


def _perceptions(spec: GameSpec) -> dict[str, dict[str, str]]:
    """Each player's perceived slice (view + declared overrides)."""

    out = {}
    for p in spec.players:
        ov = spec.perception_overrides.get(p, {})
        out[p] = {f: ov.get(f, v) for f, v in spec.state.items() if f in spec.views[p]}
    return out


def score_run(report: dict[str, Any], spec: GameSpec) -> dict[str, Any]:
    """Recovery, redundancy (EXACT sent/lacked bit counts) and the first
    `Correct` record, computed from the self-hashed report + the spec.

    Redundancy (pre-registered, operationalized): a bit = one Say delta
    over a cell or the anchor fact. A bit the receiver ALREADY KNEW is
    redundant: the receiver perceives that subject with that value,
    OR the anchor is about the shared row the receiver holds (always,
    here), OR the receiver got that exact (subject, value) before."""

    state = spec.state
    truth_grid = {c: state[c] for c in CELLS}
    perceptions = _perceptions(spec)

    commits = report["commits"]
    grids = {p: commits.get(p, {}).get("grid", {}) for p in spec.players}
    correct_cells = {p: sum(1 for c in CELLS if grids[p].get(c) == truth_grid[c]) for p in spec.players}

    sent: dict[str, int] = {p: 0 for p in spec.players}
    redundant: dict[str, int] = {p: 0 for p in spec.players}
    received: dict[str, set[tuple[str, str]]] = {p: set() for p in spec.players}

    for entry in report["transcript"]:
        action = entry["action"]
        if action["kind"] != "say" or not entry.get("delivered"):
            continue
        sender = entry["actor"]
        receivers = [p for p in spec.players if p != sender] if action["receiver"] == "shared" else [action["receiver"]]
        for d in action["deltas"]:
            subject, obj = d["subject"], d["object"]
            if subject not in CELLS and subject != DOOR_FACT:
                continue  # only cell/anchor bits count (beliefs/corrections don't)
            value = obj[len("value=") :]
            for r in receivers:
                sent[sender] += 1
                if subject == DOOR_FACT:
                    already = any(c in perceptions[r] for c in ROW3_CELLS)  # the anchor's row is held
                else:
                    already = perceptions[r].get(subject) == value or (subject, value) in received[r]
                if already:
                    redundant[sender] += 1
                else:
                    received[r].add((subject, value))

    first_correct = None
    for entry in report["transcript"]:
        if entry["action"]["kind"] == "correct":
            first_correct = {
                "round": entry["round"],
                "by": entry["actor"],
                "target": entry["action"]["target"],
                "object": entry["action"]["deltas"][0]["object"] if entry["action"]["deltas"] else None,
            }
            break

    return {
        "correct_cells": correct_cells,
        "recovery": all(v == len(CELLS) for v in correct_cells.values()),
        "redundancy": {p: {"sent": sent[p], "redundant": redundant[p], "lacked": sent[p] - redundant[p]} for p in spec.players},
        "first_correct": first_correct,
        "n_corrects": sum(1 for e in report["transcript"] if e["action"]["kind"] == "correct"),
    }


# ── the acceptance run: 12 runs × 12 checks ───────────────────────────────


def _forced_v0_attempt() -> dict[str, Any]:
    """Check-6 kernel sub-check: a V0 agent whose policy ATTEMPTS the
    correction is rejected with the named gap and never delivered."""

    ep = make_episode("clean")
    spec = ep["spec"]

    def rogue(view: dict[str, str], round_no: int, transcript: list[dict[str, Any]]) -> Action:
        if round_no != 1:
            return Pass()
        return Correct(
            "b",
            DOOR_FACT,
            (correct_delta("a", "b", "c1", "c2", 1, spec.name, ()),),
        )

    a = Agent("a", spec, rogue, capabilities=CAPS["V0"], policy_note="V0 forced attempt")
    b = Agent("b", spec, lambda view, r, t: Pass(), capabilities=CAPS["V0"], policy_note="V0")
    report = Game(spec, {"a": a, "b": b}, seed=GAMERUN_SEED).run(write=False)
    rej = report["agents"]["a"]["rejections"]
    return {
        "rejected": bool(rej) and "assert_about_other" in rej[0]["reason"],
        "named_gap": rej[0]["reason"] if rej else None,
        "n_corrects_in_transcript": sum(1 for e in report["transcript"] if e["action"]["kind"] == "correct"),
    }


def run_e5_1(out_dir: Path | None = None) -> dict[str, Any]:
    """The official E5.1 acceptance: 2 episodes × 3 variants = 12 runs +
    the forced-V0 sub-check; writes the per-run game reports and
    `phase-5/e5.1.json` (checks included)."""

    from kainos.harness.paths import default_results_dir

    out_dir = out_dir if out_dir is not None else default_results_dir()
    (out_dir / "phase-5").mkdir(parents=True, exist_ok=True)

    runs: dict[str, dict[str, Any]] = {}
    for episode in ("clean", "false"):
        for variant in ("V0", "V1", "V2"):
            key = f"e5.1-{episode}-{variant.lower()}"
            ep = make_episode(episode)
            game = build_game(episode, variant)
            report = game.run(write=True, out_dir=out_dir)
            score = score_run(report, ep["spec"])
            runs[key] = {"episode": episode, "variant": variant, "planted_col": ep["planted_col"], "report": report, "score": score}

    forced = _forced_v0_attempt()

    def frac(d: dict[str, int]) -> Fraction:
        return Fraction(d["redundant"], d["sent"]) if d["sent"] else Fraction(0)

    clean = {v: runs[f"e5.1-clean-{v.lower()}"] for v in ("V0", "V1", "V2")}
    false = {v: runs[f"e5.1-false-{v.lower()}"] for v in ("V0", "V1", "V2")}

    def r12(v: dict[str, Any], p: str) -> dict[str, int]:
        return v["score"]["redundancy"][p]

    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append({"check": len(checks) + 1, "name": name, "passed": bool(passed), "detail": detail})

    # 1 — clean episode: every variant recovers (20/20 each)
    ok = all(runs[k]["score"]["recovery"] for k in runs if runs[k]["episode"] == "clean")
    add(
        "clean-recovery-all-variants",
        ok,
        {k: runs[k]["score"]["correct_cells"] for k in sorted(runs) if k.startswith("e5.1-clean")},
    )

    # 2 — clean: V1 and V2 redundancy exactly 1/9 per agent
    detail2 = {
        f"{v}/{p}": f"{r12(clean[v], p)['redundant']}/{r12(clean[v], p)['sent']}" for v in ("V1", "V2") for p in ("a", "b")
    }
    add("clean-redundancy-v1-v2-exact-1-of-9", all(frac(r12(clean[v], p)) == Fraction(1, 9) for v in ("V1", "V2") for p in ("a", "b")), detail2)

    # 3 — clean: V0 redundancy exactly 5/13 per agent; gap == 32/117 >= 0.25
    gap = Fraction(5, 13) - Fraction(1, 9)
    detail3 = {
        "v0": {p: f"{r12(clean['V0'], p)['redundant']}/{r12(clean['V0'], p)['sent']}" for p in ("a", "b")},
        "gap": f"{gap.numerator}/{gap.denominator}",
    }
    add(
        "clean-redundancy-v0-exact-5-of-13-and-gap",
        all(frac(r12(clean["V0"], p)) == Fraction(5, 13) for p in ("a", "b")) and gap == Fraction(32, 117) and gap >= Fraction(25, 100),
        detail3,
    )

    # 4 — false, V1: latency == 4 (by a, target b) AND both grids 20/20
    fc4 = false["V1"]["score"]["first_correct"]
    add(
        "false-v1-detection-round-4-and-recovery",
        fc4 is not None and fc4["round"] == 4 and fc4["by"] == "a" and fc4["target"] == "b" and false["V1"]["score"]["recovery"],
        {**fc4, "recovery": false["V1"]["score"]["recovery"], "correct_cells": false["V1"]["score"]["correct_cells"]},
    )

    # 5 — false, V2: same — second-order belief modeling suffices
    fc5 = false["V2"]["score"]["first_correct"]
    add(
        "false-v2-detection-round-4-and-recovery",
        fc5 is not None and fc5["round"] == 4 and fc5["by"] == "a" and fc5["target"] == "b" and false["V2"]["score"]["recovery"],
        {**fc5, "recovery": false["V2"]["score"]["recovery"], "correct_cells": false["V2"]["score"]["correct_cells"]},
    )

    # 6 — false, V0: zero corrections; a commits the planted row (exactly
    #      2 cells wrong); b 20/20; and the forced V0 attempt is a named-gap rejection
    v0 = false["V0"]
    v0_grid_a = v0["report"]["commits"].get("a", {}).get("grid", {})
    ep_false = make_episode("false")
    truth3 = {c: ep_false["truth"][c] for c in ROW3_CELLS}
    wrong_a = [c for c in ROW3_CELLS if v0_grid_a.get(c) != truth3[c]]
    wrong_total = [c for c in CELLS if v0_grid_a.get(c) != ep_false["truth"][c]]
    add(
        "false-v0-structurally-uncorrectable",
        v0["score"]["n_corrects"] == 0
        and sorted(wrong_a) == sorted(wrong_total)
        and len(wrong_a) == 2
        and v0["score"]["correct_cells"]["b"] == len(CELLS)
        and forced["rejected"]
        and forced["n_corrects_in_transcript"] == 0,
        {
            "wrong_cells_a": wrong_total,
            "v0_b_correct": v0["score"]["correct_cells"]["b"],
            "forced_attempt": forced,
        },
    )

    # 7 — false, V1 & V2: disputed pair preserved in EACH of the 4 stores
    detail7 = {}
    ok7 = True
    for v in ("V1", "V2"):
        for p in ("a", "b"):
            audit = false[v]["report"]["audit"][p]
            detail7[f"{v}/{p}"] = audit["n_disputes_preserved"]
            ok7 = ok7 and audit["n_disputes_preserved"] >= 2
    add("false-disputed-pairs-preserved-in-all-four-stores", ok7, detail7)

    # 8 — all 12 runs: zero audit violations (no unbacked mind-reading)
    viol = {k: sum(len(a["violations"]) for a in r["report"]["audit"].values()) for k, r in runs.items()}
    add("all-runs-zero-audit-violations", all(v == 0 for v in viol.values()), {k: v for k, v in viol.items() if v})

    # 9 — all 12 runs: zero view leaks
    leaks = {k: r["report"]["negative_control"]["view_leaks"] for k, r in runs.items()}
    add("all-runs-zero-view-leaks", all(v == 0 for v in leaks.values()), {k: v for k, v in leaks.items() if v} or "0 everywhere")

    # 10 — determinism: re-execute all 12 runs, hashes must match
    rerun = {}
    ok10 = True
    for k, r in runs.items():
        r2 = build_game(r["episode"], r["variant"]).run(write=False)
        rerun[k] = r2["determinism_hash"]
        ok10 = ok10 and r2["determinism_hash"] == r["report"]["determinism_hash"]
    add("all-runs-bit-identical-on-rerun", ok10, {"sample": {k: rerun[k][:22] for k in sorted(rerun)[:3]}})

    # 11 — all 12 runs: zero budget rejections (and zero corruption events: p=0)
    ev = {k: [e["kind"] for e in r["report"]["channel"]["events"]] for k, r in runs.items()}
    add("all-runs-no-budget-rejections-no-corruption", all(not e for e in ev.values()), {k: v for k, v in ev.items() if v} or "clean")

    # 12 — all 24 commits are exactly 20-cell reconstructions
    bad = []
    for k, r in runs.items():
        for p in spec_players(r["report"]):
            g = r["report"]["commits"].get(p, {}).get("grid", {})
            if set(g) != set(CELLS):
                bad.append(f"{k}/{p}: {len(g)} cells")
    add("all-24-commits-are-20-cell-reconstructions", not bad, bad or "24/24 full grids")

    passed = sum(1 for c in checks if c["passed"])
    report = {
        "experiment": "e5.1",
        "claim": "The Shared Grid (T2): ToM separates on redundancy, the false-belief probe is structurally clean, disputes survive — see experiments.md",
        "seed": SEED,
        "runs": {
            k: {
                "episode": r["episode"],
                "variant": r["variant"],
                "planted_col": r["planted_col"],
                "determinism_hash": r["report"]["determinism_hash"],
                "score": r["score"],
            }
            for k, r in runs.items()
        },
        "forced_v0_attempt": forced,
        "checks_total": CHECKS,
        "checks_passed": passed,
        "checks": checks,
    }
    (out_dir / "phase-5" / "e5.1.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def spec_players(report: dict[str, Any]) -> list[str]:
    return list(report["players"])


class E5_1Experiment:
    """House-style experiment object (benches lazily import Result and
    write their full report themselves)."""

    name = "e5.1"
    hypothesis = (
        "Agents that model their partner's perspective (V1/V2) beat the ToM ablation (V0) at "
        "equal budget on the computable redundancy ratio, and only they can pass the embedded "
        "false-belief probe: V0 is structurally incapable of the explicit correction assertion "
        "(capability gate), commits the planted row, and the mismatch survives as a disputed "
        "pair — never averaged."
    )
    metric = "acceptance checks passed (0-12)"
    threshold = "12/12"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e5_1()
        passed = report["checks_passed"]
        return Result(
            name=self.name,
            passed=passed == CHECKS,
            value=passed / CHECKS,
            evidence=[
                Path("results/phase-5/e5.1.json"),
            ]
            + [Path(f"results/phase-5/e5.1-{k.split('e5.1-', 1)[1]}.json") for k in sorted(report["runs"])],
            config={
                "seed": SEED,
                "runs": sorted(report["runs"]),
                "checks_passed": passed,
                "checks": CHECKS,
                "deviations": ["D-e5a-amend (round-6 door-corridor coherence rule)", "D-e5b (commit count 24)"],
                "dataset_hash": None,
            },
            threshold=self.threshold,
        )
