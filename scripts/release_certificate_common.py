#!/usr/bin/env python3
"""Shared strict primitives for the detached publication certificate."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import re
import stat
import subprocess
import zipfile
from pathlib import Path, PurePosixPath


SCHEMA = "publication-certificate/1.0"
VERSION = "1.0.0-candidate"
TAG = "v1.0.0-candidate"
SLUG = "exact-low-length-recht-re-inequalities"
REPOSITORY_URL = f"https://github.com/ipitchford/{SLUG}"
VERSION_DOI = "10.5281/zenodo.21709239"
RECORD_URL = "https://zenodo.org/records/21709239"
RELEASE_TITLE = "Exact Low-Length Recht–Ré Inequalities"
RELEASE_STATUS = "anonymous unrefereed candidate"
ARCHIVE_PREFIX = f"{SLUG}-{TAG}"
ARCHIVE_NAME = f"{ARCHIVE_PREFIX}.zip"
PAPER_ASSET_NAME = f"{ARCHIVE_PREFIX}.pdf"
REPLAY_ASSET_NAME = f"release-replay-{TAG}.txt"
ZIP_TIME = (2026, 7, 30, 12, 0, 0)
TERMINAL_MARKER = "PUBLICATION-CANDIDATE REPLAY: PASS"
ENVIRONMENT_PREFIX = "REPLICATION ENVIRONMENT: PASS "
DOI_PATTERN = re.compile(r"10\.5281/zenodo\.\d+\Z")
OID_PATTERN = re.compile(r"[0-9a-f]{40,64}\Z")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
RFC3339_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\Z"
)
MANIFEST_LINE = re.compile(r"([0-9a-f]{64})  \./(.+)\Z")
FORBIDDEN_ARCHIVE_PARTS = {
    ".git",
    ".venv",
    "__MACOSX",
    "__pycache__",
}
REPLAY_COMMAND = [
    "python3 -m venv .venv",
    (
        ".venv/bin/python -m pip install "
        "-r environment/requirements-lock.txt"
    ),
    ".venv/bin/python scripts/replay_all.py --python .venv/bin/python",
]
ASSURANCE_ASSERTS = [
    "byte identity of the declared subjects",
    "the declared Git tag-to-commit binding",
    "the publisher-recorded deterministic replay outcome",
    "the intended GitHub and Zenodo locators",
]
ASSURANCE_NON_ASSERTS = [
    "mathematical correctness or novelty",
    "semantic completeness of the encodings",
    "formal verification",
    "independent external reproduction",
    "external peer review or journal acceptance",
    "accountable authorship",
    "publication priority",
]
EXCLUSIONS = {
    "certificate_hash_is_detached": True,
    "certificate_is_outside_payload": True,
    "hosting_metadata_is_not_immutable_content": True,
}
INTERNAL_PATHS = {
    "paper_source": "paper/exact_low_length_recht_re.tex",
    "root_manifest": "PACKAGE_MANIFEST.sha256",
    "m4_manifest": "releases/m4/MANIFEST.sha256",
    "m5_manifest": "releases/m5/MANIFEST.sha256",
    "m6_manifest": "releases/m6-balanced/MANIFEST.sha256",
    "replay_receipt": "REPLAY_RECEIPT_2026-07-30.md",
}
SUBJECT_SPECS = {
    "paper_pdf": (PAPER_ASSET_NAME, "application/pdf", None),
    "replication_archive": (ARCHIVE_NAME, "application/zip", None),
    "replay_transcript": (REPLAY_ASSET_NAME, "text/plain", None),
    "paper_source": (
        "exact_low_length_recht_re.tex",
        "application/x-tex",
        INTERNAL_PATHS["paper_source"],
    ),
    "root_manifest": (
        "PACKAGE_MANIFEST.sha256",
        "text/plain",
        INTERNAL_PATHS["root_manifest"],
    ),
    "m4_manifest": (
        "MANIFEST.sha256",
        "text/plain",
        INTERNAL_PATHS["m4_manifest"],
    ),
    "m5_manifest": (
        "MANIFEST.sha256",
        "text/plain",
        INTERNAL_PATHS["m5_manifest"],
    ),
    "m6_manifest": (
        "MANIFEST.sha256",
        "text/plain",
        INTERNAL_PATHS["m6_manifest"],
    ),
    "replay_receipt": (
        "REPLAY_RECEIPT_2026-07-30.md",
        "text/markdown",
        INTERNAL_PATHS["replay_receipt"],
    ),
}


@dataclass(frozen=True)
class ArchiveSnapshot:
    file_hashes: dict[str, str]
    file_modes: dict[str, int]
    manifest: dict[str, str]
    manifest_bytes: bytes
    member_count: int
    prefix: str


@dataclass(frozen=True)
class GitSnapshot:
    commit: str
    file_hashes: dict[str, str]
    file_modes: dict[str, int]
    object_format: str
    signature_status: str
    tag_object: str
    tree: str


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rfc3339(value: str, label: str) -> datetime:
    if not RFC3339_PATTERN.fullmatch(value):
        raise ValueError(f"{label} is not an RFC 3339 timestamp: {value!r}")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a UTC offset")
    return parsed


def safe_relative(value: str, label: str) -> str:
    if not value or "\\" in value:
        raise ValueError(f"{label}: unsafe path {value!r}")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or any(part in {"", ".", ".."} for part in pure.parts)
        or pure.as_posix() != value
    ):
        raise ValueError(f"{label}: unsafe path {value!r}")
    if any(part in FORBIDDEN_ARCHIVE_PARTS for part in pure.parts):
        raise ValueError(f"{label}: forbidden path {value!r}")
    return value


def parse_manifest(data: bytes) -> dict[str, str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"root manifest is not UTF-8: {exc}") from exc
    listed: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        match = MANIFEST_LINE.fullmatch(line)
        if not match:
            raise ValueError(
                f"root manifest line {line_number} is malformed"
            )
        digest, relative = match.groups()
        safe_relative(relative, f"root manifest line {line_number}")
        if relative == "PACKAGE_MANIFEST.sha256":
            raise ValueError("root manifest must not list itself")
        if relative in listed:
            raise ValueError(f"duplicate root-manifest path: {relative}")
        listed[relative] = digest
    if not listed:
        raise ValueError("root manifest is empty")
    return listed


def _unsafe_zip_type(member: zipfile.ZipInfo) -> str | None:
    mode = member.external_attr >> 16
    if not mode:
        return "missing Unix file mode"
    if stat.S_ISLNK(mode):
        return "symbolic link"
    if member.is_dir() and stat.S_ISDIR(mode):
        return None
    if not member.is_dir() and stat.S_ISREG(mode):
        return None
    return f"special file mode {mode:o}"


def inspect_archive(path: Path) -> ArchiveSnapshot:
    seen: set[str] = set()
    raw_hashes: dict[str, str] = {}
    raw_modes: dict[str, int] = {}
    manifest_bytes: bytes | None = None
    with zipfile.ZipFile(path) as handle:
        members = handle.infolist()
        if not members:
            raise ValueError("replication archive is empty")
        if handle.comment:
            raise ValueError("replication archive must not contain a comment")
        top_levels = {
            PurePosixPath(member.filename).parts[0]
            for member in members
            if PurePosixPath(member.filename).parts
        }
        if top_levels != {ARCHIVE_PREFIX}:
            raise ValueError(
                "archive top-level directory must be exactly "
                f"{ARCHIVE_PREFIX!r}, found {sorted(top_levels)!r}"
            )
        for member in members:
            name = member.filename
            if name in seen:
                raise ValueError(f"duplicate archive member: {name}")
            seen.add(name)
            bare_name = name[:-1] if name.endswith("/") else name
            safe_relative(bare_name, "archive member")
            if member.flag_bits & 0x1:
                raise ValueError(f"encrypted archive member: {name}")
            if member.flag_bits & ~0x800:
                raise ValueError(
                    f"unexpected ZIP flags on archive member: {name}"
                )
            if member.comment or member.extra:
                raise ValueError(
                    f"archive member has comment/extra metadata: {name}"
                )
            if member.create_system != 3:
                raise ValueError(
                    f"archive member lacks controlled Unix origin: {name}"
                )
            if member.date_time != ZIP_TIME:
                raise ValueError(
                    f"archive member timestamp differs: {name}"
                )
            unsafe_type = _unsafe_zip_type(member)
            if unsafe_type:
                raise ValueError(f"{unsafe_type} in archive: {name}")
            if member.is_dir() or name.endswith("/"):
                if member.compress_type != zipfile.ZIP_STORED:
                    raise ValueError(
                        f"archive directory must be stored: {name}"
                    )
                continue
            if member.compress_type != zipfile.ZIP_DEFLATED:
                raise ValueError(
                    f"archive file must use deflate compression: {name}"
                )
            relative = name.removeprefix(f"{ARCHIVE_PREFIX}/")
            if relative == name:
                raise ValueError(f"member lies outside archive prefix: {name}")
            safe_relative(relative, "archive payload")
            data = handle.read(member)
            raw_hashes[relative] = sha256_bytes(data)
            raw_modes[relative] = (member.external_attr >> 16) & 0o777
            if relative == "PACKAGE_MANIFEST.sha256":
                manifest_bytes = data
    if manifest_bytes is None:
        raise ValueError("archive lacks PACKAGE_MANIFEST.sha256")
    manifest = parse_manifest(manifest_bytes)
    expected = set(manifest) | {"PACKAGE_MANIFEST.sha256"}
    actual = set(raw_hashes)
    if actual != expected:
        raise ValueError(
            "archive/root-manifest file sets differ: "
            f"missing={sorted(expected - actual)!r}, "
            f"extra={sorted(actual - expected)!r}"
        )
    for relative, expected_digest in manifest.items():
        if raw_hashes[relative] != expected_digest:
            raise ValueError(
                f"archive member differs from root manifest: {relative}"
            )
    return ArchiveSnapshot(
        file_hashes=raw_hashes,
        file_modes=raw_modes,
        manifest=manifest,
        manifest_bytes=manifest_bytes,
        member_count=len(seen),
        prefix=ARCHIVE_PREFIX,
    )


def run_git(
    repository: Path,
    arguments: list[str],
    *,
    text: bool = True,
    check: bool = True,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=check,
        capture_output=True,
        text=text,
    )


def normalize_remote(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("git@github.com:"):
        stripped = "https://github.com/" + stripped[len("git@github.com:") :]
    if stripped.endswith(".git"):
        stripped = stripped[:-4]
    return stripped.rstrip("/")


def inspect_git(repository: Path) -> GitSnapshot:
    tag_type = run_git(repository, ["cat-file", "-t", TAG]).stdout.strip()
    if tag_type != "tag":
        raise ValueError(f"{TAG} is not an annotated tag")
    tag_object = run_git(repository, ["rev-parse", TAG]).stdout.strip()
    commit = run_git(
        repository,
        ["rev-parse", f"{TAG}^{{commit}}"],
    ).stdout.strip()
    tree = run_git(
        repository,
        ["rev-parse", f"{TAG}^{{tree}}"],
    ).stdout.strip()
    object_format = run_git(
        repository,
        ["rev-parse", "--show-object-format"],
    ).stdout.strip()
    expected_length = {"sha1": 40, "sha256": 64}.get(object_format)
    if expected_length is None:
        raise ValueError(f"unsupported Git object format: {object_format}")
    for label, value in (
        ("tag object", tag_object),
        ("commit", commit),
        ("tree", tree),
    ):
        if not OID_PATTERN.fullmatch(value) or len(value) != expected_length:
            raise ValueError(f"invalid {label} ID for {object_format}: {value}")

    tag_bytes = run_git(
        repository,
        ["cat-file", "tag", TAG],
        text=False,
    ).stdout
    has_signature = any(
        marker in tag_bytes
        for marker in (
            b"-----BEGIN PGP SIGNATURE-----",
            b"-----BEGIN SSH SIGNATURE-----",
        )
    )
    signature_check = run_git(
        repository,
        ["verify-tag", TAG],
        check=False,
    )
    if has_signature and signature_check.returncode != 0:
        raise ValueError("annotated tag has a signature that does not verify")
    signature_status = "verified" if has_signature else "unsigned"

    listing = run_git(
        repository,
        ["ls-tree", "-r", "-z", TAG],
        text=False,
    ).stdout
    file_hashes: dict[str, str] = {}
    file_modes: dict[str, int] = {}
    for record in listing.split(b"\0"):
        if not record:
            continue
        try:
            metadata, encoded_path = record.split(b"\t", 1)
            mode_raw, object_type, oid_raw = metadata.split(b" ", 2)
            relative = encoded_path.decode("utf-8")
            mode_text = mode_raw.decode("ascii")
            oid = oid_raw.decode("ascii")
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError(f"malformed Git tree entry: {record!r}") from exc
        safe_relative(relative, "Git tree")
        if object_type != b"blob" or mode_text not in {"100644", "100755"}:
            raise ValueError(
                f"unsupported Git entry {mode_text} "
                f"{object_type.decode('ascii', 'replace')} {relative}"
            )
        blob = run_git(
            repository,
            ["cat-file", "blob", oid],
            text=False,
        ).stdout
        file_hashes[relative] = sha256_bytes(blob)
        file_modes[relative] = int(mode_text[-3:], 8)

    remote = run_git(
        repository,
        ["remote", "get-url", "origin"],
    ).stdout.strip()
    if normalize_remote(remote) != REPOSITORY_URL:
        raise ValueError(
            f"origin URL does not match release repository: {remote!r}"
        )
    return GitSnapshot(
        commit=commit,
        file_hashes=file_hashes,
        file_modes=file_modes,
        object_format=object_format,
        signature_status=signature_status,
        tag_object=tag_object,
        tree=tree,
    )


def bind_archive_to_git(
    archive: ArchiveSnapshot,
    git: GitSnapshot,
) -> None:
    archive_paths = set(archive.file_hashes)
    git_paths = set(git.file_hashes)
    if archive_paths != git_paths:
        raise ValueError(
            "archive/Git file sets differ: "
            f"missing={sorted(git_paths - archive_paths)!r}, "
            f"extra={sorted(archive_paths - git_paths)!r}"
        )
    for relative in sorted(archive_paths):
        if archive.file_hashes[relative] != git.file_hashes[relative]:
            raise ValueError(f"archive differs from Git tag: {relative}")
        if archive.file_modes[relative] != git.file_modes[relative]:
            raise ValueError(
                f"archive mode differs from Git tag: {relative}"
            )
