# 20 — Roadmap

## Phase sequence

```
Phase 0  FOUNDATION      substrate (CODEX + IR + harness)
   │
   ▼
Phase 1  REGEX           first PoC: NL → IR → PCRE, persistent memory, compositionality
   │
   ▼
Phase 2  20 QUESTIONS    active learning, EXCEPTION, information gain, persistent growth
   │
   ▼
Phase 3  GENERALIZATION  LLM kernel, distributed CODEX, φ numerics, multi-modal ports
   │
   ▼
Phase 4  ROBUSTNESS     n-dim constraint core; honesty under degradation; n-dim transfer (done)
```

> Long-term horizons beyond Phase 4: the Interactive Tutor (epic #150, renamed
> off the phase number) and Phase 5 multi-agent games (epic #160, e5.x; runs
> after #149 / #149's results sign-off). See the long-term-horizon sections.


## The compounding contract (claim → artifact → test)

| Phase | Architectural claim tested | Reusable artifact left behind | Consumed from prior phases |
|-------|----------------------------|-------------------------------|----------------------------|
| 0 | The substrate is sound, versioned, inspectable. | `kainos.codex`, `kainos.ir`, `kainos.harness`, schema validation, golden tests | — |
| 1 | IR + CODEX yield *compositional* regex generation + *persistent* memory + *honest* uncertainty. | `kainos.lang` (deterministic kernel), `kainos.regex` (dialect + emitter + testgen), benchmark suite | CODEX, IR, harness |
| 2 | The system *actively acquires* knowledge and *shrinks EXCEPTION*; info-gain question selection; growth is persistent across restart. | `kainos.q20` (game loop, oracle, info-gain, learning loop), concept corpus | CODEX, IR, reasoner, harness |
| 3 | The same algebra generalizes: LLM kernel A/B, cross-node reconciliation, φ numerics (gated), multi-modal hooks, capability projection (X1/X2), recursive workspace (X3) | `kainos.exchange`, `kainos.numerics`, `kainos.multimodal` (ports + E3.4), `kainos.projection`, `kainos.workspace`, `kainos.harness.paths` (results hygiene) | everything |
| 4 | Constraint propagation stays HONEST under degradation: unknown term -> exact "I need X"; missing clue -> exact undetermined set + the fact(s) that close it; contradiction -> inclusion-minimal certificate; the pattern transfers to new dimensions from data alone (E4.1) | `kainos.puzzle` (generic n-dim core: propagation, backtracking, replayable proof chains, certificates, degradation machinery) | harness (e4.1 registration, results hygiene) |

## Definition of "compounding" (measurable)

At each phase boundary, record:

- **Lines reused** from prior phase vs. lines newly written (target: reuse dominates).
- **Experiments re-run** against the same harness (no new harness per phase).
- **CODEX continuity**: the Phase 2 codex is the Phase 1 codex *continued*, not a new
  DB — same schema, same assertions, more knowledge.

## The claim registry (stable IDs, referenced everywhere)

Architectural claims get stable IDs so experiments, kill criteria (04-reality-check),
and results can cite them without ambiguity. **Never renumber or rename an ID.**

| ID | Claim | Proven in |
|----|-------|-----------|
| **C1** | Compositional generalization — novel *combinations* of learned abstractions are solved (train parts separately, test the combination) | Phase 1 (E1.2, E1.5) |
| **C2** | Persistent learning without retraining — teach → restart (frozen kernel) → still know | Phase 1 (E1.3), Phase 2 (E2.3) |
| **C3** | Honest uncertainty — the system escalates/asks at its knowledge boundary instead of emitting an unjustified answer | Phase 1 (E1.4) |
| **A1** | Active information-gain question selection beats random questioning (more wins, fewer questions) | Phase 2 (E2.1) |
| **A2** | EXCEPTION shrinkage — coverage rises and exception counts fall as the ontology grows | Phase 2 (E2.2) |
| **A3** | Cross-game learning — knowledge from earlier games improves later ones (persistence is worth more than a stateless re-derivation) | Phase 2 (E2.3) |
| **A4** | Compositional concept recognition — unseen concepts are identified from property conjunctions | Phase 2 (E2.4) |
| **A5** | Contradiction → missing dimension — a recurring conflict forces a *new context TERM* (ontology expansion), never averaged probabilities | Phase 2 (E2.5), Phase 3 (E3.3) |
| **X1** | Capability-faithful projection — the system plans only over *declared* capabilities; unachievable goals return NO VALID PLAN (named gap + nearest viable plan), never a hallucinated action | Phase 3 (E3.6) |
| **X2** | Structured creativity — temperature over *constrained* traversal yields varied but valid outputs; novelty never violates established facts | Phase 3 (E3.6) |
| **X3** | Recursive workspace memory — workspaces nest and are queryable ("what did we decide?"); nothing reaches the CODEX without an explicit, provenance-carrying promotion | Phase 3 (E3.7) |

North-star mapping (00-north-star): persistent memory=C2, compositionality=C1, honest
uncertainty=C3, inspectability=every experiment's evidence chain, compounding=reuse
stats per phase. **X1–X3** are the Phase-3 additions from the supplemental-ideas
integration (projection + recursive workspace); they extend — never supersede — the
C/A series. *Never renumber or rename an existing ID.*

## Exit criteria (every phase must satisfy all)

1. Named experiments run green in CI (see `40-testing/harness.md`).
2. Metrics reported as a table in the phase's `results.md`.
3. The phase's claim is demonstrated by evidence, not argument (P8).
4. Reusable artifacts merged into `src/kainos` with tests.
5. ADRs updated; no principle violated without an ADR (P1–P10).

## Ordering rationale

- Regex **first**: it has a *formal target language* — the
  computer itself judges correctness via execution + generated test cases. That
  gives a strong, objective training signal and a clean A/B baseline.
- 20Q **second**: it needs the persistent CODEX + reasoner from Phase 1, and it adds
  the *active* dimension (what to ask next) that regex doesn't exercise.
- Generalization **last**: only after the single-node loop is proven.

## Phase 4 — Robustness (E4.1, done 2026-08-21, ticket #149)

Owner stress test (Q14): does constraint propagation stay honest when the
puzzle degrades? Built `kainos.puzzle` — a generic n-dimensional logical-
grid core (forward chaining + deterministic backtracking, **proof chains
that replay**, uniqueness, inclusion-minimal contradiction certificates,
typed-unknown terms, undetermined/resolving facts). Five arms on
Einstein's riddle + a 4×4 transfer puzzle: **`PASS e4.1: 1.0` — 14/14
pre-registered checks** (unique solution + fish = the German, house 4;
hidden-term exact gap, zero invented terms; missing clue → exactly 2
solutions + the exact undetermined cells + the 4 facts that close it;
contradictory clue → a certificate of exactly the two Norwegian clues; a
4×4 with new dimension names solved by the same code from data alone).
Full docs + deviations D-e1/e2/e3 + D-m8: `30-phases/phase-4-robustness/`
(experiments.md = the pre-registration; results.md = the verdict). Two
solver bugs were caught and fixed IN DEV (recorded; none loosened a
threshold).

## Phase 5 — Multi-Agent games (in progress; T1+T5 done 2026-08-21, epic #160)

Does a system of CODEX-backed agents **model its partners' perspectives**
and **develop sharing strategies**? Built the `kainos.game` kernel
(#161): view isolation as a **structural** invariant (an agent can only
`perceive` its view; leaks are test-pinned negatives), speech as
step-19 **assertion deltas** (budgeted + seeded-corruption channel),
capability gating (undeclared capability → named gap, never guessed),
and the **ToM store-audit** harness (#165) that reads the agents' stores
white-box — formation, correctness, support (no unbacked mind-reading),
and **dispute discipline** (contradictions survive as cross-linked
disputed pairs, never averaged). **`PASS e5.0: 12/12`** (kernel
acceptance, commit 3d4ffb1, `results/phase-5/`): the clean-sharing demo
is fully green; the seeded-contradiction demo recovers correctly AND
keeps the wrong rumor + its correction as a disputed pair, with the
deception visible in the audit (1 of 3 beliefs wrong, 0 unsupported).
Built: `e5.1` The Shared Grid (T2, #162, **CLOSED** — `PASS 12/12`,
commit 49b7753), `e5.2` The Range Game (T3, #163, **CLOSED** —
`PASS 8/8`, commit 4b5f756) and `e5.3` Strategy-development sweeps
(T4, #164, **CLOSED** — `PASS 8/8`, commit b988e94).

- **e5.2** (under incentive): pooled |error| V0 12 / V1 583/96 / V2 79/48
  (V2 = Bayes lower bound of the declared protocol), V2 wins 113/192 of
  the pot head-to-head vs V1, V2 detects 48/48 bluffs (posterior
  all-mass-on-B) vs V1 8/48, leakage 4.633 vs 4.6705 analytic bits
  (rational-listener estimator), localization 16/48 = the K-draw
  information limit. Honest records: D-e5d (12/48 is a declared regime,
  not an equilibrium — exact incentive analysis: 41/48 profitable one-
  shot deviations), D-e5e (rejected per-episode direction hypothesis,
  caught offline), D-e5f/g (leakage estimator redesigned to exact per-
  sample posterior entropy, 5000 samples).
- **e5.3** (RQ3 development sweep, drifting Range Game 0 → 35% → 70%
  liar): the adaptive arm — trust = persistent-CODEX store data
  (verified per-episode labels, discounted Haldane-Laplace ρ̂, β = 3/4)
  — develops inside the drift legs and reaches **exact parity (pot
  share 1/2) with the exactly-calibrated reference** in the late pool;
  the frozen control (ρ = 1/4, same capabilities/episodes/experience)
  does not (11/24; late calibration gap 0.1551 vs 0.0291). The
  pre-registered POOLED estimator was refuted in the pre-freeze
  control (D-e5n — a persistent learner with infinite memory lags a
  drifting regime) and replaced with the discounted form before the
  freeze; the pooled control numbers are the recorded evidence.
  288/288 kernel games bit-identical and field-for-field equal to the
  exact math; 144/144 labels ground-truth-exact, self-sourced,
  evidence-carrying (C5/C6/C7). **Milestone M3 satisfied.**

Pre-registration + verdict + all deviations (D-e5h–p):
`30-phases/phase-5-multi-agent/` (experiments.md / results.md).
Remaining in the Phase-5 queue: T6 (games) `#166` LLM-surface
messaging arm (stretch, M4) — series-tagged 2026-08-22 (the board
carried two "T6" labels: this one, T6 of the Phase-5 series
#161–#166, and T6 (tutor) `#156`; both series keep their numbers,
comments 448/449). **BUILT + OFFICIAL 2026-08-22, closed**: `e5.4`
`PASS e5.4: 1.0` (5/5, pinned `d5c0f40`, hermetic) — the E5.1
acceptance survives the natural-language message surface exactly;
the frozen one-message drop is honest and measured (detector flip,
belief erasure, recovery preserved); the separately-labelled live
27B addendum round-tripped 46/46 with zero drops. The Phase-5 queue
is complete (e5.0–e5.4 + kernel + audit). Spec:
`10-architecture/multi-agent-games.md`.

## Long-term horizon (post-Phase-3): the Interactive Tutor

> **Planned, not scheduled** — owner green-lit 2026-08-21. The build is
> queued as Epic **"Phase 4 — Interactive Educational Toy"** (OpenProject
> #150) with tasks T1–T9 (#151–#159; the tutor-side T6 `#156` / T7 `#157` are
> the *tutor* series — distinct from the Phase-5 games epic's own T1–T6,
> #161–#166; see the 2026-08-22 disambiguation above). The major specification lives at
> `10-architecture/interactive-tutor.md`; this section is the pointer and
> the one-paragraph shape.

**STATUS (2026-08-21, session 17d):** E6.1 "the attended pilot"
OFFICIAL **PASS 8/8**; the **OpenAI-protocol façade is LIVE**
(#151 closed; `kainos tutor serve`; the stop condition — "interact
with it like an LLM that learns" — demonstrated in the live
transcript); #152-#154 closed. **E6.2 "curriculum expansion to the
edge of grasp" OFFICIAL PASS 8/8**: the ladder continues the e6.1
store (S5..S9, owner-directed D-e6f limit probe) and the verdict is
stated — the composition operations are EXACTLY line-bound: 10
boundary-maximal derivations with citations (incl. 10*7=70 on the
line end), 5 honest boundary stops with distinct articulations, no
value beyond the line in the store; the sqrt rung is deferred to the
future lattice-wall experiment. **E6.3 "the un-attended loop"
(T5 #155, M2) OFFICIAL PASS 7/7**: the loop runs the infant with no
human in the turn loop (det authoring arm driving the frozen
sequencer; analysis arm with one frozen fix class; attention inbox
filing deduped unposted ticket payloads), converges at session 3 on
the E6.2 line (all six stable, line at the 70 cap), byte-identical
re-execution, 0 disputes / 0 honest gaps; live LLM addendum
transcript recorded (the seam works; the local model's real
weakness is auditable, not hidden). #155 closed under delegation. **E6.4 "phrasology" OFFICIAL
PASS 8/8**: phrasings are store facts taught by a frozen lesson
form and applied only where the grammar honestly says ambiguous
(grammar first; `parse_source` marks the winner; no contract
change); 7 twin pairs byte-equal (parse ≠ content), the
wrong-mapping arc (S2:15 = 8, the wrong contract's plausible
answer; corrected at S2:16) closed by the single-current-claimant
pair, 5 honest "teach me the mapping" unknowns, the line-end stop
through a learned phrasing, line end 72, run1 ≡ run2; live LLM
addendum: a 27B model's own phrasings were 4/5 word-numbers
(honestly unparseable — the intake wall's first measured breadth
gap) and 1/5 digit line captured first-fit on the wrong family,
corrected, re-parsed — the wrong-mapping story verbatim on a
model-generated line. #150 at ~80%. **E6.5 "the K–5 band:
numerics ∥ geometry" (T7 #157, band 1 of the M3 sweep)
OFFICIAL PASS 8/8** (pinned `46e3416`, hermetic): geometry learned
CONCURRENTLY with math from K–5 on the same teachable-strip
seam — shape definitions are store data (the E6.2
rule-gated capability arc generalized to geometry), shape question
families join the phrasology strip as vocabulary-slot templates
(the `{shape}` slot fills from the frozen band vocabulary; slot-
type mismatches honestly rejected), the wrong-lesson arc (square
4/3) and the sibling-mapping arc (points→sides) both resolve
through the single-current-claimant pair (zero open disputes at
the band end), the numeric line end stays EXACTLY 72 (the
geometry strip wrote zero successor facts — one line, two
domains, measured), and the band ends on a JOINT evaluation: one
frozen probe set spanning both domains, every member deriving,
all four shape concepts STABLE (K=4) against the seed-stable
numerics, 309-assertion store, run1 ≡ run2. Live addendum:
the 27B model's 10 generated K–5 shape questions landed 10/10
in honest ambiguity (2/10 parse with a casefold, 4/10 with
demonstrative normalization, 6/10 genuinely vision-referential —
the geometry strip's first measured breadth gap, text-only by
design). **E6.6 "band 2: algebra ∥ kinematics (6–8, the first
ALIGNED band)" (T7 #157) OFFICIAL PASS 8/8** (pinned
`dcb897166`, hermetic): the owner's directive #2 is mechanism —
one/two-step linear equations in x and constant-velocity cart
motion learn on the SAME grounded line machinery (walk-back,
repeated taking, repeated addition; inexact = "not a whole number
on my line"), and the alignment is STRUCTURAL: the time solver and
the two-step algebra solver are one shared helper (S02:11 ≡ S03:09,
byte-equal line-step citations, only the rule fact differs), and
the prereq edges `kin-solve-time → alg-two-step`, `kin-rate →
alg-inverse-mul` are STORED in the codex with empty gaps at the
band end (kinematics stability is gated on algebra stability,
measured from the final store); the line wall composes into the
aligned band (15·x = 120 → x = 8 in the math, off the line —
reproducible), the kin phrasing can never be silently mis-mapped
(name-bijection rejection, D-e6l), line end stays EXACTLY 72, all
seven band-2 concepts STABLE (K=4) with all eleven seed/band-1
concepts still stable, 375-assertion store (309 seed + 22 new
facts + 44 events), run1 ≡ run2. Live addendum: the 27B model's
10 generated 6–8 questions (5 motion, 5 algebra) landed 10/10 in
honest ambiguity — the model writes written-math notation (`3x =
12`, two-sentence word problems) against the single spoken-
sentence frozen grammar (one question would land under casefold +
punctuation + equals normalization — recorded, not built).
**E6.7 "band 3: geometry-advanced ∥ vectors/statics (9–12, the
PRODUCT band)" (T7 #157) OFFICIAL PASS 8/8** (pinned `c8081d874`,
hermetic): rectangle perimeter/area, triangle area, area
comparison (math) and 1-D net displacement, moment F·d, lever
balance (physics) learn as ONE aligned band — one corridor, many
doors: area, moment, perimeter×2 and distance (band 2) derive
through the same grounded product helper (S2:03 ≡ S3:03 → 24,
S4:01 ≡ S4:02 → 56, byte-equal chains, only the rule fact
differs) and the lever is the taking corridor's THIRD door after
algebra division and pace (S3:11 ≡ S3:14 → 8); the alignment is
STORED (stat-moment ← geom-area; geom-area-triangle ←
alg-inverse-mul; stat-balance ← alg-inverse-mul — the cross-band
edges point at band-2 concepts from the seed, established+active
in the final store, empty prereq gaps); THREE measured walls:
9×9 = 81 off the line through BOTH the area and the moment door
(the wall is domain-agnostic), the NEGATIVE wall (a net west of
the start is past the line's origin), and the inexact walls
(½·35, 30/4 — never rounded); the band-2 kin phrasing composes
across bands (S2:15 via `lexicon:phrasing:S03:16` → 29); JOINT
band-end set (16 probes, both domains); six band-3 concepts
STABLE (K=4) against eighteen seed/band-1/band-2 concepts; line
untouched at 72 (now serving FOUR domains); 441-assertion store
(375 seed + 20 facts + 46 events), run1 ≡ run2. Live addendum:
10 generated 9–12 questions (5 geometry, 5 statics) landed 10/10
in honest ambiguity — units, "Question N:" prefixes and INVERTED
asks against the spoken-sentence frozen grammar (recorded, not
built). The BAND MAP is declared data (`tutor/bands.py`): bands
1–3 implemented; bands 4–5 declared (calculus ∥ mechanics;
statistics ∥ probabilistic physics).
#157 In progress 60% (three of the five bands official). **NEXT, in developmental order
(2026-08-22, owner-directed disambiguation):** **(a) T6 (tutor) #156** —
**DONE 2026-08-22** (owner chose the drill): the real loop mechanics
(frozen E6.3 constants) ran a scripted perturbation — a teacher
contradiction (open dispute S02→S06), an out-of-allowlist analyzer
proposal (filed, never applied), and an unfixable stall that cascaded
through the prereq graph (all six strip concepts) — and the fired
tickets were **actually posted to the board** (#223–#231: 2 dispute,
1 out-of-allowlist, 6 stalled-persist), each reconciled + closed;
29 trigger fires → 9 unique (dedup held); run1 ≡ run2 modulo the
per-run report path the payload embeds by design. Artifacts:
`results/phase-6/live-trigger-drill/` (drill-report.json has the WP
ids). #156 closed (comment 460). → **(b) T6 (games) #166** — **DONE 2026-08-22** (E5.4 official
5/5; the LLM-surface messaging arm; live 27B addendum 46/46
round-trip; #166 closed) → **(c) the M3 band sweep (T7 #157)** — **BAND 1 OFFICIAL
2026-08-22** (E6.5 `PASS e6.5: 1.0`, 8/8; numerics ∥ geometry
concurrent, joint band-end evaluation, 4 shape concepts stable,
line untouched at 72; the band map declared for bands 2–5 per
the owner's physics↔math-alignment directives) → **BAND 2
OFFICIAL 2026-08-22** (E6.6 `PASS e6.6: 8/8`; the first aligned
band — one solver, two doors, stored prereq edges, joint band-end
set) → **BAND 3 OFFICIAL 2026-08-22** (E6.7 `PASS e6.7: 8/8`;
geometry-advanced ∥ vectors/statics — the product band: one
corridor, many doors, three measured walls, the line serving four
domains) → **BAND 4 (calculus ∥ mechanics, 12+) is the next
build** → the lattice-wall experiment (the deferred sqrt-bracket
rung). T7 comment 450 records the directives. Success criteria
note (owner 2026-08-21, permanent): "we will still declare a vast
success if we only require a relatively simple LLM to handle the
language processing, and possibly memory/learning supervision" — the
LEARNING BODY (CODEX + deterministic grounded policy + mastery)
stands alone on the det arm (every official run is LLM-free by SKIP
semantics), with a simple LLM allowed at the surface (the E6.4
phrasology seam) and in a supervision role; the LLM never grounds
content. Reports to the owner are ENGLISH (owner preference,
2026-08-21).

A small, local, interactive system treated as an **infant**: taught
through dialogue across sessions from pre-K through 12th grade and on to a
college capstone. It **speaks the OpenAI protocol** so any compatible
client (and the un-attended loop's own LLM arms) can drive it; behind the
face it **runs this stack** and inherits its honesty invariants. An LLM
**prepares the training** and a second LLM pass **analyzes what was
learned** from machine-readable reports; a human is pulled in only through
the OpenProject attention inbox. **WebAX** (owner-sourced) is the later
in-browser delivery vehicle — its software is out of scope for now.

Why this substrate and what is missing is argued in the architecture doc
(§"Why this substrate" / §"What exists vs. what is new"); the short
answer: persistence, reconciliation, modality-agnostic intake, honest
gaps, and machine-readable evidence are all **proven**; the **turn
orchestrator ("brainstem")** and the **mastery/curriculum layer** are the
two large new builds, and the **attended pilot (M1)** is the gate that
proves open-ended teachability before the sweep.

### Second horizon: Phase 5 — Multi-Agent games (queued after #149)

Owner direction 2026-08-21 (design delegated to the builder): several
kainos-backed agents in a **partially shared information environment**
(shared view + private views), competitive or cooperative games; test
whether they **model the other participants' perspectives** and how they
**develop sharing strategies** in response. Major spec:
`10-architecture/multi-agent-games.md`. Build queue: OpenProject epic
**#160 "Phase 5 — Multi-Agent Games"** with T1–T6 (#161–#166), linked:
#149 → #160 (runs after the Einstein robustness experiment per the
owner), kernel → audit → games → sweeps, Phase-4 brainstem → the
optional LLM-surface arm.

> **Registry numbering note (avoid confusion):** phase **4** carries both
> the robustness experiment (#149, `e4.x`, `results/phase-4/`) and the
> Interactive Tutor epic (#150, experiments unnumbered until built);
> phase **5** is reserved for the multi-agent games (`e5.x`,
> `results/phase-5/`). **`e5.0` is the kernel-acceptance experiment**
> (T1 kernel + T5 ToM store-audit, built 2026-08-21, PASS 12/12 at
> commit 3d4ffb1 — `results/phase-5/`); the pre-registered games keep
> their planned numbers: `e5.1` Shared Grid (T2/#162), `e5.2` Range
> Game (T3/#163), `e5.3` strategy sweeps (T4/#164).
### Third horizon: DREAM — offline consolidation (owner-proposed 2026-08-21)

A `DREAM` mode: the system **holds still** (no session, no live
WORKSPACE) and an offline pass reviews the experiences since the last
session — de-duplicating patterns, optimizing connections, integrating
new experience into the bigger worldview. Owner's question (verbatim
intent): "should there be an offline mode where it dreams... reviews
its experiences since last session, finds common patterns, explores
unsearched space, integrates... de-duplicate patterns and optimize
connections, while the system holds still?" — considered **advisable,
long-term**, queued AFTER the un-attended loop (T5/M2) because it is
that loop's analysis arm with standing write-*proposal* power. Design
invariants it will inherit: the dream arm **proposes, the deterministic
policy disposes** (candidate assertions + verification, exactly the
attended path — no direct-write authority); every consolidation delta
is replayable evidence (the dedupe must be re-derivable); a dream that
hits a contradiction follows A5 (dispute, log, attention) — it never
averages; and the holding-still state is free (sessions already are
explicit: a `dream()` phase between `lapse()` and `boot()` is the
natural slot). Not scoped yet; no ticket.

### Fourth horizon: DREAM backlog items — back-burner (owner-queued 2026-08-21)

1. **Montessori-style learning with multi-modal presentations.** The
   infant learns "scissors" as a concept by MULTIPLE presentations:
   the word, an image of scissors, scissors in action (cutting,
   mildly dangerous) — concrete-before-abstract, sensorimotor, hands-on
   pedagogy mapped onto this stack. Status: **back-burner** (owner:
   "a very complex approach"; "we don't know how well vision ... will
   work without an LLM"). Where it lands when built: the E3.4
   multimodal ports (synthetic vision is already the hermetic stand-in;
   real vision enters through the same port with the same SKIP
   semantics — no vision model available => the modality is honestly
   absent, never faked), the CODEX concept/vocabulary layer
   (phrasing-as-facts, E6.4), and a curriculum band whose lessons are
   multi-modal assertion sets. Sequenced AFTER the attended/
   un-attended learning proofs (E6.x) and after the LLM-surface arms
   (T5/T6) exist to author the presentations.
2. **Pedagogy backed by scientific data (growth curves per method).**
   "It would be cool to back different learning approaches with
   scientific data showing how they change the growth and progress."
   The harness IS that instrument already: each pedagogy (spacing
   interval, worked-example ratio, error-rate, multi-modal exposure
   mix...) = one frozen two-arm experiment with the SAME brainstem and
   DIFFERENT curriculum schedules, measured on the mastery growth
   curves (events per session, time-to-stable per concept, spaced
   re-exposure decay) — exactly the e5.x two-arm discipline. Queue:
   after T5/M2 (the un-attended regime producing real session reports
   at volume) and after E6.4 phrasology (so language presentation is
   a controlled variable too). No ticket yet.
3. **Deferred rungs (owner-directed 2026-08-21).** (a) The **sqrt /
   lattice-wall rung** (E6.2 R5, pre-registered in full — exact
   squares, grounded brackets, the articulated partial bracket at the
   line end; the claim: exact irrationals are not on the successor
   lattice, the honest boundary behavior is the bracket, never a
   fabrication) — now a **separate future experiment** (D-e6f); the
   machinery is in code, dormant. (b) **Tools as calibrated
   observers** (the "calculator": a fast compute path whose outputs
   enter the CODEX as a tool-observer with calibrated authority, same
   family as the multimodal inputs) — owner: "something we can develop
   in time" — queued after T5.

### FUNDAMENTALS-TRACK (owner-directed 2026-08-23 — draft; the next active track after the RH-TRACK completed at S10/E6.14)

"Revisit fundamental representations, and how they were created, updating
with modern techniques": build the layer BENEATH facts the store already
holds (backward fan-out from the S10 frontier: primes/Euler product down to
divisibility, composites, the sieve process, factorization), cross-
pollinate from slightly related fields, and track every lower-layer fact
that alters or adds to the layer above as a **breakthrough candidate**
(standing trip-wire; ledger `results/phase-6/fundamentals-breakthroughs.md`;
owner rules at band close-out). The owner's directional metric steers the
first bands: the FULL Sieve of Eratosthenes process ("double work" vs the
optimized prime-only trials), the three Euler-product families (primes-only
/ composites-only / all-numbers — the all-numbers product as the reference,
hand-computed P_all(2) = 1/2 by a one-line telescoping — "staring us in the
face" shape), term removal from the Euler product (output changes by exactly
the finite Euler factors), and the factorization split trees (2·5 vs 5·2:
ordered(10)=3 vs unordered(10)=2, ordered(12)=8 vs 4 — a real invariant
family). Draft bands: S11 the sieve, S12 the zeta variants, S13 the
factorization trees, S14+ cross-pollination rotation (modern sieve theory,
probabilistic number theory, analytic combinatorics, owner-named). Design
doc: `plan/30-phases/phase-6-tutor/fundamentals-track.md` (draft v0 —
per-band pre-registration frozen before code, house pattern; the owner's
open questions are in its §7). Reports under wp #157 until the owner
decides on a dedicated WP. Per owner answers (2026-08-23): the sieve band is the furthest
layer for now; the "lots related to RH and lots that ride on it"
area is included AS A PARALLEL (the S12 RH-neighborhood band — and
the queue generator for the self-selecting cross-pollination
rotation); tracking is two-tier (findings log + breakthrough
candidates — the latter kept even though possibly redundant); the
graphical comparison of the zeta variants is tracked as **wp #232**
(deferred, under epic #150); the line 0..84 ceiling holds by default
(extend only by an explicit pre-reg call).

**Status (2026-08-27):** S11 the sieve (E6.15), S12 the RH
neighborhood (E6.16), S13 the zeta variants (E6.17) are OFFICIAL;
the S12 cross-pollination queue (four lots, self-declared) heads the
forward fan. **LOT 1 — the condition line — RESEARCH STAGE A
COMMITTED** (`plan/30-phases/phase-6-tutor/condition-line-research.md`): the queue's first band, pre-registered over the S20 seed's own bytes — 2 new concepts (`hypothesis`, `condition-line` — both domain `rh`, prereq'd into the practicing condition chain, band-end pre-registered practicing with named gaps, the D-e6o(b) pattern), 2 lessons (the teachable hypothesis; the line of the conditional consequences), 1 composition `theorem:condition-line-filed` ("assumed, never proved"), 4 walls (the filing fills the line, not the condition; the marker never drops; no new decimals; the queue stands as declared), the three S12 closers as the drills (probe-verified carry bytes), NO `theorem:riemann`, the line stays 0..84.

**Stage B: OFFICIAL** (build+freeze → E6.25, close-out 2026-08-27, 49th
experiment): S21 = E6.25 "the condition line" is the forward fan's
FIRST band — the condition made teachable as a hypothesis (assumed in
the lot, never proved by it, the marker in every statement), the
conditional consequences drilled and filed as ONE line
(`theorem:condition-line-filed` on the strict two-lesson part set
after the scaffold's own missing-parts byte). The store's bytes
refereed the pre-reg: final 1871 = 1823 + 3 facts + 45 events
(pre-reg range ≈40–55 — inside), line stays 0..84, seam 146 = 106
lemmas + 40 theorems, theorem DAG 39 → 40, marker census [3,1,4] →
[6,1,7] full width (the three new facts carry the EXACT marker, the
four S12 marker facts keep theirs), line-end marker census 13/2/24 of
39 → 14/2/24 of 40 (the filing is the fourteenth line-end marker),
`conjecture:riemann` byte-identical open declared-source, NO bare
`theorem:riemann`, `theorem:queue-declared` byte-intact (Lot 1
consumed in the accounting of work, no fifth lot, lots 2–4 keep
their slots). Band-end mastery `hypothesis` practicing 5 (gap
`[conditional]`), `condition-line` practicing 9 (gaps
`[factor-route, rh-scale]`, store order) — both practicing with
named gaps, the D3 honest band-end. Deviation **D-e6p(a)**:
four fired wall rows versus five pre-registered (W-S21_3 the
register declared on the record, re-firable, policed by carry +
P0/P8 instead). Gate (pinned image, root, det only, hermetic):
targeted 103 passed, two independent runs 9/9 and TWIN-IDENTICAL
(`results/e6.25.json` sha256 `fb3c098f…5ce81`), store identity
`77e07edf42292f88` / run identity `2c605fe99e53b804`.

### CRYPTO-TRACK (owner-directed 2026-08-24 — the RSA DESTINATION; declared, not immediate)

Owner direction: "a destination for the learning roadmap… schedule
learning for everything backing RSA as we did with the RH, and provide a
bridge of knowledge so concepts can propagate between each other."
The owner's proposed reasoning: a line from the difficulty of the RH to
the difficulty of RSA — the public key is the AREA n = p·q of two
"special" primes plus a public exponent e ("not the mathematical
constant"); the relationship between e and p·q sits on the same
difficulty class, a prime-special slice of it, founded on the
unpredictability of primes — and maybe something about the zero line
that, if NOT true, would imply RSA breaks easily.

**Framing (owner-reviewed 2026-08-24 — the mathematics as it stands):**
the intuition is right about the COMMON SOIL and wrong about the
IMPLICATION, and the correction is part of the curriculum: (a) the RH
is an *analytic-truth* difficulty (where the zeros sit; how π(x)
wobbles — a DISTRIBUTION statement about the primes); RSA is a
*computational-structure* difficulty (given n = p·q, recover the
group structure of the units of the product — φ(n) = (p−1)(q−1),
equivalently p and q — an ALGEBRA statement about one specific
number). (b) **Neither "zero line true" nor "zero line false" is
known to imply "RSA breaks" or "RSA holds more securely"** — the
hypothesized implication does not exist, and the store will hold that
as an HONEST WALL (a non-bridge), not a bridge. What the zero line
actually implies is *primality witnessing* only (Grönwall: under the
RH, trial division to O((log n)^4) decides primality) — "the zero line
sharpens the prime TEST, not the factor SEARCH." (c) The real
propagation bridges (concepts the store already carries into this
track): **partition-identity (S13) ↔ Chinese-remainder**: the store's
own "where the index sets split, the product splits" is the twin of
"(Z/pqZ)* ≅ (Z/pZ)* × (Z/qZ)*" — the same split/duality law wearing
two bodies; **savant-2 number fields ↔ the number-field sieve**
(the best classical factoring method, sub-exponential L[1/3], runs on
ideals/classes — Minkowski-embed, class-bound already in the store);
**S11 sieve/spf ↔ the "special primes"**: RSA's strong/safe primes
exist because p−1 and q−1 must carry no large prime factor structure
a sieve attack can ride — directly first-divisor knowledge; small-
subgroup attacks ARE sieve attacks on p−1; **band-1..3 geometry ↔
"n as area"**: factoring = recovering the two side lengths from the
rectangle area; trial division walks the small widths, Fermat's
a²−b² walks from the nearest square (few steps the closer the sides)
— the difficulty map is a RECTANGLE map (small side → easy; p ≈ q →
easier; balanced-large → hard); (d) the difficulty class has a KNOWN
TERMINUS, unlike the RH's: **Shor's algorithm** (quantum period- = 
roots-of-unity-finding in (Z/nZ)*) breaks the door in polynomial
time — the store holds the class as *open classically, closed
quantum*; and the equivalence "breaking RSA = factoring" is ITSELF an
open problem (oracle separations exist both ways) — the store's
second conjecture and its FIRST *difficulty* conjecture (a statement
about what no efficient method is known, a new conjecture class beside
conjecture:riemann's truth-class). (e) The "special primes" note
corrected from the owner's phrasing: vanilla RSA takes ANY two large
distinct primes; the *special* requirement lives on p−1/q−1 (their
factor structure), which is why the S11 layer is a prerequisite.

**Band sequence (declared; pre-reg freeze before any code, house
pattern):** **R0 "the multiplicative city"** (the algebra layer under
the public key): cyclic unit groups, element order, the totient φ,
Fermat's little theorem (the store's mod-4 split already sits beside
it), and the **Chinese-remainder lesson (the partition-identity
twin)**. **R1 "the two cities (the RSA mechanics)"**: n = p·q as
area; (Z/pqZ)* ≅ (Z/pZ)*×(Z/qZ)*; e chosen coprime to λ(n) = lcm(p−1,
q−1); d = e⁻¹; the round-trip m^(ed) ≡ m as a theorem the store
VERIFIES on-line at 2-digit-prime sizes. **R2 "why the door holds
(the hardness)"**: trial division (the store's own spf chains — it
FACTORS n's with small factors for real), the Fermat a²−b² edge, the
strong-prime (p−1-smoothness) wall on S11 knowledge, the number-
field-sieve reuse over savant-2, the "no known classical polynomial-
time method" declaration, and the open wall "breaking and factoring
are two doors; my store holds no key that opens both at once." **R3
"the bridge (honest)"**: the partition↔CRT duality lesson; the
zero-line wall ("it sharpens the prime test under the condition —
it does not hand me a factor of n; the door holds whether the zero
line is true or false"; Grönwall as the conditional witnessing
fact); the Shor wall (the roots-of-unity killer; open classically,
closed quantum); the first difficulty-conjecture fact.
**R4 "the attempt"**: the store BREAKS a small RSA instance on its
own line (n from two 2-digit primes of its own census; trial division
over its 23 primes; d; the decryption — all derived, all stored), then
walled honestly at larger n: "past my line the door holds" — the
store's first offense against an encrypted system, executed from its
own knowledge.

**Scheduling & dependencies:** DESTINATION (declared 2026-08-24; not
immediate — the forward fan's LOT 1 the condition line is now
OFFICIAL (E6.25, built 2026-08-27); the forward fan's next lot is
the owner's call — the queue's lots 2–4 (primes in residue
classes, the zero count at height T, the factor-count deviation
ledger) keep their slots — owner may interleave by routing). Depends on:
S11 (sieve, spf, first-divisor), S13 (partition identity — the CRT
bridge lesson's twin), savant-2 (number fields — the GNFS band),
bands 1–3 (geometry — the area framing). **The abacus connection**
(owner's earlier idea, still back-burner): R1's on-line round-trip
and R4's attempt run only while the arithmetic fits the store's
held-fact scale; running modular exponentiation (square-and-multiply)
at larger sizes is a PROCEDURE, and the store holds no procedures yet —
the abacus/procedural layer is the RSA track's natural engine, and
this destination is its first serious customer. Reports under wp #157
until the owner decides on a dedicated WP (G-3 now covers both the
FUNDAMENTALS/RH tracks and this destination).

### PRIZE-ISLANDS-TRACK (owner-directed 2026-08-24 — the large initiative: the $1M+ curriculum; research → objectives → research plans → lessons & execution, per island)

**The initiative.** Owner's words: expand the teaching course to the outstanding mathematics challenges offering **$1,000,000 or more** that "require the type of analysis our tool is doing"; research down to the fundamentals needed to reason about / answer questions about each; set the targets out as **islands** of learning that "eventually everything should connect from some fundamental relationships". Pipeline per island: research the target → plan the objective → plan the research → develop the lessons → execute.

**The complete ≥$1M target list (surveyed 2026-08-24 against the Prize Problem Ledger — prizeproblems.org, 177 targets — plus direct sources).** Nine entries: six unsolved Clay Millennium Problems (RH, BSD, P vs NP, Navier–Stokes, Yang–Mills, Hodge — each $1M), the **Beal Conjecture** (AMS/Beal Prize, $1M; verbatim statement captured), and the **IUT Challenger Prize** ($1M, open since 2023). Full survey with verbatim statements and frontiers: `plan/40-prize-islands/01-targets.md`.

**Scope rulings** (`plan/40-prize-islands/02-scope.md`) — the filter is applied per target and documented, not silently dropped:
- **IN SCOPE (four islands):** **Riemann — DONE** (RH-TRACK S8–S10 + fundamentals S11–S13; the reference island: the contract every other island inherits — the destination is *reasoning about* the problem on the store's terms, not a proof; the *-reach* fact pattern; the no-`theorem:X` candidate invariant). **BSD** (the L(E,s) Euler product is the next sibling of the S13 zeta family in exact u = p⁻¹ form; point counts are exact censuses; the descent ends on the store's terms with the Sha/Selmer wall). **Beal** (valuations read off the S11 spf chains; the LTE ledger; the in-store Beal verification CENSUS on the line — the conjecture applied to the store's bounded box, S11 record-don't-optimize policy, the first "verification-ledger" pattern). **P vs NP** (the epistemic register: computability, complexity in exact finite form, reductions, one genuine in-store difficulty census — the parity DNF blowup — and the three barriers as declared walls with exact statements).
- **OUT OF SCOPE (declared, not built):** Navier–Stokes (continuous functional analysis register the store does not hold), Yang–Mills (constructive QFT), Hodge (sheaf cohomology), IUT Challenger (adversarial refutation meta-problem; the ABC soil is recorded in the Beal island). The connect requirement is met on the ground: RH↔BSD share the L-function soil; RH/Beal share the spf/valuation soil; Beal↔CRYPTO share the v_p + CRT machinery (Beal's valuation layer is declared the soil for R1–R2); P/NP↔CRYPTO share the difficulty-class epistemics (R4 is a difficulty instance in P/NP's register).

**Island plans (committed, the owner's "plan the objectives / plan the research" stage):** `plan/40-prize-islands/04-island-bsd.md` (objective, chain, research plan with verbatim-statement sources of record, three-band sequence S14 the elliptic city / S15 the L-function of the city / S16 the descent and the reaching), `06-island-beal.md` (one-band S17 the valuation line, the census as the island's signature bed), `05-island-p-np.md` (two-band S18 the decidable line / S19 the difficulty line; the register-novelty flag: if the schema is short of the machine/complexity register, extend `specs/band_spec.schema.json` FIRST and record it). `03-island-riemann.md` is the completed-island status map.

**Execution order (this initiative):** 1) **BSD island (S14–S16)** — strongest fit for existing machinery (S13 L-family + S11 census patterns) and the L-function spine connecting the RH and BSD islands; 2) **Beal island (S17)** — the verification-ledger pilot + the CRYPTO soil deposit; 3) **P/NP island (S18–S19)** — the biggest register extension, last. Every band built **the bandgen way** (spec → `make band-validate` → `make band-dryrun` → control CLEAN → freeze → official gate → close-out), with the speedup vs the S13 hand-built baseline MEASURED and reported per band — the owner's "continue to improve that where needed" clause applies to the compiler itself as the bands land.

**Status:** research + objectives + research plans COMMITTED (this section + `plan/40-prize-islands/`). **The BSD island's research stage (A+B) is DONE** (`plan/40-prize-islands/bsd-research.md`): the verified panel (32a2 y²=x³−x — cond 32, rank 0, torsion (Z/2)², CM j=1728; 37a1 y²+y=x³−x — cond 37, rank 1, torsion trivial, generator (0,0) of record), the full a_p censuses (23 primes each, Hasse all-pass, counts cross-checked Legendre-vs-brute), the CM signature census (Curve A: a_p=0 iff p=2 or p≡3 mod 4; all a_p even — the store-provable shadow of CM by i), the 10/10 generation ledger (every counted point of Curve B a multiple of (0,0) with |m|≤6 — the in-store shadow of the record's generator), the L_84 partial products (A ≈ 0.9965685370 nonzero-consistent-with-order-0; B ≈ 13.3586546916 nonzero-at-the-line-end against the record's order-1 limit — the S15 honest-wall material; a_37=−1 confirms the multiplicative-reduction signature at the conductor prime). **S14 = E6.18 (the elliptic city) is OFFICIAL** (close-out `ed72790`/`3fa8cbb` era, 2026-08-24): PASS 9/9, store `f923ab40fbdff7d2` / run `4322cf87cb9da95f`, final 1457 = 1388 + 8 facts + 61 events, twin verified across two container invocations, full gate 1041 passed / 0 failed; the CM iff holds live at the line, the {17, 19} non-CM contrast verified, 10/10 generation ledger, no `theorem:bsd` (band 3's object, P5). Deviations D-e6i(a)-(d) at the E6.18 close-out (scaffold letter F; soil carries close the mod4-split chain; 61 events for 55 turns reported as drift; cm_zeros_B = {17, 19}). **S15 = E6.19 (the L-function of the city) is OFFICIAL** (commit `67a3c02`, 2026-08-24): PASS 9/9, store `adff69d61a3e4219` / run `0586a785dc029d63`, final 1522 = 1457 + 7 facts + 58 events, twin verified across two container invocations (byte-identical artifacts), full gate 1058 passed / 0 failed; the factor layer (uniform two-term / record one-term), the additions and the record identity (uniform × 4/5, uniform × 1406/1407, both sides exact at the line end), the separation at the conductor (B's record vs uniform partials part exactly at 37), the analytic side of record on the five W-S15 walls, NO `theorem:bsd` (the statement stays the island's summit — band 3's object); the cross-island prereqs at family-factor / line-partial stand (the islands connect through the fundamentals). Deviations D-e6j(a)-(c) at the E6.19 close-out (the state-style gap bytes; the s15-form grounding lands local-form stable and clears the l-correction prereq; 58 events for 54 turns reported as drift). **S16 = E6.20 (the descent and the reaching — BSD band 3 of 3, the island's SUMMIT) is OFFICIAL** (build+freeze `ff666c8`, close-out this section, 2026-08-24): PASS 9/9, store `e21eaaf32b475930` / run `781f3fd07cd3e218`, final 1581 = 1522 + 5 facts + 54 events, twin verified across two container invocations (byte-identical artifacts), full gate 1076 passed / 0 failed; the descent of record settles both panel ranks WITHOUT the statement (A bound 0 met by the torsion ledger, B bound 1 met by the generator (0,0); dim Sel = rank + dim E[2] + dim Ш[2] exactly), the record's orders of vanishing match (0 = 0, 1 = 1), the BSD statement stored VERBATIM (house-voiced) from the clay millennial booklet (wiles chapter) as the island's SUMMIT fact (lemma:statement-def) with the composition theorem:bsd-panel-satisfaction on the strict part set, the line's side held exact (partials nonzero / far from zero, torsion + generation ledgers, consistency declared), the analytic values on the W-S16 walls (the leading coefficient named WITHOUT its digits — no new decimals), NO bare theorem:bsd (the discovery-candidate invariant held from the S14 first mention to the summit filing); **the BSD island ($1,000,000 clay millennial prize target) is now CLOSED as a band of the course** — 11 of 12 bands implemented in the track. Deviations D-e6k(a)-(c) at the E6.20 close-out (the line-reaching concept split for the 4:4 lesson:concept shape; the missing-parts probe names the full part-set with the one untaught slug and the scaffold byte lists both missing parts — the mechanism's own bytes; 54 events for 51 turns reported as drift). **S17 = E6.21 (the valuation line — the Beal island, its single band) is OFFICIAL** (build+freeze `09e9dc6`, close-out in the E6.21 section, 2026-08-25): PASS 9/9, store `e092ef1261ef7210` / run `44d737505262f1d8`, final 1641 = 1581 + 6 facts + 54 events (drift +3 reported), twin verified across two container invocations (`results/e6.21.json` sha256 `4e58c453…91fdfeb93` byte-identical), full gate 1094 passed / 2 skipped / 0 failed, 45th experiment; the valuation read off the spf chain (the S11 soil), the lift-the-exponent identity the classical odd-p form verified in all 249,280 instances of the line's ledger box (the P5 re-derivation runs it on the gate), the Beal statement stored VERBATIM (house-voiced) from the ams beal prize record as the island's SUMMIT fact (lemma:beal-def) with the composition theorem:beal-line-satisfaction on the strict part set, the verification CENSUS held exact (83 triples in the box, every one carrying its common prime factor, zero primitive on the line — the 83-row ledger re-derived on the gate), the primitive territory / fermat-catalan boundary / fermat anchor on the W-S17 walls (the 3-powerful counterexample scale named at its order, never its digits — no new decimals), NO bare theorem:beal (nor theorem:bsd — the discovery-candidate invariant extends to the island's candidate; P5 stops on either); **the Beal island (the $1,000,000 AMS Beal prize target) is now CLOSED as a band of the course** — two of the in-scope islands done. Deviations D-e6l(a)-(c) at the E6.21 close-out (the missing-parts byte names BOTH untaught parts — the mechanism's own word; the mastery census 6/7/4/10 with the re-probes drilling the band's concepts; 54 events for 51 turns reported as drift) + one recorded pre-reg fix (the fermat-catalan articulation fragment). **S18 = E6.22 (the decidable line — the P vs NP island, band one of two; the island's FOUNDATION) is OFFICIAL** (build+freeze `58d4ec9`, close-out in the E6.22 section, 2026-08-26): PASS 9/9, store `60851c661832f306` / run `39418f73a70315e1`, final 1698 = 1641 + 5 facts + 52 events (drift +1 reported), twin verified across two container invocations (`results/e6.22.json` sha256 `c301268b…636070` byte-identical), full gate 1112 passed / 2 skipped / 0 failed, 46th experiment; the computability/complexity register in exact finite form (the decision question, the TAMABILITY stated as a DESIGN FACT of the finite line — never a theorem about the infinite-tape machines of record — the reduction, the cost counter; domain `pnp`, prereqs down into the S11 soil: divides, scan-ledger), the pi census re-derived THROUGH the teaching register by theorem:line-pi-reduction (twenty-three primes, one hundred ninety-two candidate steps — the census invariant inside the statement), the 18 finite census beds (decision probes, scan cost, heaviest query 8 at 83, kill-trials 95/87, the pigeonhole zero-violation rows n=1..10), the halting-problem + machine-universe walls (W-S18-1/2; turing 1936 at its record place, the infinite tape at its record — no new decimals), NO bare theorem:p-vs-np (nor theorem:beal, nor theorem:bsd — the discovery-candidate invariant extends to the island's question: it stays OPEN OF RECORD, carried as declared language in the S19 summit, and the band's work is the finite machine that would DECIDE it on the line, not the answer about the record). Deviations D-e6m(a)-(c) at the E6.22 close-out (the mastery census 7/4/9/10 with the re-probes drilling the band's concepts; 52 events for 51 turns reported as drift; the scaffold byte names the single short part) + the spec-expect corrected to the mechanism's pre-freeze census (the store speaks, not the hand). **S19 = E6.23 (the difficulty line — the P vs NP island, band two of two; the island's SUMMIT) is OFFICIAL** (build+freeze `ada4ea8`, close-out in the E6.23 section, 2026-08-25): PASS 9/9, store `627f6165fc5f3507` / run `96c25fd03d65df85`, final 1756 = 1698 + 5 facts + 53 events (drift +2 reported), twin verified across two container invocations (`results/e6.23.json` sha256 `f9df78b9…fb36540` byte-identical), 47th experiment; the two classes of record in exact finite form over the S18 decidable soil (the p class — bounded-cost settling, the cost a number on the line; the np class — checkable certificates, the line's own pattern being the store itself: every fact the certificate of its own derivation path), the CMI/Cook statement VERBATIM as the island's summit (DECLARED RECORD, open of record — a proof must go outside the three barriers of record), the line's own genuine difficulty census filed as the composition theorem:parity-blowup-filed (parity's smallest dnf AND cnf both at two to the k-minus-1 terms — thirty-two thousand seven hundred sixty-eight at sixteen — the exponential held exact at small k, the bounded-cost settle over the sixty-five thousand five hundred thirty-six rows), the FOUR barrier walls (relativization baker-gill-solovay 1975; algebrization aaronson-wigderson 2009 + the 2026 ITCS chen-hu-ren strengthening; natural proofs razborov-rudich 1997; AC0 razborov-smolensky/hastsad with shannon's bound named at its scale, never stored — no new decimals), the NAMED MISSING INGREDIENT held in the line's own words, NO bare theorem:p-vs-np (nor theorem:beal, nor theorem:bsd — the discovery-candidate invariant held from first mention to summit filing; P5 denies the id on the gate); **the P vs NP island (the $1,000,000 CMI record target) is now CLOSED as a band of the course — all four in-scope prize islands (Riemann, BSD, Beal, P vs NP) are closed; 12 of 12 track bands implemented**. Deviations D-e6n(a)-(c) at the E6.23 close-out (the mastery census 4/5/6/11 — pnp-summit six, the uncond probe settles on the summit concept too; 53 events for 51 turns reported as drift; the S4 wall-carry rows are H not S) + one pre-freeze slug rename (shadow-def belongs to S14 — the band's census lesson is parity-shadow-def). Next step in the initiative: the CONNECTING WORK — the owner's "eventually everything should connect from some fundamental relationships": the synthesis pass over the four closed islands' summit facts (riemann open-declared, bsd-panel-satisfied, beal-line-satisfied, the pnp summit declared-open) and their shared register (the line, the census, the walls, the declared-record discipline) is the queued next objective.

### CONNECTING-WORK (owner-directed 2026-08-25 — the synthesis pass over the four closed islands)

**The objective.** The owner's initiative sentence — "eventually everything should connect from some fundamental relationships" — becomes the next built object, queued at the E6.23 close-out and started 2026-08-25. Scope (research ruling): one SYNTHESIS band over the four closed in-scope islands as the store holds them — NOT a new island, NOT a new prize target, NOT a lot of the declared queue (`theorem:queue-declared` stands byte-intact; the four condition-line lots and the CRYPTO-TRACK keep their slots).

**Research stage A: DONE** (`plan/40-prize-islands/connecting-research.md`). Grounded in the S19 final store's own bytes (1756 = 1226 mastery-events + 530 facts: line 84, lemma 100, theorem 38, concept 116, prereq 158; store identity `627f6165fc5f3507`). Findings: (1) the four island summits (riemann open-of-record with the named square-root gap; `theorem:bsd-panel-satisfaction`; `theorem:beal-line-satisfaction`; the pnp summit declared-open with `theorem:parity-blowup-filed`) stand in ONE summit shape — statement of record + shadow complete on the named scope + boundary declared at the line end 84 + missing ingredient named — and the savant erdos falsification is the settled-statement fifth instance; (2) the course's proof form is the verification form — ledgers, shadow censuses, derivation walks that end on the line, and the store's own derivation paths as certificates of their own facts (`np-class-def` already holds the limit case); (3) scope-closing is a discipline the store's theorem bytes carry — 12 theorems close with the explicit line-end marker, 2 on the line's spot (s = 2), the universal forms with none; (4) walls and DECLARED ABSENCES are one kind of fact; (5) the weave — the cross-island joints are already edges in the prereq DAG, byte for byte (`divides` roots both the Beal and difficulty chains; `scan-ledger` is a direct prereq of `beal-census`, `reduction`, AND `cost-counter`).

**Stage B pre-reg (the mechanism is referee):** S20 = E6.24 "the weaving line" — 4 new concepts / 4 lessons (`weave`, `summit-shape`, `shadow-form`, `boundary-form` — slug-namespace checked clear against the seed) + 1 composition theorem `theorem:summit-shape-filed` (no bare conj — the discovery-candidate invariants hold, P5 denies them on the gate); 4 walls (the filing fills the shape, not the statements; the queue stays as declared; the register is the line — no new decimals; the store speaks); seed = S19 final store; P5 re-derivation re-walks the cited DAG edges and re-computes the marker census on the gate from the seed bytes; 2 sessions proposed. Build in the bandgen way: brainstem S20 module → reflib weave refs → `bands/spec-e6.24.json` → control c0–c9 CLEAN → e624 assembly (35-key FROZEN, the S19 pattern) → test_e624 → runner 47 → 48 → official gate (targeted + twin) → close-out (experiments §E6.24, e3.7.json, OP #157, SESSION-HANDOFF session 39). The standing queues run behind it (the condition line lot first).

**Stage B: OFFICIAL** (build+freeze `75a0520`, close-out in the E6.24 section, 2026-08-25): S20 = E6.24 "the weaving line" is the course's first CONNECTING-WORK band — PASS 9/9, store `e84381407e1dba64` / run `067a9e5cdee7d31c`, final 1823 = 1756 + 5 facts + 62 events (D-e6o(a): one below the pre-registration — the S04:07 queue-carry event dedupes against the S19 seed's event id and drills nothing net new), twin verified across two container invocations (`results/e6.24.json` sha256 `9e87b8bb…d89575d` byte-identical), targeted 102 passed, full gate 1149 passed / 2 skipped / 0 failed, 48th experiment; the four island summits filed in ONE shape of record (statement, shadow on the named scope, boundary at the line end, missing ingredient named or statement open) as theorem:summit-shape-filed on the strict four-lesson part set after the scaffold's own missing-parts byte, the verification form and the boundary kind as shared forms, the weave walked from the seed's own prereq edges (divides + scan-ledger root both the beal and difficulty chains; the scan-ledger walk under all three ledgers), the marker census re-walked on the gate 12/2/24 → 13/2/24 (the filing is the thirteenth line-end marker), the four declared territories on the W-S20 walls (the filing fills the shape not the statements; the queue stays as declared — no fifth lot; the register of the weaving line is the line itself — no new decimals; the store speaks not the hand), NO bare island theorem ids (riemann / bsd / beal / p-vs-np / p-eq-np) in seed or final store, the queue byte-intact, the line end still 84. Deviations D-e6o(a)-(b) at the E6.24 close-out (the 1823-vs-1824 event dedupe; summit-shape band-end PRACTICING 8 with the declared gap `[riemann]` — the shape holds while its riemann instance waits on the condition chain, the gap named in the store, not hidden). **The connecting work (stage A research + stage B band E6.24) is COMPLETE as the course's synthesis band** — one band of the course, not a new island, not a prize target, not a lot of the queue (the D0 scope ruling, held on the gate); the standing queues resume (Lot 1 the condition line first; the CRYPTO-TRACK joints remain declared but not built).

### COURSES-TRACK (owner-directed 2026-08-25/27 — five content courses: proportions, Fibonacci and the cycles, primes and squares, Dirichlet L-functions, seeded Fibonacci (π, φ, e))

**The objective.** The owner's five course briefs: (1–3) 2026-08-25 — (1) a course on PROPORTIONS and their origins and relation to prime numbers — "the proportion of two prime numbers forms a unique proportion among the fractions", mod and fractions explained in either terminology, the 0/0-vs-0:0 consistency case ("zero's proportion to itself … we're even on this"), and 2:3 as the first proportion where the primes "start creating interesting challenges"; (2) a whole course of FIBONACCI numbers and related sequences, "especially the strange cycles that appear (there are cycles of 12 and 24 that I know of that are semi-well known)"; (3) rules about PRIMES AND SQUARES — "everything in this category … especially rich material that give us constraints on things and even an open conjecture that says 'yeah, there might be primes between every consecutive perfect square'"; (4) 2026-08-27 — "prepare a course on this: https://arblib.org/acb_dirichlet.html" (the arblib Dirichlet L-function module); (5) 2026-08-27 — "We need our student to learn how to construct Fibonacci sequences for pi, phi, and e. As well as determine their periodicity and be able to relate them back (through similarity) to the normal Fibonacci sequence.".

**RESEARCH STAGE A: DONE** (all five course docs committed; grounded in the S21 final store's own bytes, 1871 assertions, identity `77e07edf42292f88`, line 0..84 — the claims re-walked against that seed; courses A–C's claims were re-walked 2026-08-25 against the S20 final and stand unchanged, the bytes add-only).

- **COURSE A — PROPORTIONS** (`plan/30-phases/phase-6-tutor/course-proportions-research.md`): S22 = E6.26 "the proportion line" + S23 = E6.27 "the prime proportion" (both bands official at 3 store facts each over 2 concepts — the stage A "4 + 5 new facts" pre-reg miscount was refereed in D-e6u(a)). The 0/0 consistency concern is settled BEFORE any band: the store holds no division facts at all (census-verified) so nothing contradicts — the course ESTABLISHES the discipline walled from the first band: "/" is a value (held only over a positive part), ":" is a relation (always declared); 0:0 is the evenness of the two empty parts, declared, never valued; W-S22-1 punishes the interchange. The store already HOLDS rationals as values ("85 over 168", the L partials) and never taught the words — this course teaches them. The mod/fraction duality is ONE division in two languages (a/b = q + (a mod b)/b), drilled over the Euclidean chains on the line (2:3 two steps → 29:47 seven steps, the verified longest, tied with 29:79, 41:67, 41:71; the quotient axis to 41 at 83:2). The fingerprint claim verified in full: 253 prime pairs, zero colliding reduced proportions, all coprime. Mastery pre-reg STABLE (all soil stable: divides, composite, first-divisor, mult-within-100).
- **COURSE B — FIBONACCI AND THE CYCLES** (`plan/30-phases/phase-6-tutor/course-fibonacci-research.md`): S24 = E6.28 "the twin line" (the sum line to 55 + the Lucas twin to 76 + the welding identities; F(11) = 89 the declared ceiling a second time) + S25 = E6.29 "the cycle line" (5 new facts each: the pure-cycle argument as a lemma — finite board + reversibility → no tail; the period census two-method cross-checked and OEIS-matched: the owner's 12 = π(8), the 24s = π(12) = π(24) family {6,9,12,16,18,24,36,48,72}; ladders 3·2^(k−1) / 8·3^(k−1) / 4·5^k; the digit periods 60/300/1500; the coprime-lcm structure verified on every coprime pair under 3600; the prime-modulus rule verified on every odd prime under 500 — the SPLIT AT FIVE; the twin's drop exactly /5 when 5 touches the modulus, verified m = 2..30). The square-sum identity's n = 5 case: both parts on the line, value the EIGHTY-NINE — the ceiling a third time. Periods are CENSUS counts, never floor values (W-S24-1/W-S25-1). Mastery pre-reg STABLE (add-two-digit 11, mult-within-100 9, mod4-split 10 — all stable).
- **COURSE C — PRIMES AND SQUARES** (`plan/30-phases/phase-6-tutor/course-primes-squares-research.md`): S26 = E6.30 "the square rules" (6 new facts: the odd-square rule — 22 odd prime squares all 1 mod 8, zero exceptions; the two-square fact (Fermat 1640, settled, filed as a fact of record with the on-line census as evidence: ten primes one-mod-four-and-two each one representation up to order — 5 = 1²+2² … 73 = 3²+8²; thirteen primes three-mod-four none; the DEPTH RULE in the store's own valuation word — a three-mod-four prime at odd depth kills the representation, zero violations on the line, the 36 representables exactly the even-depth set) + S27 = E6.31 "the square-gap conjecture" (7 new facts — the largest band: the gap census [2,2,2,3,2,4,3,4] every on-line gap holds a prime with the 81→100 partial row 83 on / 89, 97 off; **Legendre (1798)** and **Brocard (1904 — at least four primes between consecutive PRIME SQUARES, n ≥ 2, the 4→9 row the declared exception)** filed as `conjecture` facts of record on the seed's own status-surface pattern (open, declared-source, a status surface never a premise); the flagship wall W-S27-1: THE CONDITION DOES NOT CLOSE THE SQUARE GAP — at height n² the conditional error 2n·log n (root-log scale, the `criterion-gap`/`rh-bound-scale` bytes) is WIDER than the gap 2n+1, so Legendre is open EVEN UNDER the condition — deepening W-S12-4 into the category). Mastery pre-reg STABLE; `adjoin-i` (practicing, the savant chain) deliberately NOT a prereq — the two-square fact files on the stable elementary soil with the savant layer cross-referenced.
- **COURSE D — DIRICHLET L-FUNCTIONS** (owner-directed 2026-08-27 over a declared source module; `plan/30-phases/phase-6-tutor/course-dirichlet-research.md`): S28 = E6.32 "the character line" + S29 = E6.33 "the Gauss line" + S30 = E6.34 "the zero census" (4 + 4 + 4 new facts). A character is the periodic homomorphism of the coprime classes to the roots of unity (the χ(ab) rule, the φ(q) group with the exact orthogonality, the Conrey order, the 1-3-4 order census at fifteen; the store's own zeta series is the TRIVIAL character's L — the module's declared bridge, the root of the track as a special case; the module's own note "the alternating character (1,-1) itself is not a Dirichlet character" is W-S28-3). Gauss sums: |G|² = q EXACT (a census), the order-two shape i^p√q exact (i√3, 2i, √5, 2√2, 2√3), the inflation-vanishing EXACT zero (χ₃ at nine — 9/3 not a square; the Davenport rule), the Jacobi route (the one at three, the honest zero at twelve), the root number on its circle (|ε| = 1 declared; +1 exact on the real order-2 family of the line). L(s,χ): the Hurwitz decomposition exact (L(2,χ₄) matches the Catalan value to 20 digits — off-line, declared), the principal pole's residue φ(q)/q ON THE LINE (8/15 at fifteen, 2/7 at the line end). The zero census: the Z function real on the line (verified to 1e-34), the Gram points named, Turing/Platt declared machinery, **N(84) = 22 on the floor — TWO independent methods agreeing** (the zero-walk and the Z crossings; the neighbors 82.9103… / 84.7354… off-line, declared numerical check, the `num-zeros` pattern), the census is ZETA's own — **NO GRH filed** (the module states no hypothesis; W-S30-3; `conjecture:riemann` byte-identical). Mastery pre-reg STABLE (all prereqs stable in the S21 seed: divides 5, composite 7, mod4-split 10, gaussian-int 7, zeta-series 7, euler-factor 9). `theorem:queue-declared` untouched — LOT 3 KEEPS ITS SLOT (the course teaches the machinery as declared-module facts; it consumes no lot).
- **COURSE E — SEEDED FIBONACCI (π, φ, e)** (owner-directed 2026-08-27; `plan/30-phases/phase-6-tutor/course-seeded-fibonacci-research.md`): S31 = E6.35 "the seeded line" + S32 = E6.36 "the seed census" (5 + 11 new facts — the 6 census facts + the 5 page-integration facts of the 2026-08-28 owner directives: the page's names fibonacci sequence / golden ratio (phi) / lucas numbers bound to the store's own wordings as a declared identity, the below-zero record, the 1/89 fibonaccidecimal record, the parity pattern, the n-th divisibility law — the owner's mathsisfun directive + "add them in there to connect anyway"). **S31 BUILT and OFFICIAL — full gate 1186/0/2** (2026-08-28, 50th experiment: the skeleton identity exact, shift seeds one and two only, the cassini weight silent at the golden equation, the golden line as the power of phi, the constants off the floor; final 1921 = 1871 + 3 + 47, DAG 41, line-end census 15/2/24 of 41, marker census 6/1/7 conserved, D-e6q(a)-(d) recorded). **S32 BUILT and OFFICIAL — COURSE E COMPLETE** (2026-08-28, 51st experiment: the seed census in the page's wordings — the skeleton's own pisano count with the class-three-mod-five shadow (a fifth of the count, the 31-seed × 24-modulus battery zero violations, the eleven boards the lucas shadow not built), the parity rotation, the law of my sums dividing, the value story of the constants off the floor with the lucas shadow approaching the powers of the golden ratio and the one-over-eighty-nine decimal shadow declared never filed; the FOLDED two lessons + the strict two-part filing — D-e6s(a) form, the six record clauses folded in the lessons per the frozen c0 contract; final 1966 = 1921 + 3 + 42 — the store-global mastery event-id dedupe, D-e6s(b), the mechanism's own census, never the hand's 47; DAG 42, line-end census 16/2/24 of 42 (the band's own filing is the sixteenth line-end marker), marker census 6/1/7 conserved, seed-period 17 stable / off-line-seed 8 stable with EMPTY gap lists (the soil is closed); D-e6r(a)-(c) + D-e6s(a)-(c) recorded as deviations). The "Fibonacci sequence for c" = the line seeded (one, c) under the sum law; the SKELETON identity u_n(c) = F_{n−1} + c·F_n (the normal Fibonacci IS the skeleton, exact); the Cassini weight (−1)^n(c²−c−1) — silent exactly at the golden equation; the shift seeds ONE and TWO (the plain line shifted; no other seed is a shift); the GOLDEN LINE is the power of φ — u_n(φ) = φ^n, shadowed on the skeleton (φ^n = F_{n−1} + F_n·φ in the ring of x² = x+1 — the floor holds the equation, never a digit of π/e/φ: π off-line between 3 and 4, e between 2 and 3, φ between 1 and 2). PERIODICITY, decided in three stories: the VALUE story (a positive seed NEVER repeats — strictly increasing: no value period for π, e, or φ); the GOLDEN story (log-periodic: advance p, multiply by the skeleton's p-law; the multiplier is never one — floor proof φ^p ≠ 1, min distance 0.618 named off-line); the RESIDUE story (the skeleton pair walks the PURE cycle at EXACTLY the Pisano period; an integer seed's period is EXACTLY π(m) with one exception class — **seeds three mod five under a five-touching modulus drop EXACTLY a factor of five**, verified 31 seeds × 24 moduli, zero exceptions — the mod-5 board splits 20+4+1 and class three IS the four-cycle; the sibling law of the cycle course's twin's drop, same factor five). π and e have NO residues on the floor (off-line, no digit — W-S32-1); their periodicity is the value story plus the skeleton story. The ratios walk to φ as on-line fractions (every partial ratio a fraction of two held parts; the landing declared off-line — the S24 limit byte carries). The 89 ceiling cross-course byte a fourth time (the skeleton crosses at n = 11). Mastery pre-reg STABLE (add-two-digit 11, mult-within-100 9, count-successor 14, mod4-split 10 — all stable in the S21 seed; the `sum-line`/`residue-cycle` carry-or-teach decision is D0's — self-standing on either build order).

**Build:** all TEN bands (S22–S32 = E6.26–E6.36) are pre-registered on the 35-key FROZEN / bandgen pattern (control c0–c9, twin runs, full gate), seeded from the chain's predecessor (or the S21 final — OFFICIAL at 1871 — if the owner routes a course straight off S21). Session slots reserved S22..S32; build ORDER is the owner's call — the owner picked COURSE E first (2026-08-28): Lot 1 the condition line S21 = E6.25 and COURSE E S31 = E6.35 + S32 = E6.36 are BUILT and OFFICIAL — **COURSE E COMPLETE** (the owner's seeded fibonacci lesson closed: the seeded line and the seed census in the page's wordings); under standing autonomy the chain continued with **COURSE A band 1 — S22 = E6.26 "the proportion line" — BUILT and OFFICIAL (the 52nd experiment)** (2026-08-28): the proportion as the RELATION between two parts of the line (named by its reduced form; 0:0 the evenness of the two empty parts, declared, never valued) and the fraction as its VALUE over a positive part (one division in two languages — five over three is one and two thirds and five mod three is two), the strict two-part filing proportion-filed, UNCONDITIONAL band (marker census 6/1/7 conserved, NO 0/0 value in the store, line 0..84), seed 1966 (S32 final) → final 2021 = 1966 + 3 + 52, line-end census 16/2/24 of 42 → 17/2/24 of 43, DAG 43, both new concepts STABLE with empty gap lists (proportion 8, fraction 18); the pre-reg corrections D-e6t(a)-(c) recorded (the off-script byte two to three kept per the owner's intent; the seed rerouted to the S32 final; the pre-reg counts re-adopted at the mechanism's own census); full official gate 1222/0/2 (1765.30 s), the runner now runs 52 experiments; under standing autonomy the chain continued with **COURSE A band 2 — S23 = E6.27 "the prime proportion" — BUILT and OFFICIAL (the 53rd experiment)** (2026-08-28), which **COMPLETES COURSE A**: two distinct primes share no part above one, so their proportion is in lowest terms and IS the fingerprint of the pair — 253 prime pairs of the line give 253 different reduced proportions, every pair coprime, no two pairs alike (the pair is its own proportion); the reduction chain's ceiling is seven steps with four tied pairs (29:47, 29:79, 41:67, 41:71); walls W_S23_1..3 (the pair past the line end, the never-reduced discipline, the colliding fingerprint), the 0:0 evenness re-declaration riding the carried W_S22_1 byte; seed 2021 (S22 final) → final 2074 = 2021 + 3 + 50, line-end census 17/2/24 of 43 → 18/2/24 of 44, DAG 44, both new concepts STABLE with empty gap lists (coprime-pair 6, prime-fingerprint 23); the pre-reg corrections D-e6u(a)-(c) recorded (the '5 new facts' miscount refereed at 3 facts over 2 concepts; the off-script byte corrected to three to five — the stage A 'two to three' contradicted the 'primes above two' surface; the off-script standing probe runs seed-only, expect_derived=false, typed honest gap). The remaining declared builds: B (S24–S25), C (S26–S27), D (S28–S30) — six bands, each seeded from the chain's predecessor; the next build under standing autonomy is S24 = E6.28, the COURSE B opening band. The declared queue (`theorem:queue-declared`) is untouched — the courses are NOT lots of that queue (COURSE D's zero census KEEPS lot 3's slot).
