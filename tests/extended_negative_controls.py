#!/usr/bin/env python3
"""Known-bad controls for the m=6 and quadratic metric extensions."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    return parser.parse_args()


def run(
    python: Path,
    flags: list[str],
    script: Path,
    arguments: list[str],
    cwd: Path,
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(python), *flags, str(script), *arguments],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def require_rejection(
    failures: list[str],
    label: str,
    result: subprocess.CompletedProcess[str],
    marker: str,
) -> None:
    combined = result.stdout + result.stderr
    rejected = result.returncode != 0 and marker in combined
    print(f"  {label}: {'REJECTED' if rejected else 'MISSED'}")
    if not rejected:
        failures.append(
            f"{label}: exit={result.returncode}; "
            f"tail={combined.strip().splitlines()[-8:]}"
        )


def main() -> int:
    args = parse_args()
    python = args.python.absolute()
    failures: list[str] = []

    with tempfile.TemporaryDirectory(prefix="lailim-m6-coordinate-") as temp:
        copied = Path(temp) / "m6-balanced"
        shutil.copytree(ROOT / "releases/m6-balanced", copied)
        path = copied / "m6_upper_parametric_functions.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        functions = record["functions"]
        if functions[0] == functions[1]:
            failures.append("m6 coordinate fixture selected equal functions")
        functions[0], functions[1] = functions[1], functions[0]
        path.write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        for mode, flags in (("normal", []), ("optimized", ["-O"])):
            result = run(
                python,
                flags,
                Path("check_parametric_identities.py"),
                [],
                copied,
                args.timeout,
            )
            require_rejection(
                failures,
                f"m6-coordinate-order/{mode}",
                result,
                "M6IdentityError",
            )

    for mode, flags in (("normal", []), ("optimized", ["-O"])):
        result = run(
            python,
            flags,
            Path("releases/m6-balanced/certify_base_psd_flint.py"),
            ["--inject-indefinite"],
            ROOT,
            args.timeout,
        )
        require_rejection(
            failures,
            f"m6-indefinite-criterion/{mode}",
            result,
            "M6BasePSDError",
        )

    for mode, flags in (("normal", []), ("optimized", ["-O"])):
        result = run(
            python,
            flags,
            Path(
                "releases/m5/counterexamples/"
                "verify_n5_lower_counterexample.py"
            ),
            ["--inject-omit-rr-path"],
            ROOT,
            args.timeout,
        )
        require_rejection(
            failures,
            f"second-moment-omit-path/{mode}",
            result,
            "VerificationError",
        )

    if failures:
        print("EXTENDED NEGATIVE CONTROLS: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("EXTENDED NEGATIVE CONTROLS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
