# Peer Review Report

## Manuscript Information

- **Title**: *Exact Recht–Ré Inequalities Through Product Length Five: Uniform rational certificates and a sharp five-factor threshold*
- **Manuscript ID**: Not assigned
- **Review Date**: 30 July 2026
- **Review Round**: Round 1
- **Reference venue**: SIAM Journal on Matrix Analysis and Applications or a comparably strong specialist journal

---

## Reviewer Information

### Reviewer Role

Peer Reviewer 2 (Domain)

### Reviewer Identity

Senior matrix analyst specializing in Loewner order, noncommutative arithmetic–geometric mean inequalities, free-polynomial positivity, exact computer-assisted proofs, and symmetric-group reductions.

### Review Focus

I reviewed the correctness and scope of the mathematical statements as presented, the semantic connection between the free-localizer certificates and the Loewner inequalities, the symmetric-group reductions, and the paper's positioning in the matrix-inequality and random-reshuffling literature. I also inspected the accompanying exact artifacts read-only and ran the standard-library verifiers for the four- and five-factor results and the exact De Sa counterexample. I did not inspect any other referee report.

---

## Overall Assessment

### Recommendation

- [ ] **Accept**
- [ ] **Minor Revision**
- [x] **Major Revision**
- [ ] **Reject**

### Confidence Score

**4/5 — high confidence.** The matrix-analysis, Loewner-order, and representation-theoretic aspects are directly within my expertise. I did not independently rederive every orbit encoder, test vector, or one of the 1,704 coefficient records by hand, so I reserve one point of confidence.

### Summary Assessment

This manuscript claims a complete exact status through product length five for the original Recht–Ré norm inequality: a two-sided all-\(n\) theorem for four factors, an all-\(n\) upper theorem for five factors, a restored lower theorem for \(n\geq 6\), and an exact sharp failure at \(m=n=5\). The proof combines free localizers, symmetric Gram-orbit coordinates, balanced-block transport, rational continuation, fixed-size representation blocks, and shifted-positive principal-minor certificates. The mathematical architecture is coherent, the normalization and Loewner reductions are correct, and my read-only replay of the standard-library implementations reproduced all stated exact terminal obligations, including De Sa's eigenvalue \(-285/2\).

If validated at the semantic level, the two main theorems are substantial and highly suitable for a specialist matrix-analysis venue. The present obstacle is expository rather than an identified false statement: the load-bearing passage from free words and orbit coordinates to the concrete representation blocks is mostly delegated to code and data. The paper itself does not yet give a sufficiently explicit validation theorem, canonical orbit specification, or proof that the machine test vectors exhaust the relevant isotypic components for every stable integer \(n\). The literature discussion also omits several directly adjacent works, most notably Albar–Junge–Zhao and Yun–Sra–Jadbabaie. I therefore recommend major revision and re-review, while emphasizing that the manuscript appears to contain a potentially important result rather than a merely incremental computation.

---

## Strengths

### S1: A substantial completion of the four- and five-factor strata

Theorem 2.2 (pp. 2–3) cleanly separates four claims: the two-sided four-factor inequality for every \(n\geq4\), the five-factor upper inequality for every \(n\geq5\), the five-factor lower inequality for every \(n\geq6\), and sharp failure of the latter at \(n=5\). This is the right formulation after Lai and Lim exposed the asymmetry between the two Loewner sides. Completing the previously open four-factor family and locating the five-factor lower threshold would be a genuine advance.

### S2: Correct normalization and operator-order formulation

Lemma 2.1 (p. 2) correctly uses \(S=\sum_iA_i\succeq0\), homogeneity, and Hermiticity of the reversal-invariant ordered sum to show equivalence between the original spectral-norm inequality and the normalized two-sided Loewner bound. This is concise and mathematically sound. The theorem then keeps the upper and lower sides separate, avoiding the conceptual ambiguity that affected the original conjecture.

### S3: A strong exact positivity mechanism

