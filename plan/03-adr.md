# 03 — Architecture Decision Records (ADR)

Living log. Each entry: status, decision, rationale, consequences, supersedes.
A decision here is binding until a later ADR overturns it.

## ADR-0001 — Languages: Python (in Docker) for prototypes, Perl for regex glue, Rust long-term

- **Status:** Accepted — supersedes the earlier "Python only" decision.
- **Decision:**
  - **Prototype Phases 0–2 in Python ≥3.11**, running inside a pinned Docker image
    (ADR-0010) so the host stays clean.
  - **Perl** for regex-specific scripting and — especially — the **regex judge**
    (compile + full-match verdicts). Perl is the canonical home of regex and is
    more ubiquitous than Python for it.
  - **Rust** as the long-term implementation language for the final architecture:
    port the proven core and copy-in/translate any crates the ecosystem lacks.
- **Rationale:** Python is fastest to *falsify* the claims, but its venv is fragile —
  Docker makes the toolchain reproducible data instead. Perl gives a real regex
  engine for the judge at zero new deps. Rust fits the end-state (persistent graph
  store, constraint solving, bit-level φ ops) and honors ADR-0006's "rewrite only
  what's proven."
- **Consequences:** The regex judge lives in Perl. The core (CODEX/IR/reasoner) stays
  language-agnostic at the IR boundary (ADR-0003), so a Rust port is a drop-in
  replacement behind the same interfaces. No premature Rust.

## ADR-0002 — CODEX storage: abstraction over SQLite first, graph DB later

- **Status:** Accepted
- **Decision:** Define a `CodexStore` interface (add/remove/query assertions). Ship a
  SQLite-backed implementation (quad table + indices) for Phases 0–1. Optionally add
  a `networkx` in-memory implementation for fast experiments.
- **Rationale:** The document notes a graph DB is a fine *storage engine* but the
  *model* is "assertions, not facts". SQLite is zero-ops, inspectable, portable, and
  keeps us from over-investing in a graph engine before the semantics are stable.
- **Consequences:** A `CodexStore` port (Neo4j/JanusGraph/…) is a Phase 3 concern.
  Inspectability (P9) is served by a `sqlite3` CLI + dump tool.

## ADR-0003 — Semantic IR serialization: JSON

- **Status:** Accepted
- **Decision:** Semantic IR is a JSON-serializable structure with a versioned schema
  (`ir.schema.json`), not a Python object graph on the wire.
- **Rationale:** Language/modality agnostic (P7), trivially inspectable (P9),
  diffable for provenance/debugging, and testable with golden files.
- **Consequences:** A `Codec` validates IR against the schema at every boundary.

## ADR-0004 — Language Kernel: deterministic grammar first, LLM second

- **Status:** Accepted
- **Decision:** Phase 1's language kernel is a **deterministic, hand-written parser
  over a restricted English grammar** (regex-description subset). The LLM path is a
  drop-in `LanguageKernel` implementation added later, so the A/B experiment
  (conventional vs. CODEX) is clean.
- **Rationale:** The core claim (P2) is about *separating knowledge from language*,
  not about parsing skill. A deterministic parser removes a confound, is free, and
  can be run in CI. The LLM becomes a second implementation of the same interface.
- **Consequences:** The `LanguageKernel` interface is the contract; the grammar
  subset is defined in `30-phases/phase-1-regex/spec.md`.

## ADR-0005 — Every phase ships a falsifiable experiment

- **Status:** Accepted
- **Decision:** No phase is "done" until its named experiment runs green in CI and
  its metric is reported. "Building" is not a deliverable; "demonstrating a claim"
  is.
