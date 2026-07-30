# Exact replay receipt — 30 July 2026

## Environment

```text
Python 3.13.5
SymPy 1.14.0
Linux 6.12.13 x86_64, glibc 2.41
```

## Primary dependency-free verifier

Command:

```bash
python3 verifiers/verify_m5_restoration_stdlib.py
```

Output:

```text
IDENTITIES: 152 rational-function equations verified exactly.
BLOCK COUNTS: degree<=4 interpolation and independent n=11 replay passed.
SEED TRANSVERSALS: 23 upper and 30 lower free coordinates reconstruct the exact affine certificates uniquely.
POSITIVITY n>=6: block construction, 51 exact determinants, positive coefficients, and kernel passed.
n=5 UPPER ENDPOINT: exact identity, kernel, and rational Sylvester tests passed.
SEED: parametric family specializes exactly to both n=6 certificates.
VERIFIED (stdlib): Recht--Re m=5 upper bound holds for n>=5 and both bounds hold for n>=6.
```

Resource record:

```text
elapsed=6.74 s
max_rss=153072 KB
exit=0
```

## Independent SymPy verifier

Command:

```bash
python3 verifiers/verify_m5_restoration_sympy.py
```

Output:

```text
IDENTITIES: 76 upper and 76 lower orbit equations verified exactly.
BLOCK COEFFICIENTS: exact degree<=4 interpolation and independent n=11 check passed.
SEED TRANSVERSALS: 23 upper and 30 lower free coordinates reconstruct the exact affine certificates uniquely.
POSITIVITY n>=6: 51 determinant polynomials and the upper kernel verified exactly.
n=5 UPPER ENDPOINT: exact identity, kernel, and rational Sylvester tests passed.
SEED: parametric family specializes exactly to both n=6 certificates.
VERIFIED: Recht--Re m=5 upper bound holds for n>=5 and both bounds hold for n>=6.
```

Resource record:

```text
elapsed=1.91 s
max_rss=114452 KB
exit=0
```

## Seed-to-family derivation

Command:

```bash
python3 src/derive_parametric_family.py
```

Output:

```text
upper: all 81 orbit functions re-derived exactly from balanced six-block averaging.
lower: all 81 orbit functions re-derived exactly from balanced six-block averaging.
DERIVATION VERIFIED.
```

Resource record:

```text
elapsed=6.94 s
max_rss=161180 KB
exit=0
```

All load-bearing arithmetic is exact. No floating-point tolerance enters acceptance.
