r"""PCRE judge (P1.07, ADR-0009) — the objective arbiter.

`judge()` does NOT use Python `re`. It invokes the Perl judge script (the
canonical engine), which compiles the pattern and full-matches each example
(`\A(?:pattern)\z`), returning a JSON verdict. "Correct" therefore means
"matches the intended language under the canonical engine", not "looks
plausible".

The script ships with the package (src/kainos/regex/judge.pl — pinned data,
ADR-0001/0010); a local scripts/judge.pl, if present, takes precedence.
Protocol: pattern as argv[1]; TSV lines `1<TAB>example` / `0<TAB>example`
(expected match?) on stdin; JSON `{ok, mismatches, compile_error}` on stdout
— perl-base ships in the pinned image, and nothing is installed on the host.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# The judge script ships in-package (ADR-0009: the regex engine is Perl; the
# script is pinned data next to the code, not a host installation). A local
# scripts/judge.pl, if present, takes precedence (convenience override).
_JUDGE_SCRIPT_CANDIDATES = (Path(__file__).resolve().parent.parent.parent.parent / "scripts" / "judge.pl",
                           Path(__file__).resolve().parent / "judge.pl")


def _judge_script() -> Path:
    for candidate in _JUDGE_SCRIPT_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("perl judge script missing (expected src/kainos/regex/judge.pl)")

__all__ = ["Verdict", "judge"]

_JUDGE_TIMEOUT = 10.0


@dataclass
class Verdict:
    """Judge outcome for one pattern over one example set.

    `mismatches` entries: {"text", "expected", "got", "note"} — the
    human-readable diff of every misjudged example (including a
    `compile_error` note when the pattern itself failed to compile).
    """

    ok: bool
    mismatches: list[dict] = field(default_factory=list)
    compile_error: str | None = None

    def summary(self) -> str:
        if self.compile_error and not self.mismatches:
            return f"FAIL: pattern did not compile ({self.compile_error})"
        if self.ok:
            return "PASS: full-match on every positive, no match on every negative"
        bad = "; ".join(f'{m["text"]!r}: {m["note"]}' for m in self.mismatches[:3])
        more = f" (+{len(self.mismatches) - 3} more)" if len(self.mismatches) > 3 else ""
        return f"FAIL: {bad}{more}"


def judge(pcre: str, positive: list[str], negative: list[str]) -> Verdict:
    """Full-match every example with the Perl judge; return the verdict."""

    script = _judge_script()
    lines = "".join(f"1\t{t}\n" for t in positive) + "".join(f"0\t{t}\n" for t in negative)
    try:
        res = subprocess.run(
            ["perl", str(script), pcre],
            input=lines,
            capture_output=True,
            text=True,
            timeout=_JUDGE_TIMEOUT,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return Verdict(ok=False, mismatches=[], compile_error=f"judge unavailable: {e}")
    if res.returncode != 0:
        detail = (res.stderr or "").strip()[:200]
        return Verdict(ok=False, mismatches=[], compile_error=f"judge failed (rc={res.returncode}): {detail}")
    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError as e:
        return Verdict(ok=False, mismatches=[], compile_error=f"judge output is not JSON: {e}")
    return Verdict(
        ok=bool(data.get("ok")),
        mismatches=list(data.get("mismatches", [])),
        compile_error=data.get("compile_error"),
    )