Sections 3–5 (pp. 3–7) identify the right proof object: an identity
\[
(n)_m\mp e_{m,n}
=\sum_i\mathcal L_{x_i}(G_{m,n,i})+\mathcal L_{n-\sum x_i}(H_{m,n})
\]
with exact rational positive semidefinite Gram matrices. The direct factorization argument on p. 3 is enough for complex Hermitian substitutions and does not invoke an unnecessary completeness direction of a Positivstellensatz. The fixed multiplicity blocks \(8,6,1,1\) and \(4,4,1,1\), followed by Sylvester tests and a separately treated forced kernel, are well chosen for a dimension-free proof.

### S4: Exact and transparent sharpness at \(m=n=5\)

Section 6.3 (pp. 7–8) is particularly strong. It gives De Sa's matrices explicitly over \(\mathbb Q\), proves their spectra are \(2,1,1,1,0\), verifies their mean is \(I\), and states the exact decomposition
\[
\frac{1}{120}E_{5,5}
=\frac{29}{64}\!\left(I-\frac15\mathbf1\mathbf1^{\mathsf T}\right)
-\frac{19}{16}\frac15\mathbf1\mathbf1^{\mathsf T}.
\]
The resulting eigenvalue \(-285/2<-120\) makes the threshold claim self-contained at the conceptual level and removes dependence on unreplayed numerical SDP/Farkas evidence.

### S5: Unusually careful assurance boundaries

The status box on p. 1 and the reproducibility boundary on pp. 8–9 explicitly distinguish exact replay, independent implementation, derivation cross-checking, seed discovery, semantic coverage, and third-party audit. This calibration is exemplary for a computer-assisted theorem. My own execution of the three standard-library paths reproduced the paper's stated exact results.

---

## Weaknesses

### W1: The semantic certificate-to-theorem bridge is not yet sufficiently explicit

**Problem**: Sections 3.1 and 5 (pp. 3 and 6–7) state that there are 59 stabilizer orbits, 22 full-symmetry orbits, 76 canonical word-pattern equations per sign, and fixed multiplicity blocks, but the manuscript does not define the canonical orbit encoder, exhibit the representation test vectors, or prove in-text that the resulting blocks are congruent to the full Gram matrices for every stable integer \(n\). The key sentence that the "concrete orbit maps and test vectors ... are part of the released certificates" transfers a mathematical proof obligation to implementation artifacts. Section 7 itself acknowledges that exact replay does not establish semantic coverage.

**Why it matters**: The main theorem is dimension-free and rests entirely on the assertion that the verified finite arrays encode every coefficient and every isotypic component of the intended free-polynomial problem. A coding error shared by both implementations at precisely this semantic layer would not be detected by the redundant arithmetic engines.

**Suggestion**: Add a formal **certificate-validation theorem** with: (i) a mathematical definition of the orbit key for a pair of words (and the distinguished letter for \(G\)); (ii) a lemma proving the 59/22 counts in the stated stable ranges; (iii) an explicit formula or immutable table for each representation test-vector family and its normalization; (iv) a proof that these vectors span all multiplicity spaces in (12)–(13); and (v) a theorem stating exactly which finite checks imply the operator inequality. Include at least one nontrivial orbit-to-block calculation by hand and bind the remaining tables to immutable hashes.

**Severity**: Major

### W2: The balanced continuation should be elevated from a calculation to a general theorem

**Problem**: Section 4 (pp. 4–5) contains the conceptual heart of the paper, but it is presented as two parallel constructions. Equations (9)–(11) implicitly define a polynomial/rational continuation from a \(b\)-variable certificate, yet the hypotheses under which this transport preserves coefficient identities are not packaged as a general statement. The distinction between a genuine hypergeometric expectation at \(n=br\) and an algebraic continuation at other real \(n\) is stated, but the proof of the scaling factor \((b/n)^{d+1}\), the role of the distinguished letter, and the absence of relevant poles are compressed.

**Why it matters**: As written, readers may view the paper as two large certificate computations. A general balanced-seed lifting theorem would expose the reusable mathematical contribution and would provide a principled route toward product length six and beyond.

