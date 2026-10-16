"""Kainos CLI (P0.07) — inspect the CODEX and Semantic IR from the shell.

The concrete form of inspectability (invariant #9): humans (and later
experiments) can read the CODEX and validate IRs without writing code.

Usage:
    kainos codex add    --file assertion.json [--db data/codex.sqlite]
    kainos codex query  [--subject S] [--relation R] [--status STATUS] [--db P]
    kainos codex explain <id> [--db P]
    kainos codex dump   [--out out.json] [--db P]
    kainos ir validate  <file.json>

Exit codes: 0 on success (``ir validate`` prints ``OK``); 1 on a handled
error (bad file/JSON/schema — message on stderr); 2 on usage error (argparse).
``codex query`` prints one JSON object per line (JSON lines, sorted keys);
``codex explain`` of an unknown id prints the ``{"id": ..., "missing": true}``
rendering with exit 0 — explain never raises (plan 10.1).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from kainos.codex.explain import explain
from kainos.codex.models import Assertion, EpistemicState
from kainos.codex.sqlite import SqliteCodexStore
from kainos.codex.store import CodexStore
from kainos.harness.report import render
from kainos.harness.runner import (
    Result,
    load_results,
    render_listing,
    run_experiments,
    selected,
)
from kainos.ir.codec import validate
from kainos.regex.ir import to_ir
from kainos.regex.pipeline import default_codex, describe

__all__ = ["DEFAULT_DB", "main"]

DEFAULT_DB = "data/codex.sqlite"


class CliError(Exception):
    """A handled CLI error (bad file / JSON / schema) — message goes to stderr, exit 1."""


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point (``[project.scripts] kainos``). Returns the exit code."""
    args = build_parser().parse_args(argv)
    try:
        if args.domain == "ir":
            return _ir_validate(args.file)
        if args.domain == "experiment":
            if args.command == "list":
                return _experiment_list()
            if args.command == "run":
                return _experiment_run(args)
            if args.command == "report":
                return _experiment_report(args)
            raise CliError(f"unhandled experiment command: {args.command!r}")
        if args.domain == "regex":
            if args.command == "describe":
                return _regex_describe(args)
            if args.command == "explain":
                return _regex_explain(args)
            raise CliError(f"unhandled regex command: {args.command!r}")
        if args.domain == "tutor":
            if args.command == "serve":
                return _tutor_serve(args)
            raise CliError(f"unhandled tutor command: {args.command!r}")
        if args.domain == "modela":
            if args.command == "train":
                return _modela_train(args)
            if args.command == "predict":
                return _modela_predict(args)
            raise CliError(f"unhandled modela command: {args.command!r}")
        if args.domain == "q20":
            if args.command == "growth":
                return _q20_growth(args)
            raise CliError(f"unhandled q20 command: {args.command!r}")
        store = _open_store(args.db)
        try:
            if args.command == "add":
                return _codex_add(store, args.file)
            if args.command == "query":
                return _codex_query(store, args)
            if args.command == "explain":
                return _codex_explain(store, args.id)
            if args.command == "dump":
                return _codex_dump(store, args.out)
            raise CliError(f"unhandled codex command: {args.command!r}")
        finally:
            store.close()
    except CliError as e:
        print(str(e), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="kainos",
        description="Kainos-Logos CLI — inspect the CODEX and Semantic IR (invariant #9).",
    )
    domains = p.add_subparsers(dest="domain", required=True)

    codex = domains.add_parser("codex", help="CODEX assertion store operations")
    csub = codex.add_subparsers(dest="command", required=True)

    pa = csub.add_parser("add", help="add an assertion from a JSON file (kainos/codex/1 dict)")
    pa.add_argument("--file", required=True, help="path to the assertion JSON file")
    pa.add_argument("--db", default=DEFAULT_DB, help=f"sqlite path (default: {DEFAULT_DB})")

    pq = csub.add_parser("query", help="query assertions; one JSON object per line on stdout")
    pq.add_argument("--subject", help="filter by subject term id")
    pq.add_argument("--relation", help="filter by relation term id")
    pq.add_argument("--status", help="filter by epistemic status (candidate|established|...)")
    pq.add_argument("--db", default=DEFAULT_DB)

    pe = csub.add_parser("explain", help="print the assertion's recursive evidence chain")
    pe.add_argument("id", help="assertion id")
    pe.add_argument("--db", default=DEFAULT_DB)

    pd = csub.add_parser("dump", help="dump the store as {terms, assertions} JSON")
    pd.add_argument("--out", help="write to this file instead of stdout")
    pd.add_argument("--db", default=DEFAULT_DB)

    ir = domains.add_parser("ir", help="Semantic IR operations")
    isub = ir.add_subparsers(dest="command", required=True)
    pv = isub.add_parser("validate", help="validate an IR JSON file against kainos/ir/1")
    pv.add_argument("file", help="path to the IR JSON file")

    ex = domains.add_parser("experiment", help="experiment harness (measure, don't argue)")
    esub = ex.add_subparsers(dest="command", required=True)
    esub.add_parser("list", help="registered experiments + thresholds")
    er = esub.add_parser("run", help="run experiments; persists results/<name>.{json,md}")
    group = er.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="run every registered experiment")
    group.add_argument("--name", help="run one experiment (exact key or unique short name)")
    group.add_argument("--phase", type=int, help="run all experiments registered for phase N")
    er.add_argument("--results-dir", default="results", help="output dir (default: results)")
    ep = esub.add_parser("report", help="render a markdown report from persisted results")
    ep.add_argument("--out", help="write the report to this file (default: stdout)")
    ep.add_argument("--phase", type=int, default=None, help="only results of phase N (eN.* registry keys)")
    ep.add_argument("--results-dir", default="results", help="results dir to read (default: results)")

    rx = domains.add_parser("regex", help="Phase 1 NL-regex pipeline (parse - resolve - emit - judge)")
    rsub = rx.add_subparsers(dest="command", required=True)
    rd = rsub.add_parser("describe", help="run the full pipeline; print the JSON result")
    rd.add_argument("text", help="the restricted-English description")
    rd.add_argument("--codex", help="sqlite CODEX path (default: a fresh in-memory seed lexicon)")
    rd.add_argument("--seed", type=int, default=0, help="testgen seed (default: 0)")
    re_ = rsub.add_parser("explain", help="run the pipeline; print the full IR + trace + PCRE + verdict")
    re_.add_argument("text", help="the restricted-English description")
    re_.add_argument("--codex", help="sqlite CODEX path (default: a fresh in-memory seed lexicon)")
    re_.add_argument("--seed", type=int, default=0, help="testgen seed (default: 0)")

    tu = domains.add_parser("tutor", help="The Interactive Tutor (epic #150): the OpenAI-protocol face")
    tsub = tu.add_subparsers(dest="command", required=True)
    ts = tsub.add_parser("serve", help="serve /v1/models + /v1/chat/completions (local-only by default)")
    ts.add_argument("--persist", default="tutor-live", help="session persistence dir (default: tutor-live/)")
    ts.add_argument("--port", type=int, default=8321, help="port (default: 8321)")
    ts.add_argument("--host", default="127.0.0.1", help="bind host (default: 127.0.0.1 — local-only privacy boundary)")
    ts.add_argument("--backend", choices=("none", "ollama"), default="none", help="LLM surface arm (default: none — the deterministic arm, SKIP semantics)")

    ma = domains.add_parser("modela", help="Model A baseline (E1.5): train on the seed corpus / predict")
    msub = ma.add_subparsers(dest="command", required=True)
    mt = msub.add_parser("train", help="train Model A on the seed corpus only and write data/models/model_a.pt")
    mt.add_argument("--epochs", type=int, default=None, help="override the pinned epoch count (default: 200)")
    mp = msub.add_parser("predict", help="one inference on the committed artifact")
    mp.add_argument("text", help="the description to translate")
    mp.add_argument("--weights", help="weights path (default: the committed data/models/model_a.pt)")

    q20p = domains.add_parser("q20", help="20Q world (phase 2): growth dashboard on the seeded CODEX")
    q20sub = q20p.add_subparsers(dest="command", required=True)
    qg = q20sub.add_parser("growth", help="seed the CODEX with the 20Q corpus, render results/phase-2/growth.md")
    qg.add_argument("--out", default="results/phase-2/growth.md", help="output path for the growth dashboard")
    return p


