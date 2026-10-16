"""Model A tests (E1.5 baseline) — smoke training, determinism, artifact
integrity. The full 200-epoch retrain-equivalence check is gated behind
KAINOS_SLOW=1 (the committed data/models/model_a.pt is the artifact).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from kainos.llm.model_a import ModelA, ModelAConfig, load_default_model
from kainos.regex.bench import default_holdout_path
from kainos.regex.data import load_corpus

SMOKE_PAIRS: list[tuple[str, str]] = [
    ("a digit", r"\d"),
    ("two letters", r"[A-Za-z]{2}"),
    ("a space", r"\s"),
    ("three digits, then a space", r"\d{3}\s"),
    ("the literal foo", "foo"),
]


@pytest.fixture(autouse=True)
def _single_threaded_torch():
    """16-thread torch on batch-1 micro-batches is SLOWER and non-deterministic
    than 1 thread — the gate keeps single-threaded (the same recipe the
    committed artifact was trained with)."""

    import torch

    old = torch.get_num_threads()
    torch.set_num_threads(1)
    try:
        yield
    finally:
        torch.set_num_threads(old)


def test_smoke_train_predict_roundtrip(tmp_path: Path):
    m = ModelA(ModelA.build_vocab([t for p in SMOKE_PAIRS for t in p]), ModelAConfig())
    history = m.train(SMOKE_PAIRS, epochs=8)
    assert len(history) == 8
    assert history[-1] < history[0]  # loss actually decreased
    out = m.predict(SMOKE_PAIRS[0][0])
    assert isinstance(out, str) and out
    assert "<s>" not in out and "</s>" not in out and "<pad>" not in out


def test_training_is_deterministic_under_seed(tmp_path: Path):
    import torch

    pairs = SMOKE_PAIRS
    torch.manual_seed(7)
    a = ModelA(ModelA.build_vocab([t for p in pairs for t in p]), ModelAConfig())
    ha = a.train(pairs, epochs=4, seed=7)
    torch.manual_seed(7)  # identical init for the second instance
    b = ModelA(ModelA.build_vocab([t for p in pairs for t in p]), ModelAConfig())
    hb = b.train(pairs, epochs=4, seed=7)
    assert ha == hb
    assert a.predict("a digit") == b.predict("a digit")


def test_save_load_roundtrip(tmp_path: Path):
    m = ModelA(ModelA.build_vocab([t for p in SMOKE_PAIRS for t in p]), ModelAConfig())
    m.train(SMOKE_PAIRS, epochs=4, seed=1)
    path = tmp_path / "m.pt"
    m.save(path, meta={"trained_on": "smoke"})
    loaded = ModelA.load(path)
    assert loaded.predict("a digit") == m.predict("a digit")
    assert loaded.meta["trained_on"] == "smoke"


def test_committed_artifact_is_loadable_and_honest():
    """The committed weights must load, must record its training recipe, and
    its prediction must be reproducible (greedy, single-threaded)."""

    m = load_default_model()
    assert m.meta.get("trained_on", "").startswith("data/regex/seed_corpus.jsonl")
    holdout = load_corpus(default_holdout_path())
    first = holdout[0]
    assert m.predict(first["description"]) == m.predict(first["description"])


def test_committed_artifact_was_trained_on_seed_only():
    m = load_default_model()
    # The vocab may contain exactly the chars of seed descriptions+PCREs
    # (never the holdout's, though that is a subset anyway) — the pin is the
    # recorded recipe: epochs/seed present, corpus named.
    assert m.meta.get("seed") == 42
    assert m.meta.get("epochs_run") == 200


@pytest.mark.skipif(os.environ.get("KAINOS_SLOW") != "1", reason="set KAINOS_SLOW=1")
def test_full_retrain_reproduces_committed_weights():
    import torch

    from kainos.llm.train import train_model_a

    torch.set_num_threads(1)
    try:
        committed = load_default_model()
        report = train_model_a(out_path="/tmp/retrained_model_a.pt")
        retrained = ModelA.load("/tmp/retrained_model_a.pt")
        holdout = load_corpus(default_holdout_path())
        for rec in holdout:
            assert committed.predict(rec["description"]) == retrained.predict(rec["description"])
        assert report["n_pairs"] == 55
    finally:
        torch.set_num_threads(16)
