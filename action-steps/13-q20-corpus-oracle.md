# Action Step 13 — 20Q corpus + property oracle + CODEX seed (P2.01–P2.02)

> Self-contained: you need only `00-CONTEXT.md` + this file.

## Goal

The 20 Questions world: a concept corpus with property tables, a seeded deterministic
oracle, and the whole corpus loaded into the CODEX as assertions.

## Prerequisites

- [ ] Phase 1 complete (steps 06–12), since this reuses `kainos.codex`, `kainos.ir`.

## Background

20 Questions is the active-learning environment. The oracle answers
`yes / no / unknown / sometimes`; `unknown` (undefined property) and `sometimes`
(conditional property) are what create EXCEPTION pressure and the contradiction→
dimension signal. The corpus must live in the CODEX (assertions with provenance), not
in a separate data structure the reasoner can't see.

## Steps

### 1. `data/q20/concepts.json`

100–300 concepts across categories (animals, objects, foods, vehicles, places,
people). Each: `{id, label, categories: [..], properties: {alive: "no", manufactured:
"yes", has_wheels: "yes", wheel_count: 2, can_carry_person: "yes", has_engine: "no", ...}}`.
Property values: `"yes" | "no" | "sometimes" | <number>`; **omit** a property to make
it `unknown` for that concept (intentional EXCEPTION seeds).

### 2. `data/q20/questions.json`

The valid question set: `{id, surface, kind, property}` where `kind ∈
{property_probe, category_probe}`. E.g. `{id:"q_alive", surface:"Is it alive?",
kind:"property_probe", property:"alive"}`.

### 3. `src/kainos/q20/oracle.py`

`answer(concept_id, question, seed=0) -> str` (`yes|no|unknown|sometimes|number`):
- `property_probe`: look up the property → `yes`/`no`/`number`; missing → `unknown`;
  value `"sometimes"` → `sometimes`.
- `category_probe`: `yes` if `category` in `categories`, else `no`.
- Fully deterministic.

### 4. CODEX seed

`src/kainos/q20/seed.py` — `seed(codex)`: for each concept/property/category, add
assertions:
```
concept --has_property--> property=value      (Source(uri="q20_corpus", version="1"), status=established)
concept --is_a--> category                     (same source/status)
```
Omit properties that are missing (they stay `unknown` — do not write `unknown`
assertions; absence is the signal).

### 5. Tests

- `tests/q20/test_oracle.py`: deterministic; missing property → `unknown`;
  `"sometimes"` → `sometimes`; category probe correct.
- `tests/q20/test_seed.py`: every concept/property present as an assertion; `dump()`
  shows provenance on each; no bare edges.

## Verification

```bash
pytest tests/q20/test_oracle.py tests/q20/test_seed.py -q
```

Expect: all green.

## Done when

- [ ] corpus (100–300 concepts) + questions + deterministic oracle exist
- [ ] corpus seeded into CODEX as assertions with provenance
- [ ] `unknown`/`sometimes` behavior correct and tested

## If stuck

`plan/30-phases/phase-2-20questions/game-spec.md` (oracle + corpus).