#: The face's endpoints (one line for the serve banner).
MODEL_HINT = "/v1/models + /v1/chat/completions"


def _tutor_serve(args) -> int:
    """Run the OpenAI-protocol face (T1, #151): local-only by default."""

    from pathlib import Path as _Path

    from kainos.tutor.facade import make_server

    backend = None
    if args.backend == "ollama":
        from kainos.lang.llm import OllamaBackend

        backend = OllamaBackend()
    server = make_server(_Path(args.persist), host=args.host, port=args.port, backend=backend)
    print(f"kainos infant serving {MODEL_HINT} at http://{args.host}:{args.port}/v1 (local-only: {args.host == '127.0.0.1'})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
    finally:
        server.server_close()
    return 0


def _open_store(db: str) -> SqliteCodexStore:
    parent = Path(db).parent
    if parent != Path("."):
        parent.mkdir(parents=True, exist_ok=True)
    return SqliteCodexStore(db)


def _status_enum(value: str | None) -> EpistemicState | None:
    if value is None:
        return None
    try:
        return EpistemicState(value)
    except ValueError:
        valid = ", ".join(s.value for s in EpistemicState)
        raise CliError(f"unknown status {value!r} (valid: {valid})") from None


def _codex_add(store: SqliteCodexStore, path: str) -> int:
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as e:
        raise CliError(f"cannot read {path}: {e}") from None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise CliError(f"invalid JSON in {path}: {e}") from None
    try:
        a = Assertion.from_dict(data)
    except (KeyError, TypeError, ValueError) as e:
        raise CliError(f"not a valid assertion (kainos/codex/1): {e}") from None
    store.add(a)
    print(f"added {a.id}")
    return 0


def _codex_query(store: SqliteCodexStore, args: argparse.Namespace) -> int:
    results = store.query(
        subject=args.subject,
        relation=args.relation,
        status=_status_enum(args.status),
    )
    for a in results:
        print(json.dumps(a.to_dict(), sort_keys=True))
    return 0


def _codex_explain(store: SqliteCodexStore, id: str) -> int:
    # explain() never raises: an unknown id prints the {"id": ..., "missing": true}
    # rendering with exit 0 (same contract as the store, plan 10.1).
    print(json.dumps(explain(store, id), indent=2, sort_keys=True))
    return 0


def _codex_dump(store: SqliteCodexStore, out: str | None) -> int:
    d = store.dump()
    text = json.dumps(d, indent=2, sort_keys=True)
    if out is None:
        print(text)
        return 0
    p = Path(out)
    if p.parent != Path("."):
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text + "\n", encoding="utf-8")
    print(f"wrote {len(d['assertions'])} assertions, {len(d['terms'])} terms to {out}", file=sys.stderr)
    return 0


