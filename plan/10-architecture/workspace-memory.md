# 10.x — WORKSPACE (recursive memory subsystem)

> Phase 3 capability (ADR-0012), claim **X3** (recursive memory + explicit
> promotion). Origin: `SUPPLEMENTAL_IDEAS.md` ("a recursive memory sub-system so
> that we can store intermediate forms as their own graph… make memory a
> recursively addressable space of structured thought").

## The principle (P12)

**Memory is recursively addressable structure, not a bigger context window.**
Intermediate representations are *objects*: they can be stored, linked,
interrogated, revised, forked, or discarded — and they can contain other
workspaces.

A **WORKSPACE** is a bounded, named, lifetime-scoped container of thought:

```
WORKSPACE(id, parent: WORKSPACE | None, lifetime, label)
├── facts / interpretations        (IRs — Semantic IR instances)
├── hypotheses                     (unverified)
├── constraints
├── questions                      (open)
├── plans                          (candidate + selected)
├── results
├── exceptions                     (EXCEPTION-state markers)
├── references                     (SOURCE pointers, other IRs, child workspaces)
└── children: [WORKSPACE …]
```

- **Recursion:** any workspace may contain child workspaces (a document gets one
  child per chapter; a project gets one per sub-area). A child may hold everything
  its material needs; the parent only carries what survives abstraction across
  children. This is *hierarchical cognition* — and it is the answer to
  "analyze a 500-page document" without a 500-page context.
- **Queryability:** "what did we decide about transportation?" is a graph query
  over workspace IRs — never a reprocessing of the conversation that produced
  them.

## Lifetimes & promotion (explicit, never implicit)

```
EPHEMERAL → SESSION → PROJECT → LONG_TERM (CODEX)
```

Each workspace has exactly one `lifetime`. Content does **not** migrate
automatically:

- **Promote** is a deliberate operation: `workspace.promote(ir)` writes the IR's
  relationships into the CODEX as **candidate assertions with full provenance**
  (`source=workspace_<id>`, `observer=…`). They then pass the ordinary
  verification/consolidation path (Phase 2 learning loop) before `established`.
- **Nothing promotes implicitly.** An unreferenced workspace's content that was
  never promoted is absent from CODEX queries by construction (X3 test).
- Demotion/expiration: an expired workspace is dumped to `results/`-class storage
  (regenerable) or discarded; durable content survives only via promotion.

This is the concrete answer to "how does the system learn without corrupting
itself": working memory never writes truth; only verified, provenance-carrying
promotions do.

## Sources vs. analyses

A document does not *become* knowledge. `SOURCE` (uri, hash, version) is one
object; each analysis is a **versioned IR** referencing it:

```
SOURCE(DOC_1847)
├── ANALYSIS_v1 (IR)   ← chapter workspaces under it
├── ANALYSIS_v2 (IR)
└── …
```

"What did we conclude last time?" = query for the latest analysis IR. "Re-analyze
for contradictions with the current model" = **new workspace operation**, output
versioned `ANALYSIS_vN+1` — the previous analysis is never overwritten. If the
source changes (hash differs), derived knowledge is flagged stale (dependency
tracking via `DERIVED_FROM`).

## Sessions & nested contexts

- A **session** is a workspace with `lifetime=SESSION` — the built-in bounded
  context of one interaction/episode.
- **Nested contexts** solve local-vs-global truth: "keys → table" holds in
  `EVENT(home, 14:00)` without becoming globally true after 18:00; the unknown
  transition (`UNKNOWN_EVENT` with `caused: KEY_LOCATION_CHANGE`) is itself a
  structured IR, not an explanation the system must invent (ties into A5's
  contradiction handling and the validity-interval mechanics in `codex.md`).

## Where it lives / scope guards

- `src/kainos/workspace/` (directive 22). Persistence: workspaces are JSON
  (versioned IRs inside), so they ride the existing codec; the *long-term* side is
  always the CODEX.
- Phase 3 only. Phases 1–2 keep their current state models (game state, pipeline
  result); workspace is the generalization those de-facto patterns become.
- No external document ingestion in Phase 3 scope: SOURCE objects are exercised
  with local file sources (hash + tiny analysis IRs).
