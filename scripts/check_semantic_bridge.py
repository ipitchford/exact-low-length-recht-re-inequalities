#!/usr/bin/env python3
"""Independent semantic checks for the Recht--Re certificate encoding.

This checker deliberately does not use the compressed coefficient matrices or
the stored representation blocks.  It rebuilds the mathematical bridge from:

* concrete words and explicit permutation actions;
* invariant Gram-matrix orbit coordinates;
* direct (uncompressed) free-localizer expansion; and
* explicit symmetry-adapted representative vectors.

All acceptance arithmetic is exact.  The ``--inject`` options are known-bad
fixtures used by ``tests/semantic_negative_controls.py``.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import OrderedDict, defaultdict, deque
from fractions import Fraction as F
from pathlib import Path
from typing import Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]


class SemanticError(RuntimeError):
    """Raised when a theorem-to-certificate semantic obligation fails."""


def require(condition: bool, context: str) -> None:
    if not condition:
        raise SemanticError(context)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inject",
        choices=(
            "none",
            "omit-pattern",
            "corrupt-orbit",
            "corrupt-vector",
            "omit-block",
        ),
        default="none",
        help="Inject one known semantic fault; for negative-control use only.",
    )
    return parser.parse_args()


ARGS = parse_args()


# ---------------------------------------------------------------------------
# Exact linear algebra


def rank_fraction(rows: Iterable[Sequence[int | F]]) -> int:
    matrix = [list(map(F, row)) for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        for j in range(column, column_count):
            matrix[rank][j] /= pivot_value
        for row in range(row_count):
            if row == rank or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            for j in range(column, column_count):
                matrix[row][j] -= multiplier * matrix[rank][j]
        rank += 1
        if rank == row_count:
            break
    return rank


class RowSpace:
    """Small exact row space used for orbit-span checks."""

    def __init__(self, width: int):
        self.width = width
        self.pivots: dict[int, list[F]] = {}

    def add(self, source: Sequence[int | F]) -> bool:
        row = list(map(F, source))
        require(
            len(row) == self.width,
            f"row-space width mismatch: expected {self.width}, got {len(row)}",
        )
        for pivot in sorted(self.pivots):
            if row[pivot]:
                multiplier = row[pivot]
                base = self.pivots[pivot]
                for column in range(pivot, self.width):
                    row[column] -= multiplier * base[column]
        pivot = next((j for j, value in enumerate(row) if value), None)
        if pivot is None:
            return False
        pivot_value = row[pivot]
        for column in range(pivot, self.width):
            row[column] /= pivot_value
        for old_pivot, base in list(self.pivots.items()):
            if base[pivot]:
                multiplier = base[pivot]
                for column in range(pivot, self.width):
                    base[column] -= multiplier * row[column]
                self.pivots[old_pivot] = base
        self.pivots[pivot] = row
        return True

    @property
    def rank(self) -> int:
        return len(self.pivots)


def exact_psd_ldl(matrix: Sequence[Sequence[F]], label: str) -> None:
    """Certify PSD by exact symmetric elimination.

    For a PSD matrix, a zero diagonal in any Schur complement forces its
    remaining row and column to vanish.  Thus this no-pivot LDL test is both
    necessary and sufficient over the rationals.
    """

    work = [list(map(F, row)) for row in matrix]
    size = len(work)
    require(
        all(len(row) == size for row in work),
        f"{label}: matrix is not square",
    )
    require(
        all(work[i][j] == work[j][i] for i in range(size) for j in range(size)),
        f"{label}: matrix is not symmetric",
    )
    for k in range(size):
        pivot = work[k][k]
        require(pivot >= 0, f"{label}: negative LDL pivot {pivot} at {k}")
        if pivot == 0:
            nonzero = [j for j in range(k + 1, size) if work[k][j]]
            require(
                not nonzero,
                f"{label}: zero LDL pivot has nonzero entries at {nonzero}",
            )
            continue
        for i in range(k + 1, size):
            for j in range(i, size):
                work[i][j] -= work[i][k] * work[k][j] / pivot
                work[j][i] = work[i][j]


# ---------------------------------------------------------------------------
# Concrete words, equality patterns, and invariant Gram orbits


Word = tuple[int, ...]
Pair = tuple[Word, Word]


def words(n: int) -> list[Word]:
    return (
        [()]
        + [(i,) for i in range(n)]
        + [(i, j) for i in range(n) for j in range(n)]
    )


def transpose_normalized(left: Word, right: Word) -> Pair:
    return min((left, right), (right, left))


def canonical_entry(
    left: Word,
    right: Word,
    distinguished: int | None,
) -> tuple[int, ...]:
    """Canonical equality pattern of an unordered pair of words.

    When ``distinguished`` is not ``None``, its label is fixed as canonical
    label zero and all other labels are canonically renamed by first
    appearance.  Otherwise every label is renamed by first appearance.
    """

    def one(first: Word, second: Word) -> tuple[int, ...]:
        relation = {distinguished: 0} if distinguished is not None else {}
        next_label = 1 if distinguished is not None else 0
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

    key = min(one(left, right), one(right, left))
    if ARGS.inject == "corrupt-orbit" and distinguished is not None:
        # Merge two genuine point-stabilizer classes.  The explicit group
        # action comparison below must reject this convention.
        if key == (0, -1, 0):
            return (0, -1)
    return key


def orbit_map(distinguished: int | None) -> OrderedDict[tuple[int, ...], int]:
    result: OrderedDict[tuple[int, ...], int] = OrderedDict()
    for left in words(6):
        for right in words(6):
            key = canonical_entry(left, right, distinguished)
            if key not in result:
                result[key] = len(result)
    return result


G_ORBITS = orbit_map(0)
H_ORBITS = orbit_map(None)


def restricted_growth(word: Word) -> Word:
    relation: dict[int, int] = {}
    output: list[int] = []
    for symbol in word:
        if symbol not in relation:
            relation[symbol] = len(relation)
        output.append(relation[symbol])
    return tuple(output)


def restricted_growth_strings(length: int) -> list[Word]:
    if length == 0:
        return [()]
    result: list[Word] = []

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


PATTERNS = sum(
    (restricted_growth_strings(length) for length in range(6)),
    [],
)
if ARGS.inject == "omit-pattern":
    PATTERNS = PATTERNS[:-1]


def apply_permutation(word: Word, permutation: Sequence[int]) -> Word:
    return tuple(permutation[symbol] for symbol in word)


def permutation_family(n: int, distinguished: int | None) -> list[tuple[int, ...]]:
    if distinguished is None:
        return list(itertools.permutations(range(n)))
    other = [i for i in range(n) if i != distinguished]
    result: list[tuple[int, ...]] = []
    for image in itertools.permutations(other):
        permutation = list(range(n))
        for source, target in zip(other, image):
            permutation[source] = target
        result.append(tuple(permutation))
    return result


def actual_orbit_key(
    pair: Pair,
    permutations: Sequence[Sequence[int]],
) -> Pair:
    left, right = pair
    return min(
        transpose_normalized(
            apply_permutation(left, permutation),
            apply_permutation(right, permutation),
        )
        for permutation in permutations
    )


def audit_orbit_classifier() -> None:
    n = 5
    basis = words(n)
    unordered_pairs = [
        (basis[i], basis[j])
        for i in range(len(basis))
        for j in range(i, len(basis))
    ]
    for label, distinguished, expected in (
        ("G", 0, 59),
        ("H", None, 22),
    ):
        permutations = permutation_family(n, distinguished)
        actual_to_canonical: dict[Pair, set[tuple[int, ...]]] = defaultdict(set)
        canonical_to_actual: dict[tuple[int, ...], set[Pair]] = defaultdict(set)
        for pair in unordered_pairs:
            actual = actual_orbit_key(pair, permutations)
            canonical = canonical_entry(*pair, distinguished)
            actual_to_canonical[actual].add(canonical)
            canonical_to_actual[canonical].add(actual)
        require(
            len(actual_to_canonical) == expected,
            f"{label}: explicit permutation action has "
            f"{len(actual_to_canonical)} orbits, expected {expected}",
        )
        require(
            len(canonical_to_actual) == expected,
            f"{label}: canonical classifier has "
            f"{len(canonical_to_actual)} classes, expected {expected}",
        )
        require(
            all(len(keys) == 1 for keys in actual_to_canonical.values())
            and all(len(keys) == 1 for keys in canonical_to_actual.values()),
            f"{label}: canonical classifier is not equivalent to group orbits",
        )
    print("ORBIT CLASSIFIER: explicit S_5 and S_4 actions give exactly 22 and 59 classes.")


def audit_word_patterns() -> None:
    concrete = {
        restricted_growth(word)
        for length in range(6)
        for word in itertools.product(range(5), repeat=length)
    }
    encoded = set(PATTERNS)
    require(
        len(PATTERNS) == len(encoded),
        "word-pattern list contains duplicates",
    )
    require(
        concrete == encoded and len(encoded) == 76,
        f"word-pattern coverage mismatch: concrete={len(concrete)}, "
        f"encoded={len(encoded)}, missing={sorted(concrete - encoded)[:3]}, "
        f"extra={sorted(encoded - concrete)[:3]}",
    )
    print("WORD PATTERNS: all concrete words through degree five give exactly 76 classes.")


# ---------------------------------------------------------------------------
# Direct, uncompressed certificate expansion


def falling(n: int, m: int) -> int:
    return math.prod(n - j for j in range(m))


def load_orbit_values(relative: str, side: str) -> list[F]:
    path = ROOT / relative
    record = json.loads(path.read_text(encoding="utf-8"))[side]
    values = list(map(F, record["orbit_values"]))
    require(
        len(values) == 81,
        f"{relative}/{side}: expected 81 orbit values, got {len(values)}",
    )
    return values


def gram_entry(
    values: Sequence[F],
    left: Word,
    right: Word,
    distinguished: int | None,
) -> F:
    key = canonical_entry(left, right, distinguished)
    if distinguished is None:
        return values[59 + H_ORBITS[key]]
    return values[G_ORBITS[key]]


def direct_localizer_expansion(
    n: int,
    values: Sequence[F],
) -> dict[Word, F]:
    basis = words(n)
    coefficients: defaultdict[Word, F] = defaultdict(F)
    for distinguished in range(n):
        for left in basis:
            reversed_left = tuple(reversed(left))
            for right in basis:
                entry = gram_entry(
                    values,
                    left,
                    right,
                    distinguished,
                )
                if entry:
                    coefficients[
                        reversed_left + (distinguished,) + right
                    ] += entry
    for left in basis:
        reversed_left = tuple(reversed(left))
        for right in basis:
            entry = gram_entry(values, left, right, None)
            if not entry:
                continue
            coefficients[reversed_left + right] += n * entry
            for generator in range(n):
                coefficients[
                    reversed_left + (generator,) + right
                ] -= entry
    return {
        word: coefficient
        for word, coefficient in coefficients.items()
        if coefficient
    }


def target_polynomial(n: int, m: int, side: str) -> dict[Word, F]:
    target: dict[Word, F] = {(): F(falling(n, m))}
    sign = F(-1 if side == "upper" else 1)
    for word in itertools.permutations(range(n), m):
        target[word] = sign
    return target


def full_gram_matrix(
    n: int,
    values: Sequence[F],
    distinguished: int | None,
) -> list[list[F]]:
    basis = words(n)
    return [
        [
            gram_entry(values, left, right, distinguished)
            for right in basis
        ]
        for left in basis
    ]


def audit_concrete_certificates() -> None:
    obligations = (
        (
            "m4/base5/upper",
            5,
            4,
            "upper",
            "releases/m4/certificates/base5_seed_certificates.json",
        ),
        (
            "m4/base5/lower",
            5,
            4,
            "lower",
            "releases/m4/certificates/base5_seed_certificates.json",
        ),
        (
            "m4/n4/upper",
            4,
            4,
            "upper",
            "releases/m4/certificates/n4_orbit_certificates.json",
        ),
        (
            "m4/n4/lower",
            4,
            4,
            "lower",
            "releases/m4/certificates/n4_orbit_certificates.json",
        ),
        (
            "m5/base6/upper",
            6,
            5,
            "upper",
            "releases/m5/certificates/base6_seed_certificates.json",
        ),
        (
            "m5/base6/lower",
            6,
            5,
            "lower",
            "releases/m5/certificates/base6_seed_certificates.json",
        ),
        (
            "m5/n5/upper",
            5,
            5,
            "upper",
            "releases/m5/certificates/n5_upper_certificate.json",
        ),
    )
    for label, n, m, side, relative in obligations:
        values = load_orbit_values(relative, side)
        actual = direct_localizer_expansion(n, values)
        expected = target_polynomial(n, m, side)
        all_words = set(actual) | set(expected)
        discrepancies = [
            (word, actual.get(word, F(0)), expected.get(word, F(0)))
            for word in sorted(all_words, key=lambda word: (len(word), word))
            if actual.get(word, F(0)) != expected.get(word, F(0))
        ]
        require(
            not discrepancies,
            f"{label}: direct concrete-word identity failed; "
            f"first discrepancies={discrepancies[:3]}",
        )
        exact_psd_ldl(
            full_gram_matrix(n, values, 0),
            f"{label}/G",
        )
        exact_psd_ldl(
            full_gram_matrix(n, values, None),
            f"{label}/H",
        )
    print("CONCRETE CERTIFICATES: seven full word-level identities and fourteen Gram PSD tests passed.")


# ---------------------------------------------------------------------------
# Symmetry-adapted representatives and completeness


Vector = list[int]


def vector(n: int, items: Iterable[tuple[Word, int]]) -> Vector:
    basis = words(n)
    index = {word: i for i, word in enumerate(basis)}
    result = [0] * len(basis)
    for word, coefficient in items:
        result[index[word]] += coefficient
    return result


def vectors_h(n: int) -> list[list[Vector]]:
    trivial = [
        vector(n, [((), 1)]),
        vector(n, [((i,), 1) for i in range(n)]),
        vector(n, [((i, i), 1) for i in range(n)]),
        vector(
            n,
            [
                ((i, j), 1)
                for i in range(n)
                for j in range(n)
                if i != j
            ],
        ),
    ]
    a = [0] * n
    a[0] = 1
    a[1] = -1
    standard = [
        vector(n, [((i,), a[i]) for i in range(n)]),
        vector(n, [((i, i), a[i]) for i in range(n)]),
        vector(
            n,
            [
                ((i, j), a[i] + a[j])
                for i in range(n)
                for j in range(n)
                if i != j
            ],
        ),
        vector(
            n,
            [
                ((i, j), a[i] - a[j])
                for i in range(n)
                for j in range(n)
                if i != j
            ],
        ),
    ]
    q = vector(
        n,
        [
            ((0, 1), 1),
            ((1, 0), 1),
            ((2, 3), 1),
            ((3, 2), 1),
            ((0, 2), -1),
            ((2, 0), -1),
            ((1, 3), -1),
            ((3, 1), -1),
        ],
    )
    cycle_items = [
        ((0, 1), 1),
        ((1, 0), -1),
        ((1, 2), 1),
        ((2, 1), -1),
        ((2, 0), 1),
        ((0, 2), -1),
    ]
    if ARGS.inject == "corrupt-vector":
        cycle_items[0] = ((0, 1), 2)
    cycle = vector(n, cycle_items)
    blocks = [trivial, standard, [q], [cycle]]
    if ARGS.inject == "omit-block":
        blocks = blocks[:-1]
    return blocks


def vectors_g(n: int) -> list[list[Vector]]:
    nondistinguished = range(1, n)
    trivial = [
        vector(n, [((), 1)]),
        vector(n, [((0,), 1)]),
        vector(n, [((i,), 1) for i in nondistinguished]),
        vector(n, [((0, 0), 1)]),
        vector(n, [((0, i), 1) for i in nondistinguished]),
        vector(n, [((i, 0), 1) for i in nondistinguished]),
        vector(n, [((i, i), 1) for i in nondistinguished]),
        vector(
            n,
            [
                ((i, j), 1)
                for i in nondistinguished
                for j in nondistinguished
                if i != j
            ],
        ),
    ]
    a = [0] * n
    a[1] = 1
    a[2] = -1
    standard = [
        vector(n, [((i,), a[i]) for i in nondistinguished]),
        vector(n, [((0, i), a[i]) for i in nondistinguished]),
        vector(n, [((i, 0), a[i]) for i in nondistinguished]),
        vector(n, [((i, i), a[i]) for i in nondistinguished]),
        vector(
            n,
            [
                ((i, j), a[i] + a[j])
                for i in nondistinguished
                for j in nondistinguished
                if i != j
            ],
        ),
        vector(
            n,
            [
                ((i, j), a[i] - a[j])
                for i in nondistinguished
                for j in nondistinguished
                if i != j
            ],
        ),
    ]
    q = vector(
        n,
        [
            ((1, 2), 1),
            ((2, 1), 1),
            ((3, 4), 1),
            ((4, 3), 1),
            ((1, 3), -1),
            ((3, 1), -1),
            ((2, 4), -1),
            ((4, 2), -1),
        ],
    )
    cycle = vector(
        n,
        [
            ((1, 2), 1),
            ((2, 1), -1),
            ((2, 3), 1),
            ((3, 2), -1),
            ((3, 1), 1),
            ((1, 3), -1),
        ],
    )
    return [trivial, standard, [q], [cycle]]


def vectors_g4() -> list[list[Vector]]:
    n = 4
    nondistinguished = range(1, n)
    trivial = [
        vector(n, [((), 1)]),
        vector(n, [((0,), 1)]),
        vector(n, [((i,), 1) for i in nondistinguished]),
        vector(n, [((0, 0), 1)]),
        vector(n, [((0, i), 1) for i in nondistinguished]),
        vector(n, [((i, 0), 1) for i in nondistinguished]),
        vector(n, [((i, i), 1) for i in nondistinguished]),
        vector(
            n,
            [
                ((i, j), 1)
                for i in nondistinguished
                for j in nondistinguished
                if i != j
            ],
        ),
    ]
    a = [0] * n
    a[1] = 1
    a[2] = -1
    standard = [
        vector(n, [((i,), a[i]) for i in nondistinguished]),
        vector(n, [((0, i), a[i]) for i in nondistinguished]),
        vector(n, [((i, 0), a[i]) for i in nondistinguished]),
        vector(n, [((i, i), a[i]) for i in nondistinguished]),
        vector(
            n,
            [
                ((i, j), a[i] + a[j])
                for i in nondistinguished
                for j in nondistinguished
                if i != j
            ],
        ),
        vector(
            n,
            [
                ((i, j), a[i] - a[j])
                for i in nondistinguished
                for j in nondistinguished
                if i != j
            ],
        ),
    ]
    sign = vector(
        n,
        [
            ((1, 2), 1),
            ((2, 1), -1),
            ((2, 3), 1),
            ((3, 2), -1),
            ((3, 1), 1),
            ((1, 3), -1),
        ],
    )
    return [trivial, standard, [sign]]


def adjacent_generators(n: int, distinguished: int | None) -> list[tuple[int, ...]]:
    labels = [i for i in range(n) if i != distinguished]
    generators: list[tuple[int, ...]] = []
    for first, second in zip(labels, labels[1:]):
        permutation = list(range(n))
        permutation[first], permutation[second] = second, first
        generators.append(tuple(permutation))
    return generators


def act_vector(
    source: Sequence[int],
    n: int,
    permutation: Sequence[int],
) -> Vector:
    basis = words(n)
    index = {word: i for i, word in enumerate(basis)}
    result = [0] * len(basis)
    for i, coefficient in enumerate(source):
        if coefficient:
            result[index[apply_permutation(basis[i], permutation)]] += coefficient
    return result


def orbit_span(
    representative: Vector,
    n: int,
    distinguished: int | None,
) -> list[list[F]]:
    space = RowSpace(len(representative))
    queue: deque[list[F]] = deque()
    if space.add(representative):
        queue.append(list(map(F, representative)))
    generators = adjacent_generators(n, distinguished)
    while queue:
        current = queue.popleft()
        for permutation in generators:
            image = act_vector(current, n, permutation)
            if space.add(image):
                queue.append(list(map(F, image)))
    return list(space.pivots.values())


def degree_two_matrix(vector_value: Sequence[int], n: int) -> list[list[int]]:
    index = {word: i for i, word in enumerate(words(n))}
    return [
        [vector_value[index[(i, j)]] for j in range(n)]
        for i in range(n)
    ]


def audit_exceptional_vector(
    representative: Vector,
    n: int,
    active_labels: Sequence[int],
    symmetric: bool,
    label: str,
) -> None:
    matrix = degree_two_matrix(representative, n)
    require(
        all(
            matrix[i][j] == (matrix[j][i] if symmetric else -matrix[j][i])
            for i in active_labels
            for j in active_labels
        ),
        f"{label}: exceptional representative has wrong transpose symmetry",
    )
    require(
        all(
            sum(matrix[i][j] for j in active_labels) == 0
            for i in active_labels
        ),
        f"{label}: exceptional representative has nonzero row sum",
    )
    inactive = set(range(n)) - set(active_labels)
    require(
        all(
            matrix[i][j] == 0
            for i in range(n)
            for j in range(n)
            if i in inactive or j in inactive
        ),
        f"{label}: exceptional representative uses an inactive label",
    )


def contraction_rows(
    n: int,
    distinguished: int | None,
    blocks: Sequence[Sequence[Vector]],
) -> list[list[int]]:
    basis = words(n)
    orbit_lookup = G_ORBITS if distinguished is not None else H_ORBITS
    rows: list[list[int]] = []
    for block in blocks:
        for i, left_vector in enumerate(block):
            for j in range(i, len(block)):
                right_vector = block[j]
                row = [0] * len(orbit_lookup)
                left_support = [
                    k for k, coefficient in enumerate(left_vector) if coefficient
                ]
                right_support = [
                    k for k, coefficient in enumerate(right_vector) if coefficient
                ]
                for left_index in left_support:
                    for right_index in right_support:
                        key = canonical_entry(
                            basis[left_index],
                            basis[right_index],
                            distinguished,
                        )
                        row[orbit_lookup[key]] += (
                            left_vector[left_index]
                            * right_vector[right_index]
                        )
                rows.append(row)
    return rows


def audit_decomposition(
    n: int,
    distinguished: int | None,
    blocks: Sequence[Sequence[Vector]],
    expected_block_sizes: Sequence[int],
    expected_orbit_rank: int,
    expected_span_dimensions: Sequence[int],
    label: str,
) -> None:
    require(
        [len(block) for block in blocks] == list(expected_block_sizes),
        f"{label}: block sizes {[len(block) for block in blocks]} "
        f"do not match {list(expected_block_sizes)}",
    )
    full_space = RowSpace(len(words(n)))
    for block_index, (block, expected_dimension) in enumerate(
        zip(blocks, expected_span_dimensions)
    ):
        for representative in block:
            span = orbit_span(representative, n, distinguished)
            require(
                len(span) == expected_dimension,
                f"{label}: block {block_index} representative orbit has "
                f"dimension {len(span)}, expected {expected_dimension}",
            )
            for row in span:
                full_space.add(row)
    require(
        full_space.rank == len(words(n)),
        f"{label}: symmetry-adapted orbit spans cover dimension "
        f"{full_space.rank}, expected {len(words(n))}",
    )
    rows = contraction_rows(n, distinguished, blocks)
    actual_rank = rank_fraction(rows)
    require(
        actual_rank == expected_orbit_rank,
        f"{label}: contraction-map rank {actual_rank}, "
        f"expected {expected_orbit_rank}",
    )


def audit_representation_completeness() -> None:
    h4 = vectors_h(4)
    require(
        len(h4) == 4,
        f"H/n=4: expected four isotypic blocks, got {len(h4)}",
    )
    audit_exceptional_vector(h4[2][0], 4, range(4), True, "H4/[2,2]")
    audit_exceptional_vector(h4[3][0], 4, range(4), False, "H4/[2,1,1]")
    audit_decomposition(
        4,
        None,
        h4,
        (4, 4, 1, 1),
        22,
        (1, 3, 2, 3),
        "H/n=4",
    )

    g4 = vectors_g4()
    audit_exceptional_vector(
        g4[2][0],
        4,
        range(1, 4),
        False,
        "G4/sign",
    )
    audit_decomposition(
        4,
        0,
        g4,
        (8, 6, 1),
        58,
        (1, 2, 1),
        "G/n=4",
    )

    h5 = vectors_h(5)
    require(
        len(h5) == 4,
        f"H/n=5: expected four isotypic blocks, got {len(h5)}",
    )
    audit_exceptional_vector(h5[2][0], 5, range(5), True, "H5/[3,2]")
    audit_exceptional_vector(h5[3][0], 5, range(5), False, "H5/[3,1,1]")
    audit_decomposition(
        5,
        None,
        h5,
        (4, 4, 1, 1),
        22,
        (1, 4, 5, 6),
        "H/n=5",
    )

    g5 = vectors_g(5)
    audit_exceptional_vector(
        g5[2][0],
        5,
        range(1, 5),
        True,
        "G5/[2,2]",
    )
    audit_exceptional_vector(
        g5[3][0],
        5,
        range(1, 5),
        False,
        "G5/[2,1,1]",
    )
    audit_decomposition(
        5,
        0,
        g5,
        (8, 6, 1, 1),
        59,
        (1, 3, 2, 3),
        "G/n=5",
    )
    print("REPRESENTATIONS: endpoint and stable vectors span every isotypic component; contraction ranks are 58, 59, and 22.")


def finite_differences(values: Sequence[int]) -> list[list[int]]:
    levels = [list(values)]
    while len(levels[-1]) > 1:
        levels.append(
            [
                levels[-1][i + 1] - levels[-1][i]
                for i in range(len(levels[-1]) - 1)
            ]
        )
    return levels


def audit_contraction_degrees() -> None:
    """Redundantly check the degree-four consequence of the counting lemma.

    The paper proves the load-bearing combinatorial statement: a contraction
    coefficient is a signed count of assignments of at most four free labels,
    hence a combination of falling factorials of degree at most four.  Here we
    independently evaluate eight stable sizes and require every exact fifth
    difference to vanish.
    """

    for label, distinguished, vector_builder in (
        ("G", 0, vectors_g),
        ("H", None, vectors_h),
    ):
        samples = [
            contraction_rows(n, distinguished, vector_builder(n))
            for n in range(5, 13)
        ]
        row_count = len(samples[0])
        column_count = len(samples[0][0])
        require(
            all(
                len(sample) == row_count
                and all(len(row) == column_count for row in sample)
                for sample in samples
            ),
            f"{label}: contraction schema changes across stable sizes",
        )
        for row in range(row_count):
            for column in range(column_count):
                values = [sample[row][column] for sample in samples]
                differences = finite_differences(values)
                require(
                    all(value == 0 for value in differences[5]),
                    f"{label}: contraction ({row},{column}) has nonzero "
                    f"fifth difference {differences[5]}",
                )
    print("COUNTING DEGREE: every contraction coefficient has zero exact fifth differences across eight stable sizes.")


def main() -> int:
    require(
        len(G_ORBITS) == 59 and len(H_ORBITS) == 22,
        f"stable orbit counts are G={len(G_ORBITS)}, H={len(H_ORBITS)}",
    )
    audit_orbit_classifier()
    audit_word_patterns()
    audit_representation_completeness()
    audit_contraction_degrees()
    audit_concrete_certificates()
    if ARGS.inject != "none":
        raise SemanticError(
            f"known-bad fixture {ARGS.inject!r} escaped all semantic checks"
        )
    print("SEMANTIC BRIDGE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
