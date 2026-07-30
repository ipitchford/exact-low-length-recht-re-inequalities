#!/usr/bin/env python3
"""Strictly verify the detached certificate, full archive, and Git tag."""

from __future__ import annotations

import argparse
import json
import subprocess
import uuid
import zipfile
from pathlib import Path

from release_certificate_common import (
    ARCHIVE_NAME,
    ARCHIVE_PREFIX,
    ASSURANCE_ASSERTS,
    ASSURANCE_NON_ASSERTS,
    DOI_PATTERN,
    ENVIRONMENT_PREFIX,
    EXCLUSIONS,
    OID_PATTERN,
    PAPER_ASSET_NAME,
    RECORD_URL,
    RELEASE_STATUS,
    RELEASE_TITLE,
    REPLAY_ASSET_NAME,
    REPLAY_COMMAND,
    REPOSITORY_URL,
    SCHEMA,
    SHA256_PATTERN,
    SLUG,
    SUBJECT_SPECS,
    TAG,
    TERMINAL_MARKER,
    VERSION,
    VERSION_DOI,
    bind_archive_to_git,
    inspect_archive,
    inspect_git,
    rfc3339,
    safe_relative,
    sha256,
    sha256_bytes,
)


TOP_LEVEL_FIELDS = {
    "assurance",
    "certificate_id",
    "exclusions",
    "generated_at",
    "git",
    "publication",
    "release",
    "replay",
    "schema",
    "subjects",
    "zip_inventory",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--sidecar", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--paper", type=Path, required=True)
    parser.add_argument("--replay-log", type=Path, required=True)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    return parser.parse_args()


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def mapping(
    parent: object,
    key: str,
    failures: list[str],
) -> dict[str, object]:
    if not isinstance(parent, dict):
        failures.append(f"{key}: parent must be an object")
        return {}
    value = parent.get(key)
    if not isinstance(value, dict):
        failures.append(f"{key}: must be an object")
        return {}
    return value


def exact_keys(
    value: dict[str, object],
    expected: set[str],
    label: str,
    failures: list[str],
) -> None:
    if set(value) != expected:
        failures.append(
            f"{label}: unexpected fields "
            f"{sorted(set(value) ^ expected)!r}"
        )


def validate_subject_file(
    item: dict[str, object],
    path: Path,
    failures: list[str],
) -> None:
    role = str(item.get("role", "unknown"))
    if not path.is_file():
        failures.append(f"{role}: missing {path}")
        return
    if item.get("name") != path.name:
        failures.append(f"{role}: filename mismatch")
    if item.get("bytes") != path.stat().st_size:
        failures.append(f"{role}: byte-count mismatch")
    if item.get("sha256") != sha256(path):
        failures.append(f"{role}: SHA-256 mismatch")


