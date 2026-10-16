# 10.x — Multi-Agent Games: perspective modeling + sharing strategy (Phase 5)

> **Status: PLANNED — queued after #149** (the Einstein-puzzle robustness
> experiment); long-term horizon, not scheduled. Build queue: OpenProject
> epic "Phase 5 — Multi-Agent Games" + tickets (created 2026-08-21). The
> owner green-lit the direction and delegated the design: *"I don't know the
> best way to set this up or test for this kind of interaction so I'll leave
> it to you."*

Owner's ask (gist): multiple kainos-backed agents in a **partially shared
information environment** — a shared view plus private views — playing
competitive or cooperative games. Test whether they **(a)** can **model the
perspective of the other participants** and **(b)** how they **develop
sharing strategies in response to those models**.

## Research questions (falsifiable, up front)

- **RQ1 (formation):** Given its private state and the other agent's
  behavior, does an agent maintain **correct, provenance-linked** assertions
  in its own store about (i) the other's private state and (ii) the
  other's *beliefs*?
- **RQ2 (use):** Do **behavioral** metrics (message redundancy,
  false-belief correction, bluff detection) separate the ToM-capable agent
  from a ToM-**ablated** agent at equal capability budget?
- **RQ3 (development):** Across episodes whose conditions change
  (tightening budgets, unreliable opponent, shifting deception incentive),
  does the agent's sharing **policy change in an inspectable,
  provenance-carrying way** — and does performance move with it?

**Honesty boundary (scope, named before building):** what this setup
measures is **formal model tracking** — belief-formation rules derived from
the declared game protocol + observed behavior, white-box and exact — not
open-ended "psychological" Theory of Mind. Open-endedness is the *stretch*
arm (LLM-surface messages, optional, SKIP-semantics per E3.1), and even it
is contract-bounded. This is the stronger, testable claim; the weaker one is
declared out.

## The two games (chosen to *separate* the two questions)

### E5.1 — "The Shared Grid" (cooperative; RQ1+RQ2 first- and second-order)

- A grid of cells, each with a property from a small known vocabulary
  (e.g. `{empty, wall, goal, key, door}`); a path must be jointly produced.
- **Views are disjoint + a shared layer:** agent A holds rows 1–2 private,
  B holds rows 4–5 private, both see row 3 — *but the shared layer is the
  probe*: in the false-belief episodes, A's copy of row 3 is **planted
  wrong** (A believes B sees what B does not).
- Communication: structured messages (assertion sets over the cell
  vocabulary) through a scoped channel with a per-episode **budget** in
  bits/messages (tightened across the sweep).
- **Why it measures ToM:** an agent that models B's perspective sends *only
  the missing facts*; one that doesn't re-sends what B already has. The
  information-theoretic minimum is **computable from the view spec**, so the
  separation is an exact ratio, not a vibe:
  - `redundancy = (bits sent − bits the receiver lacked) / bits sent`.
- **Second-order probe (Sally-Anne in a game, embedded — the design's
  signature):** with A's shared view planted wrong, only an agent modeling
  *what B believes* can notice (B acts as if row 3 were otherwise) and emit
  the **explicit correction assertion** ("your row 3 is wrong"). Metrics:
  *detection latency* (round of the first explicit mismatch assertion) and
  *recovery rate* (both end with the correct grid). A non-ToM agent can at
  best limp via failure; it *cannot emit the correction sentence* — the
  probe is structurally clean.

### E5.2 — "The Range Game" (competitive; RQ1+RQ2 under incentive)

