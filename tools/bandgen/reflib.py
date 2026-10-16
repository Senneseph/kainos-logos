"""The reference registry (bandgen v0.1).

Beds are DECLARED as computations, never as hand-written values:
the spec names a reference function + args, and bandgen evaluates it
against the SAME python reference the experiments' P4 checks import
(brainstem's ``_s13_py_*`` / ``_s11_py_*`` family). One reference
implementation serves both the compiler and the referee — the
D-e6h(b) hand-computed-bed bug class cannot exist in a value that is
computed, not written.

The registry is open by design: each band adds its own reference
functions here (or in its brainstem module and registers them) as
the curriculum grows. v0.1 ships the S11/S12/S13 (fundamentals)
references needed to reproduce the S13 acceptance case.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from typing import Any

from kainos.tutor import brainstem as B


def _frac_words(v: Fraction) -> str:
    """The house word rendering (exactly the experiments' ``_frac``:
    '85 over 168'; integers render bare)."""
    return f"{v.numerator} over {v.denominator}" if v.denominator != 1 else str(v.numerator)


def _frac_slash(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}"


# --- S13 (the zeta variants) references --------------------------------

def ref_family(sign: int, indexset: str, exp: int, N: int = 84) -> Fraction:
    """A family partial: sign ±, index set all/primes/composites,
    exponent s, height N (the store's own python reference)."""
    return B._s13_py_family(sign, indexset, exp, N)


def ref_telescope(N: int) -> Fraction:
    """The telescope spot (N+1)/(2N) as an exact rational."""
    return B._s13_py_telescope(N)


def ref_removal(p: int, exp: int) -> Fraction:
    """The single-prime removal multiplier p^s / (p^s - 1)."""
    return B._s13_py_removal(p, exp)


def ref_removal_max(exp: int, N: int = 84) -> tuple[int, str]:
    """The largest removal multiplier on the line at s=exp, with the
    prime it stands at (the S13_BEDS 'removal_max_s2/s3' shape:
    (prime, word))."""
    best_p, best_v = 0, Fraction(0)
    for p in B._s13_py_primes(N):
        v = B._s13_py_removal(p, exp)
        if v > best_v:
            best_p, best_v = p, v
    return (best_p, _frac_words(best_v))


def ref_set_removal(primes: list[int], exp: int) -> Fraction:
    """The set-removal multiplier: the product of the single removals
    over the named primes (removing several terms multiplies by the
    product of their reciprocals' reciprocals — control: the bed
    cross-check catches a reciprocal product, D-e6h(b))."""
    acc = Fraction(1)
    for p in primes:
        acc *= B._s13_py_removal(p, exp)
    return acc


def ref_set_removal_map(sets: list[list[int]], exp: int) -> dict[str, str]:
    """The S13_BEDS 'set_removal_s2' shape: {'2,3': '3/2', ...} (slash
    rendering, comma-keyed)."""
    return {
        ",".join(str(p) for p in ps): _frac_slash(ref_set_removal(ps, exp)) for ps in sets
    }


def ref_census(end: int = 84) -> dict[str, int]:
    """The line census above one: integers / primes / composites
    (the S13_BEDS 'census' shape)."""
    ps = B._s13_py_primes(end)
    integers = end - 1
    return {"integers": integers, "primes": len(ps), "composites": integers - len(ps)}


def ref_removal_below2_count(exp: int, N: int = 84) -> int:
    """How many single-removal multipliers on the line stay below 2
    (every one of them does at s=2 — the S13_BEDS count shape)."""
    return sum(1 for p in B._s13_py_primes(N) if B._s13_py_removal(p, exp) < 2)


def ref_telescope_spots(heights: list[int]) -> dict[str, str]:
    """The named telescope spots as {str(N): 'a/b'} (slash rendering,
    the S13_BEDS 'telescope_spots' shape)."""
    return {str(N): _frac_slash(B._s13_py_telescope(N)) for N in heights}


def ref_telescope_named(heights: list[int]) -> tuple[str, ...]:
    """The named-spot values in the given order (the S13_BEDS
    'telescope_named_spots' tuple shape)."""
    return tuple(_frac_slash(B._s13_py_telescope(N)) for N in heights)


def ref_spf_chain(n: int) -> list[int]:
    """The smallest-prime-factor chain (the S11 reference)."""
    return B._s11_py_chain(n)


def ref_spf(n: int) -> int:
    return B._s11_py_spf(n)


def ref_order_s2() -> list[str]:
    """The frozen s=2 ordering of the six family partials (declared
    content, but it is the order the mechanism's own values sort to —
    kept as a reference so the compiler can re-verify it)."""
    vals = {
        "minus-all": B._s13_py_family(-1, "all", 2),
        "minus-prime": B._s13_py_family(-1, "primes", 2),
        "minus-comp": B._s13_py_family(-1, "comp", 2),
        "plus-comp": B._s13_py_family(1, "comp", 2),
        "plus-prime": B._s13_py_family(1, "primes", 2),
        "plus-all": B._s13_py_family(1, "all", 2),
    }
    return [k for k, _ in sorted(vals.items(), key=lambda kv: kv[1])]


# --- S14 (the elliptic city — BSD island band 1) references ------------

_PANELS = {"A": "B14_A", "B": "B14_B"}


def _panel_args(panel: str) -> tuple[int, int, int]:
    return getattr(B, _PANELS.get(panel, ""), (0, 0, 0))


def ref_ap_table(panel: str, end: int = 84) -> list[str]:
    """The a_p census over the line's primes for the named panel
    (A = 32.a3, B = 37.a1; the S14_BEDS 'ap_A'/'ap_B' shape)."""
    a3, a, b = _panel_args(panel)
    return [str(B._bsd_py_ap(p, a3, a, b)) for p in B._s13_py_primes(end)]


def ref_fp_count(p: int, panel: str) -> int:
    """#E(F_p) for the named panel at the prime p."""
    a3, a, b = _panel_args(panel)
    return B._bsd_py_count(p, a3, a, b)


def ref_cm_zeros(panel: str, end: int = 84) -> list[int]:
    """The primes of the line where the panel's a_p is zero (the CM
    signature set for A; empty for B)."""
    a3, a, b = _panel_args(panel)
    return [p for p in B._s13_py_primes(end) if B._bsd_py_ap(p, a3, a, b) == 0]


def ref_small_points() -> list[list[int]]:
    """The on-line small points of panel B (|x|,|y| <= the line end;
    the S14_BEDS 'small_B' table — declared from the verified
    research record and re-verified by the e618 bed budget against
    an independent on-curve scan)."""
    return [list(pt) for pt in B.S14_BEDS["small_B"]]


def ref_gen_ledger() -> dict[str, int]:
    """The mP generation ledger for B's generator (the S14_BEDS
    'gen_B' table; re-verified by the e618 bed budget with the
    mechanism's own _bsd_py_mul)."""
    return dict(B.S14_BEDS["gen_B"])


def ref_lpartial(panel: str, end: int = 84) -> Fraction:
    """The panel's L partial product at the line end (exact rational)."""
    a3, a, b = _panel_args(panel)
    return B._bsd_py_Lpartial(a3, a, b, end)


# --- S15 (the L-function of the city — BSD island band 2) references ---

def ref_lfactor(p: int, panel: str, form: str = "uniform") -> Fraction:
    """The factor the prime p carries for the named panel: the uniform
    two-term form (every prime) or the record form (one term at the
    ramified conductor primes 2 / 37)."""
    a3, a, b = _panel_args(panel)
    return B._bsd_py_lfactor(p, a3, a, b, form)


def ref_lpartial_uniform(h: int, panel: str) -> Fraction:
    """The uniform L partial up to height h (product over primes <= h)."""
    a3, a, b = _panel_args(panel)
    return B._bsd_py_lpartial_uniform(a3, a, b, end=h)


def ref_lpartial_record(h: int, panel: str) -> Fraction:
    """The RECORD L partial up to height h (one-term form at the
    ramified primes)."""
    a3, a, b = _panel_args(panel)
    return B._bsd_py_lpartial_record(a3, a, b, end=h)


def ref_lcorr(panel: str, end: int = 84) -> Fraction:
    """The product of the ramification corrections R_p/U_p at the
    ramified primes of the named panel (4/5 for A; 1406/1407 for B)."""
    a3, a, b = _panel_args(panel)
    return B._bsd_py_lcorr(a3, a, b, end)


def ref_ramified_pair(panel: str) -> dict[str, str]:
    """The ramified factor pair (uniform -> record) for the named
    panel (A: 5/4 -> 1; B: 1407/1369 -> 38/37), slash-rendered so
    the bed value is JSON-stable (the referee re-derives the
    Fractions through _bsd_py_lfactor either way)."""
    a3, a, b = _panel_args(panel)
    p = 2 if (a3, a, b) == B.B14_A else 37
    return {
        "uniform": _frac_slash(B._bsd_py_lfactor(p, a3, a, b, "uniform")),
        "record": _frac_slash(B._bsd_py_lfactor(p, a3, a, b, "record")),
    }



# ------------------------------------------------------------------
# S16 (E6.20) references — the descent and the reaching. The answer
# bytes mirror _policy_savant16 exactly (control c2 is the referee).
def _s16_frac_words(v) -> str:
    from fractions import Fraction as _F
    v = _F(v) if not isinstance(v, _F) else v
    sign = "minus " if v < 0 else ""
    v = abs(v)
    if v.denominator == 1:
        return f"{sign}{v.numerator}"
    return f"{sign}{v.numerator} over {v.denominator}"


def ref_s16_order(panel: str, end: int = 84) -> str:
    a3, a, b = _panel_args(panel)
    w = "A" if (a3, a, b) == B.B14_A else "B"
    u = B._bsd_py_lpartial_uniform(a3, a, b, end)
    pname = "the first panel member" if w == "A" else "the second panel member"
    if w == "A":
        return (f"of record, the L product of {pname} is nonzero at s equal to one — order zero of vanishing — "
                f"and on my line the exact partial {_s16_frac_words(u)} stands nonzero for the line's side, at the line end {end}")
    return (f"of record, the L product of {pname} vanishes at s equal to one, of order one — and on my line "
            f"the exact partial {_s16_frac_words(u)} stands far from zero for the line's side (the vanishing is the divergence "
            f"of the infinite product past the line), at the line end {end}")


def ref_s16_rank(panel: str, end: int = 84) -> str:
    w = panel
    if w == "A":
        return (f"of record, the algebraic rank of the first panel member is zero — settled by the two-descent: the selmer "
                f"dimension two against its two-torsion dimension two, the descent bound zero, met by the torsion ledger "
                f"(its three torsion points, no generator); no B S D is used, at the line end {end}")
    return (f"of record, the algebraic rank of the second panel member is one — settled by the two-descent: the selmer "
            f"dimension one against its two-torsion dimension zero, the descent bound one, met by the generator "
            f"(x zero y zero) of record, on my line; no B S D is used, at the line end {end}")


def ref_s16_descend(panel: str, end: int = 84) -> str:
    if panel == "A":
        return (f"for the first panel member, the descent bound is the selmer dimension two minus the two-torsion "
                f"dimension two — zero — and the point ledger holds only its three torsion points (x zero y zero, x one "
                f"y zero, x minus one y zero), so the rank is zero, settled, at the line end {end}")
    return (f"for the second panel member, the descent bound is the selmer dimension one minus the two-torsion "
            f"dimension zero — one — and the generator (x zero y zero) of record, on my line, meets it (the rank is at "
            f"least one), so the rank is one, settled, at the line end {end}")


def ref_s16_selmer(panel: str, end: int = 84) -> str:
    if panel == "A":
        return (f"of record, two: the rank zero plus the two-torsion dimension two plus the two-shaf dimension zero "
                f"(the shaf is trivial of record on both members), at the line end {end}")
    return (f"of record, one: the rank one plus the two-torsion dimension zero plus the two-shaf dimension zero "
            f"(the shaf is trivial of record on both members), at the line end {end}")


def ref_s16_torsion(end: int = 84) -> str:
    return ("the torsion ledger of the first panel member holds its three integral two-torsion points on my line — "
            "(x zero y zero), (x one y zero), (x minus one y zero) — the full two-torsion of record (z/2 squared), "
            f"and nothing else on the line, at the line end {end}")


def ref_s16_gen(end: int = 84) -> str:
    return ("the generation ledger of the second panel member holds the generator (x zero y zero) of record, and "
            "every point my line counted is a small multiple of it — ten of ten of the ledger, closed on the line, "
            f"at the line end {end}")


def ref_s16_consistent(end: int = 84) -> str:
    uA = B._bsd_py_lpartial_uniform(*B.B14_A, end)
    uB = B._bsd_py_lpartial_uniform(*B.B14_B, end)
    return (f"yes — on my line: the first member's exact uniform partial {_s16_frac_words(uA)} stands nonzero, consistent with "
            f"the record's order zero, and the second member's exact partial {_s16_frac_words(uB)} stands far from zero at the "
            f"line end, consistent with the record's order one (the vanishing is the divergence of the infinite product "
            f"past the line), at the line end {end}")


def ref_s16_reach(end: int = 84) -> str:
    uA = B._bsd_py_lpartial_uniform(*B.B14_A, end)
    uB = B._bsd_py_lpartial_uniform(*B.B14_B, end)
    rB = B._bsd_py_lpartial_record(*B.B14_B, end)
    return (f"the line holds toward the summit: the exact partials (the first member's uniform partial {_s16_frac_words(uA)} holds "
            f"nonzero, the second member's uniform partial {_s16_frac_words(uB)} and record partial {_s16_frac_words(rB)} stand far from "
            f"zero), the torsion ledger of the first member (its three integral two-torsion points on the line — x zero "
            f"y zero, x one y zero, x minus one y zero), and the generation ledger of the second member (the generator "
            f"(x zero y zero), and every point my line counted is a small multiple of it — ten of ten), at the line end {end}")


def ref_s16_bsd(end: int = 84) -> str:
    return ("the summit of the island is the statement itself — held in my store as a declared record fact (the "
            "clay millennial booklet, the wiles chapter): the order of vanishing of the L product at s equal to one "
            "equals the algebraic rank — and on my panel the two sides are settled of record and they agree: order "
            "zero equals rank zero for the first member, and order one equals rank one for the second, "
            f"at the line end {end}")


def ref_s16_sides(panel: str, end: int = 84) -> str:
    words = {0: "zero", 1: "one"}
    o, r = B.S16_BEDS["order"][panel], B.S16_BEDS["rank"][panel]
    pname = "the first panel member" if panel == "A" else "the second panel member"
    return (f"for {pname}, the analytic side is the order {words[o]} of vanishing of record, the algebraic side is "
            f"the rank {words[r]} of record — the order {words[o]} equals the rank {words[r]}, at the line end {end}")


def ref_s16_bandstate(end: int = 84) -> str:
    return ("the summit band holds the statement itself, stored as a declared record fact (the clay millennial "
            "booklet, the wiles chapter), with its satisfaction on the panel of record — order zero equals rank zero "
            "for the first member, order one equals rank one for the second — and the line's side standing: the "
            "two-descent exact sequence and descent bounds, the exact partials consistent with both orders — the "
            "island's summit filed, the island closed, "
            f"at the line end {end}")


def ref_s16_uncond(end: int = 84) -> str:
    return ("nothing the summit band says is conditional on the Riemann hypothesis — the two-descent, the exact "
            "sequence, the selmer census, and the statement of record are unconditional mathematics on my panel, and "
            "the record's values (the L values, the leading coefficient) stand named of record on their walls, "
            f"at the line end {end}")


def ref_s16_wall(wall: str) -> str:
    """The wall bytes (needs_info: <wall text>): W1 the descent of
    record, W2 the L-value of record, W3 the panel's completeness."""
    w = getattr(B.Brainstem, f"W_S16_{wall}")
    return f"needs_info: {w}"





# ── S17 (E6.21, the Beal island) — the valuation-line beds ─────────────

def ref_s17_vp(n: str, p: str, end: int = 84) -> str:
    N = B._S17_NUM_WORD[n]
    P = B._S17_P_WORD[p]
    depth = B._beal_py_v_p(N, P)
    assert depth == B.S17_BEDS["vp"][(N, P)], "the valuation bed drifted"
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    return (f"the p-adic depth of {n} at the prime {p} of record is {words[depth]} — read off "
            f"the {p}-rung of the first-divisor factorization chain of {n}, at the line end {end}")


def ref_s17_lte(which: str, end: int = 84) -> str:
    x, y = (4, 1) if which == "a" else (10, 1)
    p, n = 3, 3
    vm = B._beal_py_v_p(x - y, p)
    vn = B._beal_py_v_p(n, p)
    vt = B._beal_py_v_p(x ** n - y ** n, p)
    assert vt == vm + vn, "the lte bed drifted"
    words = {1: "one", 2: "two", 3: "three"}
    if which == "a":
        lhs = "four cubed minus one cubed — sixty-three — holds two of the three-rung"
    else:
        lhs = "ten cubed minus one cubed — nine hundred and ninety-nine — holds three of the three-rung"
    return (f"it holds: {lhs}, while the difference {x - y} holds {words[vm]} of the three-rung and the exponent "
            f"three holds {words[vn]} of it — {words[vm]} plus {words[vn]} is {words[vt]} — the depth of the "
            f"difference plus the depth of the exponent, at the line end {end}")


def ref_s17_lte_ledger(end: int = 84) -> str:
    assert (B.S17_BEDS["lte_instances"], B.S17_BEDS["lte_failures"]) == (249280, 0), "the lte ledger drifted"
    return (f"two hundred forty-nine thousand two hundred eighty of record: the odd primes at or below my line end, "
            f"the difference a multiple of the prime with neither term divisible by it, the exponents three through "
            f"the line end — every one holds: zero deviations, at the line end {end}")


def ref_s17_beal(end: int = 84) -> str:
    return (f"the statement of record, as the ams beal prize holds it: if a to the x power plus b to the y power "
            f"equals c to the z power, with a, b, c, x, y and z positive and x, y and z each above two, then "
            f"a, b and c have a common prime factor — no pairwise coprime solution exists once every exponent is "
            f"above two, at the line end {end}")


def ref_s17_census(end: int = 84) -> str:
    assert B.S17_BEDS["census_count"] == B._beal_py_census()[0] == 83, "the census bed drifted"
    return (f"eighty-three triples in the box — a, b, c at or below my line end, the exponents between three and "
            f"ten of record — and every one of the eighty-three carries its common prime factor: no primitive "
            f"triple in the box, at the line end {end}")


def ref_s17_empt(end: int = 84) -> str:
    assert B.S17_BEDS["primitive_count"] == B._beal_py_census()[1] == 0, "the primitive census drifted"
    return (f"zero — no primitive triple lives on my line; the line ends where the primitive triples would live, "
            f"and that territory is a wall, at the line end {end}")


def ref_s17_family(end: int = 84) -> str:
    rows = B.S17_BEDS["census"]
    twos = sum(1 for r in rows if r[6] == 2)
    odds = len(rows) - twos
    return (f"the two-power twins (two to the n plus two to the n equals two to the n plus one), the three-family "
            f"(three cubed plus six cubed equals three to the fifth), the seven-family (seven cubed plus seven to "
            f"the fourth equals fourteen cubed), the fifteen-family (fifteen to the fourth plus fifteen to the "
            f"fifth equals thirty to the fourth), and the seventeen, nineteen, twenty-six, twenty-eight, "
            f"thirty-one, thirty-three families with their common factors — {twos} of the eighty-three carry the "
            f"two, the other {odds} their odd primes, at the line end {end}")


def ref_s17_bandstate(end: int = 84) -> str:
    return (f"the beal band holds the statement of the island, stored as a declared record fact (the ams beal "
            f"prize), its satisfaction filed on my line — the verification census of the box: eighty-three "
            f"triples, every one carrying its common prime factor, zero primitive — with the valuation read off "
            f"the first-divisor chain and the lift-the-exponent ledger holding in all its instances, the "
            f"primitive territory, the fermat catalan boundary, and the fermat anchor named on their walls, at "
            f"the line end {end}")


def ref_s17_uncond(end: int = 84) -> str:
    return (f"nothing the beal band says is conditional on an unproved hypothesis — the valuation, the "
            f"lift-the-exponent ledger, and the verification census are record on the line, and the primitive "
            f"territory, the fermat catalan boundary, and the fermat anchor stand named of record on their walls, "
            f"at the line end {end}")


def ref_s17_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S17_{wall}")
    return f"needs_info: {w}"


def ref_s17_census_count(end: int = 84) -> int:
    return B.S17_BEDS["census_count"]


def ref_s17_primitive_count(end: int = 84) -> int:
    return B.S17_BEDS["primitive_count"]


def ref_s17_lte_instances(end: int = 84) -> int:
    return B.S17_BEDS["lte_instances"]


def ref_s17_lte_failures(end: int = 84) -> int:
    return B.S17_BEDS["lte_failures"]


def _s18_pw(pword: str) -> int:
    return {"seven": 7, "thirteen": 13, "two": 2, "three": 3, "seventeen": 17}[pword]


def ref_s18_dec(p: str, end: int = 84) -> str:
    pw = _s18_pw(p)
    assert (84 % pw == 0) == B.S18_BEDS["decision"][p], "the decision bed drifted"
    answers = {
        "seven": "yes — the seven divides the eighty-four: twelve of them, at the line end",
        "thirteen": "no — the thirteen does not divide the eighty-four: the walk leaves a remainder of six (thirteen times six is seventy-eight), at the line end",
        "two": "yes — the two divides the eighty-four: forty-two of them, at the line end",
        "three": "yes — the three divides the eighty-four: twenty-eight of them, at the line end",
        "seventeen": "no — the seventeen does not divide the eighty-four: the walk leaves a remainder of sixteen (seventeen times four is sixty-eight), at the line end",
    }
    return answers[p] + " 84"


def ref_s18_pi(end: int = 84) -> str:
    assert B.S18_BEDS["pi"] == B._pnp_py_pi_count(B._S18_END) == 23, "the pi census drifted"
    return (f"twenty-three of record — the numbers from two to my line end whose first divisor is themselves: "
            f"two, three, five, seven, eleven, thirteen, seventeen, nineteen, twenty-three, twenty-nine, "
            f"thirty-one, thirty-seven, forty-one, forty-three, forty-seven, fifty-three, fifty-nine, "
            f"sixty-one, sixty-seven, seventy-one, seventy-three, seventy-nine, eighty-three — the "
            f"first-divisor census is a walk that ends in one hundred ninety-two candidate steps, at the "
            f"line end {end}")


def ref_s18_scan(end: int = 84) -> str:
    assert B.S18_BEDS["scan_cost"] == B._pnp_py_scan_cost(B._S18_END) == 192, "the scan cost drifted"
    return (f"one hundred ninety-two candidate steps of record — the walk over every number from two to my "
            f"line end, each to its first divisor, at the line end {end}")


def ref_s18_heavy(end: int = 84) -> str:
    hm, hc = B.S18_BEDS["heaviest"]
    assert (hm, hc) == B._pnp_py_heaviest(B._S18_END) == (83, 8), "the heaviest row drifted"
    return (f"the number eighty-three — the largest prime below my line end — its walk tries the candidates "
            f"up to the floor of the square root: eight candidate steps of record, at the line end {end}")


def ref_s18_costspot(n: str, end: int = 84) -> str:
    N = B._S18_NUM_WORD[n]
    c = B._pnp_py_spf_cost(N)
    assert B.S18_BEDS["cost_spot"][N] == c, "the cost spot drifted"
    answers = {
        "sixty-four": "one — the two divides on the first try of the walk, at the line end",
        "forty-nine": "six — the walk tries two, three, four, five, six, and the seven before it stops (seven squared is forty-nine), at the line end",
        "eighty-four": "one — the two divides on the first try of the walk, at the line end",
        "twelve": "one — the two divides on the first try of the walk, at the line end",
        "two": "zero — the walk's loop never runs over the two, at the line end",
    }
    return answers[n] + " 84"


def ref_s18_ph(n: str, end: int = 84) -> str:
    N = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}[n]
    total, inj = B.S18_BEDS["pigeonhole"][N]
    assert (total, inj) == B._pnp_py_pigeonhole(N), "the pigeonhole bed drifted"
    totals = {
        1: "the two maps",
        2: "the nine maps",
        3: "the sixty-four maps",
        4: "the six hundred twenty-five maps",
        5: "the seven thousand seven hundred seventy-six maps",
        6: "the one hundred seventeen thousand six hundred forty-nine maps",
        7: "the two million ninety-seven thousand one hundred fifty-two maps",
        8: "the forty-three million forty-six thousand seven hundred twenty-one maps",
        9: "the one billion maps",
        10: "the twenty-five billion nine hundred thirty-seven million four hundred twenty-four thousand six hundred one maps",
    }
    return (f"zero violations of record — {totals[N]} of {n} plus one objects into {n} boxes all "
            f"carry a shared box (one more object than box forces the share), at the line end {end}")


