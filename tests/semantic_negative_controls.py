#!/usr/bin/env python3
"""Require the semantic checker to reject four known-bad encodings."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = (
    "omit-pattern",
    "corrupt-orbit",
    "corrupt-vector",
    "omit-block",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    python = args.python.absolute()
    failures: list[str] = []
    for fixture in FIXTURES:
        for mode, flags in (("normal", []), ("optimized", ["-O"])):
            result = subprocess.run(
                [
                    str(python),
                    *flags,
                    "scripts/check_semantic_bridge.py",
                    "--inject",
                    fixture,
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=args.timeout,
                check=False,
            )
            combined = result.stdout + result.stderr
            rejected = (
                result.returncode != 0
                and "SemanticError" in combined
            )
            print(
                f"  {fixture}/{mode}: "
                f"{'REJECTED' if rejected else 'MISSED'}"
            )
            if not rejected:
                failures.append(
                    f"{fixture}/{mode}: exit={result.returncode}; "
                    f"tail={combined.strip().splitlines()[-5:]}"
                )
    if failures:
        print("SEMANTIC NEGATIVE CONTROLS: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("SEMANTIC NEGATIVE CONTROLS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