- **Rationale:** P8 (measure, don't argue) and the north-star success criteria.
- **Consequences:** `40-testing/harness.md` defines the experiment runner contract.

## ADR-0006 — φ/Fibonacci numerics are isolated and optional

- **Status:** Accepted
- **Decision:** The φ-positional number system ("power stepping") is a Phase 3,
  standalone, benchmark-gated experiment. It is **never** a dependency of the CODEX
  schema or the Phase 0–2 pipeline.
- **Rationale:** The document itself rates it ★★★★★ but explicitly warns against
  assuming superiority. It must be tested on its own metric
  ("useful neural computation per bit-op") without entangling core semantics.
- **Consequences:** Core CODEX stores strengths as ordinary numbers (or compact
  ints) with a `Numerics` strategy seam reserved for Phase 3.

## ADR-0007 — Repo layout: `src/kainos` package + `tests/` mirror

- **Status:** Accepted
- **Decision:** Monorepo, single package `kainos`, mirroring `tests/`. Plan lives in
  `plan/`, specs in `specs/`, data in `data/`. See `90-appendices/repo-layout.md`.
- **Rationale:** One package keeps the compounding import graph simple and lets the
  CODEX core be reused by regex, 20Q, and generalization phases.
- **Consequences:** Public package name `kainos` is reserved; phases add submodules,
  never sibling packages.

## ADR-0008 — Provenance and epistemic state are mandatory, not optional

- **Status:** Accepted
- **Decision:** Every assertion in the CODEX carries `source`, `context`, `validity
  interval`, `confidence`, and `status` from the very first line of Phase 0. There
  is no "bare edge" escape hatch.
- **Rationale:** P1/P6 and the document's repeated warning that these aren't
  secondary features but "part of the learning architecture itself".
- **Consequences:** The CODEX schema in `10-architecture/codex.md` has these fields
  non-nullable; tests assert their presence.

## ADR-0009 — Regex judge runs under Perl's regex engine

- **Status:** Accepted — supersedes the earlier "Python `re`" decision.
- **Decision:** The regex **judge** (compile + full-match verdicts on generated
  examples) runs under **Perl's regex engine**, not Python's `re`. The emitter
  targets the Perl/PCRE-compatible construct set we emit (no backrefs/recursion
  initially).
- **Rationale:** Perl is the canonical, ubiquitous regex host; its engine is a
  superset of PCRE. Python's `re` is not PCRE and has Unicode-aware shorthand
  divergence. User direction: "PCRE is Perl, we have Perl."
- **Consequences:** The judge is a small Perl script invoked by the harness; the
  emitted subset is validated against it. The core (CODEX/IR/reasoner) stays Python
  (in Docker). If an in-process judge is ever needed, the Python `regex` module is a
  fallback, but Perl is canonical.

## ADR-0010 — Idempotent Docker build; every dependency is pinned data

- **Status:** Accepted
- **Decision:** All build/run tooling (Python, Perl, llama.cpp, libraries) is declared
  in an in-repo `Dockerfile` + pinned lockfile. Development and tests run **inside**
  the container; the host is never modified. Pin every version: base image digest,
  Python, pip hashes, llama.cpp commit.
- **Rationale:** "Every system dependency is now data" — reproducibility and a clean
  host, avoiding the venv horror. Matches the compounding/reproducibility goals
  (seeded, hash-pinned results).
- **Consequences:** `Dockerfile`, `.dockerignore`, and a lockfile become part of the
  repo. CI builds the image and runs the suite inside it. Phases 0–2 are CPU-only in
  the container; GPU (Vulkan) pass-through is a Phase-3 concern.

## ADR-0011 — Projection: capabilities are first-class TERMS; planning runs over the CODEX

- **Status:** Accepted
- **Decision:** Add a projection layer (Phase 3, directive 21): capabilities are
  explicit TERMS with `PRECONDITION`/`INPUT`/`EFFECT`/`COST` assertions in the
  CODEX; the reasoner gains a bounded plan search (precondition-checked effect
  application until a terminal state satisfies the goal). A goal with no valid plan
  is a first-class **NO VALID PLAN** result (named capability gap + nearest viable
  plan + search trace). Traversal may be stochastic under a **semantic temperature**
  parameter, but novelty may never violate established facts or hard constraints.
- **Rationale:** Principle P11 and the supplementary design ("goal-directed
  semantic transformation"): the hard problem is not parsing or language generation
  — it is deciding, from a structured goal, which declared transformations satisfy
  it. LLMs "just answer" and fabricate capabilities; a declared-capability planner
  turns "I can't, but here's the nearest viable plan" into a *verifiable* output.
  It reuses the machinery already built: information-gain question selection (A1)
  picks clarification questions over *plan branches*; EXCEPTION states cover the
  failure taxonomies.
- **Consequences:** `src/kainos/projection/` is Phase 3 only and must not alter
  Phase 0–2 pipelines. E3.6 (X1/X2) is benchmark-gated with **simulated**
  capabilities — no real side effects. Response contracts are data (per interaction
  type), extendable without new code paths.

## ADR-0012 — WORKSPACE memory: recursive IR containers with explicit promotion

- **Status:** Accepted
- **Decision:** Add a `kainos.workspace` module (Phase 3, directive 22): a WORKSPACE
  is a bounded, named, lifetime-scoped (`EPHEMERAL|SESSION|PROJECT|LONG_TERM`),
  recursively nestable container of Semantic IRs + hypotheses + constraints + plans
  + exceptions + references. Long-term content enters the CODEX **only** via an
  explicit `promote()` that writes candidate assertions with
  `provenance.source = workspace_<id>`, which then pass ordinary verification.
  Sources (documents) are held as SOURCE objects with **versioned analysis IRs** —
  the document never becomes the knowledge.
- **Rationale:** Principle P12 and the supplementary design: persistent-memory
  problems and unbounded-context bloat are solved by making memory a recursively
  addressable space of structured thought. Implicit promotion is the corruption
  path ("penguins can fly" from one joking session); explicit, provenance-carrying
  promotion keeps the CODEX's epistemic discipline (P1, ADR-0008) intact. Phases
  1–2 already use de-facto workspaces (20Q game state, pipeline results) — this
  generalizes them without changing the proven pipeline.
- **Consequences:** `src/kainos/workspace/` is Phase 3 only; E3.7 (X3) verifies
  queryability, recursion, and promotion discipline. Distributed nodes (step 19)
  may exchange workspace IRs as future deltas, but the Phase 3 protocol stays
  assertion-delta-only unless E3.7 shows a need.

## ADR-0013 — Morpho-scavenged mechanisms are pattern transfers, benchmark-gated, and never a dependency

- **Status:** Accepted (2026-08-20; proposal recorded in SCAVENGE_MORPHO.md §4)
- **Decision:** The MorphoHDL runtime mechanisms (M1–M7: materialization
  registry, interleaved pruning, fanout-bounded materialization, fallback
  unwinding, space–time duality, largest-first ordering, flat binding-point
  genome) may be brought into Kainos-Logos **only as patterns re-implemented in
  our own semantics**, each behind a seam, each **benchmark-gated adopt/reject
  with a written margin**. No MorphoHDL code, data, or dependency is committed;
  the source stays a local, git-ignored checkout (`references/morpho`,
  Apache-2.0) used for verification only.
- **Rationale:** MorphoHDL demonstrates that a tiny rewrite kernel + a fallback
  mechanism + aggressive interleaved pruning generates unbounded, verified
  structure from compact definitions — operationally the same shape as our C1
  (compositional generalization) and A5 (contradiction → dimension) claims.
  Its substrate (bit buses, LUTs) is semantically incompatible with our
  provenance-carrying assertion graph (P1, ADR-0008), so we take the
  mechanisms and leave the semantics. The benchmark gates exist to defeat the
  plan's top-scoped risk — *metaphor overfit*: every borrow must demonstrate a
  concrete win in our domain (speedup, smaller frontier, cleaner NO VALID PLAN)
  or be rejected. Mirrors ADR-0006's isolation discipline for φ numerics.
- **Consequences:** (1) `SCAVENGE_MORPHO.md` is the canonical transfer record;
  M-IDs are stable and never renumbered. (2) Each borrow ships with a
  seam-neutrality regression (mechanism OFF ⇒ byte-identical pipeline),
  Morpho-style counters in the experiment JSON for inspectability (P9), and
  results under `results/scavenge/` (LAYOUT G9). (3) Section 4 verdicts — one
  adopt/reject line per M1–M7 with the margin — are appended to this ADR by
  Scavenge Step I before Phase 3 sign-off. (4) OpenProject epic for the
  scavenge: ticket #139 (steps A–I: #140–#148), wires: A→B→#119, #124→C→#125,
  #123→G→#125, #120→D, #130→E/H, #131→F/I.

## ADR-0013 §4 — Scavenge verdicts (one line per M, with the written margin)

- **M1 (materialization registry / specialization cache): ADOPTED (2026-08-21).**
  Gate met on the E1.2 compositional set itself (`data/regex/compositional_set.jsonl`,
  40 records, one shared seeded CODEX — the E1.2 shape): cached vs. uncached
  resolution **byte-identical** (`identical: true`) at a measured **1.60x**
  wall-time margin (916µs → 574µs parse+resolve+emit; 51 cache hits / 5 misses
  over 5 distinct terms). The margin is modest because the seeded CODEX is
  small — the cache's value scales with repetition of (abstraction,
  context-signature) pairs, which is exactly the workload E1.2-style runs
  create. Interim seed-corpus run (1.73x, 55 records) preserved at
  `results/scavenge/m1-seed-corpus.json`; final verdict artifact
  `results/scavenge/m1.json`. Seam-neutrality regression:
  `tests/regex/test_m1_cache.py` (mechanism OFF ⇒ identical pipeline). This
  verdict closes the re-run note in #141's interim artifact (board audit
  2026-08-21, owner-directed).
