# Phase 6 (tutor) — E6.1 verdict

**Date:** 2026-08-21 (session 17) · **Official run:** Docker, hermetic,
no Ollama, `KAINOS_GIT_COMMIT=79cb5bd` (pre-work HEAD per house pattern)
· **Verdict: `PASS e6.1: 1.0` (8/8)** — reproduced byte-identically on
re-execution (C7; re-run after the sequencer added → same sha256).

## The claim, in one sentence

A system whose knowledge is a provenance-mandatory CODEX is
**teachable in the open-ended regime**: across four attended sessions of
a narrow pre-K/grade-1 strip it reaches stable mastery of both concepts
with replayable evidence, answers out-of-strip probes with the honest
`needs_info` (zero fabricated values), keeps every correction pair
(retained, closed, linked — never averaged), survives a restart with
bit-equal answers, and does all of it with 100% contract-valid turns,
100% provenance-complete store, and byte-identical re-execution.

## What each check bought (official values = frozen derived constants)

| check | what it proves | official value |
|---|---|---|
| C1 | all 30 turns validate against the verbatim 7-contract set | 30/30, 0 violations |
| C2 | learning: the frozen trajectory + 11 proof chains replayed offline | count-successor stable from S1; add-within-10 unexposed→stable at S2; 0 dangling cites |
| C3 | no fabrication: the honest no carries an absence audit that the check re-audits against the S3 snapshot | 3/3 probes `needs_info` |
| C4 | correction discipline + the **single-current-claimant invariant** (D-e6c) | both pairs kept/closed/linked; 0 open disputes; 0 duplicate claimants store-wide |
| C5 | persistence: S2-taught drills re-asked after the restart | 2/2 bit-equal (answers + traces); S3 booted restored over an EMPTY workspace |
| C6 | provenance completeness of the 45-assertion final store | 100%; 0 unbacked grounded cites |
| C7 | determinism & hygiene | run1≡run2 byte-identical (8 files); attention = exactly {S04:03}; 0 fallbacks, 0 fabrications |
| C8 | the surface arm: official = det (SKIP semantics); MockBackend seam | confirm-used / disagreement-falls-back / phrase-fallback, IRs identical across arms (6 llm events, 2 recorded fallbacks) |

## What is NOT claimed

- Not an open-ended curriculum: 2 concepts, one band-pair, a scripted
  teacher (the un-attended LLM authoring arm is T5/M2). The strip is
  narrow by design — the pilot gates the sweep.
- No claim the LLM arm improves pedagogy: the official run is the
  deterministic arm; the LLM seam is proven VALID (confirm/fallback/
  grounded phrasing), not evaluated for teaching quality.
- No transfer claim: `7+8 = needs_info` IS the honesty (the strip edge
  is respected, not apologized for). Stable is a per-strip evidence
  bar (K=4), not a general arithmetic theorem.
- The pilot's store is the in-memory CODEX behind a byte-stable JSON
  dump (the session runtime is store-agnostic; SQLite-backed persistence
  rides the exchange codec's proven parity — a drop-in, not a pilot
  blocker). Multimodal intake (E3.4 ports) is not wired into the pilot:
  the M1 gate is the text protocol.
- `e6.1` is the hermetic pilot CORE of M1. Full M1 adds a real
  OpenAI client driving the strip — #151 (the façade) is the build that
  closes that distance; no new experiment is needed for it (the M1 demo
  rides e6.1's evidence + the façade's unit tests).

## Deviations (see the pre-registration for the full table)

- **D-e6a** — pre-registration arithmetic fix (30 turns, not 27; S3
  persistence probes corrected to drills S2 actually taught). No design
  change; the verbatim script is authoritative.
- **D-e6b** — LLM classification tightened to CONFIRM mode (no rescue
  of unparseable text — the fabrication vector). No threshold change.
- **D-e6c** — **flagship: the control run caught an amnesia bug
  pre-freeze.** A correction had created a second established claimant
  for the same value; with two active established facts per subject,
  the grounded derivation guard (`len(acts) != 1`) honestly answered
  `needs_info` — the infant "forgot" a fact it had just re-established,
  and C5 persistence failed. Fixed as the **single-current-claimant
  invariant**: corroboration/correction RE-ESTABLISH the existing
  claimant (evidence += turn, re-verified); a different value is
  created and disputed, never overwritten; closed claimants stay
  `obsolete` with their validity interval. The correction now
  VINDICATES the original fact (it becomes the pair's replacement side —
  see the C4 pair ids). A store-wide duplicate-claimant audit was added
  to C4. No check weakened — the frozen C4 semantics are unchanged, and
  a pre-registered check caught a fabrication-adjacent bug before the
  freeze, exactly as the harness exists to do.
- **D-e6d** (scope note, not an experiment deviation) — the spec's
  layer-3/layer-4 text names "sqlite CODEX", a "planner" reuse, and a
  multimodal port: the pilot uses the in-memory store + JSON dump
  (store-agnostic runtime; SQLite parity is proven by the exchange
  codec), a grounded fact-chain solver (replayable-proof discipline,
  E3.6's, but the tutor's "plan" is an arithmetic-fact chain, not a
  capability plan — the E3.6 planner is not the right machinery), and
  the text port only. Recorded so the spec→build mapping is honest.

## Artifacts

- Build: `src/kainos/tutor/{__init__,mastery,brainstem,session,sequencer,bench}.py`;
  tests `tests/tutor/` (55 tests: mastery, brainstem, session,
  sequencer, e6.1 bench-pinned).
- Pre-registration (frozen before the official run, derived constants
  frozen pre-freeze): `plan/30-phases/phase-6-tutor/experiments.md`.
- Official: `results/e6.1.{json,md}`, `results/phase-6/SUMMARY.md`,
  `results/phase-6/e6.1-run1/{codeX,session}-S01..04.json`,
  `results/phase-6/e6.1-run2/…` (the byte-identity control).
