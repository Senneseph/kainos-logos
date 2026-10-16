"""E4.1 runner — constraint-propagation robustness under degradation.

Arms per ``plan/90-appendices/lateral-thinking-game.md`` + Q14 (frozen
choices in ``plan/30-phases/phase-4-robustness/experiments.md``):

- **A full puzzle** (Einstein's riddle, 5x5, clue-for-clue): solved
  UNIQUELY with a proof chain; the fish question answered; every proof
  step REPLAYS from the initial domains to the final assignment.
- **B partial term knowledge**: the pet term ``fish`` is typed-but-unknown
  (placeholder). The grid still completes uniquely; the system says
  EXACTLY which cell it cannot name ("I need x piece of information") and
  names NOTHING outside the given vocabulary (no hallucination).
- **C missing clue**: clue #11 ("horses next to Dunhill") absent =>
  EXACTLY two solutions. The system reports the EXACT undetermined facts
  (per variable, the positions that vary) and names a canonical ``At``
  fact whose addition restores the unique true solution.
- **D contradictory clue**: "the Norwegian lives in the fifth house"
  appended => unsatisfiable, with an INCLUSION-MINIMAL contradiction
  certificate (exactly the two Norwegian clues) and a minimality
  self-check.
- **E pattern transfer**: a different 4x4 puzzle (new dimension names, no
  house/colour) solved by the SAME core code, uniquely, with a replayable
  proof.
- **F LLM surface arm** (optional): mapped surface sentence -> structured
  clue, via the owner's optional Ollama; SKIP semantics (the deterministic
  core is the verdict).

``value`` = passed deterministic checks / 14 (pre-registered). The F arm
is reported but NOT part of the 14 (design decision, D-m8 in results.md).

Deterministic: no RNG anywhere in the arms; the only env dependence is the
optional F arm. Exit 0 iff all 14 checks pass.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from kainos.harness.paths import default_results_dir
from kainos.puzzle.core import (
    At,
    PuzzleSpec,
    Solution,
    minimal_certificate,
    resolving_facts,
    solve,
    undetermined_facts,
)
from kainos.puzzle.puzzles import (
    EINSTEIN,
    EINSTEIN_CONTRADICTION_CLUE,
    EINSTEIN_CONTRADICTION_TEXT,
    EINSTEIN_FISH_TERM,
    EINSTEIN_HIDDEN_ARM,
    TRANSFER_4x4,
)

__all__ = ["E4_1Experiment", "run_e4_1"]

#: Enumeration bound for the multi-solution arms (exact counts expected).
ENUMERATE_CAP = 400

#: Pre-registered arm C choice: 0-based index of the dropped clue (#11,
#: 1-based: "The man who keeps horses lives next to the man who smokes
#: Dunhill"). Dev-verified: its removal leaves EXACTLY two solutions and
#: admits single-At resolutions (every other drop was checked too; the
#: full drop table is in experiments.md).
ARM_C_DROPPED_CLUE = 10

#: Ground truth for arm A (verified by hand against all 15 clue texts with
#: the declared adjacent-Left semantics; the solver derives it
#: independently — this is the scorer's oracle, not an input).
EINSTEIN_TRUTH: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str], dict[str, str]] = (
    {"color": "yellow", "nationality": "norwegian", "drink": "water", "cigar": "dunhill", "pet": "cats"},
    {"color": "blue", "nationality": "dane", "drink": "tea", "cigar": "blends", "pet": "horses"},
    {"color": "red", "nationality": "brit", "drink": "milk", "cigar": "pall_mall", "pet": "birds"},
    {"color": "green", "nationality": "german", "drink": "coffee", "cigar": "prince", "pet": "fish"},
    {"color": "white", "nationality": "swede", "drink": "beer", "cigar": "blue_master", "pet": "dogs"},
)

#: Ground truth for arm E (same dev-verification discipline).
TRANSFER_TRUTH: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]] = (
    {"wall": "green", "person": "ada", "meal": "rice", "music": "cello"},
    {"wall": "blue", "person": "cy", "meal": "salmon", "music": "drums"},
    {"wall": "gold", "person": "dee", "meal": "lamb", "music": "jazz"},
    {"wall": "red", "person": "ben", "meal": "tofu", "music": "piano"},
)


def _grid(sol: Solution, spec: PuzzleSpec) -> list[dict[str, str]]:
    return sol.as_grid(spec)


def _replay_proof(spec: PuzzleSpec, sol: Solution) -> tuple[bool, str]:
    """Replay each variable's proof steps from the initial full domains;
    the final domain must be exactly the assigned position, and every
    clue cause must reference a real clue id. The proof chain is
    SUFFICIENT (not merely consistent)."""

    full = frozenset(range(1, spec.houses + 1))
    n_clues = len(spec.clues)
    for key, pos in sorted(sol.assignment.items()):
        steps = sol.proof[key]
        if not steps:
            return False, f"{key}: empty proof"
        dom = full
        for step in steps:
            dom = dom - frozenset(step.removed)
            if step.clue_id is not None and not (0 <= step.clue_id < n_clues):
                return False, f"{key}: proof references clue#{step.clue_id} out of range"
        if dom != frozenset({pos}):
            return False, f"{key}: replay ends at {sorted(dom)}, assigned {pos}"
    return True, "all proofs replay to their assignments"


def _named_values(spec: PuzzleSpec, sol: Solution) -> set[tuple[str, str]]:
    return {(row_dim, val) for row in _grid(sol, spec) for row_dim, val in row.items()}


def _visible_vocab(spec: PuzzleSpec) -> set[tuple[str, str]]:
    return {(d.name, t) for d in spec.dimensions for t in d.visible()}


def _check(checks: list[dict[str, Any]], name: str, ok: bool, why: str) -> None:
    checks.append({"name": name, "passed": bool(ok), "detail": why})


def _arm_a() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    detail: dict[str, Any] = {}
    rep = solve(EINSTEIN, cap=2)
    detail["status"] = rep.status
    detail["n_solutions"] = len(rep.solutions)

    _check(checks, "A1 unique solution", rep.status == "solved" and rep.unique, f"status={rep.status}, n={len(rep.solutions)}")
    sol = rep.solutions[0] if rep.solutions else None
    grid = _grid(sol, EINSTEIN) if sol else []
    _check(checks, "A2 grid = ground truth", bool(grid) and grid == list(EINSTEIN_TRUTH), json.dumps(grid, sort_keys=True))
    fish_pos = sol.pos("pet", EINSTEIN_FISH_TERM) if sol else None
    fish_cell = (grid[fish_pos - 1] if sol and fish_pos is not None else {})
    _check(
        checks,
        "A3 who owns the fish: the German, house 4",
        fish_pos == 4 and fish_cell.get("nationality") == "german" and fish_cell.get("color") == "green",
        f"fish at position {fish_pos}: {fish_cell}",
    )
    if sol:
        ok, why = _replay_proof(EINSTEIN, sol)
    else:
        ok, why = False, "no solution to replay"
    _check(checks, "A4 proof chains replay", ok, why)
    detail["fish_answer"] = {"position": fish_pos, "cell": fish_cell}
    detail["branches"] = [list(b) for b in sol.branches] if sol else []
    return checks, {**detail, "sol": sol, "rep": rep}


def _arm_b() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    detail: dict[str, Any] = {}
    spec = EINSTEIN.with_hidden("pet", EINSTEIN_HIDDEN_ARM)
    rep = solve(spec, cap=2)
    sol = rep.solutions[0] if rep.solutions else None
    detail["status"] = rep.status
    grid = _grid(sol, spec) if sol else []

    pet_by_pos = {p + 1: grid[p].get("pet") for p in range(5)} if sol else {}
    expected_known = {1: "cats", 2: "horses", 3: "birds", 5: "dogs"}
    _check(
        checks,
        "B1 grid completes uniquely with typed placeholder",
        rep.status == "solved"
        and rep.unique
        and pet_by_pos.get(4) == "pet:u1"
        and all(pet_by_pos.get(p) == v for p, v in expected_known.items()),
        f"status={rep.status}, pet column={pet_by_pos}",
    )
    gaps = sol.gaps(spec) if sol else ()
    g = gaps[0] if len(gaps) == 1 else None
    statement_ok = (
        g is not None
        and g.dim == "pet"
        and g.placeholder == "pet:u1"
        and g.pos == 4
        and "pet" in g.statement
        and "position 4" in g.statement
        and "I will not invent one" in g.statement
    )
    _check(
        checks,
        "B2 exact gap statement (typed-but-unknown, no guess)",
        len(gaps) == 1 and statement_ok,
        f"gaps={[(x.dim, x.placeholder, x.pos) for x in gaps]}",
    )
    if sol:
        named = _named_values(spec, sol)
        vocab = _visible_vocab(spec)
        _check(
            checks,
            "B3 no hallucination (named terms subset of given vocabulary)",
            named <= vocab,
            f"outside-vocabulary names: {sorted(named - vocab)}",
        )
    else:
        _check(checks, "B3 no hallucination", False, "no solution")
    detail["grid"] = grid
    detail["gap"] = (
        {"dim": g.dim, "placeholder": g.placeholder, "pos": g.pos, "statement": g.statement} if (sol and g) else None
    )
    return checks, {**detail, "sol": sol, "rep": rep, "spec": spec}


def _arm_c() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    detail: dict[str, Any] = {}
    dropped = EINSTEIN.clues[ARM_C_DROPPED_CLUE]
    red = EINSTEIN.with_clues(tuple(c for i, c in enumerate(EINSTEIN.clues) if i != ARM_C_DROPPED_CLUE))
    rep = solve(red, cap=ENUMERATE_CAP)
    sols = rep.solutions
    detail["status"] = rep.status
    detail["n_solutions"] = len(sols)
    detail["capped"] = rep.capped
    detail["dropped_clue"] = f"#{ARM_C_DROPPED_CLUE + 1}: {dropped.text}"

    _check(
        checks,
        "C1 dropping the clue yields EXACTLY two solutions (a minimal counterexample pair)",
        rep.status == "underdetermined" and len(sols) == 2 and not rep.capped,
        f"status={rep.status}, n={len(sols)}, capped={rep.capped}",
    )

    # C2: the reported undetermined facts must equal the countermodel
    # variation computed INDEPENDENTLY by comparing the two grids directly;
    # determined cells must agree across both solutions AND match the arm A
    # ground truth (they are forced even with the clue missing).
    expected: dict[tuple[str, str], tuple[int, ...]] = {}
    for key in red.variable_keys():
        positions = tuple(sorted({s.pos(key[0], key[1]) for s in sols}))
        if len(positions) > 1:
            expected[key] = positions
    reported = {k: v for k, v in undetermined_facts(sols).items() if len(v) > 1}
    det_ok = len(sols) == 2 and all(
        sols[0].pos(k[0], k[1]) == sols[1].pos(k[0], k[1])
        and EINSTEIN_TRUTH[sols[0].pos(k[0], k[1]) - 1][k[0]] == k[1]
        for k in red.variable_keys()
        if k not in expected
    )
    _check(
        checks,
        "C2 reported undetermined facts == EXACT countermodel variation (determined cells match the true solution)",
        len(sols) == 2 and reported == expected and det_ok,
        f"undetermined={ {f'{k[0]}/{k[1]}': list(v) for k, v in reported.items()} }",
    )

    # C3: the named resolving facts must (a) all be canonical At facts over
    # ACTUALLY-undetermined cells, (b) each restore a unique solution when
    # added, and (c) include a fact agreeing with the TRUE solution for the
    # undetermined cells — the original answer remains reachable. Honest
    # scope: the system names the facts, it cannot recover which clue was
    # missing (that would require knowing the clue, not just the grid).
    facts = resolving_facts(red)
    if facts:
        over_undetermined = all(
            isinstance(f, At) and (f.dim, f.term) in expected and f.pos in expected[(f.dim, f.term)]
            for f, _ in facts
        )
        all_unique = all(r.status == "solved" and r.unique for _, r in facts)
        truth_reachable = any(
            EINSTEIN_TRUTH[f.pos - 1][f.dim] == f.term for f, _ in facts
        )
        _check(
            checks,
            "C3 named resolving facts: all canonical At over actually-undetermined cells, each restores uniqueness, and the true answer remains reachable",
            over_undetermined and all_unique and truth_reachable,
            f"{len(facts)} resolving facts: {[f.text for f, _ in facts]}; truth_reachable={truth_reachable}",
        )
        detail["resolving_facts"] = [f.text for f, _ in facts]
        detail["truth_reachable"] = truth_reachable
    else:
        _check(checks, "C3 resolving fact exists", False, "no single At fact restores uniqueness")
        detail["resolving_facts"] = []
        detail["truth_reachable"] = False
    detail["solutions"] = [_grid(s, red) for s in sols]
    return checks, {**detail, "rep": rep, "spec": red}


def _arm_d() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    detail: dict[str, Any] = {}
    spec_d = EINSTEIN.with_clues(EINSTEIN.clues + (EINSTEIN_CONTRADICTION_CLUE,))
    rep = solve(spec_d, cap=1)
    detail["status"] = rep.status
    detail["added_clue"] = f"#{len(spec_d.clues)}: {EINSTEIN_CONTRADICTION_TEXT}"

    cert = minimal_certificate(spec_d, rep.contradiction.clue_ids) if rep.contradiction else []
    detail["certificate"] = [
        {"clue": i + 1, "text": spec_d.clues[i].text} for i in cert
    ]
    _check(
        checks,
        "D1 unsatisfiable, with certificate = exactly the two Norwegian clues",
        rep.status == "no_solution" and rep.contradiction is not None and cert == [8, 15],
        f"status={rep.status}, certificate(0-based)={cert}",
    )
    min_ok = True
    for cid in cert:
        without = spec_d.with_clues(tuple(c for i, c in enumerate(spec_d.clues) if i != cid))
        if solve(without, cap=1).status == "no_solution":
            min_ok = False
    base_ok = solve(EINSTEIN, cap=1).status == "solved"
    reason = rep.contradiction.reason if rep.contradiction else "n/a"
    _check(
        checks,
        "D2 certificate is inclusion-minimal (removing any member is satisfiable) and the base puzzle is solvable",
        min_ok and base_ok and "norwegian" in reason.lower(),
        f"per-member satisfiable={min_ok}, base solved={base_ok}; reason: {reason}",
    )
    return checks, {**detail, "rep": rep, "spec": spec_d}


def _arm_e() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    detail: dict[str, Any] = {}
    rep = solve(TRANSFER_4x4, cap=2)
    sol = rep.solutions[0] if rep.solutions else None
    detail["status"] = rep.status
    detail["n_solutions"] = len(rep.solutions)
    grid = _grid(sol, TRANSFER_4x4) if sol else []
    _check(
        checks,
        "E1 the 4x4 transfer puzzle (new dimension names) is solved uniquely by the same core",
        rep.status == "solved" and rep.unique,
        f"status={rep.status}, n={len(rep.solutions)}",
    )
    if sol:
        ok, why = _replay_proof(TRANSFER_4x4, sol)
    else:
        ok, why = False, "no solution"
    _check(
        checks,
        "E2 transfer grid = ground truth and its proof chains replay",
        grid == list(TRANSFER_TRUTH) and ok,
        f"grid match={grid == list(TRANSFER_TRUTH)}; {why}",
    )
    detail["grid"] = grid
    detail["branches"] = [list(b) for b in sol.branches] if sol else []
    return checks, {**detail, "sol": sol, "rep": rep}


def _arm_f() -> dict[str, Any]:
    """Optional LLM surface arm: a held-out surface sentence -> structured
    clue. SKIP semantics: no backend / not requested => skipped; the
    deterministic core is the verdict (design decision D-m8)."""

    if os.environ.get("KAINOS_E41_LLM") != "1" or not os.environ.get("OLLAMA_ENDPOINT"):
        return {
            "status": "SKIPPED",
            "reason": (
                "optional LLM surface arm not requested (set KAINOS_E41_LLM=1 + OLLAMA_ENDPOINT); "
                "the deterministic core run is the verdict for e4.1"
            ),
        }
    try:
        from kainos.lang.llm import OllamaBackend, _extract_json
    except ImportError as e:
        return {"status": "SKIPPED", "reason": f"LLM module unavailable: {e}"}
    try:
        backend = OllamaBackend()
    except Exception as e:  # noqa: BLE001 — reachability probe: any failure means SKIP
        return {"status": "SKIPPED", "reason": f"Ollama backend unreachable: {type(e).__name__}: {e}"}

    system = (
        "You convert grid-puzzle clue sentences into one structured clue. "
        "Forms: at {dim, term, pos}; pair {dim_a, term_a, dim_b, term_b} (same position); "
        "left {dim_a, term_a, dim_b, term_b} (a immediately left of b); "
        "next {dim_a, term_a, dim_b, term_b} (adjacent). "
        "Dimensions: color (red, green, white, yellow, blue), nationality (brit, swede, dane, norwegian, german), "
        "drink (tea, coffee, milk, beer, water), cigar (pall_mall, dunhill, blends, blue_master, prince), "
        "pet (dogs, birds, cats, horses, fish). Positions are 1-based, left to right. "
        "Reply with exactly one JSON object: {form, ...fields}."
    )
    user = "The Dane lives in the second house."
    expected = {"form": "at", "dim": "nationality", "term": "dane", "pos": 2}
    try:
        raw = backend.complete(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        )
        parsed = _extract_json(raw)
    except Exception as e:  # noqa: BLE001
        return {"status": "FAILED", "reason": f"backend call/parse error: {type(e).__name__}: {e}", "expected": expected}
    ok = all(parsed.get(k) == v for k, v in expected.items())
    return {
        "status": "PASS" if ok else "FAIL",
        "sentence": user,
        "expected": expected,
        "got": parsed,
        "model": getattr(backend, "model", "unknown"),
    }


def run_e4_1(out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = Path(out_dir) if out_dir is not None else default_results_dir()  # results hygiene
    checks: list[bool] = []
    arms: dict[str, Any] = {}
    notes: list[str] = []

    for name, fn in (("A", _arm_a), ("B", _arm_b), ("C", _arm_c), ("D", _arm_d), ("E", _arm_e)):
        arm_checks, detail = fn()
        for c in arm_checks:
            checks.append(c["passed"])
        arms[name] = {"checks": arm_checks, **{k: v for k, v in detail.items() if k not in ("sol", "rep", "spec")}}
        notes.append(f"arm {name}: {sum(c['passed'] for c in arm_checks)}/{len(arm_checks)} checks pass")

    arms["F"] = _arm_f()  # reported, not part of the 14 (D-m8)

    passed = bool(all(checks))
    report = {
        "name": "e4.1",
        "experiment": "constraint-propagation robustness under degradation (Einstein's riddle, n-dim core)",
        "arms": {k: v for k, v in arms.items()},
        "checks": len(checks),
        "checks_passed": sum(checks),
        "notes": notes,
        "passed": passed,
    }
    (out_dir / "phase-4").mkdir(parents=True, exist_ok=True)
    (out_dir / "phase-4" / "e4.1.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


class E4_1Experiment:
    """Phase-4 experiment: does constraint-propagation reasoning stay
    HONEST under degradation? (Q14)

    ``value`` = passed deterministic arm checks / 14 (pre-registered in
    phase-4-robustness/experiments.md)."""

    name = "e4.1"
    hypothesis = (
        "a generic n-dimensional constraint core (forward chaining + deterministic "
        "backtracking + proof chains) solves the given puzzle uniquely and, when "
        "degraded (unknown term / missing clue / contradictory clue), says EXACTLY "
        "what is missing or contradicted — never guessing, never averaging"
    )
    metric = (
        "A: unique solution + ground-truth grid + fish answer + proof replay; "
        "B: typed-unknown term -> unique grid + exact gap statement + no hallucination; "
        "C: one missing clue -> exactly two solutions + exact undetermined facts + a "
        "single canonical At fact restoring the unique true solution; "
        "D: contradictory clue -> no_solution + inclusion-minimal certificate (the two "
        "Norwegian clues) + minimality self-check; "
        "E: a different 4x4 puzzle (new dimension names) solved uniquely by the same "
        "code + proof replay (pattern transfer)"
    )
    threshold = "14/14 deterministic arm checks pass (value >= 1.0); no invented terms, no guessed facts"

    def run(self) -> Any:
        from kainos.harness.runner import Result

        report = run_e4_1()
        value = report["checks_passed"] / report["checks"] if report["checks"] else 0.0
        return Result(
            name=self.name,
            passed=bool(report["passed"]),
            value=value,
            evidence=[Path("results/phase-4/e4.1.json")],
            config={
                "checks_passed": report["checks_passed"],
                "checks": report["checks"],
                "arm_f_status": report["arms"]["F"]["status"],
                "arm_a_status": report["arms"]["A"]["status"],
                "arm_c_solutions": report["arms"]["C"]["n_solutions"],
                "arm_d_certificate": report["arms"]["D"]["certificate"],
                "arm_e_status": report["arms"]["E"]["status"],
            },
        )
