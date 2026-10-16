**Signed by:** step 20 / action P3.11 — fills `plan/30-phases/phase-3-generalization/results.md`.
*Runs LAST — after directives 21 and 22 (ordering exception, see epic).*

The project is signed off when **all five** Phase 3 exit criteria are met:

1. **E3.1–E3.7 run green and are reported.**
2. The **multi-modal demo (E3.4)** resolves one abstract pattern across two
   modalities.
3. The **2-node reconciliation demo (E3.3)** produces a higher-order TERM.
4. **φ/Fibonacci results are reported as *adopt or reject***, never silently
   merged.
5. `plan/30-phases/phase-3-generalization/results.md` **consolidates all phases**
   and states, in one table, whether the unifying claim survived (plus
   `results/phase-3/SUMMARY.md` rendered by the harness).

**The eight "full-realized" acceptance checks** (each must map to an evidence
artifact):

1. accepts any of ≥2 modalities (text + one synthetic non-text modality) into the
   same CODEX;
2. learns continuously without retraining the neural kernel;
3. expands its own ontology when contradictions reveal missing dimensions;
4. synchronizes knowledge across ≥2 nodes via assertion deltas;
5. abstains/asks at its knowledge boundary;
6. exposes an inspectable trace for every conclusion;
7. plans only over declared capabilities — an unachievable goal yields **NO VALID
   PLAN** with the named gap + nearest viable plan, never a fabricated action
   (**X1**);
8. keeps memory recursively addressable — workspaces nest, "what did we decide?"
   is a graph query, and nothing reaches the CODEX without explicit promotion
   (**X3**).

**North-star criteria** (`plan/00-north-star.md`) — each needs end-to-end
evidence across phases: persistent memory (**C2**) · compositionality (**C1**) ·
honest uncertainty (**C3**) · inspectability (every experiment's evidence chain) ·
compounding (reuse stats per phase).

**Kill criterion:** **K4 (gated)** — φ/Fibonacci numerics/topology must win a
benchmark with a margin or be recorded **reject** (ADR-0006).

**Final verdict question** (`plan/90-appendices/research-questions.md`): *Can the
system discover an abstraction that its designer did not explicitly put into the
ontology?* If yes, we crossed the boundary from "fills slots in a predefined
framework" to "expands the space in which it reasons." That is the whole point.
