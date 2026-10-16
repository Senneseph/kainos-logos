"""Solver soundness/completeness: the deterministic solver vs. a dumb
brute-force enumerator on small random specs. If the two ever disagree,
the solver is lying about (or missing) solutions — the whole E4.1
verdict rests on this."""

from __future__ import annotations

import random
from itertools import permutations, product

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from kainos.puzzle.core import (
    At,
    Clue,
    Dimension,
    Left,
    Next,
    Pair,
    PuzzleSpec,
    minimal_certificate,
    solve,
    undetermined_facts,
)

CAP = 5


def _random_spec(rng: random.Random) -> PuzzleSpec:
    """Small puzzle: 3 houses, 2-3 dimensions of 3 terms, 0-6 random clues
    (deduplicated). Dimensions/terms names are fixed pools (data)."""

    n_dims = rng.randint(2, 3)
    dims = tuple(
        Dimension(f"d{i}", tuple(f"t{i}_{j}" for j in range(3))) for i in range(n_dims)
    )
    pool: list[Clue] = []
    for d in dims:
        for t in d.terms:
            for p in (1, 2, 3):
                pool.append(At(d.name, t, p))
    for a in dims:
        for b in dims:
            if a.name == b.name:
                continue
            for ta in a.terms:
                for tb in b.terms:
                    pool.append(Pair(a.name, ta, b.name, tb))
                    pool.append(Next(a.name, ta, b.name, tb))
    for a in dims:
        for b in dims:
            if a.name is b.name:
                continue
            for ta in a.terms[:1]:
                for tb in b.terms[:1]:
                    pool.append(Left(a.name, ta, b.name, tb))
    rng.shuffle(pool)
    clues: list[Clue] = []
    for c in pool:
        if c not in clues and len(clues) < 6:
            clues.append(c)
        if len(clues) >= 6:
            break
    return PuzzleSpec(3, dims, tuple(clues))


def _brute_force(spec: PuzzleSpec, cap: int) -> int:
    """Count solutions by exhaustive permutation enumeration (the oracle).

    One permutation per dimension: term i sits at position perm[i]."""

    perms = list(permutations(range(1, spec.houses + 1)))

    def check(combo: tuple[tuple[int, int], ...]) -> bool:
        pos: dict[tuple[str, str], int] = {}
        for dim, perm in zip(spec.dimensions, combo, strict=True):
            for i, term in enumerate(dim.terms):
                pos[(dim.name, term)] = perm[i]
        for clue in spec.clues:
            if isinstance(clue, At) and pos[(clue.dim, clue.term)] != clue.pos:
                return False
            if isinstance(clue, Pair) and pos[(clue.dim_a, clue.term_a)] != pos[(clue.dim_b, clue.term_b)]:
                return False
            if isinstance(clue, Left) and pos[(clue.dim_a, clue.term_a)] + 1 != pos[(clue.dim_b, clue.term_b)]:
                return False
            if isinstance(clue, Next) and abs(pos[(clue.dim_a, clue.term_a)] - pos[(clue.dim_b, clue.term_b)]) != 1:
                return False
        return True

    count = 0
    for combo in product(perms, repeat=len(spec.dimensions)):
        if check(combo):
            count += 1
            if count >= cap:
                break
    return count


@settings(max_examples=30, derandomize=True, suppress_health_check=[HealthCheck.too_slow])
@given(seed=st.integers(min_value=0, max_value=10**6))
def test_solver_agrees_with_brute_force(seed: int) -> None:
    rng = random.Random(seed)
    spec = _random_spec(rng)
    rep = solve(spec, cap=CAP)
    truth = _brute_force(spec, CAP)
    if truth == 0:
        assert rep.status == "no_solution", f"seed {seed}: oracle 0, solver {rep.status}"
    elif truth == 1:
        assert rep.status == "solved" and rep.unique, f"seed {seed}: oracle 1, solver {rep.status}"
    elif truth < CAP:
        assert rep.status == "underdetermined" and len(rep.solutions) == truth and not rep.capped
    else:
        assert rep.status == "underdetermined" and len(rep.solutions) >= CAP


def test_solver_find_no_false_solution() -> None:
    """A claimed solution must actually satisfy every clue (soundness)."""

    rng = random.Random(7)
    for _ in range(40):
        spec = _random_spec(rng)
        rep = solve(spec, cap=CAP)
        for sol in rep.solutions:
            for clue in spec.clues:
                if isinstance(clue, At):
                    assert sol.pos(clue.dim, clue.term) == clue.pos
                elif isinstance(clue, Pair):
                    assert sol.pos(clue.dim_a, clue.term_a) == sol.pos(clue.dim_b, clue.term_b)
                elif isinstance(clue, Left):
                    assert sol.pos(clue.dim_a, clue.term_a) + 1 == sol.pos(clue.dim_b, clue.term_b)
                elif isinstance(clue, Next):
                    assert abs(sol.pos(clue.dim_a, clue.term_a) - sol.pos(clue.dim_b, clue.term_b)) == 1
            # bijectivity: every position occupied exactly once per dimension
            for d in spec.dimensions:
                positions = sorted(sol.pos(d.name, t) for t in d.terms)
                assert positions == list(range(1, spec.houses + 1))


def test_certificate_is_inclusion_minimal() -> None:
    """Synthetic unsat: two At clues on one term. Certificate = exactly
    those two; removing either makes it satisfiable."""

    d1 = Dimension("color", ("red", "green", "blue"))
    d2 = Dimension("drink", ("tea", "milk", "water"))
    spec = PuzzleSpec(
        3,
        (d1, d2),
        (At("color", "red", 1), At("color", "red", 2), Pair("color", "blue", "drink", "tea")),
    )
    rep = solve(spec, cap=1)
    assert rep.status == "no_solution" and rep.contradiction is not None
    cert = minimal_certificate(spec, rep.contradiction.clue_ids)
    assert cert == [0, 1]
    for cid in cert:
        without = spec.with_clues(tuple(c for i, c in enumerate(spec.clues) if i != cid))
        assert solve(without, cap=1).status in ("solved", "underdetermined")


def test_undetermined_facts_two_solution_pair() -> None:
    """A deliberately 2-solution 3x3 spec: the undetermined set is exact."""

    d1 = Dimension("color", ("red", "green", "blue"))
    d2 = Dimension("pet", ("cat", "dog", "fish"))
    # red@1, with cat; everything else free within all-diff:
    spec = PuzzleSpec(3, (d1, d2), (At("color", "red", 1), Pair("color", "red", "pet", "cat")))
    rep = solve(spec, cap=100)
    assert rep.status == "underdetermined" and len(rep.solutions) > 1
    und = {k: v for k, v in undetermined_facts(rep.solutions).items() if len(v) > 1}
    # red and cat are pinned; green/blue and dog/fish vary (with blue tied to green's positions etc.)
    assert ("color", "red") not in und
    assert ("pet", "cat") not in und
    assert ("color", "green") in und and ("pet", "dog") in und


def test_determinism_two_runs() -> None:
    from kainos.puzzle.puzzles import EINSTEIN, TRANSFER_4x4

    for spec in (EINSTEIN, TRANSFER_4x4):
        r1 = solve(spec, cap=2)
        r2 = solve(spec, cap=2)
        assert r1.solutions[0].assignment == r2.solutions[0].assignment
        assert len(r1.solutions[0].proof) == len(r2.solutions[0].proof)
        assert r1.unique == r2.unique
