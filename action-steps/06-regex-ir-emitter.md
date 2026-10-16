# Action Step 06 — Regex IR dialect + PCRE emitter (P1.01–P1.02)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

The regex-dialect AST nodes (as a specialization of the generic Semantic IR) and a
PCRE emitter that translates them deterministically.

## Prerequisites

- [ ] Steps 01–05 done (Phase 0 complete).

## Background

This is the first "real" phase. The AST is the Semantic IR's regex **dialect**; the
emitter is a *dumb* rule-applier — meaning lives in the CODEX (step 07), not here.
The emitter must be byte-exact for the canonical examples (they become tests).

## Steps

### 1. `src/kainos/regex/ir.py`

Enums + nodes for the dialect:

```
Node (base)
Sequence(elements: list[Node])
Repeat(node: Node, quantifier: Quantifier)
Class(kind: ClassKind)                 # digit, letter, word, whitespace, any
Literal(text: str)
Anchor(kind: AnchorKind)               # start, end
Alternative(branches: list[Node])
Group(node: Node)
Flag(name: str)                        # e.g. "case_insensitive"
UnresolvedRef(surface: str, candidates: list[str])
Quantifier (enum): one_or_more, zero_or_more, optional, exactly(n), at_least(n), at_most(n), between(a,b)
```

Each node implements `to_generic() -> dict` and `from_generic(dict) -> Node`, mapping
onto the generic IR: a node is an `entity` with a `type` from this dialect's enum,
wired by `relationships` (`sequence`, `repeat`, `alternative_branch`, `flag`). The
generic→dialect round-trip must be lossless (test it).

### 2. `src/kainos/regex/emitter.py`

`emit(node: Node) -> str` per this table (byte-exact):

| AST | PCRE |
|-----|------|
| `Sequence(a,b,c)` | elements **concatenated, unwrapped**: `a b c` |
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
| `Literal(s)` | `s` with regex metachars `\.^$*+?()[]{}|` escaped |
| `Anchor(start)` | `^` |
| `Anchor(end)` | `$` |
| `Alternative(a,b)` | `(?:a|b)` |
| `Group(n)` | `(?:n)` |
| `Flag(case_insensitive)` | prefix `(?i)` |

`UnresolvedRef` has no PCRE — emitting one must **raise** `UnresolvedError` (never
guess; the resolver in step 08 resolves it first).

### 3. Tests

`tests/regex/test_ir.py`: every node round-trips generic→dialect losslessly.
`tests/regex/test_emitter.py`: table-driven — every rule above; plus the two canonical
examples (byte-exact):
- `Sequence[Literal("cat"), Repeat(Class(digit), one_or_more)]` → `cat\d+`
- `Flag(case_insensitive) + Sequence[Repeat(Class(digit), exactly 3), Literal("-"),
  Alternative(Literal("foo"), Literal("bar"))]` → `(?i)\d{3}-(?:foo|bar)`
- emitting an `UnresolvedRef` raises.

Note: sequences emit as plain concatenation — only `Group`/`Alternative` add `(?:…)`
wrapping. (An earlier draft row `Sequence(a,b,c) → (?:a)(?:b)(?:c)` contradicted both
canonical examples and is corrected here; the authoritative table is in
`plan/30-phases/phase-1-regex/spec.md` §3.)

## Verification

```bash
pytest tests/regex -q
```

Expect: all green, canonical examples byte-exact.

## Done when

- [ ] `ir.py` + `emitter.py` exist; generic↔dialect round-trip lossless
- [ ] all emitter rules green, including canonical examples (byte-exact)
- [ ] `UnresolvedRef` emit raises
- [ ] `pytest tests/regex -q` green

## If stuck

`plan/30-phases/phase-1-regex/spec.md` §2–§3 (the authoritative tables).