- **M2 (interleaved dead-branch pruning in the q20 learning loop):
  REJECT (pattern mismatch; no measurable delta).** `q20/learn.py` is a
  sequential consolidation pass (per trace row: write candidate → verify
  siblings → promote / dispute / keep; conflicts are re-expressed by
  `detect_dimension` under distinct contexts) — there is no growth frontier,
  no search state, no dead branch to prune into, and the official artifact
  carries no frontier/expansion statistic at all (`e2.2.json` claims are
  dimension growth, `dimensions_grown: 6`). Pruning the one thing the loop
  can call "dead" (conflicting evidence) would violate the keep-
  contradictions invariant (A5/ADR-0008) — dimension re-expression already
  IS the post-hoc cleanup. Gate ("fewer expansions; reject if the post-hoc
  cleanup was already optimal — no delta"): expansions are 0 → 0; margin =
  the E2.2 official PASS of the existing cleanup path.
- **M3 (fanout-bounded reference materialization in the codex store):
  REJECT (no gate workload; measured knee recorded).** The Step D gate
  demands a materialization latency win at fanout 2–256 on a REAL workload.
  Measured (Docker probe, `results/scavenge/m3-m6-probe.json`, 2026-08-22):
  full-scan `query()` median **5.4µs** / p95 11.8µs on the project's largest
  official store (245 assertions, e6.4 final); **138µs** / p95 162µs on a
  synthetic 5000-assertion store for which no project workload exists.
  Revisit knee (recorded, not a threshold change): ~10⁴–10⁵ assertions,
  where scans enter the millisecond regime and start competing with
  pipeline costs. No cache/invalidation surface introduced (P1/P9 untouched).
- **M4 (EXCEPTION as unwinding control flow; `NoValidPlan` with the longest
  valid prefix): ADOPTED-AS-NATIVE (no transfer).** The pattern is fully
  present in the mature design and its Step-E gate is itself an official
  claim: `projection/planner.py` returns first-class `NoValidPlan` (named
  unmeetable gap + `nearest_prefix` = longest no-repetition progress prefix +
  the full failed-attempt trace), the DFS unwinds on precondition / budget /
  no-new-fact stops and records each — the "impossible" contract is X1 under
  P11 (declared, not implied). Margin: the E3.6 official PASS includes the X1
  thresholds (named gap + nearest viable plan, no fabricated action). The A.2
  cross-link (escalation-record shape → NoValidPlan) is confirmed.
- **M5 (space–time duality in workspace promotion; re-derivation cost as a
  measured input): REJECT (unfalsifiable — no reuse metrics exist).** The
  Step F gate: "reuse stats show promotion follows the policy (else the
  policy is unfalsifiable — reject)"; the doc's own risk section: "M5 needs
  reuse metrics first." Verified across the mature tree (q20, projection,
  workspace, codex, exchange): zero reuse / re-derivation / compounding
  counters anywhere; `e3.7.json` carries no reuse statistic (its claims are
  fork isolation, promotion integrity, query accuracy, recursion depth,
  source versioning). Promotion remains the explicit, role-scoped
  `promote()` (ADR-0012: workspace never writes truth; candidates through the
  verification path; idempotent; lapse → results). Borrowing the cost-based
  materialization decision without a cost model would add an unfalsifiable
  policy — the exact metaphor-overfit risk ADR-0013 exists to defeat.
