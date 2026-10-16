# Phase 4 — Robustness (E4.1): constraint propagation under degradation

> Ticket: **#149** (owner idea, 2026-08-20; framing frozen as Q14 in
> `plan/90-appendices/research-questions.md`). This document is the
> PRE-REGISTRATION: every choice, ground truth, and threshold below was
> frozen from dev-verified runs BEFORE the official run. Changes after the
> official run are deviations, recorded in `results.md`.

## Hypothesis (Q14)

Does **constraint-propagation reasoning stay honest under degradation**?
Presented with terms it may not fully know, can the system recall and apply
the pattern; when a term is unknown or a clue is missing or contradictory,
can it come back with exactly "I need X" or the contradiction — instead of
guessing? And does the pattern transfer to n-dimensional facts named by the
prompt (new puzzle = new data, same code)?

## The core (`src/kainos/puzzle/core.py`)

A generic n-dimensional logical-grid solver. **No puzzle is hardcoded.**

- **Spec = data:** `PuzzleSpec(houses, dimensions, clues)`; a
  `Dimension(name, terms, hidden)` — `hidden` terms become typed
  placeholders `<name>:u<k>` (the "typed but unknown" representation, arm
  B).
- **Four canonical clue forms:** `At(dim, term, pos)` ·
  `Pair(da,ta,db,tb)` (same position) · `Left(da,ta,db,tb)` (a immediately
  left of b: `pos(a)=pos(b)-1`) · `Next(...)` (adjacent, either order).
  Every dimension is a bijection terms↔positions (stated axiom, never a
  listed clue).
- **Solving:** deterministic forward chaining (clause applications in
  declared order + hidden/naked single all-diff inferences to a fixpoint,
  **every narrowing logged** with its cause) + deterministic backtracking
  (smallest domain, tie-break dimension order then term, values
  ascending, **per-trial domain copies** — see deviation D-e2).
- **Proof chains:** each solution carries the ordered narrowing log of its
  path; replaying it from the initial domains reproduces the assignment
  exactly (verified by check A4/E2 — sufficiency, not mere consistency).
- **Uniqueness:** search continues past the first solution;
  `status=="solved"` ⟺ exactly one (deviation D-e3 fixed a labeling bug
  where >1 solutions under the cap were reported "solved").
- **Contradiction certificate:** on domain wipeout, the fired clue ids are
  inclusion-minimalised by deletion re-testing
  (`minimal_certificate`): unsat as-is, satisfiable with any member out.
- **Degradation machinery:** `Solution.gaps()` (typed-but-unnameable
  cells, exact "I need X" statements) · `undetermined_facts(solutions)`
  (per-variable positions across all solutions) · `resolving_facts(spec)`
  (canonical `At` facts that restore a unique solution).

## Deviation D-e1 — the "on the left of" semantics (frozen 2026-08-21)

The appendix clue 4 says "the green house is **on the left of** the white
house" — English-ambiguous (adjacent or not). **Decision: encode it as
`Left` (immediately left — the stricter reading).** Dev verification
tested both: adjacent reading → the 15 clues have EXACTLY ONE solution
(adopted); dropping clue 4 entirely yields 8 solutions, of which 7 satisfy
the relaxed "strictly left" reading (7 ≠ 1). The stricter reading
uniquely solves the text as given, so it is adopted and this is recorded
as a decision, not an escape hatch. (The core's `Left` docstring carries
the same note.)

## Arms — frozen choices (all dev-verified before freezing)