**Suggestion**: State and prove a general "balanced-certificate continuation theorem" for arbitrary \(m,b\), with the seed identity, group invariance, orbit-stability range, formal continuation operator, pole domain, and coefficient-identity conclusion explicit. Then specialize it to \((m,b)=(4,5)\) and \((5,6)\). Positivity can remain a separate certificate-dependent proposition.

**Severity**: Major

### W3: The directly relevant literature lineage is incomplete

**Problem**: The background on pp. 1–2 moves from Recht–Ré to Israel–Krahmer–Ward, Zhang, Lai–Lim, and De Sa. It omits Albar, Junge, and Zhao's two directly adjacent studies of noncommutative and symmetrized AGM inequalities. More seriously, p. 9 cites Peng's 2026 resolution of the SS–RS–GD inequalities without citing the Yun–Sra–Jadbabaie 2021 COLT open problem that formulated those inequalities. The current wording also attributes the termwise or expectation-of-norms result only to Israel–Krahmer–Ward without noting Duchi's earlier formulation of that variant.

**Why it matters**: A strong specialist-journal article must distinguish the original norm-of-sum conjecture, the termwise-norm variant, the symmetrized \(A^*\cdots A\) variant, dimension-free weakened constants, and the later well-conditioned SS–RS–GD formulation. These are nearby but non-equivalent statements, and the novelty claim is clearest only when the distinctions are explicit.

**Suggestion**: Add a compact comparison table with columns "object averaged," "placement of norm," "order versus norm," "assumptions," and "known status." At minimum discuss and cite:

- W. Albar, M. Junge, and M. Zhao, *Noncommutative versions of the arithmetic-geometric mean inequality*, arXiv:1703.00546 (2017): dimension-free constants for general operators and an order version under additional hypotheses.
- W. Albar, M. Junge, and M. Zhao, *On the symmetrized arithmetic-geometric mean inequality for operators*, arXiv:1803.02435 (2018): the adjacent symmetrized-product formulation and failure of the optimistic constant-one version.
- C. Yun, S. Sra, and A. Jadbabaie, *Open Problem: Can Single-Shuffle SGD be Better than Reshuffling SGD and GD?*, COLT/PMLR 134 (2021), 4653–4658: the source problem resolved by Peng.
- J. Duchi, *Commentary on “Towards a Noncommutative Arithmetic-Geometric Mean Inequality”* (2012), if a stable bibliographic record is available, for the termwise-norm variant later proved through length three by Israel–Krahmer–Ward.

For broader matrix-analysis placement, Bhatia–Kittaneh's 2008 matrix AGM survey/revisit and Alaifari–Cheng–Pierce–Steinerberger's 2020 matrix rearrangement work are also worth considering.

**Severity**: Major

### W4: The appendices expose the certificate data asymmetrically

**Problem**: Appendix A prints the four-factor parametric free functions, whereas Appendix B prints only the five-factor base and endpoint transversals. The full five-factor parametric functions remain only machine-readable. Conversely, long numeric tables consume several pages without providing the orbit definition needed to interpret the indices.

**Why it matters**: This makes the paper neither fully self-contained nor optimally concise. The asymmetry may also leave the mistaken impression that the five-factor family is less explicitly determined.

**Suggestion**: Choose one consistent policy. Preferably keep one illustrative function family and one complete small endpoint in the paper, move all large tables to a versioned supplement, and provide an immutable archive identifier plus SHA-256 manifest. Alternatively, print equivalent reconstruction data for both product lengths together with the canonical orbit schema.

**Severity**: Minor

### W5: Several range and terminology qualifications should be tightened

**Problem**: Equations (12)–(13) on p. 6 are presented as complete decompositions without immediately stating the stable ranges in which the listed partitions are distinct and valid. The status table on p. 2 says "two-sided norm inequality," while nearby prose switches among "Recht–Ré inequality," "upper Loewner bound," and "operator theorem." On p. 5, \(\mathbb E_n^{(b)}\) is denoted as an expectation even where \(n\) is merely a formal or real continuation parameter.

