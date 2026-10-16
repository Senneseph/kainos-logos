"""The OpenAI-protocol face (T1, #151): real HTTP, OpenAI shapes, honest
errors, and — the point — an infant that LEARNS across HTTP calls.

Stdlib only (urllib + the face's http.server); an ephemeral port on
127.0.0.1; the protocol is exercised like a real client would.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator

import pytest

from kainos.tutor.facade import DEFAULT_HOST, MODEL_ID, make_server


class Server:
    def __init__(self, persist, **kw):
        self.h = DEFAULT_HOST
        self.http = make_server(persist, host=self.h, port=0, **kw)
        self.port = self.http.server_address[1]
        self.t = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.t.start()

    def base(self):
        return f"http://{self.h}:{self.port}"

    def close(self):
        self.http.shutdown()
        self.http.server_close()
        self.t.join(timeout=5)


@pytest.fixture()
def srv(tmp_path) -> Iterator[Server]:
    s = Server(tmp_path / "live")
    yield s
    s.close()


def _post(url, body, raw: bytes | None = None) -> tuple[int, bytes]:
    data = raw if raw is not None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def _get(url) -> tuple[int, bytes]:
    try:
        with urllib.request.urlopen(url) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def _turn(srv: Server, text: str, **kw) -> dict:
    status, raw = _post(
        srv.base() + "/v1/chat/completions",
        {"model": MODEL_ID, "messages": [{"role": "user", "content": text}], **kw},
    )
    assert status == 200, raw
    return json.loads(raw)


def test_models_endpoint(srv):
    status, raw = _get(srv.base() + "/v1/models")
    assert status == 200
    d = json.loads(raw)
    assert d["object"] == "list"
    assert d["data"][0]["id"] == MODEL_ID
    assert d["data"][0]["object"] == "model"


def test_completion_shape_and_learning_across_http_calls(srv):
    d0 = _turn(srv, "7 + 8 is what?")
    c0 = d0["choices"][0]["message"]["content"]
    assert d0["object"] == "chat.completion"
    assert d0["choices"][0]["finish_reason"] == "stop"
    assert d0["model"] == MODEL_ID
    assert d0["usage"]["total_tokens"] > 0
    assert "don't know" in c0  # honest no BEFORE the teaching (zero fabrication)

    for n in range(5):
        r = _turn(srv, f"after {n} comes {n + 1}")
        assert "noted" in r["choices"][0]["message"]["content"] or "comes" in r["choices"][0]["message"]["content"]

    d = _turn(srv, "what comes after 3?")
    c = d["choices"][0]["message"]["content"]
    assert "4" in c  # learned across plain HTTP POSTs


def test_streaming_chunks_and_done(srv):
    for n in range(5):
        _turn(srv, f"after {n} comes {n + 1}")
    status, raw = _post(
        srv.base() + "/v1/chat/completions",
        {"model": MODEL_ID, "stream": True, "messages": [{"role": "user", "content": "2 + 3 is what?"}]},
    )
    assert status == 200
    text = raw.decode("utf-8")
    assert text.endswith("data: [DONE]\n\n")
    content_parts: list[str] = []
    obj_seen = set()
    for line in text.splitlines():
        if not line.startswith("data: "):
            continue
        payload = line[6:]
        if payload == "[DONE]":
            continue
        d = json.loads(payload)
        obj_seen.add(d["object"])
        delta = d["choices"][0]["delta"].get("content", "")
        if delta:
            content_parts.append(delta)
    assert obj_seen == {"chat.completion.chunk"}
    joined = "".join(content_parts)
    assert "5" in joined  # 2 + 3 = 5, streamed


def test_malformed_body_is_400_not_confused_200(srv):
    status, raw = _post(srv.base() + "/v1/chat/completions", None, raw=b"{not json")
    assert status == 400
    d = json.loads(raw)
    assert d["error"]["type"] == "invalid_request_error"
    assert "JSON" in d["error"]["message"]


def test_missing_messages_is_400(srv):
    status, raw = _post(srv.base() + "/v1/chat/completions", {"model": MODEL_ID})
    assert status == 400
    assert json.loads(raw)["error"]["type"] == "invalid_request_error"


def test_no_user_message_is_400(srv):
    status, _ = _post(srv.base() + "/v1/chat/completions", {"messages": [{"role": "system", "content": "hi"}]})
    assert status == 400


def test_unknown_paths_and_methods_are_envelopes(srv):
    status, raw = _get(srv.base() + "/v1/nope")
    assert status == 404
    assert json.loads(raw)["error"]["type"] == "invalid_request_error"
    status, raw = _get(srv.base() + "/other")
    assert status == 404
    # GET on a POST endpoint: BaseHTTPRequestHandler has no do_GET route -> 404
    status, _ = _post(srv.base() + "/v1/sessions/lapse", {})
    assert status == 200  # the documented extension, used below


def test_lapse_extension_persists_and_reboots(srv, tmp_path):
    for n in range(4):
        _turn(srv, f"after {n} comes {n + 1}")
    status, raw = _post(srv.base() + "/v1/sessions/lapse", {})
    assert status == 200
    d = json.loads(raw)
    assert d["ended"] == 1 and d["next"] == 2
    (tmp_path / "live" / "codeX-S01.json").exists()  # the persisted CODEX dump
    (tmp_path / "live" / "session-S01.json").exists()  # the session report
    # knowledge survived: a fresh session answers from the restored CODEX
    c = _turn(srv, "what comes after 2?")["choices"][0]["message"]["content"]
    assert "3" in c


def test_persona_recorded_from_system_message(srv, tmp_path):
    status, _raw = _post(
        srv.base() + "/v1/chat/completions",
        {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": "You are the infant. Be honest about what you do not know."},
                {"role": "user", "content": "after 1 comes 2"},
            ],
        },
    )
    assert status == 200
    persona = json.loads((tmp_path / "live" / "persona.json").read_text())
    assert "infant" in persona["persona"]


def test_local_only_default():
    assert DEFAULT_HOST == "127.0.0.1"