- Registry: `e6.1` in `SRC/kainos/harness/runner.py` (24 experiments).

---

# E6.2 — "Curriculum expansion to the edge of grasp"

## Verdict

**E6.2 is BUILT and OFFICIAL: `PASS e6.2: 1.0` (8/8)**, hermetic Docker
run pinned to the pre-work HEAD `033cd45` (the façade commit),
`KAINOS_RESULTS_DIR` unset, no Ollama — 135 turns (the 30-turn e6.1
replay, continuing that store, + the 105-turn ladder S5..S9),
byte-identical re-execution, and id-level continuity with the official
e6.1 S4 store (every official assertion reproduced; the only S4
additions are the four new curriculum rows).

## What is claimed (the one-liner)

A CODEX infant, continued from the e6.1 store without reset, learns a
new concept EXACTLY when its rule enters the store (subtraction by
walk-back, multiplication by composed repeated addition, comparison by
walking) and reaches EXACTLY as far as its number line does: all 10
boundary-maximal in-line derivations (70-1, 70-35, 69-68, 55-27,
70-70=0, 8*8=64, 9*7=63, **10*7=70 landing exactly on the line end**,
1*9, 0*5) derive with citations, the 5 first out-of-line instances stop
at the boundary with distinct honest articulations (walk-off /
beyond-line / line-end, each re-audited against the snapshot), no value
beyond the line exists anywhere in the store, and the whole run is
contract-valid, offline-replay-verified, dispute-audited, and
deterministic.

## What was measured (official values, matching the frozen pre-registration)

| check | official value | pass |
|---|---|---|
| C1 contract validity | 135/135 turns valid | ✓ |
| C2 trajectory + replay | 6 concepts per the frozen table; 30 ladder derivation-correct events; 0 replay violations | ✓ |
| C3 A/B arc | 3/3 pairs flip (S6:01→03, S7:31→35, S8:21→23); the "3 * 4" gap names multiplication before, derives 12 after | ✓ |
| C4 honesty at edges | 5/5 frozen edges with correct mode audits + articulations; line end 70 in the S9 snapshot | ✓ |
| C5 data-driven activation | exactly 3 policy facts; counterfactual removal flips the drill back to the honest gap | ✓ |
| C6 disputes + attention | both pairs kept/closed/linked (vindicated originals); 0 disputes, 0 duplicate claimants; attention = {S04:03, S05:15, S07:33} | ✓ |
| C7 determinism + continuity | 18/18 files byte-identical; e6.1 S4 store reproduced id-for-id; 0 fabrication events | ✓ |
| C8 the stopping point | 10/10 boundary-maximal derivations; honest-stop set exactly the frozen 5; store line end 70 | ✓ |

Per-session: S01 14 turns (36 total) → S05 16 (80) → S06 9 (89) →
S07 39 (159) → S08 27 (206) → S09 14 (**220 final assertions**).
Ladder script hash `fef771e00e5ed982`; full 135-turn hash
`0ae3d802e7ccb4c7`.

## The stopping point (the wall, as the owner defined it)

"Where it can't grasp a new concept" — the ladder answers that
precisely: the composition operations are not "unable" at arbitrary
points; they are **exactly line-bound**. Every instance on the line
derives (with citations) and the first instance beyond the line stops
with the correct, mode-specific articulation — walking back past 0
leaves the line; starting beyond the line end is out of reach
("i don't even have 100 to start from"); a repeated addition that
crosses the line end does not finish. Pushing further extends the LINE
by lessons (pedagogy: S05/S07/S08 extended it 20→50→70); the boundary
semantics — the grasp — held across all three extensions without
revision. The next conceptual wall beyond the line (the deferred sqrt
rung: exact irrationals not on the successor lattice, the grounded
bracket as honest boundary) is reserved for the lattice-wall
experiment (D-e6f).

## What is NOT claimed

- Not that the infant "computes fast": it derives by chained cited
  facts (10*7=70 is 70 cited successor steps — slow, exact,
  replayable). The calculator/tools horizon (owner-noted) is about
  speed and enters as a calibrated observer, queued after T5.
- Not a breadth sweep (M3 is the multi-domain K-5 sweep); this is one
  domain's depth ladder on one band pair.
- Not an LLM result: the official run is the det arm (no backend); the
  LLM remains the confirm/surface seam (D-e6b) and (per the owner's
  success criteria note) the future simple-LLM language/supervision
  layer — the learning body stands alone.

## Deviations (full text in experiments.md)

- **D-e6a/b** inherited from the E6.1 pre-registration (script is
  authoritative; LLM classification confirm-only).
- **D-e6e** (pre-build references): C3's impossible-arc reference
  corrected (the e6.1 script has no multiplication probe — the arc is
  S7:31→S7:35 within the ladder); the attention freeze corrected for
  the CONTINUED conflict history (the e6.1 replay carries episodes
  S2:04/S4:03, so run attention is {S04:03, S05:15, S7:33}).
