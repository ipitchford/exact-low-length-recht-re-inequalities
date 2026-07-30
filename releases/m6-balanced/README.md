# Six-factor balanced-family exact release

This module supports the six-factor clauses of the anonymous unified paper:

- the upper Recht--Ré Loewner bound whenever \(7\mid n\);
- the lower bound whenever \(8\mid n\); and
- the two-sided norm inequality whenever \(56\mid n\).

It does **not** prove either sign at intervening dimensions, a sharp
six-factor threshold, or any endpoint counterexample.

## Exact proof layers

`check_parametric_identities.py` reconstructs 797 point-stabilizer Gram
orbits, 211 fully symmetric Gram orbits, and all 1,156 free-word equality
patterns. It verifies 1,156 rational identities for each sign.

`certify_base_psd_flint.py` specializes the rational Gram entries at the
upper seed \(n=7\) and lower seed \(n=8\), clears one positive common
denominator per seed, constructs the full integer Gram matrices, and computes
their exact ranks and characteristic polynomials with FLINT. For a real
symmetric matrix \(A\), nonnegative coefficients of
\(\det(tI+A)\) are equivalent to \(A\succeq0\).

The balanced-coloring theorem in the paper transports those exact seed
certificates by congruence averaging to multiples of 7 and 8. Rational
continuation alone is not used to infer positivity.

## Individual replay

From the package root, after installing `environment/requirements-lock.txt`:

```bash
.venv/bin/python releases/m6-balanced/check_parametric_identities.py
.venv/bin/python releases/m6-balanced/certify_base_psd_flint.py
```

The second command computes characteristic polynomials of matrices as large
as \(585\times585\) and can take several minutes.

The two JSON files retain their recovered exact values:

```text
upper f0db80568847c91ef075fa49640205d07d96c96b22f3b706cd0db62066cabb6c
lower a24bf15495988840bb3cd30bcde4a1de5528a1d6633f32295c2deb9d50a9a186
```

See `BASE_PSD_RECEIPT.md`, `CLAIM_EVIDENCE_MATRIX.md`, and
`MANIFEST.sha256` for the exact evidence boundary.
