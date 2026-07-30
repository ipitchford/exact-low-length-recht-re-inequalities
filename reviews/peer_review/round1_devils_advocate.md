# Devil's Advocate Review

## Recommendation

**Major revision; do not release or submit the present artifact set.**

I did not falsify the stated \(m=4\) or \(m=5\) theorem. The exact identities,
positivity certificates, exceptional endpoints, and De Sa counterexample
survived both the bundled checks and independent fixed-\(n\) attacks. The
blocking defects are presently artifact identity and auditability, not a
located mathematical counterexample: both release manifests fail, the package
has no Git identity, and load-bearing semantic checks were added while this
review was in progress and are not yet bound into a frozen release.

Audit snapshot: 30 July 2026, 18:49 BST. The unified TeX had SHA-256
`ff61428ad462ca959b3b11fbe6edb5cae61b42f9565f80f102d0abfcaeca4115`;
the subsequently added semantic checker had SHA-256
`a07c804180ed36e1d1de8018966a67e9f799433fd79225647ab46edbbe4867f2`.

### Review-integrity disclosure

I did not open any existing referee report or editorial decision. However, an
absolute-path `rg` exclusion behaved differently from the intended relative
glob and accidentally surfaced a few isolated lines from review files in tool
output. I stopped that search, did not open those files, did not use the
snippets as evidence, informed the coordinating editor immediately, and based
the findings below on the manuscript, certificate JSON, verifiers, and my own
attacks. A separate strict clean-room review is warranted.

## Strongest Counter-Argument

The paper's strongest vulnerability is that a large internally consistent
certificate stack can still prove the wrong formalization. Both main verifiers
share the same equality-pattern convention, the same ordering of 59 and 22
Gram orbits, and the same hand-selected representation vectors. If that common
semantic bridge omitted a word class, merged two group orbits, or tested an
incomplete set of isotypic components, exact rational arithmetic and positive
minor inventories would only certify the mistranslated problem. Likewise,
balanced lifting proves certificate identities at multiples of the base size,
and rational continuation extends those identities, but neither step
transports positive semidefiniteness to nonmultiples. Any general theorem that
silently promotes identity continuation to positivity would therefore fail.
Finally, a norm of an averaged product is not an expectation of product norms
or an algorithmic convergence rate, so a generic “random reshuffling is
better” corollary would not follow.

This counter-argument was substantially weakened by the exact semantic checker
added during review: it compared canonical classes with explicit \(S_5\) and
\(S_4\) actions, expanded seven concrete free-polynomial identities without
the compressed equation matrices, checked fourteen full Gram matrices by
exact LDL elimination, and established representation-span and contraction
ranks. My separate orbit-span and full-Gram reconstructions agreed. The
remaining objection is consequently release binding: these new checks appeared
after the initial snapshot, the paper does not yet make their certificate
validation contract explicit, and the hashes currently fail.

## Issue List

### CRITICAL

None found in the stated \(m=4/m=5\) theorem chain.

### MAJOR

| # | Dimension | Issue | Location / required remedy |
|---|---|---|---|
| 1 | Reproducibility and provenance | Both `MANIFEST.sha256` files fail: 7 mismatches in `releases/m4` and 8 in `releases/m5`. The mismatches include both verifiers, derivation scripts, release manuscripts, and shell runners. Thus the advertised one-command release gate ends in `PUBLICATION-CANDIDATE REPLAY: FAIL`, even though every arithmetic and mutation stage passes. The certificate JSON files themselves still match their listed hashes. | `README.md`, `REPRODUCIBILITY.md`, paper §7 and §9, both release manifests. Freeze one tree, rebuild manifests deliberately, replay from a fresh extraction, and publish the resulting receipt and immutable archive hash. |
| 2 | Machine-to-mathematics bridge | The manuscript states the orbit counts and block vectors schematically, but does not give a certificate-validation theorem proving that the concrete orbit classifier, word patterns, representative vectors, and contraction maps cover the full Gram spaces. This was the principal possible foundation collapse. The new `scripts/check_semantic_bridge.py` supplies strong exact evidence, but appeared during review, is not mentioned in the manuscript's replay inventory, and is not bound to a release identity. | Paper §§3, 5, and 7, especially the reproducibility boundary on p. 9. Add explicit canonical definitions and a short validation lemma; list the representatives or a hash-bound table; explain why orbit spans and contraction rank imply full PSD coverage; then bind the checker and its negative controls into the frozen package. |
| 3 | Snapshot identity | The directory is not a Git repository, yet `provenance/SOURCE_PROVENANCE.md` invokes repository commit history. Load-bearing files changed during the audit. A reader cannot identify which byte-level package a verdict applies to. | `provenance/SOURCE_PROVENANCE.md` and package root. Supply a commit/tag or immutable archive digest and prohibit edits during external review. |

### MINOR

| # | Dimension | Issue | Location / required remedy |
|---|---|---|---|
| 1 | Claim-evidence consistency | The \(m=5\) claim-evidence matrix still describes external Lai--Lim numerical evidence as the sharpness acceptance condition, whereas the unified paper and counterexample program use De Sa's exact rational witness as the load-bearing proof. | `releases/m5/CLAIM_EVIDENCE_MATRIX.md`, “Sharpness of threshold.” Replace the stale acceptance condition with the exact in-package replay. |
| 2 | Reviewability | The exact checks are much stronger than the prose makes independently reconstructible. At least one worked orbit-to-coefficient calculation and one orbit-to-block contraction should be printed, so a reader can connect the formal definitions to the code without reverse engineering it. | Paper §§3–5 or a hash-bound technical appendix. |

