#!/usr/bin/env python3
"""Require every LaTeX citation key to resolve and every bibitem to be used."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPTS = (
    ROOT / "paper/exact_low_length_recht_re.tex",
)
CITE_PATTERN = re.compile(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}")
BIB_PATTERN = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}")


def main() -> int:
    failures: list[str] = []
    for path in MANUSCRIPTS:
        source = path.read_text(encoding="utf-8")
        cited = {
            key.strip()
            for group in CITE_PATTERN.findall(source)
            for key in group.split(",")
            if key.strip()
        }
        declared = {key.strip() for key in BIB_PATTERN.findall(source)}
        missing = sorted(cited - declared)
        orphaned = sorted(declared - cited)
        label = path.relative_to(ROOT)
        if missing:
            failures.append(f"{label}: missing bibitems: {', '.join(missing)}")
        if orphaned:
            failures.append(f"{label}: uncited bibitems: {', '.join(orphaned)}")
        if not missing and not orphaned:
            print(
                f"{label}: PASS ({len(cited)} cited keys, "
                f"{len(declared)} bibitems)"
            )
    if failures:
        print("CITATION KEY AUDIT: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("CITATION KEY AUDIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
