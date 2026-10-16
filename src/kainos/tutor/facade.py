"""The OpenAI-protocol face (T1, #151): a THIN stdlib HTTP server.

The system is now interacted with like an LLM: any OpenAI-compatible
client (OpenAI SDK with `base_url` pointed here, curl, or the un-
attended loop's own LLM arms) can drive the infant.

Surface (protocol-compatible shapes; local-only bind by default —
the privacy boundary is the spec's standing rule):

- ``GET  /v1/models``            -> the model list (``kainos-infant``)
- ``POST /v1/chat/completions``  -> one brainstem turn per request;
  ``stream=false`` (single JSON) or ``stream=true`` (SSE chunks,
  terminated by ``data: [DONE]``)
- ``POST /v1/sessions/lapse``    -> documented extension: ends the
  current session (the persisted report + CODEX dump are written) and
  arms the next one; the following completion auto-boots it

Grounding rules (inherited, not negotiated by the protocol):

- **The CODEX is the student.** The request's `messages` history is
  protocol compliance only — the authoritative memory is the store
  (the infant does not re-derive its knowledge from the client's
  transcript; that would be a second, un-provenanced memory).
- `system` message(s) -> the persona / session brief, recorded in
  `<persist>/persona.json` (faithful to the last one sent).
- The LAST user message is the turn's surface text; the response
  content is the brainstem's grounded phrasing (deterministic template
  on the det arm — or the LLM-phrased one when a backend is attached;
  the IR is always CODEX-derived).
- Protocol errors are OpenAI-style error envelopes (400/404/405) —
  never a confused 200 with a half-formed answer.

`usage` carries a documented heuristic (whitespace word count), not a
BPE claim: the pilot makes no tokenizer assertion.
"""

from __future__ import annotations

import json
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING, Any

from kainos.tutor.session import InfantRuntime

if TYPE_CHECKING:  # pragma: no cover
    from kainos.lang.llm import Backend

__all__ = ["MODEL_ID", "InfantServer", "make_server"]

MODEL_ID = "kainos-infant"
DEFAULT_HOST = "127.0.0.1"  # local-only by default (privacy boundary)
DEFAULT_PORT = 8321


def _error(status: int, message: str, typ: str = "invalid_request_error", code: str | None = None) -> tuple[int, dict[str, Any]]:
    env: dict[str, Any] = {"error": {"message": message, "type": typ, "param": None}}
    if code is not None:
        env["error"]["code"] = code
    return status, env


def _words(s: str) -> int:
    return len(s.split())