def validate_nested_schema(
    certificate: dict[str, object],
    failures: list[str],
) -> tuple[
    dict[str, dict[str, object]],
    dict[str, object],
    dict[str, object],
]:
    exact_keys(certificate, TOP_LEVEL_FIELDS, "certificate", failures)
    if certificate.get("schema") != SCHEMA:
        failures.append("unsupported certificate schema")

    assurance = mapping(certificate, "assurance", failures)
    exact_keys(
        assurance,
        {"asserts", "does_not_assert"},
        "assurance",
        failures,
    )
    if assurance.get("asserts") != ASSURANCE_ASSERTS:
        failures.append("assurance.asserts differs from the release schema")
    if assurance.get("does_not_assert") != ASSURANCE_NON_ASSERTS:
        failures.append(
            "assurance.does_not_assert differs from the release schema"
        )
    exclusions = mapping(certificate, "exclusions", failures)
    if exclusions != EXCLUSIONS:
        failures.append("exclusions differ from the release schema")

    generated_at = certificate.get("generated_at")
    if not isinstance(generated_at, str):
        failures.append("generated_at must be a string")
        generated_time = None
    else:
        try:
            generated_time = rfc3339(generated_at, "generated_at")
        except ValueError as exc:
            failures.append(str(exc))
            generated_time = None

    release = mapping(certificate, "release", failures)
    expected_release = {
        "slug": SLUG,
        "status": RELEASE_STATUS,
        "title": RELEASE_TITLE,
        "version": VERSION,
    }
    if release != expected_release:
        failures.append("release identity differs from the frozen release")

    git_record = mapping(certificate, "git", failures)
    exact_keys(
        git_record,
        {"commit", "object_format", "repository", "tag", "tree"},
        "git",
        failures,
    )
    if git_record.get("repository") != REPOSITORY_URL:
        failures.append("Git repository URL differs")
    object_format = git_record.get("object_format")
    oid_length = {"sha1": 40, "sha256": 64}.get(object_format)
    if oid_length is None:
        failures.append("unsupported Git object format")
    for field in ("commit", "tree"):
        value = git_record.get(field)
        if (
            not isinstance(value, str)
            or not OID_PATTERN.fullmatch(value)
            or (oid_length is not None and len(value) != oid_length)
        ):
            failures.append(f"git.{field} is not a valid object ID")
    tag_record = mapping(git_record, "tag", failures)
    exact_keys(
        tag_record,
        {"annotated", "name", "object", "signature_status"},
        "git.tag",
        failures,
    )
    if tag_record.get("annotated") is not True:
        failures.append("Git tag must be declared annotated")
    if tag_record.get("name") != TAG:
        failures.append("Git tag name differs")
    tag_object = tag_record.get("object")
    if (
        not isinstance(tag_object, str)
        or not OID_PATTERN.fullmatch(tag_object)
        or (oid_length is not None and len(tag_object) != oid_length)
    ):
        failures.append("git.tag.object is not a valid object ID")
    if tag_record.get("signature_status") not in {"unsigned", "verified"}:
        failures.append("Git tag signature status is invalid")

    publication = mapping(certificate, "publication", failures)
    exact_keys(
        publication,
        {"github", "zenodo"},
        "publication",
        failures,
    )
    github = mapping(publication, "github", failures)
    expected_github = {
        "release_url": f"{REPOSITORY_URL}/releases/tag/{TAG}",
        "tag": TAG,
    }
    if github != expected_github:
        failures.append("GitHub publication locator differs")
    zenodo = mapping(publication, "zenodo", failures)
    exact_keys(
        zenodo,
        {"concept_doi", "record_url", "version_doi"},
        "publication.zenodo",
        failures,
    )
    if zenodo.get("version_doi") != VERSION_DOI:
        failures.append("Zenodo version DOI differs")
    if zenodo.get("record_url") != RECORD_URL:
        failures.append("Zenodo record URL differs")
    concept_doi = zenodo.get("concept_doi")
    if concept_doi is not None and (
        not isinstance(concept_doi, str)
        or not DOI_PATTERN.fullmatch(concept_doi)
        or concept_doi == VERSION_DOI
    ):
        failures.append("Zenodo concept DOI is invalid")

    replay = mapping(certificate, "replay", failures)
    exact_keys(
        replay,
        {
            "command",
            "completed_at",
            "environment_result",
            "evidence_kind",
            "exit_code",
            "fresh_extraction",
            "result",
            "terminal_marker",
        },
        "replay",
        failures,
    )
    expected_replay = {
        "command": REPLAY_COMMAND,
        "evidence_kind": "publisher-recorded deterministic replay",
        "exit_code": 0,
        "fresh_extraction": True,
        "result": "pass",
        "terminal_marker": TERMINAL_MARKER,
    }
    for field, expected in expected_replay.items():
        actual = replay.get(field)
        if field == "exit_code":
            valid = type(actual) is int and actual == expected
        else:
            valid = actual == expected
        if not valid:
            failures.append(f"replay.{field} differs")
    environment_result = replay.get("environment_result")
    if (
        not isinstance(environment_result, str)
        or not environment_result.startswith(ENVIRONMENT_PREFIX)
    ):
        failures.append("replay.environment_result is invalid")
    completed_at = replay.get("completed_at")
    if not isinstance(completed_at, str):
        failures.append("replay.completed_at must be a string")
        completed_time = None
    else:
        try:
            completed_time = rfc3339(
                completed_at,
                "replay.completed_at",
            )
        except ValueError as exc:
            failures.append(str(exc))
            completed_time = None
    if (
        generated_time is not None
        and completed_time is not None
        and completed_time > generated_time
    ):
        failures.append("replay completion is later than issuance")

    subjects = certificate.get("subjects")
    if not isinstance(subjects, list):
        failures.append("subjects must be a list")
        subjects = []
    by_role: dict[str, dict[str, object]] = {}
    for item in subjects:
        if not isinstance(item, dict) or not isinstance(item.get("role"), str):
            failures.append("malformed subject")
            continue
        role = str(item["role"])
        if role in by_role:
            failures.append(f"duplicate subject role: {role}")
            continue
        by_role[role] = item
    if set(by_role) != set(SUBJECT_SPECS):
        failures.append(
            "subject roles differ: "
            f"{sorted(set(by_role) ^ set(SUBJECT_SPECS))!r}"
        )
    for role, (name, media_type, git_path) in SUBJECT_SPECS.items():
        item = by_role.get(role)
        if item is None:
            continue
        expected_fields = {"bytes", "media_type", "name", "role", "sha256"}
        if git_path is not None:
            expected_fields |= {"archive_member", "git_path"}
        exact_keys(item, expected_fields, f"subject.{role}", failures)
        if item.get("name") != name:
            failures.append(f"{role}: declared filename differs")
        if item.get("media_type") != media_type:
            failures.append(f"{role}: media type differs")
        byte_count = item.get("bytes")
        if type(byte_count) is not int or byte_count < 0:
            failures.append(f"{role}: bytes must be a nonnegative integer")
        digest = item.get("sha256")
        if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
            failures.append(f"{role}: malformed SHA-256")
        if git_path is not None:
            try:
                safe_relative(git_path, f"{role}.git_path")
            except ValueError as exc:
                failures.append(str(exc))
            if item.get("git_path") != git_path:
                failures.append(f"{role}: Git path differs")
            expected_member = f"{ARCHIVE_PREFIX}/{git_path}"
            if item.get("archive_member") != expected_member:
                failures.append(f"{role}: archive member locator differs")

    zip_inventory = mapping(certificate, "zip_inventory", failures)
    exact_keys(
        zip_inventory,
        {"member_count", "top_level_directory"},
        "zip_inventory",
        failures,
    )
    member_count = zip_inventory.get("member_count")
    if type(member_count) is not int or member_count <= 0:
        failures.append("zip_inventory.member_count must be positive")
    if zip_inventory.get("top_level_directory") != ARCHIVE_PREFIX:
        failures.append("archive top-level directory differs")
    return by_role, git_record, replay