def _ir_validate(path: str) -> int:
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as e:
        print(f"cannot read {path}: {e}", file=sys.stderr)
        return 1
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"invalid JSON in {path}: {e}", file=sys.stderr)
        return 1
    try:
        validate(data)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    print("OK")
    return 0


def _experiment_list() -> int:
    print(render_listing())
    return 0


def _codex_from_args(codex_path: str | None) -> CodexStore:
    if codex_path is None:
        return default_codex()
    parent = Path(codex_path).parent
    if parent != Path("."):
        parent.mkdir(parents=True, exist_ok=True)
    return SqliteCodexStore(codex_path)


def _regex_describe(args: argparse.Namespace) -> int:
    try:
        result = describe(args.text, _codex_from_args(args.codex), seed=args.seed)
    except ValueError as e:
        print(f"could not parse {args.text!r}: {e}", file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0


def _regex_explain(args: argparse.Namespace) -> int:
    try:
        result = describe(args.text, _codex_from_args(args.codex), seed=args.seed)
    except ValueError as e:
        print(f"could not parse {args.text!r}: {e}", file=sys.stderr)
        return 1
    lines: list[str] = []
    lines.append(f"describe: {args.text!r}")
    lines.append("")
    lines.append("IR (resolved dialect tree, generic kainos/ir/1 form):")
    lines.append(json.dumps(to_ir(result.ir), indent=2, sort_keys=True))
    lines.append("")
    lines.append("Resolved trace:")
    if result.resolved_trace:
        for entry in result.resolved_trace:
            lines.append(f"  - {json.dumps(entry, sort_keys=True)}")
    else:
        lines.append("  (no entries)")
    if result.escalation is not None:
        lines.append("")
        lines.append(f"ESCALATION (no regex emitted): {json.dumps(result.escalation, sort_keys=True)}")
    else:
        lines.append("")
        lines.append(f"PCRE: {result.pcre}")
        if result.verdict is not None:
            lines.append(f"Verdict: {result.verdict.summary()}")
            for m in result.verdict.mismatches:
                lines.append(f"  - {json.dumps(m, sort_keys=True)}")
    lines.append("")
    lines.append(f"Confidence: {result.confidence:.2f}")
    print("\n".join(lines))
    return 0


def _modela_train(args: argparse.Namespace) -> int:
    from kainos.llm.train import train_model_a

    print(json.dumps(train_model_a(epochs=args.epochs), indent=2, sort_keys=True))
    return 0


def _modela_predict(args: argparse.Namespace) -> int:
    from kainos.llm.train import predict_model_a

    print(json.dumps(predict_model_a(args.text, weights_path=args.weights), indent=2, sort_keys=True))
    return 0


def _q20_growth(args: argparse.Namespace) -> int:
    from kainos.codex.memory import InMemoryCodexStore
    from kainos.q20 import load_corpus, load_questions, seed
    from kainos.q20.dashboard import write_growth

    store = InMemoryCodexStore()
    stats = seed(store)
    out = write_growth(store, load_corpus(), load_questions(), args.out)
    print(f"seeded {stats['total']} assertions ({stats['concepts']} concepts)")
    print(f"wrote {out}")
    return 0


def _experiment_run(args: argparse.Namespace) -> int:
    try:
        exps = selected(name=args.name, all=args.all, phase=args.phase)
    except LookupError as e:
        print(str(e), file=sys.stderr)
        return 1
    _, rc = run_experiments(exps, Path(args.results_dir))
    return rc


def _experiment_report(args: argparse.Namespace) -> int:
    rows = load_results(Path(args.results_dir), args.phase)
    if not rows:
        where = f"for phase {args.phase}" if args.phase is not None else ""
        print(f"no persisted results {where} under {args.results_dir}/", file=sys.stderr)
        return 1
    results = [
        Result(
            name=d["name"],
            passed=d["passed"],
            value=d["value"],
            evidence=[Path(p) for p in d.get("evidence", [])],
            config=d.get("config", {}),
            threshold=d.get("threshold"),
        )
        for d in rows
    ]
    text = render(results)
    if args.out is None:
        print(text)
        return 0
    p = Path(args.out)
    if p.parent != Path("."):
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text + "\n", encoding="utf-8")
    print(f"wrote report for {len(results)} experiment(s) to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
