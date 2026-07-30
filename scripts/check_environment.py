#!/usr/bin/env python3
"""Require the exact runtime versions used by the publication replay."""

from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError, version


EXPECTED = {
    "mpmath": "1.3.0",
    "python-flint": "0.8.0",
    "sympy": "1.14.0",
}


def main() -> int:
    failures: list[str] = []
    if sys.version_info < (3, 11):
        failures.append(
            f"Python {sys.version.split()[0]} is installed; expected >=3.11"
        )
    observed: dict[str, str] = {}
    for distribution, expected in EXPECTED.items():
        try:
            observed[distribution] = version(distribution)
        except PackageNotFoundError:
            failures.append(f"{distribution}: not installed")
            continue
        if observed[distribution] != expected:
            failures.append(
                f"{distribution}: {observed[distribution]}, expected {expected}"
            )
    if failures:
        print("REPLICATION ENVIRONMENT: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(
        "REPLICATION ENVIRONMENT: PASS "
        f"(Python {sys.version.split()[0]}, "
        + ", ".join(f"{name} {observed[name]}" for name in sorted(observed))
        + ")"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
