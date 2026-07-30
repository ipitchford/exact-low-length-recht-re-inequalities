# Peer Review Report

## Manuscript Information

- **Title**: Exact Recht--Ré Inequalities Through Product Length Five: Uniform rational certificates and a sharp five-factor threshold
- **Manuscript ID**: Not assigned
- **Review Date**: 30 July 2026
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role

Peer Reviewer 1 (Methodology)

### Reviewer Identity

Specialist in exact computer-assisted proofs at the interface of matrix
analysis, noncommutative polynomial optimization, rational sum-of-squares
certification, and computational representation theory. I am calibrating this
report against the methodological expectations of a strong specialist journal
in matrix analysis.

### Review Focus

I evaluate the theorem-to-certificate-to-code chain: normalization, free
localizers, orbit compression, balanced continuation, representation-theoretic
block positivity, determinant certificates, exceptional endpoints, verifier
semantics, negative controls, and clean-environment reproducibility. Multiple
implementations that share the certificate schema, orbit conventions, test
vectors, and proof architecture are treated as redundant checks rather than
independent validation.

---

## Overall Assessment

### Recommendation

- [ ] **Accept**
- [ ] **Minor Revision**
- [x] **Major Revision**
- [ ] **Reject**

### Confidence Score

**4/5** — The exact-arithmetic and matrix/SOS methodology is within my area of
expertise. I have high confidence in the identified proof-assurance and
reproducibility obligations, while a definitive judgment on the theorem itself
would still benefit from an independent line-by-line specialist reconstruction
of the representation reduction.

### Summary Assessment

The manuscript proves new four- and five-factor Recht--Ré bounds using rational
free-localizer certificates, balanced-block continuation, symmetry reduction,
and exact determinant positivity, together with a rational sharpness witness
at \(m=n=5\). The mathematical architecture is coherent, the acceptance
arithmetic is exact, and the counterexample replay is especially clean.
Moreover, the manuscript commendably distinguishes redundant implementation
agreement from independent validation (pp. 1 and 9).

The central methodological weakness is that the human-readable proof does not
yet establish the semantic completeness of the hard-coded representation test
vectors and block contractions. Section 5 states the isotypic decompositions
and multiplicities, but neither defines the actual vectors used by the
verifiers nor proves that their contractions detect positivity on every
isotypic component. The related degree-\(\leq4\) interpolation premise is also
asserted rather than proved. These are theorem-critical links, not merely
expository details. In addition, my clean read-only replay found that all proof
executables pass in normal and optimized Python modes, but the package-level
gate fails because both release manifests are stale. The work is promising and
likely repairable in one substantial revision, but a strong specialist journal
should require those semantic and release-integrity gaps to be closed and
re-reviewed.

---

## Strengths

### S1: Exact acceptance arithmetic throughout

Sections 3--7 (pp. 3--9) reduce the proof obligations to rational identities,
exact ranks, exact block entries, exact determinant polynomials, and exact
kernels. The verifiers use `Fraction` or SymPy rational arithmetic and do not
accept any theorem claim using a floating-point tolerance. My replay confirmed
that all seven executable paths complete successfully under both ordinary
Python and `python -O`. This is a substantial methodological strength for a
computer-assisted theorem.

### S2: Clear theorem-to-certificate architecture

The normalization lemma (p. 2), direct free-localizer argument (p. 3), stable
certificate identities (Proposition 3.1, pp. 3--4), continuation argument
(pp. 4--5), and determinant positivity mechanism (pp. 5--7) form a coherent
logical chain. In particular, the manuscript correctly distinguishes rational
identity continuation from positivity continuation (p. 5), preventing a
common computer-assisted-proof overreach.

### S3: Exact and internally replayed sharpness witness

Section 6.3 (pp. 7--8) gives rational matrices, an exact projector-based PSD
proof, the arithmetic-mean identity, and the closed form of the symmetrized
product. The accompanying program independently enumerates all \(120\)
permutations over rational arithmetic and verifies the eigenvalue
\(-285/2<-120\). This makes the five-factor lower threshold sharp without
depending on an unreproduced numerical SDP.

### S4: Fail-closed verifier repair and adversarial controls

The package replaces optimization-sensitive `assert` acceptance checks with
explicit `VerificationError` conditions and statically excludes new assertions
from the acceptance paths. I ran the mutation suite read-only: all twelve
normal/optimized baselines passed, and every applicable verifier rejected each
of the eight one-field mutations (parametric identity, determinant record,
seed, and endpoint for both product lengths) with nonzero status and an
explicit failure. This is unusually good verifier-engineering practice.

### S5: Honest assurance and discovery boundaries

