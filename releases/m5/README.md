# Recht–Ré at product length five: exact restoration beyond the counterexample

This release proves, by exact rational free sum-of-squares certificates, the following theorem.

Let `A_1,...,A_n` be positive semidefinite Hermitian matrices of arbitrary common dimension and assume `sum_i A_i <= n I` in Loewner order. Write

`E_{5,n}(A) = sum A_{i1} A_{i2} A_{i3} A_{i4} A_{i5}`

over all ordered five-tuples of distinct indices. Then

- `E_{5,n}(A) <= (n)_5 I` for every integer `n >= 5`;
- `-(n)_5 I <= E_{5,n}(A)` for every integer `n >= 6`.

Therefore the two-sided Recht–Ré norm inequality holds for `m=5` for every integer `n >= 6`. De Sa's explicit rational lower-bound counterexample at `(m,n)=(5,5)` is replayed exactly in `counterexamples/verify_n5_lower_counterexample.py`, making the threshold sharp. Lai and Lim independently reported a numerical lower-SDP optimum of `144.6488` and approximate Farkas evidence against feasibility at `120`; that historical SDP computation is not replayed here. Their surviving upper-half conjecture is proved here for the entire five-factor row.

## Exact replay

The primary verifier uses only Python's standard library:

```bash
python3 verifiers/verify_m5_restoration_stdlib.py
```

The second exact implementation uses SymPy:

```bash
python3 verifiers/verify_m5_restoration_sympy.py
```

The derivation cross-check starts from the exact six-variable seeds and recovers every published rational orbit function:

```bash
python3 src/derive_parametric_family.py
```

Run both implementations, the derivation cross-check, and the exact sharpness
counterexample with:

```bash
./verify.sh
```

No acceptance test uses floating-point arithmetic or a numerical tolerance.

## What is checked

The exact replay reconstructs and verifies:

1. all 152 rational-function coefficient equations for the upper and lower free-polynomial identities;
2. the 59 stabilizer orbits, 22 full-symmetry orbits, and 76 canonical word patterns;
3. the exact affine ranks and the 23 upper / 30 lower seed transversals;
4. the `8,6,1,1` and `4,4,1,1` representation blocks;
5. all 51 required determinant polynomials, including all 929 strictly positive coefficients after shifting by `n-6`;
6. the one-dimensional equality kernel of the upper `G` trivial block;
7. the separate exact upper certificate at `n=5`;
8. exact specialization of the parametric family back to both `n=6` seeds; and
9. exact recovery of all 162 orbit functions by balanced six-block continuation; and
10. De Sa's rational `n=5` lower counterexample by exact enumeration of all
    `120` permutations.

## Files

- `../../paper/exact_low_length_recht_re.pdf`: unified anonymous proof paper.
- `FREE_SEED_VALUES.md`: human-readable seed transversals.
- `certificates/base6_seed_certificates.json`: exact upper and lower seeds at `n=6`.
- `certificates/n5_upper_certificate.json`: exact upper endpoint at `n=5`.
- `certificates/parametric_orbit_functions.json`: all rational functions of `n`.
- `certificates/scaled_block_matrices.json`: exact scaled representation blocks.
- `certificates/principal_minors.json`: the 51 determinant polynomials.
- `verifiers/verify_m5_restoration_stdlib.py`: dependency-free exact checker.
- `verifiers/verify_m5_restoration_sympy.py`: second exact checker, implemented with SymPy.
- `src/derive_parametric_family.py`: exact seed-to-family derivation cross-check.
- `counterexamples/verify_n5_lower_counterexample.py`: exact sharpness replay.
- `CLAIM_EVIDENCE_MATRIX.md`: claim-to-artifact audit map.
- `AUDIT_HANDOFF.md`: concise third-party audit instructions.
- `REPLAY_RECEIPT_2026-07-30.md`: recorded clean replay.

## Evidence and attribution boundary

The proof is exact and executable but has not yet undergone journal peer review. The free Positivstellensatz/SDP framework is due to Lai and Lim; symmetry reduction follows Gatermann–Parrilo; numerical-to-rational recovery follows Peyrl–Parrilo; and validity at integer multiples follows Zhang's Lemma 3.1. The new mathematical content claimed here is the exact five-factor seed and endpoint certificates, their rational six-block continuation, and the uniform positivity proof.

The two verifiers are exact implementations with different arithmetic engines, but they share the certificate schema, orbit conventions, representation vectors, and proof architecture. Their agreement is redundant implementation evidence, not an independent third-party audit. The derivation program is a seed-to-family cross-check, not a third proof. This release reproduces exact proof-certificate replay from the stated seeds; it does not reproduce the original numerical SDP search or rational-seed discovery process described in `DISCOVERY_NOTES.md`.

Anthropic Fable 5 independently audited the companion `m=4` work and motivated treating this five-factor theorem as a separate Part II. It has not audited this `m=5` release. Targeted literature searches through 30 July 2026 found no prior five-factor restoration theorem; search absence is not proof of priority.

Human research direction is anonymous in this package. OpenAI GPT-5.6 Sol
contributed proof construction, exact certificate code, and drafting. AI
systems are tools, not authors.
