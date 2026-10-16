# Phase 4 — Robustness: results (E4.1)

> Official run **`PASS e4.1: 1.0` — 14/14 pre-registered arm checks**,
> Docker hermetic, commit **d5a06e8**, evidence `results/phase-4/e4.1.json`
> (full report) + `results/e4.1.json` (harness record) +
> `results/phase-4/SUMMARY.md`. Pre-registration: `experiments.md`
> (frozen before this run).

## The verdict in one line

**Constraint propagation stayed honest under every degradation tested:**
unique proof with a correct fish answer on the full puzzle; a typed-but-
unknown term produced an exact "I need that name for the pet at house 4"
statement with **zero invented terms**; one missing clue was answered
with the **exact** undetermined cells and the **exact** facts that would
close it; a contradictory clue produced an **inclusion-minimal
certificate** (just the two Norwegian clues); and a different 4×4 puzzle
with new dimension names was solved uniquely by the **same code, no
changes**.

## Arm evidence (official run)

| Arm | Result | Key evidence |
|-----|--------|--------------|
| A full puzzle | solved, unique | grid = ground truth; **fish = the German, house 4** (green/coffee/Prince cell); proofs replay from initial domains |
| B hidden `fish` term | solved, unique, honest gap | placeholder `pet:u1` at house 4; one gap: *"the pet at position 4 is a member of the pet vocabulary I was not given a term for (1 such term(s) total); providing that name would let me name this cell — I will not invent one"*; named values ⊆ visible vocabulary |
| C missing clue #11 | exactly 2 solutions | undetermined = {horses, fish} over {2,4}; 23 determined cells all agree with the true solution; 4 resolving `At` facts, each restores uniqueness; true answer reachable |
| D Norwegian-in-5 | no_solution + certificate | certificate = **exactly** {#9 "first house", #16 "fifth house"} — inclusion-minimal (removing either is satisfiable); base puzzle still solves |
| E 4×4 transfer | solved, unique, 1 branch | new dimensions (wall/person/meal/music) picked up from spec data; ground truth; proofs replay |
| F LLM surface | SKIPPED | optional arm (D-m8): no Ollama in the official run; deterministic core is the verdict |

All 14 checks: A1–A4, B1–B3, C1–C3, D1–D2, E1–E2 — see `experiments.md`
for the pre-registered definitions; per-check detail in
`results/phase-4/e4.1.json → arms.*.checks`.

## Claims (bounded, per the project convention)

1. **The core is sound and complete at this scale** — verified against an
   independent brute-force enumerator on ~100 small random specs (tests,
   derandomized), and against two full puzzles with hand-verified
   ground truth. "At this scale" = ≤5×5 grids, ≤16 clues.
2. **Honesty under degradation is behavioral, not asserted** — each
   degraded arm's output was checked for *exactness* (exact gap, exact
   undetermined set, exact certificate), not just "some sensible answer".
3. **`Left` = immediately-left is an English-ambiguity decision (D-e1),
   not a finding** — it is what makes the appendix text uniquely
   solvable (verified); the relaxed reading was tested (7 solutions) and
   set aside.
4. **Q14 (owner's framing): YES, at the deterministic core level.** Term
   knowledge can be partial without breaking the pattern (arm B: the
   system *localizes* the fish-keeper even though it cannot name the
   fish); missing information is reported as an exact request; broken
   information is reported as a minimal contradiction; the pattern
   transfers to new dimensions from data alone. What is NOT claimed: open-
   ended surface-language robustness (arm F is the first measurement of
   that layer — SKIPPED here by design), and anything beyond grid-shaped
   constraint problems.
5. **The proof chains are the honest part of the artifact**: every
   assignment carries its causal derivation (clue ids / axiom / branch),
   sufficient by replay — the same "show your work" discipline the
   project applies to its own results.

## Deviations (all recorded in `experiments.md`; none loosened a threshold)

| id | what | impact |
|----|------|--------|
| D-e1 | "on the left of" encoded as `Left` (adjacent); relaxed reading tested & set aside | documented semantics choice; puzzle uniquely solvable under it |
| D-e2 | dev-caught soundness bug: backtracking leaked narrowed domains to sibling branches (dropped-clue sanity run exposed it: 1 sol WITH clue, 0 WITHOUT) | fixed pre-freeze (per-trial domain copies); no effect on frozen choices |
| D-e3 | dev-caught semantics bug: `solve()` labeled >1-solutions-below-cap as "solved" | fixed pre-freeze; status contract now `solved` ⟺ exactly one |
| D-m8 | arm F reported but not in the 14 | design decision: e4.1 verdicts the deterministic core |

## Acceptance checklist

- [x] Gate: **603 passed / 2 skipped**, ruff clean, mypy clean (73 files) — Docker,
      fast-gate env for e3.2/e3.5.
- [x] Official run hermetic+seeded (no RNG in arms), commit injected,
      `PASS e4.1: 1.0`, results + SUMMARY committed together (below).
- [x] Thresholds pre-registered in `experiments.md` BEFORE the official
      run (14/14; exact-set checks, not vibes).
- [x] Solver soundness cross-checked against a brute-force oracle
      (property test, derandomized) + all claimed solutions re-verified
      clue-by-clue.
- [x] Deviations D-e1/D-e2/D-e3/D-m8 recorded with impact.
- [x] Q14 updated with the verdict; roadmap references this phase.

**Next (owner-governed queue):** #149 awaits owner sign-off on these
results (In Review after this commit); then Phase 5 multi-agent games
(#160, linked after #149) and the Interactive Tutor (#150) remain the
two long-term horizons. #135 (Phase-3 milestone) still awaits the
owner's one-word sign-off.