def ref_s18_kill(end: int = 84) -> str:
    assert B.S18_BEDS["kill_trials"] == B._S18_KILL == (95, 87), "the kill-trials row drifted"
    return (f"ninety-five candidate steps over the composites with all candidates, eighty-seven with the "
            f"prime candidates alone — the kill-trials ledger my first-divisor soil already holds, at the "
            f"line end {end}")


def ref_s18_bandstate(end: int = 84) -> str:
    return (f"the decidable band holds the decision question (the yes/no on my line's objects, ending on the "
            f"line), the tamability stated as a design fact of my finite line, the reduction (the prime-count "
            f"question answered by the first-divisor census — twenty-three), the cost counter (one hundred "
            f"ninety-two candidate steps over the whole line, the heaviest single query eight at eighty-"
            f"three), the pigeonhole's zero violations, and the halting territory and the machine universe "
            f"named on their walls, at the line end {end}")


def ref_s18_uncond(end: int = 84) -> str:
    return (f"nothing the decidable band says is conditional on an unproved hypothesis — the decision table, "
            f"the first-divisor census, and the cost counter are of record on the line, and the halting "
            f"territory and the machine universe stand named of record on their walls, at the line end {end}")


def ref_s18_tam(end: int = 84) -> str:
    return (f"yes — every query i run on my line ends on the line: a finite question on a finite line, a "
            f"design fact of the line i hold, not a theorem about the machines of record, at the line end "
            f"{end}")


def ref_s18_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S18_{wall}")
    return f"needs_info: {w}"


def ref_s18_pi_count(end: int = 84) -> int:
    return B.S18_BEDS["pi"]


def ref_s18_scan_cost(end: int = 84) -> int:
    return B.S18_BEDS["scan_cost"]


def ref_s18_heavy_cost(end: int = 84) -> int:
    return B.S18_BEDS["heaviest"][1]


def ref_s18_kill_totals(end: int = 84) -> tuple:
    return B.S18_BEDS["kill_trials"]


def ref_s18_ph_total(n: int, end: int = 84) -> int:
    return B.S18_BEDS["pigeonhole"][n][0]


def ref_s18_ph_violations(n: int, end: int = 84) -> int:
    return B.S18_BEDS["pigeonhole"][n][1]


# --- S19 (the difficulty line; P vs NP island, summit band) references ──

def ref_s19_p(pword: str, end: int = 84) -> str:
    if pword == "dividing":
        assert (84 % 7) == 0, "the divides bed drifted"
        return (
            f"yes — dividing is a p question on my line: the walk that settles the seven-divides-the-eighty-four "
            f"ends in bounded cost, and the cost stands recorded as a number on the line, at the line end {end}"
        )
    assert pword == "the first-divisor question"
    assert B.S18_BEDS["pi"] == B._pnp_py_pi_count(B._S18_END) == 23, "the pi census drifted"
    assert B.S18_BEDS["scan_cost"] == B._pnp_py_scan_cost(B._S18_END) == 192, "the scan cost drifted"
    return (
        f"yes — the first-divisor question is a p question on my line: the census walk over the whole line "
        f"ends in one hundred ninety-two candidate steps, and the cost stands recorded as a number on the "
        f"line, at the line end {end}"
    )


