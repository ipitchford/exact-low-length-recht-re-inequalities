#!/usr/bin/env python3
"""Replay De Sa's exact rational m=n=5 lower-bound counterexample.

The construction and closed form are from:
Christopher M. De Sa, "Random Reshuffling is Not Always Better,"
Advances in Neural Information Processing Systems 33 (2020).

The final checks give the exact noiseless-quadratic expected-iterate
corollary obtained by scaling the witness matrices by one half.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction as F
from typing import Iterable


Matrix = list[list[F]]


class VerificationError(RuntimeError):
    """Raised when an exact counterexample obligation fails."""


def require(condition: bool, context: str) -> None:
    if not condition:
        raise VerificationError(context)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inject-omit-rr-path",
        action="store_true",
        help="Known-bad fixture: omit one reshuffling path",
    )
    return parser.parse_args()


def identity(size: int) -> Matrix:
    return [[F(i == j) for j in range(size)] for i in range(size)]


def zero(size: int) -> Matrix:
    return [[F(0) for _ in range(size)] for _ in range(size)]


def matadd(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[i][j] + right[i][j] for j in range(len(left))]
        for i in range(len(left))
    ]


def matscale(value: F, matrix: Matrix) -> Matrix:
    return [[value * entry for entry in row] for row in matrix]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    size = len(left)
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(size)), F(0))
            for j in range(size)
        ]
        for i in range(size)
    ]


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix)]


def matvec(matrix: Matrix, vector: Iterable[F]) -> list[F]:
    values = list(vector)
    return [
        sum((entry * value for entry, value in zip(row, values)), F(0))
        for row in matrix
    ]


def outer(left: Iterable[F], right: Iterable[F]) -> Matrix:
    left_values = list(left)
    right_values = list(right)
    return [[a * b for b in right_values] for a in left_values]


def dot(left: Iterable[F], right: Iterable[F]) -> F:
    return sum((a * b for a, b in zip(left, right)), F(0))


def matrix_sum(matrices: Iterable[Matrix], size: int) -> Matrix:
    total = zero(size)
    for matrix in matrices:
        total = matadd(total, matrix)
    return total


def matrix_power(matrix: Matrix, exponent: int) -> Matrix:
    result = identity(len(matrix))
    factor = matrix
    while exponent:
        if exponent & 1:
            result = matmul(result, factor)
        factor = matmul(factor, factor)
        exponent //= 2
    return result


def expected_second_moment(
    updates: list[Matrix],
    sequences: Iterable[tuple[int, ...]],
) -> tuple[Matrix, int]:
    """Return E[P^T P] for P=C_{i_m}...C_{i_1}, exactly."""

    size = len(updates[0])
    total = zero(size)
    count = 0
    for sequence in sequences:
        product = identity(size)
        for index in sequence:
            product = matmul(updates[index], product)
        total = matadd(total, matmul(transpose(product), product))
        count += 1
    require(count > 0, "second-moment sequence family is empty")
    return matscale(F(1, count), total), count


def main() -> int:
    args = parse_args()
    n = 5
    one = [F(1) for _ in range(n)]
    matrices: list[Matrix] = []
    y_vectors: list[list[F]] = []

    for distinguished in range(n):
        y = [F(-1, 10) for _ in range(n)]
        y[distinguished] = F(2, 5)
        y_vectors.append(y)
        matrix = matadd(
            identity(n),
            matadd(outer(one, y), outer(y, one)),
        )
        matrices.append(matrix)

        require(dot(one, y) == 0, f"A_{distinguished + 1}: 1^T y != 0")
        require(dot(y, y) == F(1, 5), f"A_{distinguished + 1}: y^T y != 1/5")
        positive_vector = [one[i] + 5 * y[i] for i in range(n)]
        kernel_vector = [one[i] - 5 * y[i] for i in range(n)]
        require(
            matvec(matrix, positive_vector)
            == [2 * value for value in positive_vector],
            f"A_{distinguished + 1}: eigenvalue-2 vector failed",
        )
        require(
            matvec(matrix, kernel_vector) == [F(0) for _ in range(n)],
            f"A_{distinguished + 1}: kernel vector failed",
        )
        positive_projection = matscale(
            F(1, 10),
            outer(positive_vector, positive_vector),
        )
        kernel_projection = matscale(
            F(1, 10),
            outer(kernel_vector, kernel_vector),
        )
        complement_projection = matadd(
            identity(n),
            matscale(
                F(-1),
                matadd(positive_projection, kernel_projection),
            ),
        )
        projections = (
            positive_projection,
            kernel_projection,
            complement_projection,
        )
        for projection_index, projection in enumerate(projections):
            require(
                matmul(projection, projection) == projection,
                f"A_{distinguished + 1}: projector {projection_index} "
                "is not idempotent",
            )
        for left_index in range(len(projections)):
            for right_index in range(left_index + 1, len(projections)):
                require(
                    matmul(projections[left_index], projections[right_index])
                    == zero(n),
                    f"A_{distinguished + 1}: projectors "
                    f"{left_index},{right_index} are not orthogonal",
                )
        spectral_reconstruction = matadd(
            matscale(F(2), positive_projection),
            complement_projection,
        )
        require(
            matrix == spectral_reconstruction,
            f"A_{distinguished + 1}: exact PSD spectral decomposition failed",
        )
        require(
            all(
                matrix[i][j] == matrix[j][i]
                for i in range(n)
                for j in range(n)
            ),
            f"A_{distinguished + 1}: matrix is not symmetric",
        )

    # The exact orthogonal-projector reconstruction certifies eigenvalues
    # 2, 0, 1 and therefore positive semidefiniteness without numerics.
    mean = matscale(F(1, n), matrix_sum(matrices, n))
    require(mean == identity(n), "arithmetic mean is not I")

    product_sum = zero(n)
    for permutation in itertools.permutations(range(n)):
        product = identity(n)
        for index in permutation:
            product = matmul(product, matrices[index])
        product_sum = matadd(product_sum, product)

    falling = 120
    random_reshuffle_mean = matscale(F(1, falling), product_sum)
    projection_one = matscale(F(1, n), outer(one, one))
    projection_perp = matadd(identity(n), matscale(F(-1), projection_one))
    expected = matadd(
        matscale(F(29, 64), projection_perp),
        matscale(F(-19, 16), projection_one),
    )
    require(
        random_reshuffle_mean == expected,
        "symmetrized product does not match De Sa's exact closed form",
    )

    lower_eigenvalue = F(-19, 16)
    require(
        matvec(random_reshuffle_mean, one)
        == [lower_eigenvalue for _ in range(n)],
        "all-ones lower eigenpair failed",
    )
    e_lower_eigenvalue = falling * lower_eigenvalue
    require(
        e_lower_eigenvalue == F(-285, 2),
        f"unexpected E_{{5,5}} eigenvalue {e_lower_eigenvalue}",
    )
    require(
        e_lower_eigenvalue < -falling,
        "counterexample does not violate E_{5,5} >= -120 I",
    )

    # Exact optimization translation.  Put C_i=A_i/2 and H_i=I-C_i.
    # The unit-step gradient update for f_i(x)=x^T H_i x/2 is x <- C_i x.
    updates = [matscale(F(1, 2), matrix) for matrix in matrices]
    hessians = [
        matadd(identity(n), matscale(F(-1), update))
        for update in updates
    ]
    for distinguished, (update, hessian, y) in enumerate(
        zip(updates, hessians, y_vectors)
    ):
        positive_vector = [one[i] + 5 * y[i] for i in range(n)]
        kernel_vector = [one[i] - 5 * y[i] for i in range(n)]
        positive_projection = matscale(
            F(1, 10),
            outer(positive_vector, positive_vector),
        )
        kernel_projection = matscale(
            F(1, 10),
            outer(kernel_vector, kernel_vector),
        )
        complement_projection = matadd(
            identity(n),
            matscale(
                F(-1),
                matadd(positive_projection, kernel_projection),
            ),
        )
        require(
            update
            == matadd(
                positive_projection,
                matscale(F(1, 2), complement_projection),
            ),
            f"C_{distinguished + 1}: contraction spectrum reconstruction failed",
        )
        require(
            hessian
            == matadd(
                kernel_projection,
                matscale(F(1, 2), complement_projection),
            ),
            f"H_{distinguished + 1}: PSD spectrum reconstruction failed",
        )

    mean_update = matscale(F(1, n), matrix_sum(updates, n))
    require(
        mean_update == matscale(F(1, 2), identity(n)),
        "mean contraction is not I/2",
    )
    reshuffling_operator = matscale(
        F(1, 2**5),
        random_reshuffle_mean,
    )
    expected_reshuffling_operator = matadd(
        matscale(F(29, 2048), projection_perp),
        matscale(F(-19, 512), projection_one),
    )
    require(
        reshuffling_operator == expected_reshuffling_operator,
        "scaled reshuffling operator has the wrong exact projector form",
    )
    with_replacement_operator = matrix_power(mean_update, 5)
    require(
        with_replacement_operator == matscale(F(1, 32), identity(n)),
        "with-replacement expected operator is not I/32",
    )
    reshuffling_norm = F(19, 512)
    with_replacement_norm = F(1, 32)
    require(
        reshuffling_norm > with_replacement_norm,
        "scaled witness does not separate expected-iterate operator norms",
    )
    require(
        matvec(reshuffling_operator, one)
        == [F(-19, 512) for _ in range(n)],
        "scaled all-ones reshuffling eigenpair failed",
    )

    # The first-moment ordering above reverses at the mean-square level.
    # Enumerate every permutation and every length-five iid sequence.
    rr_sequences = list(itertools.permutations(range(n)))
    if args.inject_omit_rr_path:
        rr_sequences.pop()
    rr_second_moment, rr_paths = expected_second_moment(
        updates,
        rr_sequences,
    )
    wr_second_moment, wr_paths = expected_second_moment(
        updates,
        itertools.product(range(n), repeat=n),
    )
    require(rr_paths == 120, f"expected 120 RR paths, got {rr_paths}")
    require(wr_paths == 3125, f"expected 3125 WR paths, got {wr_paths}")

    expected_rr_second_moment = matadd(
        matscale(F(1435, 1048576), projection_perp),
        matscale(F(421, 131072), projection_one),
    )
    expected_wr_second_moment = matadd(
        matscale(F(365, 65536), projection_perp),
        matscale(F(91, 8192), projection_one),
    )
    require(
        rr_second_moment == expected_rr_second_moment,
        "random-reshuffling second moment has the wrong projector form",
    )
    require(
        wr_second_moment == expected_wr_second_moment,
        "with-replacement second moment has the wrong projector form",
    )
    perpendicular_gap = F(4405, 1048576)
    all_ones_gap = F(1035, 131072)
    require(
        perpendicular_gap > 0 and all_ones_gap > 0,
        "second-moment projector gaps are not strictly positive",
    )
    require(
        matadd(
            wr_second_moment,
            matscale(F(-1), rr_second_moment),
        )
        == matadd(
            matscale(perpendicular_gap, projection_perp),
            matscale(all_ones_gap, projection_one),
        ),
        "second-moment Loewner gap has the wrong projector form",
    )

    print("DE SA n=5 MATRICES: 5 exact rational PSD matrices verified.")
    print("NORMALIZATION: arithmetic mean equals I exactly.")
    print(
        "SYMMETRIZED PRODUCT: "
        "29/64*(I-J/5) - 19/16*(J/5) verified over 120 permutations."
    )
    print("LOWER FAILURE: E_{5,5} has eigenvalue -285/2 < -120.")
    print("QUADRATIC UPDATES: C_i=A_i/2 and H_i=I-C_i are PSD contractions/Hessians.")
    print("EXPECTED ITERATE: random reshuffling norm 19/512 > with-replacement norm 1/32.")
    print(
        "SECOND MOMENT: RR = 1435/1048576*P_perp + "
        "421/131072*P_1 over 120 paths."
    )
    print(
        "SECOND MOMENT: WR = 365/65536*P_perp + "
        "91/8192*P_1 over 3125 paths."
    )
    print(
        "METRIC SEPARATION: E_WR[P^T P] - E_RR[P^T P] "
        "= 4405/1048576*P_perp + 1035/131072*P_1 is positive definite."
    )
    print("M5 SHARPNESS COUNTEREXAMPLE: VERIFIED EXACTLY.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
