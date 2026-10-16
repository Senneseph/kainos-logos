"""Train / predict CLI for Model A (E1.5 baseline).

Directive paths `scripts/train_baseline.py` / `scripts/predict.py`:
`scripts/` is gitignored (user-managed, never modified), so the same logic
lives in-package — reachable as `kainos modela train` and
`kainos modela predict "..."`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kainos.llm.model_a import (
    ModelA,
    ModelAConfig,
    file_hash,
    load_default_model,
)
from kainos.regex.bench import default_corpus_path
from kainos.regex.data import load_corpus

__all__ = ["TRAIN_META", "WEIGHTS_PATH", "predict_model_a", "train_model_a"]

WEIGHTS_PATH = Path("data/models/model_a.pt")
# The pinned training recipe (recorded in the artifact + E1.5 config):
TRAIN_META: dict[str, Any] = {
    "trained_on": "data/regex/seed_corpus.jsonl (55 records, descriptions -> expected_pcre)",
    "held_out": "compositional_set.jsonl / holdout_set.jsonl are NEVER seen during training",
    "epochs": 200,
    "batch": 8,
    "lr": 1e-3,
    "seed": 42,
    "config": ModelAConfig().to_dict(),
    "determinism": "torch seed + seeded shuffle; single-threaded CPU ops",
}


def train_model_a(out_path: str | Path = WEIGHTS_PATH, epochs: int | None = None) -> dict:
    """Train Model A on the seed corpus only and write the artifact."""

    import torch

    # Single thread => deterministic CPU ops (the artifact is committed).
    old = torch.get_num_threads()
    torch.set_num_threads(1)
    try:
        # Seed BEFORE construction: nn weight init draws from the global RNG,
        # so a full retrain under the pinned seed reproduces the artifact.
        torch.manual_seed(TRAIN_META["seed"] if isinstance(TRAIN_META["seed"], int) else 42)
        records = load_corpus(default_corpus_path())
        pairs = [(r["description"], r["expected_pcre"]) for r in records]
        vocab = ModelA.build_vocab([t for pair in pairs for t in pair])
        model = ModelA(vocab, ModelAConfig())
        history = model.train(pairs, epochs=int(TRAIN_META["epochs"]) if epochs is None else epochs)
        path = Path(out_path)
        model.save(path, meta={**TRAIN_META, "epochs_run": len(history), "final_loss": history[-1]})
    finally:
        torch.set_num_threads(old)
    return {
        "weights": str(path),
        "weights_sha256": file_hash(path),
        "n_pairs": len(pairs),
        "vocab_size": len(vocab),
        "first_loss": history[0],
        "final_loss": history[-1],
        "epochs": len(history),
    }


def predict_model_a(text: str, weights_path: str | Path | None = None) -> dict:
    """One inference on the committed artifact. Model A never abstains."""

    import torch

    old = torch.get_num_threads()
    torch.set_num_threads(1)
    try:
        if weights_path is None:
            model = load_default_model()
            path = "data/models/model_a.pt (committed)"
        else:
            model = ModelA.load(weights_path)
            path = str(weights_path)
        return {"description": text, "pcre": model.predict(text), "weights": path}
    finally:
        torch.set_num_threads(old)


def main(argv: list[str] | None = None) -> int:
    import sys

    argv = argv if argv is not None else sys.argv[1:]
    if not argv or argv[0] == "train":
        report = train_model_a()
        print(json.dumps(report, indent=1))
        return 0
    if argv[0] == "predict" and len(argv) >= 2:
        print(json.dumps(predict_model_a(" ".join(argv[1:])), indent=1))
        return 0
    print("usage: kainos modela train | kainos modela predict \"description\"")
    return 1
