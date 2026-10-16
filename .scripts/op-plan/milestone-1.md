**Signed by:** step 12 / action P1.16 — fills `plan/30-phases/phase-1-regex/results.md`.

Phase 1 is signed off when **all five** exit criteria are met:

1. **E1.1 parity == 1.0** on the seed corpus (every operator). *(09)*
2. **E1.2** — pipeline beats the no-CODEX baseline on novel combinations by ≥0.1
   absolute, pipeline ≥ 0.8. *(10)*
3. **E1.3** — teach → restart → reuse with frozen kernel (**C2**) + **E1.4** vague
   set never emits an unjustified regex (**C3**). *(11)*
4. **E1.5** — Model B > Model A on held-out combinations; B abstains correctly on
   the vague set where A cannot. *(12)*
5. `results.md` **signed off with reuse stats** (compounding contract — P0
   artifacts consumed). *(12)*

**Kill criteria to check at sign-off** (`plan/04-reality-check.md` §4 — null
hypotheses committed before building):

- **K1:** If the teach→restart→reuse loop (C2) does not survive a restart with a
  frozen kernel, the "knowledge separated from weights" claim is dead.
  **Stop or redesign.**
- **K2:** If, on the *novel* claims (C2/C3/A5), the CODEX adds no measurable
  benefit over a plain `dict` + compiler of equivalent complexity, the
  architecture is overhead. **Stop.**

After sign-off: mark steps 06–12 ✅ in `action-steps/README.md`; proceed to
`action-steps/13-q20-corpus-oracle.md`.