The status box on p. 1 and the reproducibility boundary on p. 9 explicitly say
that the two arithmetic engines share the certificate schema, orbit
conventions, representation vectors, and high-level reduction. The manuscript
also states that seed discovery is not reproduced. These calibrations are
accurate and materially improve the scientific reliability of the package.

---

## Weaknesses

### W1: The representation test vectors are not proved semantically complete

**Problem**: Section 5 (pp. 5--6) gives the abstract decompositions
\[
\mathcal W_n\cong4[n]\oplus4[n-1,1]\oplus[n-2,2]\oplus[n-2,1,1]
\]
and the analogous stabilizer decomposition, then immediately treats block
sizes \(G:8,6,1,1\) and \(H:4,4,1,1\) as a complete positivity test. The
actual test vectors appear only as hard-coded arrays in both verifiers. The
paper does not prove that these vectors lie in the claimed irreducibles, give
the stated multiplicity representatives with compatible intertwiners, and
make restriction to the displayed blocks equivalent to positivity of the full
invariant Gram matrices. The two implementations share these vectors, so
their agreement cannot discharge this obligation.

**Why it matters**: Positive restrictions to selected subspaces do not imply
positivity of a full matrix unless those subspaces are shown to furnish a
complete isotypic block diagonalization. This is the principal semantic bridge
between the determinant certificates and Proposition 3.1.

**Suggestion**: Add a self-contained lemma and appendix that explicitly list
the \(G\)- and \(H\)-test vectors, construct the corresponding equivariant
maps, prove their irreducible types and independence, and derive the PSD
equivalence by Schur's lemma. Add an exact release check that the contraction
map from invariant orbit coordinates to symmetric block entries has full rank
\(59\) for \(G\) and \(22\) for \(H\) throughout the stable regime (with the
appropriate rank \(58\) for the \(n=4\) stabilizer endpoint). In my read-only
audit the shipped contractions had ranks \(59/59\) and \(22/22\) at
\(n=5,6,10\), so the requested check appears feasible; it is not currently a
release obligation.

**Severity**: **Critical**

### W2: The polynomial interpolation degree bound needs a proof, not one extra point

**Problem**: The verifiers reconstruct every representation-block coefficient
from five values and test one additional value (p. 8). The code comment says
that degree \(\leq4\) follows from “at most four freely summed indices,” but
Section 5 does not state or prove this combinatorial lemma. Agreement at one
out-of-sample integer does not establish a global degree bound.

**Why it matters**: If any contraction coefficient had degree \(>4\), five
interpolation points plus one check would not identify its all-\(n\) polynomial.
The subsequent determinant families could then certify the wrong block
functions away from the sampled values.

**Suggestion**: Prove that every orbit contraction is a finite integer
combination of falling-factorial counts \((n-c)_r\) with \(r\leq4\), including
the stabilizer case, and therefore has degree at most four. Preferably make the
verifier construct these coefficient polynomials directly from equality
patterns/falling factorials; interpolation may remain as a redundant check.

**Severity**: **Major**

### W3: The submitted replication package currently fails its own release gate

**Problem**: I ran
`scripts/replay_all.py --skip-mutations` with the supplied Python environment.
Every exact proof path, verifier-safety check, citation check, claim-inventory
check, and \(m=6\) classification passed. Nevertheless, the final result was
`PUBLICATION-CANDIDATE REPLAY: FAIL` because both `MANIFEST.sha256` files
contain stale hashes. The mismatches include the repaired verifiers,
derivation scripts, `verify.sh`, and several release documents. This conflicts
with the package status statement that the repaired releases have new
manifests. In addition, p. 8 labels the three per-release shell commands as the
“complete replay commands,” although they omit manifest validation,
normal-versus-optimized comparison, negative controls, and package-level
integrity checks.

**Why it matters**: A replication package is not release-qualified when its
own cryptographic integrity gate fails. Readers following the manuscript also
receive a less stringent command than the one that defines package acceptance.

**Suggestion**: Regenerate exhaustive manifests only after the final
manuscript/code revision, run the full non-skipped replay from a clean
extraction, archive the complete transcript plus environment and artifact
hashes, and make `scripts/replay_all.py` the canonical manuscript command.
Clarify that the per-release scripts are proof-only convenience commands.

**Severity**: **Major**

### W4: Negative controls test data corruption but not the shared semantic code

**Problem**: The mutation suite effectively tests fail-closed handling of four
certificate-data classes. It does not challenge shared code that generates the
76 word patterns, canonicalizes \(G/H\) orbits, constructs test vectors,
contracts representation blocks, or maps certificate identities to concrete
free-polynomial coefficients. Both arithmetic implementations reproduce much
of this logic almost line for line.

