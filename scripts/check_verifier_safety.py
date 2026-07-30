#!/usr/bin/env python3
"""Reject optimization-sensitive assertions in acceptance code."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_ROOTS = (
    ROOT / "releases/m4",
    ROOT / "releases/m5",
    ROOT / "releases/m6-balanced",
    ROOT / "scripts",
    ROOT / "tests",
)


def main() -> int:
    violations: list[str] = []
    acceptance_code = sorted(
        path
        for directory in ACCEPTANCE_ROOTS
        for path in directory.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    for path in acceptance_code:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                violations.append(
                    f"{path.relative_to(ROOT)}:{node.lineno}: assert is "
                    "removed by python -O"
                )
    if violations:
        print("VERIFIER SAFETY: FAIL")
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print(
        "VERIFIER SAFETY: PASS "
        f"({len(acceptance_code)} files; no optimization-sensitive asserts)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
