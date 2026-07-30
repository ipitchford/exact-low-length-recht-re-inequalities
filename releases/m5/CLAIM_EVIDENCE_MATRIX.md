# Claim–evidence matrix

| Claim | Human argument | Machine evidence | Acceptance condition |
|---|---|---|---|
| Upper identity for every integer `n >= 6` | Paper, Proposition 2.1 and Sections 3–4 | `parametric_orbit_functions.json`; both exact implementations | All 76 canonical coefficient equations vanish identically as rational functions of the parameter `n`, then specialize at each integer `n >= 6` |
| Lower identity for every integer `n >= 6` | Paper, Proposition 2.1 and Sections 3–4 | Same | All 76 canonical coefficient equations vanish identically as rational functions of the parameter `n`, then specialize at each integer `n >= 6` |
| Exact six-variable upper and lower seeds | Paper, Sections 3–4 and Appendix A | `base6_seed_certificates.json`; transversal checks | The fixed free coordinates reconstruct unique exact affine solutions and specialize from the parametric family |
| Upper endpoint at `n=5` | Paper, Section 6 | `n5_upper_certificate.json`; both verifiers | Exact word identity, exact kernel, and rational Sylvester tests |
| Symmetry orbit counts `59+22` | Paper, Sections 3 and 5 | Both verifiers reconstruct canonical orbit maps | Counts equal 59 and 22 by direct reconstruction without reading stored orbit maps |
| Representation block sizes | Paper, Section 5 | Both verifiers construct explicit test vectors and orbit contractions | `G: 8,6,1,1`; `H: 4,4,1,1` |
| Uniform positive semidefiniteness for every integer `n >= 6` | Paper, Section 5 | `scaled_block_matrices.json`, `principal_minors.json`; both exact implementations | The algebraic multiplicity-block families are positive on the real parameter range `n >= 6`: 51 exact leading-minor polynomials have strictly positive coefficients in `t=n-6`, and the upper singular block has the stated exact kernel and a positive `7x7` leading block. Integer specializations give the Gram matrices used by the theorem |
| 929 positive coefficients | Paper, Section 5 | Both verifiers recompute determinants rather than trusting the stored list | 438 upper plus 491 lower coefficients, each strictly positive rational |
| Balanced six-block origin of the family | Paper, Section 4 | `src/derive_parametric_family.py` | All 81 upper and 81 lower published orbit functions are recovered exactly from the two seeds |
| Two-sided Recht–Ré inequality for `m=5` and every integer `n>=6` | Paper, Theorem 1.2 | Follows from exact identities plus Gram positivity | Every localizer evaluates positive semidefinite under `A_i >= 0` and `nI-sum A_i >= 0` |
| Sharpness of threshold | Paper, Section 1 | External: [Lai and Lim (2020), Section 4](https://proceedings.mlr.press/v119/lai20a.html), which reports numerical optimum `144.6488` and approximate Farkas evidence against feasibility at `120` | The published lower-bound failure at `n=5` is combined with this release's exact two-sided proof for every integer `n>=6`; the external computation is not replayed here |

The load-bearing theorem does not depend on the numerical SDP used to discover the rational seed. Numerical data are absent from every acceptance path.

“Both exact implementations” means redundant exact checking with different arithmetic engines. They share the certificate schema, orbit conventions, representation vectors, and overall proof architecture; this is not an independent third-party audit. `src/derive_parametric_family.py` is a seed-to-family derivation cross-check, not a third proof. The release reproduces certificate verification from the exact seeds, not the original numerical SDP discovery process.
