#!/usr/bin/env python3
"""Exact base-PSD certificates for the m=6 balanced-family release.

Requires python-flint 0.8.0.  Each rational full Gram matrix is multiplied by
a common positive denominator and converted to an integer matrix.  For a real
symmetric matrix A, all eigenvalues are nonnegative if and only if every
coefficient of det(t I + A) is nonnegative: symmetry makes all roots real,
and a negative eigenvalue would give a positive root while a polynomial with
nonnegative coefficients is strictly positive on t>0.

This proves PSD only at the two base sizes.  Combined with the balanced-seed
continuation theorem and the separate exact identity audit, it supports the
upper m=6 inequality on multiples of 7 and the lower inequality on multiples
of 8.  It does not prove either inequality at intervening sizes.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import math
import time
from collections import OrderedDict
from fractions import Fraction as F
from pathlib import Path

import flint
from flint import fmpz_mat


ROOT = Path(__file__).resolve().parent
EXPECTED_JSON_SHA256 = {
    "upper": "f0db80568847c91ef075fa49640205d07d96c96b22f3b706cd0db62066cabb6c",
    "lower": "a24bf15495988840bb3cd30bcde4a1de5528a1d6633f32295c2deb9d50a9a186",
}
EXPECTED_DENOMINATORS = {
    "upper": 16941456000000,
    "lower": 262144000000,
}
EXPECTED_MATRICES = {
    ("upper", "G"): (
        400,
        399,
        "c95af891ab9992fd2681af349044732a988ba147db9e43eec4288e2317589f51",
    ),
    ("upper", "H"): (
        400,
        400,
        "a8bbe7306acc878d612c8d8bd3695a036d35852e3d1257263205ec809a497419",
    ),
    ("lower", "G"): (
        585,
        585,
        "bd0867a98fd93a7cb624200f7d965cf4983448e0cf30c843d7b7fd7a49729a03",
    ),
    ("lower", "H"): (
        585,
        585,
        "32e99420c0feb2bbbcd08fdf4e40fc2847ed1ab945620073397b5394d75b6a46",
    ),
}


class M6BasePSDError(RuntimeError):
    """Raised when an exact base-PSD obligation fails."""


def require(condition: bool, context: str) -> None:
    if not condition:
        raise M6BasePSDError(context)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inject-indefinite",
        action="store_true",
        help="Run a known-bad 2x2 criterion fixture and require rejection",
    )
    return parser.parse_args()


def arithmetic_fraction(expression: str, n: int) -> F:
    """Evaluate the restricted rational-expression grammar exactly."""

    def evaluate(node: ast.AST) -> F:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return F(node.value)
        if isinstance(node, ast.Name) and node.id == "n":
            return F(n)
        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op,
            (ast.UAdd, ast.USub),
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                require(
                    right.denominator == 1,
                    f"nonintegral exponent {right}",
                )
                return left ** right.numerator
        raise M6BasePSDError(
            f"unsupported expression node "
            f"{ast.dump(node, include_attributes=False)}"
        )

    return evaluate(ast.parse(expression, mode="eval"))


def words(alphabet_size: int) -> list[tuple[int, ...]]:
    return [()] + [
        tuple(word)
        for length in range(1, 4)
        for word in itertools.product(range(alphabet_size), repeat=length)
    ]


def canonical_entry(
    left: tuple[int, ...],
    right: tuple[int, ...],
    stabilizer: bool,
) -> tuple[int, ...]:
    def encode(
        first: tuple[int, ...],
        second: tuple[int, ...],
    ) -> tuple[int, ...]:
        relation = {0: 0} if stabilizer else {}
        next_label = 1 if stabilizer else 0
        output: list[int] = []
        for symbol in (*first, -1, *second):
            if symbol == -1:
                output.append(-1)
                continue
            if symbol not in relation:
                relation[symbol] = next_label
                next_label += 1
            output.append(relation[symbol])
        return tuple(output)

    return min(encode(left, right), encode(right, left))


def orbit_map(stabilizer: bool) -> OrderedDict[tuple[int, ...], int]:
    result: OrderedDict[tuple[int, ...], int] = OrderedDict()
    for left in words(7):
        for right in words(7):
            key = canonical_entry(left, right, stabilizer)
            if key not in result:
                result[key] = len(result)
    return result


def integer_gram(
    alphabet_size: int,
    integer_values: list[int],
    orbits: OrderedDict[tuple[int, ...], int],
    stabilizer: bool,
    offset: int,
) -> fmpz_mat:
    basis = words(alphabet_size)
    rows = [[0] * len(basis) for _ in basis]
    for i, left in enumerate(basis):
        for j in range(i, len(basis)):
            key = canonical_entry(left, basis[j], stabilizer)
            value = integer_values[offset + orbits[key]]
            rows[i][j] = value
            rows[j][i] = value
    require(
        all(rows[i][j] == rows[j][i] for i in range(len(rows)) for j in range(len(rows))),
        "constructed Gram matrix is not symmetric",
    )
    return fmpz_mat(rows)


def certify_matrix(
    matrix: fmpz_mat,
    label: str,
    expected_size: int,
    expected_rank: int,
    expected_digest: str,
    expected_all_ones_kernel: bool = False,
) -> None:
    size = matrix.nrows()
    require(
        size == expected_size and matrix.ncols() == expected_size,
        f"{label}: size {size}x{matrix.ncols()}, expected "
        f"{expected_size}x{expected_size}",
    )
    print(f"{label}: exact rank...", flush=True)
    rank = matrix.rank()
    require(
        rank == expected_rank,
        f"{label}: rank {rank}, expected {expected_rank}",
    )
    if expected_all_ones_kernel:
        ones = fmpz_mat([[1] for _ in range(size)])
        product = matrix * ones
        require(
            all(int(product[row, 0]) == 0 for row in range(size)),
            f"{label}: all-ones equality vector is not in the kernel",
        )
        require(
            size - rank == 1,
            f"{label}: all-ones vector does not span a one-dimensional kernel",
        )
        print(f"{label}: all-ones kernel PASS", flush=True)
    started = time.monotonic()
    print(f"{label}: exact characteristic polynomial...", flush=True)
    characteristic = matrix.charpoly()
    elapsed = time.monotonic() - started
    coefficients = list(characteristic.coeffs())
    require(
        len(coefficients) == size + 1,
        f"{label}: characteristic degree mismatch",
    )
    plus_coefficients = [
        ((-1) ** (size + degree)) * int(coefficient)
        for degree, coefficient in enumerate(coefficients)
    ]
    require(
        all(coefficient >= 0 for coefficient in plus_coefficients),
        f"{label}: det(tI+A) has negative coefficients at "
        f"{[i for i, z in enumerate(plus_coefficients) if z < 0][:5]}",
    )
    zero_count = sum(coefficient == 0 for coefficient in plus_coefficients)
    expected_zeros = size - expected_rank
    require(
        zero_count == expected_zeros,
        f"{label}: coefficient zero count {zero_count}, "
        f"expected {expected_zeros}",
    )
    digest = hashlib.sha256(
        "\n".join(map(str, coefficients)).encode("ascii")
    ).hexdigest()
    require(
        digest == expected_digest,
        f"{label}: characteristic coefficient digest {digest}, "
        f"expected {expected_digest}",
    )
    positive_bits = [
        coefficient.bit_length()
        for coefficient in plus_coefficients
        if coefficient > 0
    ]
    print(
        f"{label}: PSD PASS; size={size}, rank={rank}, "
        f"det(tI+A) nonnegative coefficients={len(coefficients)}, "
        f"zero_coefficients={zero_count}, "
        f"coefficient_bits={min(positive_bits)}..{max(positive_bits)}, "
        f"raw_det_xI_minus_A_coeffs_sha256={digest}, "
        f"elapsed={elapsed:.3f}s",
        flush=True,
    )


def main() -> int:
    args = parse_args()
    require(
        flint.__version__ == "0.8.0",
        f"python-flint {flint.__version__} is installed; expected 0.8.0",
    )
    if args.inject_indefinite:
        indefinite = fmpz_mat([[1, 0], [0, -1]])
        certify_matrix(
            indefinite,
            "KNOWN-BAD indefinite fixture",
            expected_size=2,
            expected_rank=2,
            expected_digest="fixture-must-fail-before-digest",
        )
        raise M6BasePSDError("known-bad indefinite fixture was accepted")

    g_orbits = orbit_map(True)
    h_orbits = orbit_map(False)
    require(
        (len(g_orbits), len(h_orbits)) == (797, 211),
        f"unexpected orbit counts {(len(g_orbits), len(h_orbits))}",
    )
    for side, alphabet_size in (("upper", 7), ("lower", 8)):
        path = ROOT / f"m6_{side}_parametric_functions.json"
        observed_json_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(
            observed_json_digest == EXPECTED_JSON_SHA256[side],
            f"{path.name}: SHA-256 {observed_json_digest}, expected "
            f"{EXPECTED_JSON_SHA256[side]}",
        )
        record = json.loads(path.read_text(encoding="utf-8"))
        require(
            record.get("side") == side,
            f"{path.name}: side metadata mismatch",
        )
        require(
            record.get("base") == alphabet_size,
            f"{path.name}: base metadata mismatch",
        )
        require(
            isinstance(record.get("functions"), list)
            and len(record["functions"]) == 1008
            and all(
                isinstance(expression, str) and expression.strip()
                for expression in record["functions"]
            ),
            f"{path.name}: expected 1008 nonempty function strings",
        )
        values = [
            arithmetic_fraction(expression, alphabet_size)
            for expression in record["functions"]
        ]
        require(len(values) == 1008, f"{side}: expected 1008 values")
        denominator = 1
        for value in values:
            denominator = math.lcm(denominator, value.denominator)
        require(
            denominator == EXPECTED_DENOMINATORS[side],
            f"{side}: common denominator {denominator}, expected "
            f"{EXPECTED_DENOMINATORS[side]}",
        )
        integer_values = [
            value.numerator * (denominator // value.denominator)
            for value in values
        ]
        require(
            all(F(value, denominator) == original for value, original in zip(integer_values, values)),
            f"{side}: common-denominator conversion failed",
        )
        print(
            f"M6 {side} n={alphabet_size}: "
            f"common denominator={denominator}",
            flush=True,
        )
        for label, stabilizer, offset, orbits in (
            ("G", True, 0, g_orbits),
            ("H", False, 797, h_orbits),
        ):
            expected_size, expected_rank, expected_digest = EXPECTED_MATRICES[
                (side, label)
            ]
            matrix = integer_gram(
                alphabet_size,
                integer_values,
                orbits,
                stabilizer,
                offset,
            )
            certify_matrix(
                matrix,
                f"M6 {side} n={alphabet_size} {label}",
                expected_size,
                expected_rank,
                expected_digest,
                expected_all_ones_kernel=(
                    side == "upper" and label == "G"
                ),
            )
    print("M6 BASE PSD: EXACT PASS (python-flint 0.8.0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
