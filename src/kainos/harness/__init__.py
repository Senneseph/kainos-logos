"""kainos.harness — experiment runner: every claim is an experiment, never prose.

`runner` symbols are re-exported lazily (PEP 562) so that
`python -m kainos.harness.runner` (wired to `make bench`) does not trigger the
RuntimeWarning about executing a module already imported by the package __init__.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kainos.harness.dummy import DummyExperiment
from kainos.harness.report import render

if TYPE_CHECKING:  # pragma: no cover - typing surface only
    from kainos.harness.runner import (
        REGISTRY,
        RESULTS_DIR,
        Experiment,
        Result,
        git_commit,
        load_results,
        render_listing,
        resolve,
        result_to_dict,
        run,
        run_experiments,
        selected,
    )

__all__ = [
    "REGISTRY",
    "RESULTS_DIR",
    "DummyExperiment",
    "Experiment",
    "Result",
    "git_commit",
    "load_results",
    "render",
    "render_listing",
    "resolve",
    "result_to_dict",
    "run",
    "run_experiments",
    "selected",
]


def __getattr__(name: str):
    import importlib

    if name in __all__:
        module = importlib.import_module(f"{__name__}.runner")
        try:
            return getattr(module, name)
        except AttributeError:
            pass
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
