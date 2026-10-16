"""E5.2 "The Range Game" (competitive; RQ1+RQ2 under incentive).

Pre-registered in ``plan/30-phases/phase-5-multi-agent/experiments.md``;
verdict + deviations in ``.../results.md``.

The game (frozen design)
------------------------
Two agents ``a``, ``b``; each holds a secret integer in ``1..N`` (N=48,
seeded). Protocol (common knowledge, declared to both):

* R1 (a then b) — ONE claim about the OWN value: a canonical window of
  width W=8 (windows = starts 1..41). Players whose value is in the
  declared deceiver set B BLUFF: one of the K=4 canonical windows
  farthest from the value (uniform seeded draw — always disjoint from
  the value, so the claim is genuinely false). Others announce the
  honest window H(x) (the unique width-8 window containing x, most
  centred).
* R2 (a then b) — ONE claim about one's ESTIMATE of the other's value:
  the width-8 canonical window centred on the posterior E|·|-median
  after the other's R1. Deceivers instead announce one of the K windows
  farthest from their true estimate window (uniform seeded draw — a
  false claim about their own belief).
* COMMIT — each commits an integer estimate of the other's number,
  after the full transcript. Errors e_t = |est_t − x_other|; the
  smaller takes the pot (1.0/0.0; tie 0.5).

The V-ablation (equal lines, equal budgets — only the commit differs)
----------------------------------------------------------------------
* **V0** — no ToM slots; frozen zero-information commit: the
  unique-smallest E|·|-optimal of the uniform prior (24).
* **V1** — ``model_other_beliefs``: exact Bayes posterior conditioning
  on R1 claims only (the declared belief model: honest outside B,
  K-way random bluffer inside B, B declared). Commit = E|·|-median.
* **V2** — ``model_other_state``: exact Bayes posterior conditioning on
  the FULL transcript. A deceiver's R2 claim draws from a value-
  dependent set, so the joint line (W1, W2) identifies values that R1
  alone leaves mixed.

Deceiver set (derived constant, frozen at pre-registration)
-----------------------------------------------------------
B* = the fixed point of bluff-profitability, started from ALL 48 (the
maximal-deception profile — the spec's "incentive-rewarded" framing):
  B_{t+1} = { x : W_bluff(x) > W_honest(x)  (against the receiver class,
               with B_t declared) }
evaluated as best responses (the sender deviates; the receiver models
the declared profile). The game then declares B = B*(V2) — bluffing is
kept only where it pays against the STRONGEST declared receiver
(maximin-consistent). The optimal bluffing frequency = |B|/N; the
filing's target is 12/48 — the frozen METHOD produces the frozen VALUE,
recorded in experiments.md before the official run (mismatch vs 12 →
deviation, as per house rule for derived constants).

Exactness: all posteriors are integer-weighted distributions over the
48 values (no floats in any decision); derived quantities are exact
rationals; floats appear only in reported percentages and 2-decimal MI
(500-sample leakage uses exact counts; the analytic joint is enumerated
exactly).
"""

from __future__ import annotations

import random
from fractions import Fraction

N = 48
W = 8
K = 4
WINDOW_STARTS = tuple(range(1, N - W + 2))  # 1..41 inclusive (last window (41,48))


def windows() -> tuple[tuple[int, int], ...]:
    return tuple((s, s + W - 1) for s in WINDOW_STARTS)


