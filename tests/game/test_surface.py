"""E5.4 surface codec: frozen grammar, round-trip integrity, the
bounded-retry-then-drop discipline, and the X2 strip (seam neutrality)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kainos.game.actions import Pass
from kainos.game.agent import Agent
from kainos.game.scheduler import Game
from kainos.game.shared_grid import (
    CAPS,
    CELLS,
    DOOR_FACT,
    GAMERUN_SEED,
    build_game,
    cell_delta,
    correct_delta,
    make_episode,
)
from kainos.game.surface import (
    GRAMMAR_SHA,
    LLM_SYSTEM_PROMPT,
    CanonicalRenderer,
    ClaimSpec,
    LlmRenderer,
    ScriptedDropRenderer,
    SurfaceCodec,
    claim_from_delta,
    parse_sentence,
    render_sentence,
)
from kainos.lang.llm import MockBackend


def _derived_path() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        cand = base / "results" / "phase-5" / "e5.4-derived.json"
        if cand.exists():
            return cand
    return Path("")


@pytest.mark.parametrize("value", ["empty", "wall", "goal", "key", "door"])
def test_cell_round_trip_all_grid_cells(value: str) -> None:
    codec = SurfaceCodec(CanonicalRenderer())
    for cell in CELLS:
        d = cell_delta("a", cell, value, 1, 0, "g", "cell")
        out, log = codec.pass_deltas((d,))
        assert len(out) == 1 and out[0].assertion.id == d.assertion.id, cell
        assert log[0]["status"] == "delivered"
        assert log[0]["text"] == f"a says: {cell} is {value}."


def test_anchor_and_correct_round_trip() -> None:
    codec = SurfaceCodec(CanonicalRenderer())
    for col in ("c1", "c2", "c3", "c4"):
        a = cell_delta("b", DOOR_FACT, col, 3, 0, "g", "anchor")
        out, log = codec.pass_deltas((a,))
        assert (
            out[0].assertion.id == a.assertion.id
            and log[0]["text"] == f"b says: my door in row 3 is at column {col}."
        )
    d = correct_delta("a", "b", "c2", "c4", 4, "g", ("ev",))
    out, log = codec.pass_deltas((d,))
    assert out[0].assertion.id == d.assertion.id
    assert log[0]["text"] == "a says: b, your door reading is c4, mine is c2."


@pytest.mark.parametrize(
    "text",
    [
        "a says: r1c2 is empty",  # no period
        "a says: r1c2 is purple.",  # out-of-vocabulary value
        "a says: r6c2 is wall.",  # out-of-grid cell
        "a says: r1c5 is wall.",  # out-of-grid column
        "",  # nothing
        "a says: the door is at column 2",  # free-form (the LLM's natural temptation)
        "a says: b, your door reading is c5, mine is c2.",  # column out of range
        "a says: my door in row 3 is at column c0.",  # column out of range
        "a says: a, your door reading is c1, mine is c2.",  # self-targeted correction
        "A says: r1c2 is wall.",  # uppercase sender
    ],
)
def test_parser_is_strict(text: str) -> None:
    assert parse_sentence(text) is None, text


def test_claim_classification_and_rejects() -> None:
    assert (
        claim_from_delta(cell_delta("a", "r1c2", "wall", 1, 0, "g", "cell")) is not None
    )
    assert claim_from_delta(correct_delta("a", "b", "c1", "c2", 4, "g", ())) is not None
    # a belief-shaped delta is not a surface claim (not a channel sentence)
    from kainos.codex.memory import InMemoryCodexStore
    from kainos.exchange.protocol import AssertionDelta
    from kainos.game.agent import belief_assertion

    st = InMemoryCodexStore()
    b = belief_assertion("a", "b", DOOR_FACT, "c2", "agent:a")
    st.add(b)
    d = AssertionDelta(assertion=b, node_id="a", timestamp="2026-01-01T00:00:00+00:00")
    assert claim_from_delta(d) is None  # relation `believes` is not in the grammar
    import dataclasses

    spec = dataclasses.replace(make_episode("clean")["spec"], name="t")
    rogue = lambda view, r, t_: Pass()
    g = Game(
        spec,
        {
            "a": Agent("a", spec, rogue, CAPS["V0"]),
            "b": Agent("b", spec, rogue, CAPS["V0"]),
        },
        seed=GAMERUN_SEED,
    )
    assert g.surface is None  # the structured arm is the default (bit-identical kernel)


def test_llm_renderer_round_trips_and_drops_bounded() -> None:
    probe_cell = ClaimSpec("cell", "a", {"cell": "r1c3", "value": "key"})
    probe_anchor = ClaimSpec("anchor", "a", {"col": "2"})
    good = [render_sentence(probe_cell), render_sentence(probe_anchor)]
    mock = MockBackend(good)
    codec = SurfaceCodec(LlmRenderer(mock, "mock-model"))
    out, log = codec.pass_deltas(
        (
            cell_delta("a", "r1c3", "key", 1, 0, "g", "cell"),
            cell_delta("a", DOOR_FACT, "c2", 3, 0, "g", "anchor"),
        )
    )
    assert len(out) == 2 and all(x["status"] == "delivered" for x in log)
    assert len(mock.calls) == 2  # one completion per delta (no retry needed)
    assert LLM_SYSTEM_PROMPT in mock.calls[0][0]["content"]

    # a renderer that never round-trips: ONE bounded retry, then drop + log
    bad = MockBackend(["the door, i would say, is at column two, roughly"])
    codec2 = SurfaceCodec(LlmRenderer(bad, "bad-model"))
    d = cell_delta("a", DOOR_FACT, "c2", 3, 0, "g", "anchor")
    out2, log2 = codec2.pass_deltas((d,))
    assert out2 == ()
    assert log2[0]["status"] == "dropped"
    assert len(bad.calls) == 2  # exactly the bounded retry — no rescue loops
    assert (
        log2[0]["text"] == bad.replies[-1]
    )  # the failed sentence is recorded verbatim (auditable)


def test_scripted_drop_is_exact() -> None:
    codec = SurfaceCodec(ScriptedDropRenderer(drop=("b", "anchor")))
    d_kept = cell_delta("b", DOOR_FACT, "c1", 3, 0, "g", "anchor")
    d_other_cell = cell_delta("b", "r4c2", "wall", 2, 1, "g", "cell")
    d_a_anchor = cell_delta("a", DOOR_FACT, "c3", 3, 0, "g", "anchor")
    out, log = codec.pass_deltas((d_kept, d_other_cell, d_a_anchor))
    statuses = [x["status"] for x in log]
    assert statuses == ["dropped", "delivered", "delivered"]
    assert len(out) == 2


def test_x2_strip_seam_neutrality_one_game() -> None:
    """The X2 claim on one game (the full 6-run claim is X2 in e54.py):
    canonical-codec report, surface blocks stripped, hashes to the
    structured arm's determinism hash."""

    import dataclasses

    from kainos.game.e54 import _stripped_hash

    g_off = build_game("clean", "V1")
    r_off = g_off.run(write=False)
    g_on = dataclasses.replace(
        build_game("clean", "V1"), surface=SurfaceCodec(CanonicalRenderer())
    )
    r_on = g_on.run(write=False)
    # the only added machine content is the surface log itself
    assert _stripped_hash(r_on) == r_off["determinism_hash"]
    assert any("surface" in e for e in r_on["transcript"])
    # ... and every agent's store is content-identical
    for p in r_off["players"]:
        s_off = sorted(
            (a.id, a.subject.id, a.relation.id, str(a.object_id))
            for a in g_off.agents[p].codex.query()
        )
        s_on = sorted(
            (a.id, a.subject.id, a.relation.id, str(a.object_id))
            for a in g_on.agents[p].codex.query()
        )
        assert s_on == s_off, p
    # canonical grammar pin (grammar drift is a test failure by construction)
    derived = _derived_path()
    if derived.exists():
        assert GRAMMAR_SHA == json.loads(derived.read_text())["grammar_sha"]
    else:
        assert GRAMMAR_SHA.startswith("sha256:")