- **M6 (largest-first / upper-bound ordering in the q20 selector + planner):
  REJECT (no delta).** Measured on the real E2 corpus (Docker probe,
  `m3-m6-probe.json`): 17 questions × 149 concepts; one selection step (the
  full candidate scan, 22.25 oracle splits) = median **2.68ms**. The only way
  an upper-bound ordering beats that is early termination of the 17-candidate
  scan — which requires a cheap tight IG bound. But a tight bound requires
  exactly the oracle-split evaluations it would save (the `H(H_a)` terms of
  `IG(q) = H(H) − Σ P(a)·H(H_a)` are unknown without the split); the only
  a-priori bound is the trivial H(H), which every candidate ties — zero
  pruning power. Gate ("identical answers at equal-or-lower expansions"): the
  variant achieves equal (0 of 17 pruned), never lower. No delta → reject.
- **M7 (flat binding points; leaf substitution in capabilities + reconciler):
  ADOPTED-AS-NATIVE (no transfer).** `projection/capabilities.py`:
  capabilities are flat store rows (subject + preconditions/effect/cost
  properties, established); `load_capabilities` reads the planner's entire
  move set from store rows; "calling seed_capabilities with a new name is
  itself the store-operation way to grant a capability — no code change
  (P11)" — flat binding-point encoding as the architecture itself. Leaf
  substitution is already the first-class store op: `obsoletize_capability`
  (retire the rows) + `seed_capabilities` (re-declare), composition
  untouched. `exchange/reconciler.py`'s role is cross-node merge /
  reconciliation (ADR-0016), not leaf swapping — no op missing there.
  Margin: the E3.3 and E3.6 official PASS runs (exchange semantics; planner
  move-set claims) are the verifying evidence; A.2's "confirmed, no change"
  stands.

