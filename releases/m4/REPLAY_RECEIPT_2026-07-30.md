# Exact replay receipt — version 1.1, 30 July 2026

Environment: Python 3.13.5; SymPy 1.14.0; Linux 6.12.13 x86_64, glibc 2.41.

## Dependency-free verifier

```text
IDENTITIES: 152 rational-function equations verified exactly.
BLOCK COUNTS: degree<=4 interpolation and independent n=10 replay passed.
SEED TRANSVERSALS: 23 upper and 30 lower free coordinates reconstruct the exact affine certificates uniquely.
POSITIVITY n>=5: block construction, 51 exact determinants, positive coefficients, and kernel passed.
n=4: exact identities and all rational Sylvester tests passed.
VERIFIED (stdlib): Recht--Re m=4 holds for every integer n>=4.
```

Resource record: `elapsed=6.58 s`, `max_rss=151400 KB`, `exit=0`.

## SymPy verifier

```text
IDENTITIES: 76 upper and 76 lower orbit equations verified exactly.
BLOCK COEFFICIENTS: exact degree<=4 interpolation and independent n=10 check passed.
SEED TRANSVERSALS: 23 upper and 30 lower free coordinates reconstruct the exact affine certificates uniquely.
POSITIVITY n>=5: 51 determinant polynomials and the upper kernel verified exactly.
n=4: both exact identities and all representation-block positivity tests passed.
VERIFIED: Recht--Re m=4 holds for every integer n>=4.
```

Resource record: `elapsed=1.64 s`, `max_rss=114160 KB`, `exit=0`.

## Seed-to-family derivation

```text
upper: all 81 orbit functions re-derived exactly from balanced five-block averaging.
lower: all 81 orbit functions re-derived exactly from balanced five-block averaging.
DERIVATION VERIFIED.
```

Resource record: `elapsed=7.87 s`, `max_rss=158164 KB`, `exit=0`.

No load-bearing acceptance test uses floating-point arithmetic.
