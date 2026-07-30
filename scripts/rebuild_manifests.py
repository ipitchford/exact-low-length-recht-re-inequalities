#!/usr/bin/env python3
"""Rebuild deterministic SHA-256 manifests after an authorized release edit."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_NAMES = {".DS_Store"}
IGNORED_SUFFIXES = {
    ".aux",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".synctex.gz",
}
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv"}


def included(path: Path, root: Path, destination: Path) -> bool:
    relative = path.relative_to(root)
    if path.resolve() == destination.resolve():
        return False
    if relative.name in IGNORED_NAMES:
        return False
    if any(part in IGNORED_PARTS for part in relative.parts):
        return False
    return not any(relative.name.endswith(suffix) for suffix in IGNORED_SUFFIXES)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(directory: Path, destination: Path) -> int:
    paths = sorted(
        path
        for path in directory.rglob("*")
        if path.is_file() and included(path, directory, destination)
    )
    body = "".join(
        f"{sha256(path)}  ./{path.relative_to(directory).as_posix()}\n"
        for path in paths
    )
    destination.write_text(body, encoding="utf-8")
    return len(paths)


def main() -> int:
    for release_name in ("m4", "m5", "m6-balanced"):
        release = ROOT / f"releases/{release_name}"
        count = write_manifest(release, release / "MANIFEST.sha256")
        print(f"{release_name}: wrote {count} entries")
    count = write_manifest(ROOT, ROOT / "PACKAGE_MANIFEST.sha256")
    print(f"package: wrote {count} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