**Why it matters**: None of these appears to invalidate the proof, but precise range and formulation labels are important because several adjacent inequalities in the literature are not equivalent.

**Suggestion**: State \(n\ge4\) for (12) and \(n\ge5\) for (13), with the special \(n=4\) stabilizer decomposition handled separately. Reserve "expectation" for \(n=br\) and call the general object a hypergeometric continuation functional. Define once whether "Recht–Ré inequality" means the original spectral-norm statement or the normalized two-sided Loewner equivalent.

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract

- The title is accurate and the subtitle usefully signals that the five-factor lower threshold is not \(n=5\).
- "The remaining cases through product length five" is defensible only after the literature table clarifies that this refers to the original norm-of-sum/Loewner-equivalent formulation, not the several termwise or symmetrized variants.
- The abstract's certificate statistics are informative, but one sentence should state the genuinely conceptual contribution: balanced rational continuation converts finite symmetric seed certificates into uniform all-\(n\) families.

### Introduction and Literature Review

- The Recht–Ré, Lai–Lim, Zhang, Israel–Krahmer–Ward, and De Sa statements are substantially accurate.
- The characterization of Israel–Krahmer–Ward as a termwise-norm or expectation-of-norms inequality is important and correct; it must remain clearly separated from the present norm-after-summation statement.
- Lai and Lim's contribution is accurately described: they prove \(m=2,3\) for arbitrary \(n\), numerically certify the \(m=4,n=4,5\) cases, formulate the all-\(m\) upper conjecture, and obtain the \(m=n=5\) lower obstruction through SDP/Farkas methods.
- De Sa's explicit family and the exact \(n=5\) formula are correctly attributed.
- The Albar–Junge–Zhao and Yun–Sra–Jadbabaie omissions should be repaired as described in W3. Peng should be presented as resolving Yun–Sra–Jadbabaie's well-conditioned SS–RS–GD question, not as an isolated contemporary result.

### Theoretical Framework

- The free-localizer framework is appropriate. The manuscript correctly uses only the elementary soundness implication \(Q\succeq0,\ g(A)\succeq0\Rightarrow\mathcal L_g(Q)(A)\succeq0\), so the citation to Helton–Klep–McCullough supplies context rather than a load-bearing completeness theorem.
- The Gatermann–Parrilo citation appropriately motivates symmetry reduction, but it does not by itself establish the concrete noncommutative orbit maps or the block sizes in this problem. Those details are the paper's own proof obligation.
- Peyrl–Parrilo is appropriately invoked for rational reconstruction after numerical discovery; the text correctly says numerical values are discarded before acceptance.
- Zhang's balanced lifting is the right antecedent for Section 4. The manuscript should make clearer which part is inherited (validity at multiples) and which part is new (rational orbit continuation plus all-\(n\) positivity).

### Main Mathematical Argument

- Lemma 2.1 is correct.
- Reversal indeed makes \(E_{m,n}\) Hermitian.
- Proposition 3.1, if the stated exact identities and positive semidefinite Gram matrices are semantically faithful to the released encodings, directly proves the stable-range theorem.
- The permutation-module decompositions and multiplicity-block sizes are correct in the stable ranges. Under \(S_n\),
  \[
  \mathcal W_n\cong4[n]\oplus4[n-1,1]\oplus[n-2,2]\oplus[n-2,1,1],
  \]
  and under the point stabilizer one obtains multiplicities \(8,6,1,1\). The manuscript should add the explicit range qualifications.
- The singular-block argument on pp. 6–7 is valid: a positive definite leading \(7\times7\) block plus a kernel vector with nonzero last coordinate yields a matrix congruent to \(A\oplus0\).
- Strict positivity of every shifted coefficient in (14) is sufficient for all \(n\ge b_m\), and the separate endpoint strategy is logically clean.
- The exact De Sa counterexample is correctly normalized and evaluated.

