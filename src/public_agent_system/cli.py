"""Command-line interface for local registry and envelope validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .core import new_envelope, validate_envelope
from .registry import AGENTS, AGENTS_BY_ID


def _read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("The top-level JSON value must be an object")
    return value


def _write_json(path: Path, value: dict, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite {path}; use --force if intentional")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect the public agent registry and validate handoff envelopes.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all public agents")

    show_parser = subparsers.add_parser("show", help="Show one public agent")
    show_parser.add_argument("agent_id")

    validate_parser = subparsers.add_parser("validate", help="Validate a handoff envelope")
    validate_parser.add_argument("path", type=Path)

    new_parser = subparsers.add_parser("new", help="Create a draft handoff envelope")
    new_parser.add_argument("--source", required=True)
    new_parser.add_argument("--target", required=True)
    new_parser.add_argument("--purpose", required=True)
    new_parser.add_argument("--deliverable", required=True)
    new_parser.add_argument("--gate", choices=("INTERNAL", "REVIEW", "ACTION", "BLOCKED"), default="REVIEW")
    new_parser.add_argument("--output", type=Path)
    new_parser.add_argument("--force", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "list":
        for agent in AGENTS:
            print(f"{agent['id']}  {agent['name']}  -> {agent['output']}")
        return 0

    if args.command == "show":
        agent = AGENTS_BY_ID.get(args.agent_id)
        if agent is None:
            print(f"Unknown agent: {args.agent_id}")
            return 2
        print(json.dumps(agent, indent=2))
        return 0

    if args.command == "validate":
        try:
            envelope = _read_json(args.path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"INVALID: {exc}")
            return 2
        result = validate_envelope(envelope)
        if result.valid:
            print("VALID")
            return 0
        print("INVALID")
        for error in result.errors:
            print(f"- {error}")
        return 1

    envelope = new_envelope(
        source_agent=args.source,
        target_agent=args.target,
        purpose=args.purpose,
        primary_deliverable=args.deliverable,
        gate=args.gate,
    )
    result = validate_envelope(envelope)
    if not result.valid:
        print("INVALID DRAFT REQUEST")
        for error in result.errors:
            print(f"- {error}")
        return 1
    if args.output:
        try:
            _write_json(args.output, envelope, args.force)
        except OSError as exc:
            print(f"Could not write envelope: {exc}")
            return 2
        print(f"Wrote {args.output}")
    else:
        print(json.dumps(envelope, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

