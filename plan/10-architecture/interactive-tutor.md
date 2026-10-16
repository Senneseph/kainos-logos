# 10.x — The Interactive Tutor: an "infant" that speaks the OpenAI protocol (long-term horizon)

> **Status: PLANNED — not built.** Green-lit by the owner 2026-08-21 as a
> long-term goal. The build is queued as OpenProject work items (epic
> "Phase 4 — Interactive Educational Toy"); this document is the major
> specification. Per the owner's scope decision: plan now, build later.

## What it is

A small, local, **interactive toy**: a system treated as an **infant** —
taught through dialogue over many sessions across a day, progressing from
pre-K through 12th grade and on to (first-year) college. It **speaks the
OpenAI protocol** (a standard `/v1/chat/completions`-style endpoint) so
any compatible client — chat UIs, SDKs, the unattended loop's own LLM
arms — can talk to it. Behind the protocol face it runs **our stack**:
CODEX as memory, Semantic IR as the universal medium, the planner as
action capability, WORKSPACE as session memory — and it *does its best to
work correctly*, i.e. it inherits the stack's honesty invariants
(never fabricate; provenance on every claim; honest gaps; contradictions
reconciled, never averaged).

**"Runs mostly un-attended":** an external LLM prepares the training
(authors curriculum + drill sessions) and a second LLM pass analyzes what
was learned and where problems developed — from *machine-readable*
session reports, not prose. A human is pulled in only through the
attention inbox (this project's OpenProject board is the on-call channel):
unresolvable contradictions, mastery regressions, or proposed curriculum
changes.

> **WebAX** (owner-sourced technology, arrives later) greatly simplifies
> and speeds development using standardized building techniques, targeting
> in-browser delivery on a powerful computer. **We do not plan WebAX's
> software here** — the tickets document the *need*; the one assumption we
> make is flagged in "Open questions".

## Why this substrate (feasibility, in one table)

The question "is the current model expandable/teachable enough?" — the
substrate says **yes, structurally**; the *proof of open-ended
teachability* is not yet in the repo (the pilot milestone is what buys it).

| Requirement | Proven today (evidence) | Gap |
|---|---|---|
| Long-lived memory that survives sessions | E2.3/E2.4 (learning across restart, frozen kernel), sqlite CODEX durable | session lifecycle glue (boot/restore/lapse as first-class ops) |
| Teach by correction, without corruption | A8 provenance; E1.3 (`user_instruction` → established after restart); E3.7 promotion discipline (candidates only) | correction flow at dialogue scale |
| Contradiction → growth, not averaging | E2.5 (A5: new `ctx:time` TERM), E3.3 (two nodes, same TERM, byte-identical convergence) | — |
| Modality-agnostic intake | `kainos/ir/1` + PerceptionPort (E3.4): any sensor/reducer that emits a valid IR joins the algebra | ports for math notation, code (band-specific) |
| Honest "I don't know / I need X" | E3.1 (fallback scoring), E3.6 (`NoValidPlan` + named gap), #149 in progress (degradation stress) | — |
| Machine-readable "what was learned" (LLM-analyzable) | harness reports: per-experiment JSON + provenance-carrying CODEX dumps | mastery model (below) turns facts into *measurable* progress |
| OpenAI-protocol face | — (thin adapter over a thin interface) | the façade (small) |
| The turn loop itself — perceive → decide → respond → remember | **No orchestrator exists today** | the "brainstem" (the biggest new component) |
| Pedagogy (what counts as "learned", what's next, spaced recall) | — | mastery model + curriculum engine (the biggest new layer) |

## Target architecture (five layers)

1. **Protocol façade (new, thin).** OpenAI-compatible HTTP server:
   `/v1/models`, `/v1/chat/completions` (streaming + non-streaming;
   `/v1/completions` optional later). `system` carries persona + session
   brief; user/assistant turns map onto the seven interaction contracts
   (request/question/command/assertion/correction/impossible/ambiguous —
   already data in `projection/contract.py`). **Protocol errors map to
   contract outcomes, never to a confused 200.** Local-only bind by
   default (privacy boundary, §F below).
2. **Session orchestrator — the "brainstem" (new; the real work).**
   The turn loop: `perceive` (select the port) → IR → classify (7
   contracts) → **policy** (answer-from-CODEX / attempt-via-planner / ask-
   a-clarifying-question / honest-no / accept-correction) →
   **grounded response composition** (meaning from the CODEX, fluent
   surface from the LLM; the split is provenance-marked so "what the
   infant actually knows" is distinguishable from "how it phrases
   things") → memory writes (WORKSPACE for the session, CODEX status
   transitions ONLY through the verification path).
3. **Memory & identity (mostly exists).** sqlite CODEX (provenance,
   validity intervals), WORKSPACE (lifetimes, dump/load — E3.7),
   SOURCE/ANALYSIS for teaching-material versioning. New: session
   lifecycle (boot → restore → lapse) as first-class operations; the
   teacher-correction flow at dialogue scale (correction = candidate
   assertion, `observer = teacher`, verified before `established` — the
   E1.3 pattern generalized).
4. **Mastery & curriculum (new; the big pedagogy layer).**
   - *Knowledge graph:* concepts with prerequisites, difficulty, domain,
     and band (pre-K, K-5, 6-8, 9-12, college-1). The graph is store data
     (CODEX terms + relations) — curriculum changes are data edits with
     provenance, not code changes (the P11 discipline applied to
     schooling).
   - *Mastery state per concept:* `unexposed → exposed → practicing →
     stable`, with transitions requiring **experiment-grade evidence**
     (a correct plan/proof/query the stack can verify) — never
     self-report. "It learned fractions" must mean *the CODEX can
     produce the evidence*.
   - *Sequencer:* next-unit policy = prerequisites stable ∧ highest
     learning value; the projected planner's bounded-search machinery is
     reused, capabilities swapped for teaching moves.
   - *Recall & decay:* a spaced re-exposure queue for stable-but-stale
     concepts (the lifetime enum + `lapse` are the operational substrate;
     forgetting is a first-class, logged event, not data loss).
5. **The un-attended loop (new; scheduled, not daemons).**
   - *Authoring arm* (LLM): picks the sequencer's next unit, authors the
     drill dialogue, drives it through the OpenAI façade — it is just
     another OpenAI client, which is the whole point of the protocol
     choice.
   - *Analysis arm* (LLM): consumes **machine-readable session reports**
     (CODEX diffs, mastery transitions, honest-gap events
     `needs_info/impossible/ambiguous`, failed verifications) and emits
     a diagnosis: learned / stalled / proposed curricular fix. This is
     tractable because the harness + CODEX already emit exactly this
     report discipline (Phase-3 synergy).
   - *Attention inbox:* the loop **pauses and files an OpenProject
     ticket** when it meets an unresolvable contradiction, repeated
     mastery regression, or when an LLM arm proposes a curriculum change.
     Owner approval gates the change. "Mostly un-attended" means the
     human lives at the board — the way this project already runs.

## What exists vs. what is new (honest scorecard)

| Layer | Exists & proven | New build |
|---|---|---|
| Protocol | — | façade (small) |
| Dialogue | 7 contracts (data); LLMKernel single-shot parse (E3.1) | brainstem turn policy + grounded composition (large) |
| Memory | sqlite CODEX, WORKSPACE, SOURCE/ANALYSIS, restart (E2.3), promotion (E3.7) | session lifecycle glue; corrections at scale (medium) |
| Pedagogy | — | knowledge graph, mastery, sequence, decay (large) |
| Loop | harness JSON report discipline | authoring + analysis arms, attention inbox (medium) |
| Delivery | — | WebAX integration (placeholder until the tech lands) |

## Open questions (to confirm with the owner as WebAX arrives)

1. **Brain-as-server, browser-as-client?** Working assumption: the brain
   is a resident local server (our Python stack behind the OpenAI
   protocol); WebAX supplies the polished in-browser client shell. If
   WebAX's standardized techniques instead mandate **in-browser
   compute**, the fallback is a Pyodide/wasm port of the pure-Python
   core — plausible (the CODEX/IR/harness are dependency-light by
   design) but a real port; decide when the tech is visible.
2. **LLM placement:** authoring/analysis arms on LAN Ollama-class models,
   or cloud? Privacy boundary (§below) holds either way, but cost/quality
   of the *analysis* arm argues for the strongest model available.
3. **"College" scope:** proposed reading — the college band is a
   **capstone** (a #149-class robustness exam + a cross-domain
   synthesis project), not a full degree. Confirm.
4. **Curriculum width:** the system proves teachability on **narrow
   strips first** (grade-1 arithmetic + one domain per band) before
   widening. The pilot milestone gates the sweep — same discipline as
   Phase 1 → 2 → 3.

## Non-goals (until the horizon says otherwise)

- A general chatbot wrapped around an LLM — the LLM is a *tool arm*; the
  identity and knowledge are the CODEX's.
- Multi-user / cloud deployment / child-facing safety beyond local
  boundaries — until WebAX delivery actually ships a public surface.
- Real-time voice. Text-first is the protocol face.

## Suggested milestones (undated — the epic carries them when scheduled)

- **M1 — Attended pilot:** 20 grade-1 arithmetic sessions with a real
  OpenAI client; a human (the owner) is the teacher; mastery strip ends
  `stable` with verified evidence. *Buys: proof that the substrate is
  teachable in the open-ended regime everything else so far has not
  entered.*
- **M2 — Un-attended week:** authoring + analysis arms run a narrow strip
  for 7 days; the attention inbox pings at least once on a real weakness;
  the loop's own proposed fix, once approved, measurably moves mastery.
- **M3 — Band sweep:** K-5 across three domains with promotion gates
  (band-end experiment suites are the "promotions").
- **M4 — WebAX browser client** (owner's tech; brain unchanged).

## Standing rules the toy inherits (non-negotiable)

1. Never fabricate: unknown → honest `needs_info`/`impossible`/`ambiguous`
   (E3.6/#149 discipline). 2. Provenance on every durable fact (A8) — a
   teaching session is a SOURCE, a lesson is an ANALYSIS. 3. Contradiction
   is reconciled into structure, never averaged (A5). 4. Status changes
   only through verification (E3.7 promotion rule generalizes: the
   teacher is a high-authority observer, not an absolute one). 5. Forgetting
   is logged, decay is scheduled.

## Status (2026-08-21, session 17)

**E6.1 "the attended pilot" is BUILT and OFFICIAL PASS 8/8** (registry
`e6.1`, commit `79cb5bd` pin; `plan/30-phases/phase-6-tutor/`). The two
large new builds named above now exist:

- **Brainstem (layer 2, #152 DONE):** the turn loop
  `perceive → classify (all 7 contracts) → policy → grounded response →
  memory writes`. Policies: answer-from-store (successor chaining with a
  per-step provenance cite), accept-lesson (candidate → verified),
  accept-correction (both sides retained, closed, linked), honest
  `needs_info`/`impossible`/`ambiguous`. The LLM surface runs the E3.1
  SKIP semantics: no backend → deterministic arm; backend present →
  confirm-mode classification (D-e6b) + phrasing (surface only —
  `content_from = "codeX"` always).
- **Session runtime (layer 3, #153 DONE):** boot → restore → lapse over
  the persistent CODEX (byte-stable dumps; forgetting logged); strictly
  sequential sessions; correction flow at dialogue scale.
- **Mastery/curriculum (layer 4, #154 DONE):** the concept graph as
  store data (P11), the `unexposed→exposed→practicing→stable` machine as
  a pure recompute (K=4 evidence bar, prereq gate, conflict block), and
  the sequencer + spaced re-exposure queue (pure recompute too;
  `REEXPOSE_INTERVAL = 3`).

Pilot evidence (frozen pre-registration → control → official, all
reproduced exactly): 30 scripted turns over 4 sessions; both concepts
`stable` with 11 replayable proof chains; zero fabricated values (the
honest no carries an absence audit that the check re-audits); both
correction pairs kept/closed/linked with zero open disputes; the
restart preserves answers bit-equal; 100% contract-valid turns; 100%
provenance-complete store; byte-identical re-execution. Flagship
deviation **D-e6c**: the control run caught an amnesia bug (a
correction had created a second established claimant, so the derivation
guard honestly "forgot" the fact) — fixed pre-freeze as the
**single-current-claimant invariant** (corroboration/correction
re-establish, never duplicate), with a store-wide audit in C4.

**Remaining to full M1:** the OpenAI-protocol façade (#151) so a real
OpenAI client (or the owner, as teacher) can drive the pilot; the M1
text's "20 sessions with a real client" is then a demo, not a build.
T5 (un-attended loop) is where the LLM authoring/analysis arms take the
sequencer and the session reports. T9 (WebAX) awaits owner tech.

## Status (2026-08-21, session 17b — supersedes the session-17 block above)

- **T1 #151 OpenAI-protocol façade: DONE** (`src/kainos/tutor/facade.py`
  + CLI `kainos tutor serve`): `/v1/models`, `/v1/chat/completions`
  (stream + non-stream), `/v1/sessions/lapse`; local-only bind; OpenAI
  error envelopes; the CODEX is the student (client history is protocol
  compliance only). LIVE transcript: teach over HTTP → honest gap on an
  out-of-strip sum → lapse → reboot → same answers (learning
  persisted). #151 closed under delegation. **The owner's stop
  condition ("interacted with like an LLM that can learn") is
  demonstrated**, and his success-criteria note is recorded in the
  roadmap: a relatively simple LLM handling language processing and
  possibly memory/learning supervision would still count as a vast
  success — the learning body (CODEX + deterministic grounded policy +
  mastery) already stands alone on the det arm.
- **E6.2 "curriculum expansion to the edge of grasp": BUILT + OFFICIAL
  `PASS e6.2: 1.0` (8/8)** (pinned pre-work HEAD `033cd45`). The
  infant CONTINUES from the e6.1 store (S5..S9; id-level continuity
  proven): taught via rule-facts — subtraction (walk-back),
  multiplication (composed repeated addition), comparison (walking) —
  and the S9 LIMIT PROBE (owner-directed, D-e6f: "first don't give it
  square roots — let's see how far subtraction and multiplication can
  go") pins the answer: **the composition operations are exactly
  line-bound** — all 10 boundary-maximal in-line cases derive with
  citations (incl. 10\*7=70 landing exactly on the line end) and the
  5 first out-of-line cases stop with distinct honest articulations
  (walk-off / beyond-line / line-end); no value beyond the line exists
  in the store. Final: 220 assertions, 6/6 concepts stable, 135
  contract-valid turns, byte-identical re-execution. Verdict:
  `plan/30-phases/phase-6-tutor/results.md` (E6.2 section).
- **Deferred (owner-directed, D-e6f):** the sqrt / lattice-wall rung
  (exact irrationals not on the successor lattice; the grounded
  bracket as honest boundary) — reserved as its own future experiment;
  machinery dormant in the brainstem, unregistered in the curriculum.
- **Back-burner (owner-queued 2026-08-21, roadmap "Fourth horizon"):**
  Montessori-style multi-modal presentations (scissors: word + image +
  action; rides the E3.4 ports' SKIP semantics when vision is built);
  pedagogy backed by scientific growth-curve data (the harness as
  instrument: one frozen two-arm experiment per method); tools as
  calibrated observers (the "calculator" — speed, not understanding;
  queued after T5).
- **Remaining for full M1:** the façade demo is done; M1's "20 sessions
  with a real client" is now a DEMO, not a build. **NEXT: T5 #155
  (the un-attended loop)** — the LLM authoring arm drives the
  sequencer, the analysis arm reads the machine-readable session
  reports, and attention events flow to the OpenProject inbox (#156
  guardrails). Then T6 #166 (the multi-agent LLM-surface arm) rides the
  same brainstem seam. T7/T8 (curriculum map / persona) fold into the
  T5 pass. T9 (WebAX) awaits owner tech.

## Status (2026-08-21, session 17c — supersedes 17b for T5 only)

- **T5 #155 "the un-attended loop" (M2): BUILT + OFFICIAL `PASS
  e6.3: 1.0` (7/7)** (pinned pre-work HEAD `1e9fa84`, hermetic, no
  Ollama). `src/kainos/tutor/loop.py`: the authoring arm (det; LLM
  typed seam with E3.1 SKIP semantics + bounded retry), the
  analysis arm (reads the machine-readable session reports; ONE
  frozen fix class: re-expose), the attention inbox (frozen
  triggers file deduped ticket payloads; hermetic never posts).
  Official run: 97 turns over 3 sessions, converged at S3 (all six
  concepts stable, line exactly at the E6.2 cap 70), run2
  byte-identical, loop-report sha equal to the frozen control, 0
  disputes / 0 honest gaps / 0 tickets. Verdict:
  `plan/30-phases/phase-6-tutor/results.md` §E6.3; deviations
  D-e6g (strip-exposure policy fix) + D-e6h (stall trigger
  refinement), both pre-build.
- **Live LLM addendum** (Ollama 27B through the typed seams):
  transcript at `results/phase-6/e6.3-live/` — the seam works
  end-to-end; the local model's real weakness (it loops `after 0
  comes 1`, no state tracking) is AUDITABLE in the run, with no
  fabricated progress and no spurious triggers. Trigger machinery
  (dispute / stall / out-of-allowlist → ticket payloads; `op wp
  create` posting wired) is unit-proven; no live trigger fired in
  the 2-session run, so the live POST did not execute — reported as
  such. Backlog note (future trigger, not a #155 scope change): an
  "author made no progress" condition is not in the frozen trigger
  set.
- **#155 closed under delegation (100%); #150 at 75%.**
- **NEXT:** E6.4 phrasology (the sketch is registered; pre-register
  before build — this is the direct cure for the observed LLM-author
  weakness class: the infant will LEARN the phrasings a real model
  actually uses), then T6 #166 (the multi-agent LLM-surface arm on
  the same seam) and the M3 band sweep when the owner wants width.

## Status (2026-08-21, session 17d — supersedes 17c for E6.4)

- **E6.4 "phrasology — learning to parse in its own way": BUILT +
  OFFICIAL `PASS e6.4: 1.0` (8/8)** (pinned pre-work HEAD
  `942d2e2`, hermetic, no Ollama). Phrasings are STORE FACTS
  (relation `phrasing-map`): taught by the frozen lesson form
  `the phrasing "<NEW>" is the same as "<CANONICAL>"`, applied only
  where the frozen grammar honestly says ambiguous (grammar first;
  the lexicon EXTENDS, never overrides), `parse_source` marks the
  winner (no contract change — required-field whitelists), and a
  wrong mapping is corrected through the existing
  single-current-claimant pair (the superseded fact is kept,
  `obsolete`, validity ended, linked). 42 turns on the official
  e6.3 S3 seed (182/182 id-continuous): 7 phrasing facts (6
  established, 1 superseded), 7 byte-equal twin pairs (parse ≠
  content), 5 honest "teach me the mapping" unknowns, the
  line-end stop THROUGH a learned phrasing (S3:08), the equality
  case through the corrected cmp phrasing (S4:11), line end 72,
  245 final assertions, run1 ≡ run2. Verdict:
  `results.md` §E6.4; deviations D-e6i (the mechanism) + D-e6j
  (slot-map semantics: the placeholder NAMES are the map; the
  canonical lesson is recorded as `after {a} comes {b}`).
- **Live LLM addendum** (qwen-test 27B as the teacher's voice;
  `results/phase-6/e6.4-live/`): 4/5 model lines spoke WORD numbers
  → honestly ambiguous (the model's own surface is the intake wall's
  first measured breadth gap); 1/5 digit line was captured
  first-fit on the WRONG family, parsed, corrected, re-parsed —
  the S2:14/16 wrong-mapping story happening verbatim on a
  model-generated line.
- **#150 at 80% (T1–T5 + the surface strip done; T6 #166 + the M3
  band sweep + the lattice wall remain).**
- **NEXT:** T6 #166 (the multi-agent LLM-surface arm riding the
  same brainstem seam — E3.1 SKIP semantics already proven in the
  e6.1 C8 / e6.3 L6 checks), then the M3 band sweep (multi-domain
  K-5 width) and the lattice-wall experiment (the deferred
  sqrt-bracket rung) when the owner wants width.
