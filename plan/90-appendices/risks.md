# 90 — Risks & mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | The deterministic kernel can't scale beyond the seed grammar (brittleness). | High | Medium | LLM kernel (ADR-0004) is the escape hatch; interface is fixed so swapping is free. |
| R2 | CODEX doesn't actually help — baseline parity (E1.2/E1.5 fail). | Medium | High | The A/B is designed to *falsify* cheaply; a fail is a valid, publishable negative result. |
| R3 | Abstraction discovery (contradiction→dimension) is too hard / produces garbage terms. | Medium | High | Gate it narrowly (A5/E3.3) on one canonical conflict first; require human-sign-off on new TERMs initially. |
| R4 | The graph DB becomes a garbage dump (unbounded EXCEPTION). | Medium | Medium | Epistemic states + provenance mandatory from day one (ADR-0008); consolidation requires verification. |
| R5 | φ/Fibonacci is numerology; wasted effort. | High | Low | Strictly gated (ADR-0006), isolated, adopt/reject; can't block core. |
| R6 | Scope creep → never finish Phase 1. | Medium | High | Exit criteria + experiment gates; "start embarrassingly small" (P10). |
| R7 | LLM backend unavailable/costly for E1.5. | Medium | Low | A/B still runnable with a tiny local model; deterministic kernel keeps the pipeline CI-green regardless. |
| R8 | Benchmarks leak (compositional set accidentally overlaps seed). | Low | High | Seeded generator + explicit "no duplicate of seed" assert (P1.10). |
| R9 | "Higher-order representation" is unfalsifiable mush. | Medium | Medium | Every such claim must name the new TERM and show both assertions retained as `established` (E2.5/E3.3). |
| R10 | Distribution/GPU work distracts before single-node proof. | Medium | High | Phase 3 strictly after Phases 0–2; execution fabric seam exists but GPU/φ backends deferred. |
| R11 | Projection drifts into agent scope creep (real side effects, open-ended planning, goal drift). | Medium | High | ADR-0011 caps it: Phase 3 only, **simulated** capabilities in E3.6 (no real actions), bounded search depth/cost, plans validated against declared capabilities (P11). The claim tested is planning faithfulness, not tool use. |
| R12 | Workspace memory becomes a second, corruptible memory store (dual bookkeeping vs. CODEX). | Medium | Medium | ADR-0012 discipline: explicit promote() only (P12), promotion always lands as *candidate* assertions on the ordinary verification path, negative control in E3.7 asserts un-promoted content is invisible to the CODEX. |

## The one risk that matters most

**R2** — if the CODEX doesn't demonstrably help, the whole thesis is in question.
That is exactly why Phase 1 is built to answer it first, cheaply, with an objective
judge (the regex executor) and a clean A/B. If it fails there, better to know in
week 2 than year 2.