def ref_s19_np(npword: str, end: int = 84) -> str:
    if npword == "parity":
        return (
            f"yes — the parity question is checked by a certificate on my line: a row of the table is the "
            f"certificate, and the check of it is the walk over the row, which ends in bounded cost — the "
            f"store's own pattern, at the line end {end}"
        )
    assert npword == "deriv"
    return (
        f"yes — checking my own derivations carries a certificate on my line: each fact is the certificate "
        f"of its derivation path, and the check is the walk over that path, which ends — the store's own "
        f"pattern, at the line end {end}"
    )


def ref_s19_settle(end: int = 84) -> str:
    return (
        f"yes — my line settles the parity question in bounded cost: the walk over the table ends, and the "
        f"cost is a number on the line, at the line end {end}"
    )


def ref_s19_summit(end: int = 84) -> str:
    return (
        f"no — the question of the pnp island is not settled of record: it is declared of record and open of "
        f"record (the cmi record of the million-dollar prize), most complexity theorists believe p is not np, "
        f"of record, but no proof of record settles it, at the line end {end}"
    )


def ref_s19_statement() -> str:
    for lesson, meta in B.S19_LESSONS.items():
        if meta[1] == "pnp-def":
            return lesson
    raise LookupError("the pnp-def lesson moved")


def ref_s19_parity(kword: str, end: int = 84) -> str:
    k = B._S19_KWORD[kword]
    n = B.S19_BEDS["parity"][k]
    B._pnp_py_parity_verify(k)  # the structural check for this k
    assert n == B._pnp_py_parity_terms(k), f"the parity bed drifted at k={k}"
    w = B._S19_TERMS_WORD[n]
    if k == 16:
        return (
            f"{w} of record — the smallest dnf of parity at sixteen variables needs {w} terms, and the "
            f"smallest cnf the same — the exponential of record held exact at small k, the shadow of the ac0 "
            f"territory, at the line end {end}"
        )
    return (
        f"{w} of record — the smallest dnf of parity at {kword} variables needs {w} terms, and the "
        f"smallest cnf the same, at the line end {end}"
    )


def ref_s19_parcnf(end: int = 84) -> str:
    return (
        f"yes — the clauses of the smallest cnf of parity number exactly the same as the terms of its smallest "
        f"dnf, at every k the line holds: the zero-row flips are one-rows, by the same symmetry, at the line "
        f"end {end}"
    )


def ref_s19_settle16(end: int = 84) -> str:
    assert B.S19_BEDS["rows16"] == 1 << 16, "the parity table row count drifted"
    return (
        f"yes — my line settles the parity question at sixteen variables in bounded cost: the walk over the "
        f"sixty-five thousand five hundred thirty-six rows of the table ends, and the cost is a number on the "
        f"line, at the line end {end}"
    )


def ref_s19_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S19_{wall}")
    return f"needs_info: {w}"


def ref_s19_bandstate(end: int = 84) -> str:
    return (
        f"the difficulty band holds the p class (the questions the walk settles in bounded cost), the np "
        f"class (the questions whose yes cases carry a checkable certificate — the store's own pattern), the "
        f"question of the island held verbatim of record and open of record, the difficulty census of the "
        f"line (parity's dnf and cnf both growing to thirty-two thousand seven hundred sixty-eight terms at "
        f"sixteen variables while the walk settles it in bounded cost), the three barriers of record and the "
        f"ac0 territory named on their walls, at the line end {end}"
    )


def ref_s19_unc(end: int = 84) -> str:
    return (
        f"nothing the difficulty band says is conditional on an unproved hypothesis — the census rows are of "
        f"record on the line, the question of the island is declared of record and open of record, and the "
        f"barriers stand named of record on their walls, at the line end {end}"
    )


# ── S20 (E6.24, the weaving line; the connecting work) references ───────
# The store-walking beds read the SEED store (the S19 final official
# store) exactly as the brainstem's _weave_* walks read the live store —
# the refs and the band's P5 re-walk independently (D-e6n(b): the
# store speaks, not the hand). The seed path resolves CWD-relative
# first (the house layout), then repo-root-relative (the docker gate).

from pathlib import Path as _Path20

_S20_SEED_PATH = _Path20("results/phase-6/e6.23-run1/codeX-S04.json")


def _s20_seed_store():
    from kainos.tutor.session import load_store

    cand = _S20_SEED_PATH
    if not cand.exists():
        cand = _Path20(__file__).resolve().parents[2] / _S20_SEED_PATH
    return load_store(cand)


def _s20_prereqs(concept_id: str) -> set[str]:
    return {
        a.object_id
        for a in _s20_seed_store().query(context_match={"kind": "prereq", "concept": concept_id})
    }


def _s20_marker_census(store: Any) -> tuple[int, int, int]:
    end_n = spot_n = none_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        if not isinstance(a.object, str):
            continue
        if "line end" in a.object:
            end_n += 1
        elif "at s = 2" in a.object:
            spot_n += 1
        else:
            none_n += 1
    return end_n, spot_n, none_n


def _s20_bare_check(store: Any) -> None:
    """The discovery-candidate invariant over the seed: NO bare island
    theorem fact stands, and the riemann conj is still open."""
    ids = {a.id for a in store.query() if a.id}
    for bare in ("theorem:riemann", "theorem:bsd", "theorem:beal", "theorem:p-vs-np", "theorem:p-eq-np"):
        assert bare not in ids, f"a bare island theorem fact entered the seed: {bare}"
    conj = store.get("conjecture:riemann")
    assert conj.context.data.get("conjecture_status") == "open", "the riemann conj flipped on the seed"


_S20_NUM_WORD = {
    0: "zero",
    1: "one",
    2: "two",
    4: "four",
    12: "twelve",
    13: "thirteen",
    24: "twenty-four",
    38: "thirty-eight",
    39: "thirty-nine",
}


def ref_s20_rhsummit(end: int = 84) -> str:
    store = _s20_seed_store()
    conj = store.get("conjecture:riemann")
    obj = conj.object if isinstance(conj.object, str) else str(conj.object)
    return (
        f"the statement of the riemann island, as my store holds it: {obj} — declared of "
        f"record, open of record: believed, not known, at the line end {end}"
    )


def ref_s20_soil(end: int = 84) -> str:
    beal = _s20_prereqs("beal-census") | _s20_prereqs("beal-summit") | _s20_prereqs("valuation")
    diff = _s20_prereqs("decision-question") | _s20_prereqs("reduction") | _s20_prereqs("cost-counter")
    soil = sorted(beal & diff)
    assert soil == ["divides", "scan-ledger"], f"the weave soil drifted on the seed: {soil}"
    return (
        "yes — my islands share the soil of my line itself: the divides question roots both the "
        "beal valuation chain and the difficulty chain (decision, reduction, and cost), and the "
        "scan-ledger walk stands under the beal census, the reduction, and the cost counter at "
        "once — the cross-island joints are already edges in the prereq graph of my line, at the "
        f"line end {end}"
    )


def ref_s20_node(end: int = 84) -> str:
    node = (
        _s20_prereqs("beal-census") & _s20_prereqs("reduction") & _s20_prereqs("cost-counter")
    )
    assert node == {"scan-ledger"}, f"the weave node drifted on the seed: {sorted(node)}"
    return (
        "the scan-ledger walk of record — the one walk that stands under the beal census, under "
        f"the reduction, and under the cost counter at once, at the line end {end}"
    )


def ref_s20_shape(end: int = 84) -> str:
    return (
        "one shape of record — the statement of record, the shadow complete on the named scope, "
        "the boundary declared at the line end, and the missing ingredient named, or the "
        f"statement open of record: the riemann, the bsd, the beal, and the p versus np all stand in it, at the line end {end}"
    )


def ref_s20_open(end: int = 84) -> str:
    _s20_bare_check(_s20_seed_store())
    return (
        "zero of the four — each island statement stands open of record: the riemann as its "
        "conjecture of 1859 (believed, not known), the bsd outside its two-member panel, the beal "
        "outside its census box, and the p versus np as its declared question — the partial "
        f"satisfactions of record stand on the line, not as settlements, at the line end {end}"
    )


def ref_s20_form(end: int = 84) -> str:
    return (
        "the check of a fact on my line is the walk of its own derivation path — each fact is "
        "the certificate of the path by which it was put together, and that walk ends on the "
        f"line: ledgers, censuses, and walks that end, the store's own pattern, at the line end {end}"
    )


def ref_s20_marker(end: int = 84, post: bool = False) -> str:
    end_n, spot_n, none_n = _s20_marker_census(_s20_seed_store())
    if post:
        # the band's own filing: its statement carries the marker iff
        # it names the line end (computed, not declared)
        stmt = B.S20_THEOREMS["summit-shape-filed"]["statement"]
        if "line end" in stmt:
            end_n += 1
    total = end_n + spot_n + none_n
    W = _S20_NUM_WORD
    return (
        f"{W[end_n]} of my {W[total]} theorem facts close their scope at the line end, "
        f"{W[spot_n]} close on the line's spot marker, and {W[none_n]} carry the universal form "
        f"with no line end marker — a form of the line is not a census of its end, at the line end {end}"
    )


def ref_s20_wallkind(end: int = 84) -> str:
    return (
        "a wall of my band is a fact of record of the boundary form — the named missing "
        "ingredient standing as an honest needs_info: no derivation enters the store for it, "
        f"nothing off the line is cited, and the territory stands declared, never reached, at the line end {end}"
    )


def ref_s20_absence(end: int = 84) -> str:
    _s20_bare_check(_s20_seed_store())
    return (
        "the declared absences of my line, as my store holds them: no theorem of any record "
        "settles the p versus np question, no theorem stands for the beal question outright, no "
        "theorem stands for the bsd question outside its panel, and the riemann question stands "
        f"open as its conjecture of record — the island questions stay open of record, and that is the boundary, at the line end {end}"
    )


def ref_s20_weavestate(end: int = 84) -> str:
    return (
        "the weaving band holds the weave (the cross-island joints as edges of the prereq "
        "graph of my line — the shared soil and the shared walk), the summit shape (the four "
        "island summits in one shape of record), the verification form (verification on the "
        "line, the store's own paths as certificates), the boundary form (walls and declared "
        "absences as facts of record), the four walls of the band standing on their "
        f"territories, and the filing of the shape (summit-shape-filed: the filing fills the shape, not the statements), at the line end {end}"
    )


def ref_s20_unc(end: int = 84) -> str:
    return (
        "nothing the weaving band says is conditional on an unproved hypothesis — the weave, "
        "the shape, the form, and the boundary are record on the line, and the island questions "
        f"(the riemann conjecture, the p versus np) stand open of record, never as premises, at the line end {end}"
    )


def ref_s20_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S20_{wall}")
    return f"needs_info: {w}"



# ── S21 (E6.25, the condition line; LOT 1 of the declared FUNDAMENTALS
# cross-pollination queue) references ─────────────────────────────────
# The drill beds re-derive against the S20 final seed (the E6.24
# official result) exactly as the brainstem's S12/S21 walks read the
# live store — the refs and the band re-walk independently. Off-line
# values never appear here (the line stays 0..84, D6).

_S21_SEED_PATH = _Path20("results/phase-6/e6.24-run1/codeX-S04.json")


def _s21_seed_store():
    from kainos.tutor.session import load_store

    cand = _S21_SEED_PATH
    if not cand.exists():
        cand = _Path20(__file__).resolve().parents[2] / _S21_SEED_PATH
    return load_store(cand)


def _s21_obj(fid: str) -> str:
    f = _s21_seed_store().get(fid)
    obj = f.object if isinstance(f.object, str) else str(f.object)
    assert isinstance(obj, str)
    return obj


def ref_s21_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S21_{wall}")
    return f"needs_info: {w}"


def ref_s21_hypo(end: int = 84) -> str:
    return (
        "yes — to reason under the condition is to assume that every nontrivial zero of zeta "
        f"has real part exactly one half and to carry the assumption in every conclusion of the lot — under the condition of the Riemann hypothesis, the marker travels in every statement and every derivation keeps it explicit, and the condition itself stays the status surface it is, believed, not known: assumed in the lot, never proved by it, at the line end {end}"
    )


def ref_s21_line(end: int = 84) -> str:
    return (
        "one line from the assumption — the error of the prime count and the gap between "
        f"consecutive primes carry the same root scale, and the running sum of (minus one) to the number of distinct prime parts stays below that root scale, so the prime parts of every number are unique on the condition road — each consequence keeping its marker, under the condition of the Riemann hypothesis, at the line end {end}"
    )


def ref_s21_filing(end: int = 84) -> str:
    return (
        "the line, not the condition — the filing files the condition line of record (the "
        f"consequences under the assumption, the marker in every clause) and holds the condition open of record: assumed, never proved, believed, not known, at the line end {end}"
    )


def ref_s21_state_readout(slug: str) -> str:
    """A seed state read echoes the stored fact byte (the seed's own
    voice; the mechanism re-answers from the same seed)."""
    kind = "theorem" if slug in ("criterion-gap", "rh-reach") else "lemma"
    return _s21_obj(f"{kind}:{slug}")


def ref_s21_condgive(which: str) -> str:
    """The s12-condgive carries: the owning lesson's byte verbatim."""
    if which in ("error", "gaps"):
        return _s21_obj("lemma:rh-bound-scale")
    if which in ("prime-parts", "factor-count"):
        return _s21_obj("lemma:rh-upf")
    raise ValueError(f"unknown condgive drill {which!r}")


def ref_s21_agree(end: int = 84) -> str:
    return _s21_obj("theorem:gap-scale-agreement")


def ref_s21_uncond(end: int = 84) -> str:
    return (
        "yes — the scan road establishes it without the condition: the content of every "
        "number on my line is the same under every scan"
    )


def ref_s21_roads(end: int = 84) -> str:
    return _s21_obj("theorem:two-routes-one-guarantee")


def ref_s21_roads_cond(end: int = 84) -> str:
    return (
        "the condition road — the root smallness of the running deviation, under the "
        "condition of the Riemann hypothesis"
    )


