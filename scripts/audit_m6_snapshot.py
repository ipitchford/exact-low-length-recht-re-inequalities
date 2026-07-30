#!/usr/bin/env python3
"""Safely inventory the remaining exploratory m=6 endpoint/all-n snapshot.

Binary pickle files are hashed but never deserialized.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
M6 = ROOT / "exploratory/m6"

REQUIRED_INPUTS = (
    "orbits.pkl",
    *(f"interpbasis_G_{index}.pkl" for index in range(7)),
    *(f"interpbasis_H_{index}.pkl" for index in range(7)),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not M6.is_dir():
        print("M6 SNAPSHOT AUDIT: FAIL (exploratory/m6 is absent)")
        return 1

    missing = [name for name in REQUIRED_INPUTS if not (M6 / name).is_file()]
    pickles = sorted(M6.glob("*.pkl"))
    print("M6 EXPLORATORY BINARY FILES: HASHED ONLY; NOT DESERIALIZED")
    for path in pickles:
        print(f"  {sha256(path)}  {path.name}")
    print(f"M6 REQUIRED INPUTS MISSING: {len(missing)}")
    for name in missing:
        print(f"  - {name}")
    print(
        "M6 EXPLORATORY STATUS: all-n block and endpoint work remains "
        "incomplete; balanced theorem evidence is under releases/m6-balanced"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