- **D-e6f** (owner-directed, pre-freeze): the pre-registered S9 sqrt
  rung replaced by the 14-turn subtraction/multiplication LIMIT PROBE
  ("first don't give it square roots — let's see how far subtraction
  and multiplication can go"); the `sqrt-bracket` concept deferred with
  its rung to the lattice-wall experiment (machinery dormant in code);
  the subtraction failure split into walk-off vs beyond-line (frozen,
  separately audited); ladder 101→105 turns, run 131→135. No threshold
  loosened and nothing re-run to pass: the deviation is a scope change
  applied before any freeze, with the full pre-registration re-
  registered and re-controlled before the official run.

## Artifacts

- Build: `src/kainos/tutor/e62.py` (+ the brainstem sub boundary
  precision, the curriculum trim, the runner registration); tests
  `tests/tutor/test_e62.py` (19 tests: the extended grammar, rule
  lessons, the four gated policies, the A/B flips, the boundary
  honesty, add-strip routing, the full 135-turn bench pin).
- Official: `results/e6.2.{json,md}`, `results/phase-6/SUMMARY.md`
  (now covers e6.1 + e6.2), `results/phase-6/e6.2-run1/{codeX,
  session}-S01..09.json`, `results/phase-6/e6.2-run2/…`.
- Registry: `e6.2` in `src/kainos/harness/runner.py` (25 experiments).

---

# E6.3 — "The un-attended loop" (T5 #155, milestone M2)

## Verdict

**E6.3 is BUILT and OFFICIAL: `PASS e6.3: 1.0` (7/7)**, hermetic Docker
run pinned to the pre-work HEAD `1e9fa84`, `KAINOS_RESULTS_DIR`
unset, no Ollama — the loop runs the infant through N sessions with
NO human in the turn loop: a det authoring arm driving the frozen
sequencer, a det analysis arm acting only within one frozen fix
class, and the attention inbox filing deduped, unposted ticket
payloads on the frozen triggers. The run converges at the fixed
point — all six concepts stable, the number line exactly at the
E6.2 cap (70).

## What is claimed (the one-liner)

The M1/E6.2 infant runs un-attended and stays honest: every one of
the 97 issued lines is replay-verified to be exactly the decision
the frozen policy makes at that store state (the author invents
nothing), every diagnosis is recomputable from the machine-readable
session reports, the run is byte-identical across re-executions,
the line cap (70) is a property of the FINAL STORE (not just of the
author), zero honest-gap turns (the grounded author creates none),
zero disputes, zero tickets — and the loop stops at session 3,
where all six concepts are stable and the line has reached its
frozen horizon.

## What was measured (official values, matching the frozen pre-registration)

| check | official value | pass |
|---|---|---|
| L1 loop contract | 97/97 turns contract-valid; 3 session reports machine-complete | ✓ |
| L2 author authority | full-session replay: 97/97 lines == the frozen policy's decision at the pre-state (S1: 40 line lessons; S2: 30 line lessons + 4 successor drills + 2 strip exposures + 2 rule lessons; S3: 16 drills + 1 rule lesson) | ✓ |
| L3 learning dynamics | trajectory == control table; converged at session 3; final store 182, line end 70 | ✓ |
| L4 analysis audit | 0 applied fixes (none due); mastery monotone across sessions | ✓ |
| L5 attention inbox | trigger set == frozen []; payloads deduped; `posted: []` (hermetic never posts) | ✓ |
| L6 arm seam | official arm = det; `llm_arm: skipped-no-backend`; typed seams present | ✓ |
| L7 determinism + wall | run1 ≡ run2 (7/7 files byte-identical); 0 values beyond the cap; 0 disputes; loop-report sha `9339b7e25ce0c46b` == control | ✓ |

## The live LLM addendum (recorded, not part of the official value)

A small live run (Ollama `qwen-test:latest`, 27B Q8, temperature 0,
2 sessions × 12 turns, cap 16) drove the loop through the typed
LLM seams — transcript: `results/phase-6/e6.3-live/live-transcript.json`.
Findings, reported as observed:

- **The seam works end-to-end**: 24/24 model lines parsed into the
  frozen grammar, canonicalized, said, and audited; 0 drops in this
  run (the drop path is unit-proven: garbage is retried once, then
  dropped + logged — no rescue loops, E3.1).
- **The model's real weakness is visible, not hidden**: the local
  model repeats `after 0 comes 1` on every turn — it can produce the
  canonical form but cannot track loop state. The loop recorded
  exactly that: the line stayed at 1, no concept advanced, no
  fabricated progress, the LLM analysis arm correctly answered
  `answer=none` (nothing to re-expose), no triggers fired, nothing
  posted. A weak teacher is an AUDITABLE fact, not a silent failure.
- **M2's "inbox pings at least once" clause**: the trigger
  machinery — conflict from a wrong lesson (unit-proven: files the
  `dispute:` payload), unfixable stall (unit-proven: files the
  `stalled:` payload after the second consecutive session) — is
  proven at unit level and wired to real ticket posting
  (`op wp create`, delegation); no trigger fired in the two-session
  live run, so the live POST path did not execute. Reported as:
  mechanism proven, live exercise pending a longer/weaker run.
- **Backlog note (future loop, not part of #155's frozen scope):**
  the frozen trigger set (dispute / stall / out-of-allowlist) does
  not include an "author made no progress" condition — the observed
  live repetition is not a trigger. If the live regime wants to
  ping on that, it is a future registered trigger, not a backport.

## What is NOT claimed

- Not 7 calendar days (M1 text's "un-attended week"): the loop is a
  scheduled function, not a daemon — the compressed N-session run is
  what the experiment measures; the calendar is a deployment shape
  and is said as such.
- Not the LLM arms' official result: the official value is the det
  arm (house rule: official runs are hermetic, no Ollama). The live
  addendum above is the LLM evidence, labelled as such.
- Not curriculum invention or multi-agent teaching: the loop drives
  the six registered concepts; widening the map is M3.
- Not "it teaches itself": the teacher is the deterministic frozen
  policy here (LLM when configured); what the loop proves is that
  NO human is needed in the turn loop while every learning event
  stays store-auditable.

## Deviations (full text in experiments.md §E6.3)

- **D-e6g** (pre-build, policy fix): author rule 2 as first
  registered left the addition strips unexposed forever (the
  sequencer proposes only exposed-or-better; the strips have no
  lesson) — a guaranteed non-convergence at the line cap, caught in
  design review against `sequencer.due_concepts` before any loop
  code existed; rule 2 now explicitly exposes the first ready
  unexposed concept (frozen lesson, else the sequencer's first
  grounded drill).
- **D-e6h** (pre-build, trigger refinement): the stall trigger as
  first registered assumed a fix exists; a stall with no grounded
  drill (e.g. an unlearned capability probed by the LLM arm) is
  precisely the spec's unresolvable case — the trigger is the
  second-consecutive-stalled session, with or without an applied
  fix. The det run's frozen trigger set is unchanged (it can never
  produce a stall).

## Artifacts

- Build: `src/kainos/tutor/loop.py` (+ runner registration → 26
  experiments); tests `tests/tutor/test_e63.py` (9 tests: the
  author policy, the canonical forms, the deterministic-LLM-seam
  byte-identity, the bounded-retry drops, the wrong-lesson dispute
  ticket, the unfixable-stall persist trigger, the ticket payload
  shape, the full-run pins, the experiment class).
- Frozen constants: `results/phase-6/e6.3-derived.json` (the
  machine reference; the pre-registration carries the human-readable
  copy).
- Official: `results/e6.3.{json,md}`, `results/phase-6/SUMMARY.md`
  (now covers e6.1 + e6.2 + e6.3),
  `results/phase-6/e6.3-run{1,2}/{codeX,session}-S01..03.json` +
  `loop-report.json` (byte-identical across runs).
- Live addendum: `results/phase-6/e6.3-live/live-transcript.json`.

---

# E6.4 — "Phrasology: learning to parse in its own way" (T-tutor surface strip; owner-proposed)

## Verdict

**E6.4 is BUILT and OFFICIAL: `PASS e6.4: 1.0` (8/8)**, hermetic
Docker gate (ruff + mypy 96 files + 785 passed / 2 skipped), and an
official run pinned to the pre-work HEAD `942d2e2`
(`KAINOS_RESULTS_DIR` unset, no Ollama). The infant's INTAKE became
a curriculum strip: phrasings are STORE FACTS (relation
`phrasing-map`), taught by their frozen lesson form, applied only
where the frozen grammar honestly says ambiguous, byte-comparable in
content to their canonical twins, and corrected through the
already-proven single-current-claimant machinery.

## What is claimed (the one-liner)

The infant's intake boundary is exactly its lexicon: every taught
phrasing family parses (and composes with the grounded layer —
including the line-end stop THROUGH a learned phrasing), every
untaught phrasing stays an honestly named ambiguity ("teach me the
mapping"), parse ≠ content (a learned parse's IR is byte-equal to
its canonical twin except `parse_source`), and extending the intake
is TEACHING — a store fact with provenance — not code change, not
grammar drift.

## What was measured (official values, matching the frozen pre-registration)

| item | official value |
|---|---|
| script | 42 turns (S2=18, S3=13, S4=11), `script_hash 03f00f1f04a9e040` |
| seed continuity | 182/182 id-for-id from the official e6.3 S3 store; 0 additions/losses |
| A/B arc | S2:01 ambiguous → S2:04 = 13 (learned sum); S2:02 → S2:08 = 12 (learned succ); S2:13 → S2:17 (cmp, post-correction) |
| wrong-mapping arc | S2:14 teaches WRONG (valid mapping, wrong semantics); S2:15 = **8** (a subtraction answer, plausible for the wrong contract); S2:16 corrects; S2:17 = "yes — 17 is 8 steps beyond 9" |
| parse ≠ content | 7 frozen twin pairs byte-equal beyond `parse_source` (+ the documented `turn:` provenance marker); response texts byte-equal |
| fact audit | 7 phrasing facts: 6 established, 1 superseded (kept, `obsolete`, validity ended, links its replacement), 0 open disputes, 0 duplicate claimants |
| honest unknowns | 5 ambiguous turns (S2:01, S2:02, S2:13, S3:09, S4:09), the frozen "teach me the mapping" articulation, zero store writes |
| composition | S3:08 "take 3 away from 100" THROUGH the learned sub phrasing → honest line-end stop; S3:05 line 70→71, S3:11 the successor at the new end, S4:06 line 71→72, S4:11 the equality case "neither — 7 is 7" |
| phrasology mastery | `stable`, 17 applications (K=4), 24 events, 0 unresolved conflicts |
| final store | 245 assertions, line end exactly **72**, 0 fabrication, all 42 turns det arm |
| determinism | 8 files per run dir, run1 ≡ run2 byte-identical (`fixed_epoch` clock) |

## The live LLM addendum (recorded, not part of the official value)

A real model (qwen-test:latest, 27B Q8, native `/api/chat`
`think:false`) proposed five teacher phrasings in its own words;
each went to the E6.4 infant (seeded from the official e6.3 S3
store) as-is. Findings, transcript verbatim at
`results/phase-6/e6.4-live/live-transcript.json`:

- 4/5 lines used WORD numbers ("two", "three", "one") — outside
  the frozen slot class (numeric slots). The infant stopped
  honestly with the frozen phrasing-gap articulation, every time.
  The model's own surface is the first measured wall of the intake
  strip: as the grammar speaks DIGITS, the model speaks WORDS.
- 1/5 line ("If you had 2 apples and got 2 more, how many would
  you have?") carried digits → templated → the first-fit rule
  captured it on ADD (the first canonical family whose slot names
  match) → it parsed (4) → the family-targeted correction flipped
  the mapping to MUL → it parsed (4 — 2+2 = 2·2, the values
  coincide; the mapping switched, the old one closed and linked).
  The S2:14/16 story (valid mapping, wrong contract, corrected by
  the single-current-claimant pair) happened VERBATIM on a
  model-generated line, live.
- Environment note: the owner's Ollama proxy intermittently
  rejected the project client's `format`/`options` fields
  (HTTP-200 error documents); the addendum therefore used the
  native wire call (the client's own request minus those two
  fields). Recorded, not hidden.

## What is NOT claimed

- Not a free-form NL parser: learned phrasings are slot-filling
  templates over the numeric grammar (the frozen placeholder
  class); the live addendum shows a real model speaking words —
  that breadth is future CURRICULUM on this mechanism.
- Not an LLM result: the official value is the det arm (house
  rule). The LLM is the teacher's VOICE in the addendum; the
  infant itself never calls a model.
- Not a content claim: E6.2's wall (the WHAT-it-can-know boundary,
  line end 70 in the seed, extended here only by taught lessons to
  72) stands untouched; E6.4 changes HOW it receives.
- The wrong-mapping episode is scripted (S2:14/16) in the
  official run; the live addendum adds the live instance.

## Deviations (full text in experiments.md §E6.4)

- **D-e6i**: the registered mechanism (M1–M8) — the sketch's six
  pillars became the concrete pre-freeze mechanism registration
  (teaching pattern + placement, canonical template vocabulary,
  the phrasing fact shape, the grammar-first lexicon consult, the
  `parse_source` field via whitelist semantics with NO contract
  change, the honest unknown articulation, the phrasology mastery
  concept, the seed/continuity shape).
- **D-e6j** (pre-freeze, caught in build review): the
  first-registered slot semantics (ordered positional bijection;
  the lesson recorded as `after {n} comes {m}`) is unworkable —
  the sub template `take {b} away from {a}` requires the names to
  carry meaning, and the canonical lesson's POLICY slots are
  named a/b. Refinement: the placeholder NAMES are the slot map
  (each new-template name names the canonical slot its surface
  position fills); the canonical lesson is recorded as
  `after {a} comes {b}` (surface unchanged). No check of any
  earlier experiment is touched; the grammar is unchanged.

## Artifacts

- Build: `src/kainos/tutor/e64.py` + the brainstem phrasology
  machinery (`TEACH_RE`, `CANON_TEMPLATES`, the lexicon consult,
  the teach/correction policies, `parse_source`, the
  unknown-phrasing articulation) (+ runner registration → 27
  experiments); tests `tests/tutor/test_e64.py` (8 tests: the
  teach→parse loop, the no-numbers teach line, invalid-mapping
  honesty, the unknown-then-parsed arc, the wrong-mapping
  correction pair, the lesson family, the full-run pins, the
  experiment class).
- Frozen constants: `results/phase-6/e6.4-derived.json` (+ the
  pre-registration's human-readable copy).
- Official: `results/e6.4.{json,md}`, `results/phase-6/SUMMARY.md`
  (now covers e6.1–e6.4),
  `results/phase-6/e6.4-run{1,2}/{codeX,session}-S0*.json` +
  `e6.4-report.json` (byte-identical across runs).
- Live addendum: `results/phase-6/e6.4-live/live-transcript.json`.

# E6.5 — "The K–5 Band: numerics ∥ geometry (band 1 of the M3 band sweep)"

`(T7 #157; the owner's 2026-08-22 directives, comment 450 — built
2026-08-22; pre-registered in experiments.md §E6.5 before code)`

## Verdict

`PASS e6.5: 1.0 (threshold 8/8)` — official run hermetic (no Ollama),
pinned pre-work HEAD `46e3416`. Band 1 of the M3 sweep is OFFICIAL:
**geometry learned CONCURRENTLY with math from K–5, on the same
teachable-strip seam, ending on a JOINT evaluation — and the band
VERIFIES: all four shape concepts stable (K = 4) against the
seed-stable numerics, the numeric line untouched (end 72), two runs
byte-identical.**

## What is claimed (the one-liner)

The K–5 band teaches two domains at once on ONE mechanism: shape
definitions are store data (the E6.2 rule-gated capability arc,
generalized to geometry — teach the definition, the drill unlocks;
probe before teaching and the gap is honestly named with the exact
canonical lesson to teach), shape question families join the
phrasology strip as vocabulary-slot templates (D-e6i generalized:
`{shape}` fills from the frozen band vocabulary, never a fixed word,
never a number — slot-type mismatches are honestly rejected), and
the band ends on one frozen probe set spanning BOTH domains with
every member deriving correctly — the joint map, not two silos.

## What was measured (official values, matching the frozen
pre-registration)

- **P1** 48 turns, every response contract-valid.
- **P2** the three pre-teach gaps honest (S02:02 triangle, S02:15
  rectangle, S03:01 circle — "not a capability i have been taught",
  zero store writes, zero grounds); the out-of-band pentagon
  (S02:07) honestly ambiguous; the per-session domain sequence
  equals the frozen interleave (S2 `NGGGGNBGGGGNGGGG` · S3
  `GGGGNGGGGNNBGN` · S4 `GGGGGGGGGGNNNNNNNG` — concurrency
  scripted, not emergent).
- **P3** the single-current-claimant arc: the wrong square lesson
  (4 sides / 3 corners, S02:08) answers "3" while active (S02:09 —
  E6.4's S02:15 pattern), the correction (S02:10) supersedes it
  (kept, obsolete, validity ended `2026-08-21T021000+00:00`, linked
  to `cap:shape-square:def:S02:10`), and the band ends with exactly
  one established claimant per shape matching the frozen table
  (triangle 3/3, square 4/4, rectangle 4/4, circle none/none); the
  phrasology sibling arc mirrors it (points-phrasing on the CORNERS
  family at the end, the sides-family mapping obsolete); **zero open
  disputes**.
- **P4** the shape phrasology works end-to-end: the edges phrasing
  is lexicon-parsed after its lesson, the seed phrasology still
  works THROUGH the band (S03:14, S04:16, S04:17), grammar-first
  holds on every canonical probe, and the cross-family mapping
  attempt (vocabulary slot → number family, S03:12) is honestly
  rejected with no store write. (Recorded honestly: the pre-S2:13
  edges probe carries a second cause of ambiguity — its shape is
  out-of-band — so the A/B's measured half is the post-lesson
  parse; the untaught surface wall is the S02:07 boundary probe.)
- **P5** every derived answer grounded; every shape drill cites
  exactly its claimant, and the answered value equals the cited
  claimant's STORED value (re-read from the store, circle's "none"
  included) — zero ungrounded answers in 48 turns.
- **P6** the numeric line end is **exactly 72** at the band end —
  the geometry strip wrote ZERO successor facts (one line, two
  domains, measured); all 245 seed ids present (id-for-id
  continuity with the official e6.4 store).
- **P7** the JOINT band-end set (S04): 3,3,4,4,4,4,none,none,4,4
  (shape drills over all 4 shapes + edges/points phrasings) ·
  needs_info at the line wall · 35,43,36,yes (the four numeric
  families) · assertion (corroborated seed phrasing) · 72 · none
  (phrasing + circle composition) — ONE check, both domains.
- **P8** mastery at the band end: shape-triangle **stable** (6
  correct) · shape-square **stable** (5) · shape-rectangle
  **stable** (4) · shape-circle **stable** (6); all six seed
  numerics remain stable; phrasology stable (24 correct); run1 ≡
  run2 byte-identical (8 files); all 48 turns det arm; final store
  **309** assertions.

## The live LLM addendum (recorded, not part of the official value)

Ran 2026-08-22 (9.5 s): `pi-qwen-fast:latest` generated 10
K–5-style teacher shape questions; each was parsed by the band
surface (the official e6.5 final store: det grammar + the 9
established phrasings). **As written: 10/10 landed in honest
ambiguity — the surface boundary held.** The diagnosis (per
question, in the addendum) is the first measured breadth gap for
the GEOMETRY strip: 2/10 parse with a casefold of the model's
sentence-initial capital; 4/10 with casefold + the demonstrative
substitution (`this/your` → `a`); the other 6/10 are genuinely
out-of-band (vision-style references — "point to…", "show me where
…" — the band surface is text-only in band 1). Model breadth is
data; the mechanism's honesty is the claim (E6.4 precedent: 4/5 of
the model's numeric phrasings were word numbers, honestly
ambiguous). Artifacts: `results/phase-6/e6.5-live/addendum.json`.

## What is NOT claimed

- That free-form or visual geometry language is handled (the band
  surface is four lesson forms + two drill families + the taught
  phrasings, text-only; demonstratives and pictures are out of
  band by design — the addendum measures exactly where they fall).
- That bands 2–5 are built: they are declared in the map
  (`tutor/bands.py`, `results/phase-6/bands-map.json`) per the
  owner's directive #2 — band 2 (6–8) algebra ∥ kinematics, band 3
  (9–12) geometry-advanced ∥ vectors/statics, band 4 calculus ∥
  mechanics, band 5 (college-1) statistics ∥ probabilistic
  physics — each `declared`, no mechanism, no probes, no claims
  this run.
- Anything about LLM competence in the official value (det arm;
  the addendum is labelled separately).
- That the K–5 shape vocabulary is complete (four shapes; the rest
  is the honest boundary — S02:07 is the standing measurement).

## Deviations (full text in experiments.md §E6.5)

- **D-e6k** — script correction PRE-OFFICIAL: registered S4:13
  ("78 - 25 is what?", expected 53) is not derivable on the seeded
  line (end 72) — the mechanism answered the honest wall one turn
  earlier than S4:11; replaced with "68 - 25 is what?" → 43. No
  threshold loosened; the wall itself is preserved and still
  probed.
- The frozen bookkeeping (per-shape correct counts 6/5/4/6) was
  fixed from the control — S03:07's triangle probe counts for the
  strip under the then-wrong sibling mapping (the derivation was
  grounded, so it is recorded), and S03:13 is the rectangle probe.

## Artifacts

- Pre-registration + deviations + frozen derived constants:
  `plan/30-phases/phase-6-tutor/experiments.md` (E6.5 section) +
  `results/phase-6/e6.5-derived.json`.
- Build: `src/kainos/tutor/bands.py` (the curriculum map, P11
  data), `src/kainos/tutor/brainstem.py` (the geometry strip:
  shape table + grammar, vocabulary-slot lexicon, claimant
  policies), `src/kainos/tutor/e65.py` (matrix + P1–P8 +
  experiment class); runner registration (`e6.5`; 29 experiments).
- Tests: `tests/tutor/test_e65.py` (16 tests: the mechanism);
  `tests/harness/test_runner.py` (registry count).
- Official: `results/e6.5.{json,md}` (pinned `46e3416`, script
  `97d1c38f79841deb`), `results/phase-6/e6.5-run{1,2}/` (byte-
  identical), `results/phase-6/bands-map.json` (the declared map +
  validation), SUMMARY regen (e6.1–e6.5).
- Live addendum: `results/phase-6/e6.5-live/addendum.json`.

# E6.6 — "Band 2: algebra ∥ kinematics (6–8, the first aligned band)"

`(T7 #157, the M3 band sweep, band 2; official 2026-08-22, pinned
`dcb897166`; pre-registered in experiments.md §E6.6 before code)`

## Verdict

**PASS e6.6: 8/8 (8/8).** The owner's directive #2 is mechanism:
algebra and kinematics learn as ONE aligned band on the same
teachable-strip seam — one solver, two doors (byte-equal line-step
citations through the algebra and kinematics doors, only the rule
fact differs), the alignment stored as prereq edges in the codex
(empty gaps at the band end, measured from the store), inexact
division and off-line probes are honest, the kin phrasing can never
be silently mis-mapped (name bijection), and the band ends on a
JOINT evaluation spanning both domains.

## What is claimed (the one-liner)

Band 2 (6–8): one- and two-step linear equations in x and
constant-velocity cart motion learn concurrently with the SAME
grounded line machinery, the algebra↔kinematics alignment is
STRUCTURAL (shared solver + stored prereq edges gating kinematics
stability on algebra stability), the numeric line is untouched
(end 72, zero new successor facts), all seven band-2 concepts are
`stable` (K = 4) with all eleven seed/band-1 concepts still
`stable`, the line wall composes into the aligned band (15·x = 120:
x = 8 in the math, off the line), and two runs are byte-identical.

## What was measured (official values, matching the frozen
derived constants EXACTLY)

- **P1** 48 turns (S2 = 16, S3 = 16, S4 = 16),
  all contracts valid, script hash `62322a8d360d8681`.
- **P2** honest pre-teach gaps (S02:01 algebra, S02:13 kinematics —
  the canonical lesson articulation, zero writes); the frozen
  per-session interleave holds: S2 `GAAANAAAHAAAGHNA` · S3
  `KKKKKKHKKKAKKKBK` · S4 `AKAAKKKKKKHAKAKN`.
- **P3** 25 derived inverses exact and grounded (walk-back /
  repeated taking / repeated addition, each citing its rule fact +
  the line steps): the frozen table (47, 29, 8, 6, 35, 72, 29, 9,
  8, 42, 6, 5, 35, 8, 6, 7, 7, 6, 7, 27, 24, 42, 6, 7, 8, 9, 5, …),
  and the inexact probe S02:09 (7·x = 20) honestly: "leaves 6 … not
  a whole number on my line."
- **P4** the wall composes: S02:14 + S04:11 (15·x = 120 →
  "my number line ends at 72") and S03:07 (position 92 off the
  line; the distance 32 FITS — the articulation says so) all honest
  needs_info citing nothing; the on-line maximals (45+27=72, 8·9=72
  twice, 72−45=27) still derive — the wall is a measured knee.
- **P5** the alignment literal: S02:11 (algebra door) ≡ S03:09
  (kinematics door) → 6 = 6, identical line-step citations, only
  `cap:alg-two-step:rule` vs `cap:kin-solve-time:rule` differs;
  the aligned prereq edges are STORED (established + active) in the
  final store; the final-store mastery view shows empty prereq gaps
  on all four kin concepts (their algebra counterparts stable
  first).
- **P6** the phrasing discipline: S03:15's wrong cross-family
  attempt (the leaving-phrasing → the TIME family, `t` vs `c`)
  honestly rejected on the slot-name bijection (zero writes);
  S03:16 establishes `phrasing:S03:16`; S04:02 byte-equal to its
  canonical twin S03:05 modulo parse_source (+ equal texts); S4:10
  parses via the learned phrasing (grounded 42); exactly one
  established kin phrasing in the final store; zero open disputes.
- **P7** the JOINT band-end set (16 probes, one check, both
  domains): 47, 29, 8, 6, 35, 72, 29, 9, 8, 42, needs_info (the
  reproducible wall), 6, 5, 35, 8, 14 — every member derived-
  correct or honest-exactly-frozen.
- **P8** mastery: the seven band-2 concepts all `stable` with the
  frozen correct counts (5/4/4/4/5/4/4) and EMPTY prereq gaps; the
  eleven seed/band-1 concepts remain `stable`; the line end is
  EXACTLY 72; 309/309 seed ids id-for-id; final store 375 = 309 +
  22 new facts (7 rule lessons + 1 kin phrasing + 7 curriculum
  facts + 7 prereq edges) + 44 mastery events; run1 ≡ run2 byte-
  identical (run identity `961c8d121eb2de12`); all det arm.
- **The bands map** (`results/phase-6/bands-map.json`): band-2 →
  `implemented` (evidence `e6.6`), bands 3–5 remain `declared`.

## The live LLM addendum (recorded, not part of the official value)

`pi-qwen-fast:latest` (native /api/chat, think:false) generated 10
6–8 grade questions (5 motion, 5 algebra) in 10.5 s → **10/10
landed in honest ambiguity** — the band-2 surface's first measured
breadth gap (band 1's shape strip: 5/10). Diagnosis: the model
writes WRITTEN MATH NOTATION (`3x = 12`, `x + 5 = 9`, two-
sentence word problems with units) while the frozen grammar is
single spoken-sentence forms; "What is x if x + 5 = 9?" would land
under casefold + punctuation + equals normalization — a recorded
surface-widen candidate, not built. Zero silent writes on the
official store.

## What is NOT claimed

- General algebra or physics (the 6–8 aligned core: one/two-step
  whole-number linear equations in x + constant-velocity cart
  motion; fractions, negatives, acceleration, multi-object motion
  are out of band).
- Fractions (inexact = honest "not a whole number on my line").
- LLM competence in the official value (det arm; addendum
  labelled separately).
- Band coverage beyond band 2 (bands 3–5 remain declared, no
  mechanism, no probes, no claims).

## Deviations (full text in experiments.md §E6.6)

- **D-e6l** (pre-code, design review): the E6.5-style sibling
  phrasology arc is structurally unworkable on the kin strip
  (each family carries different slot names; the bijection-by-name
  forbids cross-family mappings outright). Replaced pre-code with
  the name-bijection REJECTION arc — a stronger claim (a kin
  phrasing can never be silently mis-mapped).
- **D-e6m** (pre-freeze, smoke test): slot names must be pure
  lowercase letters (the mechanism's placeholder regex `{[a-z]+}`
  + fixed-number check `\d`); the digit-carrying name `{d0}`
  renamed `{start}` on the UNRELEASED band-2 templates (no pinned
  artifact references them).

## Artifacts

- Pre-registration + deviations + frozen derived constants:
  `plan/30-phases/phase-6-tutor/experiments.md` (E6.6 section).
- Build: `src/kainos/tutor/bands.py` (band-2 → implemented),
  `src/kainos/tutor/brainstem.py` (the aligned strip: seven frozen
  lessons, seven grammar families, the shared repeated-taking
  corridor, the seven rule-gated policies, the 10-template
  canonical vocabulary), `src/kainos/tutor/e66.py` (matrix + P1–P8
  + experiment class); runner registration (`e6.6`; 30
  experiments).
- Tests: `tests/tutor/test_e66.py` (16 tests: the mechanism);
  `tests/harness/test_runner.py` (registry count 30);
  `tests/tutor/test_e65.py` (the band-map test now validates the
  whole sweep-so-far registry).
- Official: `results/e6.6.{json,md}` (pinned `dcb897166`, script
  `62322a8d360d8681`), `results/phase-6/e6.6-run{1,2}/` (byte-
  identical), `results/phase-6/bands-map.json`, SUMMARY regen
  (e6.1–e6.6).
- Live addendum: `results/phase-6/e6.6-live/addendum.json`.

---

# E6.7 — "Band 3: geometry-advanced ∥ vectors/statics (9–12, the product band)"

`(T7 #157, the M3 band sweep, band 3; official 2026-08-22, pinned
`c8081d874`; pre-registered in experiments.md §E6.7 before code;
owner-directed "Continue to BAND 3")`

## Verdict

**PASS e6.7: 8/8 (8/8).** The third band of the M3 sweep is
official: geometry-advanced (rectangle perimeter/area, triangle
area, area comparison) and 1-D vectors/statics (east-west net
displacement, moment F·d, lever balance) learn as ONE aligned band
on the same teachable-strip seam — the PRODUCT BAND: ONE corridor,
many doors. Area, moment, perimeter×2 and distance (band 2) all
derive through the same grounded product helper — the frozen twin
probes measure the doors byte-equal (S2:03 ≡ S3:03 → 24, S4:01 ≡
S4:02 → 56; only the rule fact differs) — and the lever is the
band-2 repeated-taking corridor's THIRD door after algebra
division and pace (S3:11 ≡ S3:14 → 8, the algebra door's taking
cites shared by the balance door, which cites the product chain on
top). The alignment is STORED, not described: the cross-domain
prereq edges (`stat-moment ← geom-area` intra-band;
`geom-area-triangle ← alg-inverse-mul` and `stat-balance ←
alg-inverse-mul` cross-BAND, pointing at band-2 concepts from the
seed) are established+active assertions in the final store with
EMPTY prereq gaps on all six band-3 concepts. THREE measured walls
compose: the PRODUCT wall (9×9 = 81 off the line, firing through
BOTH the area and the moment door — the wall is domain-agnostic,
reproduced S4:11/S4:10), the NEGATIVE wall (a net west of the
start is past the line's origin — the grounded difference is
cited, the west side is honestly unreachable), and the INEXACT
walls (½·35 and 30/4 leave remainders — "not a whole number on my
line", never rounded). The band-2 kin phrasing from the seed
composes across bands (S2:15 parsed via `lexicon:phrasing:S03:16`,
grounded 29); the surface never forgets (9 established phrasings
seed → final); the band ENDS on the JOINT evaluation (one frozen
probe set, one check, both domains); all six band-3 concepts
stable (K = 4: counts 5/6/4/4/4/6) against all eighteen
seed/band-1/band-2 concepts; the line is untouched at 72 — it now
serves FOUR domains; 375 seed ids id-for-id; final store 441 =
375 + 20 new facts + 46 mastery events; run1 ≡ run2
byte-identical (run identity `ab85ba15f5f36627`).

## Deviations (full text in experiments.md §E6.7)

- **D-e6n** (build time, caught by the control): two turns the
  frozen script marks HONEST (S3:13 the inexact lever, S4:07 the
  negative wall) were transcribed `S` instead of `H` in the first
  hand copy of the derived per-session domain sequences; the
  control's P2 flagged the mismatch; corrected to `H` per the P2
  letter definition. Script/seed/checks/thresholds untouched.
- **D-e6o** (pre-registration doc inconsistency, resolved in favor
  of the frozen script): the Design's lesson-order bullet and the
  frozen script disagree on the moment/net order; the script
  ("teacher lines authoritative") was followed exactly.

## Live addendum (X6, separately labelled — never part of the
official value)

10 live 9–12 teacher questions (5 geometry-advanced, 5
vectors/statics; `pi-qwen-fast:latest`, 11.4 s, 0 call errors) →
**10/10 landed in honest ambiguity** (zero silent writes).
Diagnosis: the model writes in SCHOOLTEXT FORM — units everywhere
('square units', 'cm', 'm', 'N', 'm/s²'), 'Question N:' numbering
prefixes, multi-sentence framing, and INVERTED asks (solving for
an input: "if the area is 12 and its base is 6, what is its
height?") — against the single SPOKEN-SPEECH frozen grammar.
Recorded surface-widen candidates (NOT built): unit-stripping +
prefix-stripping normalization; the inverted family is a NEW
grammar family (out of band); acceleration is declared out of band.
Artifacts: `results/phase-6/e6.7-live/addendum.json`.

## What is NOT claimed

- General geometry or mechanics (2-D vectors, Pythagorean
  distances, angles, acceleration, non-rectangular areas — out of
  band).
- Negative numbers (west of the start = the NEGATIVE wall — the
  line's origin is a measured boundary).
- Fractions (halves and lever quotients are exact-or-honest).
- LLM competence in the official value (det arm; addendum
  labelled separately).

## Artifacts

- Pre-registration + deviations + frozen derived constants:
  `plan/30-phases/phase-6-tutor/experiments.md` (E6.7 section).
- Build: `src/kainos/tutor/bands.py` (band-3 → implemented),
  `src/kainos/tutor/brainstem.py` (the product strip: six frozen
  lessons, seven grammar families, the shared product + taking
  corridors riding the band-2 helpers, the seven rule-gated
  policies), `src/kainos/tutor/e67.py` (matrix + P1–P8 +
  experiment class); runner registration (`e6.7`; 31
  experiments).
- Tests: `tests/tutor/test_e67.py` (16 tests: the mechanism);
  `tests/harness/test_runner.py` (registry count 31);
  `tests/tutor/test_e65.py` (the band-map test now validates the
  whole sweep-so-far registry at 3 implemented bands).
- Official: `results/e6.7.{json,md}` (pinned `c8081d874`, script
  `d748aaf9953c0466`), `results/phase-6/e6.7-run{1,2}/` (byte-
  identical), `results/phase-6/bands-map.json`, SUMMARY regen
  (e6.1–e6.7).
- Live addendum: `results/phase-6/e6.7-live/addendum.json`.
