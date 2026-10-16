# 90 — Open research questions (ordered by leverage)

These are the questions the experiments are *really* probing. Keep this list honest;
update it as phases complete.

1. **Does the explicit IR+CODEX intermediate help compositional generalization**
   (E1.2/E1.5)? — the core bet.
2. **Can persistent knowledge be cleanly separated from neural weights** (E1.3/E2.3)?
   — the "no retraining" claim.
3. **Can the system reliably recognize its own knowledge boundary** (E1.4/A2) and
   escalate correctly (infer/search/retrieve/ask)?
4. **Can contradiction drive ontology expansion** without producing garbage (A5/E3.3)?
5. **Does the same abstract CODEX pattern span modalities** (E3.4)? — the "one
   algebra" prelude.
6. **Does φ/Fibonacci numerics or topology actually win a benchmark** (E3.2/E3.5)?
   — adopt/reject, no faith.
7. **What is the minimal neural component?** If the CODEX carries knowledge, how
   small can the language organ get? (Phase 3 investigation.)
8. **Does "coverage" (verified/encountered) track real competence**, or is it just
   bookkeeping? (A2 longitudinal.)
9. **Does declared-capability planning beat "just answer"?** (X1/E3.6 — does the
   NO VALID PLAN contract measurably reduce capability hallucination vs. an LLM
   answering the same unachievable goals?)
10. **Is semantic temperature a usable creativity dial?** (X2/E3.6 — does temperature
    over constrained traversal produce genuinely varied-yet-valid outputs, and where
    is the quality/validity frontier?)
11. **Does recursive workspace memory beat long-context retrieval** for
    cross-session question answering ("what did we decide?")? (X3/E3.7 — the
    graph-query answer vs. re-reading the conversation.)
12. **Is "eventually/evidence-consistent" federation actually workable** for
   incremental learning? (E3.3.)
13. **The one-line test:** can the system discover an abstraction its designer did
    not put in the ontology? (A5, then a Phase-3 stress test with a genuinely novel
    concept family.)
    **Verdict (final, 2026-08-21, step 20):** YES — at the term/dimension level.
    The seed ontology had no `time`-dimension TERM; the E2.5 contradiction loop
    coined `ctx:time:*` on its own, and E3.3 replicated the discovery: two nodes
    with separate, never-merged ontologies each invented the SAME TERM
    (`ctx:time:polar_bear`), then converged to byte-identical knowledge (P4,
    zero averaging). Honest scope: the designed artifact was the PROCEDURE
    (candidate dimensions + coining rule); the discovery is WHICH dimension
    resolves the contradiction + the concrete term — inside the designed
    space, not specified by any label/prompt. No structurally new RELATION
    TYPE was ever observed (values/contexts yes, new algebra no). Full verdict:
    `plan/30-phases/phase-3-generalization/results.md` → "the one test".
14. **Does constraint-propagation reasoning stay honest under degradation?** (the
    lateral-thinking stress test: Einstein's riddle + degraded variants — partial
    term knowledge, unknown surface terms, missing/contradictory clues → "I need X"
    or a stated contradiction, and n-dimension generalization where the prompt names
    the dimensions. Spec + owner's framing: `lateral-thinking-game.md` in this
    folder; owner idea, 2026-08-20.)
    **Verdict (2026-08-21, #149/e4.1):** YES, at the deterministic core level —
    bounded. `kainos.puzzle` (generic n-dim constraint core with replayable proof
    chains) passed all 14 pre-registered checks (`PASS e4.1: 1.0`): full puzzle
    solved uniquely (fish = the German, house 4); a hidden pet term produced an
    EXACT "I need that name" gap with zero invented terms; a missing clue was
    answered with the exact undetermined cells (exactly 2 solutions) and the exact
    facts that close it; a contradiction produced an inclusion-minimal certificate
    (just the two Norwegian clues); a 4×4 puzzle with new dimension names was
    solved by the same code from data alone. NOT claimed: open-ended
    surface-language robustness (the optional LLM surface arm is SKIPPED-by-design
    in the official run — it measures a different layer) or any claim beyond
    grid-shaped constraints at toy scale. Full verdict + deviations:
    `plan/30-phases/phase-4-robustness/results.md`.

## Keep-out (questions we are deliberately NOT pursuing now)

- Full multi-modal perception (real images/audio) — synthetic ports only until the
  core is proven.
- Hardware/GPU acceleration — until a kernel is proven worth accelerating.
- Scale (millions of terms) — until the single-node loop works.
- "Is this AGI?" — out of scope; the north star is falsifiable and narrow.