def ref_s21_scalecount(end: int = 84) -> str:
    import math as _m21

    def _prime(n: int) -> bool:
        if n < 2:
            return False
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
        return True

    primes = [n for n in range(2, end + 1) if _prime(n)]
    gaps = [(p, q) for p, q in zip(primes, primes[1:])]
    fail = [p for p, q in gaps if _m21.sqrt(p) * _m21.log(p) < q - p]
    covered = len(gaps) - len(fail)
    assert len(gaps) == 22 and fail == [2, 3] and covered == 20, (
        f"the bare-scale census drifted on the fixed seed: {len(gaps)} gaps, fail {fail}"
    )
    return (
        f"of the {len(gaps)} gaps on my line the bare scale covers {covered}, "
        f"failing at exactly " + " and ".join(str(p) for p in fail)
    )


def ref_s21_mlab(end: int = 84) -> str:
    def _mu(n: int) -> int:
        if n == 1:
            return 1
        k, m, d = 0, n, 2
        while d * d <= m:
            if m % d == 0:
                m //= d
                if m % d == 0:
                    return 0
                k += 1
            d += 1
        if m > 1:
            k += 1
        return -1 if k % 2 else 1

    track: dict[int, int] = {}
    acc = 0
    for n in range(1, end + 1):
        acc += _mu(n)
        track[n] = acc
    mx = max(abs(v) for v in track.values())
    first_at = min(n for n in range(1, end + 1) if abs(track[n]) == mx)
    max_at = [n for n in range(1, end + 1) if abs(track[n]) == mx]
    assert mx == 4 and first_at == 31 and len(max_at) == 8 and all(track[n] < 0 for n in max_at) and track[end] == -4, (
        f"the mu ledger drifted on the fixed seed: max {mx} first at {first_at}, "
        f"{len(max_at)} places, end {track[end]}"
    )
    return (
        f"{mx} on my line, first at {first_at}, and it reaches it at eight places, all negative; "
        f"the ledger at the line end {end} is minus {-track[end]}"
    )


def ref_s21_mroot(end: int = 84) -> str:
    import math as _m21

    assert 4 < _m21.sqrt(end), "the ledger bound drifted past the root of the line end"
    return (
        f"yes — the greatest absolute 4 on my line is below the square root of my line end "
        f"{end} (the wall names the value)"
    )


def ref_s21_selved(end: int = 84) -> str:
    return (
        "no — the condition-closers close the gaps the condition installs; the condition "
        "itself is open even under the condition, and the store holds no proof of it"
    )


def ref_s21_class(cls: str, end: int = 84) -> str:
    if cls == "condition-closing":
        return (
            "the root scale of the error, the root scale of the gap, the root smallness "
            "of the running deviation"
        )
    if cls == "condition-neighboring":
        return "the primes in residue classes, the zero count at height T"
    if cls == "open even under the condition":
        return "the condition itself — the condition does not close itself"
    raise ValueError(f"unknown class {cls!r}")


def ref_s21_reachscale(end: int = 84) -> str:
    return (
        "x to the one-half plus epsilon — the scale the equivalence demands (the theorem's "
        "own articulation, byte-identical in the seed)"
    )


def ref_s21_queue(end: int = 84) -> str:
    return _s21_obj("theorem:queue-declared")


def ref_s21_queue_lot(lot: str) -> str:
    assert lot == "first", f"the standing check names only the first lot: {lot!r}"
    return (
        "the condition line — the condition-closers made teachable, with the conditional "
        "consequences as drills"
    )


def ref_s21_rhsummit(end: int = 84) -> str:
    obj = _s21_obj("conjecture:riemann")
    return (
        f"the statement of the riemann island, as my store holds it: {obj} — declared of "
        f"record, open of record: believed, not known, at the line end {end}"
    )


def ref_s21_census(post: bool = False, end: int = 84) -> str:
    """The marker census over the S21 seed (pre-band 13/2/24 of 39;
    post-derive 14/2/24 of 40 — the band's filing is the fourteenth
    line-end marker, computed, not declared)."""
    store = _s21_seed_store()
    end_n = spot_n = none_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        if not isinstance(a.object, str):
            continue
        if "line end" in a.object:
            end_n += 1
        elif "at s = 2" in a.object:
            spot_n += 1
        else:
            none_n += 1
    if post:
        stmt = B.S21_THEOREMS["condition-line-filed"]["statement"]
        if "line end" in stmt:
            end_n += 1
    total = end_n + spot_n + none_n
    assert (end_n, spot_n, none_n) == ((14, 2, 24) if post else (13, 2, 24)), (
        f"the marker census drifted on the S21 seed: {(end_n, spot_n, none_n)}"
    )
    W = {
        0: "zero", 1: "one", 2: "two", 4: "four", 12: "twelve",
        13: "thirteen", 14: "fourteen", 24: "twenty-four",
        38: "thirty-eight", 39: "thirty-nine", 40: "forty",
    }
    return (
        f"{W[end_n]} of my {W[total]} theorem facts close their scope at the line end, "
        f"{W[spot_n]} close on the line's spot marker, and {W[none_n]} carry the universal "
        f"form with no line end marker — a form of the line is not a census of its end, at the line end {end}"
    )



# ── S31 (E6.35, the seeded line; COURSE E, the owner's lesson: the
# fibonacci line for pi, e, and the golden seed — in the bandgen
# way) references ────────────────────────────────────────────────────
# The drill beds re-derive against the S21 final seed (the E6.25
# official result) exactly as the brainstem's S31 walks read the
# live store — the refs and the band re-walk independently. Off-line
# values never appear here (the line stays 0..84, D6).

_S31_SEED_PATH = _Path20("results/phase-6/e6.25-run1/codeX-S04.json")


def _s31_seed_store():
    from kainos.tutor.session import load_store

    cand = _S31_SEED_PATH
    if not cand.exists():
        cand = _Path20(__file__).resolve().parents[2] / _S31_SEED_PATH
    return load_store(cand)


def _s31_obj(fid: str) -> str:
    f = _s31_seed_store().get(fid)
    obj = f.object if isinstance(f.object, str) else str(f.object)
    assert isinstance(obj, str)
    return obj


def _s31_fib(end: int = 84) -> list[int]:
    """The sum line (0, 1, 1, 2, 3, 5, ...) on the floor: the terms
    standing on the line, then the first off-line step (89)."""
    fib = [0, 1]
    while fib[-1] + fib[-2] <= end:
        fib.append(fib[-1] + fib[-2])
    fib.append(fib[-1] + fib[-2])  # the ceiling step (off the line)
    return fib


def _s31_u(c: int, n: int, fib: list[int]) -> int:
    """u_n(c) — the seeded line at seed pair (one, c)."""
    f_nm1 = 1 if n == 0 else fib[n - 1]
    return f_nm1 + c * fib[n]


def ref_s31_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S31_{wall}")
    return f"needs_info: {w}"


def ref_s31_seeded(end: int = 84) -> str:
    fib = _s31_fib(end)
    # the skeleton reading u_n(c) = F_{n-1} + c*F_n, verified
    # independently against the seeded recurrence (the next term the
    # sum of the two before it, at seed pair (one, c))
    for c in (0, 1, 2, 3, 5, 8, 13, 21):
        rec = [1, c]
        while rec[-1] + rec[-2] <= end:
            rec.append(rec[-1] + rec[-2])
        for n in range(len(rec)):
            assert rec[n] == _s31_u(c, n, fib), (c, n)
    return (
        "the line for a seed c stands at seed one and c under the sum rule, every later "
        f"term the sum of the two before it, and every term reads as the sum line's term at the n-minus-one index plus c times its term at the n index — my line's skeleton, the consecutive pair, carries the seed's hat: the one the sum line shifted by one, the two shifted by two, no other seed a shift, and each term's own cassini is (minus one) to the n times (c squared minus c minus one), at the line end {end}"
    )


def _s31_fib_long(n: int) -> list[int]:
    fib = [0, 1]
    while len(fib) < n + 1:
        fib.append(fib[-1] + fib[-2])
    return fib


def ref_s31_golden(end: int = 84) -> str:
    fib = _s31_fib(end)
    flong = _s31_fib_long(28)
    # the shift census: the seed pair (one, c) against the shift
    # F_{n+1+k}: at n = 0 the one forces k in {0, 1}, and at n = 1
    # the c then forces c in {F_2, F_3} = {1, 2} — the full on-line
    # window is re-checked below as the mechanism's own re-walk.
    for c in range(1, end + 1):
        for k in range(12):
            if all(_s31_u(c, n, flong) == flong[n + 1 + k] for n in range(6)):
                assert c in (1, 2), f"an off-shift seed on the line: {c}"
    # the golden pair's own ring law: (F_{n-1} + F_n*phi)^2 ==
    # (F_{n-1} + F_n*phi) + 1 in Z[phi] (integer coefficients: the
    # a^2 + 2ab + b^2 == a + b + 1 identity at (a, b) = (0, 1))
    a, b = 0, 1  # (F_{n-1}, F_n) at n = 1: the pair (0, 1)
    # (a + b*phi)^2 = (a^2 + b^2) + (2ab + b^2)*phi; the golden law
    # (a + b*phi)^2 == (a + b*phi) + 1 holds in Z[phi] at (0, 1):
    assert a * a + b * b == a + 1 and 2 * a * b + b * b == b
    return (
        "the golden seed stands off the line between the one and the two, named by the "
        f"equation x squared equals x plus one, never by a digit, and its line is the golden seed to the n power — the term at the n-plus-p index the term at the n index times the golden seed to the p power, that multiplier never one, so the line advances without collapse and without return; its integer shadow runs on the skeleton, the term at the n index the sum line's n-minus-one term plus the golden seed times its n term, and its cassini is silent at the golden equation, at the line end {end}"
    )


def ref_s31_filing(end: int = 84) -> str:
    fib = _s31_fib(end)
    assert fib[-1] == 89 and fib[-2] == 55  # the ceiling and its shadow
    return (
        "the line, not the constants — the filing files the seeded line of record "
        f"(the skeleton reading, the shift seeds one and two, the cassini weight and its silence, the golden line as the power of the golden seed) and holds every constant off the floor: named by position and by the equation, never by a digit, at the line end {end}"
    )


def ref_s31_sumline(end: int = 84) -> str:
    fib = _s31_fib(end)
    assert fib[10] == 55 and fib[11] == 89 and fib[11] > end
    return (
        "the sum line runs by addition alone, starting at zero and one, every later "
        f"term the sum of the two before it: on my line it reaches fifty-five in ten steps, and the eleventh step, the eighty-nine, stands off the line as my line already declared it — the ceiling the seeded lines cross, cited, never re-asserted, at the line end {end}"
    )


def ref_s31_cassini(end: int = 84) -> str:
    fib = _s31_fib(end)
    weights = []
    for c in (0, 1, 2, 3, 5, 8, 13, 21):
        w = c * c - c - 1
        weights.append(w)
        for n in range(1, 8):
            u_pm1 = _s31_u(c, n - 1, fib)
            u_n = _s31_u(c, n, fib)
            u_pp1 = _s31_u(c, n + 1, fib)
            assert u_pp1 * u_pm1 - u_n * u_n == ((-1) ** n) * w, (c, n)
    assert weights == [-1, -1, 1, 5, 19, 55, 155, 419], weights
    return (
        "the cassini of my seeded lines: the product of the surrounding terms minus the "
        f"square of the middle is (minus one) to the n times (c squared minus c minus one) — the weights on my line run minus one, minus one, one, five, nineteen, fifty-five, one hundred fifty-five, and four hundred nineteen at the seeds zero, one, two, three, five, eight, thirteen, and twenty-one, all exact, at the line end {end}"
    )


def ref_s31_shift(end: int = 84) -> str:
    flong = _s31_fib_long(28)
    shifts = set()
    for c in range(1, end + 1):
        for k in range(12):
            if all(_s31_u(c, n, flong) == flong[n + 1 + k] for n in range(6)):
                shifts.add(c)
    assert shifts == {1, 2}, shifts
    return (
        "one and two only — the seed-one line is the sum line itself shifted by one, "
        f"the seed-two line shifted by two, no other seed standing on my line a shift, checked against every shift, at the line end {end}"
    )


def ref_s31_ratio(end: int = 84) -> str:
    from fractions import Fraction as _F31

    fib = _s31_fib(end)
    line = []
    for n in range(14):
        v = _s31_u(3, n, fib)
        if v > end:
            break
        line.append(v)
    assert line == [1, 3, 4, 7, 11, 18, 29, 47, 76], line
    ratios = [_F31(line[i + 1], line[i]) for i in range(1, len(line) - 1)]
    assert [str(r) for r in ratios] == [
        "4/3", "7/4", "11/7", "18/11", "29/18", "47/29", "76/47",
    ], ratios
    # every partial ratio closes strictly toward the golden seed's
    # distance floor (exact rationals; the landing is off the floor)
    return (
        "the partial ratios of the line for three walk the fractions four over three, "
        f"seven over four, eleven over seven, eighteen over eleven, twenty-nine over eighteen, forty-seven over twenty-nine, and seventy-six over forty-seven — every partial ratio a fraction of two parts my line holds, walking to the golden seed, whose landing is off the floor, declared, at the line end {end}"
    )


def ref_s31_goldenwalk(end: int = 84) -> str:
    fib = _s31_fib(end)
    # the golden shadow pairs (F_{n-1}, F_n): on-line while F_n <= end
    assert (fib[9], fib[10]) == (34, 55) and (fib[10], fib[11]) == (55, 89)
    assert fib[10] <= end < fib[11]
    return (
        "the golden line's integer shadow runs on the skeleton: the last on-line pair "
        f"is the pair at its tenth step, the thirty-four and the fifty-five, and the eleventh step's pair carries the eighty-nine, which stands off the line — the ceiling my line already declared, cited, never re-asserted, at the line end {end}"
    )