**Sweep verdict summary (2026-08-22, owner-directed revisit):** 1 adopted
borrow (M1, measured 1.60x), 2 patterns already native (M4, M7 — no transfer
needed; their gates are official claims), 3 rejections with written margins
(M2 pattern mismatch, M3 no gate workload, M6 no delta), 1 rejection as
unfalsifiable (M5, no reuse metrics). No MorphoHDL code, data, or
dependency was committed (ADR-0013 decision, verified: `references/morpho`
remains local + gitignored).

## ADR-0014 — φ numerics (E3.5): precision winner, ops loser — REJECTED at 8 bits, stays isolated

- **Status:** Accepted (2026-08-20; E3.5 official run `results/phase-3/e3.5.json`, commit 06d2b56)
- **Decision:** The φ-positional system (s·φ^n, exponent-add multiply,
  Fibonacci-carry normalization) is **rejected** as a numeric substrate at the
  8-bit budget: it wins the pre-registered error-per-op axis (4.50e-6 vs best
  baseline 7.60e-6, −41%; MAC rms rel err 0.00186 vs 0.00247/0.0707 for
  FP8/INT8) and the power-histogram axis (L1 0.0 vs 0.070/0.540), but loses the
  ops axis (334.7 ops/result vs best baseline 161.5, 2.07×). Per the
  pre-registered verdict rule all three axes must hold to adopt. It remains an
  isolated experiment behind the `kainos.numerics` seam (ADR-0006), never a
  dependency of the CODEX or any Phase 0–3 pipeline; `FloatNumerics` stays the
  default and the seam-neutrality regression (E1.1 unchanged) stays green.
- **Rationale:** The mechanism is real and measurable — φ's midpoint mantissa
  over [1,φ) gives finer relative resolution than E4M3 at 3 mantissa quanta
  bits, and its exponent field IS a power bin (the histogram axis is exact by
  construction). But the MAC's local-rewrite overhead is structural: 3 ops per
  pair (sign xor + exponent add + mass add) vs 2 for baseline mul+add, plus
  Fibonacci carries (each a counted divide) and a spread digit-string fold that
  baselines read out with one dequant scale. At 8 bits that overhead swamps the
  precision edge. This is the honest negative the plan (P8) demanded — recorded,
  not redefined: no threshold or op model was moved to make it pass.