**Why it matters**: A shared semantic error can survive both implementations
and all existing certificate mutations. The manuscript itself correctly
recognizes this boundary on p. 9, but the strongest feasible package should
reduce it.

**Suggestion**: Add a structurally separate semantic bridge checker that, at
the base and endpoint sizes, expands the full concrete word-indexed Gram
matrices without restricted-growth-string compression, verifies every concrete
word coefficient, checks the full group actions and block-map ranks, and
compares direct full-matrix PSD/LDL results with the reduced blocks. Add code
mutations or known-negative fixtures for an omitted word pattern, a changed
orbit convention, a corrupted test vector, and a missing irreducible block.

**Severity**: **Major**

### W5: Discovery provenance is incomplete

**Problem**: The rational seed certificates are reproducible, but the SDP
inputs, solver versions, complete logs, and selection/rounding history are not
preserved (p. 9). The exact reconstruction makes discovery non-load-bearing,
but readers cannot reproduce how the successful affine free coordinates were
found or assess search multiplicity.

**Why it matters**: This does not weaken a correct certificate proof, but it
limits method replication and makes it harder to extend the architecture to
six factors or audit possible researcher degrees of freedom.

**Suggestion**: Retain the current candid limitation. If any discovery files
remain, archive them as explicitly non-load-bearing provenance with hashes. Add
a precise algorithmic specification of the feasibility model, objective or
regularizer, rational rounding rule, and exact-reconstruction acceptance rule
so future researchers can reproduce the method even if the historical run is
unrecoverable.

**Severity**: **Minor**

---

## Detailed Comments

### Title & Abstract

- The title accurately identifies the scope and does not overclaim an
  all-\(m\) restoration.
- The abstract gives unusually useful certificate counts and threshold
  information. It should add one phrase indicating that completeness of the
  representation reduction is established by a human lemma plus an executable
  rank check once W1 is repaired.
- “Two exact implementations” is appropriately qualified in the adjacent
  status box; keeping that qualification near every “independent” or
  “cross-check” phrase is important.

### Introduction

- The research question and theorem delta are clear: settle the open
  four-factor family, restore the five-factor upper bound including its
  endpoint, and determine the sharp lower threshold.
- The distinction among the norm inequality, termwise norm results, and
  Loewner certificates is methodologically helpful.

### Literature Review / Theoretical Framework

- From a methodological perspective, the manuscript uses only the easy
  free-localizer direction, not completeness of a Positivstellensatz (p. 3).
  This is correct and should remain explicit.
- The representation-theoretic framework is the least self-contained part.
  The abstract multiplicity calculation is not yet enough to validate the
  concrete block contractions.

### Methodology / Research Design

- **Design type**: theoretical research with exact computer-assisted
  certificate verification.
- **Alignment**: the design is appropriate. A rational SOS certificate plus an
  exact all-parameter positivity proof can answer the theorem question without
  reproducing the numerical discovery run.
- **Theorem-to-code trace**:
  1. Lemma 2.1 converts the norm statement to normalized two-sided Loewner
     bounds.
  2. Equations (6)--(7) encode those bounds as positive free localizers.
  3. The 76 restricted-growth patterns per sign encode all equality patterns
     through degree five in the stable range.
  4. Balanced coloring transports exact seeds to infinitely many multiples;
     rational identity then continues the coefficient equations.
  5. Representation contractions and determinant polynomials are intended to
     prove uniform Gram positivity.
  6. Separate certificates cover \(m=4,n=4\) and the \(m=5,n=5\) upper
     endpoint; an exact rational construction covers lower sharpness.
- Steps 1--4 and 6 are well supported. Step 5 needs the explicit completeness
  and degree lemmas described in W1--W2.
- **Sampling/statistical reporting**: not applicable. This is a purely
  theoretical paper; no inferential statistics, sampling, effect sizes, or
  confidence intervals are involved.

### Results / Findings

- The theorem statements match the replayed acceptance summaries:
  two-sided \(m=4\) for \(n\ge4\), upper \(m=5\) for \(n\ge5\), and lower
  \(m=5\) for \(n\ge6\).
- The determinant counts and positive-coefficient counts are reconstructed
  rather than merely read from JSON, which is good.
- The paper should not describe a package as fully reproducible until the
  manifests and full runner pass together from a clean extraction.

### Discussion

- Section 8 and the status box are strong. They avoid inferring a universal
  optimization advantage from a matrix inequality and correctly exclude the
  incomplete six-factor artifacts from every theorem path.
