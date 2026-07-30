#!/usr/bin/env python3
"""Issue the strict outer certificate for the frozen candidate release."""

from __future__ import annotations

import argparse
import hashlib
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
    INTERNAL_PATHS,
    PAPER_ASSET_NAME,
    RECORD_URL,
    RELEASE_STATUS,
    RELEASE_TITLE,
    REPLAY_ASSET_NAME,
    REPLAY_COMMAND,
    REPOSITORY_URL,
    SCHEMA,
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
    run_git,
    sha256,
)


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--paper", type=Path, required=True)
    parser.add_argument("--replay-log", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sidecar", type=Path)
    parser.add_argument("--repository-url", default=REPOSITORY_URL)
    parser.add_argument("--tag", default=TAG)
    parser.add_argument("--version", default=VERSION)
    parser.add_argument("--version-doi", default=VERSION_DOI)
    parser.add_argument("--concept-doi")
    parser.add_argument("--record-url", default=RECORD_URL)
    parser.add_argument("--issued-at", required=True)
    parser.add_argument("--replay-completed-at", required=True)
    return parser.parse_args()


def subject(role: str, path: Path, media_type: str) -> dict[str, object]:
    return {
        "bytes": path.stat().st_size,
        "media_type": media_type,
        "name": path.name,
        "role": role,
        "sha256": sha256(path),
    }


def require_release_constants(args: argparse.Namespace) -> None:
    observed = {
        "repository-url": args.repository_url,
        "tag": args.tag,
        "version": args.version,
        "version-doi": args.version_doi,
        "record-url": args.record_url,
    }
    expected = {
        "repository-url": REPOSITORY_URL,
        "tag": TAG,
        "version": VERSION,
        "version-doi": VERSION_DOI,
        "record-url": RECORD_URL,
    }
    for label, expected_value in expected.items():
        if observed[label] != expected_value:
            raise ValueError(
                f"{label} must be {expected_value!r}, "
                f"found {observed[label]!r}"
            )
    if args.concept_doi is not None:
        if not DOI_PATTERN.fullmatch(args.concept_doi):
            raise ValueError(f"invalid concept DOI: {args.concept_doi}")
        if args.concept_doi == VERSION_DOI:
            raise ValueError("concept DOI must differ from the version DOI")


def require_output_safety(
    args: argparse.Namespace,
    sidecar: Path,
) -> None:
    inputs = {
        args.archive.resolve(),
        args.paper.resolve(),
        args.replay_log.resolve(),
    }
    output = args.output.resolve()
    detached = sidecar.resolve()
    if output == detached:
        raise ValueError("certificate and sidecar paths must differ")
    if output in inputs or detached in inputs:
        raise ValueError("certificate outputs must not overwrite an input")
    repository = ROOT.resolve()
    for label, path in (("certificate", output), ("sidecar", detached)):
        if path.is_relative_to(repository):
            raise ValueError(
                f"{label} must be outside the certified repository: {path}"
            )


def replay_environment(text: str) -> str:
    lines = text.rstrip().splitlines()
    if not lines or lines[-1] != TERMINAL_MARKER:
        raise ValueError("replay log lacks the exact terminal PASS line")
    environment = [
        line.strip()
        for line in lines
        if line.strip().startswith(ENVIRONMENT_PREFIX)
    ]
    if len(environment) != 1:
        raise ValueError(
            "replay log must contain exactly one detailed environment "
            "PASS line"
        )
    return environment[0]


def issue(args: argparse.Namespace) -> tuple[bytes, Path]:
    require_release_constants(args)
    for label, path, expected_name in (
        ("archive", args.archive, ARCHIVE_NAME),
        ("paper", args.paper, PAPER_ASSET_NAME),
        ("replay log", args.replay_log, REPLAY_ASSET_NAME),
    ):
        if not path.is_file():
            raise ValueError(f"missing {label}: {path}")
        if path.name != expected_name:
            raise ValueError(
                f"{label} filename must be {expected_name!r}, "
                f"found {path.name!r}"
            )

    issued_at = rfc3339(args.issued_at, "issued-at")
    completed_at = rfc3339(
        args.replay_completed_at,
        "replay-completed-at",
    )
    if completed_at > issued_at:
        raise ValueError("replay completion cannot be later than issuance")

    sidecar = args.sidecar or args.output.with_suffix(
        args.output.suffix + ".sha256"
    )
    require_output_safety(args, sidecar)
    if run_git(
        ROOT,
        ["status", "--porcelain", "--untracked-files=all"],
    ).stdout.strip():
        raise ValueError("repository must be clean before certificate issuance")

    archive_snapshot = inspect_archive(args.archive)
    git_snapshot = inspect_git(ROOT)
    head = run_git(ROOT, ["rev-parse", "HEAD"]).stdout.strip()
    if git_snapshot.commit != head:
        raise ValueError("annotated release tag must peel to the current HEAD")
    bind_archive_to_git(archive_snapshot, git_snapshot)

    replay_text = args.replay_log.read_text(encoding="utf-8")
    environment_result = replay_environment(replay_text)
    paper = subject("paper_pdf", args.paper, "application/pdf")
    archive = subject(
        "replication_archive",
        args.archive,
        "application/zip",
    )
    replay = subject(
        "replay_transcript",
        args.replay_log,
        "text/plain",
    )
    paper_member = "paper/exact_low_length_recht_re.pdf"
    if archive_snapshot.file_hashes.get(paper_member) != paper["sha256"]:
        raise ValueError("archive paper does not match the release PDF")

    internal_subjects: list[dict[str, object]] = []
    for role, relative in INTERNAL_PATHS.items():
        path = ROOT / relative
        if not path.is_file():
            raise ValueError(f"missing internal subject: {relative}")
        media_type = SUBJECT_SPECS[role][1]
        item = subject(role, path, media_type)
        item["git_path"] = relative
        item["archive_member"] = f"{ARCHIVE_PREFIX}/{relative}"
        if archive_snapshot.file_hashes.get(relative) != item["sha256"]:
            raise ValueError(f"archive member mismatch: {relative}")
        internal_subjects.append(item)

    certificate_key = (
        f"{REPOSITORY_URL}|{TAG}|{git_snapshot.commit}|{archive['sha256']}"
    )
    certificate_id = "urn:uuid:" + str(
        uuid.uuid5(uuid.NAMESPACE_URL, certificate_key)
    )
    certificate = {
        "assurance": {
            "asserts": ASSURANCE_ASSERTS,
            "does_not_assert": ASSURANCE_NON_ASSERTS,
        },
        "certificate_id": certificate_id,
        "exclusions": EXCLUSIONS,
        "generated_at": args.issued_at,
        "git": {
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
        },
        "publication": {
            "github": {
                "release_url": f"{REPOSITORY_URL}/releases/tag/{TAG}",
                "tag": TAG,
            },
            "zenodo": {
                "concept_doi": args.concept_doi,
                "record_url": RECORD_URL,
                "version_doi": VERSION_DOI,
            },
        },
        "release": {
            "slug": SLUG,
            "status": RELEASE_STATUS,
            "title": RELEASE_TITLE,
            "version": VERSION,
        },
        "replay": {
            "command": REPLAY_COMMAND,
            "completed_at": args.replay_completed_at,
            "environment_result": environment_result,
            "evidence_kind": "publisher-recorded deterministic replay",
            "exit_code": 0,
            "fresh_extraction": True,
            "result": "pass",
            "terminal_marker": TERMINAL_MARKER,
        },
        "schema": SCHEMA,
        "subjects": [paper, archive, replay, *internal_subjects],
        "zip_inventory": {
            "member_count": archive_snapshot.member_count,
            "top_level_directory": ARCHIVE_PREFIX,
        },
    }
    encoded = (
        json.dumps(
            certificate,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    return encoded, sidecar


def main() -> int:
    args = parse_args()
    try:
        encoded, sidecar = issue(args)
    except (
        OSError,
        UnicodeDecodeError,
        ValueError,
        zipfile.BadZipFile,
        subprocess.CalledProcessError,
    ) as exc:
        raise SystemExit(f"PUBLICATION CERTIFICATE: REFUSED\n  - {exc}") from exc

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded)
    digest = hashlib.sha256(encoded).hexdigest()
    sidecar.write_text(
        f"{digest}  {args.output.name}\n",
        encoding="utf-8",
    )
    certificate_id = json.loads(encoded)["certificate_id"]
    print(f"PUBLICATION CERTIFICATE: ISSUED {certificate_id}")
    print(f"certificate sha256: {digest}")
    print(f"sidecar: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