- **Consequences:** (1) The seam survives: `Numerics` protocol + inert
  `FloatNumerics` default are now core infrastructure — any future numeric
  strategy (broader φ bit budgets, carry-hardware op models, block-φ schemes)
  enters behind the same protocol and re-runs E3.5's A/B. (2) `PhiNumerics` +
  `fib_normalize` stay in `src/kainos/numerics/phi.py` as the experimental
  implementation (library tests pin its mathematics: round-trip bound, the
  Fibonacci identity φ^(k+2)=φ^(k+1)+φ^k, mass preservation, reserved zero
  code). (3) Re-adoption requires a new pre-registered A/B at a different bit
  budget or op model, never a reinterpretation of this one.

## ADR-0015 — Fibonacci residual recurrence (E3.2): ADOPTED as an architecture option at equal parameter budget

- **Status:** Accepted (2026-08-20; E3.2 official run `results/phase-3/e3.2.json`, commit 06d2b56)
- **Decision:** The topological claim **survives at toy scale**: a recurrence
  X_{k+2} = tanh(f(X_{k+1}) + X_k) with ONE shared map f, readout at X3,
  beats a same-budget (115-param) 10→6→6→1 MLP on test RMSE for **all 3 seeds**
  (0.6396 vs 0.7115, 0.5075 vs 0.5343, 0.3507 vs 0.3625; mean relative
  improvement +6.87%) on a linear + cyclic-pair-interaction task. Adopted as an
  **architecture option** for the reasoner's numeric core, not as a forced
  replacement: the recurrence is available wherever a fixed-width numeric
  sub-computation is needed, behind the same benchmark record; the default
  path remains the simpler MLP-shaped computation until a production task
  shows the margin at stake.
- **Rationale:** The finding CONTRADICTS the plan's honest expectation ("null
  or negative"), which is exactly why the pre-registered all-3-seeds rule
  exists: the win is consistent (3/3 seeds, +3.3% to +10.1%), both arms far
  beat the no-learning baseline (so the delta is a real equal-budget effect,
  not a training accident), and both arms' gradients are finite-difference
  verified in the suite (max rel err < 1e-6) — the optimizer cannot be the
  confound. The plausible mechanism is the residual (linear-shortcut) topology
  plus weight sharing: fewer independent parameters to overfit, smoother
  optimization landscape — an OPTIMIZATION edge at equal capacity, i.e. the
  "recurrence across topology" the plan hypothesized. The width-schedule
  variant (1,1,2,3,5,8) was not run separately (deviation D6): the recurrence
  arm is the stronger claim and the schedule its natural extension.
- **Consequences:** (1) `benchmarks/topology/` is the canonical record;
  re-running is hermetic and deterministic (3 seeds, pure Python, no
  dependencies). (2) When the reasoner (or later sub-projects) needs a
  fixed-width numeric path, the recurrence is the documented candidate with
  this margin — adoption in a production pipeline requires the same A/B at the
  real task scale. (3) The "one recurrence" thesis (results.md) now has one
  positive (topology) and one negative (numerics) datapoint — the thesis is
  neither proven nor killed; steps 19–22 add the remaining rows.

## ADR-0016 — Distributed-CODEX exchange semantics (E3.3): idempotent, conflict-preserving merge; receiver-state-derived reconciliation; contract coupling to `kainos/codex/1`

