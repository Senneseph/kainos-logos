"""LLMKernel (P1.14, productionized in P3.01) — a conventional next-token model
behind the SAME `LanguageKernel` protocol as the deterministic kernel (invariant
#2: the kernel is an organ; this seam is where a neural one plugs in).

The LLM is the PARSER only: `parse(text)` prompts it to emit the dialect AST
as a generic IR JSON document, which is validated (schema + from_ir) before
anyone trusts it; one self-correction retry on an invalid document. `realize()`
and `propose()` stay deterministic (emitter / no proposals) — justification is
the CODEX pipeline's job, not the model's.

Deterministic fallback (P3.01): if the backend fails (timeout / connection /
no valid document after the retry) the kernel returns its configured fallback
kernel's reading with a LOWERED score instead of losing the interpretation;
without a fallback the error propagates.

Runtime (owner's direction, 2026-08-20 — supersedes the llama-server/GGUF pin
in reality-check §5): a LOCAL Ollama server on the LAN, model from the
`OLLAMA_MODEL` env (the pinned snapshot is recorded in experiment configs).
The server's custom `/v1` proxy is flaky (request-body quirks) and the model
is a thinking model, so the client uses the NATIVE `/api/chat` with
`think: false` and `format: "json"`. No hosted APIs.

Prompt v2 (P3.01): the step-12 prompt encoded the deterministic grammar's
vocabulary verbatim — correct for the in-grammar seed corpus, but wrong for
STEP 17's open phrasing, where descriptions use synonyms/idioms the grammar
doesn't spell out. v2 keeps the dialect contract (types, relationships,
vocabulary classes — unchanged) and adds an explicit instruction to MAP
open phrasing onto the dialect with general language understanding, so
"word characters" -> word class, "alphanumeric" -> Alternative(letter, digit).
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

import jsonschema  # type: ignore[import-untyped]  # no py.typed shipped; stubs would need a lockfile pin

from kainos.lang.kernel import Interpretation
from kainos.regex.emitter import emit
from kainos.regex.ir import Node, from_ir

if TYPE_CHECKING:
    from kainos.lang.kernel import LanguageKernel

__all__ = ["Backend", "LLMKernel", "MockBackend", "OllamaBackend", "build_ast_prompt"]


@runtime_checkable
class Backend(Protocol):
    """One completion: messages -> assistant text. Deterministic at temperature 0."""

    def complete(self, messages: list[dict[str, str]]) -> str: ...


class MockBackend:
    """Test backend: canned replies served in call order (last one repeats)."""

    def __init__(self, replies: list[str]) -> None:
        self.replies = list(replies)
        self.calls: list[list[dict[str, str]]] = []

    def complete(self, messages: list[dict[str, str]]) -> str:
        i = len(self.calls)
        self.calls.append(messages)
        return self.replies[min(i, len(self.replies) - 1)]


def _env(name: str) -> str:
    """Env value with shell-style quoting stripped (.env lines are quoted)."""

    return os.environ.get(name, "").strip().strip('"').strip("'")


class OllamaBackend:
    """Native `/api/chat` client for the owner's local Ollama server (LAN,
    offline). `endpoint` may point at the OpenAI-compatible `/v1` URL (kept
    for .env compatibility) — the native API base is derived by stripping it."""

    def __init__(
        self,
        endpoint: str | None = None,
        model: str | None = None,
        timeout: float = 600.0,
        max_tokens: int = 2048,
        temp: float = 0.0,
    ) -> None:
        ep = endpoint if endpoint is not None else _env("OLLAMA_ENDPOINT")
        if not ep:
            raise ValueError("OLLAMA_ENDPOINT not set (owner's .env)")
        self.base = ep.strip().strip('"').rstrip("/").removesuffix("/v1").rstrip("/")
        self.model = model if model is not None else _env("OLLAMA_MODEL")
        if not self.model:
            raise ValueError("OLLAMA_MODEL not set (owner's .env)")
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.temp = temp

    def complete(self, messages: list[dict[str, str]]) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "think": False,  # thinking models: disable the scratchpad
                "format": "json",  # JSON discipline for the AST document
                "options": {"temperature": self.temp, "num_predict": self.max_tokens},
            }
        ).encode()
        req = urllib.request.Request(
            f"{self.base}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.load(resp)
        content = data["message"]["content"]
        if data.get("done_reason") not in (None, "stop"):
            raise ValueError(f"model stopped early (done_reason={data.get('done_reason')!r})")
        return content

    def server_info(self) -> dict[str, Any]:
        """The pinned snapshot record: model id, architecture, size, params."""

        body = json.dumps({"name": self.model}).encode()
        req = urllib.request.Request(
            f"{self.base}/api/show",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.load(resp)
        mi = data.get("model_info", {})
        details = data.get("details", {})
        return {
            "model": self.model,
            "endpoint": self.base,
            "architecture": mi.get("general.architecture"),
            "parameter_count": details.get("parameter_size") or mi.get("general.parameter_count"),
            "quant_type": mi.get("general.file_type"),
            "modified_at": data.get("modified_at"),
        }

    def ping(self) -> list[str]:
        """Cheap reachability probe (P3.01): GET /api/tags -> the model names
        the server knows. Raises OSError/urllib.error when unreachable — the
        E3.1 experiment uses it to skip instead of hang when the LAN server is
        down, and to record the pinned model in the run config."""

        req = urllib.request.Request(f"{self.base}/api/tags")
        with urllib.request.urlopen(req, timeout=min(self.timeout, 10.0)) as resp:
            data = json.load(resp)
        return [m.get("name", "") for m in data.get("models", [])]


def build_ast_prompt(text: str) -> list[dict[str, str]]:
    """The system/user messages asking for the dialect AST as generic IR JSON
    (the shape to_ir() produces — verified byte-level against the codec)."""

    system = (
        "You translate a restricted-English regex description into the Kainos regex "
        "dialect AST, expressed as a GENERIC IR JSON document. Respond with ONLY the "
        "JSON document (no prose, no markdown).\n\n"
        "Document shape: {\"kind\": \"pattern\", \"entities\": [...], \"relationships\": "
        "[...], optionally \"unresolved\": [...], \"meta\": {\"dialect\": \"kainos/regex/1\"}}.\n\n"
        "Entities are {\"id\": \"e0\", \"type\": T} (optionally \"labels\": [...]), with ids "
        "e0, e1, ... assigned in PRE-ORDER of the AST (the root is e0, then depth-first "
        "children in order). Types and labels:\n"
        "- Sequence: {} (children via 'sequence' relationships).\n"
        "- Alternative: {} (branches via 'alternative_branch' relationships).\n"
        "- Repeat: {} (child via a 'repeat' relationship).\n"
        "- Group: {} (child via a 'group' relationship).\n"
        "- Class: labels [K] where K is one of digit|letter|word|whitespace|any.\n"
        "- Anchor: labels [A] where A is one of start|end.\n"
        "- Flag: labels [\"case_insensitive\"].\n"
        "- Literal: labels [\"<text>\"].\n\n"
        "Vagueness: a word the description does not define (not in the vocabulary "
        "below) goes into the \"unresolved\" array as {\"id\": \"u0\", \"surface\": "
        "\"<word or phrase>\", \"candidates\": [\"<plausible term id>\", ...]} (ids u0, "
        "u1, ...) and is referenced like an entity from a relationship. Do NOT invent "
        "characters for such words; do NOT use 'unresolved' for vocabulary words.\n\n"
        "Relationships are {\"subject\": \"<id>\", \"relation\": R, \"object\": \"<id>\", "
        "\"context\": C} with R one of: \"sequence\" (C = {\"position\": <int>}), "
        "\"alternative_branch\" (C = {\"branch\": <int>}), \"group\" (C = {}), \"flag\" "
        "(C = {\"position\": <int>}), \"repeat\" (C = the quantifier). The quantifier in "
        "C is one of: {\"kind\": \"one_or_more\"}, {\"kind\": \"zero_or_more\"}, "
        "{\"kind\": \"optional\"}, {\"kind\": \"exactly\", \"n\": <int>}, "
        "{\"kind\": \"at_least\", \"n\": <int>}, {\"kind\": \"at_most\", \"n\": <int>}, "
        "{\"kind\": \"between\", \"a\": <int>, \"b\": <int>}. Exactly one entity (or "
        "unresolved entry) is the root: the single id that no relationship points to.\n\n"
        "Vocabulary (the ONLY words you may define): anchors: 'beginning of string', "
        "'start of string' (start) and 'end of string' (end); flag: 'ignoring case'; "
        "literals: 'the literal <text>' (text runs to the next connector); classes: "
        "digit/digits, letter/letters, word/words, whitespace/space/spaces, any/anything; "
        "quantifiers: one or more, zero or more, optional/optionally/maybe, exactly <n>, "
        "at least <n>, at most <n>, between <n> and <m>; numbers: number 5 (literal), "
        "number one (unresolved: ambiguous); structure: 'a group of ...', 'either A or B'; "
        "connectors: ',' 'then' 'and' 'followed by'. Everything else is a CODEX term -> "
        "unresolved.\n\n"
        "Open phrasing: the description may use SYNONYMS AND IDIOMS not in the "
        "vocabulary. MAP them onto the dialect with general language understanding, "
        "keeping the dialect contract: 'word characters' is the word class; a "
        "'string of X' / 'run of X' / 'stuff that is X' usually means a Repeat of X "
        "(one or more, unless it says 'zero or more' / 'as many as you want', then "
        "'at least two of them' means at_least n=2; 'alphanumeric' is ONE OR MORE of "
        "(letter OR digit), an Alternative of the two classes. Compose the dialect; "
        "never invent characters or new class labels. 'The tail of the string' / "
        "'the end' is the end anchor; 'some whitespace padding' is a repeat of "
        "the whitespace class. Use \"unresolved\" ONLY for a term you truly cannot "
        "map to the dialect (then offer candidates); do not mark idiom words unresolved.\n\n"

        "Example — 'three digits, then a hyphen':\n"
        '{"kind": "pattern", '
        '"entities": [{"id": "e0", "type": "Sequence"}, {"id": "e1", "type": "Repeat"}, '
        '{"id": "e2", "type": "Class", "labels": ["digit"]}], '
        '"relationships": '
        '[{"subject": "e1", "relation": "repeat", "object": "e2", "context": {"kind": "exactly", "n": 3}}, '
        '{"subject": "e0", "relation": "sequence", "object": "e1", "context": {"position": 0}}, '
        '{"subject": "e0", "relation": "sequence", "object": "u0", "context": {"position": 1}}], '
        '"unresolved": [{"id": "u0", "surface": "hyphen", "candidates": ["hyphen"]}], '
        '"meta": {"dialect": "kainos/regex/1"}}'
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": text},
    ]


_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = _FENCE_RE.sub("", text).strip()
    if not cleaned.startswith("{"):
        start = cleaned.find("{")
        if start < 0:
            raise ValueError("model returned no JSON object")
        cleaned = cleaned[start :]
    return json.loads(cleaned)


class LLMKernel:
    """The LLM as a LanguageKernel: parse via the model (validated), realize via
    the deterministic emitter. Keeps the LanguageKernel contract exactly."""

    def __init__(
        self,
        backend: Backend,
        schema_path: str | Path = "specs/ir.schema.json",
        max_attempts: int = 2,
        fallback: LanguageKernel | None = None,
        fallback_score: float = 0.5,
    ) -> None:
        self._backend = backend
        self._schema_path = Path(schema_path)
        self.max_attempts = max_attempts
        self._fallback = fallback
        self.fallback_score = fallback_score
        self.fallback_events: list[dict[str, str]] = []
        self._schema: dict[str, Any] | None = None

    def _load_schema(self) -> dict[str, Any]:
        if self._schema is None:
            if not self._schema_path.is_file():
                here = Path(__file__).resolve()
                fallback = here.parents[3] / "specs" / "ir.schema.json"
                if fallback.is_file():
                    self._schema_path = fallback
            self._schema = json.loads(self._schema_path.read_text(encoding="utf-8"))
        return self._schema

    def parse(self, text: str, context: dict | None = None) -> list[Interpretation]:
        """One valid reading is returned (first valid attempt wins). Raises
        ValueError when the model cannot produce a valid dialect document AND no
        fallback kernel is configured (or the fallback also fails). A fallback
        reading is marked with a score <= `fallback_score` (P3.01)."""

        from kainos.lang.deterministic import _unresolved_surfaces

        messages = build_ast_prompt(text)
        last_error = "no attempts"
        llm_error: Exception | None = None
        for attempt in range(self.max_attempts):
            content = ""
            try:
                content = self._backend.complete(messages)
                doc = _extract_json(content)
                jsonschema.validate(doc, self._load_schema())
                node = from_ir(doc)
                return [
                    Interpretation(ir=node, score=1.0, unresolved=_unresolved_surfaces(node))
                ]
            except Exception as e:  # noqa: BLE001 — kernel boundary: any backend/protocol/shape error retries, then falls back
                last_error = f"{type(e).__name__}: {e}"
                llm_error = e
                if attempt + 1 < self.max_attempts:
                    messages = messages + [
                        {"role": "assistant", "content": content},
                        {
                            "role":
                            "user",
                            "content": f"Invalid document: {last_error}. Try again; "
                            "respond with ONLY the JSON document.",
                        },
                    ]
        if self._fallback is not None:
            try:
                interps = self._fallback.parse(text)
            except Exception:  # noqa: BLE001 — fallback parse may fail for any reason; the LLM error is reported
                self.fallback_events.append(
                    {"text": text, "error": last_error, "fallback": "failed"}
                )
                raise ValueError(
                    f"LLM could not produce a valid AST after {self.max_attempts} attempts "
                    f"and the fallback kernel also failed: {last_error}"
                ) from llm_error
            self.fallback_events.append({"text": text, "error": last_error, "fallback": "used"})
            return [
                replace(i, score=min(i.score, self.fallback_score)) for i in interps
            ]
        raise ValueError(
            f"LLM could not produce a valid AST after {self.max_attempts} attempts: {last_error}"
        )

    def realize(self, ir: object, style: str | None = None) -> str:
        """The deterministic emitter — the LLM adds nothing to realization."""

        if not isinstance(ir, Node):
            raise TypeError(f"realize() expects a dialect Node, got {type(ir)!r}")
        return emit(ir)

    def propose(self, ir: object) -> list[dict]:
        return []
