# Independent audit handoff

## Decisive replay

```bash
sha256sum -c MANIFEST.sha256
python3 verifiers/verify_all_n_stdlib.py
python3 verifiers/verify_all_n_sympy.py
python3 src/derive_parametric_family.py
```

## Adversarial checks

1. Rebuild the 59 and 22 equality-pattern orbit maps.
2. Reconstruct all 76 word-pattern equations for each sign by direct free-word expansion.
3. Pin the 23/30 seed coordinates and verify full complementary rank.
4. Recompute the representation blocks independently from the decomposition of the length-at-most-two word space.
5. Recompute all 51 leading determinants and their coefficients after the shift `t=n-5`.
6. Treat the singular upper block by the explicit kernel/congruence argument, not by a zero determinant.
7. Replay the separate `n=4` endpoint without assuming stable representation types.
8. Compare exact instances at several residue classes not covered directly by five-block lifting.

The paper and bundle distinguish exact theorem verification from provisional literature priority.