- **Status:** Accepted (2026-08-21; E3.3 official run `results/phase-3/e3.3.json`, commit for step 19)
- **Decision:** The distributed-CODEX exchange takes these OPERATIONAL
  semantics (the design doc's principles, made testable):
  1. **Merge is idempotent:** a delta whose assertion id the target already
     holds is a no-op (`duplicate` in the report). Idempotency must hold on
     real traffic, not just unit tests — in a two-direction exchange each
     node re-receives its own facts via the other; E3.3's merge reports list
     those round-trip ids under `duplicates`.
  2. **Merge preserves conflict:** same subject + relation + aspect with a
     different value ⇒ both sides become `disputed` with cross-linked
     evidence **in both directions**; the sender's status never overrides the
     receiver's store (each node derives epistemic state from identical
     evidence — Principle 4, convergence not consensus). Merge touches only
     `status`/`evidence`/`exception` — objects and polarities are
     byte-preserved (no averaging, invariant #6).
  3. **Reconciliation is the single-node mechanism, distributed:** the
     plan's candidate list (`time, location, role, modality, context`, in
     order) under the operational test — a specific dimension D explains a
     conflicting group iff every pair of sides with different values carries
     *different* D values in their context data (absent key ≠ value); the
     catch-all `context` explains iff the sides' context data differ in any
     key. Explained ⇒ new context TERM `ctx:<D>:<subject>` (kind `context`)
     declared as knowledge + every side re-expressed under its context and
     re-established. Unexplained ⇒ left `disputed`, nothing invented (the
     honest negative is a first-class outcome, P8).
  4. **Contract coupling:** `assertion_delta.schema.json` is a SELF-CONTAINED
     MIRROR of the `kainos/codex/1` assertion shape (house style: internal
     `$refs` only; RFC 3986 relative-URI resolution also makes a cross-file
     `$ref` from the delta's own `$id` base unresolvable). A codex contract
     bump to v2 MUST ship `kainos/exchange/assertion-delta/2` in the same
     change.
- **Rationale:** E3.3 met all six pre-registered checks on both nodes (new
  TERM, both values established, distinct contexts, disputed 4→0, no
  averaging, converged identical knowledge) with the exact single-node E2.5
  mechanism reused — the recurrence across knowledge representation survives
  in distributed form. The operational test for "D explains both sides" was
  the step's refinement of the plan's prose; candidate list is the plan's,
  verbatim.
- **Consequences:** (1) Phase 4 transport/replication work builds on THIS
  protocol module (deltas, idempotent merge, reconciliation) — the design
  doc's scope guard (no transport in Phase 3) is deliberate: the protocol is
  the deliverable. (2) Timestamps are opaque metadata: merge/reconcile never
  consume them (E3.3 pins fixed timestamps for reproducibility, deviation
  D-m5); ordering/liveness are transport concerns, out of scope here.
  (3) The `declares_context` assertion makes context terms first-class and
  queryable — the reasoner can inspect WHY a contradiction was resolved
  (inspectability, acceptance check #6).

## ADR-0017 — E3.6 operationalization: plan-family clarification policy, bounded no-repetition search, gap = unmeetable fact

- **Status:** Accepted (2026-08-21; E3.6 official run `results/phase-3/e3.6.json`, commit be439a3)
- **Decision:** The projection design (ADR-0011) takes these OPERATIONAL
  semantics:
  1. **Search:** bounded DFS over the declared capability set (depth +
     cumulative-cost bound, sorted capability order — deterministic), with
     **no capability repetition within a plan** (deviation D8; a repeating
     no-precondition capability would make "longest valid prefix" unbounded).
     Every node of the search is either goal-satisfying, budget-stopped, or
     trace-logged with the exact reason (`precondition_failed` + missing
     facts / `no_new_fact` / `repeated_capability` / `budget`).
  2. **NoValidPlan semantics:** `gap` = an unmeetable fact — a goal fact no
     declared capability can produce (the shallowest, i.e. first in sorted
     goal order); `nearest_prefix` = the longest no-repetition sequence in
     which every step holds its preconditions and adds at least one new
     fact (the furthest point of provable work toward the goal). Both are
     reported under the `impossible` response contract (named gap + nearest
     viable plan) — the refusal is inspectable, not prose.
  3. **Clarification policy operationalization (deviation D9):** "small /
     large" search space = 1 vs ≥2 distinct valid plans for the goal; "high
     stakes" = the goal's declared stakes. Large + high stakes → **ask**
     (clarifying question over the plan branches, ≤2 discriminating
     candidate plans); ambiguous + low stakes → **choose a default** from
     the CODEX `has_default` assertions; the default is the CHOSEN plan,
     validated as a legal plan before application and recorded in the plan
     trace (overridable, visible — deviation D-m6).
  4. **Creativity constraints as store data (X2):** the pruning set is the
     store's ESTABLISHED negative facts (`<fact>=no` established property
     rows); an obsolete negative row is no constraint. Hard constraint: a
     branch whose accumulated effects touch an established negative fact is
     removed before selection and recorded in the audit trace.
- **Rationale:** E3.6 met every pre-registered check on the official run
  (validity 1.0, refusal 1.0, 4 distinct valid plans at T>0 over 3 seeds vs
  a floor of 2, T=0 deterministic, policy ask/default correct, all response
  contracts valid). The P11 property (no undeclared capability ever named)
  is pinned by a hypothesis test over 120 random goal/initial pairs — the
  plan layer can be trusted to REFUSE rather than fabricate, which is the
  claim X1 exists to make.
- **Consequences:** (1) `src/kainos/projection/` is the Phase-3 plan layer;
  later work (a real reasoner loop) calls `plan()`/`traverse()` and renders
  through `contract.py` — adding interaction types or capabilities is data
  only. (2) The simulated scope guard stands: capabilities have
  preconditions/effects but no executable side effects; a real tool-use
  integration is a NEW A/B, not a reinterpretation of E3.6.

## ADR-0018 — workspace promotion + query operational semantics (step 22)

- **Context:** ADR-0012 fixes the semantics of WORKSPACE (recursive,
  lifetime-scoped, explicit candidate promotion, sources ≠ knowledge) but
  leaves two operational gaps the E3.7 script exposes: (1) the script promotes
  a role held by a grandchild through the forked root — role resolution
  and provenance-crediting were unspecified; (2) id derivation for
  idempotent re-promotion was unspecified.
- **Decision:**
  1. `promote(root, role, codex, observer)` resolves `role` by deterministic
     BFS over the subtree; the role must be unique (ambiguity → ValueError).
     Provenance `source = workspace_<root_id>` and assertion id
     `as_promoted_ws_<root>_<role>_r<i>` credit the ROOT the promotion was
     invoked on (deviation D10).
  2. Re-promotion of the same (root, role, i) is a no-op: deterministic ids
     make idempotence a store lookup, not a comparison (the step-19
     delta-merge discipline applied inside one node).
  3. `WorkSpace.query` = BFS over all IRs at all depths; a string predicate is
     a case-sensitive substring over (subject, relation, object); result rows
     are sorted (workspace, role, index) — "what did we decide?" is a
     deterministic graph query, never a conversation re-run.
  4. Only `promote` writes workspace content into the CODEX, and only as
     candidates. `lapse` writes to results-class storage. P12 therefore holds
     by construction, and the E3.7 negative control (un-promoted IR → zero
     CODEX assertions) is recorded in the result file, not just the tests.
- **Status:** accepted. Consequences: every promoted assertion names exactly
  one workspace root (auditable lineage); a workspace can never silently
  establish truth in the CODEX — the Phase-2 verification path still
  stands between a promotion and `established`.

## ADR-0019 — cross-modal corroboration: ports → one modality-blind abstraction (step 20)

- **Context:** E3.4 must test "the same abstract CODEX represents patterns
  across modalities" with the cheapest honest modality (a synthetic vision
  port). The semantics — what a port is, where the shared abstraction
  lives, and what "one entity consolidated from ≥2 modalities" means in
  CODEX terms — were unspecified.
