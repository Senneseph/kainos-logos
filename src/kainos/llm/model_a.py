"""Model A — the no-CODEX conventional baseline for E1.5 (step 12).

A small char-level transformer seq2seq, English description -> PCRE, trained
on the **seed corpus only** (the compositional/holdout sets are never seen).
It has no CODEX path, no resolver, no judge: if it emits a wrong pattern, it
emits a wrong pattern. That is exactly what the A/B compares.

Deliberately tiny (dim 96, 2+2 layers): the claim under test is that
*architecture* (CODEX pipeline vs. next-token model) beats *scale* on unseen
combinations — a small model makes the comparison clean, not a contest of
compute.

Determinism: training and inference run with a single torch thread and a
seeded RNG, so a retrain with the pinned seed/epochs reproduces the committed
artifact (tests/llm/test_model_a.py pins smoke-level reproducibility; the
full retrain check is gated behind KAINOS_SLOW=1).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from torch import nn

__all__ = ["ModelA", "ModelAConfig", "default_weights_path", "load_default_model"]

PAD, BOS, EOS = 0, 1, 2


@dataclass(frozen=True)
class ModelAConfig:
    dim: int = 96
    nhead: int = 4
    enc_layers: int = 2
    dec_layers: int = 2
    dim_ff: int = 192
    max_src: int = 96
    max_tgt: int = 64
    dropout: float = 0.1

    def to_dict(self) -> dict[str, Any]:
        return {
            "dim": self.dim,
            "nhead": self.nhead,
            "enc_layers": self.enc_layers,
            "dec_layers": self.dec_layers,
            "dim_ff": self.dim_ff,
            "max_src": self.max_src,
            "max_tgt": self.max_tgt,
            "dropout": self.dropout,
        }


class _Seq2Seq(nn.Module):
    def __init__(self, vocab: int, cfg: ModelAConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.embedding = nn.Embedding(vocab, cfg.dim, padding_idx=PAD)
        self.pos_src = nn.Embedding(cfg.max_src, cfg.dim)
        self.pos_tgt = nn.Embedding(cfg.max_tgt + 3, cfg.dim)
        enc = nn.TransformerEncoderLayer(
            d_model=cfg.dim, nhead=cfg.nhead, dim_feedforward=cfg.dim_ff,
            dropout=cfg.dropout, batch_first=True,
        )
        dec = nn.TransformerDecoderLayer(
            d_model=cfg.dim, nhead=cfg.nhead, dim_feedforward=cfg.dim_ff,
            dropout=cfg.dropout, batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(enc, num_layers=cfg.enc_layers)
        self.decoder = nn.TransformerDecoder(dec, num_layers=cfg.dec_layers)
        self.out = nn.Linear(cfg.dim, vocab)

    def _pad(self, ids: list[int], limit: int) -> torch.Tensor:
        ids = ids[:limit]
        ids = [BOS] + ids + [EOS]
        if len(ids) > limit + 2:
            ids = ids[: limit + 2]
        ids = ids + [PAD] * max(0, limit + 2 - len(ids))
        return torch.tensor([ids], dtype=torch.long)

    def forward(
        self, src: torch.Tensor, tgt: torch.Tensor, src_mask: torch.Tensor, tgt_mask: torch.Tensor
    ) -> torch.Tensor:
        mem = self.encoder(self.embedding(src), src_key_padding_mask=src_mask)
        tgt_emb = self.embedding(tgt) + self.pos_tgt(torch.arange(tgt.size(1), device=tgt.device))
        out = self.decoder(tgt_emb, mem, tgt_key_padding_mask=tgt_mask, memory_key_padding_mask=src_mask)
        return self.out(out)


class ModelA:
    """Char-level seq2seq with a (de)re-serializable vocabulary."""

    def __init__(self, vocab: list[str], cfg: ModelAConfig, model: _Seq2Seq | None = None) -> None:
        self.vocab = vocab
        self.cfg = cfg
        self.char2id = {c: i for i, c in enumerate(vocab)}
        self._model = model if model is not None else _Seq2Seq(len(vocab), cfg)
        self._meta: dict[str, Any] = {}

    # ── vocab ───────────────────────────────────────────────────────────────

    @staticmethod
    def build_vocab(tensors: list[str]) -> list[str]:
        chars = sorted({c for t in tensors for c in t if c.isprintable()})
        return ["<pad>", "<s>", "</s>"] + chars

    # ── (de)serialization ───────────────────────────────────────────────────

    def _text_ids(self, text: str, limit: int) -> list[int]:
        """Char ids for `text` (unmappable chars dropped, truncated to limit)."""

        return [self.char2id[c] for c in text if c in self.char2id][:limit]

    def _src_ids(self, text: str) -> list[int]:
        ids = [BOS] + self._text_ids(text, self.cfg.max_src)
        return ids + [PAD] * max(0, self.cfg.max_src + 2 - len(ids))

    def _tgt_pair(self, pcre: str) -> tuple[list[int], list[int]]:
        """(decoder input, decoder target) for a PCRE: input BOS-prefixed, target
        EOS-prefixed (shifted by one), both padded to max_tgt(+1)."""

        plain = self._text_ids(pcre, self.cfg.max_tgt)
        tgt_in = ([BOS] + plain) + [PAD] * (self.cfg.max_tgt - len(plain))
        tgt_out = ([EOS] + plain) + [PAD] * (self.cfg.max_tgt - len(plain))
        return tgt_in, tgt_out

    def save(self, path: str | Path, meta: dict[str, Any] | None = None) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "vocab": self.vocab,
                "config": self.cfg.to_dict(),
                "state": self._model.state_dict(),
                "meta": meta or {},
            },
            path,
            _use_new_zipfile_serialization=True,
        )

    @classmethod
    def load(cls, path: str | Path) -> ModelA:
        blob = torch.load(path, map_location="cpu", weights_only=False)
        cfg = ModelAConfig(**blob["config"])
        model = _Seq2Seq(len(blob["vocab"]), cfg)
        model.load_state_dict(blob["state"])
        out = cls(list(blob["vocab"]), cfg, model)
        out._meta = dict(blob.get("meta") or {})
        return out

    @property
    def meta(self) -> dict[str, Any]:
        return self._meta

    # ── training ───────────────────────────────────────────────────────────

    def train(
        self,
        pairs: list[tuple[str, str]],
        epochs: int = 200,
        batch: int = 8,
        lr: float = 1e-3,
        seed: int = 42,
    ) -> list[float]:
        """Teacher-forced training on (description, pcre) pairs. Returns the
        per-epoch loss history. Deterministic under the pinned seed."""

        for _ in range(2):
            torch.manual_seed(seed)
        gen = torch.Generator().manual_seed(seed)
        self._model.train()
        opt = torch.optim.Adam(self._model.parameters(), lr=lr)
        history: list[float] = []
        n = len(pairs)
        for epoch in range(epochs):
            order = torch.randperm(n, generator=gen).tolist()
            total, seen = 0.0, 0
            for b0 in range(0, n, batch):
                for i in order[b0 : b0 + batch]:
                    src, tgt_text = pairs[i]
                    src_ids = self._src_ids(src)
                    tgt_in, tgt_out = self._tgt_pair(tgt_text)
                    src_t = torch.tensor([src_ids], dtype=torch.long)
                    tgt_in_t = torch.tensor([tgt_in], dtype=torch.long)
                    tgt_out_t = torch.tensor([tgt_out], dtype=torch.long)
                    logits = self._model(src_t, tgt_in_t, src_t == PAD, tgt_in_t == PAD)
                    loss = nn.functional.cross_entropy(
                        logits[0, 1:, :].reshape(-1, len(self.vocab)),
                        tgt_out_t[0, 1:].reshape(-1),
                        ignore_index=PAD,
                    )
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
                    total += loss.item()
                    seen += 1
            history.append(total / max(seen, 1))
        self._model.eval()
        return history

    # ── inference ───────────────────────────────────────────────────────────

    def predict(self, text: str) -> str:
        """Greedy decode: English description -> PCRE string (never raises on
        content; an LLM-like baseline simply always produces *some* output)."""

        self._model.eval()
        src_ids = self._src_ids(text)
        src_t = torch.tensor([src_ids], dtype=torch.long)
        with torch.no_grad():
            generated = [BOS]
            for _ in range(self.cfg.max_tgt):
                tgt_in = generated + [PAD] * max(0, self.cfg.max_tgt + 1 - len(generated))
                tgt_in_t = torch.tensor([tgt_in], dtype=torch.long)
                logits = self._model(src_t, tgt_in_t, src_t == PAD, tgt_in_t == PAD)
                nxt = int(torch.argmax(logits[0, -1, :]).item())
                if nxt == EOS or nxt == PAD:
                    break
                generated.append(nxt)
        id2char = {i: c for c, i in self.char2id.items() if i not in (PAD, BOS, EOS)}
        out = "".join(id2char[i] for i in generated if i in id2char)
        return out.strip()


def default_weights_path() -> Path:
    """The committed trained artifact: `data/models/model_a.pt` (CWD, then
    the checkout containing this package)."""

    here = Path(__file__).resolve()
    candidates = (
        Path("data/models/model_a.pt"),
        here.parents[3] / "data/models/model_a.pt",
    )
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("model_a.pt not found (run: kainos modela train)")


def load_default_model() -> ModelA:
    return ModelA.load(default_weights_path())


def file_hash(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
