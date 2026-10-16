"""Scaffold smoke test (step 01): the package imports and reports its version.

pytest exits 5 on an empty collection, so this one test keeps
`pytest -q` at exit 0 from day one (action-step 01 "pytest exits 0").
"""

import kainos


def test_version():
    assert kainos.__version__ == "0.1.0"