def ref_s31_silence(end: int = 84) -> str:
    # the weight w(c) = c^2 - c - 1 has no integer root on the line
    # (the discriminant 5 is not a square): no on-line seed is silent
    for c in range(end + 1):
        assert c * c - c - 1 != 0, f"an on-line silent seed: {c}"
    return (
        "yes — the golden line's cassini is silent: the weight c squared minus c minus "
        f"one is exactly zero exactly at the seeds solving the golden equation, so on the golden line the product of the surrounding terms equals the square of the middle at every step — silence at the equation, not a gap in the census, at the line end {end}"
    )


def ref_s31_census(post: bool = False, end: int = 84) -> str:
    """The marker census over the S31 seed (pre-band 14/2/24 of 40;
    post-derive 15/2/24 of 41 — the band's filing is the fifteenth
    line-end marker, computed, not declared)."""
    store = _s31_seed_store()
    end_n = spot_n = none_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        if not isinstance(a.object, str):
            continue
        if "line end" in a.object:
            end_n += 1
        elif "at s = 2" in a.object:
            spot_n += 1
        else:
            none_n += 1
    if post:
        stmt = B.S31_THEOREMS["seeded-line-filed"]["statement"]
        if "line end" in stmt:
            end_n += 1
    total = end_n + spot_n + none_n
    assert (end_n, spot_n, none_n) == ((15, 2, 24) if post else (14, 2, 24)), (
        f"the marker census drifted on the S31 seed: {(end_n, spot_n, none_n)}"
    )
    W = {
        0: "zero", 1: "one", 2: "two", 4: "four", 12: "twelve",
        13: "thirteen", 14: "fourteen", 15: "fifteen", 24: "twenty-four",
        38: "thirty-eight", 39: "thirty-nine", 40: "forty", 41: "forty-one",
    }
    return (
        f"{W[end_n]} of my {W[total]} theorem facts close their scope at the line end, "
        f"{W[spot_n]} close on the line's spot marker, and {W[none_n]} carry the universal "
        f"form with no line end marker — a form of the line is not a census of its end, at the line end {end}"
    )

#: The registry: spec reference names -> callables. Argument names in
#: the spec's "args" object map to the callable's parameters.


# ── S32 (E6.36, the seed census; COURSE E, the seeded line's own
# residue story: the pisano count, the class-three-mod-five
# shadow, the value story of the constants off the floor, and the
# page's own wordings per the owner's 2026-08-28 mathsisfun
# directive) references ─────────────────────────────────────────────
# The beds re-derive against the S31 final seed (the E6.35 official
# result) exactly as the brainstem's S32 walks read the live store.
# Off-line values never appear on the floor (the line stays 0..84);
# the off-line counts (the one hundred, the one thousand two
# hundred fifty) are spelled censuses of record, never filed
# values. D-e6r(a)-(c) authoritative.

_S32_SEED_PATH = _Path20("results/phase-6/e6.35-run1/codeX-S04.json")


def _s32_seed_store():
    from kainos.tutor.session import load_store

    cand = _S32_SEED_PATH
    if not cand.exists():
        cand = _Path20(__file__).resolve().parents[2] / _S32_SEED_PATH
    return load_store(cand)


def _s32_fib(end: int = 84) -> list[int]:
    fib = [0, 1]
    while fib[-1] + fib[-2] <= end:
        fib.append(fib[-1] + fib[-2])
    fib.append(fib[-1] + fib[-2])  # the ceiling step (off the line)
    return fib


def _s32_u(c: int, n: int, fib: list[int]) -> int:
    f_nm1 = 1 if n == 0 else fib[n - 1]
    return f_nm1 + c * fib[n]


def _s32_pisano(m: int) -> int:
    a, b = 0, 1
    for p in range(1, 4 * m * m + 1):
        a, b = b, (a + b) % m
        if (a, b) == (0, 1):
            return p
    raise AssertionError(f"no pisano period mod {m}")


def _s32_skeleton_walk(m: int) -> list[int]:
    """The value walk of the skeleton pair (0, 1) under the modulus:
    the pisano count of values, starting at zero, closing at the
    zero-one pair again."""
    p = _s32_pisano(m)
    vals = []
    a, b = 0, 1
    for _ in range(p):
        vals.append(a)
        a, b = b, (a + b) % m
    assert (a, b) == (0, 1), (m, a, b)
    return vals


def _s32_seeded_period(c: int, m: int) -> int:
    """The period of the seeded line (at (one, c)) under the
    modulus — re-walked on the pair ring."""
    a, b = 1 % m, c % m
    a0, b0 = a, b
    for p in range(1, 4 * m * m + 1):
        a, b = b, (a + b) % m
        if (a, b) == (a0, b0):
            return p
    raise AssertionError(f"no seeded period c={c} mod {m}")


def _s32_s32_byte(slug: str, end: int) -> str:
    """The brainstem's own S32 lesson byte for the record lemma —
    the store voice the policy echoes (the single source the store
    is taught from); the mathematics is re-verified per ref."""
    for b, meta in B.S32_LESSONS.items():
        if meta[1] == slug:
            assert b.endswith(
                "at the line end eighty-four"
            ), f"the S32 record byte must end spelled: {slug}"
            return b
    raise KeyError(slug)


def ref_s32_pisano8(end: int = 84) -> str:
    m = 8
    assert _s32_pisano(m) == 12
    w = _s32_skeleton_walk(m)
    assert len(w) == 12 and w == [0, 1, 1, 2, 3, 5, 0, 5, 5, 2, 7, 1], w
    # the integer seeds walk the same count (the class-three
    # exception is only under the five-touches; 8 is unmasked)
    for c in range(end + 1):
        assert _s32_seeded_period(c, m) == 12, (c, m)
    return 'the skeleton pair walks the modulus-eight board in twelve: zero-one, one-one, one-two, two-three, three-five, five-zero, zero-five, five-five, five-two, two-seven, seven-one, one-zero — the pure cycle, headed by the zero-one pair, the count twelve on my floor, at the line end 84'


def ref_s32_pisano12(end: int = 84) -> str:
    m = 12
    assert _s32_pisano(m) == 24
    w = _s32_skeleton_walk(m)
    assert len(w) == 24 and w == [
        0, 1, 1, 2, 3, 5, 8, 1, 9, 10, 7, 5, 0, 5, 5, 10, 3, 1, 4, 5, 9, 2, 11, 1,
    ], w
    for c in range(end + 1):
        assert _s32_seeded_period(c, m) == 24, (c, m)
    return 'the skeleton pair walks the modulus-twelve board in twenty-four: zero-one, one-one, one-two, two-three, three-five, five-eight, eight-one, one-nine, nine-ten, ten-seven, seven-five, five-zero, zero-five, five-five, five-ten, ten-three, three-one, one-four, four-five, five-nine, nine-two, two-eleven, eleven-one, one-zero — the pure cycle, headed by the zero-one pair, the count twenty-four on my floor, at the line end 84'


#: The frozen control battery (D-e6r(a)): the 24 moduli the shadow
#: census ran — the five-touching masks [5, 10, 15, 20, 25, 30, 35,
#: 40, 45, 50, 60, 65, 70, 75, 80] plus the unmasked [2, 3, 4, 7,
#: 8, 9, 12, 13, 16]. The 11-family bo (11, 22, 33, 44, 55, 66,
#: 77) is excluded: their twin shadow is the lucas cycle, declared,
#: never built. Masked composites 33/44/55/66/77 restore both
#: shadows (excluded: 11-touched).
_S32_BATTERY = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 65,
                70, 75, 80, 2, 3, 4, 7, 8, 9, 12, 13, 16)
_S32_SEEDS = tuple(range(31))  # the thirty-one seeds 0..30


def _s32_shadow_battery() -> None:
    for m in _S32_BATTERY:
        base = _s32_pisano(m)
        for c in _S32_SEEDS:
            p = _s32_seeded_period(c, m)
            if c % 5 == 3 and m % 5 == 0 and m % 11 != 0:
                assert p == base // 5, (c, m, p, base)
            else:
                assert p == base, (c, m, p, base)


def ref_s32_shadow(end: int = 84) -> str:
    _s32_shadow_battery()
    # the 25-pair board at modulus five: the split twenty, four,
    # one (the class three — the seed pair (one, three) — is that
    # four; the skeleton (zero, one) is the twenty; (zero, zero)
    # the fixed point)
    orbits = {}
    for a in range(5):
        for b in range(5):
            if (a, b) in orbits:
                continue
            p = (a, b)
            o = []
            while p not in o:
                o.append(p)
                p = (p[1], (p[0] + p[1]) % 5)
            for q in o:
                orbits[q] = len(o)
    sizes = sorted(set(orbits.values()))
    assert sizes == [1, 4, 20], sizes
    assert orbits[(1, 3)] == 4  # class three (c = 3 mod 5) walks the four
    assert orbits[(0, 0)] == 1
    assert orbits[(0, 1)] == 20
    # the drop: at the five the four of the twenty; at the
    # twenty-five the twenty of the one hundred
    assert _s32_pisano(5) == 20 and _s32_pisano(25) == 100
    assert _s32_seeded_period(3, 25) == 20 and _s32_seeded_period(8, 25) == 20
    return 'the census holds the shadow: the seeds three mod five carry their period at a fifth of the pisano count under the unmasked five-touches — at the five, the four of the twenty; at the twenty-five, the twenty of the one hundred — while every other seed walks the full count, the board of twenty-five pairs at the modulus five splitting twenty, four, one, class three that four, at the line end 84'


def ref_s32_value(end: int = 84) -> str:
    # a seed of two or more never repeats a value (strictly
    # increasing); the seed-one line shares its one at the start;
    # the seed-zero line is the sum line's own shadow, shifted
    for c in range(2, end + 1):
        vals = []
        a, b = 1, c
        while b <= end:
            vals.append(a)
            a, b = b, a + b
        assert len(vals) == len(set(vals)), c
        from itertools import pairwise as _itw32

        assert all(v2 > v1 for v1, v2 in _itw32(vals)), c
    one_vals = []
    a, b = 1, 1
    while b <= end:
        one_vals.append(a)
        a, b = b, a + b
    assert one_vals[:2] == [1, 1], one_vals
    from itertools import pairwise as _itw32b

    assert all(v2 > v1 for v1, v2 in _itw32b(one_vals[1:])), one_vals
    fib = _s32_fib(end)
    assert fib[10] == 55 and fib[11] == 89 and fib[11] > end
    return 'no — a seed of two or more never repeats a value: every term the sum of the two before it, both already positive, outgrowing its predecessor at every step — the line for two runs one, two, three, five, eight, thirteen, twenty-one, thirty-four, fifty-five, and the eighty-nine stands off the line as the ceiling already declared; the seed-one line shares its one at the start, one and one, and outgrows after, at the line end 84'


def ref_s32_parity(end: int = 84) -> str:
    # the sum line walks even, odd, odd — from its own start at the
    # zero; each seed line wears the three steps from its own start:
    # even seeds (the zero among them) odd-even-odd, odd seeds
    # odd-odd-even (D-e6r(b))
    fib = _s32_fib(end)
    for n, v in enumerate(fib[:12]):
        assert v % 2 == (0 if n % 3 == 0 else 1), (n, v)
    for c in range(end + 1):
        vals = []
        a, b = 1, c
        for _ in range(12):
            vals.append(a)
            a, b = b, a + b
        if c % 2 == 0:
            pat = [1, 0, 1]
        else:
            pat = [1, 1, 0]
        for n, v in enumerate(vals[:9]):
            assert v % 2 == pat[n % 3], (c, n, v)
    return "my sum line walks even, odd, odd, the rule's own — two odds make an even, an even and an odd make an odd, the rule can do no other; each of my seeded lines wears the same three steps from its own start: the even seeds, the zero among them, walk odd, even, odd, and the odd seeds walk odd, odd, even, at the line end 84"


