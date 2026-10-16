"""The Phase 1 pipeline (P1.07) — describe → parse → resolve → emit → generate
→ judge, with a full audit trace.

Invariant: **never emit what you can't justify.** If resolution leaves any
reference unresolved, the pipeline returns an escalation
(`recommended_action: "ask_human"`) with NO pcre and NO verdict — it does not
guess.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from kainos.codex.memory import InMemoryCodexStore
from kainos.codex.store import CodexStore
from kainos.lang.deterministic import DeterministicKernel
from kainos.regex.emitter import emit
from kainos.regex.ir import Node, UnresolvedRef, to_ir
from kainos.regex.judge import Verdict, judge
from kainos.regex.lexicon import seed
from kainos.regex.resolver import SpecializationCache, resolve
from kainos.regex.testgen import generate

if TYPE_CHECKING:
    from kainos.lang.kernel import LanguageKernel

__all__ = ["PipelineResult", "default_codex", "describe"]


def default_codex() -> InMemoryCodexStore:
    """A fresh in-memory CODEX with the seeded Phase 1 lexicon (the deterministic
    default; pass an explicit store for a persistent one)."""

    store = InMemoryCodexStore()
    seed(store)
    return store


@dataclass
class PipelineResult:
    text: str
    ir: Node  # the resolved dialect tree
    resolved_trace: list[dict]
    pcre: str | None
    verdict: Verdict | None
    escalation: dict | None
    confidence: float
    parse_score: float = 1.0  # the interpreting kernel's score for its reading (P3.01 marking)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "ir": to_ir(self.ir),
            "resolved_trace": self.resolved_trace,
            "pcre": self.pcre,
            "verdict": None
            if self.verdict is None
            else {
                "ok": self.verdict.ok,
                "mismatches": self.verdict.mismatches,
                "compile_error": self.verdict.compile_error,
                "summary": self.verdict.summary(),
            },
            "escalation": self.escalation,
            "confidence": self.confidence,
            "parse_score": self.parse_score,
        }


def describe(
    text: str,
    codex: CodexStore | None = None,
    seed: int = 0,
    cache: SpecializationCache | None = None,
    kernel: LanguageKernel | None = None,
) -> PipelineResult:
    """The full pipeline for one description. Raises ValueError when the text is
    structurally unparseable (the parser, not the pipeline, is in the wrong).

    `kernel` (P3.01): any `LanguageKernel`; defaults to the deterministic one.
    The CODEX/reasoner/emitter downstream of the kernel is kernel-independent —
    that is what makes the E3.1 A/B isolate the kernel contribution."""

    store = codex if codex is not None else default_codex()
    if kernel is None:
        kernel = DeterministicKernel(store)
    interp = kernel.parse(text)[0]
    tree = interp.ir
    if not isinstance(tree, Node):
        raise TypeError(f"Phase 1 kernel must produce dialect nodes, got {type(tree)!r}")

    resolved, trace = resolve(tree, store, cache=cache)

    # Escalate instead of guessing: any surviving UnresolvedRef stops the pipeline.
    if _has_unresolved(resolved):
        candidates: list[str] = []
        for entry in trace:
            if entry.get("kind") != "ref" or entry.get("status") == "resolved":
                continue
            for c in entry.get("candidates", []):
                if isinstance(c, str) and c not in candidates:
                    candidates.append(c)
        escalation = {
            "status": "requires_context",
            "candidates": [c for c in candidates if c],
            "recommended_action": "ask_human",
        }
        return PipelineResult(
            text=text,
            ir=resolved,
            resolved_trace=trace,
            pcre=None,
            verdict=None,
            escalation=escalation,
            confidence=0.0,
            parse_score=interp.score,
        )

    pcre = emit(resolved)
    positives, negatives = generate(resolved, seed=seed)
    verdict = judge(pcre, positives, negatives)
    return PipelineResult(
        text=text,
        ir=resolved,
        resolved_trace=trace,
        pcre=pcre,
        verdict=verdict,
        escalation=None,
        confidence=_confidence(trace),
        parse_score=interp.score,
    )


def _has_unresolved(node: Node) -> bool:
    if isinstance(node, UnresolvedRef):
        return True
    from kainos.regex.ir import Alternative, Group, Repeat, Sequence

    if isinstance(node, Sequence):
        return any(_has_unresolved(el) for el in node.elements)
    if isinstance(node, Alternative):
        return any(_has_unresolved(b) for b in node.branches)
    if isinstance(node, (Repeat, Group)):
        return _has_unresolved(node.node)
    return False


def _confidence(trace: list[dict]) -> float:
    """Verified points / total points, where a point is a Class verification or a
    reference that was rotated. A fully-verified pattern is 1.0; a pattern of
    pure literals/anchors (nothing to verify against the CODEX) is 1.0 — there
    is nothing to be unjustified about it."""

    points = [e for e in trace if e.get("kind") in ("class", "ref")]
    if not points:
        return 1.0
    verified = [
        e
        for e in points
        if (e.get("kind") == "class" and e.get("assertion_id") is not None)
        or (e.get("kind") == "ref" and e.get("status") == "resolved")
    ]
    return len(verified) / len(points)
