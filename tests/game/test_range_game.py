"""Math core of The Range Game: windows, exact posteriors, simulation,
leakage machinery, and the frozen-design pins (the offline derivation
that the official run must reproduce)."""

from __future__ import annotations

import math
import random
from fractions import Fraction

import pytest

from kainos.game import range_game as rg

B12 = frozenset(x for x in range(1, rg.N + 1) if x % 4 == 0)


class TestWindows:
    def test_41_canonical_windows(self):
        ws = rg.windows()
        assert len(ws) == 41
        assert ws[0] == (1, 8) and ws[-1] == (41, 48)
        assert all(hi - lo == rg.W - 1 for lo, hi in ws)

    def test_honest_window_contains_value(self):
        for x in range(1, rg.N + 1):
            lo, hi = rg.honest_window(x)
            assert lo <= x <= hi

    def test_honest_window_preimage_sizes(self):
        # anchor function: interior windows have exactly one preimage
        # value (v = start + 4); the two edge windows have five each.
        pre: dict[tuple[int, int], list[int]] = {}
        for x in range(1, rg.N + 1):
            pre.setdefault(rg.honest_window(x), []).append(x)
        assert len(pre) == 41
        assert sorted(pre[(1, 8)]) == [1, 2, 3, 4, 5]
        assert sorted(pre[(41, 48)]) == [45, 46, 47, 48]
        assert all(len(v) == 1 for w, v in pre.items() if w not in ((1, 8), (41, 48)))

    def test_bluff_windows_disjoint_and_farthest(self):
        for x in range(1, rg.N + 1):
            fw = rg.bluff_windows(x)
            assert len(fw) == rg.K
            for lo, hi in fw:
                assert not (lo <= x <= hi), (x, fw)
            gaps = [rg._gap(x, w) for w in fw]
            assert gaps == sorted(gaps, reverse=True)
            # strictly the top-4: nothing outside has a bigger gap
            outside = [rg._gap(x, w) for w in rg.windows() if rg._gap(x, w) > 0 and w not in fw]
            assert max(gaps) >= max(outside)

    def test_farsexcludes_the_window_itself(self):
        for w in rg.windows():
            far = rg._farset_of_window(w)
            assert w not in far and len(far) == rg.K


class TestPosteriors:
    def test_r1_weights_structure(self):
        for w in rg.windows():
            post = rg.posterior_r1(w, B12)
            for v, weight in post.items():
                if v in B12:
                    assert weight == 1 and w in rg.bluff_windows(v)
                else:
                    assert weight == rg.K and rg.honest_window(v) == w
            # every value in B whose farset contains w is present
            expected = {
                v
                for v in range(1, rg.N + 1)
                if (v in B12 and w in rg.bluff_windows(v))
                or (v not in B12 and rg.honest_window(v) == w)
            }
            assert set(post) == expected

    def test_full_sweep_support_decomposition(self):
        # the 41^3 sweep: posterior_full's support is EXACTLY the
        # honest branch (weight K^2) union the bluffer branch (weight 1)
        n_checked = 0
        for w1 in rg.windows():
            for w2 in rg.windows():
                for wrec in rg.windows():
                    declared = rg.declared_r2_window(wrec, B12)
                    far = rg._farset_of_window(declared)
                    post = rg.posterior_full(w1, w2, wrec, B12)
                    for v, weight in post.items():
                        if v in B12:
                            assert weight == 1 and w1 in rg.bluff_windows(v) and w2 in far
                        else:
                            assert weight == rg.K * rg.K and rg.honest_window(v) == w1 and w2 == declared
                    honest = {v for v in range(1, rg.N + 1) if v not in B12 and rg.honest_window(v) == w1 and w2 == declared}
                    bluff = {v for v in B12 if w1 in rg.bluff_windows(v) and w2 in far}
                    assert set(post) == honest | bluff
                    n_checked += 1
        assert n_checked == 41**3

    def test_v2_branch_separation(self):
        # the R2 claim perfectly separates honest from bluffer senders:
        # for a fixed (w1, wrec), exactly one of {declared, far} matches
        declared = rg.declared_r2_window((1, 8), B12)
        far = rg._farset_of_window(declared)
        assert declared not in far


class TestCommitAndMedian:
    def test_v0_is_24(self):
        e = rg.commit_estimate("V0", (1, 8), (1, 8), (1, 8), B12)
        assert e == 24

    def test_median_minimizes_and_tiebreaks_smallest(self):
        # uniform 1..48: both 24 and 25 minimize; smallest wins
        w = {v: 1 for v in range(1, rg.N + 1)}
        assert rg.est_median(w) == 24

    def test_empty_posterior_raises(self):
        with pytest.raises(ValueError):
            rg.est_median({})


