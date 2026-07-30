#!/usr/bin/env python3
"""Build a deterministic, mode-preserving ZIP directly from the release tag."""

from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from release_certificate_common import (
    ARCHIVE_NAME,
    ARCHIVE_PREFIX,
    TAG,
    ZIP_TIME,
    bind_archive_to_git,
    inspect_archive,
    inspect_git,
    run_git,
    safe_relative,
)


ROOT = Path(__file__).resolve().parents[1]
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def tagged_files() -> list[tuple[str, int, bytes]]:
    listing = run_git(
        ROOT,
        ["ls-tree", "-r", "-z", TAG],
        text=False,
    ).stdout
    files: list[tuple[str, int, bytes]] = []
    for record in listing.split(b"\0"):
        if not record:
            continue
        try:
            metadata, encoded_path = record.split(b"\t", 1)
            mode_raw, object_type, oid = metadata.split(b" ", 2)
            relative = encoded_path.decode("utf-8")
            mode_text = mode_raw.decode("ascii")
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError(f"malformed Git tree entry: {record!r}") from exc
        safe_relative(relative, "Git tree")
        if object_type != b"blob" or mode_text not in {"100644", "100755"}:
            raise ValueError(
                f"unsupported Git entry {mode_text} {relative}"
            )
        data = run_git(
            ROOT,
            ["cat-file", "blob", oid.decode("ascii")],
            text=False,
        ).stdout
        files.append((relative, int(mode_text[-3:], 8), data))
    return sorted(files)


def directory_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name.rstrip("/") + "/", date_time=ZIP_TIME)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_STORED
    info.external_attr = (0o40755 << 16) | 0x10
    return info


def file_info(name: str, mode: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = ((0o100000 | mode) << 16)
    return info


def build(output: Path) -> None:
    if output.name != ARCHIVE_NAME:
        raise ValueError(
            f"output filename must be {ARCHIVE_NAME!r}, "
            f"found {output.name!r}"
        )
    resolved_output = output.resolve()
    if resolved_output.is_relative_to(ROOT.resolve()):
        raise ValueError("release archive must be built outside the repository")
    if run_git(
        ROOT,
        ["status", "--porcelain", "--untracked-files=all"],
    ).stdout.strip():
        raise ValueError("repository must be clean")
    git_snapshot = inspect_git(ROOT)
    head = run_git(ROOT, ["rev-parse", "HEAD"]).stdout.strip()
    if git_snapshot.commit != head:
        raise ValueError(f"{TAG} must peel to the current HEAD")

    files = tagged_files()
    directories = {ARCHIVE_PREFIX}
    for relative, _, _ in files:
        parent = PurePosixPath(relative).parent
        while parent.as_posix() != ".":
            directories.add(f"{ARCHIVE_PREFIX}/{parent.as_posix()}")
            parent = parent.parent

    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{ARCHIVE_NAME}.",
        suffix=".tmp",
        dir=output.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(
            temporary,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as handle:
            for directory in sorted(directories):
                handle.writestr(directory_info(directory), b"")
            for relative, mode, data in files:
                name = f"{ARCHIVE_PREFIX}/{relative}"
                handle.writestr(
                    file_info(name, mode),
                    data,
                    compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )
        archive_snapshot = inspect_archive(temporary)
        bind_archive_to_git(archive_snapshot, git_snapshot)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    args = parse_args()
    try:
        build(args.output)
    except (
        OSError,
        ValueError,
        zipfile.BadZipFile,
        subprocess.CalledProcessError,
    ) as exc:
        raise SystemExit(f"RELEASE ARCHIVE: REFUSED\n  - {exc}") from exc
    print(f"RELEASE ARCHIVE: PASS {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
