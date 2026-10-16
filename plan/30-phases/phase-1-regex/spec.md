# Phase 1 — Regex spec (normative tables)

Cited by action-steps 06–08. This is the authoritative grammar/dialect/emitter
definition; the directives' inlined copies must match this file, and if they drift,
this file wins and the directives get a fix.

## §1 — Input grammar (restricted English, deterministic kernel)

Clause templates (all lowercase-matched; whitespace-insensitive):

| Template | Produces |
|----------|----------|
| `beginning/start of string` … | `Anchor(start)` prefix |
| `end of string` | `Anchor(end)` suffix |
| `<quantifier-surface> <class-surface>` | `Repeat(Class, quant)` |
| `the literal <text>` | `Literal(text)` |
| `a hyphen` / bare content word (e.g. `a dash`) | direct CODEX lexicon lookup: exact `realizes_as` → `Literal(realization)`; else `UnresolvedRef(surface, candidates)` (§4) |
| `either <a> or <b>` | `Alternative(a, b)` |
| `a group of (…) ` | `Group(…)` |
| `ignoring case` | `Flag(case_insensitive)` |
| `<connector> <clause>` | sequence continuation / alternative |

**Quantifier surfaces:** `one or more`→`one_or_more`; `zero or more`→`zero_or_more`;
`optional|maybe|optionally`→`optional`; `exactly N | N <class>`→`exactly(N)`;
`at least N`→`at_least(N)`; `at most N`→`at_most(N)`; `between N and M | from N to
M`→`between(N,M)`.

**Class surfaces:** digit(s)/number(s)→`Class(digit)`; letter(s)→`Class(letter)`;
word→`Class(word)`; whitespace/space(s)→`Class(whitespace)`;
any/anything→`Class(any)`.
Disambiguation: bare "number(s)" followed by a standalone numeral → `Literal`;
else `Class(digit)`; truly ambiguous → `UnresolvedRef` with both candidates.

**Connectors:** `followed by | then | and | ,` → sequence; `or | either…or` →
alternative.

**Reference terms:** `thing`, `the … thing`, `it`, `that` →
`UnresolvedRef(surface, candidates=[…])` for rotation in the resolver.

**Lexicon-reference rule (important):** the parser assigns **no character values**,
never. `Class` surfaces keep *semantic* class identity; content words like
`hyphen`/`dash` are resolved at parse time by a **direct** CODEX lexicon lookup
(exact `realizes_as` hit → `Literal(realization)`; the test `"three digits, then a
hyphen"` → `Literal("-")` in step 07 is this path). A miss or ambiguity yields an
`UnresolvedRef`, which the phase-1 resolver (§4) handles by **rotation** or
escalation. Meaning lives in the CODEX (invariant #2); the parser is a pure function
of text → AST.

## §2 — Dialect AST

```
Node (base)                        # to_generic()/from_generic() — lossless
Sequence(elements: [Node])
Repeat(node: Node, quantifier: Quantifier)
Class(kind: digit|letter|word|whitespace|any)
Literal(text: str)
Anchor(kind: start|end)
Alternative(branches: [Node])
Group(node: Node)
Flag(name: str)                    # e.g. "case_insensitive"
UnresolvedRef(surface: str, candidates: [str])
Quantifier: one_or_more, zero_or_more, optional, exactly(n), at_least(n), at_most(n), between(a,b)
```

## §3 — Emitter (deterministic, byte-exact)

| AST | PCRE |
|-----|------|
| `Sequence(a,b,c)` | `a b c` **concatenated, no wrapping** |
| `Repeat(n, one_or_more)` | `n+` |
| `Repeat(n, zero_or_more)` | `n*` |
| `Repeat(n, optional)` | `n?` |
| `Repeat(n, exactly(k))` | `n{k}` |
| `Repeat(n, at_least(k))` | `n{k,}` |
| `Repeat(n, at_most(k))` | `n{0,k}` |
| `Repeat(n, between(a,b))` | `n{a,b}` |
| `Class(digit)` | `\d` |
| `Class(letter)` | `[A-Za-z]` |
| `Class(word)` | `\w` |
| `Class(whitespace)` | `\s` |
| `Class(any)` | `.` |
| `Literal(s)` | `s` with metachars `\.^$*+?()[]{}|` escaped |
| `Anchor(start)` | `^` |
| `Anchor(end)` | `$` |
| `Alternative(a,b)` | `(?:a|b)` |
| `Group(n)` | `(?:n)` |
| `Flag(case_insensitive)` | prefix `(?i)` |

Canonical examples (byte-exact, become golden tests):

1. `Sequence[Literal("cat"), Repeat(Class(digit), one_or_more)]` → `cat\d+`
2. `Flag(case_insensitive) + Sequence[Repeat(Class(digit), exactly(3)), Literal("-"),
   Alternative(Literal("foo"), Literal("bar"))]` → `(?i)\d{3}-(?:foo|bar)`

`UnresolvedRef` at emit time ⇒ `UnresolvedError`. The emitter never guesses
(§4 escalates first).

> **Note (correction, 2026-08-19):** an earlier draft had `Sequence(a,b,c)` →
> `(?:a)(?:b)(?:c)`, which contradicted its own canonical example 1 (`cat\d+`, unwrapped).
> Concatenation is the rule; examples 1 and 2 are both satisfiable by it.

## §4 — Resolver

`resolve(node, codex) -> (node, trace)`:

1. Each `Class` → verify/look up its `realizes_as` in the CODEX lexicon; record
   `{term, realized_as, assertion_id}` in the trace.
2. Each `UnresolvedRef` (vague references that survived the parser's direct lookup)
   → **rotate** through candidates' CODEX neighborhoods: exactly one reachable
   realization → resolve; several → keep unresolved, `status=REQUIRES_CONTEXT` +
   candidates; none → `UNSEEN`.
3. Any ref still unresolved ⇒ the pipeline returns an **escalation**
   (`recommended_action: "ask_human"`) and emits **no regex**.

## §5 — CODEX's role (lexicon)

`kainos.regex.lexicon.seed(codex)` asserts, with `Source(uri="seed_corpus")` and
`status=established`:

```
"hyphen" --realizes_as--> "-"          "start"  --realizes_as--> "^"
"digit"  --realizes_as--> "\d"         "end"    --realizes_as--> "$"
"letter" --realizes_as--> "[A-Za-z]"   "whitespace" --realizes_as--> "\s"
"word"   --realizes_as--> "\w"         "any"    --realizes_as--> "."
```

**Lexicon↔emitter parity test:** for every seeded `realizes_as` target, the emitter's
output for the corresponding node must equal the realization. The CODEX is the single
source of truth for *what a term means as characters*; the emitter's built-in class
table is its canonical projection and is held consistent by this test.

## §6 — Test generation + judge

`testgen.generate(node, seed=0) -> (positives, negatives)`: positives instantiate each
node to concrete strings and expand quantifiers within bounds; negatives mutate
exactly one element to violate one constraint. Deterministic under `seed`.

The **judge** compiles the pattern in **Perl** (`scripts/judge.pl`, ADR-0009) and
full-matches every example; `Verdict(ok, mismatches=[…])` includes a human-readable
diff. Python `re` is never the arbiter.
