"""bandgen CLI (v0.1).

    python3 -m tools.bandgen validate   bands/spec-e6.17.json
    python3 -m tools.bandgen dryrun     bands/spec-e6.17.json [--workdir DIR] [--md FILE]

validate: schema + structural checks only (fast, no runtime).
dryrun:   the full control — seed checks, computed beds, the
          labeled dry-run (x2 for the twin), the carry run, mastery
          pre/post, totals, discipline — reporting the diff table.
          Exit 0 = CLEAN (ready to freeze), 1 = diffs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

from .control import render_markdown, run_control, to_json
from .spec import REPO_ROOT, load_spec, structural_checks


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bandgen", description="the band compiler (v0.1: validate / compute / control)")
    ap.add_argument("cmd", choices=["validate", "dryrun", "tables"])
    ap.add_argument("spec", help="path to the band spec JSON (repo-relative or absolute)")
    ap.add_argument("--workdir", default=None, help="scratch root for the dry-run (default: ./.bandgen-scratch/<id>)")
    ap.add_argument("--md", default=None, help="write the control report markdown here")
    ap.add_argument("--json-out", default=None, help="write the full control report JSON here")
    args = ap.parse_args(argv)

    try:
        spec = load_spec(args.spec)
    except (OSError, ValueError, json.JSONDecodeError, jsonschema.ValidationError, KeyError) as e:
        print(f"bandgen: spec load/validation failed: {e}", file=sys.stderr)
        return 2

    if args.cmd == "validate":
        bad = structural_checks(spec)
        for b in bad:
            print(f"STRUCTURAL: {b}")
        print(("CLEAN" if not bad else f"{len(bad)} structural problems") + f" — {spec['id']}")
        return 0 if not bad else 1

    report = run_control(spec, workdir=args.workdir or (REPO_ROOT / ".bandgen-scratch" / spec["id"]))
    print(to_json(report) if not args.md and not args.json_out else "", end="" if args.md or args.json_out else "\n")
    if args.md:
        Path(args.md).write_text(render_markdown(report), encoding="utf-8")
        print(f"control report (md) -> {args.md}")
    if args.json_out:
        Path(args.json_out).write_text(to_json(report), encoding="utf-8")
        print(f"control report (json) -> {args.json_out}")
    for name, c in report["checks"].items():
        print(f"{name}: {'PASS' if c['pass'] else 'DIFF'} ({len(c.get('bad', []))} problems)")
    print(("CLEAN — ready to freeze" if report["ok"] else "DIFFS — the mechanism disagrees with the spec") + f" — {spec['id']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
