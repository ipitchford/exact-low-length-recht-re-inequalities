#!/usr/bin/env python3
"""Exact coefficient-identity verifier for the m=6 balanced release.

This freshly reconstructs the stable degree-three word orbits and
expands all free word-pattern equations. Positive semidefiniteness of the
two seed Gram matrices is checked separately by ``certify_base_psd_flint.py``.
"""

from __future__ import annotations

import ast
import json
import math
from collections import OrderedDict
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
N = sp.symbols("n")


class M6IdentityError(RuntimeError):
    """Raised when the reconstructed m=6 identity system does not vanish."""


def require(condition: bool, context: str) -> None:
    if not condition:
        raise M6IdentityError(context)


def words(alphabet_size: int) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = [()]
    for length in range(1, 4):
        result.extend(
            tuple(word)
            for word in __import__("itertools").product(
                range(alphabet_size),
                repeat=length,
            )
        )
    return result


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


def restricted_growth_strings(length: int) -> list[tuple[int, ...]]:
    if length == 0:
        return [()]
    result: list[tuple[int, ...]] = []

    def extend(prefix: list[int], maximum: int) -> None:
        if len(prefix) == length:
            result.append(tuple(prefix))
            return
        for symbol in range(maximum + 2):
            prefix.append(symbol)
            extend(prefix, max(maximum, symbol))
            prefix.pop()

    extend([0], 0)
    return result


def swap_distinguished(
    word: tuple[int, ...],
    distinguished: int,
) -> tuple[int, ...]:
    return tuple(
        distinguished
        if symbol == 0
        else 0
        if symbol == distinguished
        else symbol
        for symbol in word
    )


def falling(variable: sp.Symbol, length: int) -> sp.Expr:
    return sp.prod(variable - j for j in range(length))


def arithmetic_expression(expression: str) -> sp.Expr:
    """Parse the certificate's restricted rational-expression grammar."""

    def evaluate(node: ast.AST) -> sp.Expr:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return sp.Integer(node.value)
        if isinstance(node, ast.Name) and node.id == "n":
            return N
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
                require(right != 0, "division by zero in certificate expression")
                return left / right
            if isinstance(node.op, ast.Pow):
                require(
                    bool(right.is_Integer),
                    f"nonintegral exponent {right}",
                )
                return left ** int(right)
        raise M6IdentityError(
            "unsupported certificate expression node "
            f"{ast.dump(node, include_attributes=False)}"
        )

    return sp.cancel(evaluate(ast.parse(expression, mode="eval")))


def load_functions(side: str) -> list[sp.Expr]:
    path = ROOT / f"m6_{side}_parametric_functions.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    require(record["side"] == side, f"{path.name}: side metadata mismatch")
    require(
        record["base"] == (7 if side == "upper" else 8),
        f"{path.name}: unexpected base {record['base']}",
    )
    require(
        isinstance(record.get("functions"), list)
        and all(
            isinstance(expression, str) and expression.strip()
            for expression in record["functions"]
        ),
        f"{path.name}: functions must be a list of nonempty strings",
    )
    functions = [
        arithmetic_expression(expression)
        for expression in record["functions"]
    ]
    require(
        len(functions) == 1008,
        f"{path.name}: expected 1008 functions, got {len(functions)}",
    )
    return functions


def main() -> int:
    g_orbits = orbit_map(True)
    h_orbits = orbit_map(False)
    require(
        len(g_orbits) == 797 and len(h_orbits) == 211,
        f"stable orbit counts are G={len(g_orbits)}, H={len(h_orbits)}",
    )
    patterns = sum(
        (restricted_growth_strings(length) for length in range(8)),
        [],
    )
    require(
        len(patterns) == 1156,
        f"expected 1156 word patterns, got {len(patterns)}",
    )
    all_distinct = tuple(range(6))

    for side in ("upper", "lower"):
        functions = load_functions(side)
        require(
            sp.cancel(functions[797] - falling(N - 1, 5)) == 0,
            f"{side}: first H-coordinate ordering fingerprint failed",
        )
        sign = -1 if side == "upper" else 1
        for row, pattern in enumerate(patterns):
            degree = len(pattern)
            expression = sp.Integer(0)
            for split in range(4):
                if 0 <= degree - split - 1 <= 3:
                    left = tuple(reversed(pattern[:split]))
                    distinguished = pattern[split]
                    right = pattern[split + 1 :]
                    key = canonical_entry(
                        swap_distinguished(left, distinguished),
                        swap_distinguished(right, distinguished),
                        True,
                    )
                    expression += functions[g_orbits[key]]
            for split in range(4):
                if 0 <= degree - split <= 3:
                    left = tuple(reversed(pattern[:split]))
                    right = pattern[split:]
                    key = canonical_entry(left, right, False)
                    expression += N * functions[797 + h_orbits[key]]
            for split in range(4):
                if 0 <= degree - split - 1 <= 3:
                    left = tuple(reversed(pattern[:split]))
                    right = pattern[split + 1 :]
                    key = canonical_entry(left, right, False)
                    expression -= functions[797 + h_orbits[key]]

            target = (
                falling(N, 6)
                if pattern == ()
                else sp.Integer(sign)
                if pattern == all_distinct
                else sp.Integer(0)
            )
            residual = sp.cancel(expression - target)
            require(
                residual == 0,
                f"{side}: pattern {row}/{pattern} has residual {residual}",
            )
        print(
            f"M6 {side.upper()}: 1,156 exact rational coefficient "
            "identities passed."
        )

    print("M6 IDENTITY LAYER: EXACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
