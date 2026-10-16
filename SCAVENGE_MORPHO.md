# SCAVENGE_MORPHO — Pattern-transfer plan: MorphoHDL → Kainos-Logos

> **Status:** proposal (not yet approved). Created 2026-08-19 from a review of
> Mordvintsev's *MorphoHDL* article and its reference implementation `tiny_morpho.py`.
> **Gate:** each transfer below is **benchmark-gated adopt/reject** (same discipline as
> ADR-0006 for φ numerics). Nothing is merged into core unless it wins.
> **Owner:** plan review. Requires ADR-0013 (Section 4) before any step ships.

---

## 0. What we are doing — and what we are NOT doing

**We are scavenging seven runtime mechanisms and data-structure disciplines** from
MorphoHDL and re-implementing them *in our own semantics*, each behind a seam, each
with a falsifiable gate.

**We are NOT:**
- adopting MorphoHDL as a data representation layer (its edges are bit buses, not
  typed relationships with provenance/epistemic state — incompatible with P1/P3/P6);
- adding MorphoHDL as a dependency, a language, or a compiler;
- committing Morpho code (patterns only; the source is Apache-2.0 so adaptation would
  be legal, but pattern-borrowing keeps the tree clean — no foreign substrate);
- building circuits, LUTs, or hardware. The hardware shell is irrelevant to us.

**Why scavenge at all:** Morpho is a working demonstration that *a tiny kernel of
rewrite rules + a fallback mechanism + aggressive interleaved pruning generates
unbounded, correct structure from compact, size-agnostic definitions*. That is
precisely the operational shape of our C1 (compositional generalization) and A5
(contradiction → dimension) claims. Its mechanisms are small, verified, and
transferable; its semantics are not.

---

## 1. Source of truth (verified against code, not just the article)

| Asset | Location |
|-------|----------|
| Article | https://paradigms-of-intelligence.github.io/morpho/ (md: `article.md` beside it) |
| Reference implementation | https://github.com/paradigms-of-intelligence/morpho → `tiny_morpho.py` |
| License | Apache-2.0 (header of `tiny_morpho.py`) |