def validate_replay_log(
    path: Path,
    replay: dict[str, object],
    failures: list[str],
) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        failures.append(f"unreadable replay transcript: {exc}")
        return
    lines = text.rstrip().splitlines()
    if not lines or lines[-1] != TERMINAL_MARKER:
        failures.append("replay transcript lacks the exact terminal PASS line")
    environment = [
        line.strip()
        for line in lines
        if line.strip().startswith(ENVIRONMENT_PREFIX)
    ]
    if len(environment) != 1:
        failures.append(
            "replay transcript must contain one detailed environment line"
        )
    elif environment[0] != replay.get("environment_result"):
        failures.append("replay environment line differs from certificate")


def validate_source_root(
    source_root: Path,
    expected_hashes: dict[str, str],
    failures: list[str],
) -> None:
    try:
        root = source_root.resolve(strict=True)
    except OSError as exc:
        failures.append(f"source root is unreadable: {exc}")
        return
    actual: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        if path.is_symlink():
            failures.append(f"source root contains symlink: {relative}")
            continue
        if path.is_file():
            actual.add(relative.as_posix())
    expected = set(expected_hashes)
    if actual != expected:
        failures.append(
            "source-root/archive file sets differ: "
            f"missing={sorted(expected - actual)!r}, "
            f"extra={sorted(actual - expected)!r}"
        )
    for relative, expected_digest in expected_hashes.items():
        try:
            safe_relative(relative, "source-root subject")
            candidate = (root / relative).resolve(strict=True)
        except (OSError, ValueError) as exc:
            failures.append(f"source-root path rejected: {relative}: {exc}")
            continue
        if not candidate.is_relative_to(root):
            failures.append(f"source-root path escapes root: {relative}")
        elif not candidate.is_file():
            failures.append(f"source-root subject missing: {relative}")
        elif sha256(candidate) != expected_digest:
            failures.append(f"source-root SHA-256 mismatch: {relative}")


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    try:
        certificate_bytes = args.certificate.read_bytes()
        certificate = json.loads(
            certificate_bytes,
            object_pairs_hook=unique_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"PUBLICATION CERTIFICATE: FAIL\n  - unreadable certificate: {exc}")
        return 1
    if not isinstance(certificate, dict):
        print("PUBLICATION CERTIFICATE: FAIL\n  - certificate must be an object")
        return 1

    try:
        sidecar_parts = (
            args.sidecar.read_text(encoding="utf-8").strip().split()
        )
    except (OSError, UnicodeDecodeError) as exc:
        failures.append(f"unreadable certificate SHA-256 sidecar: {exc}")
    else:
        if len(sidecar_parts) != 2:
            failures.append("malformed certificate SHA-256 sidecar")
        else:
            expected, filename = sidecar_parts
            if filename != args.certificate.name:
                failures.append("sidecar certificate filename mismatch")
            if not SHA256_PATTERN.fullmatch(expected):
                failures.append("sidecar contains malformed SHA-256")
            elif expected != sha256_bytes(certificate_bytes):
                failures.append("certificate SHA-256 sidecar mismatch")

    by_role, git_record, replay = validate_nested_schema(
        certificate,
        failures,
    )
    for role, path in (
        ("paper_pdf", args.paper),
        ("replication_archive", args.archive),
        ("replay_transcript", args.replay_log),
    ):
        item = by_role.get(role)
        if item is not None:
            validate_subject_file(item, path, failures)
    validate_replay_log(args.replay_log, replay, failures)

    try:
        archive_snapshot = inspect_archive(args.archive)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        failures.append(f"archive validation failed: {exc}")
        archive_snapshot = None
    if archive_snapshot is not None:
        zip_inventory = certificate.get("zip_inventory", {})
        if isinstance(zip_inventory, dict) and (
            zip_inventory.get("member_count")
            != archive_snapshot.member_count
        ):
            failures.append("archive member count differs")
        paper_digest = by_role.get("paper_pdf", {}).get("sha256")
        if (
            archive_snapshot.file_hashes.get(
                "paper/exact_low_length_recht_re.pdf"
            )
            != paper_digest
        ):
            failures.append("archive paper differs from release PDF")
        for role, (_, _, git_path) in SUBJECT_SPECS.items():
            if git_path is None:
                continue
            if (
                archive_snapshot.file_hashes.get(git_path)
                != by_role.get(role, {}).get("sha256")
            ):
                failures.append(f"{role}: archive member SHA-256 mismatch")

    try:
        git_snapshot = inspect_git(args.repository)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        failures.append(f"Git tag validation failed: {exc}")
        git_snapshot = None
    if archive_snapshot is not None and git_snapshot is not None:
        try:
            bind_archive_to_git(archive_snapshot, git_snapshot)
        except ValueError as exc:
            failures.append(str(exc))
        expected_git = {
            "commit": git_snapshot.commit,
            "object_format": git_snapshot.object_format,
            "repository": REPOSITORY_URL,
            "tag": {
                "annotated": True,
                "name": TAG,
                "object": git_snapshot.tag_object,
                "signature_status": git_snapshot.signature_status,
            },
            "tree": git_snapshot.tree,
        }
        if git_record != expected_git:
            failures.append("certificate Git record differs from checked tag")

    archive_subject = by_role.get("replication_archive", {})
    archive_digest = archive_subject.get("sha256")
    commit = git_record.get("commit")
    certificate_id = certificate.get("certificate_id")
    if isinstance(archive_digest, str) and isinstance(commit, str):
        key = f"{REPOSITORY_URL}|{TAG}|{commit}|{archive_digest}"
        expected_id = "urn:uuid:" + str(
            uuid.uuid5(uuid.NAMESPACE_URL, key)
        )
        if certificate_id != expected_id:
            failures.append("certificate_id is not the deterministic UUID")
    else:
        failures.append("certificate_id inputs are malformed")

    if args.source_root and archive_snapshot is not None:
        validate_source_root(
            args.source_root,
            archive_snapshot.file_hashes,
            failures,
        )

    if failures:
        print("PUBLICATION CERTIFICATE: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(
        "PUBLICATION CERTIFICATE: PASS "
        "(annotated tag, full Git tree, complete manifest/archive, "
        "subjects, and exact replay)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