- Each agent holds a secret number in `1..N` (seeded, independent).
- Over `T` rounds each may send **one claim**: an interval (about its own
  value or its estimate of the other's) — **claims may be false** in the
  deception episodes. Then each commits an **estimate of the other's
  number**; the closer estimate takes the pot.
- **Why it measures ToM where ToM matters:** scoring is *literally*
  how well you model the other. Exact decision-theoretic baselines exist:
  - *Bayes-risk gap*: score vs. the optimal posterior under the declared
    protocol (computable for these small discrete state spaces).
  - *Leakage*: mutual information between the public transcript and each
    private value (does my talk give your number away to a rational
    listener?).
  - *Bluff usage & detection*: with misleading claims incentive-rewarded,
    (i) do agents actually bluff (usage rate vs. the optimal bluffing
    frequency for the game), and (ii) does the receiver's posterior after a
    false claim track the **correct** posterior (detection = not being
    fooled, at the calibrated price of not being *too* fooled)?

### E5.3 — "Strategy development" sweeps (RQ3, both games)

Episode sweeps with one changed condition at a time:
- E5.1: **budget tightening** (4 → 2 → 1 message/round) → does the agent's
  message *selection* sharpen toward the genuinely-missing/differing cells
  (redundancy curve under budget), and does it prioritize *confirmations* of
  high-risk cells when the channel's corruption rate rises?
- E5.2: **opponent reliability** (honest → 20% liar → 50% liar) → does the
  agent's *trust calibration* move toward the correct posterior weighting,
  and does its own bluffing frequency adapt?
- **The control that makes it a learning claim:** a V1-capped variant whose
  policy is frozen (no policy updates allowed) — if the sweeping agent
  improves and the frozen one doesn't, the delta is the *development*, not
  drift.

## Environment: the partially-shared information substrate

- **`GameSpec` = data:** player set, `views` (per-agent private sets +
  shared set), channel `{scope: private|shared, budget, corruption}`,
  turn protocol (round-based, synchronous, seeded), scorer reference.
  New game = new spec + scorer; no kernel code.
- **`kainos.game.kernel`:** `Agent` (its CODEX + bounded planner + channel
  stub + **policy store**), `Channel` (scoped message queue; a message is
  an **assertion delta** — the step-19 exchange protocol, verbatim:
  idempotent, provenance-carrying), `Scheduler` (deterministic round
  driver), `Scorer` (pure function → `GameReport` JSON in
  `results/phase-5/`, harness-registered).
- **Information isolation is a structural invariant** (enforced at the
  perceive step: an agent *cannot read* cells outside its views) and is
  pinned by test, exactly like the E3.7 negative control — a "leaky view"
  is a bug with a failing test, not an assumption.
- **Communication defaults to STRUCTURED** (assertion sets over declared
  vocabularies). The LLM-surface arm (T6, optional) adds natural-language
  messaging later; it rides E3.1 SKIP semantics and, per the queue decision,
  sits behind Phase-4 brainstem (T2) so the two efforts share one surface
  layer instead of building two.

## Measurement — the signature (store + behavior + ablation)

Black-box agent studies can only guess at the model; ours can **read it**.
Every experiment reports three layers:

1. **Store audit (white-box belief probe).** Query the agent's CODEX for
   assertions *about the other agent* (provenance `source=agent_b` /
   `evidence=observed`). Metrics: **correctness rate**, **provenance-chain
   completeness** (every "B knows/believes p" traces to an observed
   message/action — no unbacked mind-reading), and **dispute discipline**
   (when B's talk and B's behavior contradict, is the conflict *preserved
   and reconciled* — A5 at the social scale — or averaged/overwritten? That
   last check is an inherited invariant, not a new metric).
2. **Behavior**, per game, above: redundancy ratio to the computable
   minimum; detection latency/recovery; Bayes-risk gap; leakage (MI); bluff
   usage vs. optimum; posterior-after-blow vs. correct posterior.
3. **Ablations for causation** (same-budget discipline, E3.2/E3.5):
   - **V0 — ToM-ablated:** capability set (P11: capabilities ARE store
     data, so *removing* "reason-about-other" is a one-line store op, no
     code change) excludes cross-agent modeling; the store simply lacks
     those slots.
   - **V1 — full.**
   - **V2 — second-order-only** (models the other's *beliefs*, not its
     hidden state) — isolates exactly what the false-belief probe needs.
   - **Reading:** if V1 beats V0 on the behavioral metrics at equal
     capability budget, the effect is attributable to perspective modeling;
     V2's performance on the false-belief probe bounds the second-order
     contribution.

## "Develops a sharing strategy" — operationalized as *policy-as-data*

This is the design's most distinctive move and it exists **because** of
this project's P11/P12 disciplines: the agent's sharing policy (redundancy
tolerance, confirmation priority, channel trust weights, bluff frequency)
is a **cluster of store assertions with provenance** — inspectable,
versioned, and changed only through candidate→verification→established. An
episode's outcome (scorer report) generates a **candidate policy revision**;
whether it is applied is a verified decision, logged, traceable.
"Development of strategy" is then measured *precisely*: the
policy-assertion diff + performance delta across the sweep, against the
frozen-policy control. No black-box weights; the "strategy" is something
the *owner can open and read* — which is also what makes the attention/
audit story of Phase 4 consistent.

## Reused vs. new (honest scorecard)

| Part | Reused (built + proven) | New build |
|---|---|---|
| Message medium + merge semantics | assertion-delta protocol (step 19, ADR-0016), idempotent merge, provenance | GameChannel (scope, budget, corruption) |
| Private/shared isolation | CODEX stores + WORKSPACE (E3.7) | view enforcement (structural, test-pinned) |
| Action choice | bounded planner + capability-as-data (E3.6, P11) | game capabilities (`send_message`, `commit`, …) |
| Beliefs about the other | CODEX assertions + provenance + reconciliation (A5) | protocol-derived belief-formation rules + store-audit harness |
| Learning across episodes | status-transition discipline | policy-as-store-data + episode-outcome → candidate policy + frozen-policy control |
| Judging | harness, JSON reports, judges | GameScorer (pure functions; IT/decision-theoretic baselines) |
| Surface | LLMKernel (E3.1) — optional arm only | — (SKIP semantics) |

## Pre-registered threshold *forms* (numbers fixed at build time from
control runs — the *forms* are locked now, per the no-loosening discipline)

