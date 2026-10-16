# EXCEPTION System

The first-class representation of **the boundary of the system's knowledge**.

## The key distinction (P5)

- **EXCEPTION** = a *representable but insufficiently characterized* **valid**
  combination of TERMs/relationships.
- **IMPOSSIBLE** = a **hard constraint violation** — categorically different.

`TREE ∈ ANIMAL` is IMPOSSIBLE (violates `is_a` constraints).
`electronic + edible` is an EXCEPTION (both are valid concepts; their combination is
simply unexplored/unverified).

## EXCEPTION states (failure taxonomy)

| State | Meaning |
|-------|---------|
| `UNSEEN` | Never encountered. |
| `UNRESOLVED` | Encountered, cannot solve. |
| `AMBIGUOUS` | Multiple interpretations viable. |
| `CONFLICTING` | Evidence supports incompatible interpretations. |
| `UNVERIFIED` | Plausible, hasn't passed formal checking. |
| `REQUIRES_CONTEXT` | Answer depends on missing information. |
| `IMPOSSIBLE` | Violates a hard constraint (the terminal state). |

## The EXCEPTION cost `E`

```
E = depth × ambiguity × lack_of_evidence
```

Escalation ladder at runtime, keyed to `E`:

| E | Action |
|---|--------|
| low | Make a reasonable inference (best candidate). |
| medium | Search the CODEX more deeply (raise depth budget). |
| high | Retrieve evidence (go to SOURCE). |
| extreme | Ask the human ("Could you explain exactly what you mean by …?"). |

This is the principled answer to *"when should the AI stop pretending it knows?"*
and *"when should it ask for help?"*.

## The EXCEPTION lifecycle (how the ontology evolves)

```
UNKNOWN → EXCEPTION → REPEATED CONFLICT → PATTERN DETECTED
        → MISSING DIMENSION SUSPECTED → NEW CONTEXT TERM → GENERALIZED RELATIONSHIP
```

A contradiction is **evidence the representation is missing a dimension** (P6). The
learning loop uses EXCEPTION pressure to *refine the ontology*, not just to flag
errors. This is the mechanism behind "discover an abstraction the designer didn't
put in".

## Active learning via EXCEPTION

When the system asks "did you mean A or B?" and the user answers "B", the CODEX
records `EXCEPTION → clarified → VERIFIED RELATIONSHIP`. Next time, no question.
This is the *human-in-the-loop* learning path that makes training data out of
conversation.

## Coverage metric

```
Coverage(T, C) = verified_combinations(T,C) / encountered_combinations(T,C)
```

Measures "how well does the system understand term T in context C?". A shrinking
EXCEPTION space + growing ontology = *measurable learning* (see phase-2 experiments).

## Where EXCEPTION lives

Each ASSERTION may carry an `exception` field (see codex.md). A combination's
exception state is computed by the reasoner from the assertions involved; it is not
a separate silo.