## Concrete Attempted Attacks and Outcomes

| Attack | Outcome |
|---|---|
| Re-derived the normalization and checked the Hermitian/reversal and upper/lower sign conventions. | **Survived.** Homogeneity with \(t=\|\sum_iA_i\|/n\) gives exactly the two-sided normalized statement. |
| Ran all standard-library and SymPy identities, seed transversals, determinant reconstructions, kernels, and endpoints under ordinary and optimized Python in the pinned SymPy 1.14 environment. | **Survived.** All exact paths passed. |
| Re-derived all 162 orbit functions for each product length from the base seeds using balanced \(5\)- and \(6\)-block averaging. | **Survived.** Exact equality with the published rational families. |
| Rebuilt full \(G\) and \(H\) matrices directly from orbit JSON at \(m=4\), \(n=5,6,7,10,13\), and \(m=5\), \(n=6,7,8,11,14\), plus the exceptional endpoints. | **Survived.** No negative eigenvalue was found; each upper \(G\) had exactly the expected numerical zero direction and all other tested matrices were positive definite. |
| Evaluated the free localizers end-to-end on independently generated \(3\times3\) PSD tuples near the normalization boundary. | **Survived.** Relative identity residuals were \(1.0\times10^{-15}\) to \(9.3\times10^{-15}\), with positive target matrices. |
| Generated the group orbit spans of every stated representation vector. | **Survived.** At \(n=5,6,7\), the component dimensions summed to the entire \(1+n+n^2\) word space; the \(n=4\) stabilizer endpoint gave \(8+12+1=21\). |
| Ran the later exact semantic checker and its omitted-pattern, merged-orbit, corrupted-vector, and omitted-block mutations in normal and optimized modes. | **Survived.** The positive run passed and all eight injected runs were rejected. |
| Replayed De Sa's five rational matrices and all 120 products. | **Survived.** The matrices are PSD with mean \(I\), and the all-ones eigenvalue of \(E_{5,5}\) is \(-285/2<-120\). |
| Tested release integrity. | **Failed.** Fifteen listed file hashes do not match, so the aggregate release gate correctly refuses a PASS. |

These computations are strong falsification attempts, not a substitute for a
human proof of every representation-theoretic statement.

## General Continuation and Optimization Corollaries

### General continuation

A general **identity-continuation lemma** is valid with explicit hypotheses:
start from an exact base-\(b\) localizer certificate; require enough base
labels to realize every Gram-entry equality pattern; perform balanced
\(b\)-color averaging at \(n=br\); express each orbit entry as a rational
function; and exclude poles in the target range. Equality at infinitely many
multiples then proves the rational coefficient identities throughout the
stable range.

What does **not** follow is PSD at nonmultiples, or an all-\(n\) operator
inequality. Positivity needs a separate uniform argument, such as the shifted
minor certificates used here. Any proposed continuation corollary must say
“identity” rather than “positive certificate” unless it includes that second
proof. It must also state the orbit-stability threshold; small \(n\) may
require separate representation types, as \(m=4,n=4\) already demonstrates.

### Optimization

A narrow corollary is valid: for PSD Hermitian update matrices, the theorem
compares the norm of the mean ordered product of four distinct samples with
the corresponding with-replacement mean product; the analogous five-step
statement holds for \(n\ge6\). This is essentially the original
Recht--Ré formulation.

No general random-reshuffling advantage follows. The result does not compare
expectations of norms, stochastic losses, affine terms, multiple epochs, or
full-epoch products outside the proved lengths; it also does not cover
indefinite or nonsymmetric update matrices. Jensen's inequality does not
reverse this gap. The current caution in paper §8 is therefore correct and
should not be weakened.

## Ignored Alternative Paths

1. A standalone checker using a different orbit ordering and independently
   derived representation basis would reduce the remaining common-mode risk
   more than another arithmetic engine using the same schema.
2. A conventional appendix proving the certificate-validation theorem would
   turn the semantic checker from persuasive code into a transparent
   mathematical bridge.
3. The \(m=6\) material should remain non-release. A dual obstruction to this
   truncated SOS ansatz is not a matrix counterexample without a completeness
   or extraction argument.

## Missing Stakeholder Perspectives

- An accountable human author who accepts responsibility for the theorem and
  frozen code.
- An independent representation theorist or free real algebraic geometer who
  reconstructs the semantic bridge without using the package's conventions.
- An optimization specialist who polices the distinction between
  norm-of-expectation inequalities and algorithmic performance claims.

## Unexamined Premise

The package implicitly assumes that successful exact replay can be attached
to a stable research object. At present that premise is false: the object
changed during review and has neither a passing manifest nor a commit
identifier. Freeze and hash the object before asking reviewers to convert
strong computational evidence into a publication verdict.

## Observations (Non-Defects)

- The \(m=4/m=5\) statement is carefully separated from the incomplete
  \(m=6\) frontier.
- The manuscript correctly distinguishes redundant exact implementations,
  derivation replay, external audit, and peer review.
- Positive shifted coefficients are used only for positivity; rational
  continuation is correctly described as an identity argument.