### Results and Evidence

- The paper reports enough aggregate counts to make the computational burden visible: 304 rational-function coefficient identities across the two lengths, 102 principal-minor polynomials, and 1,704 positive shifted coefficients.
- My read-only execution of the three standard-library programs produced the advertised exact outcomes:
  - \(m=4\): 152 identities, seed transversals, 51 determinant records, the common kernel, and both \(n=4\) endpoints passed.
  - \(m=5\): 152 identities, direct orbit replays through \(n=11\), 51 determinant records, seed specializations, and the \(n=5\) upper endpoint passed.
  - De Sa witness: exact PSD spectra, mean \(I\), 120-product sum, and eigenvalue \(-285/2\) passed.
- These checks support the arithmetic layer but do not replace W1's semantic validation theorem.

### Discussion, Limitations, and Future Direction

- Section 8 appropriately refuses to infer a universal random-reshuffling advantage and distinguishes Peng's well-conditioned result.
- The six-factor discussion is responsibly negative: missing block-builder inputs prevent a theorem, and no putative dual file is promoted to a counterexample.
- The paper can nevertheless push into more significant territory without claiming an \(m=6\) result: formulate the general balanced-certificate continuation theorem, characterize the finite orbit-stability threshold in terms of word degree, and state a precise checklist for extending the method to arbitrary \(m\). This would turn the incomplete \(m=6\) material into a rigorous research program rather than an artifact inventory.

### Conclusion

- A short conclusion is needed. The current manuscript moves directly from limitations to disclosures. It should restate exactly what is settled, identify the new reusable mechanism, and separate three open questions: the all-\(m\) upper Loewner conjecture, the optimal lower constants beyond \(m=5\), and the existence of certificate families with bounded word degree.

### References

- The nine existing references appear accurately identified.
- The Israel–Krahmer–Ward DOI is correctly given as `10.1016/j.laa.2015.09.013`.
- Add the sources listed under W3 and explicitly distinguish their formulations.
- For a journal submission, replace bare web URLs where possible with conventional bibliographic metadata and DOI/arXiv identifiers; retain stable repository links for software and preprints.

---

## Missing Key References

1. **W. Albar, M. Junge, and M. Zhao (2017), “Noncommutative versions of the arithmetic-geometric mean inequality,” arXiv:1703.00546.** Directly relevant weakened dimension-free and order formulations; necessary to position the present sharp constant-one Loewner result.
2. **W. Albar, M. Junge, and M. Zhao (2018), “On the symmetrized arithmetic-geometric mean inequality for operators,” arXiv:1803.02435.** Important adjacent symmetrized formulation and nonconstructive obstruction; it must be distinguished from the present ordered-product sum.
3. **C. Yun, S. Sra, and A. Jadbabaie (2021), “Open Problem: Can Single-Shuffle SGD be Better than Reshuffling SGD and GD?”, Proceedings of COLT, PMLR 134:4653–4658.** Essential source of the problem that Peng (2026) resolves.
4. **J. Duchi (2012), commentary on Recht and Ré.** Origin of the norm-inside-the-sum variant, subject to locating a stable bibliographic record.
5. **R. Bhatia and F. Kittaneh (2008), “The matrix arithmetic–geometric mean inequality revisited,” Linear Algebra and its Applications 428(8–9):2177–2191.** Useful broader matrix-AGM lineage for a SIMAX/LAA readership.
6. **R. Alaifari, X. Cheng, L. B. Pierce, and S. Steinerberger (2020), “On Matrix Rearrangement Inequalities,” Proceedings of the American Mathematical Society 148(5).** Adjacent rearrangement/order context.

---

## Questions for Authors