class InfantServer:
    """The stateful side of the face: one runtime, one current session,
    protocol routing. Thread-safe (one lock — turns are cheap and the
    pilot is single-student)."""

    def __init__(self, persist_dir: str | Path, backend: Backend | None = None) -> None:
        self._persist = Path(persist_dir)
        self._persist.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._rt = InfantRuntime(self._persist, backend=backend)
        self._session = self._resume_session()
        self._rt.boot(self._session)
        self._persona: str | None = None
        self._turns_served = 0

    # ── lifecycle ───────────────────────────────────────────────────────

    def _resume_session(self) -> int:
        """Continue after the last lapsed session (1 if none)."""

        last = 0
        for f in self._persist.glob("codeX-S*.json"):
            m = re.fullmatch(r"codeX-S(\d+)\.json", f.name)
            if m:
                last = max(last, int(m.group(1)))
        return last + 1 if last >= 1 else 1

    # ── protocol handling ───────────────────────────────────────────────

    def models(self) -> tuple[int, dict[str, Any]]:
        return 200, {
            "object": "list",
            "data": [
                {
                    "id": MODEL_ID,
                    "object": "model",
                    "created": 0,
                    "owned_by": "kainos",
                }
            ],
        }

    def chat_completions(self, body: dict[str, Any]) -> tuple[int, dict[str, Any] | None, list[str] | None]:
        """One turn. Returns (status, payload, sse_chunks)."""

        with self._lock:
            messages = body.get("messages")
            if not isinstance(messages, list) or not messages:
                st, env = _error(400, "'messages' must be a non-empty list")
                return st, env, None
            persona: str | None = None
            surface: str | None = None
            for msg in messages:
                if not isinstance(msg, dict) or not isinstance(msg.get("content"), str):
                    st, env = _error(400, "each message needs a string 'content' field")
                    return st, env, None
                role = msg.get("role")
                if role == "system":
                    persona = msg["content"]  # the last system wins (the brief)
                elif role == "user":
                    surface = msg["content"]  # the last user turn is the surface
                # assistant/tool history: accepted (protocol), not re-fed
                # (the CODEX is the memory)
            if surface is None:
                st, env = _error(400, "no 'user' message found in messages")
                return st, env, None
            if persona is not None:
                self._persona = persona
                (self._persist / "persona.json").write_text(
                    json.dumps({"persona": persona, "session": self._session}, sort_keys=True) + "\n"
                )
            try:
                r = self._rt.turn(surface)
            except Exception as exc:  # noqa: BLE001 - HTTP boundary: ANY turn failure is a 500 envelope, never a confused 200
                st, env = _error(500, f"brainstem turn failed: {exc}", typ="server_error")
                return st, env, None
            self._turns_served += 1
            content = r.response_text
            base = {
                "id": f"chatcmpl-{r.turn.replace(':', '')}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": MODEL_ID,
            }
            usage = {"prompt_tokens": _words(surface), "completion_tokens": _words(content), "total_tokens": _words(surface) + _words(content)}
            stream = bool(body.get("stream"))
            if not stream:
                payload = {
                    **base,
                    "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
                    "usage": usage,
                }
                return 200, payload, None
            chunks: list[str] = []
            words = content.split(" ")
            step = max(1, len(words) // 6) if words else 1
            for i in range(0, len(words), step):
                piece = " ".join(words[i : i + step])
                if i + step < len(words):
                    piece += " "
                chunks.append(
                    "data: "
                    + json.dumps(
                        {
                            **base,
                            "object": "chat.completion.chunk",
                            "choices": [{"index": 0, "delta": {"role": "assistant" if i == 0 else "", "content": piece}, "finish_reason": None}],
                        },
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    + "\n\n"
                )
            chunks.append(
                "data: "
                + json.dumps(
                    {
                        **base,
                        "object": "chat.completion.chunk",
                        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                        "usage": usage,
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n\n"
            )
            chunks.append("data: [DONE]\n\n")
            return 200, None, chunks

    def lapse(self) -> tuple[int, dict[str, Any]]:
        """End the current session (persisted) and boot the next."""

        with self._lock:
            rep = self._rt.lapse().to_dict()
            self._session += 1
            self._rt.boot(self._session)
            return 200, {
                "object": "infant.session",
                "ended": rep["session"],
                "next": self._session,
                "mastery": rep["mastery"],
                "attention": rep["attention"],
            }


def make_server(persist_dir: str | Path, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, backend: Backend | None = None) -> ThreadingHTTPServer:
    """Build the HTTP server (the CLI entry point and the tests use it)."""

    server = InfantServer(persist_dir, backend=backend)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args: Any) -> None:  # quiet by default
            pass

        def _send(self, status: int, payload: dict[str, Any] | None, chunks: list[str] | None = None) -> None:
            if chunks is not None:
                self.send_response(status)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                for c in chunks:
                    self.wfile.write(c.encode("utf-8"))
                return
            data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:
            if self.path == "/v1/models":
                status, payload = server.models()
                self._send(status, payload)
            elif self.path.startswith("/v1/"):
                self._send(*_error(404, f"unknown model endpoint: {self.path}"))
            elif self.path in ("/", "/healthz"):
                self._send(200, {"ok": True, "model": MODEL_ID, "session": server._session})
            else:
                self._send(*_error(404, f"not found: {self.path}"))

        def do_POST(self) -> None:
            if self.path == "/v1/chat/completions":
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b""
                try:
                    body = json.loads(raw.decode("utf-8"))
                    if not isinstance(body, dict):
                        raise TypeError("not an object")
                except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
                    self._send(*_error(400, "request body must be a JSON object"))
                    return
                status, payload, chunks = server.chat_completions(body)
                self._send(status, payload, chunks)
                return
            if self.path == "/v1/sessions/lapse":
                status, payload = server.lapse()
                self._send(status, payload)
                return
            if self.path.startswith("/v1/"):
                self._send(*_error(404, f"unknown endpoint: {self.path}"))
            else:
                self._send(*_error(404, f"not found: {self.path}"))

    return ThreadingHTTPServer((host, port), Handler)
