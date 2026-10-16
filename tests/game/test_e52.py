"""E5.2 kernel wiring + bench (reduced mode for the gate; the full
official design runs in the hermetic official run, not here)."""

from __future__ import annotations

import json

import pytest

from kainos.game import range_game as rg
from kainos.game.e52 import build_episode, run_e5_2

REPR_PAIRS = (("V0", "V0"), ("V1", "V1"), ("V2", "V2"), ("V1", "V2"), ("V2", "V1"))


def _draws() -> tuple[int, int, int, int]:
    import random

    return rg.episode_draws(random.Random(510200 + 4 + 1))  # episode i=4 (xa=4 ∈ B)


class TestEpisode:
    def test_honest_episode_transcript_and_audit(self):
        g = build_episode(1, 15, "V2", "V1", (0, 0, 0, 0), 0)
        r = g.run(write=False)
        kinds = [(e["actor"], e["action"]["kind"]) for e in r["transcript"]]
        assert kinds == [
            ("a", "say"),
            ("b", "say"),
            ("a", "say"),
            ("b", "say"),
            ("a", "commit"),
            ("b", "commit"),
        ]
        says = [e for e in r["transcript"] if e["action"]["kind"] == "say"]
        assert all(e.get("delivered") for e in says)
        assert isinstance(r["commits"]["a"]["estimate"], int)
        assert isinstance(r["commits"]["b"]["estimate"], int)
        for p in ("a", "b"):
            assert r["audit"][p]["violations"] == []
        assert r["negative_control"]["view_leaks"] == 0
        assert r["channel"]["events"] == []

    def test_v0_store_has_no_beliefs_about_other(self):
        g = build_episode(1, 15, "V0", "V0", (0, 0, 0, 0), 0)
        g.run(write=False)
        for p in ("a", "b"):
            beliefs = [
                a
                for a in g.agents[p].codex.query()
                if a.relation.id == "believes" and a.subject.kind == "agent"
            ]
            assert beliefs == []

    def test_v2_store_belief_is_supported(self):
        g = build_episode(1, 15, "V2", "V2", (0, 0, 0, 0), 0)
        r = g.run(write=False)
        for p in ("a", "b"):
            beliefs = [
                a
                for a in g.agents[p].codex.query()
                if a.relation.id == "believes" and a.subject.kind == "agent"
            ]
            assert len(beliefs) == 1
            prov = beliefs[0].provenance
            assert prov is not None and prov.source is not None
            assert prov.source.uri == f"agent:{p}"  # self-sourced inference
            assert prov.evidence  # cites the other's claim assertions
        # and the audit sees zero violations on that content
        for p in ("a", "b"):
            assert r["audit"][p]["violations"] == []

    def test_bluffed_episode_line_is_genuinely_false(self):
        # xa=4 ∈ B: a's R1 window must not contain 4
        g = build_episode(4, 9, "V2", "V2", _draws(), 3)
        r = g.run(write=False)
        says = [
            (e["actor"], d["object"])
            for e in r["transcript"]
            if e["action"]["kind"] == "say"
            for d in e["action"]["deltas"]
            if d["subject"].endswith(":a")
        ]
        assert len(says) == 2
        r1_obj = says[0][1][len("value=") :]
        lo, hi = (int(x) for x in r1_obj.split("-"))
        assert not (lo <= 4 <= hi)


class TestBench:
    @pytest.fixture()
    def reduced(self, tmp_path, monkeypatch):
        monkeypatch.setenv("KAINOS_E52_EPISODES", "8")
        monkeypatch.setenv("KAINOS_E52_SAMPLES", "128")
        return run_e5_2(out_dir=tmp_path)

    def test_reduced_bench_passes(self, reduced):
        assert reduced["mode"] == "reduced"
        assert reduced["checks_passed"] == 8
        assert all(c["passed"] for c in reduced["checks"])
        assert reduced["fallback_uses"] == 0

    def test_reduced_bench_deterministic(self, tmp_path, monkeypatch):
        monkeypatch.setenv("KAINOS_E52_EPISODES", "8")
        monkeypatch.setenv("KAINOS_E52_SAMPLES", "128")
        r1 = run_e5_2(out_dir=tmp_path / "a")
        r2 = run_e5_2(out_dir=tmp_path / "b")
        for k in ("pooled_mean_err", "head_to_head", "detection", "leakage_bits"):
            assert r1[k] == r2[k], k

    def test_reduced_usage_is_exactly_a_quarter(self, reduced):
        for k in ("V0-V0", "V1-V1", "V2-V2", "V1-V2", "V2-V1"):
            recs = reduced["per_pair_games"][k]
            assert sum(1 for r in recs if r["a_bluffed"]) == 2
            assert sum(1 for r in recs if r["b_bluffed"]) == 2
        assert reduced["pooled_mean_err"]["V0"] != reduced["pooled_mean_err"]["V2"]

    def test_report_file_written(self, tmp_path, monkeypatch):
        monkeypatch.setenv("KAINOS_E52_EPISODES", "8")
        monkeypatch.setenv("KAINOS_E52_SAMPLES", "128")
        run_e5_2(out_dir=tmp_path)
        d = json.loads((tmp_path / "phase-5" / "e5.2.json").read_text())
        assert d["checks_passed"] == 8
        assert d["mode"] == "reduced"


class TestExperimentClass:
    def test_shape(self, monkeypatch):
        from kainos.game.e52 import E5_2Experiment

        monkeypatch.setenv("KAINOS_E52_EPISODES", "8")
        monkeypatch.setenv("KAINOS_E52_SAMPLES", "128")
        e = E5_2Experiment()
        r = e.run()
        assert e.name == "e5.2"
        assert e.threshold == "8/8"
        assert r.passed is True
        assert r.value == 1.0
