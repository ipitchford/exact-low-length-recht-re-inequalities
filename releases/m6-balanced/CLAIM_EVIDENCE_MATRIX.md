# Six-factor balanced-family claim--evidence matrix

| Claim | Human-readable argument | Exact executable evidence | Boundary |
|---|---|---|---|
| Upper bound for \(7\mid n\) | Unified paper: identity, seed PSD, balanced lifting | Upper JSON; 1,156 upper identities; exact \(G_7,H_7\) characteristic polynomials | Candidate computer-assisted theorem; no nonmultiple claim |
| Lower bound for \(8\mid n\) | Same, using lower seed | Lower JSON; 1,156 lower identities; exact \(G_8,H_8\) characteristic polynomials | Candidate computer-assisted theorem; no nonmultiple claim |
| Two-sided norm bound for \(56\mid n\) | Intersection of the two arithmetic families plus normalization | Both exact seed certificates and balanced transport | Does not imply a sharp threshold |
| Upper \(G_7\) is PSD of corank one | Characteristic-polynomial criterion | Exact rank 399, coefficient signs, and all-ones kernel for the \(400\times400\) integer Gram matrix | Kernel meaning is checked at the seed |
| Other seed Gram matrices are positive definite | Same | Exact full rank and strictly positive \(\det(tI+A)\) coefficients | Seed sizes only before balanced lifting |
| Parametric identities hold at stable pole-free integers | Rational identity theorem | Reconstructed orbit maps and all 2,312 coefficient equations | Identity continuation does not carry positivity |
| Endpoint failure or sharpness | None | Quarantined, unverified dual-looking pickles only | **Not claimed** |

The release replays a particular exact certificate package. Its two programs
share the same canonical orbit encoder and are not fully independent
implementations. The independent audit in
`../../reviews/peer_review/m6_balanced_audit.md` checked the mathematical
signs, scaling, FLINT convention, kernel, and balanced inference but is not
journal peer review.