class TestSimulation:
    def test_invariants_on_sampled_episodes(self):
        rng = random.Random(7)
        for _ in range(200):
            xa, xb = rng.randrange(1, rg.N + 1), rng.randrange(1, rg.N + 1)
            for la in ("V0", "V1", "V2"):
                for lb in ("V0", "V1", "V2"):
                    sim = rg.simulate_pair(xa, xb, la, lb, B12, rg.episode_draws(rng))
                    assert sim["e_a"] == abs(sim["est_a_of_b"] - xb)
                    assert sim["e_b"] == abs(sim["est_b_of_a"] - xa)
                    assert sim["win_a"] in (0.0, 0.5, 1.0)
                    assert sim["a_bluffed"] == (xa in B12)
                    # lines respect the protocol
                    if xa in B12:
                        assert sim["line_a"][0] in rg.bluff_windows(xa)
                    else:
                        assert sim["line_a"][0] == rg.honest_window(xa)
                    if xb in B12:
                        assert sim["line_b"][0] in rg.bluff_windows(xb)
                    else:
                        assert sim["line_b"][0] == rg.honest_window(xb)

    def test_b_v0_commit_is_frozen(self):
        # V0 always commits 24 regardless of the transcript
        rng = random.Random(9)
        for _ in range(50):
            xa, xb = rng.randrange(1, rg.N + 1), rng.randrange(1, rg.N + 1)
            sim = rg.simulate_pair(xa, xb, "V0", "V2", B12, rg.episode_draws(rng))
            assert sim["est_a_of_b"] == 24


class TestDesignPins:
    def test_balanced_pairs_cover_every_value(self):
        pairs = rg.balanced_pairs(5102)
        assert len(pairs) == 48
        assert {x for x, _ in pairs} == set(range(1, 49))
        assert {x for _, x in pairs} == set(range(1, 49))

    def test_frozen_pooled_errors(self):
        # the offline derivation the pre-registration freezes (seed 5102,
        # draws 510200+i+1): recomputed here from the SAME code.
        pairs = rg.balanced_pairs(5102)
        draws = [rg.episode_draws(random.Random(510200 + i + 1)) for i in range(rg.N)]
        for lvl, frozen in (("V0", Fraction(12)), ("V1", Fraction(583, 96)), ("V2", Fraction(79, 48))):
            recs = [rg.simulate_pair(xa, xb, lvl, lvl, B12, dr) for (xa, xb), dr in zip(pairs, draws)]
            pooled = Fraction(sum(r["e_a"] + r["e_b"] for r in recs), 2 * rg.N)
            assert pooled == frozen, (lvl, pooled, frozen)

    def test_frozen_detection_and_h2h(self):
        pairs = rg.balanced_pairs(5102)
        draws = [rg.episode_draws(random.Random(510200 + i + 1)) for i in range(rg.N)]

        def recs(la, lb):
            return [rg.simulate_pair(xa, xb, la, lb, B12, dr) for (xa, xb), dr in zip(pairs, draws)]

        v1 = Fraction(sum(Fraction(str(r["win_a"])) for r in recs("V1", "V2")), rg.N)
        v2 = Fraction(sum(Fraction(str(r["win_a"])) for r in recs("V2", "V1")), rg.N)
        assert v1 == Fraction(37, 96)
        assert v2 == Fraction(9, 16)
        assert (Fraction(1) - v1 + v2) / 2 == Fraction(113, 192)

        # V2 detection: every bluff-RECEIVING position puts all mass on B
        for la, lb in (("V2", "V2"), ("V1", "V2"), ("V2", "V1")):
            for r in recs(la, lb):
                if r["b_bluffed"] and la == "V2":  # a receives b's bluff
                    post = r["post_a_on_b"]
                    assert post and all(v in B12 for v in post)
                if r["a_bluffed"] and lb == "V2":  # b receives a's bluff
                    post = r["post_b_on_a"]
                    assert post and all(v in B12 for v in post)


_ANALYTIC_CACHE: dict[str, float] = {}


def _analytic(scope: str = "full") -> float:
    if scope not in _ANALYTIC_CACHE:
        _ANALYTIC_CACHE[scope] = rg.analytic_leakage(B12, scope)
    return _ANALYTIC_CACHE[scope]


class TestLeakageMachinery:
    def test_mi_exact_deterministic_line(self):
        # I(x; H(x)-line) = H(M) when the line is a function of x
        joint: dict = {}
        xc: dict[int, int] = {}
        for xa in range(1, rg.N + 1):
            xc[xa] = 1
            joint[(xa, rg.honest_window(xa))] = 1
        # I(x; M) = H(M) when M = f(x); H(M) from the actual window counts
        m_counts: dict = {}
        for (_x, m), c in joint.items():
            m_counts[m] = m_counts.get(m, 0) + c
        h_m = -sum((c / 48) * math.log2(c / 48) for c in m_counts.values() if c)
        assert abs(rg._mi_exact(joint, xc, 48) - h_m) < 1e-9

    def test_posterior_leakage_bounds(self):
        rng = random.Random(5103)
        samples = [
            rg.simulate_pair(
                rng.randrange(1, rg.N + 1), rng.randrange(1, rg.N + 1), "V2", "V2", B12, rg.episode_draws(rng)
            )
            for _ in range(300)
        ]
        mi = rg.posterior_leakage_bits(samples, B12)
        an = _analytic("full")
        assert abs(mi - an) < 0.2  # 300-sample concentration (full gate uses 5000/0.05)
        assert 0 < mi <= math.log2(rg.N)

    def test_analytic_leakage_frozen_values(self):
        assert abs(_analytic("full") - 4.670537) < 1e-4
        assert abs(_analytic("own") - 4.5787) < 1e-3
