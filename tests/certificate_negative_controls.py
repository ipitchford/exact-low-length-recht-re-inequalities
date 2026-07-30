#!/usr/bin/env python3
"""Fast adversarial controls for the detached publication certificate.

The issuer derives its repository root from ``__file__``.  This test therefore
copies the live certificate scripts into a tiny temporary Git repository,
constructs a complete tagged release there, and invokes those copied scripts as
black boxes.  A baseline must issue and verify; every one-cause mutation below
must be rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ISSUER_SOURCE = ROOT / "scripts/issue_release_certificate.py"
VERIFIER_SOURCE = ROOT / "scripts/verify_release_certificate.py"
COMMON_SOURCE = ROOT / "scripts/release_certificate_common.py"

TAG = "v1.0.0-candidate"
VERSION = "1.0.0-candidate"
SLUG = "exact-low-length-recht-re-inequalities"
REPOSITORY_URL = f"https://github.com/ipitchford/{SLUG}"
ARCHIVE_PREFIX = f"{SLUG}-{TAG}"
ARCHIVE_NAME = f"{ARCHIVE_PREFIX}.zip"
PAPER_NAME = f"{ARCHIVE_PREFIX}.pdf"
REPLAY_NAME = f"release-replay-{TAG}.txt"
CERTIFICATE_NAME = f"publication-certificate-{TAG}.json"
SIDE_CAR_NAME = f"{CERTIFICATE_NAME}.sha256"
TERMINAL_MARKER = "PUBLICATION-CANDIDATE REPLAY: PASS"
ENVIRONMENT_LINE = (
    "REPLICATION ENVIRONMENT: PASS "
    "(Python 3.11.9, mpmath 1.3.0, "
    "python-flint 0.8.0, sympy 1.14.0)"
)
ISSUED_AT = "2026-07-30T12:10:00Z"
COMPLETED_AT = "2026-07-30T12:00:00Z"
COMMAND_TIMEOUT_SECONDS = 30


class TestFailure(RuntimeError):
    """A negative control accepted invalid evidence or baseline failed."""


@dataclass(frozen=True)
class Fixture:
    repository: Path
    issuer: Path
    verifier: Path
    archive: Path
    paper: Path
    replay: Path
    certificate: Path
    sidecar: Path
    mutation_root: Path


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def command_text(result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(
        value.strip()
        for value in (result.stdout, result.stderr)
        if value and value.strip()
    )


def run(
    arguments: list[str],
    *,
    cwd: Path | None = None,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        timeout=COMMAND_TIMEOUT_SECONDS,
        check=False,
    )


def python_command(script: Path, arguments: list[str]) -> list[str]:
    optimization = ["-O"] if sys.flags.optimize else []
    return [sys.executable, *optimization, str(script), *arguments]


def require_success(
    label: str,
    result: subprocess.CompletedProcess[str],
    marker: str,
) -> None:
    output = command_text(result)
    if result.returncode != 0 or marker not in output:
        raise TestFailure(
            f"{label}: expected success containing {marker!r}, "
            f"exit={result.returncode}\n{output}"
        )
    print(f"  {label}: PASS")


def require_rejection(
    label: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    if result.returncode == 0:
        raise TestFailure(
            f"{label}: invalid evidence was accepted\n{command_text(result)}"
        )
    print(f"  {label}: PASS")


def git_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {
            "GIT_AUTHOR_NAME": "Anonymous",
            "GIT_AUTHOR_EMAIL": "anonymous@users.noreply.github.com",
            "GIT_COMMITTER_NAME": "Anonymous",
            "GIT_COMMITTER_EMAIL": "anonymous@users.noreply.github.com",
            "GIT_AUTHOR_DATE": "2026-07-30T12:00:00+00:00",
            "GIT_COMMITTER_DATE": "2026-07-30T12:00:00+00:00",
        }
    )
    return environment


def git(
    repository: Path,
    arguments: list[str],
    *,
    environment: dict[str, str] | None = None,
) -> str:
    result = run(
        ["git", "-C", str(repository), *arguments],
        environment=environment,
    )
    if result.returncode != 0:
        raise TestFailure(
            f"git {' '.join(arguments)} failed:\n{command_text(result)}"
        )
    return result.stdout


def write_fixture_files(repository: Path) -> None:
    scripts = repository / "scripts"
    scripts.mkdir(parents=True)
    for source in (ISSUER_SOURCE, VERIFIER_SOURCE, COMMON_SOURCE):
        if not source.is_file():
            raise TestFailure(f"missing live certificate script: {source}")
        shutil.copy2(source, scripts / source.name)

    files: dict[str, bytes] = {
        "paper/exact_low_length_recht_re.tex": (
            b"\\documentclass{article}\n"
            b"\\author{Anonymous}\n"
            b"\\begin{document}Fixture\\end{document}\n"
        ),
        "paper/exact_low_length_recht_re.pdf": b"%PDF-1.4\n%%EOF\n",
        "releases/m4/MANIFEST.sha256": b"fixture m4 manifest\n",
        "releases/m5/MANIFEST.sha256": b"fixture m5 manifest\n",
        "releases/m6-balanced/MANIFEST.sha256": b"fixture m6 manifest\n",
        "REPLAY_RECEIPT_2026-07-30.md": (
            b"# Fixture replay receipt\n\nPublisher-recorded test fixture.\n"
        ),
        "payload.txt": b"manifest-bound payload\n",
    }
    for relative, data in files.items():
        path = repository / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def rebuild_root_manifest(repository: Path) -> None:
    listed: list[Path] = []
    for path in repository.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(repository)
        if ".git" in relative.parts:
            continue
        if relative.as_posix() == "PACKAGE_MANIFEST.sha256":
            continue
        listed.append(path)
    lines = [
        f"{sha256(path)}  ./{path.relative_to(repository).as_posix()}"
        for path in sorted(
            listed,
            key=lambda item: item.relative_to(repository).as_posix(),
        )
    ]
    (repository / "PACKAGE_MANIFEST.sha256").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def tracked_modes(repository: Path) -> dict[str, int]:
    output = git(repository, ["ls-tree", "-r", TAG])
    modes: dict[str, int] = {}
    for line in output.splitlines():
        try:
            metadata, relative = line.split("\t", 1)
            mode_text, object_type, _object_id = metadata.split(" ", 2)
        except ValueError as exc:
            raise TestFailure(f"malformed git ls-tree line: {line!r}") from exc
        if object_type != "blob" or mode_text not in {"100644", "100755"}:
            raise TestFailure(
                f"unsupported fixture Git entry: {mode_text} "
                f"{object_type} {relative}"
            )
        modes[relative] = int(mode_text[-3:], 8)
    if not modes:
        raise TestFailure("fixture Git tree is empty")
    return modes


def zip_file_info(name: str, permissions: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(2026, 7, 30, 12, 0, 0))
    info.create_system = 3
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (stat.S_IFREG | permissions) << 16
    return info


def build_manifest_complete_archive(
    repository: Path,
    destination: Path,
) -> None:
    modes = tracked_modes(repository)
    with zipfile.ZipFile(destination, "w") as handle:
        for relative in sorted(modes):
            data = (repository / relative).read_bytes()
            info = zip_file_info(
                f"{ARCHIVE_PREFIX}/{relative}",
                modes[relative],
            )
            handle.writestr(info, data)


def issue_baseline(fixture: Fixture) -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    arguments = [
        "--archive",
        str(fixture.archive),
        "--paper",
        str(fixture.paper),
        "--replay-log",
        str(fixture.replay),
        "--output",
        str(fixture.certificate),
        "--sidecar",
        str(fixture.sidecar),
        "--issued-at",
        ISSUED_AT,
        "--replay-completed-at",
        COMPLETED_AT,
    ]
    result = run(
        python_command(fixture.issuer, arguments),
        environment=environment,
    )
    require_success(
        "baseline issuance",
        result,
        "PUBLICATION CERTIFICATE: ISSUED",
    )


def verifier_arguments(
    fixture: Fixture,
    certificate: Path,
    sidecar: Path,
    archive: Path,
    *,
    include_repository: bool = True,
) -> list[str]:
    arguments = [
        "--certificate",
        str(certificate),
        "--sidecar",
        str(sidecar),
        "--archive",
        str(archive),
        "--paper",
        str(fixture.paper),
        "--replay-log",
        str(fixture.replay),
        "--source-root",
        str(fixture.repository),
    ]
    if include_repository:
        arguments.extend(["--repository", str(fixture.repository)])
    return arguments


def invoke_verifier(
    fixture: Fixture,
    certificate: Path,
    sidecar: Path,
    archive: Path,
    *,
    include_repository: bool = True,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return run(
        python_command(
            fixture.verifier,
            verifier_arguments(
                fixture,
                certificate,
                sidecar,
                archive,
                include_repository=include_repository,
            ),
        ),
        environment=environment,
    )


def load_certificate(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TestFailure("issued certificate is not a JSON object")
    return value


def clone_certificate(value: dict[str, object]) -> dict[str, object]:
    cloned = json.loads(json.dumps(value, ensure_ascii=False))
    if not isinstance(cloned, dict):
        raise TestFailure("certificate clone is not an object")
    return cloned


def child_object(
    parent: dict[str, object],
    key: str,
) -> dict[str, object]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise TestFailure(f"baseline certificate field {key!r} is not an object")
    return value


def subjects(value: dict[str, object]) -> list[dict[str, object]]:
    raw = value.get("subjects")
    if not isinstance(raw, list):
        raise TestFailure("baseline certificate subjects is not a list")
    result: list[dict[str, object]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise TestFailure("baseline certificate has a malformed subject")
        result.append(item)
    return result


def subject(
    value: dict[str, object],
    role: str,
) -> dict[str, object]:
    matches = [
        item for item in subjects(value) if item.get("role") == role
    ]
    if len(matches) != 1:
        raise TestFailure(
            f"baseline certificate has {len(matches)} subjects for {role}"
        )
    return matches[0]


def refresh_certificate_id(value: dict[str, object]) -> None:
    git_record = child_object(value, "git")
    tag_record = child_object(git_record, "tag")
    archive_subject = subject(value, "replication_archive")
    repository = git_record.get("repository")
    tag = tag_record.get("name")
    commit = git_record.get("commit")
    archive_digest = archive_subject.get("sha256")
    if not all(
        isinstance(item, str)
        for item in (repository, tag, commit, archive_digest)
    ):
        raise TestFailure("cannot recompute certificate ID")
    key = f"{repository}|{tag}|{commit}|{archive_digest}"
    value["certificate_id"] = "urn:uuid:" + str(
        uuid.uuid5(uuid.NAMESPACE_URL, key)
    )


def refresh_archive_subject(
    value: dict[str, object],
    archive: Path,
) -> None:
    item = subject(value, "replication_archive")
    item["name"] = archive.name
    item["bytes"] = archive.stat().st_size
    item["sha256"] = sha256(archive)
    with zipfile.ZipFile(archive) as handle:
        inventory = child_object(value, "zip_inventory")
        inventory["member_count"] = len(handle.infolist())
        file_count = sum(
            1
            for member in handle.infolist()
            if not member.is_dir() and not member.filename.endswith("/")
        )
        if "file_count" in inventory:
            inventory["file_count"] = file_count
        try:
            manifest_bytes = handle.read(
                f"{ARCHIVE_PREFIX}/PACKAGE_MANIFEST.sha256"
            )
        except KeyError:
            manifest_bytes = b""
        for key in ("manifest_sha256", "root_manifest_sha256"):
            if key in inventory:
                inventory[key] = sha256_bytes(manifest_bytes)
    refresh_certificate_id(value)


def encoded_certificate(value: dict[str, object]) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def write_certificate_case(
    case_directory: Path,
    value: dict[str, object] | None = None,
    *,
    raw: bytes | None = None,
) -> tuple[Path, Path]:
    case_directory.mkdir(parents=True, exist_ok=True)
    certificate = case_directory / CERTIFICATE_NAME
    sidecar = case_directory / SIDE_CAR_NAME
    if (value is None) == (raw is None):
        raise TestFailure("certificate case requires exactly one encoding")
    encoded = raw if raw is not None else encoded_certificate(value or {})
    certificate.write_bytes(encoded)
    sidecar.write_text(
        f"{sha256_bytes(encoded)}  {certificate.name}\n",
        encoding="utf-8",
    )
    return certificate, sidecar


def mutated_archive(
    fixture: Fixture,
    label: str,
    transform: str,
) -> tuple[Path, bytes | None]:
    case_directory = fixture.mutation_root / label
    case_directory.mkdir(parents=True, exist_ok=True)
    destination = case_directory / ARCHIVE_NAME
    changed_manifest: bytes | None = None
    with zipfile.ZipFile(fixture.archive) as source:
        with zipfile.ZipFile(destination, "w") as target:
            for member in source.infolist():
                data = source.read(member)
                relative = member.filename.removeprefix(
                    f"{ARCHIVE_PREFIX}/"
                )
                if transform == "missing" and relative == "payload.txt":
                    continue
                if transform == "altered" and relative == "payload.txt":
                    data = b"altered but outer-hash-rebound payload\n"
                if (
                    transform == "wrong_manifest"
                    and relative == "PACKAGE_MANIFEST.sha256"
                ):
                    lines = data.splitlines()
                    data = b"\n".join(reversed(lines)) + b"\n"
                    changed_manifest = data
                target.writestr(member, data)
            if transform == "extra":
                target.writestr(
                    zip_file_info(
                        f"{ARCHIVE_PREFIX}/unmanifested-extra.txt",
                        0o644,
                    ),
                    b"extra archive payload\n",
                )
    return destination, changed_manifest


def archive_mutation_case(
    fixture: Fixture,
    baseline: dict[str, object],
    label: str,
    transform: str,
) -> None:
    archive, changed_manifest = mutated_archive(
        fixture,
        label,
        transform,
    )
    value = clone_certificate(baseline)
    refresh_archive_subject(value, archive)
    if changed_manifest is not None:
        root_subject = subject(value, "root_manifest")
        root_subject["bytes"] = len(changed_manifest)
        root_subject["sha256"] = sha256_bytes(changed_manifest)
    certificate, sidecar = write_certificate_case(
        fixture.mutation_root / label,
        value,
    )
    require_rejection(
        label,
        invoke_verifier(
            fixture,
            certificate,
            sidecar,
            archive,
        ),
    )


def certificate_mutation_case(
    fixture: Fixture,
    baseline: dict[str, object],
    label: str,
    mutate: object,
) -> None:
    value = clone_certificate(baseline)
    if not callable(mutate):
        raise TestFailure(f"{label}: mutation is not callable")
    mutate(value)
    certificate, sidecar = write_certificate_case(
        fixture.mutation_root / label,
        value,
    )
    require_rejection(
        label,
        invoke_verifier(
            fixture,
            certificate,
            sidecar,
            fixture.archive,
        ),
    )


def build_fixture(base: Path) -> Fixture:
    repository = base / "repository"
    assets = base / "assets"
    mutation_root = base / "mutations"
    repository.mkdir()
    assets.mkdir()
    mutation_root.mkdir()

    git_env = git_environment()
    git(repository, ["init", "-b", "main"], environment=git_env)
    git(
        repository,
        ["config", "user.name", "Anonymous"],
        environment=git_env,
    )
    git(
        repository,
        [
            "config",
            "user.email",
            "anonymous@users.noreply.github.com",
        ],
        environment=git_env,
    )
    git(
        repository,
        ["config", "commit.gpgsign", "false"],
        environment=git_env,
    )
    git(
        repository,
        ["config", "tag.gpgsign", "false"],
        environment=git_env,
    )
    git(
        repository,
        ["remote", "add", "origin", REPOSITORY_URL],
        environment=git_env,
    )

    write_fixture_files(repository)
    rebuild_root_manifest(repository)
    git(repository, ["add", "--all"], environment=git_env)
    git(
        repository,
        ["commit", "-m", "Anonymous certificate fixture"],
        environment=git_env,
    )
    git(
        repository,
        ["tag", "-a", TAG, "-m", "Anonymous candidate fixture"],
        environment=git_env,
    )

    archive = assets / ARCHIVE_NAME
    build_manifest_complete_archive(repository, archive)
    paper = assets / PAPER_NAME
    shutil.copyfile(
        repository / "paper/exact_low_length_recht_re.pdf",
        paper,
    )
    replay = assets / REPLAY_NAME
    replay.write_text(
        f"{ENVIRONMENT_LINE}\n{TERMINAL_MARKER}\n",
        encoding="utf-8",
    )

    fixture = Fixture(
        repository=repository,
        issuer=repository / "scripts/issue_release_certificate.py",
        verifier=repository / "scripts/verify_release_certificate.py",
        archive=archive,
        paper=paper,
        replay=replay,
        certificate=assets / CERTIFICATE_NAME,
        sidecar=assets / SIDE_CAR_NAME,
        mutation_root=mutation_root,
    )
    issue_baseline(fixture)
    return fixture


def main() -> int:
    mode = "optimized" if sys.flags.optimize else "normal"
    print(f"CERTIFICATE NEGATIVE CONTROLS ({mode})")
    try:
        with tempfile.TemporaryDirectory(
            prefix="recht-re-certificate-negative-"
        ) as temporary:
            fixture = build_fixture(Path(temporary))
            baseline = load_certificate(fixture.certificate)

            require_success(
                "baseline verification",
                invoke_verifier(
                    fixture,
                    fixture.certificate,
                    fixture.sidecar,
                    fixture.archive,
                ),
                "PUBLICATION CERTIFICATE: PASS",
            )
            require_rejection(
                "missing --repository",
                invoke_verifier(
                    fixture,
                    fixture.certificate,
                    fixture.sidecar,
                    fixture.archive,
                    include_repository=False,
                ),
            )

            archive_mutation_case(
                fixture,
                baseline,
                "extra archive member",
                "extra",
            )
            archive_mutation_case(
                fixture,
                baseline,
                "altered archive member",
                "altered",
            )
            archive_mutation_case(
                fixture,
                baseline,
                "missing archive member",
                "missing",
            )
            archive_mutation_case(
                fixture,
                baseline,
                "wrong root manifest",
                "wrong_manifest",
            )

            def wrong_tag_object(value: dict[str, object]) -> None:
                git_record = child_object(value, "git")
                tag_record = child_object(git_record, "tag")
                observed = tag_record.get("object")
                if not isinstance(observed, str):
                    raise TestFailure("baseline tag object is not a string")
                tag_record["object"] = "0" * len(observed)

            certificate_mutation_case(
                fixture,
                baseline,
                "wrong annotated-tag object",
                wrong_tag_object,
            )

            def false_doi(value: dict[str, object]) -> None:
                publication = child_object(value, "publication")
                zenodo = child_object(publication, "zenodo")
                zenodo["version_doi"] = "10.5281/zenodo.99999999"
                zenodo["record_url"] = (
                    "https://zenodo.org/records/99999999"
                )

            certificate_mutation_case(
                fixture,
                baseline,
                "false version DOI",
                false_doi,
            )

            def reversed_timestamps(value: dict[str, object]) -> None:
                value["generated_at"] = "2026-07-30T11:00:00Z"
                replay_record = child_object(value, "replay")
                replay_record["completed_at"] = COMPLETED_AT

            certificate_mutation_case(
                fixture,
                baseline,
                "replay later than certificate issuance",
                reversed_timestamps,
            )

            def false_replay_metadata(value: dict[str, object]) -> None:
                replay_record = child_object(value, "replay")
                replay_record["result"] = "fail"
                replay_record["exit_code"] = 1
                replay_record["fresh_extraction"] = False

            certificate_mutation_case(
                fixture,
                baseline,
                "false replay metadata",
                false_replay_metadata,
            )

            def unsafe_git_path(value: dict[str, object]) -> None:
                paper_source = subject(value, "paper_source")
                paper_source["git_path"] = str(
                    fixture.repository
                    / "paper/exact_low_length_recht_re.tex"
                )

            certificate_mutation_case(
                fixture,
                baseline,
                "unsafe absolute Git path",
                unsafe_git_path,
            )

            duplicate_source = fixture.certificate.read_text(
                encoding="utf-8"
            )
            schema_field = '"schema": "publication-certificate/1.0"'
            if duplicate_source.count(schema_field) != 1:
                raise TestFailure(
                    "cannot construct duplicate-key certificate fixture"
                )
            duplicate_encoded = duplicate_source.replace(
                schema_field,
                f"{schema_field},\n  {schema_field}",
                1,
            ).encode("utf-8")
            duplicate_certificate, duplicate_sidecar = (
                write_certificate_case(
                    fixture.mutation_root / "duplicate JSON key",
                    raw=duplicate_encoded,
                )
            )
            require_rejection(
                "duplicate JSON key",
                invoke_verifier(
                    fixture,
                    duplicate_certificate,
                    duplicate_sidecar,
                    fixture.archive,
                ),
            )

            git_env = git_environment()
            git(
                fixture.repository,
                ["tag", "-d", TAG],
                environment=git_env,
            )
            git(
                fixture.repository,
                ["tag", TAG, "HEAD"],
                environment=git_env,
            )
            require_rejection(
                "lightweight release tag",
                invoke_verifier(
                    fixture,
                    fixture.certificate,
                    fixture.sidecar,
                    fixture.archive,
                ),
            )
    except (
        OSError,
        subprocess.SubprocessError,
        TestFailure,
        ValueError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"CERTIFICATE NEGATIVE CONTROLS: FAIL\n  - {exc}")
        return 1

    print("CERTIFICATE NEGATIVE CONTROLS: PASS (12 mutations rejected)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
