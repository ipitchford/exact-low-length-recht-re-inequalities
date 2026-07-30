#!/usr/bin/env python3
"""Run the complete publication-candidate replication and integrity suite."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from dataclasses import dataclass
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
FORBIDDEN_PARTS = {"__pycache__", ".pytest_cache"}


@dataclass(frozen=True)
class Replay:
    label: str
    cwd: Path
    script: Path


REPLAYS = (
    Replay(
        "m4/stdlib",
        ROOT / "releases/m4",
        Path("verifiers/verify_all_n_stdlib.py"),
    ),
    Replay(
        "m4/sympy",
        ROOT / "releases/m4",
        Path("verifiers/verify_all_n_sympy.py"),
    ),
    Replay(
        "m4/derivation",
        ROOT / "releases/m4",
        Path("src/derive_parametric_family.py"),
    ),
    Replay(
        "m5/stdlib",
        ROOT / "releases/m5",
        Path("verifiers/verify_m5_restoration_stdlib.py"),
    ),
    Replay(
        "m5/sympy",
        ROOT / "releases/m5",
        Path("verifiers/verify_m5_restoration_sympy.py"),
    ),
    Replay(
        "m5/derivation",
        ROOT / "releases/m5",
        Path("src/derive_parametric_family.py"),
    ),
    Replay(
        "m5/n5-counterexample",
        ROOT / "releases/m5",
        Path("counterexamples/verify_n5_lower_counterexample.py"),
    ),
    Replay(
        "m6/identities",
        ROOT / "releases/m6-balanced",
        Path("check_parametric_identities.py"),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--python",
        type=Path,
        default=Path(sys.executable),
        help="Python interpreter containing SymPy 1.14.0",
    )
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--skip-mutations",
        action="store_true",
        help="Run baselines only; not sufficient for a release decision",
    )
    return parser.parse_args()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def included(path: Path, root: Path, manifest: Path) -> bool:
    relative = path.relative_to(root)
    if path.resolve() == manifest.resolve():
        return False
    if relative.name in IGNORED_NAMES:
        return False
    if any(part in IGNORED_PARTS for part in relative.parts):
        return False
    return not any(relative.name.endswith(suffix) for suffix in IGNORED_SUFFIXES)


def validate_manifest(directory: Path, manifest: Path) -> list[str]:
    failures: list[str] = []
    if not manifest.is_file():
        return [f"{manifest.relative_to(ROOT)}: missing"]
    listed: dict[str, str] = {}
    for line_number, line in enumerate(
        manifest.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        try:
            expected, relative = line.split("  ", 1)
        except ValueError:
            failures.append(f"{manifest}:{line_number}: malformed line")
            continue
        if (
            not relative.startswith("./")
            or Path(relative).is_absolute()
            or ".." in Path(relative).parts
        ):
            failures.append(
                f"{manifest}:{line_number}: unsafe relative path {relative!r}"
            )
            continue
        if relative in listed:
            failures.append(
                f"{manifest}:{line_number}: duplicate path {relative}"
            )
            continue
        if len(expected) != 64 or any(
            character not in "0123456789abcdef" for character in expected
        ):
            failures.append(
                f"{manifest}:{line_number}: malformed SHA-256 {expected!r}"
            )
            continue
        listed[relative] = expected
        path = directory / relative
        if not path.is_file():
            failures.append(f"{relative}: missing")
        elif digest(path) != expected:
            failures.append(f"{relative}: SHA-256 mismatch")

    actual = {
        f"./{path.relative_to(directory).as_posix()}"
        for path in directory.rglob("*")
        if path.is_file() and included(path, directory, manifest)
    }
    missing_entries = sorted(actual - set(listed))
    stale_entries = sorted(set(listed) - actual)
    failures.extend(f"{relative}: unlisted file" for relative in missing_entries)
    failures.extend(f"{relative}: listed but excluded/absent" for relative in stale_entries)
    if not listed:
        failures.append(f"{manifest.relative_to(ROOT)}: empty manifest")
    return failures


def forbidden_artifacts(directory: Path) -> list[str]:
    failures: list[str] = []
    for path in directory.rglob("*"):
        relative = path.relative_to(directory)
        if ".git" in relative.parts or ".venv" in relative.parts:
            continue
        forbidden_part = any(part in FORBIDDEN_PARTS for part in relative.parts)
        forbidden_name = (
            relative.name in IGNORED_NAMES
            or any(relative.name.endswith(suffix) for suffix in IGNORED_SUFFIXES)
            or relative.suffix == ".pyc"
        )
        if forbidden_part or forbidden_name:
            failures.append(relative.as_posix())
    return sorted(set(failures))


def run(
    command: list[str],
    cwd: Path,
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return subprocess.CompletedProcess(
            command,
            124,
            stdout,
            stderr + f"\nTIMEOUT after {timeout}s",
        )


def tail(result: subprocess.CompletedProcess[str], lines: int = 8) -> str:
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    return "\n".join(combined.strip().splitlines()[-lines:])


def main() -> int:
    args = parse_args()
    # Preserve a virtual-environment executable symlink so subprocesses retain
    # the selected environment's prefix and installed dependencies.
    python = args.python.absolute()
    failures: list[str] = []

    print("ENVIRONMENT")
    environment = run(
        [str(python), "scripts/check_environment.py"],
        ROOT,
        args.timeout,
    )
    print(f"  {'PASS' if environment.returncode == 0 else 'FAIL'}")
    if environment.returncode != 0:
        failures.append(f"environment:\n{tail(environment)}")
    else:
        environment_lines = [
            line.strip()
            for line in environment.stdout.splitlines()
            if line.strip()
        ]
        if len(environment_lines) != 1:
            failures.append(
                "environment: expected one nonempty result line, found "
                f"{len(environment_lines)}"
            )
        else:
            print(f"  {environment_lines[0]}")

    print("PACKAGE HYGIENE")
    forbidden = forbidden_artifacts(ROOT)
    print(f"  {'PASS' if not forbidden else 'FAIL'}")
    failures.extend(
        f"forbidden package artifact: {relative}" for relative in forbidden
    )

    print("RELEASE METADATA")
    metadata = run(
        [str(python), "scripts/check_release_metadata.py"],
        ROOT,
        args.timeout,
    )
    print(f"  {'PASS' if metadata.returncode == 0 else 'FAIL'}")
    if metadata.returncode != 0:
        failures.append(f"release metadata:\n{tail(metadata, 20)}")

    print("PUBLICATION SHAPE")
    publication_shape = run(
        [str(python), "scripts/check_publication_shape.py"],
        ROOT,
        args.timeout,
    )
    print(f"  {'PASS' if publication_shape.returncode == 0 else 'FAIL'}")
    if publication_shape.returncode != 0:
        failures.append(
            f"publication shape:\n{tail(publication_shape, 20)}"
        )

    print("MANIFESTS")
    for name in ("m4", "m5", "m6-balanced"):
        release = ROOT / f"releases/{name}"
        manifest_failures = validate_manifest(
            release,
            release / "MANIFEST.sha256",
        )
        status = "PASS" if not manifest_failures else "FAIL"
        print(f"  {name}: {status}")
        failures.extend(f"{name} manifest: {item}" for item in manifest_failures)
    package_manifest_failures = validate_manifest(
        ROOT,
        ROOT / "PACKAGE_MANIFEST.sha256",
    )
    print(
        "  package: "
        f"{'PASS' if not package_manifest_failures else 'FAIL'}"
    )
    failures.extend(
        f"package manifest: {item}" for item in package_manifest_failures
    )
    if failures:
        print("PUBLICATION-CANDIDATE PRECHECK: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("VERIFIER SAFETY")
    safety = run(
        [str(python), "scripts/check_verifier_safety.py"],
        ROOT,
        args.timeout,
    )
    print(f"  {'PASS' if safety.returncode == 0 else 'FAIL'}")
    if safety.returncode != 0:
        failures.append(f"verifier safety:\n{tail(safety)}")

    print("CITATION KEYS")
    citations = run(
        [str(python), "scripts/check_citations.py"],
        ROOT,
        args.timeout,
    )
    print(f"  {'PASS' if citations.returncode == 0 else 'FAIL'}")
    if citations.returncode != 0:
        failures.append(f"citation keys:\n{tail(citations)}")

    print("CLAIM INVENTORY")
    inventory = run(
        [str(python), "scripts/check_claim_inventory.py"],
        ROOT,
        args.timeout,
    )
    print(f"  {'PASS' if inventory.returncode == 0 else 'FAIL'}")
    if inventory.returncode != 0:
        failures.append(f"claim inventory:\n{tail(inventory)}")

    print("CERTIFICATE NEGATIVE CONTROLS")
    for mode, flags in (("normal", []), ("optimized", ["-O"])):
        certificate_controls = run(
            [
                str(python),
                *flags,
                "tests/certificate_negative_controls.py",
            ],
            ROOT,
            max(args.timeout, 120),
        )
        print(
            f"  {mode}: "
            f"{'PASS' if certificate_controls.returncode == 0 else 'FAIL'}"
        )
        if certificate_controls.returncode != 0:
            failures.append(
                f"certificate negative controls/{mode}:\n"
                f"{tail(certificate_controls, 30)}"
            )

    print("SEMANTIC BRIDGE")
    semantic_outputs: dict[str, str] = {}
    for mode, flags in (("normal", []), ("optimized", ["-O"])):
        semantic = run(
            [
                str(python),
                *flags,
                "scripts/check_semantic_bridge.py",
            ],
            ROOT,
            args.timeout,
        )
        print(
            f"  {mode}: "
            f"{'PASS' if semantic.returncode == 0 else 'FAIL'}"
        )
        if semantic.returncode != 0:
            failures.append(
                f"semantic bridge/{mode}:\n{tail(semantic, 20)}"
            )
        semantic_outputs[mode] = semantic.stdout
    if semantic_outputs["normal"] != semantic_outputs["optimized"]:
        failures.append("semantic bridge: normal and optimized stdout differ")

    print("EXACT REPLAYS")
    for replay in REPLAYS:
        outputs: dict[str, str] = {}
        for mode, flags in (("normal", []), ("optimized", ["-O"])):
            result = run(
                [str(python), *flags, str(replay.script)],
                replay.cwd,
                args.timeout,
            )
            status = "PASS" if result.returncode == 0 else "FAIL"
            print(f"  {replay.label}/{mode}: {status}")
            if result.returncode != 0:
                failures.append(
                    f"{replay.label}/{mode} exited {result.returncode}:\n"
                    f"{tail(result)}"
                )
            outputs[mode] = result.stdout
        if outputs["normal"] != outputs["optimized"]:
            failures.append(
                f"{replay.label}: normal and optimized stdout differ"
            )

    print("M6 EXACT BASE PSD")
    m6_psd = run(
        [
            str(python),
            "releases/m6-balanced/certify_base_psd_flint.py",
        ],
        ROOT,
        max(args.timeout, 900),
    )
    print(f"  {'PASS' if m6_psd.returncode == 0 else 'FAIL'}")
    if m6_psd.returncode != 0:
        failures.append(f"m6 exact base PSD:\n{tail(m6_psd, 30)}")

    if args.skip_mutations:
        print("NEGATIVE CONTROLS: SKIPPED (run is not release-qualifying)")
    else:
        print("NEGATIVE CONTROLS")
        mutation = run(
            [
                str(python),
                "tests/negative_controls.py",
                "--m4-root",
                "releases/m4",
                "--m5-root",
                "releases/m5",
                "--python",
                str(python),
                "--timeout",
                str(args.timeout),
            ],
            ROOT,
            max(args.timeout * 20, 1200),
        )
        print(f"  {'PASS' if mutation.returncode == 0 else 'FAIL'}")
        if mutation.returncode != 0:
            failures.append(f"negative controls:\n{tail(mutation, 30)}")

        print("SEMANTIC NEGATIVE CONTROLS")
        semantic_mutation = run(
            [
                str(python),
                "tests/semantic_negative_controls.py",
                "--python",
                str(python),
                "--timeout",
                str(args.timeout),
            ],
            ROOT,
            max(args.timeout * 10, 600),
        )
        print(
            f"  {'PASS' if semantic_mutation.returncode == 0 else 'FAIL'}"
        )
        if semantic_mutation.returncode != 0:
            failures.append(
                f"semantic negative controls:\n"
                f"{tail(semantic_mutation, 30)}"
            )

        print("EXTENDED NEGATIVE CONTROLS")
        extended_mutation = run(
            [
                str(python),
                "tests/extended_negative_controls.py",
                "--python",
                str(python),
                "--timeout",
                str(args.timeout),
            ],
            ROOT,
            max(args.timeout * 4, 900),
        )
        print(
            f"  {'PASS' if extended_mutation.returncode == 0 else 'FAIL'}"
        )
        if extended_mutation.returncode != 0:
            failures.append(
                f"extended negative controls:\n"
                f"{tail(extended_mutation, 30)}"
            )

    print("M6 EXPLORATORY SNAPSHOT")
    m6 = run(
        [str(python), "scripts/audit_m6_snapshot.py"],
        ROOT,
        args.timeout,
    )
    print(f"  {'PASS' if m6.returncode == 0 else 'FAIL'}")
    if m6.returncode != 0:
        failures.append(f"m6 inventory:\n{tail(m6)}")

    if failures:
        print("PUBLICATION-CANDIDATE REPLAY: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    if args.skip_mutations:
        print(
            "PUBLICATION-CANDIDATE BASELINES: PASS "
            "(NOT RELEASE-QUALIFYING; MUTATIONS SKIPPED)"
        )
        return 0
    print("PUBLICATION-CANDIDATE REPLAY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
