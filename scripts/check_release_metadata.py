#!/usr/bin/env python3
"""Fail closed when publication metadata disagrees across release surfaces."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0-candidate"
TAG = "v1.0.0-candidate"
DOI = "10.5281/zenodo.21709239"
CONCEPT_DOI = "10.5281/zenodo.21709238"
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
READBACK_SCHEMA = "recht-re.publication-readback/v1"
TAG_COMMIT = "e004658c83a71353983e67796d3dc07383e904ef"
TAG_OBJECT = "768d45469f4d0d4cbf9f2bf295a419084a7faf62"
CERTIFICATE_ID = "urn:uuid:30242f7b-e18e-50b5-bedc-bb038657a530"
CERTIFICATE_SHA256 = (
    "739ab30b0bb8358a177886b49955c7cf4d40cd65b0f4fad04ceb1d1b859cc79d"
)
EXPECTED_ASSETS = {
    "SHA256SUMS.txt": (
        585,
        "2431ba0216796c40f1a9da0052ad68726bdee9c24161ed7904caf07e824e1f8a",
    ),
    "exact-low-length-recht-re-inequalities-v1.0.0-candidate.pdf": (
        433901,
        "d02949d1a6bd61244a07d0428bec8079a656e78fed17e9bd459ff7d9b120148b",
    ),
    "exact-low-length-recht-re-inequalities-v1.0.0-candidate.zip": (
        2129414,
        "09a4817cd89b10afea7d6b59b074605041bbb40986c70eb54d29e34481ba8a5b",
    ),
    "publication-certificate-v1.0.0-candidate.json": (
        5710,
        CERTIFICATE_SHA256,
    ),
    "publication-certificate-v1.0.0-candidate.json.sha256": (
        112,
        "4a6f6b39f610ff283a5620a5d72b7ea357777ffe06ed271828b98fea147297b4",
    ),
    "release-replay-v1.0.0-candidate.txt": (
        1098,
        "661478fa4fcd1a1fd7495b1a747fde713589f35882f4902bd28841604d22c7e1",
    ),
}
EXPECTED_READBACK_CHECKS = {
    "all_six_assets_downloaded_without_authentication": True,
    "all_six_assets_match_across_local_github_and_zenodo": True,
    "github_immutable_release_attestation_verified": True,
    "github_public_clone_has_one_parentless_anonymous_commit": True,
    "github_release_asset_attestations_verified": True,
    "strict_certificate_verified_against_public_clone_and_fresh_zenodo_extraction": True,
    "zenodo_public_api_metadata_verified": True,
}


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
    require_equal(
        failures,
        "AI index concept DOI",
        archival.get("concept_doi"),
        CONCEPT_DOI,
    )
    require_equal(failures, "AI index tag", github.get("tag"), TAG)
    require_equal(
        failures,
        "AI index GitHub URL",
        github.get("url"),
        f"{REPOSITORY}/releases/tag/{TAG}",
    )

    readback = load_json("PUBLICATION_READBACK.json")
    if not isinstance(readback, dict):
        failures.append(
            "PUBLICATION_READBACK.json: top level must be an object"
        )
        readback = {}
    readback_release = readback.get("release")
    if not isinstance(readback_release, dict):
        failures.append(
            "PUBLICATION_READBACK.json: release must be an object"
        )
        readback_release = {}
    readback_github = readback.get("github")
    if not isinstance(readback_github, dict):
        failures.append(
            "PUBLICATION_READBACK.json: github must be an object"
        )
        readback_github = {}
    readback_zenodo = readback.get("zenodo")
    if not isinstance(readback_zenodo, dict):
        failures.append(
            "PUBLICATION_READBACK.json: zenodo must be an object"
        )
        readback_zenodo = {}
    readback_certificate = readback.get("certificate")
    if not isinstance(readback_certificate, dict):
        failures.append(
            "PUBLICATION_READBACK.json: certificate must be an object"
        )
        readback_certificate = {}

    require_equal(
        failures,
        "public readback schema",
        readback.get("schema"),
        READBACK_SCHEMA,
    )
    require_equal(
        failures,
        "public readback version",
        readback_release.get("version"),
        VERSION,
    )
    require_equal(
        failures,
        "public readback tag",
        readback_release.get("tag"),
        TAG,
    )
    require_equal(
        failures,
        "public readback tag commit",
        readback_release.get("commit"),
        TAG_COMMIT,
    )
    require_equal(
        failures,
        "public readback tag object",
        readback_release.get("tag_object"),
        TAG_OBJECT,
    )
    require_equal(
        failures,
        "public readback parent count",
        readback_release.get("commit_parent_count"),
        0,
    )
    require_equal(
        failures,
        "public GitHub visibility",
        readback_github.get("visibility"),
        "public",
    )
    require_equal(
        failures,
        "public GitHub immutable status",
        readback_github.get("immutable"),
        True,
    )
    require_equal(
        failures,
        "public GitHub prerelease status",
        readback_github.get("prerelease"),
        True,
    )
    require_equal(
        failures,
        "public GitHub release URL",
        readback_github.get("release_url"),
        f"{REPOSITORY}/releases/tag/{TAG}",
    )
    require_equal(
        failures,
        "public Zenodo version DOI",
        readback_zenodo.get("version_doi"),
        DOI,
    )
    require_equal(
        failures,
        "public Zenodo concept DOI",
        readback_zenodo.get("concept_doi"),
        CONCEPT_DOI,
    )
    require_equal(
        failures,
        "public Zenodo creator",
        readback_zenodo.get("creator"),
        "Anonymous",
    )
    require_equal(
        failures,
        "public Zenodo license",
        readback_zenodo.get("license"),
        "cc-zero",
    )
    require_equal(
        failures,
        "public certificate ID",
        readback_certificate.get("certificate_id"),
        CERTIFICATE_ID,
    )
    require_equal(
        failures,
        "public certificate SHA-256",
        readback_certificate.get("certificate_sha256"),
        CERTIFICATE_SHA256,
    )
    require_equal(
        failures,
        "public certificate concept DOI",
        readback_certificate.get("concept_doi_in_certificate"),
        None,
    )
    require_equal(
        failures,
        "public certificate verification",
        readback_certificate.get("strict_public_verification"),
        True,
    )
    require_equal(
        failures,
        "public readback checks",
        readback.get("checks"),
        EXPECTED_READBACK_CHECKS,
    )

    assets = readback.get("assets")
    asset_map: dict[str, dict[str, object]] = {}
    if not isinstance(assets, list):
        failures.append(
            "PUBLICATION_READBACK.json: assets must be an array"
        )
        assets = []
    for position, asset in enumerate(assets):
        if not isinstance(asset, dict):
            failures.append(
                f"PUBLICATION_READBACK.json: asset {position} "
                "must be an object"
            )
            continue
        name = asset.get("name")
        if not isinstance(name, str) or not name:
            failures.append(
                f"PUBLICATION_READBACK.json: asset {position} "
                "has no valid name"
            )
            continue
        if name in asset_map:
            failures.append(
                f"PUBLICATION_READBACK.json: duplicate asset {name!r}"
            )
            continue
        asset_map[name] = asset
    require_equal(
        failures,
        "public readback asset names",
        set(asset_map),
        set(EXPECTED_ASSETS),
    )
    for name, (expected_bytes, expected_sha256) in EXPECTED_ASSETS.items():
        asset = asset_map.get(name, {})
        require_equal(
            failures,
            f"{name} bytes",
            asset.get("bytes"),
            expected_bytes,
        )
        require_equal(
            failures,
            f"{name} SHA-256",
            asset.get("sha256"),
            expected_sha256,
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
            CONCEPT_DOI,
            REPOSITORY,
            f"{REPOSITORY}/releases/tag/{TAG}",
        ),
    )
    require_text(
        failures,
        "README.md",
        (
            DOI,
            CONCEPT_DOI,
            REPOSITORY,
            TAG,
            "PUBLICATION_READBACK.json",
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
        "(anonymous creator, CC0, DOIs, tag, assets, and public readback agree)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