1. Can the authors supply a formal certificate-validation theorem proving that the released orbit encoder and representation test vectors cover every coefficient and every isotypic component for all stable integers \(n\), rather than leaving this as an implementation-level assertion?
2. Can equations (9)–(11) be promoted to a general balanced-certificate continuation theorem, with the scaling, distinguished-letter convention, pole set, and exact specialization at multiples proved once for arbitrary \(m\) and \(b\)?
3. What systematic novelty search was used to exclude an existing all-\(n\) four-factor or restored five-factor result, and how do the authors distinguish the theorem from the Albar–Junge–Zhao, Israel–Krahmer–Ward, and Yun–Sra–Jadbabaie formulations?
4. Will the final archive have an immutable DOI or equivalent identifier that binds the manuscript, exact certificate JSON, verifier source, environment lock, negative controls, and SHA-256 manifest to the same version?

---

## Minor Issues

### Language / Terminology

- Page 2, status table: say "original Recht–Ré spectral-norm inequality" rather than merely "two-sided norm inequality."
- Page 3: define explicitly whether the scalar \(n\) in \(g_n=n-\sum_i x_i\) means \(n\mathbf1\) in the free algebra.
- Pages 4–5: use "hypergeometric continuation functional" outside the integer-multiple regime; reserve "expectation" for \(n=br\).
- Page 6: append stable ranges to decompositions (12) and (13).
- Page 7: specify whether "all-ones kernel" is in the displayed endpoint test-vector coordinates, since the stable scaled kernel in (15) is not the literal all-ones vector.
- Page 9: "matrix-free" and "dimension-free" should not be conflated when describing nearby optimization results.

### Citation and Bibliographic Format

- Add Yun–Sra–Jadbabaie before discussing Peng.
- Credit Duchi for the termwise-norm formulation if a stable source can be located.
- Add full NeurIPS bibliographic metadata for De Sa rather than only the proceedings volume and URL.
- Use a consistent convention for “Ré” in titles and metadata; the PDF metadata currently transliterates it as `Re`.

### Tables and Appendices

- The table on p. 7 labels "upper/lower minors" as \(25/26\); add a footnote explaining why the upper singular block contributes seven rather than eight leading minors.
- Appendix A and B should follow the same data-publication policy.
- Add a small schematic showing the path
  \[
  \text{seed certificate}\to\text{balanced transport}\to
  \text{rational orbit functions}\to\text{isotypic blocks}\to
  \text{positive minors}\to\text{Loewner bound}.
  \]

---

## Dimension Scores

These scores are ordinal assessments against a strong specialist-journal standard; the single major issue W1 controls my recommendation despite the high intrinsic quality.

| Dimension | Score (0–100) | Descriptor | Notes |
|---|---:|---|---|
| Originality (20%) | 91 | Exceptional | Completing \(m=4\) and sharply resolving the \(m=5\) threshold is a major specific advance if validated |
| Methodological Rigor (25%) | 78 | Strong | Exact rational architecture and successful replay; semantic orbit/block bridge needs formalization |
| Evidence Sufficiency (25%) | 77 | Strong | Extensive exact artifacts and a direct rational counterexample; shared-schema risk remains |
| Argument Coherence (15%) | 80 | Strong | Clear theorem architecture; continuation should become an explicit general theorem |
| Writing Quality (15%) | 82 | Strong | Precise and readable, with some notation/range tightening needed |
| Literature Integration | 64 | Adequate | Core sources correct, but several directly adjacent works are absent |
| Significance & Impact | 90 | Exceptional | Potentially closes a prominent matrix-inequality stratum and supplies a reusable exact method |
| **Weighted Average** | **80.8** | **Strong, but Major Revision required** | W1 is a load-bearing publication gate not captured by simple averaging |

---

## Final Recommendation Rationale

I found no concrete counterexample to the theorem statements or algebraic flaw in the human-readable reductions, and the exact standard-library replays passed. The work appears capable of becoming a significant specialist-journal contribution. Nevertheless, a theorem of this scope cannot rely on two implementations that share an insufficiently documented semantic encoder. Acceptance should therefore wait until the manuscript contains a formal, auditable bridge from free words and group actions to the finite certificate arrays, and until the literature positioning is repaired. With those revisions, I would expect the paper to merit serious consideration and likely a favorable re-review.
