# 10 — Architecture (system design, layer by layer)

The executable steps for each layer live in `../../action-steps/`; this folder is the
*why* and the shape. Read top to bottom for a full system design.

| Document | What it covers |
|----------|----------------|
| [`system-overview.md`](system-overview.md) | The end-to-end pipeline, layer by layer, and the division of labor. |
| [`codex.md`](codex.md) | The persistent semantic substrate: assertion model, store protocol, invariants. Built by action-steps 02–03. |
| [`semantic-ir.md`](semantic-ir.md) | The intermediate representation every layer speaks: schema, dialects (regex, 20Q), codec rules. Built by 03, 06, 14. |
| [`language-kernel.md`](language-kernel.md) | The text ↔ IR organ: protocol, deterministic kernel, LLM kernel (Phase 3). |
| [`reasoner.md`](reasoner.md) | Search/constraint/verification contract, escalation ladder, output contract. |
| [`exception-system.md`](exception-system.md) | The knowledge boundary: states, cost E, escalation policy, coverage. |
| [`projection.md`](projection.md) | Goal-directed semantic transformation: declared capabilities, plan search as proof, response contracts, structured creativity. Phase 3 (directive 21, gated by ADR-0011). |
| [`workspace-memory.md`](workspace-memory.md) | Recursive WORKSPACE memory: IRs as addressable objects, lifetimes & explicit promotion, source-vs-analysis. Phase 3 (directive 22, ADR-0012). |
| [`execution-fabric.md`](execution-fabric.md) | Heterogeneous execution of compiled IR ops (CPU/GPU/DB); the GPU JIT idea. |
| [`phi-numerics.md`](phi-numerics.md) | φ-exponent numerics + Fibonacci topology: isolated, benchmark-gated strategy seam. Built by 18 (gated). |
| [`distributed-codex.md`](distributed-codex.md) | Multi-node exchange of semantic transactions, conflict-preserving merge, reconciliation. Built by 19. |

## The layer structure (end state)

```
RAW INPUT (text / later: vision, audio, 3D)
        │
        ▼
┌─────────────────────┐
│  LANGUAGE KERNEL     │  neural (LLM) or deterministic — same protocol
└─────────┬───────────┘
          ▼
     SEMANTIC IR       (JSON, versioned schema; dialects per domain)
          │
     ┌────┴──────────────────────┐
     ▼                           ▼
┌───────────┐            ┌─────────────┐
│   CODEX   │            │  REASONER / │  search, constraints, consistency,
│ (persist) │◄──────────►│   SOLVER    │  EXCEPTION escalation
└─────┬─────┘            └─────────────┘
      │
      ▼
  verified / unresolved IR
      │
      ▼
┌─────────────────────┐
│  REALIZER            │  IR → natural language
└─────────────────────┘
```

Module map (target state after all phases):

| Layer | Package(s) |
|-------|------------|
| Substrate | `kainos.codex` (models, stores, explain) |
| IR | `kainos.ir` (models, codec) |
| Language kernel | `kainos.lang` (protocol, deterministic, llm) |
| Domain: regex | `kainos.regex` (dialect, emitter, lexicon, resolver, testgen, judge, pipeline, bench) |
| Domain: 20Q | `kainos.q20` (oracle, seed, hypothesis, selector, game, learn, baselines, dashboard) |
| Experiment harness | `kainos.harness` (runner, report) |
| Phase 3: kernel production | `kainos.lang.llm` (17) |
| Phase 3: numerics | `kainos.numerics` (18, gated) |
| Phase 3: exchange | `kainos.exchange` (19) |
| Phase 3: multimodal | `kainos.multimodal` (20) |

Note: there is deliberately **no `kainos.reasoner` package yet** — resolution lives in
`regex/resolver.py` (08), consolidation in `q20/learn.py` (15), reconciliation in
`exchange/reconciler.py` (19). A shared reasoner seam is created only when a second
genuinely shared need appears (see `../90-appendices/repo-layout.md`).
