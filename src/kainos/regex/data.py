"""Seed corpus access (P1.08) — the explicit form of the Phase 1 grammar.

The seed corpus is the only thing the deterministic kernel is "trained" on:
hand-authored descriptions, each with the byte-exact PCRE it must produce and
hand-authored examples that must (not) full-match it (ADR-0009 semantics).
"""

from __future__ import annotations

import json
from pathlib import Path

__all__ = ["load_corpus"]

_REQUIRED_KEYS = ("id", "description", "expected_pcre", "positive", "negative")


def load_corpus(path: str | Path) -> list[dict]:
    """Load a JSONL seed corpus; validates shape (keys, uniqueness, non-empty
    example lists) and raises ValueError (content) / TypeError (shape) on any
    defect."""

    records: list[dict] = []
    text = Path(path).read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"corpus line {lineno} is not valid JSON: {e}") from e
        missing = [k for k in _REQUIRED_KEYS if k not in rec]
        if missing:
            raise ValueError(f"corpus record {rec.get('id', f'line {lineno}')!r} is missing {missing}")
        if not isinstance(rec["positive"], list) or not isinstance(rec["negative"], list):
            raise TypeError(f"corpus record {rec['id']!r}: positive/negative must be lists")
        if not rec["positive"] or not rec["negative"]:
            raise ValueError(f"corpus record {rec['id']!r}: positive and negative must be non-empty")
        records.append(rec)
    ids = [r["id"] for r in records]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise ValueError(f"duplicate corpus record ids: {dupes}")
    return records
