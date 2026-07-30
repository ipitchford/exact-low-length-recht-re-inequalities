# Independent audit handoff

## Target theorem

For positive semidefinite Hermitian matrices with `sum_i A_i <= nI`, the ordered distinct five-product sum satisfies the upper Loewner bound for every integer `n>=5` and the lower Loewner bound for every integer `n>=6`.

## Fastest decisive audit

From the release root:

```bash
sha256sum -c MANIFEST.sha256
python3 verifiers/verify_m5_restoration_stdlib.py
python3 verifiers/verify_m5_restoration_sympy.py
python3 src/derive_parametric_family.py
```

The primary verifier has no third-party dependency. The SymPy program is a second exact implementation, and the derivation program is a seed-to-family cross-check. Expected final lines are recorded in `REPLAY_RECEIPT_2026-07-30.md`.

## Adversarial checks worth repeating independently

1. Rebuild the 59 and 22 orbit maps from canonical equality patterns rather than importing them.
2. Reconstruct the 76 coefficient equations by direct noncommutative word expansion.
3. Pin the 23 upper and 30 lower free seed coordinates and prove that the complementary columns have full rank.
4. At several nonmultiples of six, reconstruct the full orbit solution and check the formal identity and exact block positivity.
5. Independently derive the representation decomposition
   `W_n = 4[n] + 4[n-1,1] + [n-2,2] + [n-2,1,1]`
   and its restriction to `S_{n-1}`.
6. Recompute the 51 leading determinants from the rational functions and verify strict positivity of every coefficient after the shift `t=n-6`.
7. Check the upper singular block by congruence, not by determinant alone.
8. Verify the separate `n=5` upper endpoint and compare it with Lai and Lim's published lower obstruction. Their Section 4 reports a numerical lower-SDP optimum of `144.6488` and approximate Farkas evidence against feasibility at `120`; see [Lai and Lim (2020)](https://proceedings.mlr.press/v119/lai20a.html).

## Evidence boundary

No independent third-party audit of this five-factor release is claimed. The two exact verifier implementations share the certificate schema, orbit conventions, representation vectors, and proof architecture; the derivation program is a cross-check rather than a third proof. The release replays exact proof certificates from the stated seeds but does not reproduce the original numerical SDP discovery process. Anthropic Fable 5 audited the companion four-factor result only. Literature priority is provisional pending systematic expert review.
