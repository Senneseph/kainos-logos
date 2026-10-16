# RESUME PROMPT — B-3 CLOSED (post-compact), day-016 closeout

You are resuming the standing owner-directed work: **attack the Riemann
Hypothesis at its foundations**. One progress report per day. No prize
claim, no `theorem: riemann`, constants computed never recalled, honest
walls always.

## STATE (verified day-016, server clock 2026-09-11)

**B-3 is PROVEN IN LEAN and the whole package is green.** Do not re-derive
the repair; the state is durable in commits and docs:

- `rh-missing-tail` @ `ecfe5ac` (after `d3337c5` = the B-3-green commit):
  `formal/rh-lean/` = **B0, B4, B5, EulerAction, E7a, B3Core, B3Abel,
  B3Sbar, B3 (composition + b3ResidualDecomp + B3Float gate), Main** —
  `lake build` → **exit 0, 17418 jobs**; `RhAttack.lean` imports
  `RhAttack.B3`.
- **Gate** (`lake exe rhattack`): **E7a PASS** (worst |diff|·1e12
  0.019664) + **B-4 PASS 16/16** + **B-5 PASS 12/12** + **B-3
  CROSS-CHECK PASS** (Abel rel-err·1e12 = 0.001125; explicit-bound margin
  = 0.955 > 0; quadrature self-check·1e12 = 0.000167). B3Float.run was
  wired into Main.main on day-016 (it existed but was never called).
- Abstract spec: `plan/40-prize-islands/rh-attack/spec/b3-bridge-abstract.md`
  (T1–T8 + 4.33.1 type ledger + completeness contract) — **satisfied**:
  every Lean statement now matches the spec.
- Outline `RH-PROOF-OUTLINE.md` rows P5/P6/P7 = **proven in Lean**
  (kainos `0435edf`); mirror `rh-missing-tail/docs/RH-PROOF-OUTLINE.md`
  **byte-identical** (`cp` + `cmp` is the resync protocol).
- QUICKREF `references/LEAN4-4331-QUICKREF.md` (kainos, gitignored local):
  §11 = day-014 pins (sub_div corrected to the 3-arg no-proof form),
  §12 = day-016 pins (calc-justification wall, Float-literal default,
  the continuity/aesop wall, the fTp-retargeting architecture, etc.).
  Probes N3–N8 in the public README probe table; all keep compiling.
- Journals: `day-015.md` (monolith 48→30, split, B3Abel green — backfilled
  from commits), `day-016.md` (this closeout).

## THE RE-RUN RECIPE (verify before claiming anything)

```sh
cd /home/jsmille/Projects/rh-missing-tail/formal/rh-lean
export PATH="$HOME/.elan/bin:$PATH"
lake build            # expected: Build completed successfully (… jobs), exit 0
lake exe rhattack     # expected: 4 PASS lines (E7a / B-4 / B-5 / B-3)
```

The Lean files LIVE in `rh-missing-tail/formal/rh-lean`;
`kainos-logos/scripts/rh-lean` is a symlink into them. Commit only the
rh-attack paths. Reference material lives ONLY in
`kainos-logos/references/` (gitignored local; never commit it; the public
repo carries proof content only).

## THE FRONTIER (what the attack needs next)

The B-3 bridge is OFF the critical path. The open pieces:
- **P4** — the rigorous lift of the measured missing-tail law
  (explicit Φ_n + explicit Euler–Maclaurin remainder for W_n; measured to
  4 digits, onset fingerprint at G = 6×10⁶ reproduced ≤ 6%; the rigorous
  version is open).
- **P8** — **the residual floor, ∀ t — §10, OPEN, the wall.** Two routes
  are written in the outline; nothing is claimed.
- P2/P3/P5/P6/P7 are proven or proven-in-Lean (see outline §9).

Owner-protocol reminders that still bind: ONE THING AT A TIME (1 fix →
re-run → observe → next; no batched fixes, no ahead-of-time
investigation); DOCS FIRST (the pinned quickref + the archived official
docs + the pinned mathlib source under `.lake/packages/mathlib`), THEN
online search, THEN ask the owner — DO NOT GUESS ABOUT HOW LEAN WORKS;
stable toolchains only (`leanprover/lean4:v4.33.1`); probes compile and
record failures in comments; every public doc is honest and
alien-readable (no internal codes, no changelogs, no prize claim).

## PARKED OWNER-CALL ITEMS (unchanged; do not act without instruction)

1. The middle-window (1.4×10⁶, 9.9×10⁶) re-walk — re-walk or accept the
   two-engine confirmation at the window edges.
2. `A_SPECTRAL_SOLUTION.md` — keep or move.
3. The DEFECTIVE early-rewalk file — rename policy.
4. Canonical project date — server clock 2026-09-11 vs session headers
   2026-09-13.