- **Decision:**
  1. A `PerceptionPort` is ANY mapping from a raw modality input to a
     Semantic IR dict that passes the `kainos/ir/1` boundary validation.
     Ports DECLARE their input grammar and reject everything outside it
     (honest capability surface, the P11 discipline at the modality edge).
  2. The abstraction step (`abstract_pattern`) is modality-blind and
     SINGLE: it runs on every port's IR. A cross-modal pattern is recognized
     when two ports' IRs reduce to compatible patterns (same type + object);
     modality-specific fields (actor vs. locations) stay distinct — the
     algebra unifies what is shared and preserves what is specific.
  3. Entity consolidation = per-modality corroboration in the CODEX: one
     candidate assertion per modality, `provenance.source` naming the
     modality; "consolidated from ≥2 modalities" = ≥2 distinct
     modality sources behind one term. Candidates only — the verification
     path still stands between corroboration and `established` (as in
     ADR-0018's promotion rule).
- **Status:** accepted. Consequences: a third modality (audio, real vision)
  joins by implementing `PerceptionPort` only — no change to the
  abstraction step or the CODEX; and "one algebra" is now a testable,
  falsifiable property of the reduction, not a slogan.

## Log discipline

Append-only: new decisions get the next number; a superseded ADR stays, marked
superseded, with a pointer to its replacement (as ADR-0001/0009 demonstrate).
