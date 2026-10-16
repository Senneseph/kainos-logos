# 30 — Phases

Each phase folder contains:

- `README.md` — goal, scope, **exit criteria** (the sign-off checklist).
- `actions.md` — the phase's action IDs (`P*.NN`) mapped to `../../action-steps/` files.
- Spec/experiment docs — the normative tables (grammar, metrics, thresholds) that the
  directives cite.
- `results.md` — the *committed* sign-off. Templates ship here; the phase's final
  action step fills them in. (Durability rule 2 in
  `../../action-steps/LAYOUT.md`: `results/` outputs are regenerable; the finding's
  permanent home is this `results.md`.)

| Phase | Folder | Claim tested | First step |
|-------|--------|--------------|------------|
| 0 Foundation | [`phase-0-foundation/`](phase-0-foundation/README.md) | The substrate is sound, versioned, inspectable | `01-scaffold.md` |
| 1 Regex | [`phase-1-regex/`](phase-1-regex/README.md) | Compositional generation + persistent memory + honest uncertainty from IR+CODEX | `06-regex-ir-emitter.md` |
| 2 20 Questions | [`phase-2-20questions/`](phase-2-20questions/README.md) | Active acquisition; EXCEPTION shrinkage; persistent growth | `13-q20-corpus-oracle.md` |
| 3 Generalization | [`phase-3-generalization/`](phase-3-generalization/README.md) | The same algebra generalizes (LLM kernel, distribution, φ numerics, modalities) | `17-llm-kernel.md` |

Phase exit criteria are in each phase README; the cross-phase "compounding contract"
(claim → artifact → test) is in [`../20-roadmap.md`](../20-roadmap.md).
