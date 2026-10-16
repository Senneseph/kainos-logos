"""Session-wide test isolation — results hygiene (the "vanished reports" fix).

The experiment benches write their evidence to a DEFAULT output root
(``kainos.harness.paths.default_results_dir``). Before 2026-08-21 that
default was the literal ``results/`` resolved against the CWD, so EVERY
pytest run silently rewrote the repo's tracked official artifacts (full
phase reports + flat records) with test-time data — ``commit: unknown``,
fast-sample env knobs — and the rendered ``SUMMARY.md`` went stale or was
regenerated from the clobbered data. Official runs have to happen AFTER
the gate, or after manual ``git checkout`` restores, each time.

That was the root cause of the recurring "the reports disappeared" —
they were overwritten in place, not deleted. Fix: the test session
redirects the default root to a session tmpdir *before* collection, so
test runs never touch ``results/``. Official CLI runs leave
``KAINOS_RESULTS_DIR`` unset and are byte-for-byte as before.

Set at conftest import time so it applies to ALL test modules, including
experiment classes instantiated at import/collection time.
"""

import os
import tempfile

os.environ["KAINOS_RESULTS_DIR"] = tempfile.mkdtemp(prefix="kainos-test-results-")
