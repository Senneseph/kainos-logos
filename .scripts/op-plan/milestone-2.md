**Signed by:** step 16 / action P2.15 — fills `plan/30-phases/phase-2-20questions/results.md`.

Phase 2 is signed off when **all four** exit criteria are met:

1. **E2.1–E2.5 run green and are reported.**
2. The **growth dashboard** shows exception space shrinking across ≥N games.
3. A **restart demo**: train on game set 1 → restart → play game set 2, showing
   retention + improvement with frozen kernel.
4. `plan/30-phases/phase-2-20questions/results.md` has **metric tables + the
   growth curve** (plus `results/phase-2/SUMMARY.md` rendered by the harness
   `report` command).

**Kill criterion to check at sign-off** (`plan/04-reality-check.md` §4):

- **K3:** If contradiction→dimension (A5) produces garbage terms that a human
  can't sign off on after one canonical conflict, the "self-expanding ontology"
  claim is unfalsifiable. **Constrain it or drop it.**

After sign-off: mark steps 13–16 ✅ in `action-steps/README.md`; proceed to
`action-steps/17-llm-kernel.md`.