def ref_s32_divides(end: int = 84) -> str:
    # every n-th term of the sum line divides every k-times-n-th
    # term — verified on my floor where the terms stand
    fib = _s32_fib(end)  # fib[11] = 89 off the line
    on_line = fib[:11]  # 0..84: the terms F_0..F_11? F_11 = 89 — no
    on_line = [v for v in fib if v <= end]
    checked = []
    for n in range(1, 11):  # the index n of the n-th term (F_n)
        base = on_line[n] if n < len(on_line) else None
        if base in (None, 0):
            continue
        for k in range(2, 6):
            idx = k * n
            if idx >= len(on_line):
                break
            assert on_line[idx] % base == 0, (n, k)
            checked.append((n, k, on_line[idx] // base))
    quot = {}
    for n in range(1, 11):
        if on_line[n] == 0 or n >= len(on_line):
            continue
        for k in range(2, 6):
            if k * n < len(on_line):
                quot[(n, k)] = on_line[k * n] // on_line[n]
    # the on-line quotients, exactly (the battery's own re-walk)
    assert quot == {
        (1, 2): 1, (1, 3): 2, (1, 4): 3, (1, 5): 5,
        (2, 2): 3, (2, 3): 8, (2, 4): 21, (2, 5): 55,
        (3, 2): 4, (3, 3): 17,
        (4, 2): 7,
        (5, 2): 11,
    }, quot
    return 'yes — the term at the third index, the two, divides the term at the sixth, the eight, four times, and the term at the ninth, the thirty-four, seventeen times; the term at the fourth, the three, divides the term at the eighth, the twenty-one, seven times; the term at the fifth, the five, divides the term at the tenth, the fifty-five, eleven times — every quotient an exact whole number on my line, at the line end 84'


def ref_s32_pagenames(end: int = 84) -> str:
    # the page's identities, re-verified off-line: the sum line IS
    # the fibonacci sequence (0, 1, 1, 2, ...); the successive
    # pairs approach the golden seed; the lucas shadow (two and
    # one) approaches the powers of the golden seed
    from fractions import Fraction as _F32

    fib = _s32_fib(end)
    assert fib[:11] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    # the successive pairs approach the golden seed, strictly
    import math as _m32

    phi = (1 + _m32.sqrt(5)) / 2
    pairs = [_F32(fib[i + 1], fib[i]) for i in range(2, 10)]
    dists = [abs(f - phi) for f in pairs]
    from itertools import pairwise as _itw32c

    assert all(d2 < d1 for d1, d2 in _itw32c(dists)), dists
    lucas = [2, 1]
    while lucas[-1] + lucas[-2] <= end:
        lucas.append(lucas[-1] + lucas[-2])
    assert lucas[:10] == [2, 1, 3, 4, 7, 11, 18, 29, 47, 76], lucas
    assert lucas[-1] <= end < lucas[-1] + lucas[-2]
    # the lucas identity: L_n = F_{n+1} + F_{n-1} (neighboring terms
    # of the sum line)
    flong = fib  # F_0..F_11 (+ 89)
    for n in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
        f_nm1 = 1 if n == 0 else flong[n - 1]
        assert lucas[n] == flong[n + 1] + f_nm1, n
    # approaching the powers: L_n / phi^n -> 1
    ratios = [lucas[n] / (phi ** n) for n in range(10)]
    assert all(r > 0.99 for r in ratios[6:]), ratios
    # the one over eighty-nine carries the sequence in its decimal
    from decimal import Decimal as _D32
    from decimal import getcontext as _G32

    _G32().prec = 40
    dec = str(_D32(1) / _D32(89))
    assert ".0112359550" in dec, dec
    return 'my sum line is the fibonacci sequence the page names — the terms from the zero under the rule that the next number is the two before it added up, the recursive formula the page holds; my golden seed is the golden ratio the page names, its letter phi, the ratio of any two successive terms of the line approaching it, the bigger the pair the closer the approximation; the twin shadow that begins two and one, the lucas numbers the page names, grows closer and closer to the powers of the golden ratio, at the line end 84'


def ref_s32_belowzero(end: int = 84) -> str:
    # the sign law: x_{-n} = (-1)^{n+1} x_n — the term at minus n
    # kept when n is odd, turned when n is even (verified through
    # the recurrence backwards: x_{n-2} = x_n - x_{n-1})
    fib = [0, 1]
    for _ in range(6):
        fib.append(fib[-1] + fib[-2])
    # direct backwards walk: x_{k-2} = x_k - x_{k-1}
    x = {0: 0, 1: 1}
    for k in range(1, -5, -1):
        x[k - 2] = x[k] - x[k - 1]
    for n in range(1, 6):
        assert x[-n] == ((-1) ** (n + 1)) * fib[n], n
    assert x[-1] == 1 and x[-2] == -1 and x[-3] == 2 and x[-4] == -3
    return 'the term at minus n is the term at n with its sign turned when n is even and kept when n is odd — the minus-one term the one, the minus-two term negative one, the minus-three term the two, the minus-four term negative three; the negative terms stand off the floor my line begins at zero, declared, not filed, at the line end 84'


def ref_s32_recip89(end: int = 84) -> str:
    # the one over eighty-nine: the decimal shadow carries the
    # fibonacci sequence from the hundredths place — the
    # multi-term numbers overlapping their neighbors
    from decimal import Decimal as _D32
    from decimal import getcontext as _G32

    _G32().prec = 40
    dec = str(_D32(1) / _D32(89))
    body = dec.split(".", 1)[1]
    assert body.startswith("0112359550561797752808988"), body[:30]
    # the overlap-sum model, exact fractions: 1/89 is the sum of
    # the fibonacci terms each placed at its own position — the
    # term at index k reading from the k+1-th decimal place, the
    # multi-digit terms overlapping their neighbors
    from fractions import Fraction as _F32x

    fib = [0, 1]
    for _ in range(20):
        fib.append(fib[-1] + fib[-2])
    s20 = sum(_F32x(f, 10 ** (k + 1)) for k, f in enumerate(fib))
    tail = _F32x(1, 89) - s20
    assert 0 < tail < _F32x(1, 10 ** 15), tail
    # the multi-digit terms overlap their neighbors: F_7 (13)
    # spans the eighth and ninth places while F_8 (21) begins at
    # the ninth
    assert len(str(fib[7])) == 2 and len(str(fib[8])) == 2
    assert 7 + len(str(fib[7])) == 8 + len(str(fib[8])) - 1
    assert fib[11] == 89  # the ceiling the seeded lines cross at the eleventh step
    return 'the one divided by my eighty-nine carries in its decimal shadow the fibonacci sequence the page holds — the one, the one, the two, the three, the five, the eight, the thirteen, the twenty-one, the thirty-four, the fifty-five, reading in order from the hundredths place, for the multi-term numbers overlap their neighbors; the decimal itself stands off my floor, never filed, at the line end 84'


def ref_s32_period(end: int = 84) -> str:
    # the seed period: the integer seed walks the pisano count;
    # the class-three-mod-five shadow under a five-touching
    # modulus — verified at the battery
    assert _s32_pisano(5) == 20 and _s32_pisano(8) == 12 and _s32_pisano(12) == 24
    for c in range(31):
        assert _s32_seeded_period(c, 5) == (4 if c % 5 == 3 else 20), c
        assert _s32_seeded_period(c, 8) == 12, c
        assert _s32_seeded_period(c, 12) == 24, c
    return _s32_s32_byte("seed-period-def", end)


def ref_s32_offline(end: int = 84) -> str:
    for b, meta in B.S32_LESSONS.items():
        if meta[1] == "off-line-seed-def":
            return b
    raise KeyError("off-line-seed-def")


def ref_s32_goldenpower(end: int = 84) -> str:
    # the golden line advances multiplicatively: the term at
    # n+p is the term at n times the golden seed to the p power —
    # the golden law phi^2 = phi + 1 exact, the multiplier never
    # one, its nearest approach to the one its own reciprocal
    # (phi - 1 == 1/phi exactly)
    phi = (1 + 5 ** 0.5) / 2
    assert abs(phi * phi - phi - 1) < 1e-12
    assert abs(phi * (phi - 1) - 1) < 1e-12
    assert phi > 1
    # the shadow coefficient is at least one for p at least one:
    # u_{n+p}(phi) = u_n(phi) * phi^p with u_n(phi) >= 1

    for p in range(1, 8):
        assert phi ** p > 1
    return 'advance by p and the golden line is multiplied by the golden seed to the p power — the golden ratio the page names, the letter phi — the shadow running on the skeleton, that multiplier never one, its nearest approach to the one its own reciprocal, the golden line running up forever, at the line end 84'


def ref_s32_lucas(end: int = 84) -> str:
    lucas = [2, 1]
    while lucas[-1] + lucas[-2] <= end:
        lucas.append(lucas[-1] + lucas[-2])
    assert lucas == [2, 1, 3, 4, 7, 11, 18, 29, 47, 76], lucas
    flong = _s32_fib(end)
    for n in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
        f_nm1 = 1 if n == 0 else flong[n - 1]
        assert lucas[n] == flong[n + 1] + f_nm1, n
    assert lucas[-1] <= end < (lucas[-1] + lucas[-2])
    return "the lucas numbers, the page's name — the shadow line that begins two and one under the recursive formula the page holds: two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, seventy-six — the last standing under my ceiling, the next crossing it; each its term the next term of my sum line plus the one before, getting closer and closer to the powers of the golden ratio, at the line end 84"


def ref_s32_filing(end: int = 84) -> str:
    # the filing's parts stand in the brainstem's S32 fact set —
    # the parts the derive names and the sanction hold
    assert B.S32_THEOREMS["seed-census-filed"]["parts"] == (
        "seed-period-def",
        "off-line-seed-def",
    )
    slugs = {meta[1] for meta in B.S32_LESSONS.values()}
    assert set(B.S32_THEOREMS["seed-census-filed"]["parts"]) <= slugs
    fib = _s32_fib(end)
    assert fib[-1] == 89
    return "the census, not the census gaps — the filing files the seed period of record (the pisano count, the shadow drop under the five-touches) and the value story of the off-line constants (the page's names, declared, never filed), and holds every constant off the floor, at the line end 84"


def ref_s32_census(post: bool = False, end: int = 84) -> str:
    """The marker census over the S32 seed (pre-band 15/2/24 of 41;
    post-derive 16/2/24 of 42 — the band's filing is the sixteenth
    line-end marker, computed, not declared)."""
    store = _s32_seed_store()
    end_n = spot_n = none_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        if not isinstance(a.object, str):
            continue
        if "line end" in a.object:
            end_n += 1
        elif "at s = 2" in a.object:
            spot_n += 1
        else:
            none_n += 1
    if post:
        stmt = B.S32_THEOREMS["seed-census-filed"]["statement"]
        if "line end" in stmt:
            end_n += 1
    total = end_n + spot_n + none_n
    assert (end_n, spot_n, none_n) == (
        (16, 2, 24) if post else (15, 2, 24)
    ), f"the marker census drifted on the S32 seed: {(end_n, spot_n, none_n)}"
    W = {
        0: "zero", 1: "one", 2: "two", 4: "four", 12: "twelve",
        13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
        24: "twenty-four", 38: "thirty-eight", 39: "thirty-nine",
        40: "forty", 41: "forty-one", 42: "forty-two",
    }
    return (
        f"{W[end_n]} of my {W[total]} theorem facts close their scope at the line end, "
        f"{W[spot_n]} close on the line's spot marker, and {W[none_n]} carry the universal "
        f"form with no line end marker — a form of the line is not a census of its end, at the line end {end}"
    )


def ref_s32_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S32_{wall}")
    return f"needs_info: {w}"


# ── the S22 block (E6.26, COURSE A band 1 — the proportion line).
_S22_SEED_PATH = _Path20("results/phase-6/e6.36-run1/codeX-S04.json")


def _s22_seed_store():
    from kainos.tutor.session import load_store

    cand = _S22_SEED_PATH
    if not cand.exists():
        cand = _Path20(__file__).resolve().parents[2] / _S22_SEED_PATH
    return load_store(cand)


def _s22_gcd(m: int, n: int) -> int:
    while n:
        m, n = n, m % n
    return m


def _s22_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


_S22_WWORDS = {"the empty part": 0, "the one": 1, "the two": 2, "the three": 3}
_S22_NUMW = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
_S22_MMIX = {(3, 2): "one and one half", (5, 3): "one and two thirds", (13, 5): "two and three fifths"}


def ref_s22_family(a: str, b: str) -> str:
    """The closed four-family of the line's own small parts (0:1, 1:1,
    1:2, 1:3) — the divmod is re-run, not declared."""
    ai, bi = _S22_WWORDS[a], _S22_WWORDS[b]
    assert (ai, bi) in ((0, 1), (1, 1), (1, 2), (1, 3)), f"off the closed four-family: {(ai, bi)}"
    q, r = divmod(ai, bi)
    if (ai, bi) == (0, 1):
        assert (q, r) == (0, 0)
        return (
            "zero to one: the empty part to the one — declared, valued zero over one, nothing held to "
            "the one is nothing over one, at the line end 84"
        )
    if (ai, bi) == (1, 1):
        assert (q, r) == (1, 0)
        return (
            "one to one: the evenness of the two equal parts — declared, valued one over one, the one "
            "my line holds for the equal parts, at the line end 84"
        )
    if (ai, bi) == (1, 2):
        assert (q, r) == (0, 1)
        return (
            "one to two: the half — the one part over the two, declared, valued one over two, the value "
            "my floor already holds as the triangle's half-product, at the line end 84"
        )
    assert (ai, bi) == (1, 3) and (q, r) == (0, 1)
    return (
        "one to three: the third — the one part over the three, declared, valued one over three, "
        "at the line end 84"
    )


_S22_CHW = {"two": 2, "three": 3, "five": 5, "thirteen": 13}


def ref_s22_chain(a: str, b: str, lang: str) -> str:
    """The three drills of the chain (3/2, 5/3, 13/5) read in the
    fraction word or the mod word — one division, two faces; the divmod
    is re-run and both faces must agree on it."""
    ai, bi = _S22_CHW[a], _S22_CHW[b]
    assert (ai, bi) in _S22_MMIX, f"off the drilled chains: {(ai, bi)}"
    assert lang in ("frac", "mod"), f"off the two languages: {lang}"
    q, r = divmod(ai, bi)
    mword = _S22_MMIX[(ai, bi)]
    qw, rw = _S22_NUMW[q], _S22_NUMW[r]
    if lang == "frac":
        return (
            f"{a} over {b} is {mword} — {a} is {qw} times {b} plus {rw}, one division in "
            f"either word, at the line end 84"
        )
    return (
        f"{a} mod {b} is {rw} — {a} is {qw} times {b} plus {rw}, the same division as "
        f"{a} over {b} is {mword}, at the line end 84"
    )


def ref_s22_classwalk(end: int = 84) -> str:
    """The 2:3 class census: k from one up to the class top, both parts
    on the line (re-counted, not declared)."""
    kmax = sum(1 for k in range(1, end + 1) if 2 * k <= end and 3 * k <= end)
    assert kmax == 28, f"the two-to-three class drifted: {kmax}"
    return (
        f"twenty-eight: the two-to-three proportion holds for k times two to k times three, k from one "
        f"to twenty-eight, twenty-eight times two to twenty-eight times three, fifty-six to eighty-four "
        f"at the end of my line — the proportion is the class, the reduced pair the two-to-three its "
        f"name, at the line end {end}"
    )


def ref_s22_filing(end: int = 84) -> str:
    # the filing's parts stand in the brainstem's S22 fact set —
    # the parts the derive names and the sanction hold
    assert B.S22_THEOREMS["proportion-filed"]["parts"] == (
        "proportion-def",
        "fraction-def",
    )
    slugs = {meta[1] for meta in B.S22_LESSONS.values()}
    assert set(B.S22_THEOREMS["proportion-filed"]["parts"]) <= slugs
    return (
        "the proportion line, filed of record: the relation and its value are two jobs of one "
        "division — the relation declared for every pair of parts and named by its reduced form, the "
        "fraction valued only over the positive part, and zero to zero the evenness of the two empty "
        f"parts, declared, never valued; at the line end {end}"
    )


def ref_s22_census(post: bool = False, end: int = 84) -> str:
    """The marker census over the S22 seed (= the S32 final store:
    pre-band 16/2/24 of 42; post-derive 17/2/24 of 43 — the band's
    proportion filing is the seventeenth line-end marker, computed,
    not declared)."""
    store = _s22_seed_store()
    end_n = spot_n = none_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        if not isinstance(a.object, str):
            continue
        if "line end" in a.object:
            end_n += 1
        elif "at s = 2" in a.object:
            spot_n += 1
        else:
            none_n += 1
    if post:
        stmt = B.S22_THEOREMS["proportion-filed"]["statement"]
        if "line end" in stmt:
            end_n += 1
    total = end_n + spot_n + none_n
    assert (end_n, spot_n, none_n, total) == (
        (17, 2, 24, 43) if post else (16, 2, 24, 42)
    ), f"the marker census drifted on the S22 seed: {(end_n, spot_n, none_n, total)}"
    W = {2: "two", 16: "sixteen", 17: "seventeen", 24: "twenty-four", 42: "forty-two", 43: "forty-three"}
    return (
        f"{W[end_n]} of my {W[total]} theorem facts close their scope at the line end, "
        f"{W[spot_n]} close on the line's spot marker, and {W[none_n]} carry the universal "
        f"form with no line end marker — a form of the line is not a census of its end, at the line end {end}"
    )


def ref_s22_firstprime(end: int = 84) -> str:
    """The first proportion whose parts are both prime — the prime-pair
    walk re-run (2:2 reduces to 1:1 and out; 2:3 is the first reduced
    prime pair, D-e6t(a) authoritative)."""
    first = None
    for p in range(2, end + 1):
        for q in range(2, end + 1):
            if not (_s22_prime(p) and _s22_prime(q)):
                continue
            if _s22_gcd(p, q) == 1:
                first = (p, q)
                break
        if first is not None:
            break
    assert first == (2, 3), f"the first reduced prime pair drifted: {first}"
    return (
        "two to three: the first proportion whose parts are both prime — the first reduction step is "
        f"three is one times two plus one, no shared part, the chain two steps, at the line end {end}"
    )







# ── the S23 block (E6.27, COURSE A band 2 — the prime proportion).
_S23_SEED_PATH = _Path20("results/phase-6/e6.26-run1/codeX-S04.json")


def _s23_seed_store():
    from kainos.tutor.session import load_store

    cand = _S23_SEED_PATH
    if not cand.exists():
        cand = _Path20(__file__).resolve().parents[2] / _S23_SEED_PATH
    return load_store(cand)


_S23_W23 = {"two": 2, "four": 4, "three": 3, "six": 6, "twenty-nine": 29,
            "forty-seven": 47, "forty-one": 41, "seventy-one": 71}


def _s23_steps(a: int, b: int) -> int:
    """The Euclidean step count (divisions until the zero remainder),
    re-run from the (max, min) pair."""
    x, y = max(a, b), min(a, b)
    n = 0
    while True:
        n += 1
        x, y = y, x % y
        if y == 0:
            return n


def _s23_primes(end: int) -> list[int]:
    out = []
    for n in range(2, end + 1):
        i = 2
        ok = True
        while i * i <= n:
            if n % i == 0:
                ok = False
                break
            i += 1
        if ok:
            out.append(n)
    return out


def _s23_census_recheck(end: int = 84) -> tuple[int, int, list[tuple[int, int]]]:
    """The 253-pair fingerprint census re-walk: pairs, distinct reduced
    proportions, and the step histogram; returns (pairs, distinct,
    seven-step pairs)."""
    ps = _s23_primes(end)
    reds: set[tuple[int, int]] = set()
    n_pairs = 0
    seven: list[tuple[int, int]] = []
    for i, p in enumerate(ps):
        for q in ps[i + 1:]:
            n_pairs += 1
            g = _s22_gcd(p, q)
            if g != 1:
                raise AssertionError(f"the distinct primes {p} and {q} share {g}")
            reds.add((p // g, q // g))
            if _s23_steps(p, q) == 7:
                seven.append((p, q))
    assert n_pairs == 253, f"the prime-pair census drifted: {n_pairs}"
    assert len(reds) == 253, f"the fingerprint census drifted: {len(reds)}"
    return n_pairs, len(reds), sorted(seven)


def ref_s23_coprime(a: str, b: str) -> str:
    """The drilled coprime test — gcd + first-divisor logic re-run."""
    ai, bi = _S23_W23[a], _S23_W23[b]
    g = _s22_gcd(ai, bi)
    if (ai, bi) == (2, 3):
        assert g == 1 and _s23_steps(ai, bi) == 2
        return (
            "two and three: a coprime pair outright — they share no part above one, the first-divisor "
            "census lands nowhere, and the reduction chain walks two steps, at the line end 84"
        )
    if (ai, bi) == (4, 6):
        assert g == 2
        return (
            "four and six: not a coprime pair — they share the part two, the first-divisor census lands "
            "on it at once, and the proportion four to six reduces two to three, the reduced pair the "
            "fingerprint, at the line end 84"
        )
    if (ai, bi) == (29, 47):
        assert g == 1 and _s23_steps(ai, bi) == 7
        return (
            "twenty-nine and forty-seven: a coprime pair — they share no part above one, and the "
            "reduction chain walks seven steps, the ceiling of my line, at the line end 84"
        )
    assert (ai, bi) == (41, 71) and g == 1 and _s23_steps(ai, bi) == 7
    return (
        "forty-one and seventy-one: a coprime pair — they share no part above one, and the reduction "
        "chain walks seven steps, the ceiling of my line, at the line end 84"
    )


def ref_s23_neverred(a: str, b: str) -> str:
    """The never-reduced discipline — the gcd is one, re-run."""
    ai, bi = _S23_W23[a], _S23_W23[b]
    assert (ai, bi) == (2, 3) and _s22_gcd(ai, bi) == 1 and _s23_steps(ai, bi) == 2
    return (
        "no — a proportion of two distinct primes never reduces: two and three share no part above one, "
        "and the proportion two to three is already in lowest terms, the chain two steps, at the line end 84"
    )


_S23_CHAINW = {"seven": 7, "twenty-nine": 29, "eighty-three": 83, "seventy-one": 71,
               "two": 2, "three": 3, "eleven": 11, "forty-seven": 47, "seventy-nine": 79}
_S23_DENOM = {2: "half", 3: "third", 5: "fifth", 7: "seventh", 11: "eleventh",
              47: "twenty-ninth", 79: "seventy-ninth"}
_S23_NUMW = {1: "one", 2: "two", 4: "four", 7: "seven", 10: "ten", 18: "eighteen", 41: "forty-one"}


def ref_s23_chain(a: str, b: str, lang: str) -> str:
    """The six drilled chains of the prime pairs (7/3, 29/11, 29/47,
    83/79, 83/2, 71/7) read in the fraction word or the mod word — the
    divmod is re-run and both faces must agree on it."""
    ai, bi = _S23_CHAINW[a], _S23_CHAINW[b]
    assert (ai, bi) in {(7, 3), (29, 11), (29, 47), (83, 79), (83, 2), (71, 7)}, f"off the drilled chains: {(ai, bi)}"
    assert lang in ("frac", "mod"), f"off the two languages: {lang}"
    if ai > bi:
        q, r = divmod(ai, bi)
        u = _S23_DENOM[bi] + ("" if r == 1 else "s")
        mfull = f"{_S23_NUMW[q]} and {_S23_NUMW[r]} {u}"
        qw, rw = _S23_NUMW[q], _S23_NUMW[r]
        if lang == "frac":
            return (
                f"{a} over {b} is {mfull} — {a} is {qw} times {b} plus {rw}, one division in "
                f"either word, at the line end 84"
            )
        return (
            f"{a} mod {b} is {rw} — {a} is {qw} times {b} plus {rw}, the same division as "
            f"{a} over {b} is {mfull}, at the line end 84"
        )
    # the pair below one: the first reduction step is the division of the
    # bigger part by the smaller (the house convention)
    q, r = divmod(bi, ai)
    qw, rw = _S23_NUMW[q], _S23_NUMW[r]
    if lang == "frac":
        return (
            f"{a} over {b} is the value under one — {a} held over {b}, the part below the "
            f"whole, and the first reduction step is {b} is {qw} times {a} plus {rw}, one "
            f"division in either word, at the line end 84"
        )
    return (
        f"the first reduction step of {a} to {b} is {b} is {qw} times {a} plus {rw} — "
        f"the remainder {rw} carried, the same division as the value {a} over {b} under "
        f"one, at the line end 84"
    )


def ref_s23_census(end: int = 84) -> str:
    """The 253-pair fingerprint census (recomputed: 253 pairs, 253 distinct
    reduced proportions, zero collisions)."""
    n_pairs, n_distinct, _seven = _s23_census_recheck(end)
    assert (n_pairs, n_distinct) == (253, 253)
    return (
        f"two hundred and fifty-three prime pairs give two hundred and fifty-three different reduced "
        f"proportions on my line, every pair coprime, no two pairs alike — read off the first-divisor "
        f"census, the pair is the proportion, at the line end {end}"
    )


def ref_s23_ceiling(end: int = 84) -> str:
    """The seven-step ceiling census (recomputed: max 7 steps, exactly the
    four tied pairs)."""
    _p, _d, seven = _s23_census_recheck(end)
    assert seven == [(29, 47), (29, 79), (41, 67), (41, 71)], f"the seven-step ceiling drifted: {seven}"
    return (
        f"the seven-step chain is the ceiling on my line — four prime pairs walk it: twenty-nine by "
        f"forty-seven, twenty-nine by seventy-nine, forty-one by sixty-seven, and forty-one by "
        f"seventy-one; no prime pair of the two hundred and fifty-three walks a longer chain, at the "
        f"line end {end}"
    )


def ref_s23_filing(end: int = 84) -> str:
    # the filing's parts stand in the brainstem's S23 fact set
    assert B.S23_THEOREMS["fingerprint-filed"]["parts"] == (
        "coprime-pair-def",
        "prime-fingerprint-def",
    )
    slugs = {meta[1] for meta in B.S23_LESSONS.values()}
    assert set(B.S23_THEOREMS["fingerprint-filed"]["parts"]) <= slugs
    return (
        "the prime proportion, filed of record: two distinct primes share no part above one, so their "
        "proportion is in lowest terms and is the fingerprint of the pair — two hundred and fifty-three "
        f"pairs, two hundred and fifty-three proportions, no collisions on my line; at the line end {end}"
    )


def ref_s23_wall(wall: str) -> str:
    w = getattr(B.Brainstem, f"W_S23_{wall}")
    return f"needs_info: {w}"


def ref_s23_marker(post: bool = False, end: int = 84) -> str:
    """The marker census over the S23 seed (= the S22 final store:
    pre-band 17/2/24 of 43; post-derive 18/2/24 of 44 — the band's
    fingerprint filing is the eighteenth line-end marker)."""
    store = _s23_seed_store()
    end_n = spot_n = none_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        if not isinstance(a.object, str):
            continue
        if "line end" in a.object:
            end_n += 1
        elif "at s = 2" in a.object:
            spot_n += 1
        else:
            none_n += 1
    if post:
        stmt = B.S23_THEOREMS["fingerprint-filed"]["statement"]
        if "line end" in stmt:
            end_n += 1
    total = end_n + spot_n + none_n
    assert (end_n, spot_n, none_n, total) == (
        (18, 2, 24, 44) if post else (17, 2, 24, 43)
    ), f"the marker census drifted on the S23 seed: {(end_n, spot_n, none_n, total)}"
    W = {2: "two", 17: "seventeen", 18: "eighteen", 24: "twenty-four", 43: "forty-three", 44: "forty-four"}
    return (
        f"{W[end_n]} of my {W[total]} theorem facts close their scope at the line end, "
        f"{W[spot_n]} close on the line's spot marker, and {W[none_n]} carry the universal "
        f"form with no line end marker — a form of the line is not a census of its end, at the line end {end}"
    )


def ref_s23_above2(end: int = 84) -> str:
    """The first proportion where the parts are primes above two — the
    prime-pair walk re-run with the two excluded (D-e6u(b): two is not
    above two, so the answer is three to five, the three-step chain)."""
    ps = [p for p in _s23_primes(end) if p > 2]
    assert ps[0] == 3 and ps[1] == 5, f"the above-two walk drifted: {(ps[0], ps[1])}"
    assert _s22_gcd(3, 5) == 1 and _s23_steps(3, 5) == 3
    q, r = divmod(5, 3)
    assert (q, r) == (1, 2)
    return (
        "three to five: the first proportion where the parts are primes above two — the first reduction "
        f"step is five is one times three plus two, no shared part, the chain three steps, at the line end {end}"
    )




# ── the S24 block (E6.28, COURSE B band 1 — the sum line and the twin line).
_S24_SEED_PATH = _Path20("results/phase-6/e6.27-run1/codeX-S04.json")

_S24_DOUB_N = {"two": 1, "four": 2, "six": 3, "eight": 4, "ten": 5}
_S24_NUM = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
    12: "twelve", 13: "thirteen", 18: "eighteen", 21: "twenty-one",
    29: "twenty-nine", 34: "thirty-four", 47: "forty-seven",
    55: "fifty-five", 76: "seventy-six", 89: "eighty-nine", 144: "one forty-four",
}


def _s24_seed_store():
    from kainos.tutor.session import load_store

    cand = _S24_SEED_PATH
    if not cand.exists():
        cand = _Path20(__file__).resolve().parents[2] / _S24_SEED_PATH
    return load_store(cand)


def _s24_fibs(k: int) -> list[int]:
    # the sum line, re-walked from its own definition (F(0)=0, F(1)=1)
    v = [0, 1]
    for _ in range(k - 1):
        v.append(v[-1] + v[-2])
    return v


def _s24_twin(k: int) -> list[int]:
    # the twin line, re-walked from its own definition (L(0)=2, L(1)=1)
    v = [2, 1]
    for _ in range(k - 1):
        v.append(v[-1] + v[-2])
    return v


def _s24_ceiling_check(end: int = 84) -> None:
    F = _s24_fibs(12)
    L = _s24_twin(11)
    assert (F[10], F[11], L[9], L[10]) == (55, 89, 76, 123), (F[10], F[11], L[9], L[10])
    assert F[10] <= end < F[11] and L[9] <= end < L[10], "the line-end census drifted"


def ref_s24_sumwalk(end: int = 84) -> str:
    F = _s24_fibs(12)
    on = F[1:11]
    assert on == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55] and F[11] > end, f"the sum walk drifted: {on}"
    return (
        "zero, one, one, two, three, five, eight, thirteen, twenty-one, thirty-four, and fifty-five: the "
        f"sum line runs ten steps on my line, each term the sum of the two before it, at the line end {end}"
    )


def ref_s24_twinwalk(end: int = 84) -> str:
    L = _s24_twin(11)
    on = L[1:10]
    assert on == [1, 3, 4, 7, 11, 18, 29, 47, 76] and L[10] > end, f"the twin walk drifted: {on}"
    return (
        "two, one, three, four, seven, eleven, eighteen, twenty-nine, forty-seven, and seventy-six: the "
        f"twin line runs nine steps on my line under the same rule, at the line end {end}"
    )


def ref_s24_doub(idx: str, end: int = 84) -> str:
    n = _S24_DOUB_N[idx]
    F = _s24_fibs(2 * n)
    L = _s24_twin(n)
    v = F[2 * n]
    assert F[2 * n] == F[n] * L[n] and v <= end, f"the doubling at index {n} drifted: {v}"
    W = _S24_NUM
    return (
        f"{W[v]}: the doubled term at index {W[2 * n]} — the {W[F[n]]}, the term at {W[n]}, times "
        f"the {W[L[n]]}, the twin at {W[n]} — is on my line, the welding of the two lines, at the "
        f"line end {end}"
    )


def ref_s24_sqsum(a: str, b: str, end: int = 84) -> str:
    W0 = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    n = W0[a]
    assert W0[b] == n + 1, "the pair is not consecutive"
    F = _s24_fibs(2 * n + 1)
    v = F[2 * n + 1]
    assert F[n] * F[n] + F[n + 1] * F[n + 1] == v and v <= end, f"the square sum at {n} drifted: {v}"
    W = _S24_NUM
    return (
        f"{W[v]}: the square sum of the term at {W[n]} and the term at {W[n + 1]}, two consecutive "
        f"terms of my sum line — {W[F[n]]} squared plus {W[F[n + 1]]} squared — is the term at index "
        f"{W[2 * n + 1]}, at the line end {end}"
    )


def ref_s24_twinterm(end: int = 84) -> str:
    L = _s24_twin(6)
    assert L[6] == L[4] + L[5] and L[6] <= end, f"the twin term drifted: {L[6]}"
    return (
        "eighteen: the twin term at index six — the seven at four and the eleven at five, the sum of the "
        f"two before it — under the same rule the twin line runs, at the line end {end}"
    )


def s24_sumterm_ref(end: int = 84) -> str:
    F = _s24_fibs(10)
    assert F[10] == F[8] + F[9] and F[10] <= end, f"the sum term drifted: {F[10]}"
    return (
        "fifty-five: the sum line's term at index ten — the twenty-one at eight and the thirty-four at "
        f"nine, the sum of the two before it — under the same rule the sum line runs, at the line end {end}"
    )


def ref_s24_filing(end: int = 84) -> str:
    # the filing's parts stand in the brainstem's S24 fact set
    assert B.S24_THEOREMS["twin-line-filed"]["parts"] == ("sum-line-def", "twin-line-def")
    slugs = {meta[1] for meta in B.S24_LESSONS.values()}
    assert set(B.S24_THEOREMS["twin-line-filed"]["parts"]) <= slugs
    _s24_ceiling_check(end)
    return (
        "the twin line, filed of record: the sum line runs by addition alone to the fifty-five and the "
        f"twin under the same rule to the seventy-six, the identities weld the two lines at every on-line "
        f"index, and the eighty-nine stands once more as the ceiling the line already declared; at the "
        f"line end {end}"
    )


def ref_s24_marker(post: bool = False, end: int = 84) -> str:
    """The marker census over the S24 seed (= the S23 final store:
    pre-band 18/2/24 of 44; post-derive 19/2/24 of 45 — the band's twin
    filing is the nineteenth line-end marker)."""
    store = _s24_seed_store()
    end_n = spot_n = none_n = 0
    for a in store.query(context_match={"kind": "theorem"}):
        if not isinstance(a.object, str):
            continue
        if "line end" in a.object:
            end_n += 1
        elif "at s = 2" in a.object:
            spot_n += 1
        else:
            none_n += 1
    if post:
        stmt = B.S24_THEOREMS["twin-line-filed"]["statement"]
        if "line end" in stmt:
            end_n += 1
    total = end_n + spot_n + none_n
    assert (end_n, spot_n, none_n, total) == (
        (19, 2, 24, 45) if post else (18, 2, 24, 44)
    ), f"the marker census drifted on the S24 seed: {(end_n, spot_n, none_n, total)}"
    W = {2: "two", 18: "eighteen", 19: "nineteen", 24: "twenty-four", 44: "forty-four", 45: "forty-five"}
    return (
        f"{W[end_n]} of my {W[total]} theorem facts close their scope at the line end, "
        f"{W[spot_n]} close on the line's spot marker, and {W[none_n]} carry the universal "
        f"form with no line end marker — a form of the line is not a census of its end, at the line end {end}"
    )


def ref_s24_offscript(end: int = 84) -> str:
    """The largest doubled term the line holds (re-computed: the walk
    n=1.. of F(2n) = F(n)*L(n) until the value crosses the line end —
    n=5 holds at the fifty-five, n=6 lands at the one forty-four, past
    the line end, at the ceiling's territory)."""
    F = _s24_fibs(12)
    L = _s24_twin(6)
    assert F[10] == F[5] * L[5] and F[10] <= end, f"the last on-line doubling drifted: {F[10]}"
    assert F[12] == F[6] * L[6] and F[12] > end, f"the past-line doubling drifted: {F[12]}"
    return (
        f"fifty-five: the doubled term at index ten — the five, the term at five, times the eleven, the "
        f"twin at five — is the largest doubled term my line holds; the next doubled term, at index "
        f"twelve, is the one forty-four, past the line end, the ceiling's territory, at the line end {end}"
    )


REGISTRY: dict[str, Callable[..., Any]] = {
    "family": ref_family,
    "telescope": ref_telescope,
    "removal": ref_removal,
    "removal_max": ref_removal_max,
    "set_removal": ref_set_removal,
    "set_removal_map": ref_set_removal_map,
    "census": ref_census,
    "removal_below2_count": ref_removal_below2_count,
    "telescope_spots": ref_telescope_spots,
    "telescope_named": ref_telescope_named,
    "spf": ref_spf,
    "spf_chain": ref_spf_chain,
    "order_s2": ref_order_s2,
    "ap_table": ref_ap_table,
    "fp_count": ref_fp_count,
    "cm_zeros": ref_cm_zeros,
    "small_points": ref_small_points,
    "gen_ledger": ref_gen_ledger,
    "lpartial": ref_lpartial,
    "lfactor": ref_lfactor,
    "lpartial_uniform": ref_lpartial_uniform,
    "lpartial_record": ref_lpartial_record,
    "lcorr": ref_lcorr,
    "ramified_pair": ref_ramified_pair,
    "s16_order": ref_s16_order,
    "s16_rank": ref_s16_rank,
    "s16_descend": ref_s16_descend,
    "s16_selmer": ref_s16_selmer,
    "s16_torsion": ref_s16_torsion,
    "s16_gen": ref_s16_gen,
    "s16_consistent": ref_s16_consistent,
    "s16_reach": ref_s16_reach,
    "s16_bsd": ref_s16_bsd,
    "s16_sides": ref_s16_sides,
    "s16_bandstate": ref_s16_bandstate,
    "s16_uncond": ref_s16_uncond,
    "s16_wall": ref_s16_wall,
    "s17_vp": ref_s17_vp,
    "s17_lte": ref_s17_lte,
    "s17_lte_ledger": ref_s17_lte_ledger,
    "s17_beal": ref_s17_beal,
    "s17_census": ref_s17_census,
    "s17_empt": ref_s17_empt,
    "s17_family": ref_s17_family,
    "s17_bandstate": ref_s17_bandstate,
    "s17_uncond": ref_s17_uncond,
    "s17_wall": ref_s17_wall,
    "s17_census_count": ref_s17_census_count,
    "s17_primitive_count": ref_s17_primitive_count,
    "s17_lte_instances": ref_s17_lte_instances,
    "s17_lte_failures": ref_s17_lte_failures,
    "s18_dec": ref_s18_dec,
    "s18_pi": ref_s18_pi,
    "s18_scan": ref_s18_scan,
    "s18_heavy": ref_s18_heavy,
    "s18_costspot": ref_s18_costspot,
    "s18_ph": ref_s18_ph,
    "s18_kill": ref_s18_kill,
    "s18_bandstate": ref_s18_bandstate,
    "s18_uncond": ref_s18_uncond,
    "s18_tam": ref_s18_tam,
    "s18_wall": ref_s18_wall,
    "s18_pi_count": ref_s18_pi_count,
    "s18_scan_cost": ref_s18_scan_cost,
    "s18_heavy_cost": ref_s18_heavy_cost,
    "s18_kill_totals": ref_s18_kill_totals,
    "s18_ph_total": ref_s18_ph_total,
    "s18_ph_violations": ref_s18_ph_violations,
    "s19_p": ref_s19_p,
    "s19_np": ref_s19_np,
    "s19_settle": ref_s19_settle,
    "s19_summit": ref_s19_summit,
    "s19_statement": ref_s19_statement,
    "s19_parity": ref_s19_parity,
    "s19_parcnf": ref_s19_parcnf,
    "s19_settle16": ref_s19_settle16,
    "s19_wall": ref_s19_wall,
    "s19_bandstate": ref_s19_bandstate,
    "s19_unc": ref_s19_unc,
    "s20_rhsummit": ref_s20_rhsummit,
    "s20_soil": ref_s20_soil,
    "s20_node": ref_s20_node,
    "s20_shape": ref_s20_shape,
    "s20_open": ref_s20_open,
    "s20_form": ref_s20_form,
    "s20_marker": ref_s20_marker,
    "s20_wallkind": ref_s20_wallkind,
    "s20_absence": ref_s20_absence,
    "s20_weavestate": ref_s20_weavestate,
    "s20_unc": ref_s20_unc,
    "s20_wall": ref_s20_wall,
    "s21_wall": ref_s21_wall,
    "s21_hypo": ref_s21_hypo,
    "s21_line": ref_s21_line,
    "s21_filing": ref_s21_filing,
    "s21_state_readout": ref_s21_state_readout,
    "s21_condgive": ref_s21_condgive,
    "s21_agree": ref_s21_agree,
    "s21_uncond": ref_s21_uncond,
    "s21_roads": ref_s21_roads,
    "s21_roads_cond": ref_s21_roads_cond,
    "s21_scalecount": ref_s21_scalecount,
    "s21_mlab": ref_s21_mlab,
    "s21_mroot": ref_s21_mroot,
    "s21_selved": ref_s21_selved,
    "s21_class": ref_s21_class,
    "s21_reachscale": ref_s21_reachscale,
    "s21_queue": ref_s21_queue,
    "s21_queue_lot": ref_s21_queue_lot,
    "s21_rhsummit": ref_s21_rhsummit,
    "s21_census": ref_s21_census,
    "s31_wall": ref_s31_wall,
    "s31_seeded": ref_s31_seeded,
    "s31_golden": ref_s31_golden,
    "s31_filing": ref_s31_filing,
    "s31_sumline": ref_s31_sumline,
    "s31_cassini": ref_s31_cassini,
    "s31_shift": ref_s31_shift,
    "s31_ratio": ref_s31_ratio,
    "s31_goldenwalk": ref_s31_goldenwalk,
    "s31_silence": ref_s31_silence,
    "s31_census": ref_s31_census,
    "s32_wall": ref_s32_wall,
    "s22_family": ref_s22_family,
    "s22_chain": ref_s22_chain,
    "s22_classwalk": ref_s22_classwalk,
    "s22_census": ref_s22_census,
    "s22_filing": ref_s22_filing,
    "s22_firstprime": ref_s22_firstprime,
    "s23_coprime": ref_s23_coprime,
    "s23_neverred": ref_s23_neverred,
    "s23_chain": ref_s23_chain,
    "s23_census": ref_s23_census,
    "s23_ceiling": ref_s23_ceiling,
    "s23_filing": ref_s23_filing,
    "s23_wall": ref_s23_wall,
    "s23_marker": ref_s23_marker,
    "s23_above2": ref_s23_above2,
    "s24_sumwalk": ref_s24_sumwalk,
    "s24_twinwalk": ref_s24_twinwalk,
    "s24_doub": ref_s24_doub,
    "s24_sqsum": ref_s24_sqsum,
    "s24_sumterm": s24_sumterm_ref,
    "s24_twinterm": ref_s24_twinterm,
    "s24_filing": ref_s24_filing,
    "s24_marker": ref_s24_marker,
    "s24_offscript": ref_s24_offscript,
    "s32_period": ref_s32_period,
    "s32_offline": ref_s32_offline,
    "s32_pisano8": ref_s32_pisano8,
    "s32_pisano12": ref_s32_pisano12,
    "s32_shadow": ref_s32_shadow,
    "s32_value": ref_s32_value,
    "s32_parity": ref_s32_parity,
    "s32_divides": ref_s32_divides,
    "s32_pagenames": ref_s32_pagenames,
    "s32_belowzero": ref_s32_belowzero,
    "s32_recip89": ref_s32_recip89,
    "s32_goldenpower": ref_s32_goldenpower,
    "s32_lucas": ref_s32_lucas,
    "s32_filing": ref_s32_filing,
    "s32_census": ref_s32_census,
}

#: Fraction renderers for the beds table.
RENDERERS: dict[str, Callable[[Any], Any]] = {
    "slash": _frac_slash,
    "frac_words": _frac_words,
    "json": lambda v: v,
}


def evaluate(ref_name: str, args: dict[str, Any]) -> Any:
    if ref_name not in REGISTRY:
        raise KeyError(f"unknown bed reference {ref_name!r} (registry: {sorted(REGISTRY)})")
    return REGISTRY[ref_name](**args)
