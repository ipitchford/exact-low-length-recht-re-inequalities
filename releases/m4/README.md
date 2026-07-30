# Recht–Ré at product length four — exact all-`n` proof, version 1.1

This release proves the product-length-four conjecture left open by Lai and Lim.

For every integer `n >= 4`, let `A_1,...,A_n` be positive semidefinite Hermitian matrices of arbitrary common dimension with `sum_i A_i <= nI`. Then

```text
-(n)_4 I <= sum_{i,j,k,l all distinct} A_i A_j A_k A_l <= (n)_4 I,
```

where `(n)_4 = n(n-1)(n-2)(n-3)` and the sum is over ordered distinct four-tuples.

## Exact replay

```bash
python3 verifiers/verify_all_n_stdlib.py
python3 verifiers/verify_all_n_sympy.py
python3 src/derive_parametric_family.py
```

or:

```bash
./verify.sh
```

The primary verifier uses only Python's standard library. No acceptance test uses floating-point arithmetic or a numerical tolerance.

## What version 1.1 adds

- exact affine-rank checks proving that the 23 upper and 30 lower free coordinates are genuine transversals;
- the Peyrl–Parrilo citation for numerical-to-rational seed recovery;
- corrected DOI records for Helton–Klep–McCullough and Zhang;
- a precise statement of Anthropic Fable 5's independent audit scope;
- a claim–evidence matrix, audit handoff, clean replay receipt, and citation metadata.

## What is checked

The two exact proof-replay implementations reconstruct and verify:

1. all 152 rational-function coefficient identities;
2. the 59 stabilizer and 22 full-symmetry orbit conventions;
3. the exact affine ranks and the 23 upper / 30 lower seed transversals;
4. representation blocks of sizes `8,6,1,1` and `4,4,1,1`;
5. all 51 leading-principal-minor polynomials and all 775 strictly positive coefficients after shifting by `n-5`;
6. the exact upper kernel `(n^2,n,n,1,1,1,1,1)` in scaled coordinates;
7. separate exact rational upper and lower certificates at `n=4`; and
8. recovery of all 162 rational orbit functions from the exact `n=5` seeds by balanced five-block continuation.

## Main files

- `../../paper/exact_low_length_recht_re.pdf`: unified anonymous proof paper.
- `FREE_FUNCTIONS.md`: the 23 upper and 30 lower rational functions.
- `certificates/parametric_orbit_functions.json`: all 162 orbit functions.
- `certificates/base5_seed_certificates.json`: exact five-variable seeds.
- `certificates/scaled_block_matrices.json`: exact scaled representation blocks.
- `certificates/principal_minors.json`: all 51 determinant polynomials.
- `certificates/n4_orbit_certificates.json`: separate endpoint certificates.
- `CLAIM_EVIDENCE_MATRIX.md`: load-bearing claim map.
- `AUDIT_HANDOFF.md`: third-party audit instructions.
- `REPLAY_RECEIPT_2026-07-30.md`: clean exact replay.

## Evidence and attribution boundary

The free Positivstellensatz/SDP framework is due to Lai and Lim; symmetry reduction follows Gatermann–Parrilo; numerical-to-rational recovery follows Peyrl–Parrilo; and balanced-block lifting at integer multiples is Teng Zhang's Lemma 3.1. The new contribution claimed here is the explicit rational continuation, its uniform exact positivity proof, and the separate exact endpoint certificate at `n=4`.

Anthropic Fable 5 independently reconstructed the printed family and exact identity/positivity checks at `n=6,9,11,13` using a separate orbit system. It did not replay the 51 uniform minor polynomials. The bundled implementations close that executable gap but share the released proof architecture and are not external peer review.

The historical numerical SDP discovery workspace was not preserved completely.
This release reproduces the exact certificate proof, not the discovery search.

Targeted searches through 30 July 2026 found no prior all-`n` resolution; search absence is not proof of priority.

Human research direction is anonymous in this package. OpenAI GPT-5.6 Sol
contributed mathematical construction, exact certificate code, and drafting;
Anthropic Fable contributed the bounded fixed-case audit and route
identification described above. AI systems are tools, not authors.