Mechanisms **confirmed in `tiny_morpho.py`** (this is what we claim we're borrowing):

1. **Fallback as exception-unwinding.** The `@morpho` wrapper runs the cell body in
   `try/except IndexError`; on boundary failure (bus < 2, out-of-bounds access, empty
   gate input) it unwinds to `fallback` — a callable, or `fallback=N` (pass-through
   argument #N). Base cases are ordinary functions that simply don't throw.
2. **Materialization registry.** `jit_runner` compiles a cell once per concrete
   `arg_sizes` signature and caches the compiled circuit in `circuits[arg_sizes]`.
   The compiler itself resolves children on demand: it pauses the parent's wiring,
   resolves concrete input widths, compiles the child, then resumes.
3. **Interleaved optimization.** `CircuitCompiler._optimize_gate` runs *during*
   construction: constant propagation (`fix_lut_input`, `lru_cache`d), duplicate-input
   merging (`merge_lut_inputs`, `lru_cache`d), ignored-input detection (trip inputs
   where the LUT is invariant), buffer elimination, gate reduction — with counters
   (`const_elim, buf_elim, gate_reductions, dce_elim`). `strip_unused_gates` does DCE.
   Optimization runs between expansions, never only as a post-pass.
4. **Cell substitution ("alleles").** `G_Overrides` contextvar +
   `overrides.get(f.__name__, f)` lets a caller swap a sub-cell (base case) at the
   call site without rewriting the recursion — `grid(x, y, grid_base=base_skip)`.
5. **Dynamic width inference with a determinism contract.** `SPLIT` halves with
   `x[:n//2], x[n//2:]` — odd widths route the middle wire to the upper half,
   deterministically; `LSLICE`/`HSLICE` raise `IndexError` when the reference bus is
   wider than the source (→ fallback).
6. **Size-agnosticism + pass-through base cases.** Same definition, any width; base
   case is often "return an input unchanged" (`fallback=0`).

The article's future-work section (recurrent `REG`, genome/gene/expression genotype)
is **design discussion, not implementation** — we cite it as inspiration only (M7).

---

## 2. The transfer inventory (stable IDs M1–M7; never renumber)

| ID | Borrow | Morpho mechanism | Lands in (Phase) | Gate / experiment |
|----|--------|------------------|------------------|-------------------|
| **M1** | Specialization cache | `jit_runner` registry keyed by concrete signature | regex resolver (1); lifted to workspace (3) | E1.2 parity + speedup; semantic-neutrality |
| **M2** | Prune-while-growing | interleaved const-prop/DCE | q20 learn loop (2); projection planner (3) | E2.2 EXCEPTION shrinkage / frontier size |
| **M3** | Fanout-bounded reference materialization | buffer insertion at fanout limit | codex store (2–3) | query-time vs. fanout microbenchmark |
| **M4** | Fallback unwinding → NO VALID PLAN | `except IndexError → fallback` chain | projection planner/contract (3) | E3.6 X1 (gap + nearest viable prefix) |
| **M5** | Space–time duality → promotion policy | unroll in space vs. run in time (`REG`) | workspace promote (3) | E3.7 X3 + compounding reuse stats |
| **M6** | Largest-first upper-bound ordering | greedy "largest final size" expansion | q20 selector (2); planner (3) | E2.1 vs. random; E3.6 search cost |
| **M7** | Flat genome: binding-point capability encoding | genome→gene→expression; cell substitution | projection capabilities (3); reconciler | E3.3 / E3.6 representation quality |

### M1 — Specialization cache (materialization registry)

**Mechanism:** compile once per concrete signature; cache; never re-derive.
**Our version:** `SpecializationCache` — memoized partial evaluation of
`(abstraction, concrete_context_signature) → resolved sub-IR / sub-plan`. The cache is
**operational, not knowledge**: it is re-derivable and dies on restart, which
*sharpens* the C2 boundary (what must survive restart = CODEX; what may be
regenerated = cache).
**Lands:** `src/kainos/regex/resolver.py` first (cache key = resolved-term +
context hash, used by E1.2), then lifted to `src/kainos/workspace/spec_cache.py` in
Phase 3 (G3 rule: a shared seam only when a second genuine consumer appears).
**Gate:** E1.2 must produce *identical* results cached vs. uncached (semantic
neutrality), and a measured wall-time reduction on the compositional set. If it
changes outputs, reject.

### M2 — Interleaved simplification (prune-while-growing)

**Mechanism:** constant propagation + DCE as local rewrites *between* expansion steps;
overproduce, then prune (the article's morphogenesis/apoptosis parallel).
**Our version:** in the q20 learning loop and the projection planner, prune dead
branches *as the frontier grows* and simplify vacuously-satisfied sub-goals at expand
time (constant propagation in the semantic sense: a sub-goal already entailed by the
current state collapses).
**Lands:** `src/kainos/q20/learn.py`, `src/kainos/projection/planner.py`.
**Gate:** E2.2 — EXCEPTION shrinkage and coverage at equal or fewer frontier
expansions vs. the current post-hoc cleanup; planner frontier size at equal plan
quality (E3.6). Track eliminations with counters mirroring Morpho's stats
(`const_elim, dce_elim, gate_reductions` equivalents) for inspectability (P9).

### M3 — Fanout-bounded reference materialization

**Mechanism:** if a net's fanout exceeds a limit, split destinations and insert
buffers — a shared signal becomes materialized at intermediate points instead of one
giant fan-out.
**Our version:** when a TERM/context is referenced by more than `K` consumers in a
workspace/query, materialize it into an intermediate shared node rather than leaving
`N` raw reference edges. Improves query time (no repeated traversal of a hot shared
subgraph) and explanation traces (P9).
**Lands:** `src/kainos/codex/store.py` (+ `workspace/` in Phase 3).
**Gate:** microbenchmark — query latency vs. fanout with/without materialization on a
synthetic hot-term workload (e.g., a shared context referenced by 2–256 assertions).
`K` is a tunable constant; report the knee.

### M4 — Fallback unwinding → NO VALID PLAN

**Mechanism:** boundary failure throws → stack unwinds to the first fallback that
succeeds; if none, compilation fails honestly. Never a fabricated circuit.
**Our version:** EXCEPTION states become *triggerable control flow*, not just status
enums: a sub-goal that hits `IMPOSSIBLE` unwinds to the nearest viable parent plan;
`NO VALID PLAN` = the longest valid fallback prefix, exactly Morpho's unwinding.
This is the mechanization of P5 and X1.
**Lands:** `src/kainos/projection/planner.py` + `contract.py` (extends directive 21).
**Gate:** E3.6 — unachievable goals return NO VALID PLAN with a named gap *and* the
longest valid prefix; no hallucinated action (P11). Must also hold in the 20Q
mini-projection.

### M5 — Space–time duality → promotion policy

**Mechanism:** the same recursion, either unrolled as N cells (space) or run N cycles
with state (time) — `CAT(c_in, carry[:-1])` shifts in space, `REG(carry, c_in)` in
time.
**Our version:** a principled promotion policy for X3: **promote exactly what would
otherwise be re-derived repeatedly** — store the spatial (materialized) form when
re-derivation is cheaper than lookup; keep the temporal (re-derivable) form otherwise.
Gives the CODEX a defensible "what deserves durability" rule.
**Lands:** `src/kainos/workspace/promote.py` (extends directive 22).
**Gate:** E3.7 + the compounding reuse stats (lines reused vs. rewritten). Needs the
Phase-2 reuse metrics to exist first; if the metrics aren't in place, M5 waits.

### M6 — Largest-first upper-bound ordering

**Mechanism:** precompute estimated final expansion sizes (ignoring optimization),
greedily expand the largest subproblem first; BFS/largest are orderings, not
different results.
**Our version:** order the plan/info-gain frontier by cheap *upper-bound* cost or
uncertainty estimates, expand the largest first — A\* thinking without the machinery.
**Lands:** `src/kainos/q20/selector.py` (ordering variant on the E2.1 info-gain
selection), `src/kainos/projection/planner.py`.
**Gate:** E2.1 — upper-bound-ordered selection beats random and matches plain
info-gain at fewer expansions; E3.6 — plan search cost (expansions, time) at equal
plan quality. Pure ordering change: results must be identical, only cost may differ.

### M7 — Flat genome: binding-point capability encoding

**Mechanism (design discussion, not implemented):** keep the representation flat —
genome → genes → expressions with binding points for connectivity — so that mutation
and substitution are meaningful; cell substitution swaps a leaf behavior at the call
site.
**Our version:** encode projection capabilities (and, later, reconciler dimension
candidates) with a flat, binding-point structure so that "substitute a leaf" is a
first-class operation — the mechanical basis for the reconciler's new-context-TERM
re-expression (A5/E3.3) and for any future abstraction-discovery search (E2.5/E3.3).
**Lands:** `src/kainos/projection/capabilities.py`, `src/kainos/exchange/reconciler.py`.
**Gate:** E3.3 — reconciler can re-express X/NOT-X under a new context TERM via
leaf-substitution; E3.6 capability registry round-trip. No deep-nesting requirement.

### Tier-3 notes (record, don't act)

- **M8 — Partitioning determinism contract:** odd-width splits must route the middle
  element deterministically (Morpho: `x[:n//2], x[n//2:]`). Adopt as a rule for any
  subproblem-splitting in the reasoner.
- **M9 — Lazy resumable resolution:** pause parent, resolve child on demand, resume.
  Software pattern for the resolver if nested refs ever bottleneck.
- **M10 — "Cycles that dissolve vs. cycles that survive":** a contradiction that
  dissolves under a new dimension → A5; one that survives → permanent dispute. Mental
  model for the reconciler's decision boundary.
- **M11 — Minimal-context pruning:** ignore irrelevant inputs (RISC-V shift
  semantics). Compute minimal relevant context per query; likely already emergent,
  make it explicit.

---

## 3. Integration steps (in order)

Each step follows the directive template (`action-steps/README.md`) and must land in
the layout manifest with a G<n> entry if it creates a new durable path (per LAYOUT
rules — the tree and manifest never drift).

### Step A — Capture & record the source (read-only)
- [x] Verify the article + `tiny_morpho.py` are captured (this document is the
      transfer record; add a pointer in `plan/90-appendices/prior-art.md`). *(done 2026-08-20 — Appendix A.1, all six mechanisms verified at HEAD `3ff923f`; prior-art row added)*
- [x] Note license (Apache-2.0) and status ("conceptual sketch") in the record. *(done — Appendix A.1; ADR-0013)*
- **Done when:** this doc reviewed; prior-art pointer committed. **No code.** ✅ 2026-08-20 (#140)

### Step B — M1 in the regex resolver (Phase 1 infrastructure)
- [x] Add `SpecializationCache` to `src/kainos/regex/resolver.py`; key =
      `(abstraction, context_signature)`; used by the E1.2 pipeline. *(commit 1a7ff66, 2026-08-20)*
- [x] Semantic-neutrality test: cached vs. uncached produce identical outputs
      (mirror `tests/numerics/test_seam_neutral.py` style). *(tests/regex/test_m1_cache.py)*
- [x] Benchmark wall-time on the compositional set → `results/scavenge/m1.json`
      (new `results/scavenge/` dir; record as **G9** in LAYOUT). *(seed-corpus
      interim run 2026-08-20, preserved as m1-seed-corpus.json; FINAL run on the
      E1.2 compositional set 2026-08-21, board audit)*
- **Verification:** `pytest tests/regex -q && kainos experiment run --name e1.2`
      (parity unchanged) + `results/scavenge/m1.json` contains `{identical: true,
      speedup}`. ✅ — final values on the E1.2 set: `identical: true`,
      speedup 1.60 (916µs → 574µs; 51 hits / 5 misses, 40 records).
- **Gate:** identical outputs **and** measurable speedup, else reject M1's cache.
      ✅ **ADOPTED (2026-08-21)** — the gate is met on the E1.2 compositional
      set itself; ADR-0013 §4 carries the verdict line.

### Step C — M2 in the q20 learning loop (Phase 2)
- [x] Interleave dead-branch pruning + vacuous-subgoal collapse into
      `src/kainos/q20/learn.py`; counters per Morpho stats for P9.
      *(REJECTED — sweep 2026-08-22: no growth frontier exists in the loop
      (sequential consolidation pass; e2.2.json carries no frontier/expansion
      statistic); pruning conflicting evidence would violate the keep-
      contradictions invariant. Verdict in ADR-0013 §4.)*
- [x] E2.2 must show EXCEPTION shrinkage at equal-or-fewer frontier expansions.
      *(The E2.2 official PASS is the margin of the EXISTING cleanup path
      (dimensions_grown: 6); the M2 variant has nothing to beat.)*
- **Verification:** `kainos experiment run --name e2.2` + frontier-size column in
      `results/scavenge/m2.json`. *(No m2.json: the gate is vacuous — there is
      no frontier metric to fill a column with; the absence IS the evidence.)*
- **Gate:** equal coverage, fewer expansions. If the post-hoc cleanup was already
      optimal, reject (no delta). → **REJECTED (no delta; pattern mismatch)."

### Step D — M3 in the codex store (Phase 2/3)
- [x] Fanout-limited reference materialization in `src/kainos/codex/store.py`;
      tunable `K`; report the knee.
      *(REJECTED — sweep 2026-08-22: no real hot-fanout workload exists at
      project scale; the revisit knee is recorded at ~10⁴–10⁵ assertions.
      ADR-0013 §4.)*
- [x] Microbenchmark: query latency vs. fanout (2–256 consumers) with/without
      materialization → `results/scavenge/m3.json`.
      *(Ran as `results/scavenge/m3-m6-probe.json` (Docker probe): full-scan
      query() 5.4µs median / p95 11.8µs at 245 assertions (largest official
      store); 138µs / p95 162µs at synthetic 5000. No fanout-2–256 consumer
      workload to win against — the latency regime is 10⁵× below pipeline
      costs.)*
- **Gate:** materialization wins at some `K` on latency *without* degrading
      provenance (P1) or explainability (P9). → **REJECTED (no gate workload).**

### Step E — M4 in projection (Phase 3, extends directive 21)
- [x] EXCEPTION states become unwinding control flow in
      `src/kainos/projection/planner.py`; `NoValidPlan` carries the longest valid
      fallback prefix; contract updated in `contract.py`.
      *(ADOPTED-AS-NATIVE — sweep 2026-08-22: the mature planner ALREADY
      carries first-class `NoValidPlan` (named unmeetable gap +
      `nearest_prefix` + full failed-attempt trace) with DFS unwinding on
      every stop; no transfer was needed. ADR-0013 §4.)*
- **Verification:** `pytest tests/projection -q && kainos experiment run --name e3.6`.
      *(E3.6 official PASS — the verifying run.)*
- **Gate:** E3.6 X1 thresholds — named gap + nearest viable plan, no fabricated
      action (P11). → **SATISFIED by the E3.6 official run.**

### Step F — M5 in workspace promotion (Phase 3, extends directive 22)
- [x] Promotion policy in `src/kainos/workspace/promote.py`: promote what would
      otherwise be re-derived repeatedly; re-derivation cost is a measured input.
      *(REJECTED — sweep 2026-08-22: zero reuse / re-derivation counters exist
      anywhere in the mature tree, and e3.7.json carries no reuse statistics —
      the gate's own words: "else the policy is unfalsifiable — reject".
      ADR-0013 §4.)*
- [x] Depends on Phase-2 reuse metrics existing (compounding contract).
      *(Never materialized across Phases 2–6 — the dependency the risk section
      warned about; verified by grep across q20/projection/workspace/codex/
      exchange.)*
- **Verification:** `pytest tests/workspace -q && kainos experiment run --name e3.7`.
      *(E3.7 official PASS verifies the EXISTING explicit promote/lapse design
      (ADR-0012).)*
- **Gate:** E3.7 X3 + reuse stats show promotion follows the policy (else the
      policy is unfalsifiable — reject). → **REJECTED (unfalsifiable).**

### Step G — M6 in q20 selector + planner (Phase 2/3)
- [x] Upper-bound ordering variant in `src/kainos/q20/selector.py`; results must be
      *identical* to plain info-gain selection, cost may differ.
      *(REJECTED — sweep 2026-08-22: measured on the real E2 corpus (17
      questions × 149 concepts; 2.68ms median selection step, 22.25 splits);
      a tight IG bound requires exactly the split evaluations it would save,
      and the only a-priori bound (H(H)) ties every candidate — zero pruning
      power. ADR-0013 §4.)*
- [x] Same ordering in the projection planner.
      *(The planner is a bounded DFS over a small declared capability set, in
      sorted name order with a no-repetition rule (D8) — the ordering is the
      determinism contract; an upper-bound variant has the same bound issue
      (tight plan-cost bounds are the search itself).)*
- **Verification:** `kainos experiment run --name e2.1` + `e3.6`; expansion-count
      columns in `results/scavenge/m6.json`. *(Measured as `m3-m6-probe.json`;
      no variant was built — with zero pruning power an "identical answers at
      equal expansions" variant would be the current code under another name.)*
- **Gate:** identical answers at equal-or-lower expansion count.
      → **REJECTED (no delta — equal is the best achievable).**

### Step H — M7 in capabilities + reconciler (Phase 3)
- [x] Flat binding-point encoding in `src/kainos/projection/capabilities.py`;
      leaf-substitution as a first-class op in
      `src/kainos/exchange/reconciler.py`.
      *(ADOPTED-AS-NATIVE — sweep 2026-08-22: capabilities are flat store rows
      and the planner's move set loads purely from them ("granting a capability
      with a new name is itself the store-operation way — no code change, P11");
      substitution = obsoletize_capability + seed_capabilities, composition
      untouched. The reconciler's role is cross-node merge/reconciliation
      (ADR-0016), not leaf swapping — no op missing. ADR-0013 §4.)*
- **Verification:** `pytest tests/projection tests/exchange -q && kainos experiment
      run --name e3.3`. *(E3.3 official PASS (exchange) + E3.6 official PASS
      (planner move set) are the verifying runs.)*
- **Gate:** E3.3 — new context TERM produced by substitution; both assertions
      `established` under distinct contexts. → E3.3 official PASS.

### Step I — Consolidation (after all gates)
- [x] ADR-0013 (Section 4) records the adopted/rejected verdicts and the
      pattern-not-dependency rule. *(DONE 2026-08-22: M1 adopted (1.60x), M2
      rejected (no delta / pattern mismatch), M3 rejected (no gate workload,
      knee recorded), M4 + M7 adopted-as-native (gates are the official E3.6 /
      E3.3 PASS runs), M5 rejected (unfalsifiable — no reuse metrics), M6
      rejected (no delta — no cheap tight IG bound). Sweep summary line in §4.)*
- [x] `action-steps/` ledger updated (directives 10/14/21/22 scope extensions noted,
      no renumbering). *(Verified 2026-08-22: no scavenge scope extensions ever
      landed in any directive — M1 lives in `regex/resolver.py` (step 08's
      module, recorded here + ADR-0013) and the other six steps produced
      verdicts without code changes, so no directive re-scoping was required;
      the ledger is accurate as-is.)*
- [x] LAYOUT.md: G9 (`results/scavenge/`) and any new module paths recorded.
      *(DONE 2026-08-22: `results/scavenge/` recorded in
      plan/90-appendices/repo-layout.md as G9, alongside the corrected
      results/ status (committed official artifacts).)*
- [x] Adopted borrows written into `plan/30-phases/*/results.md` sign-offs with
      results cited by M-ID. *(DONE 2026-08-22: M1 cited by M-ID in
      phase-1-regex/results.md (the only adopted borrow).)*
- **Done when:** every M1–M7 has an explicit adopt/reject verdict with a written
      margin; core regression green (`pytest && make typecheck && make lint`).
      ✅ 2026-08-22 — all seven verdicts recorded in ADR-0013 §4; full Docker
      gate green on the final code state (ruff + mypy 96 files + 785 passed /
      2 skipped).

---

## 4. Guardrails

1. **ADR-0013 (proposed):** "Morpho-scavenged mechanisms are pattern transfers, never
   a dependency; each is benchmark-gated adopt/reject; no Morpho code is committed."
   Mirrors ADR-0006's isolation rule for φ numerics.
2. **Seam-neutrality regression per borrow** (M1 explicitly; same style for M2/M3/M6):
   with the mechanism disabled, the pipeline behaves byte-identically. CI must stay
   green with all scavenges off.
3. **Stable IDs:** M1–M7 (this document) and existing experiment IDs are never
   renumbered. Results cite M-IDs and claim IDs (C1/C3/X1/X2/X3) explicitly.
4. **Environment:** all benchmarks run inside the pinned Docker image (ADR-0010) on
   the Strix Halo host — **CPU-only, no CUDA**. No host-state dependencies.
5. **Inspectability (P9):** every scavenge records its counters/traces (Morpho-style
   stats) in the experiment JSON; no black-box speedups.

## 5. Risks & open questions

- **Metaphor overfit (highest risk):** Morpho's aesthetic appeal is strong and its
  semantics are wrong for us. Every borrow must demonstrate a concrete win in *our*
  domain — a speedup, a smaller frontier, a cleaner NO VALID PLAN — not a resemblance.
- **Morpho is a sketch:** mechanisms are verified only in ~870 lines of numpy code;
  corner cases are omitted. We are borrowing *patterns*, and each gate is therefore
  a real test, not a formality.
- **M3's hot-term workload is synthetic:** if no real workload in Phases 1–2 shows
  high fanout, defer M3 to Phase 3 (workspace) rather than inventing a problem.
- **M5 needs reuse metrics first:** without the compounding stats, the promotion
  policy is unfalsifiable; sequence matters (Step F after Phase 2).
- **Open:** does the LLM kernel (17) benefit from M1's cache when materializing
  repeated sub-IRs across open-phrasing inputs? Candidate extra gate, do not add to
  the critical path.

## 6. References

- Mordvintsev, A. *MorphoHDL: a minimalistic language for growing circuits.*
  https://paradigms-of-intelligence.github.io/morpho/ (article.md, tiny_morpho.py).
- Repo: https://github.com/paradigms-of-intelligence/morpho (Apache-2.0).
- Related prior art already in plan: functional HDLs (Lava, CLaSH, Chisel), L-systems
  — see the article's references for the lineage; our interest is the *mechanisms*,
  not the HDL tradition.

---

## Appendix A — Source verification & re-look at developed steps (2026-08-20, agent)

### A.1 Source verification (Step A)

Verified against the local checkout `references/morpho` (git repo, origin
`https://github.com/paradigms-of-intelligence/morpho`, HEAD `3ff923f`), at HEAD on
2026-08-20. The checkout is deliberately **untracked** — the user-managed
`.gitignore` ignores `references/` — so this appendix is the durable record; the
checkout itself is a local convenience only.

| # | Claim in §1 | Evidence in `tiny_morpho.py` (867 lines, Apache-2.0 header "Copyright 2026 Google LLC") |
|---|-------------|---------------------------------------------------------------|
| 1 | Fallback as exception-unwinding | `@morpho(f=None, fallback=None)` wrapper (L79), `try/except IndexError` (L93), `@morpho(fallback=0)` pass-through base cases (L251, L261, L307…), `partial(morpho, fallback=…)` (L81) |
| 2 | Materialization registry | `jit_runner` (L622): `circuits[arg_sizes]` compiles once per concrete size signature (L627–630), `runner._circuits` exposed (L631) |
| 3 | Interleaved optimization | `CircuitCompiler._optimize_gate` runs during construction (L424–486); `fix_lut_input`/`merge_lut_inputs` (L386/390, `lru_cache` imported L54); counters `{const_elim, buf_elim, gate_reductions, dce_elim}` (L410); `strip_unused_gates` DCE (L486–509) |
| 4 | Cell substitution ("alleles") | `G_Overrides` ContextVar (L63), `overrides.get(f.__name__, f)` resolution (L89) |
| 5 | Deterministic split + width inference | `SPLIT` = `x[:n//2], x[n//2:]` (L108); `LSLICE`/`HSLICE` raise `IndexError` when ref is wider (L110–119) → routes to fallback |
| 6 | Size-agnosticism + pass-through base cases | `@morpho(fallback=0)` recursions at arbitrary bus widths (L251–329); base cases return inputs unchanged |

**Verdict:** all six §1 mechanism claims hold at HEAD; license and "~870 lines"
scale confirmed. The article's future-work (recurrent `REG`, genotype) remains
design discussion — cited as inspiration only (per §1 and M7/M5 notes).

### A.2 Re-look: what already-developed code (Steps 01–08, commits 082c49e…a92cbac) benefits

Method: each M-ID checked against the existing tree; outcome = act now / record /
defer, with the ticket it lands in.

| M | Existing code touched | Finding | Disposition |
|---|----------------------|---------|-------------|
| **M1** | `regex/resolver.py` (Step 08) | `resolve()` re-walks CODEX (direct + 1-hop neighborhood) **per call, per tree position** — zero memoization; `describe()`'s default codex even re-seeds the lexicon. E1.2 (#119) will parse hundreds of compositional sentences: this is the first genuine multi-call consumer. | **ACT NOW** — ticket #141 (SpecializationCache, key = surface + neighborhood-signature hash; semantic-neutrality gate; `results/scavenge/m1.json`). |
| **M2** | nothing yet (no growth loops in Phase 1) | testgen generates + judges in one pass; no frontier to prune. | defer to q20 learn loop (Step 15) — ticket #142. |
| **M3** | `codex/store.py` (Step 02) | `query()`/`neighbors()` are already full-scan O(assertions) per call; with an 8-assertion seed codex fanout is immaterial. No hot-term workload exists in Phases 1–2 yet. | defer per the doc's own risk section — ticket #143, gated on a real workload. |
| **M4** | `regex/pipeline.py` (Step 08) | The escalation record `{status: requires_context, candidates, recommended_action: ask_human}` **is already the honest-uncertainty shape**; M4's future `NoValidPlan` should mirror it (named gap + longest valid prefix ≈ unresolved candidates + resolved trace prefix). | **design cross-link recorded** for Step 21 — ticket #144; no Phase-1 code change. |
| **M5** | nothing yet (workspace is Phase 3) | — | defer — ticket #145, after #131, and only once Phase-2 reuse metrics exist. |
| **M6** | nothing yet (no search loop in Phase 1) | — | defer — ticket #146, after #123. |
| **M7** | `lang/kernel.py` (Step 07) | Already leaf-swappable at the call site: `LanguageKernel` is a `runtime_checkable` Protocol and `DeterministicKernel(store)` is injected per factory — the Python twin of Morpho's `G_Overrides` allele substitution (ADR-0004 planned exactly this: deterministic kernel first, LLM kernel second). | **confirmed, no change** — the existing seam agrees with the M7 idea; #147 keeps the same flat structure for capabilities. |
| **M8** | `regex/ir.py`, `testgen.py` | Determinism already contracted: `to_ir` pre-order deterministic ids; `testgen` uses a seeded `random.Random(seed)`. No split points exist yet. | as-is; keep the contract explicit wherever splits appear (reasoner in P3). |
| **M9** | `regex/resolver.py` | Resolution is eager; Phase-1 trees are single-root and small. | record; only if nested-ref resolution ever bottlenecks. |
| **M10** | `codex/models.py` (Step 02) | The epistemic taxonomy (contested / EXCEPTION, ADR-0008) already encodes "survives"; "dissolves under a new dimension" is exactly what the Phase-3 reconciler will compute. | record; boundary model lives in the reconciler design (A5/E3.3). |
| **M11** | `regex/resolver.py` | The resolver's 1-hop rotation **is** minimal-context pruning — one bounded neighborhood, no unbounded crawl. | as-is; keep the depth bounded (recorded as an anti-scope-creep guardrail). |

**Net:** one Phase-1 action item (M1, #141 — and it lands on code written in
Step 08, so it exercises the "revisit what's developed" requirement directly),
one design cross-link (M4 → escalation-record shape), and the confirmed M7 seam.
Everything else legitimately waits for the Phase-2/3 surfaces it needs.

### A.3 Plan of record

OpenProject (project `kainos-logos`): epic **#139** with steps A–I as
**#140–#148**; wires A→B→#119, #124→C→#125, #123→G→#125, #120→D, #130→E/H,
#131→F/I. ADR-0013 records the adopt/reject discipline; prior-art.md gained the
MorphoHDL row. This appendix closes Scavenge Step A (#140).
