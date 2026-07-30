#!/usr/bin/env python3
"""Fail closed when publication metadata disagrees across release surfaces."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0-candidate"
TAG = "v1.0.0-candidate"
DOI = "10.5281/zenodo.21709239"
REPOSITORY = (
    "https://github.com/ipitchford/"
    "exact-low-length-recht-re-inequalities"
)
TITLE = (
    "Exact Low-Length Recht–Ré Inequalities: "
    "paper and exact replication package"
)
ARCHIVE = (
    "exact-low-length-recht-re-inequalities-"
    "v1.0.0-candidate.zip"
)


def load_json(relative: str) -> object:
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{relative}: unreadable JSON: {exc}") from exc


def require_equal(
    failures: list[str],
    label: str,
    actual: object,
    expected: object,
) -> None:
    if actual != expected:
        failures.append(f"{label}: expected {expected!r}, found {actual!r}")


def require_text(
    failures: list[str],
    relative: str,
    fragments: tuple[str, ...],
) -> None:
    path = ROOT / relative
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        failures.append(f"{relative}: unreadable text: {exc}")
        return
    for fragment in fragments:
        if fragment not in text:
            failures.append(f"{relative}: missing {fragment!r}")


def main() -> int:
    failures: list[str] = []

    zenodo = load_json(".zenodo.json")
    if not isinstance(zenodo, dict):
        failures.append(".zenodo.json: top level must be an object")
        zenodo = {}
    require_equal(failures, "Zenodo title", zenodo.get("title"), TITLE)
    require_equal(failures, "Zenodo version", zenodo.get("version"), VERSION)
    require_equal(failures, "Zenodo type", zenodo.get("upload_type"), "software")
    require_equal(failures, "Zenodo license", zenodo.get("license"), "cc0-1.0")
    require_equal(
        failures,
        "Zenodo creators",
        zenodo.get("creators"),
        [{"name": "Anonymous"}],
    )

    index = load_json("AI_INDEX.json")
    if not isinstance(index, dict):
        failures.append("AI_INDEX.json: top level must be an object")
        index = {}
    archival = index.get("archival_record")
    if not isinstance(archival, dict):
        failures.append("AI_INDEX.json: archival_record must be an object")
        archival = {}
    github = index.get("github_release")
    if not isinstance(github, dict):
        failures.append("AI_INDEX.json: github_release must be an object")
        github = {}
    require_equal(failures, "AI index version", index.get("version"), VERSION)
    require_equal(
        failures,
        "AI index archive",
        archival.get("archive_file"),
        ARCHIVE,
    )
    require_equal(
        failures,
        "AI index version DOI",
        archival.get("version_doi"),
        DOI,
    )
    require_equal(failures, "AI index tag", github.get("tag"), TAG)
    require_equal(
        failures,
        "AI index GitHub URL",
        github.get("url"),
        f"{REPOSITORY}/releases/tag/{TAG}",
    )

    require_text(
        failures,
        "CITATION.cff",
        (
            f"  {TITLE}",
            f"version: {VERSION}",
            'authors:\n  - name: "Anonymous"',
            "license: CC0-1.0",
            f'doi: "{DOI}"',
            REPOSITORY,
            f"{REPOSITORY}/releases/tag/{TAG}",
        ),
    )
    require_text(
        failures,
        "README.md",
        (
            DOI,
            REPOSITORY,
            TAG,
            "anonymous unrefereed candidate",
            "CC0-1.0",
            "not formal proof-assistant verification",
        ),
    )
    require_text(
        failures,
        "paper/exact_low_length_recht_re.tex",
        (
            r"\author{Anonymous}",
            DOI,
            REPOSITORY,
            VERSION,
            "CC0-1.0",
            "not treated as independent mathematical verification",
        ),
    )
    require_text(
        failures,
        "LICENSE",
        (
            "CC0 1.0 Universal",
            "Statement of Purpose",
            "Public License Fallback",
        ),
    )
    for relative in (
        "PUBLIC_DOMAIN.md",
        "RELEASE_NOTES.md",
        "AI_INDEX.md",
        "certificate/README.md",
        "scripts/issue_release_certificate.py",
        "scripts/verify_release_certificate.py",
    ):
        if not (ROOT / relative).is_file():
            failures.append(f"{relative}: missing")

    if failures:
        print("RELEASE METADATA: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(
        "RELEASE METADATA: PASS "
        "(anonymous creator, CC0, DOI, tag, archive, and URLs agree)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
