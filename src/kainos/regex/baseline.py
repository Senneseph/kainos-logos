r"""DirectBaseline (P1.11) — the no-CODEX "Model A" stand-in for E1.2.

A conventional system's best effort without the CODEX: the deterministic
kernel parsing to the dialect tree, then the emitter — with **no resolver,
no CODEX lookup**. Class identities (digit → `\d`, …) are the dialect's own
semantic identities (they ride on the Class node, not on any stored fact); a
bare content word (the lexicon's `hyphen`) has no resolution path and stays an
`UnresolvedRef`, which the emitter refuses to emit. Whatever the grammar
itself cannot surface is a failure — exactly the gap the CODEX fills, and the
contribution E1.2 is measuring (the LLM A/B is step 12, a different model).
"""

from __future__ import annotations

from dataclasses import dataclass

from kainos.lang.deterministic import DeterministicKernel
from kainos.regex.emitter import UnresolvedError, emit
from kainos.regex.ir import Node

__all__ = ["BaselineResult", "DirectBaseline"]


@dataclass(frozen=True)
class BaselineResult:
    """One baseline solve: `pcre` is None on failure (unparseable text or an
    UnresolvedRef the no-CODEX pipeline cannot discharge); `note` names the
    failing surface when there is one."""

    pcre: str | None
    note: str = ""


class DirectBaseline:
    """Kernel → emitter, no CODEX. Deterministic; no stored knowledge."""

    def __init__(self) -> None:
        self._kernel = DeterministicKernel(codex=None)

    def solve(self, text: str) -> BaselineResult:
        try:
            tree = self._kernel.parse(text)[0].ir
        except ValueError as e:
            return BaselineResult(pcre=None, note=f"unparseable: {e}")
        if not isinstance(tree, Node):
            return BaselineResult(pcre=None, note=f"not a dialect node: {type(tree)!r}")
        try:
            return BaselineResult(pcre=emit(tree))
        except UnresolvedError as e:
            return BaselineResult(pcre=None, note=str(e))
