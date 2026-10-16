# 10.x — Projection (goal-directed semantic transformation)

> Phase 3 capability (ADR-0011), claim **X1** (capability faithfulness) + **X2**
> (structured creativity). The idea originates in `SUPPLEMENTAL_IDEAS.md`
> ("the missing concept is not better language generation, it's
> goal-directed semantic transformation").

## The formula

A response is not predicted from a prompt. It is **computed**:

```
Response = Realize( Project( Parse(Input), Context, Knowledge, Capabilities, Goal ) )
```

- **Parse** — the Language Kernel turns input into Semantic IR (existing, Phase 1+).
- **Project** — the reasoner searches for a *plan*: a sequence of declared
  capabilities that transforms current world-state into a terminal state
  satisfying the goal. A goal that no valid plan satisfies is a **first-class
  outcome** (NO VALID PLAN), not an error to paper over.
- **Realize** — the surviving plan's result is turned back into language/artifact
  (existing Realizer contract).

Phases 1–2 already contain *mini*-projections: the regex pipeline is a one-step
plan (`resolve → emit → judge`) and the 20Q game loop is a plan toward an
identification goal. What Projection adds is the **general capability model**:
multi-step plans with preconditions/effects, interaction-type contracts, and
capability gap reporting.

## Capabilities are first-class TERMS (P11)

Every capability the system may invoke is an explicit, declared TERM in the CODEX
with `status=established` and provenance:

```
CAPABILITY: GENERATE_IMAGE
├── PRECONDITION: image_generator_available
├── INPUT:        visual_description
├── EFFECT:       creates IMAGE(…)
└── COST:         (class: moderate)
```

- **Declared, not implied (P11):** the planner may only use capabilities present in
  the registry. If no declared capability chain reaches the goal state, the result
  is **NO VALID PLAN** — never a hallucinated action.
- The NO VALID PLAN response contract names the **missing capability**, offers the
  **nearest viable plan** (the longest valid prefix, e.g. "I can't generate images,
  but I can produce a detailed description/prompt for an image generator"), and is
  itself inspectable (plan-search trace + why each alternative failed a
  precondition).
- Adding a capability = adding an assertion (with provenance). Removing = status →
  `obsolete`. No code change required for the planner.

## Planning as proof

A plan is a sequence `c₁ … cₙ` such that, applying each capability's effects:

```
S₀ --c₁--> S₁ --c₂--> … --cₙ--> Sₙ  where  Sₙ ⊨ GOAL
```

and every `cᵢ`'s preconditions hold at its step. The planner is a bounded search
over this space (depth budget + cost bound, like the reasoner's search). The
acceptance chain (precondition checks + effect application) **is** the evidence
artifact for inspectability (P9).

## The "space of acceptable answers"

Many inputs (e.g. "give me a picture of a dragon") define a **region** of valid
terminal states, not a single answer. Defaults come from the CODEX
(`has_default` assertions — `DRAGON → default_visualization = conventional`), are
applied as `X = DEFAULT(term)` values, and every default application is recorded in
the trace. Explicit user constraints override defaults. This is how underspecified
requests get a *justified* completion instead of a guess.

## Search-space-aware clarification policy

Beyond the EXCEPTION cost ladder (`E = depth × ambiguity × lack_of_evidence`, see
`exception-system.md`), the projection layer adds **search-space statistics** to
decide how to act on a large/ambiguous goal region:

| Space statistics | Policy |
|------------------|--------|
| small (one viable branch) | **choose** |
| large + cheap to explore | **explore** (structured traversal below) |
| large + high stakes / high cost | **ask** the user (the question that most reduces uncertainty *over the plans*) |
| ambiguous + low stakes | **choose a default** (recorded, overridable) |

The clarification question is selected by the *same* information-gain machinery as
20Q (A1) — except the hypothesis space is **candidate plans / plan branches**, not
hidden concepts.

## Structured creativity (X2)

"Most probable" ≠ "good." Traversal of the valid plan/interpretation space may be
**stochastic but constrained**:

```
P(next branch) = f(relationship strength, context fit, novelty, constraint satisfaction, history)
```

A **creativity parameter** (semantic temperature) controls exploration:

- `T = 0` — strongest valid path (deterministic).
- moderate — strong paths + occasional unusual-but-valid paths.
- high — deep exploration of unusual but valid relationships.

Hard constraint: **novelty may not violate established facts.** Temperature varies
*which valid path is taken*, never *whether an established assertion holds*
(P5/P6 remain absolute). Every creative choice is recorded in the trace (branch +
temperature + seed) so output variety is reproducible and auditable.

## Interaction types & response contracts

Parsed input carries an interaction type; each type has a **response contract**
(the shape of a correct response, checked by the realizer's validator):

| Type | Goal shape | Response contract |
|------|-----------|-------------------|
| REQUEST | produce/change an artifact | executed plan + result (+ trace) |
| QUESTION | truth/value of a proposition | answer + evidence + uncertainty state |
| COMMAND | state transition | action taken + resulting state |
| ASSERTION | record a fact | acknowledgement + provenance + epistemic state |
| CORRECTION | replace a prior assertion | superseded + replacement, both retained |
| (impossible) case | goal with NO VALID PLAN | named capability gap + nearest viable plan |
| (ambiguous) case | underspecified goal | clarifying question selected by info-gain |

Types not listed are simply unconstrained (no contract check) until added — the
list grows as domains need it.

## Scope guards

- Phase 3 only; Phases 0–2 pipelines are untouched (the regex pipeline keeps
  emitting regexes directly — it is a one-step plan and does not need the general
  planner).
- No side effects of any kind are exercised in E3.6: capabilities are
  **simulated** (a fake "image generator" that records the call), because the claim
  is about *planning faithfulness*, not tool execution.
- No new package until built: lives in `src/kainos/projection/` (directive 21).
