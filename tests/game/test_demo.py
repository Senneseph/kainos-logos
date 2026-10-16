"""T1 kernel demos — acceptance: the clean-sharing case and the
contradiction (dispute-discipline) case, plus report hygiene."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from kainos.game.demo import run_demo_games


def test_shared_view_is_fully_green() -> None:
    s = run_demo_games(write=False)["shared-view"]
    assert s["scores"] == {"a_correct": True, "b_correct": True, "score": 1.0}
    assert s["negative_control"]["view_leaks"] == 0
    for p in ("a", "b"):
        audit = s["audit"][p]
        assert audit["violations"] == []
        assert audit["n_about_other"] == 1
        assert audit["n_correct"] == 1
        assert audit["n_supported"] == 1
    # the re-share was an IDEMPOTENT duplicate, not a conflict
    dupes = [o for p in ("a", "b") for o in s["agents"][p]["observe_reports"] if o["duplicates"] == 1]
    assert len(dupes) == 2
    conflicts = [o for p in ("a", "b") for o in s["agents"][p]["observe_reports"] if o["conflicts_preserved"] > 0]
    assert conflicts == []


def test_contradiction_preserves_both_sides_and_never_averages() -> None:
    c = run_demo_games(write=False)["contradiction-talk"]
    # the game still succeeds: both agents recovered the correct value
    assert c["scores"]["score"] == 1.0
    a = c["audit"]["a"]
    # a's store holds both b's wrong rumor and its correction, DISPUTED
    # (both sides of the disputed fact pair survive, cross-linked)
    assert a["n_disputes_preserved"] == 2
    # and the deception is visible in the belief layer: exactly ONE of the
    # three beliefs about b is wrong (the rumor), zero unsupported
    assert a["n_about_other"] == 3
    assert a["n_correct"] == 2
    assert a["n_supported"] == 3
    assert a["violations"] == []
    # the conflict landed in one merge: 2 preserved (both sides marked)
    landed = [o for o in c["agents"]["a"]["observe_reports"] if o["conflicts_preserved"] == 2]
    assert len(landed) == 1 and landed[0]["disputed_pairs"] == 1


def test_reports_are_written_and_hashes_stable(tmp_path: Path) -> None:
    r1 = run_demo_games(out_dir=tmp_path / "r1")
    r2 = run_demo_games(out_dir=tmp_path / "r2")
    for name in r1:
        assert r1[name]["determinism_hash"] == r2[name]["determinism_hash"]
        stored = json.loads((tmp_path / "r1" / "phase-5" / f"{name}.json").read_text())
        assert stored["determinism_hash"] == r1[name]["determinism_hash"]
        canonical = json.dumps(
            {k: v for k, v in stored.items() if k != "determinism_hash"},
            indent=2, sort_keys=True, ensure_ascii=False,
        )
        assert stored["determinism_hash"] == "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
