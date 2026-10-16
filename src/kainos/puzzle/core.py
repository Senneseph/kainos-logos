"""E4.1 constraint core — a generic n-dimensional logical-grid solver.

The core knows NOTHING about Einstein's riddle. A ``PuzzleSpec`` is data:
``houses`` positions, an ordered list of ``Dimension``s (each with a
declared term vocabulary and, optionally, terms the system does not KNOW —
"typed but unknown", rendered as typed placeholders ``<name>:u<k>``), and a
list of ``Clue``s in four canonical forms:

- ``At(dim, term, pos)``       — the term sits at position ``pos``
- ``Pair(da, ta, db, tb)``     — ta and tb sit at the SAME position
- ``Left(da, ta, db, tb)``     — ta is immediately left of tb (pos + 1)
- ``Next(da, ta, db, tb)``     — ta and tb are at ADJACENT positions

Every dimension is a bijection between terms and positions (the stated
axiom "all different": each term used exactly once, each position occupied
by exactly one term).

The solver is deterministic:

1. **Forward chaining** — candidate-position domains per (dim, term),
   narrowed by clues (in declared order) and by the two all-different
   inferences (hidden single / naked single), to a fixpoint. Every
   narrowing is LOGGED: ``(variable, removed_positions, cause)`` where
   ``cause`` names the clue or the axiom. For any solution, the log of its
   search path, replayed from the initial domains, reproduces the
   assignment exactly — that IS the proof chain.
2. **Backtracking** — when consistent but not complete, branch on the
   smallest domain (deterministic tie-break: dimension order, term order),
   values ascending.
3. **Uniqueness** — the search continues after the first solution; up to
   ``cap`` solutions are enumerated (2 suffices to prove/refute uniqueness).
4. **Contradiction certificate** — on domain wipeout, the clue ids that
   fired before the wipeout are collected and inclusion-minimalised by
   deletion re-testing: :func:`minimal_certificate` returns a clue set
   that is unsatisfiable and becomes satisfiable if any member is removed
   (the all-different axiom is a stated premise, never listed).
5. **Degradation machinery** (the E4.1 arms):
   - hidden terms become typed placeholders; ``Solution.gaps()`` states
     EXACTLY which cells are occupied but unnameable (the honest "I need x
     piece of information" contract, arm B);
   - :func:`undetermined_facts` — per variable, the positions it occupies
     across ALL solutions of an under-determined spec (arm C: says exactly
     what is undetermined, against which alternatives);
   - :func:`resolving_facts` — the canonical ``At`` facts over
     undetermined variables that, added, restore a unique consistent
     solution (arm C: names exactly what would fix it).
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "ENUMERATION_CAP",
    "At",
    "Clue",
    "Contradiction",
    "Dimension",
    "Gap",
    "Left",
    "Next",
    "Pair",
    "PuzzleSpec",
    "Solution",
    "SolveReport",
    "minimal_certificate",
    "resolving_facts",
    "solve",
    "undetermined_facts",
]

#: The one structural axiom (stated in every verdict; never listed as a clue).
AXIOM_ALLDIFF = "all-different: each dimension is a bijection terms<->positions"

#: Maximum solutions enumerated under degradation (arm C / certificates).
ENUMERATION_CAP = 400


# ── the spec (data, not code) ──────────────────────────────────────────────


@dataclass(frozen=True)
class Dimension:
    """One row of the grid: a name, its full vocabulary, and the terms the
    system does NOT know (rendered as typed placeholders ``<name>:u<k>``)."""

    name: str
    terms: tuple[str, ...]
    hidden: frozenset[str] = frozenset()

    def placeholders(self) -> dict[str, str]:
        """true term -> placeholder name for hidden terms (sorted order)."""

        out: dict[str, str] = {}
        for k, term in enumerate(sorted(t for t in self.terms if t in self.hidden), 1):
            out[term] = f"{self.name}:u{k}"
        return out

    def visible(self) -> tuple[str, ...]:
        """The vocabulary the solver is allowed to NAME (known + placeholders),
        in declared term order."""

        ph = self.placeholders()
        return tuple(ph.get(t, t) for t in self.terms)


@dataclass(frozen=True)
class At:
    """The term sits at position ``pos`` (1-based, left to right)."""

    dim: str
    term: str
    pos: int

    @property
    def text(self) -> str:
        return f"{self.term} ({self.dim}) is at position {self.pos}"


@dataclass(frozen=True)
class Pair:
    """The two terms sit at the SAME position."""

    dim_a: str
    term_a: str
    dim_b: str
    term_b: str

    @property
    def text(self) -> str:
        return f"{self.term_a} ({self.dim_a}) is with {self.term_b} ({self.dim_b})"


@dataclass(frozen=True)
class Left:
    """A is IMMEDIATELY left of B: pos(a) = pos(b) - 1.

    (The English "on the left of" is ambiguous — adjacent or not; this core
    uses the adjacent reading, the stricter one. See deviation D-e1 in the
    phase-4 results: if the given clue text is unsatisfiable under this
    reading the phase-4 spec records which reading solves the puzzle and
    adopts that, once, documented.)
    """

    dim_a: str
    term_a: str
    dim_b: str
    term_b: str

    @property
    def text(self) -> str:
        return f"{self.term_a} ({self.dim_a}) is immediately left of {self.term_b} ({self.dim_b})"


@dataclass(frozen=True)
class Next:
    """A and B are at ADJACENT positions (order either way)."""

    dim_a: str
    term_a: str
    dim_b: str
    term_b: str

    @property
    def text(self) -> str:
        return f"{self.term_a} ({self.dim_a}) is next to {self.term_b} ({self.dim_b})"


Clue = At | Pair | Left | Next


@dataclass(frozen=True)
class PuzzleSpec:
    """The whole puzzle as data: positions, dimensions, clues (in order).
    A new puzzle = a new spec; the core code never changes (arm E relies
    on exactly this)."""

    houses: int
    dimensions: tuple[Dimension, ...]
    clues: tuple[Clue, ...]

    @property
    def dim_order(self) -> dict[str, int]:
        return {d.name: i for i, d in enumerate(self.dimensions)}

    def dim(self, name: str) -> Dimension:
        for d in self.dimensions:
            if d.name == name:
                return d
        raise KeyError(f"unknown dimension {name!r}")

    def visible_terms(self, dim_name: str) -> tuple[str, ...]:
        """The vocabulary the solver may use for this dimension."""

        return self.dim(dim_name).visible()

    def with_clues(self, clues: tuple[Clue, ...]) -> PuzzleSpec:
        return PuzzleSpec(self.houses, self.dimensions, clues)

    def with_hidden(self, dim_name: str, hidden: frozenset[str]) -> PuzzleSpec:
        dims = tuple(d if d.name != dim_name else Dimension(d.name, d.terms, hidden) for d in self.dimensions)
        return PuzzleSpec(self.houses, dims, self.clues)

    def variable_keys(self) -> list[tuple[str, str]]:
        """All (dim, term) variables in deterministic order."""

        return [(d.name, t) for d in self.dimensions for t in d.visible()]


# ── the derivation (the proof chain) ───────────────────────────────────────


@dataclass(frozen=True)
class ProofStep:
    """One logged narrowing: variable (dim, term), removed positions, cause.

    ``cause`` is either ``clue#<i>: <text>`` or ``axiom: ...`` or
    ``search: branch <p>``; replaying the steps of a solution's path from
    the initial domains reproduces its assignment (verified in tests)."""

    dim: str
    term: str
    removed: tuple[int, ...]
    cause: str

    @property
    def clue_id(self) -> int | None:
        if self.cause.startswith("clue#"):
            return int(self.cause[5:].split(":", 1)[0])
        return None


@dataclass(frozen=True)
class Contradiction(Exception):
    """A domain wipeout: the fired clue ids (certificate seed) and reason.

    Carries data AND raises: the solver ``raise``s it, tests ``except`` it."""

    clue_ids: tuple[int, ...]
    reason: str = ""


@dataclass(frozen=True)
class Gap:
    """A typed-but-unnameable cell (arm B): the honest 'I need x' statement."""

    dim: str
    placeholder: str
    pos: int
    cell: dict[str, str]
    statement: str


# ── propagation ────────────────────────────────────────────────────────────


def _causes_for(clues: tuple[Clue, ...]) -> list[str]:
    return [f"clue#{i}: {c.text}" for i, c in enumerate(clues)]


def _apply_clauses(
    spec: PuzzleSpec,
    doms: dict[tuple[str, str], frozenset[int]],
    log: list[ProofStep],
) -> bool:
    """One pass of clause application (clues in declared order)."""

    causes = _causes_for(spec.clues)
    changed = False

    def shrink(key: tuple[str, str], keep: frozenset[int], cause: str) -> None:
        nonlocal changed
        dom = doms[key]
        new = dom & keep
        if new != dom:
            doms[key] = new
            log.append(ProofStep(key[0], key[1], tuple(sorted(dom - new)), cause))
            changed = True

    for clue, cause in zip(spec.clues, causes, strict=True):
        if isinstance(clue, At):
            shrink((clue.dim, clue.term), frozenset({clue.pos}), cause)
        elif isinstance(clue, Pair):
            ka, kb = (clue.dim_a, clue.term_a), (clue.dim_b, clue.term_b)
            inter = doms[ka] & doms[kb]
            shrink(ka, inter, cause)
            shrink(kb, doms[ka] & doms[kb], cause)
        elif isinstance(clue, Left):
            ka, kb = (clue.dim_a, clue.term_a), (clue.dim_b, clue.term_b)
            shrink(ka, frozenset(p for p in doms[ka] if p + 1 in doms[kb]), cause)
            shrink(kb, frozenset(p for p in doms[kb] if p - 1 in doms[ka]), cause)
        elif isinstance(clue, Next):
            ka, kb = (clue.dim_a, clue.term_a), (clue.dim_b, clue.term_b)
            shrink(ka, frozenset(p for p in doms[ka] if any(abs(p - q) == 1 for q in doms[kb])), cause)
            shrink(kb, frozenset(p for p in doms[kb] if any(abs(p - q) == 1 for q in doms[ka])), cause)
    return changed


def _apply_alldiff(
    spec: PuzzleSpec,
    doms: dict[tuple[str, str], frozenset[int]],
    log: list[ProofStep],
) -> bool:
    """Hidden singles / naked singles per dimension, spec order, positions
    ascending. The stated axiom, never a listed clue."""

    changed = False

    def shrink(key: tuple[str, str], keep: frozenset[int], cause: str) -> None:
        nonlocal changed
        dom = doms[key]
        new = dom & keep
        if new != dom:
            doms[key] = new
            log.append(ProofStep(key[0], key[1], tuple(sorted(dom - new)), cause))
            changed = True

    for d in spec.dimensions:
        terms = list(d.visible())
        cause = f"axiom: {AXIOM_ALLDIFF} ({d.name})"
        for t in terms:  # hidden single: a term with one candidate takes it
            dom = doms[(d.name, t)]
            if len(dom) == 1:
                p = next(iter(dom))
                for t2 in terms:
                    if t2 != t:
                        shrink((d.name, t2), frozenset({q for q in doms[(d.name, t2)] if q != p}), cause)
        for p in range(1, spec.houses + 1):  # naked single: one term fits a position
            candidates = [t for t in terms if p in doms[(d.name, t)]]
            if len(candidates) == 1:
                for t2 in terms:
                    if t2 != candidates[0]:
                        shrink((d.name, t2), frozenset({q for q in doms[(d.name, t2)] if q != p}), cause)
    return changed


def _to_fixpoint(
    spec: PuzzleSpec,
    doms: dict[tuple[str, str], frozenset[int]],
    log: list[ProofStep],
) -> None:
    """Alternate clause and axiom passes until stable.

    Raises:
        Contradiction: on any domain wipeout, with the clue ids that fired
        for the emptied variable (the certificate seed — minimalised later
        by :func:`minimal_certificate`).
    """

    while True:
        changed = _apply_clauses(spec, doms, log) or _apply_alldiff(spec, doms, log)
        for key in spec.variable_keys():
            if not doms[key]:
                fired: set[int] = set()
                for step in log:
                    if step.dim == key[0] and step.term == key[1] and step.clue_id is not None:
                        fired.add(step.clue_id)
                last = next((s for s in reversed(log) if s.dim == key[0] and s.term == key[1]), None)
                if not fired:
                    # the wipeout fired without clue steps for this variable
                    # (pure axiom interplay): seed with every clue that fired
                    fired = {s.clue_id for s in log if s.clue_id is not None}
                reason = f"{key[0]}/{key[1]} wiped out by {last.cause}" if last else f"{key[0]}/{key[1]} empty"
                raise Contradiction(clue_ids=tuple(sorted(fired)), reason=reason)
        if not changed:
            return


# ── deterministic backtracking search ──────────────────────────────────────


def _branch_var(
    spec: PuzzleSpec,
    doms: dict[tuple[str, str], frozenset[int]],
) -> tuple[str, str] | None:
    free = {k: v for k, v in doms.items() if len(v) > 1}
    if not free:
        return None
    return min(free, key=lambda k: (len(doms[k]), spec.dim_order[k[0]], k[1]))


def _search(
    spec: PuzzleSpec,
    doms: dict[tuple[str, str], frozenset[int]],
    log: list[ProofStep],
    branches: list[tuple[str, str, int]],
    solutions: list[Solution],
    cap: int,
) -> None:
    if len(solutions) >= cap:
        return
    v = _branch_var(spec, doms)
    if v is None:
        if all(len(d) == 1 for d in doms.values()):
            assignment = {k: next(iter(d)) for k, d in doms.items()}
            proof = {k: tuple(s for s in log if (s.dim, s.term) == k) for k in assignment}
            solutions.append(Solution(assignment=assignment, proof=proof, branches=tuple(branches)))
        return
    for value in sorted(doms[v]):
        if len(solutions) >= cap:
            break
        # Per-trial COPY of the domains (shallow copy suffices: domains are
        # frozensets, never mutated in place) and an extended log.
        # _to_fixpoint mutates its argument on the way to a contradiction;
        # with a copy those mutations can't leak into sibling branches
        # (the earlier restore-one-var scheme leaked and pruned valid sols).
        trial = dict(doms)
        trial[v] = frozenset({value})
        tlog = log + [
            ProofStep(v[0], v[1], tuple(sorted(doms[v] - frozenset({value}))), f"search: branch {value}")
        ]
        tbranches = branches + [(v[0], v[1], value)]
        try:
            _to_fixpoint(spec, trial, tlog)
        except Contradiction:
            continue
        _search(spec, trial, tlog, tbranches, solutions, cap)


@dataclass
class Solution:
    """One complete grid: (dim, term) -> position, its proof chain, and the
    search decisions on its path (empty for a pure-propagation solve)."""

    assignment: dict[tuple[str, str], int]
    proof: dict[tuple[str, str], tuple[ProofStep, ...]]
    branches: tuple[tuple[str, str, int], ...]

    def pos(self, dim: str, term: str) -> int:
        return self.assignment[(dim, term)]

    def cell(self, pos: int, spec: PuzzleSpec) -> dict[str, str]:
        """The occupant of a position, named in the visible vocabulary."""

        return {
            d.name: next(t for t in d.visible() if self.assignment[(d.name, t)] == pos)
            for d in spec.dimensions
        }

    def gaps(self, spec: PuzzleSpec) -> tuple[Gap, ...]:
        """Every cell the solver occupies but CANNOT name (typed unknowns).

        This is the honesty contract: the system KNOWS the cell (it can
        locate it, describe its other attributes) and says EXACTLY what is
        missing — one term of a named dimension — instead of inventing one.
        """

        out: list[Gap] = []
        for d in spec.dimensions:
            for term, name in sorted(d.placeholders().items()):
                p = self.assignment[(d.name, name)]
                out.append(
                    Gap(
                        dim=d.name,
                        placeholder=name,
                        pos=p,
                        cell=self.cell(p, spec),
                        statement=(
                            f"the {d.name} at position {p} is a member of the {d.name} vocabulary "
                            f"I was not given a term for ({len(d.hidden)} such term(s) total); "
                            f"providing that name would let me name this cell — I will not invent one"
                        ),
                    )
                )
        return tuple(sorted(out, key=lambda g: (g.pos, g.dim)))

    def as_grid(self, spec: PuzzleSpec) -> list[dict[str, str]]:
        """Human layout: one row per position (1..houses), dim -> visible name."""

        return [self.cell(p, spec) for p in range(1, spec.houses + 1)]


@dataclass
class SolveReport:
    """The solver's complete, deterministic answer to one spec.

    Status contract (the arm C checks rely on it):
      - ``solved``          : exactly ONE solution (``unique`` is True);
      - ``underdetermined`` : >1 solution — either exactly ``solutions`` (the
        search explored exhaustively, ``capped`` False) or at least
        ``len(solutions)`` of them (enumeration hit ``cap``, ``capped`` True);
      - ``no_solution``     : unsatisfiable (see ``contradiction``).
    """

    status: str  # "solved" | "no_solution" | "underdetermined"
    solutions: list[Solution]
    unique: bool
    contradiction: Contradiction | None
    cap: int
    capped: bool = False  # enumeration stopped at the cap (more solutions may exist)


def _initial_domains(spec: PuzzleSpec) -> dict[tuple[str, str], frozenset[int]]:
    full = frozenset(range(1, spec.houses + 1))
    return {key: full for key in spec.variable_keys()}


def solve(spec: PuzzleSpec, cap: int = 2) -> SolveReport:
    """Forward-chain + deterministic backtracking; up to ``cap`` solutions.

    ``status == "solved"`` iff the spec has EXACTLY one solution."""

    doms = _initial_domains(spec)
    log: list[ProofStep] = []
    try:
        _to_fixpoint(spec, doms, log)
    except Contradiction as c:
        return SolveReport(status="no_solution", solutions=[], unique=False, contradiction=c, cap=cap)
    solutions: list[Solution] = []
    _search(spec, doms, log, [], solutions, cap)
    if not solutions:
        return SolveReport(status="no_solution", solutions=[], unique=False, contradiction=None, cap=cap)
    if len(solutions) == 1:
        return SolveReport(status="solved", solutions=solutions, unique=True, contradiction=None, cap=cap)
    return SolveReport(
        status="underdetermined",
        solutions=solutions,
        unique=False,
        contradiction=None,
        cap=cap,
        capped=len(solutions) >= cap,
    )


# ── contradiction certificates (arm D) ─────────────────────────────────────


def minimal_certificate(spec: PuzzleSpec, seed_clue_ids: tuple[int, ...]) -> list[int]:
    """Inclusion-minimal subset of the GIVEN clue ids (clues only; the
    all-different axiom is a stated premise, never listed) that is still
    unsatisfiable: remove any listed clue and the rest is satisfiable.
    Deterministic (ascending deletion order, re-tested with ``solve``)."""

    core = list(dict.fromkeys(seed_clue_ids))
    for cid in list(core):
        reduced = spec.with_clues(tuple(c for i, c in enumerate(spec.clues) if i != cid))
        if solve(reduced, cap=1).status == "no_solution":
            core.remove(cid)
    return sorted(core)


# ── degradation machinery (arms B / C) ────────────────────────────────────


def undetermined_facts(solutions: list[Solution]) -> dict[tuple[str, str], tuple[int, ...]]:
    """Per (dim, term): the positions it occupies ACROSS all given
    solutions. A 1-tuple is determined; a longer tuple says EXACTLY what is
    undetermined and its alternatives (arm C's output; callers filter on
    ``len > 1`` for the undetermined ones)."""

    out: dict[tuple[str, str], set[int]] = {}
    for sol in solutions:
        for key, p in sol.assignment.items():
            out.setdefault(key, set()).add(p)
    return {k: tuple(sorted(v)) for k, v in out.items()}


def resolving_facts(spec: PuzzleSpec) -> list[tuple[At, SolveReport]]:
    """Every canonical ``At`` fact over a currently-UNDETERMINED variable
    that (a) is consistent with the spec and (b) restores a unique
    solution — i.e. names EXACTLY what would fix a missing clue (arm C)."""

    base = solve(spec, cap=ENUMERATION_CAP)
    if base.unique or not base.solutions:
        return []
    vary = {k: v for k, v in undetermined_facts(base.solutions).items() if len(v) > 1}
    out: list[tuple[At, SolveReport]] = []
    for (dim, term) in sorted(vary, key=lambda k: (spec.dim_order[k[0]], k[1])):
        for pos in vary[(dim, term)]:
            fact = At(dim=dim, term=term, pos=pos)
            report = solve(spec.with_clues(spec.clues + (fact,)), cap=2)
            if report.status == "solved" and report.unique:
                out.append((fact, report))
    return out
