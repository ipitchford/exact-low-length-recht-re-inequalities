#!/usr/bin/env python3
"""Run mutation-based negative controls against the exact verifiers.

The source releases are never modified. Each control copies one release into a
temporary directory, changes one exact certificate scalar, and requires every
relevant replay path to terminate with an explicit failure in both normal and
optimized Python modes.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Release:
    name: str
    root: Path
    commands: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class Mutation:
    name: str
    release: str
    relative_json: Path
    value_path: tuple[str | int, ...]
    replay_paths: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m4-root", type=Path, required=True)
    parser.add_argument("--m5-root", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    return parser.parse_args()


def bump_exact(value: Any) -> Any:
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return str(Fraction(value) + 1)
    raise TypeError(f"Unsupported exact scalar: {value!r}")


def mutate_json(root: Path, mutation: Mutation) -> tuple[Any, Any]:
    path = root / mutation.relative_json
    data = json.loads(path.read_text(encoding="utf-8"))
    parent: Any = data
    for key in mutation.value_path[:-1]:
        parent = parent[key]
    final_key = mutation.value_path[-1]
    before = parent[final_key]
    after = bump_exact(before)
    parent[final_key] = after
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return before, after


def run_command(
    python: Path,
    root: Path,
    command: tuple[str, ...],
    timeout: int,
    optimized: bool,
) -> subprocess.CompletedProcess[str]:
    flags = ["-O"] if optimized else []
    return subprocess.run(
        [str(python), *flags, *command],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def output_tail(result: subprocess.CompletedProcess[str], lines: int = 5) -> str:
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    return "\n".join(combined.strip().splitlines()[-lines:])


def main() -> int:
    args = parse_args()
    # Preserve a virtual-environment executable symlink: resolving it would
    # select the base interpreter and lose the environment's site-packages.
    python = args.python.absolute()
    releases = {
        "m4": Release(
            "m4",
            args.m4_root.resolve(),
            {
                "stdlib": ("verifiers/verify_all_n_stdlib.py",),
                "sympy": ("verifiers/verify_all_n_sympy.py",),
                "derive": ("src/derive_parametric_family.py",),
            },
        ),
        "m5": Release(
            "m5",
            args.m5_root.resolve(),
            {
                "stdlib": ("verifiers/verify_m5_restoration_stdlib.py",),
                "sympy": ("verifiers/verify_m5_restoration_sympy.py",),
                "derive": ("src/derive_parametric_family.py",),
            },
        ),
    }
    mutations = (
        Mutation(
            "m4-parametric-identity",
            "m4",
            Path("certificates/parametric_orbit_functions.json"),
            ("upper", "orbit_functions", 0, "numerator_coefficients", 0),
            ("stdlib", "sympy", "derive"),
        ),
        Mutation(
            "m4-determinant-record",
            "m4",
            Path("certificates/principal_minors.json"),
            (
                "upper_G0",
                "leading_principal_minors",
                0,
                "coefficients_ascending_in_t",
                0,
            ),
            ("stdlib", "sympy"),
        ),
        Mutation(
            "m4-seed",
            "m4",
            Path("certificates/base5_seed_certificates.json"),
            ("upper", "orbit_values", 0),
            ("stdlib", "sympy", "derive"),
        ),
        Mutation(
            "m4-endpoint",
            "m4",
            Path("certificates/n4_orbit_certificates.json"),
            ("upper", "orbit_values", 0),
            ("stdlib", "sympy"),
        ),
        Mutation(
            "m5-parametric-identity",
            "m5",
            Path("certificates/parametric_orbit_functions.json"),
            ("upper", "orbit_functions", 0, "numerator_coefficients", 0),
            ("stdlib", "sympy", "derive"),
        ),
        Mutation(
            "m5-determinant-record",
            "m5",
            Path("certificates/principal_minors.json"),
            (
                "upper_G0",
                "leading_principal_minors",
                0,
                "coefficients_ascending_in_t",
                0,
            ),
            ("stdlib", "sympy"),
        ),
        Mutation(
            "m5-seed",
            "m5",
            Path("certificates/base6_seed_certificates.json"),
            ("upper", "orbit_values", 0),
            ("stdlib", "sympy", "derive"),
        ),
        Mutation(
            "m5-endpoint",
            "m5",
            Path("certificates/n5_upper_certificate.json"),
            ("upper", "orbit_values", 0),
            ("stdlib", "sympy"),
        ),
    )

    failures: list[str] = []
    print("BASELINES")
    for release in releases.values():
        for replay_name, command in release.commands.items():
            for optimized in (False, True):
                mode = "optimized" if optimized else "normal"
                result = run_command(
                    python,
                    release.root,
                    command,
                    args.timeout,
                    optimized,
                )
                status = "PASS" if result.returncode == 0 else "FAIL"
                print(f"  {release.name}/{replay_name}/{mode}: {status}")
                if result.returncode != 0:
                    failures.append(
                        f"baseline {release.name}/{replay_name}/{mode} exited "
                        f"{result.returncode}:\n{output_tail(result)}"
                    )

    print("NEGATIVE CONTROLS")
    for mutation in mutations:
        release = releases[mutation.release]
        with tempfile.TemporaryDirectory(
            prefix=f"lailim-{mutation.name}-"
        ) as temp_dir:
            copied_root = Path(temp_dir) / "release"
            shutil.copytree(release.root, copied_root)
            before, after = mutate_json(copied_root, mutation)
            print(f"  {mutation.name}: {before!r} -> {after!r}")
            for replay_name in mutation.replay_paths:
                for optimized in (False, True):
                    mode = "optimized" if optimized else "normal"
                    result = run_command(
                        python,
                        copied_root,
                        release.commands[replay_name],
                        args.timeout,
                        optimized,
                    )
                    combined = result.stdout + result.stderr
                    explicit_failure = any(
                        marker in combined
                        for marker in (
                            "AssertionError",
                            "VerificationError",
                            "VERIFICATION FAILED",
                        )
                    )
                    rejected = result.returncode != 0 and explicit_failure
                    status = "REJECTED" if rejected else "MISSED"
                    print(
                        f"    {replay_name}/{mode}: {status} "
                        f"(exit={result.returncode}, "
                        f"explicit_failure={explicit_failure})"
                    )
                    if not rejected:
                        failures.append(
                            f"{mutation.name}/{replay_name}/{mode} did not "
                            f"reject explicitly (exit={result.returncode}):\n"
                            f"{output_tail(result)}"
                        )

    if failures:
        print("NEGATIVE CONTROL AUDIT: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("NEGATIVE CONTROL AUDIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
