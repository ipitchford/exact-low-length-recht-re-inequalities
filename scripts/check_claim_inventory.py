#!/usr/bin/env python3
"""Derive the unified paper's quantitative evidence inventory from JSON."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "m4": {
        "orbit_functions": 162,
        "free_functions": 53,
        "minors": 51,
        "upper_coefficients": 365,
        "lower_coefficients": 410,
        "endpoints": 2,
    },
    "m5": {
        "orbit_functions": 162,
        "free_functions": 53,
        "minors": 51,
        "upper_coefficients": 438,
        "lower_coefficients": 491,
        "endpoints": 1,
    },
}
EXPECTED_M6 = {
    "upper": {
        "base": 7,
        "sha256": "f0db80568847c91ef075fa49640205d07d96c96b22f3b706cd0db62066cabb6c",
    },
    "lower": {
        "base": 8,
        "sha256": "a24bf15495988840bb3cd30bcde4a1de5528a1d6633f32295c2deb9d50a9a186",
    },
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def minor_inventory(path: Path) -> tuple[int, int, int]:
    record = load(path)
    minors = 0
    upper_coefficients = 0
    lower_coefficients = 0
    for key, block in record.items():
        if not isinstance(block, dict) or "leading_principal_minors" not in block:
            continue
        side = key.split("_", 1)[0]
        for minor in block["leading_principal_minors"]:
            coefficients = [
                Fraction(value)
                for value in minor["coefficients_ascending_in_t"]
            ]
            if not coefficients or not all(value > 0 for value in coefficients):
                raise ValueError(f"{path}: nonpositive or empty coefficients in {key}")
            if minor["degree"] != len(coefficients) - 1:
                raise ValueError(f"{path}: degree/count mismatch in {key}")
            minors += 1
            if side == "upper":
                upper_coefficients += len(coefficients)
            elif side == "lower":
                lower_coefficients += len(coefficients)
            else:
                raise ValueError(f"{path}: unknown side in {key}")
    return minors, upper_coefficients, lower_coefficients


def release_inventory(name: str) -> dict[str, int]:
    certificate_root = ROOT / f"releases/{name}/certificates"
    parametric = load(certificate_root / "parametric_orbit_functions.json")
    orbit_functions = sum(
        len(parametric[side]["orbit_functions"]) for side in ("upper", "lower")
    )
    free_functions = sum(
        len(parametric[side]["free_functions"]) for side in ("upper", "lower")
    )
    minors, upper_coefficients, lower_coefficients = minor_inventory(
        certificate_root / "principal_minors.json"
    )
    endpoint_file = (
        certificate_root / "n4_orbit_certificates.json"
        if name == "m4"
        else certificate_root / "n5_upper_certificate.json"
    )
    endpoints = sum(
        side in load(endpoint_file) for side in ("upper", "lower")
    )
    return {
        "orbit_functions": orbit_functions,
        "free_functions": free_functions,
        "minors": minors,
        "upper_coefficients": upper_coefficients,
        "lower_coefficients": lower_coefficients,
        "endpoints": endpoints,
    }


def main() -> int:
    inventories = {name: release_inventory(name) for name in ("m4", "m5")}
    failures: list[str] = []
    for name, inventory in inventories.items():
        print(f"{name}: {inventory}")
        for field, expected in EXPECTED[name].items():
            actual = inventory[field]
            if actual != expected:
                failures.append(
                    f"{name}/{field}: expected {expected}, found {actual}"
                )

    totals = {
        field: sum(inventory[field] for inventory in inventories.values())
        for field in EXPECTED["m4"]
    }
    positive_coefficients = (
        totals["upper_coefficients"] + totals["lower_coefficients"]
    )
    print(
        "unified: "
        f"{totals['orbit_functions']} orbit functions, "
        f"{totals['free_functions']} selected free functions, "
        f"{totals['minors']} minors, "
        f"{positive_coefficients} positive shifted coefficients, "
        f"{totals['endpoints']} endpoint certificates"
    )
    if positive_coefficients != 1704:
        failures.append(
            "unified/positive_coefficients: expected 1704, "
            f"found {positive_coefficients}"
        )

    m6_root = ROOT / "releases/m6-balanced"
    m6_functions = 0
    for side, expected in EXPECTED_M6.items():
        path = m6_root / f"m6_{side}_parametric_functions.json"
        record = load(path)
        functions = record.get("functions")
        if record.get("side") != side:
            failures.append(f"m6/{side}: side metadata mismatch")
        if record.get("base") != expected["base"]:
            failures.append(
                f"m6/{side}: expected base {expected['base']}, "
                f"found {record.get('base')}"
            )
        if (
            not isinstance(functions, list)
            or len(functions) != 1008
            or not all(
                isinstance(expression, str) and expression.strip()
                for expression in functions
            )
        ):
            failures.append(
                f"m6/{side}: expected 1008 nonempty function strings"
            )
        else:
            m6_functions += len(functions)
        observed_digest = sha256(path)
        if observed_digest != expected["sha256"]:
            failures.append(
                f"m6/{side}: SHA-256 {observed_digest}, "
                f"expected {expected['sha256']}"
            )
    print(
        "m6-balanced: "
        f"{m6_functions} rational functions, "
        "2,312 coefficient identities, 4 full seed Gram matrices"
    )
    if m6_functions != 2016:
        failures.append(
            f"m6/functions: expected 2016, found {m6_functions}"
        )
    if failures:
        print("CLAIM INVENTORY: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("CLAIM INVENTORY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
