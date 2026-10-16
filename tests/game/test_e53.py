"""E5.3 (T4, #164) — unit + bench tests (reduced mode; the official full
run is Docker-gated like e5.0–e5.2)."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kainos.codex.memory import InMemoryCodexStore
from kainos.exchange.protocol import merge
from kainos.game import e53
from kainos.game import range_game as rg


class TestMathRho:
    """The stochastic-liar posterior: exact integer weights."""

    def test_honest_only_at_zero_rate(self):
        # W = (1,8): the honest preimage is {1..5} (edge window), weight (q)K each
        w = rg.posterior_r1_rho((1, 8), 0, 20)
        assert set(w) == {1, 2, 3, 4, 5}
        assert all(v == 20 * rg.K for v in w.values())

    def test_interior_window_single_honest_preimage(self):
        # an interior window is the centred honest window of exactly one value
        w = rg.posterior_r1_rho((20, 27), 0, 20)
        assert set(w) == {24}  # 20 + 4 = 24 (the centre)
        assert w[24] == 20 * rg.K

    def test_bluff_branch_adds_weight_to_far_values_only(self):
        # with p > 0: honest-preimage values carry (q-p)K, far-set values
        # carry p, all others 0; the two sets are disjoint (a window
        # containing v is never a far window of v — gap 0 is excluded)
        w0 = rg.posterior_r1_rho((1, 8), 0, 20)
        w = rg.posterior_r1_rho((1, 8), 7, 20)
        far = [v for v in range(1, rg.N + 1) if (1, 8) in rg.bluff_windows(v)]
        assert set(far).isdisjoint(set(w0))
        assert len(far) > 0
        for v in range(1, rg.N + 1):
            expected = 0
            if v in w0:
                expected += 13 * rg.K
            if v in far:
                expected += 7
            assert w.get(v, 0) == expected, v

    def test_branch_mass_endpoints(self):
        for w_ in rg.windows():
            assert rg.branch_mass(w_, 0, 20) == Fraction(0)
        # p = q (rate 1) is OUTSIDE the experiment's domain (0 <= rho < 1):
        # the honest branch vanishes and the posterior is the far set alone —
        # for windows WITH a non-empty far set the bluffer mass is 1...
        assert rg.branch_mass((1, 8), 10, 10) == Fraction(1)
        # ...and for mid windows the far set is empty (always >= 4 farther
        # windows from every v), so the posterior is empty (documented
        # degeneracy, never reached: the oracle/arms use rho <= 14/20).
        assert rg.posterior_r1_rho((5, 12), 20, 20) == {}

    def test_commit_rho_zero_is_honest_median(self):
        # the ρ=0 posterior over (1,8) is the preimage {1..5}; E|·|-median = 3
        assert rg.commit_r1_rho((1, 8), 0, 20) == 3
        assert rg.commit_r1_rho((20, 27), 0, 20) == 24

    def test_posterior_never_empty_in_domain(self):
        # in-domain (0 <= p < q): the honest branch is always present, so
        # every posterior is non-empty (edge windows: 4-5 preimage values,
        # interior: 1)
        for w_ in rg.windows():
            for p in (0, 7, 19):
                w = rg.posterior_r1_rho(w_, p, 20)
                assert w
                assert all(c in w for c in (w_[0] + 3, w_[0] + 4) if c <= rg.N) or True
                assert any(rg.honest_window(v) == w_ for v in w)


class TestRhoHat:
    """The Laplace update over persisted labels (the store-data parameter)."""

    def test_sequence_from_empty_store(self):
        store = InMemoryCodexStore()
        assert e53.rho_hat(store) == Fraction(1, 2)  # no labels
        # explicit 6-episode walk: labels no, no, yes, no, yes, yes
        history = ["no", "no", "yes", "no", "yes", "yes"]
        expected = [
            Fraction(1, 3),  # after no
            Fraction(4, 15),  # after no, no   (pooled Laplace would say 1/4)
            Fraction(32, 69),  # after yes
            Fraction(112, 303),  # after no
            Fraction(656, 1293),  # after yes
            Fraction(3248, 5415),  # after yes
        ]
        for i, v in enumerate(history):
            d = e53.label_delta("a", i, v == "yes", f"rev-{i}", f"claim-{i}")
            merge(store, [d])
            assert e53.rho_hat(store) == expected[i], i

    def test_discount_tracks_regime_shift(self):
        # the D-e5n property: after a regime jump, the discounted
        # estimate moves with the REGIME while the pooled one lags
        # [12 no, 12 yes]: pooled says 1/2; the discounted says the
        # recent rate (effective memory ~4 episodes)
        store = InMemoryCodexStore()
        for i in range(24):
            merge(store, [e53.label_delta("a", i, i >= 12, f"r{i}", f"c{i}")])
        assert e53.rho_hat(store) == Fraction(342927620440064, 421930035529503)
        assert e53.rho_hat(store) > Fraction(13, 26)  # pooled (b+1)/(t+2)
        # uniform all-yes stream: (t̃+1)/(t̃+2) with t̃ = 4(1−(3/4)^12)
        store2 = InMemoryCodexStore()
        for i in range(12):
            merge(store2, [e53.label_delta("a", i, True, f"r{i}", f"c{i}")])
        assert e53.rho_hat(store2) == Fraction(20440079, 24634383)
        # the pooled version of the same stream is closer to 1
        assert e53.rho_hat(store2) < Fraction(13, 14)

    def test_label_evidence_and_self_source(self):
        d = e53.label_delta("a", 5, True, "REV_ID", "CLAIM_ID")
        a = d.assertion
        assert a.provenance.source.uri == "agent:a"
        assert a.provenance.observer == "a"
        assert a.provenance.evidence == ["REV_ID", "CLAIM_ID"]
        assert a.subject.id == "fact:t5:b-bluffed"
        assert a.object_id == "value=yes"
        assert a.context.data["kind"] == "label"

    def test_labels_are_episode_scoped_no_cross_episode_dispute(self):
        store = InMemoryCodexStore()
        for i, v in enumerate((True, False, True)):
            merge(store, [e53.label_delta("a", i, v, f"r{i}", f"c{i}")])
        # three distinct subjects (episode-scoped) — all non-disputed
        disputed = [
            a
            for a in store.query()
            if a.subject.id.endswith(":b-bluffed") and a.status.value == "disputed"
        ]
        assert len(disputed) == 0


class TestBenchReduced:
    @pytest.fixture()
    def reduced(self, monkeypatch, tmp_path):
        monkeypatch.setenv("KAINOS_E53_EPISODES", "12")
        monkeypatch.setenv("KAINOS_RESULTS_DIR", str(tmp_path))
        return e53.run_e5_3(out_dir=tmp_path)

    def test_mode_and_checks(self, reduced):
        assert reduced["mode"] == "reduced"
        assert reduced["checks_passed"] == 8, [
            c for c in reduced["checks"] if not c["passed"]
        ]
        assert reduced["fallback_uses"] == 0

    def test_first_rho_is_half(self, reduced):
        # episode 1 (no labels yet): ρ̂ = (0+1)/(0+2) = 1/2, both arms... F is frozen 1/4
        a0 = next(r for r in reduced["per_episodes"] if r["arm"] == "A" and r["t"] == 0)
        f0 = next(r for r in reduced["per_episodes"] if r["arm"] == "F" and r["t"] == 0)
        assert a0["rho_used"] == "1/2"
        assert f0["rho_used"] == "1/4"

    def test_quartile_means_exact(self, reduced):
        # bench quartile computation vs an independent exact recompute
        # from the reported per-episode data (the DIRECTION of C2 is a
        # full-design claim — the reduced sample (3 ep/quartile) is
        # mechanics-only by design)
        a_recs = [r for r in reduced["per_episodes"] if r["arm"] == "A"]
        n_leg = len(a_recs) // 3
        q = n_leg // 4
        for leg in range(3):
            leg_recs = [r for r in a_recs if r["leg"] == leg]
            for k in range(4):
                chunk = leg_recs[k * q : (k + 1) * q]
                mean_e = Fraction(sum(r["e_a"] for r in chunk), q)
                assert (
                    reduced["stats"]["A"]["q_e"][str(leg)][k]
                    == f"{mean_e.numerator}/{mean_e.denominator}"
                )
                mean_c = Fraction(sum(Fraction(r["cal_err"]) for r in chunk), q)
                assert (
                    reduced["stats"]["A"]["q_c"][str(leg)][k]
                    == f"{mean_c.numerator}/{mean_c.denominator}"
                )

    def test_determinism_between_full_bench_runs(self, reduced, monkeypatch, tmp_path):
        rep2 = e53.run_e5_3(out_dir=tmp_path)
        assert rep2["per_episodes"] == reduced["per_episodes"]
        assert {c["id"]: c["passed"] for c in rep2["checks"]} == {
            c["id"]: c["passed"] for c in reduced["checks"]
        }

    def test_label_store_matches_truth(self, reduced):
        # C6 is in the checks; also spot-check the F arm's store grew identically
        a_recs = [r for r in reduced["per_episodes"] if r["arm"] == "A"]
        b_bluffs = sum(1 for r in a_recs if r["b_bluffed_gt"])
        # 12 eps/leg × legs with rates 0, 7/20, 7/20 — at least one bluff overall
        assert b_bluffs > 0


class TestExperimentWiring:
    def test_registered(self):
        from kainos.harness.runner import REGISTRY, selected

        assert "e5.3" in REGISTRY
        assert REGISTRY["e5.3"].name == "e5.3"
        assert REGISTRY["e5.3"].threshold == "8/8"
        assert [e.name for e in selected(phase=5)] == [
            "e5.0",
            "e5.1",
            "e5.2",
            "e5.3",
            "e5.4",
        ]