### A — full puzzle (Einstein's riddle, 5×5)
Clues encoded clue-for-clue, ids = appendix line order (texts verbatim in
`puzzles.py`). **Freeze:** status `solved`, unique; the ground-truth grid
(the scorer's oracle — the solver derives it independently):

| # | color | nationality | drink | cigar | pet |
|---|-------|-------------|-------|-------|-----|
| 1 | yellow | norwegian | water | dunhill | cats |
| 2 | blue | dane | tea | blends | horses |
| 3 | red | brit | milk | pall_mall | birds |
| 4 | green | german | coffee | prince | **fish** |
| 5 | white | swede | beer | blue_master | dogs |

Fish question: **the German, house 4** (matches the classic answer — and
it was NOT used to build anything; the solver derived it).

### B — partial term knowledge
Hide the pet term **`fish`** (the answer's own term — the strongest
honesty case). Freeze: unique grid with `pet:u1` at house 4; exactly ONE
gap, `("pet", "pet:u1", 4)`, with a statement that names the dimension,
the position, and refuses to invent ("I will not invent one"); every named
output value ∈ the given visible vocabulary.

### C — missing clue
Dev table (drop one clue → solution count): #1→6, #2→2, #3→2, #4→8,
#5→4, #6→4, #7→7, #8→4, #9→17, #10→2, #11→2, #12→3, #13→4, #14→12,
**#15→1 (redundant)**. **Freeze: drop clue #11** ("The man who keeps
horses lives next to the man who smokes Dunhill"). Expected: EXACTLY two
solutions (minimal counterexample pair), differing only in the
horse/fish swap {positions 2,4}; the 23 determined cells all agree with
the true solution; `resolving_facts` returns exactly 4 canonical `At`
facts (`fish@2`, `fish@4`, `horses@2`, `horses@4` — dev-verified), all
over actually-undetermined cells, each restoring uniqueness, and the true
answer remains reachable (fish@4 / horses@2 agree with the true grid).
Honest scope, pre-registered: the system NAMES the resolving facts; it
cannot recover WHICH clue was missing (that would require the clue, not
just the grid).

### D — contradictory clue
**Freeze:** append clue #16 "The Norwegian lives in the fifth house"
(`At(nationality, norwegian, 5)`) against clue #9 (first house).
Expected: `no_solution`; certificate = **exactly {#9, #16}** (inclusion
minimal — dev-verified: removing either makes it satisfiable), reason
names the Norwegian wipeout; the base puzzle still solves (the
contradiction is the pair, not the base).

### E — pattern transfer (n-dimension, prompt-named)
A DIFFERENT puzzle, same core, new dimension names (no house/colour):
4 rooms × `wall/person/meal/music`, 9 clues (all four clue forms
represented; clue 9 "Cy's neighbor plays jazz" added in dev to pin
uniqueness). Freeze (`TRANSFER_TRUTH` in `bench.py`):

| # | wall | person | meal | music |
|---|------|--------|------|-------|
| 1 | green | ada | rice | cello |
| 2 | blue | cy | salmon | drums |
| 3 | gold | dee | lamb | jazz |
| 4 | red | ben | tofu | piano |

Expected: `solved`, unique, proof replays. **Zero code changes** — the
spec is data.

### F — LLM surface arm (optional, NOT in the 14)
Held-out surface sentence ("The Dane lives in the second house.") →
structured clue via the owner's optional Ollama backend
(`KAINOS_E41_LLM=1` + `OLLAMA_ENDPOINT`). SKIP semantics (E3.1 pattern):
no backend → reported `SKIPPED`, never a pass/fail. **Design decision
D-m8:** the deterministic core is the e4.1 verdict; the surface arm is
reported addendum (this experiment tests the core's honesty, not the
surface).

## The 14 pre-registered checks (value = passed/14; threshold: 14/14)

| # | check |
|---|-------|
| A1 | full puzzle: `solved` + unique |
| A2 | grid == ground truth |
| A3 | fish answer = German, house 4 |
| A4 | every proof chain replays from initial domains to the assignment |
| B1 | hidden fish: unique grid, placeholder `pet:u1` at 4, known pets at 1,2,3,5 |
| B2 | exactly one gap `("pet","pet:u1",4)`; statement names dim+position+refusal |
| B3 | no hallucination: named values ⊆ visible vocabulary |
| C1 | dropping #11: EXACTLY two solutions, uncapped |
| C2 | reported undetermined facts == exact countermodel variation; determined cells match the true solution |
| C3 | resolving facts: all canonical `At` over actually-undetermined cells; each restores uniqueness; true answer reachable |
| D1 | `no_solution` with certificate == exactly the two Norwegian clues |
| D2 | certificate inclusion-minimal + base puzzle solvable |
| E1 | 4×4 transfer (new dimension names): `solved` + unique, same core |
| E2 | transfer grid == ground truth; proof chains replay |

**Deviations discovered IN dev (before the official run — recorded for
transparency, none affects the frozen choices):**

- **D-e2 (soundness bug, fixed):** the original backtracking restored one
  branch variable on contradiction while `_to_fixpoint` had already
  narrowed many other domains — sibling branches inherited the corruption
  and silently pruned valid solutions (caught by the no-clue-4 sanity
  run: 1 solution with the clue, "0 solutions" without it — impossible
  for a dropped constraint). Fix: per-trial domain copies (frozensets are
  immutable, so a shallow dict copy isolates all propagation). After the
  fix the no-clue-4 run correctly returns 8 solutions.
- **D-e3 (semantics bug, fixed):** `solve()` reported `status="solved"`
  with `unique=False` when the search EXHAUSTED with >1 solutions below
  the cap — "solved" implied a single solution. Fixed the status contract:
  `solved` ⟺ exactly one; `underdetermined` (with a `capped` flag) for
  multi-solution; the arm C checks rely on this.

## Determinism / hermeticity

No RNG in any arm (the hypothesis-based property test lives in tests
only, derandomized). The only env dependence is the optional F arm.
Official run: `KAINOS_GIT_COMMIT` set, `KAINOS_RESULTS_DIR` unset,
Docker, no Ollama env → F recorded SKIPPED, 14/14 expected.