- The limitations should distinguish more sharply between (i) unreproduced
  discovery, which is non-load-bearing, and (ii) incomplete semantic
  justification of test-vector coverage, which is load-bearing and must be
  fixed rather than merely disclosed.

### Conclusion

- There is no separate conclusion section. A short conclusion would help
  restate the exact scope, the sharp threshold, and the principal extension
  target without mixing those points into the \(m=6\) limitations.
- The theorem conclusions themselves do not over-infer beyond product length
  five.

### Reproducibility

- Core proof paths passed on macOS with Python 3.13.5 and SymPy 1.14.0 in both
  normal and optimized modes.
- The full mutation suite passed and demonstrated explicit fail-closed
  behavior for all eight tested data corruptions.
- The package-level replay is not currently release-qualified because both
  manifests fail. A fresh final receipt should supersede the inherited Linux
  receipts and bind the unified manuscript, certificates, code, tests, and
  environment lock to one package hash.

### Methodological Fallacies Detected

- **Potential circular verification**: not a mathematical circular proof, but
  the two verifiers share the same semantic encodings, so their agreement
  cannot validate those encodings. The manuscript acknowledges this; W1 and W4
  specify how to reduce the risk.
- **Finite-sample extrapolation risk**: interpolation at five points plus one
  check would be insufficient without the analytic degree bound. This is
  repairable by proving the falling-factorial counting lemma.
- **No statistical fallacies apply**: there is no empirical sampling or
  hypothesis-testing component.

---

## Questions for Authors

1. Can the authors provide a complete lemma showing that each hard-coded
   \(G/H\) test-vector family furnishes the claimed irreducible multiplicity
   space and that positivity of the contracted blocks is equivalent—not merely
   necessary—to positivity of every invariant Gram matrix?
2. What is the formal combinatorial proof that every representation
   contraction coefficient has degree at most four in \(n\)? Can the release
   construct those polynomials directly rather than infer them from five
   samples?
3. Will the final artifact regenerate both manifests after all edits and
   provide a clean-extraction transcript in which the non-skipped
   `scripts/replay_all.py` run terminates in
   `PUBLICATION-CANDIDATE REPLAY: PASS`?
4. Can the authors add a genuinely different base-size checker that expands
   concrete word coefficients and full invariant Gram matrices without using
   the shared restricted-growth-string and test-vector machinery?

---

## Minor Issues

### Language / Grammar

- The prose is generally clear and technically precise.
- On p. 6, “Total \(25/26\)” should be labeled explicitly as “upper/lower” in
  the row itself; the current header is easy to misread.

### Citation Format

- No methodology-critical citation-format issue was found.

### Figures and Tables

- A compact proof-obligation table mapping theorem clauses to certificate
  identities, positivity blocks, endpoint files, verifier functions, and
  negative controls would materially improve auditability.

### Layout and Commands

- On p. 8, the standalone De Sa command is redundant because the current
  `releases/m5/verify.sh` already invokes that replay.
- Replace “complete replay commands” on p. 8 with the package-level full replay
  command; label the three displayed commands as individual proof replays.
- Reconcile the manuscript's inherited Linux receipt statement with the
  reproducibility guide's macOS consolidation environment and provide one
  current final receipt.

---

## Dimension Scores

These uncalibrated scores are ordinal judgments against a strong specialist
journal, not predictions of venue acceptance.

| Dimension | Score (0--100) | Descriptor | Notes |
|---|---:|---|---|
| Originality (20%) | 87 | Strong | New exact four-factor theorem and sharp five-factor restoration |
| Methodological Rigor (25%) | 58 | Weak | Exact arithmetic is strong, but representation completeness and interpolation degree remain theorem-critical gaps |
| Evidence Sufficiency (25%) | 66 | Adequate | Extensive certificates and mutations; shared semantic encodings and stale manifests limit current sufficiency |
| Argument Coherence (15%) | 80 | Strong | Clear normalization-to-localizer-to-positivity structure |
| Writing Quality (15%) | 82 | Strong | Precise, compact, and unusually candid about assurance boundaries |
| Literature Integration (optional) | 77 | Strong | Major methodological antecedents are connected appropriately; domain reviewer should assess completeness |
| Significance & Impact (optional) | 84 | Strong | Resolves prominent low-product-length cases with reusable exact methods |
| **Weighted Average** | **72.7** | **Major Revision override** | Numerical average is secondary; W1 is a critical single-dimension gate requiring re-review |

The recommendation is **Major Revision** despite the strong overall potential
because W1 concerns the logical sufficiency of the positivity proof and W3
means the submitted package does not currently pass its own release criterion.
