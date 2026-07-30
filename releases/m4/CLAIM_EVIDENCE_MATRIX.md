# Claim–evidence matrix

| Claim | Human argument | Machine evidence | Acceptance condition |
|---|---|---|---|
| Upper and lower free-polynomial identities for every `n>=5` | Paper, Proposition 2.1 and Sections 3–4 | `parametric_orbit_functions.json`; both exact implementations | All 152 rational-function equations vanish identically |
| Exact `n=5` seeds | Paper, Sections 3–4 | `base5_seed_certificates.json` | The 23/30 pinned coordinates reconstruct unique affine solutions and specialize from the family |
| Orbit counts `59+22` | Paper, Sections 3 and 5 | Both implementations rebuild equality-pattern orbits | Counts match the direct constructions rather than a stored orbit map |
| Representation block sizes | Paper, Section 5 | Explicit representation test vectors in both verifiers | `G: 8,6,1,1`; `H: 4,4,1,1` |
| Uniform Gram positivity for all `n>=5` | Paper, Section 5 | `scaled_block_matrices.json`, `principal_minors.json`; both implementations | 51 determinant polynomials have 775 strictly positive coefficients in `t=n-5`; singular upper block has stated kernel and positive `7x7` leading block |
| Separate endpoint `n=4` | Paper, Section 6 | `n4_orbit_certificates.json` | Exact identities and rational Sylvester tests for every representation block |
| Seed-to-family derivation | Paper, Section 4 | `src/derive_parametric_family.py` | All 81 upper and 81 lower functions recovered exactly |
| Full `m=4` Recht–Ré theorem | Paper, Theorem 1.2 | Consequence of exact identities and Gram positivity | Every localizer evaluates positive semidefinite for PSD inputs and slack |

External audit scope: Anthropic Fable 5 independently checked exact instances `n=6,9,11,13`; it did not replay the uniform determinant inventory.