- E5.1: redundancy **as a ratio of the computable IT minimum** (V1 tight,
  V0 wide — separation pre-registered as a ratio gap, not an absolute);
  false-belief probe: V1 emits the explicit correction assertion above
  threshold probability within bounded latency; V0 is *structurally
  incapable* of that assertion (the probe is clean by construction).
- E5.2: Bayes-risk **gap to the exact optimum**, per variant; leakage by
  MI; bluff detection = posterior accuracy after false claims, V1 vs. V0.
- E5.3: sweep-curve **quartile improvement** for V1 vs. flat frozen
  control (direction + significance pre-registered; magnitudes from
  control-runs, recorded as deviations if they move).

## Build status (as of 2026-08-21)

**T1 kernel (#161) + T5 ToM store-audit (#165): BUILT + CLOSED by owner
sign-off.** Acceptance `PASS e5.0: 12/12` (commit 3d4ffb1; D-m9–D-m12).

**T2 e5.1 The Shared Grid (#162): BUILT + CLOSED by owner sign-off.**
Official run `PASS e5.1: 12/12` (commit 49b7753): at equal budget, V1/V2
redundancy **1/9** vs the V0 ToM ablation **5/13** (gap 32/117,
pre-registered); the embedded false-belief probe is passed by V1
**and** V2 at exactly round 4 (the explicit correction assertion), V0
is structurally incapable of it (capability-gated, named gap) and
commits the planted row wrong at exactly the 2 planted cells.
**Milestone M1 satisfied.**

**T3 e5.2 The Range Game (#163): BUILT + CLOSED by owner sign-off
(2026-08-21, delegation: owner removed the sign-off gate — official
`PASS e5.2: 8/8` evidence stands, commit 4b5f756).** The competitive
measurement with the declared-deception regime (B = 12/48 values bluff,
exact incentive record D-e5d attached: 41/48 one-shot-profitable
deviations — the payoff structure's equilibrium is degenerate,
recorded, not hidden): pooled mean |error| **V0 12 / V1 583/96 /
V2 79/48** (V2 = the Bayes lower bound of the declared protocol), V2
wins **113/192** of the pot head-to-head vs V1, **V2 detects all 48
bluffs** (posterior all-mass-on-B) vs V1's 8/48, leakage 4.633 bits
rational-listener estimate vs 4.6705 analytic, localization 16/48 the
K-draw information limit (detection ≠ localization — the boundary is
informational). All 8 checks frozen pre-run and reproduced exactly; 240
kernel runs bit-identical and field-for-field equal to the exact math.
Pre-registration + D-e5d/e5e/f/g: `plan/30-phases/phase-5-multi-agent/experiments.md`; verdict in `results.md`. **Milestone M2
satisfied.**

**T4 e5.3 Strategy-development sweeps (#164): BUILT + CLOSED by owner
delegation (2026-08-21).** Official run `PASS e5.3: 8/8` (commit
b988e94): the RQ3 development sweep on the drifting Range Game
(opponent liability 0 → 35% → 70%, 48 balanced pairs/leg, V1-capped
arms). Arm A (trust = persistent-CODEX store data: verified
per-episode labels, discounted Haldane-Laplace ρ̂, β = 3/4) develops
inside the drift legs and **reaches exact parity (pot share 1/2) with
the exactly-calibrated reference** in the late pool; the frozen
control F (ρ = 1/4, same capabilities/episodes/experience, policy
never reads its store) does not (11/24; late calibration gap 0.1551
vs A's 0.0291). The pre-registered POOLED estimator was refuted in
the control (lagged the drifting regime; late share inferior to F) and
replaced pre-freeze (D-e5n — a recorded, reproducible result about
persistent learners); three more pre-registration fixes (D-e5o/p) and
six design records (D-e5h/i/j/k/l/m). All 8 checks frozen pre-run and
reproduced exactly; 288 kernel games bit-identical and
field-for-field equal to the exact math; 144/144 labels
ground-truth-exact, self-sourced, evidence-carrying. Spec's
quartile-improvement acceptance: met (direction + exact frozen
magnitudes). Verdict + bounded claims: `plan/30-phases/phase-5-multi-agent/results.md`.
**Milestone M3 satisfied.**

**T6 (#166, M4 stretch) — BUILT + OFFICIAL 2026-08-22**: `e5.4` the
LLM-surface messaging arm, `PASS e5.4: 1.0` (5/5) — the E5.1
acceptance survives the natural-language message surface exactly
(SKIP/canonical arm), the frozen one-message drop is honest and
measured, and the live 27B addendum round-tripped 46/46 (separately
labelled). Verdict: `30-phases/phase-5-multi-agent/results.md` (T6
section). `e5.0` is the kernel-acceptance number (roadmap registry
note); the game numbers are as pre-registered. Remaining M4 scope:
the 3+ player / team generalization (deferred — owner-gated; the
2-player games being green is its entry condition).

## Milestones (undated; sequence begins after #149)

- **M1:** kernel + E5.1 end-to-end; view-isolation negative control; the
  V0/V1 redundancy separation demonstrated.
- **M2:** E5.1 false-belief probe + V2; E5.2 with Bayes/leak/bluff metrics.
- **M3:** E5.3 development sweeps + store-audit reporting (policy diffs,
  provenance chains, dispute discipline).
- **M4 (stretch):** LLM-surface messaging arm — **DONE 2026-08-22**
  (`e5.4` official 5/5, verdict in phase-5 results.md; the arm rides
  the Phase-4 T2 surface layer per the recorded edge #152 → #166);
  3+ player / team generalization — deferred (the kernel admits it;
  the games are 2-player by design for exact baselines; entry
  condition — 2-player green — is met as of `e5.4`).

## Open questions (owner input welcome)

1. **Bluffing as a value question:** do we *want* the competitive agent to
   learn to bluff, or only to *defend* against it? Current stance: measure
   both usage and detection; the *ethics* of a shipped agent's bluffing
   belongs to Phase-4-style behavior policy (T8 there), not this experiment.
2. **LLM surface:** share Phase-4 brainstem (the edge says so) or a minimal
   surface of our own? Leaning shared — one surface layer, two consumers.
3. **n > 2:** keep 2-player for exactness; team games only in M4.