def _honest_window_raw(x: int) -> tuple[int, int]:
    s = max(1, min(x - W // 2, N - W + 1))
    return (s, s + W - 1)


def _gap(x: int, win: tuple[int, int]) -> int:
    lo, hi = win
    if hi < x:
        return x - hi
    if lo > x:
        return lo - x
    return 0


def _bluff_windows_raw(x: int) -> tuple[tuple[int, int], ...]:
    ordered = sorted(
        (w for w in windows() if _gap(x, w) > 0),
        key=lambda w: (-_gap(x, w), w[0]),
    )
    if len(ordered) < K:
        raise ValueError("not enough disjoint windows for a bluff")
    return tuple(ordered[:K])


def _farset_raw(win: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    centre = (win[0] + win[1]) / 2
    ordered = sorted(
        windows(),
        key=lambda w: (-(abs((w[0] + w[1]) / 2 - centre)), (w[0], w[1])),
    )
    return tuple(ordered[:K])


# Precomputed tables (independent of the deceiver set) + per-B caches.
_H_TABLE = {v: _honest_window_raw(v) for v in range(1, N + 1)}
_F_TABLE = {v: _bluff_windows_raw(v) for v in range(1, N + 1)}
_FAR_TABLE = {w: _farset_raw(w) for w in windows()}
_PR1_CACHE: dict[tuple[frozenset[int], tuple[int, int]], dict[int, int]] = {}
_PRHO_CACHE: dict[tuple[int, int, tuple[int, int]], dict[int, int]] = {}

_PF_CACHE: dict[
    tuple[frozenset[int], tuple[int, int], tuple[int, int], tuple[int, int]],
    dict[int, int],
] = {}
# Uniform-prior fallback (only reachable in best-response evaluations at
# profile boundaries, e.g. B = all with an honest deviation). Must be 0
# in the official run; the bench reports FALLBACK_USES.
FALLBACK_USES = 0
_UNIFORM = {v: 1 for v in range(1, N + 1)}


def honest_window(x: int) -> tuple[int, int]:
    return _H_TABLE[x]


def bluff_windows(x: int) -> tuple[tuple[int, int], ...]:
    return _F_TABLE[x]


def _farset_of_window(win: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    return _FAR_TABLE[win]


# ── R1 claim ───────────────────────────────────────────────────────────────


def r1_window(x: int, in_B: bool, draw: int | None) -> tuple[int, int]:
    if in_B:
        assert draw is not None
        return bluff_windows(x)[draw]
    return honest_window(x)


# ── exact posteriors ───────────────────────────────────────────────────────


def posterior_r1(r1_sender: tuple[int, int], B: frozenset[int]) -> dict[int, int]:
    """P(v | r1_sender) — integer weights, scale ×48K.

    v ∉ B: lik 1[W == H(v)]  → weight K.
    v ∈ B: lik 1[W ∈ F(v)]/K → weight 1.
    EMPTY result = the declared profile cannot explain the claim;
    callers fall back to the uniform prior (see FALLBACK_USES).
    """
    key = (B, r1_sender)
    hit = _PR1_CACHE.get(key)
    if hit is not None:
        return hit
    w: dict[int, int] = {}
    for v in range(1, N + 1):
        if v in B:
            if r1_sender in bluff_windows(v):
                w[v] = 1
        elif honest_window(v) == r1_sender:
            w[v] = K
    _PR1_CACHE[key] = w
    return w


def posterior_full(
    r1_sender: tuple[int, int],
    r2_sender: tuple[int, int],
    r1_receiver: tuple[int, int],
    B: frozenset[int],
) -> dict[int, int]:
    """P(v | full transcript) from the RECEIVER's side — scale ×48K².

    The sender's TRUE estimate window is a function of the RECEIVER's
    own R1 (r1_receiver): the sender estimated MY value from my claim.
    honest: r1_sender == H(v) and r2_sender == D (weight K²);
    bluff:  r1_sender ∈ F(v) and r2_sender ∈ far(D) (weight 1).
    """
    key = (B, r1_sender, r2_sender, r1_receiver)
    hit = _PF_CACHE.get(key)
    if hit is not None:
        return hit
    declared = declared_r2_window(r1_receiver, B)
    far = _farset_of_window(declared)
    w: dict[int, int] = {}
    for v in range(1, N + 1):
        if v in B:
            if r1_sender in bluff_windows(v) and r2_sender in far:
                w[v] = 1
        else:
            if honest_window(v) == r1_sender and r2_sender == declared:
                w[v] = K * K
    _PF_CACHE[key] = w
    return w


# ── the stochastic-liar model (e5.3: rate-parameterized, no deceiver set) ──


def posterior_r1_rho(r1_sender: tuple[int, int], p: int, q: int) -> dict[int, int]:
    """P(v | W, rate p/q) — the e5.3 stochastic-liar posterior, integer
    weights: w(v) = (q-p)·K·[W = H(v)] + p·[W ∈ F(v)] — every value may
    bluff with prob p/q (uniform over its K farthest windows — the 1/K
    likelihood of e5.2, kept as the K ratio against honest weight K).
    The two terms are disjoint per value (a window containing v cannot
    be a far window of v). NEVER empty: every window is the unique
    centred honest window of some values (edge windows 4–5, interior 1).
    This generalizes e5.2's declared-regime weights (K vs 1 over B):
    with p/q the regime frequency and per-value determinism it is the
    same likelihood structure."""
    key = (p, q, r1_sender)
    hit = _PRHO_CACHE.get(key)
    if hit is not None:
        return hit
    w: dict[int, int] = {}
    for v in range(1, N + 1):
        wt = 0
        if honest_window(v) == r1_sender:
            wt += (q - p) * K
        if r1_sender in bluff_windows(v):
            wt += p
        if wt:
            w[v] = wt
    _PRHO_CACHE[key] = w
    return w


def commit_r1_rho(r1_sender: tuple[int, int], p: int, q: int) -> int:
    """The V1-level commit against a rate-p/q sender (R1-only)."""
    return est_median(posterior_r1_rho(r1_sender, p, q))


def branch_mass(r1_sender: tuple[int, int], p: int, q: int) -> Fraction:
    """f(ρ, W) — the bluffer-branch mass fraction of the R1 posterior at
    rate p/q: total weight of values consistent with a BLUFF / total
    weight. Exact rational (the e5.3 calibration metric). At p=0 this
    is 0 for every claim (the bluffer branch vanishes)."""
    w = posterior_r1_rho(r1_sender, p, q)
    bluff = sum(wt for v, wt in w.items() if r1_sender in bluff_windows(v))
    tot = sum(w.values())
    return Fraction(bluff, tot) if tot else Fraction(0)


def est_median(w: dict[int, int]) -> int:
    """Smallest value minimising E|est − V| under integer weights."""
    if not w:
        raise ValueError("empty posterior")
    best: tuple[int, int] | None = None
    for cand in range(1, N + 1):
        cost = sum(abs(cand - v) * wt for v, wt in w.items())
        if best is None or (cost, cand) < best:
            best = (cost, cand)
    assert best is not None
    return best[1]


def declared_r2_window(r1_of_other: tuple[int, int], B: frozenset[int]) -> tuple[int, int]:
    """The honest R2 window for a player whose posterior over the other's
    value rests on the other's R1 claim (the declared function of the R1
    round — both R2 players use it with their own observation)."""
    global FALLBACK_USES
    w = posterior_r1(r1_of_other, B)
    if not w:
        FALLBACK_USES += 1
        return honest_window(est_median(_UNIFORM))
    return honest_window(est_median(w))


def commit_estimate(
    level: str,
    r1_sender: tuple[int, int],
    r2_sender: tuple[int, int],
    r1_receiver: tuple[int, int],
    B: frozenset[int],
) -> int:
    """The commit of a `level` agent estimating the SENDER's value from
    the transcript (R1,R2 of sender + own R1; own R2 cannot precede it)."""
    global FALLBACK_USES
    if level == "V0":
        return est_median(_UNIFORM)
    if level == "V1":
        w = posterior_r1(r1_sender, B)
    else:  # V2
        w = posterior_full(r1_sender, r2_sender, r1_receiver, B)
    if not w:
        FALLBACK_USES += 1
        return est_median(_UNIFORM)
    return est_median(w)


# ── the deceiver set: exact fixed point, started from ALL ─────────────────


def expected_win(
    x: int,
    deviate_bluff: bool,
    receiver: str,
    B: frozenset[int],
) -> Fraction:
    """Player a at value x deviating (bluff iff `deviate_bluff`), co-player
    b following the declared profile (bluffs iff x_b in B); both commit by
    the `receiver`-class policy. Exact expected win over the full finite
    space: x_b (48) x b's two draws (1/K each) x a's two own draws (1/K
    each when deviating). b models the declared profile against the
    OBSERVED a-line; nobody knows about the deviation. R2 protocol: each
    R2 claim is the declared function of the R1 round (the sender's true
    estimate window), so ordering inside R2 is protocol-invariant."""
    num = Fraction(0)
    den = 0
    for xb in range(1, N + 1):
        b_in_B = xb in B
        for bd1 in range(K if b_in_B else 1):
            b_r1 = r1_window(xb, b_in_B, bd1 if b_in_B else None)
            for ad1 in range(K if deviate_bluff else 1):
                a_r1 = bluff_windows(x)[ad1] if deviate_bluff else honest_window(x)
                # b's declared R2 window: b's estimate of a's value from
                # a's claim, modelling the declared profile on the
                # OBSERVED a_r1.
                b_decl = declared_r2_window(a_r1, B)
                for bd2 in range(K if b_in_B else 1):
                    b_r2 = (
                        _farset_of_window(b_decl)[bd2] if b_in_B else b_decl
                    )
                    for ad2 in range(K if deviate_bluff else 1):
                        a_decl = declared_r2_window(b_r1, B)
                        a_r2 = (
                            _farset_of_window(a_decl)[ad2]
                            if deviate_bluff
                            else a_decl
                        )
                        est_a_of_b = commit_estimate(receiver, b_r1, b_r2, a_r1, B)
                        est_b_of_a = commit_estimate(receiver, a_r1, a_r2, b_r1, B)
                        e_a = abs(est_a_of_b - xb)
                        e_b = abs(est_b_of_a - x)
                        if e_a < e_b:
                            num += 1
                        elif e_a == e_b:
                            num += Fraction(1, 2)
                        den += 1
    return num / den


def derive_deceiver_set(
    receiver: str,
    start: str = "all",
    iters: int = 64,
) -> frozenset[int]:
    """Fixed point of bluff-profitability (best responses, declared B)."""
    B: frozenset[int] = (
        frozenset(range(1, N + 1)) if start == "all" else frozenset()
    )
    for _ in range(iters):
        nxt: set[int] = set()
        for x in range(1, N + 1):
            w_b = expected_win(x, True, receiver, B)
            w_h = expected_win(x, False, receiver, B)
            if w_b > w_h:
                nxt.add(x)
        newB = frozenset(nxt)
        if newB == B:
            return B
        B = newB
    raise RuntimeError("deceiver set did not stabilise")


# ── episode simulation (shared by the offline derivation and the bench) ──


def simulate_pair(
    xa: int,
    xb: int,
    level_a: str,
    level_b: str,
    B: frozenset[int],
    draws: tuple[int, int, int, int],
) -> dict:
    """One full episode under the declared protocol. Draw order is fixed:
    (b_r1_draw, a_r1_draw, a_r2_draw, b_r2_draw) — a draw is consumed by
    that claim only when the sender bluffs (value in B)."""
    a_in_B = xa in B
    b_in_B = xb in B
    b_r1 = r1_window(xb, b_in_B, draws[0] if b_in_B else None)
    a_r1 = r1_window(xa, a_in_B, draws[1] if a_in_B else None)
    a_decl = declared_r2_window(b_r1, B)
    a_r2 = _farset_of_window(a_decl)[draws[2]] if a_in_B else a_decl
    b_decl = declared_r2_window(a_r1, B)
    b_r2 = _farset_of_window(b_decl)[draws[3]] if b_in_B else b_decl
    est_a_of_b = commit_estimate(level_a, b_r1, b_r2, a_r1, B)
    est_b_of_a = commit_estimate(level_b, a_r1, a_r2, b_r1, B)
    e_a = abs(est_a_of_b - xb)
    e_b = abs(est_b_of_a - xa)
    win_a = 1.0 if e_a < e_b else (0.5 if e_a == e_b else 0.0)
    return {
        "xa": xa, "xb": xb,
        "line_a": (a_r1, a_r2), "line_b": (b_r1, b_r2),
        "a_bluffed": a_in_B, "b_bluffed": b_in_B,
        "est_a_of_b": est_a_of_b, "est_b_of_a": est_b_of_a,
        "e_a": e_a, "e_b": e_b, "win_a": win_a,
        # exact posteriors used by the commits (for audit/accuracy checks):
        "post_b_on_a": (
            posterior_r1(a_r1, B) if level_b == "V1"
            else posterior_full(a_r1, a_r2, b_r1, B)
        ) if level_b in ("V1", "V2") else None,
        "post_a_on_b": (
            posterior_r1(b_r1, B) if level_a == "V1"
            else posterior_full(b_r1, b_r2, a_r1, B)
        ) if level_a in ("V1", "V2") else None,
    }


def balanced_pairs(seed: int, n: int = N) -> list[tuple[int, int]]:
    """48 episodes: a's value = i (each value exactly once), b's value a
    seeded permutation — so any per-value frequency is exactly
    measurable (e.g. bluff usage |B|/48)."""
    import random

    rng = random.Random(seed)
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    return [(i, perm[i - 1]) for i in range(1, n + 1)]


def episode_draws(rng: random.Random) -> tuple[int, int, int, int]:
    return (
        rng.randrange(K), rng.randrange(K), rng.randrange(K), rng.randrange(K)
    )


def incentive_margins(
    receiver: str, B: frozenset[int]
) -> tuple[dict[int, Fraction], int]:
    """Exact per-value deviation margins at the DECLARED set B against the
    `receiver` class: margin(x) = W_bluff(x) − W_honest(x) (best-response
    deviations; the receiver models the declared B). Returns
    ({x: margin}, count of profitable deviations)."""
    margins: dict[int, Fraction] = {}
    profitable = 0
    for x in range(1, N + 1):
        w_b = expected_win(x, True, receiver, B)
        w_h = expected_win(x, False, receiver, B)
        margins[x] = w_b - w_h
        if w_b > w_h:
            profitable += 1
    return margins, profitable


def empirical_leakage(samples: list[dict], scope: str = "own") -> float:
    """Leakage in bits, exact counts. scope 'own': I(x_a; a's own R1,R2);
    scope 'full': I(x_a; the full public transcript of both sides)."""
    joint: dict = {}
    x_counts: dict[int, int] = {}
    for s_ in samples:
        m: tuple
        if scope == "own":
            m = (s_["line_a"][0], s_["line_a"][1])
        elif scope == "full":
            m = (s_["line_a"][0], s_["line_b"][0], s_["line_a"][1], s_["line_b"][1])
        else:
            raise ValueError(scope)
        key = (s_["xa"], *m)
        joint[key] = joint.get(key, 0) + 1
        x_counts[s_["xa"]] = x_counts.get(s_["xa"], 0) + 1
    return _mi_exact(joint, x_counts, sum(x_counts.values()))


def _mm_bits(n: int, distinct: int) -> float:
    """Miller-Madow first-order bias for a Shannon entropy estimate in
    bits, sample size n, observed alphabet size `distinct`."""
    import math

    if n <= 0 or distinct <= 1:
        return 0.0
    return (distinct - 1) / (2 * n * math.log(2))


def empirical_leakage_mm(samples: list[dict], scope: str = "own") -> float:
    """Miller-Madow bias-corrected leakage (same scopes as
    :func:`empirical_leakage`). The raw plug-in estimate is biased UP on
    this sparse message space (48 values × up to 41² windows); the
    first-order correction is computed exactly from the counts."""
    joint: dict = {}
    x_counts: dict[int, int] = {}
    for s_ in samples:
        m = (
            (s_["line_a"][0], s_["line_a"][1])
            if scope == "own"
            else (s_["line_a"][0], s_["line_b"][0], s_["line_a"][1], s_["line_b"][1])
        )
        key = (s_["xa"], *m)
        joint[key] = joint.get(key, 0) + 1
        x_counts[s_["xa"]] = x_counts.get(s_["xa"], 0) + 1
    total = sum(x_counts.values())
    m_counts: dict = {}
    for (x, *m), c in joint.items():
        m_counts[tuple(m)] = m_counts.get(tuple(m), 0) + c
    return _mi_exact_mm(joint, x_counts, m_counts, total)


def _mi_exact_mm(joint: dict, x_counts: dict, m_counts: dict, total: int) -> float:
    import math

    # H(M) plug-in + MM
    h_m = -sum((c / total) * math.log2(c / total) for c in m_counts.values() if c)
    h_m += _mm_bits(total, len(m_counts))
    # H(M|X) = Σ_x P(x) [plug-in H(M|x) + MM_x]
    per_x: dict[int, list[int]] = {}
    for (x, *_m), c in joint.items():
        per_x.setdefault(x, []).append(c)
    h_mx = 0.0
    for x, counts in per_x.items():
        n_x = sum(counts)
        plug = -sum((c / n_x) * math.log2(c / n_x) for c in counts if c)
        h_mx += (n_x / total) * (plug + _mm_bits(n_x, len(counts)))
    return h_m - h_mx


def posterior_leakage_bits(samples: list[dict], B: frozenset[int]) -> float:
    """Exact rational-listener leakage: mean over samples of
    H(x_a) − H(posterior), where the posterior is the EXACT integer
    posterior over x_a from the observed full transcript of a (V2-level
    conditioning, the rational listener's computation). Unbiased — no
    cell-counting / plug-in bias — and exactly the information a
    rational listener with the declared protocol obtains."""
    import math

    tot = 0.0
    n = 0
    for s_ in samples:
        w = posterior_full(s_["line_a"][0], s_["line_a"][1], s_["line_b"][0], B)
        if not w:  # impossible under the declared model; defensive
            continue
        total = sum(w.values())
        h = -sum((c / total) * math.log2(c / total) for c in w.values())
        tot += math.log2(N) - h
        n += 1
    return tot / n


def analytic_leakage(B: frozenset[int], scope: str = "own") -> float:
    """Exact I(x_a; claims) over the full finite space: x_a x x_b x the
    four draws (b's value/draws integrated out by enumeration)."""
    samples = []
    for xa in range(1, N + 1):
        for xb in range(1, N + 1):
            for d1 in range(K):
                for d2 in range(K):
                    for d3 in range(K):
                        for d4 in range(K):
                            samples.append(
                                simulate_pair(
                                    xa, xb, "V2", "V2", B,
                                    (d1, d2, d3, d4),
                                )
                            )
    return empirical_leakage(samples, scope)


def _mi_exact(joint: dict, x_counts: dict, total: int) -> float:
    """I(X; M) = H(M) − H(M|X), exact from integer counts. Keys of
    `joint` are (x, m...) tuples; `x_counts` the marginal of x."""
    import math

    m_counts: dict = {}
    for (x, *m), c in joint.items():
        m_counts[tuple(m)] = m_counts.get(tuple(m), 0) + c
    h_m = -sum(
        (c / total) * math.log2(c / total) for c in m_counts.values() if c
    )
    h_m_given_x = -sum(
        (c / x_counts[x]) * math.log2(c / x_counts[x]) * (x_counts[x] / total)
        for (x, *_m), c in joint.items()
        if c
    )
    return h_m - h_m_given_x




def clear_caches() -> None:
    _PR1_CACHE.clear()
    _PRHO_CACHE.clear()
    _PF_CACHE.clear()
    global FALLBACK_USES
    FALLBACK_USES = 0


__all__ = [
    "FALLBACK_USES",
    "WINDOW_STARTS",
    "Fraction",
    "K",
    "N",
    "W",
    "analytic_leakage",
    "balanced_pairs",
    "bluff_windows",
    "branch_mass",
    "clear_caches",
    "commit_estimate",
    "commit_r1_rho",
    "declared_r2_window",
    "derive_deceiver_set",
    "empirical_leakage",
    "empirical_leakage_mm",
    "episode_draws",
    "est_median",
    "expected_win",
    "honest_window",
    "incentive_margins",
    "posterior_full",
    "posterior_leakage_bits",
    "posterior_r1",
    "posterior_r1_rho",
    "r1_window",
    "simulate_pair",
    "windows",
]
