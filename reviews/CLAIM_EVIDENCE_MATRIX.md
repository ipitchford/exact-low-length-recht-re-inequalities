# Unified claim--evidence matrix

| Claim | Paper argument | Exact executable evidence | Boundary |
|---|---|---|---|
| \(m=4\) two-sided bound for every \(n\ge4\) | Main theorem; stable family; endpoint | m4 certificate JSON, two arithmetic verifiers, derivation, semantic checker | Candidate computer-assisted theorem |
| \(m=5\) upper for every \(n\ge5\) | Stable upper family and \(n=5\) endpoint | m5 certificate JSON and three replay paths | Candidate computer-assisted theorem |
| \(m=5\) lower for every \(n\ge6\) | Stable lower family | Same | Sharpness requires next row |
| Exact lower failure at \(m=n=5\) | De Sa projector evaluation | Five rational PSD matrices; all 120 products; eigenvalue \(-285/2\) | Internally replayed published witness |
| \(m=6\) upper when \(7\mid n\) | Upper identity, seed PSD, balanced lifting | 1,156 identities; exact \(G_7,H_7\) characteristic polynomials | No nonmultiple or sharpness claim |
| \(m=6\) lower when \(8\mid n\) | Lower identity, seed PSD, balanced lifting | 1,156 identities; exact \(G_8,H_8\) characteristic polynomials | Same |
| \(m=6\) two-sided norm when \(56\mid n\) | Intersection plus normalization | Both six-factor seed releases | No threshold claim |
| One-epoch bias--mean-square reversal | Projector/transfer/subset derivation | 120 RR and 3,125 WR exact paths; four rational coefficients | One witness; not universal/asymptotic |
| Certificate semantics for \(m=4,5\) | Orbit, representation, degree lemmas | Structurally separate semantic checker and four mutations | Reduces, not eliminates, shared-schema risk |
| Every released file is bound | Reproducibility section | Bidirectional release and package SHA-256 manifests | Authentication is not mathematical truth |
| Verifiers fail closed under optimization | Integrity report | Static AST scan and normal/`-O` mutations | Guards a known implementation failure mode |
| Literature context | Background and bibliography | Primary-source citation audit | Search absence is not priority proof |

## Assurance ladder

This repository establishes deterministic exact replay of a specified
computer-assisted proof package. It does not by itself establish formal
verification, independent external reproduction, expert acceptance,
publication priority, or journal peer review.
