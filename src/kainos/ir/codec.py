"""Semantic IR codec (P0.05) — validated at every boundary (invariant #7).

``validate`` raises ``ValueError`` with the JSON path of the first failure;
``load`` validates then wraps (deep copy — the wrapper owns its dict, so
``dump(load(x)) == x``); ``dump`` unwraps deterministically.

The schema is bundled inside the package and loaded via ``importlib.resources``
so validation never depends on the CWD. The bundled copy
(``kainos/ir/_schemas/ir.schema.json``) must be byte-identical to the canonical
``specs/ir.schema.json`` — tests/ir/test_codec.py enforces that.
"""

from __future__ import annotations

import copy
import json
from importlib.resources import files
from typing import Any

import jsonschema  # type: ignore[import-untyped]  # no py.typed shipped; stubs would need a lockfile pin

from kainos.ir.models import SemanticIR

__all__ = ["dump", "load", "validate"]

_SPEC = files("kainos.ir").joinpath("_schemas", "ir.schema.json")
_SCHEMA: dict[str, Any] = json.loads(_SPEC.read_text("utf-8"))
_VALIDATOR = jsonschema.Draft202012Validator(_SCHEMA)


def validate(data: dict) -> None:
    """Validate against ``kainos/ir/1``.

    Raises ``ValueError`` naming the JSON path (``$.kind`` etc.) of the first
    violation when the data is not a valid IR.
    """
    errors = sorted(_VALIDATOR.iter_errors(data), key=lambda e: (list(e.absolute_path), e.message))
    if errors:
        err = errors[0]
        raise ValueError(f"IR invalid at {err.json_path}: {err.message}") from err


def load(data: dict) -> SemanticIR:
    """Validate, then wrap in :class:`SemanticIR` (deep copy; the wrapper owns it)."""
    validate(data)
    return SemanticIR(data=copy.deepcopy(data))


def dump(ir: SemanticIR) -> dict:
    """Unwrap the wrapper to its dict (deterministic; same object the wrapper owns)."""
    return ir.to_dict()
