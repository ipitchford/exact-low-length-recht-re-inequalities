#!/usr/bin/env python3
"""Numerical NON-RELEASE PSD probe for the inherited m=6 base matrices.

This builds the full concrete degree-three Gram matrices at n=7 (upper) and
n=8 (lower), bypassing the missing representation bases.  Floating-point
eigenvalues are reconnaissance only and cannot certify a theorem.
"""

from __future__ import annotations

import ast
import itertools
import json
from collections import OrderedDict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
CERT_ROOT = ROOT.parents[1] / "releases/m6-balanced"


class ProbeError(RuntimeError):
    """Raised when the exploratory schema is inconsistent."""


def require(condition: bool, context: str) -> None:
    if not condition:
        raise ProbeError(context)


def arithmetic_value(expression: str, n: int) -> float:
    """Evaluate the restricted arithmetic grammar used by the JSON files."""

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id == "n":
            return float(n)
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
                return left**right
        raise ProbeError(
            f"unsupported expression node {ast.dump(node, include_attributes=False)}"
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


def full_matrix(
    alphabet_size: int,
    values: list[float],
    orbits: OrderedDict[tuple[int, ...], int],
    stabilizer: bool,
    offset: int,
) -> np.ndarray:
    basis = words(alphabet_size)
    matrix = np.empty((len(basis), len(basis)), dtype=np.float64)
    for i, left in enumerate(basis):
        for j in range(i, len(basis)):
            key = canonical_entry(left, basis[j], stabilizer)
            entry = values[offset + orbits[key]]
            matrix[i, j] = entry
            matrix[j, i] = entry
    return matrix


def main() -> int:
    g_orbits = orbit_map(True)
    h_orbits = orbit_map(False)
    require(
        (len(g_orbits), len(h_orbits)) == (797, 211),
        f"unexpected orbit counts {(len(g_orbits), len(h_orbits))}",
    )
    for side, alphabet_size in (("upper", 7), ("lower", 8)):
        record = json.loads(
            (CERT_ROOT / f"m6_{side}_parametric_functions.json").read_text(
                encoding="utf-8"
            )
        )
        values = [
            arithmetic_value(expression, alphabet_size)
            for expression in record["functions"]
        ]
        require(len(values) == 1008, f"{side}: expected 1008 values")
        for label, stabilizer, offset, orbits in (
            ("G", True, 0, g_orbits),
            ("H", False, 797, h_orbits),
        ):
            matrix = full_matrix(
                alphabet_size,
                values,
                orbits,
                stabilizer,
                offset,
            )
            eigenvalues = np.linalg.eigvalsh(matrix)
            scale = max(1.0, float(np.max(np.abs(eigenvalues))))
            tolerance = 1e-9 * scale
            print(
                f"M6 {side} n={alphabet_size} {label}: "
                f"size={len(matrix)}, min={eigenvalues[0]:.12g}, "
                f"max={eigenvalues[-1]:.12g}, "
                f"below(-tol)={int(np.sum(eigenvalues < -tolerance))}, "
                f"near_zero={int(np.sum(np.abs(eigenvalues) <= tolerance))}"
            )
    print("M6 BASE PSD PROBE: NUMERICAL RECONNAISSANCE ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
