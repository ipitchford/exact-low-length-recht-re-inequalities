# Peer Review Report

## Manuscript Information

- **Title**: Exact Recht–Ré Inequalities Through Product Length Five: Uniform rational certificates and a sharp five-factor threshold
- **Manuscript ID**: Pre-publication candidate
- **Review Date**: 30 July 2026
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role

Peer Reviewer 3 (Perspective)

### Reviewer Identity

Stochastic-optimization and random-reshuffling theorist reviewing a computer-assisted matrix-analysis paper from the adjacent applications perspective. My expertise is in finite-sum optimization, sampling with and without replacement, quadratic update operators, and finite-epoch convergence comparisons. I treat the exact free-algebra/SOS implementation as the remit of the methodology and matrix-analysis reviewers; my focus is what the proved operator statements do—and do not—mean for optimization.

### Review Focus

This review audits the bridge between fixed positive-semidefinite matrix products and stochastic optimization: expected iterates versus expected loss, finite prefixes versus complete epochs, random reshuffling versus single shuffling, and instance-wise operator comparisons versus convergence-rate dominance. I also assess the most profitable extensions from the viewpoint of current random-reshuffling theory.

---

## Overall Assessment

### Recommendation

- [ ] **Accept** — Can be published directly, only minor formatting changes needed
- [x] **Minor Revision** — Minor but publication-relevant revisions needed; re-review is desirable but not essential
- [ ] **Major Revision** — Substantial revisions needed, re-review required after revision
- [ ] **Reject** — Not suitable for publication in this journal

### Confidence Score

**4/5 — Mostly within my area of expertise; high confidence in the optimization-facing assessment.**

### Summary Assessment

The manuscript gives exact, executable certificates for the Recht–Ré operator-norm inequality through product length five: the full two-sided four-factor result, the five-factor upper bound for all \(n\geq5\), the five-factor lower bound for \(n\geq6\), and an exact sharp failure at \(m=n=5\). From an optimization perspective, this is a meaningful closure of a matrix-inequality stratum that arose from sampling-without-replacement questions, and the manuscript commendably says on p. 9 (Section 8) that it does not prove a universal advantage for random reshuffling.

The remaining issue is interpretive rather than a defect in the core theorem. The paper never gives the explicit dictionary from \(E_{m,n}\) to a quadratic-gradient update, does not distinguish the norm of the expected iterate from expected squared error, and invokes the contemporary SS–RS–GD result without defining those three operators. Consequently, an optimization reader can see that the authors are cautious but cannot see exactly what has been proved for an algorithm. This is readily repairable. Indeed, the present results yield a clean finite-horizon quadratic corollary, including an exact five-step expected-iterate counterexample after scaling De Sa’s matrices. I recommend minor revision to add this bridge, update the 2026 optimization context, and reprioritize future work toward second-moment and conditioned inequalities.

---

## Strengths

### S1: The manuscript maintains an unusually careful evidence boundary

The abstract’s “Status and evidence boundary” and the reproducibility paragraph on pp. 8–9 explicitly separate exact replay from independent mathematical audit and distinguish certificate verification from historical seed discovery. From the adjacent optimization field, where matrix abstractions are often carried farther than their assumptions warrant, this restraint is a major strength. Section 8 likewise states that the results “do not prove a universal optimization advantage for random reshuffling.”

### S2: The result has a precise finite-horizon interpretation waiting to be stated

The definition of \(E_{m,n}\) on pp. 1–2 is exactly the without-replacement average of an ordered \(m\)-step product. Theorem 2.2 therefore determines the first unresolved short-product strata relevant to fixed linear update maps: four distinct updates for every \(n\geq4\), and five distinct updates for \(n\geq6\), with the diagonal five-step obstruction identified exactly. This is more informative than a bare “the conjecture is false” statement because it locates the first sharp threshold.

### S3: The exact endpoint witness is especially valuable for optimization translation

Section 6.3 (pp. 7–8) gives rational matrices with spectrum \(\{0,1,1,1,2\}\), arithmetic mean \(I\), and a normalized reshuffled-product eigenvalue \(-19/16\). Because the witness is rational and replayed by enumerating all \(5!\) products, it can be converted without numerical ambiguity into a noiseless quadratic-gradient example. This offers a far cleaner applications bridge than the historical numerical SDP alone.

### S4: The paper does not confuse its result with recent conditioned SS–RS–GD work

Section 8 correctly presents Peng’s near-identity RS–GD theorem as a different perturbative result and notes the failure of SS–RS even arbitrarily close to identity. That is an important boundary: the unrestricted five-factor theorem and the conditioned multi-epoch theorem answer different questions. The citation is timely and directly relevant.

### S5: The proof architecture suggests tractable adjacent research questions

The common orbit coordinates, exact affine transversals, fixed symmetry blocks, and rational continuation in Sections 3–5 are not merely a way to certify the current claims. They provide reusable machinery for optimization-relevant variants, especially palindromic products \(P^\ast P\) and condition-number-localized product inequalities.

---

## Weaknesses

### W1: The optimization meaning of the main theorem is not stated mathematically

**Problem**: The introduction says the inequality is “motivated by the comparison of with- and without-replacement iterations in stochastic optimization” (p. 2, Section 1), while Section 8 says it does not prove a universal reshuffling advantage. The manuscript never fills the gap between those two sentences. In particular, it does not define a quadratic update \(B_i=I-\eta H_i\), the without-replacement operator
\[
R_{\mathrm{wo}}^{(m)}=\frac{1}{(n)_m}E_{m,n}(B),
\]
or its with-replacement counterpart
\[
R_{\mathrm{wr}}^{(m)}=\left(\frac1n\sum_{i=1}^n B_i\right)^m.
\]

**Why it matters**: Without this dictionary, readers may incorrectly infer an expected-loss or convergence-rate theorem. The proved norm inequality controls
\[
\sup_{\|x_0\|=1}\bigl\|\mathbb E[x_m]\bigr\|
=\|R^{(m)}\|,
\]
for a fixed linear/noiseless update model. It does **not** by itself control \(\mathbb E\|x_m\|\), \(\mathbb E\|x_m\|^2\), or expected objective suboptimality.

**Suggestion**: Add a short subsection after Theorem 2.2 entitled, for example, “Finite-horizon quadratic interpretation.” For common-minimizer quadratics \(f_i(x)=\tfrac12x^\top H_i x\) with \(0\preceq \eta H_i\preceq I\), define \(B_i=I-\eta H_i\). State a corollary that the worst-case norm of the expected iterate after four without-replacement steps is no larger than under four with-replacement steps for every \(n\geq4\), and that the analogous five-step statement holds for \(n\geq6\). Explicitly state that this is an expected-iterate/bias comparison, not a mean-square-risk comparison.

**Severity**: Major for the cross-disciplinary interpretation, but readily correctable without changing the core proof.

### W2: The paper omits a strong exact optimization corollary already contained in the five-factor witness

**Problem**: Section 6.3 stops at the matrix inequality. Let \(C_i=A_i/2\) for the exact De Sa matrices. Then \(0\preceq C_i\preceq I\), \(\frac15\sum_iC_i=I/2\), and
\[
\left\|\frac1{120}E_{5,5}(C)\right\|=\frac{19}{512}
>\frac{16}{512}
=\left\|\left(\frac15\sum_iC_i\right)^5\right\|.
\]
Taking \(H_i=I-C_i\succeq0\) and \(f_i(x)=\tfrac12x^\top H_i x\), a unit-stepsize gradient update is exactly \(x\leftarrow C_i x\).

**Why it matters**: This gives a concise, fully exact, ordinary noiseless-quadratic statement: after one five-sample epoch, the worst-case norm of the expected iterate under random reshuffling can exceed that under with-replacement sampling. It explains the practical mathematical content of the sharp \(m=n=5\) obstruction without invoking a nonlinear or heavily engineered learning problem. It also makes clear why this does not contradict near-identity theorems: the \(C_i\) are contractions but singular, hence far from the well-conditioned regime.

**Suggestion**: Add this as a formal corollary immediately after Section 6.3, with the two exact constants \(19/512\) and \(1/32=16/512\). Describe it as an expected-iterate comparison only. This is the highest-value immediate extension available from the existing result.

**Severity**: Major opportunity for significance; omission does not invalidate the theorem.

### W3: SS, RS, and GD are invoked without defining the operators or the epoch structure

**Problem**: Section 8 (p. 9) refers to “RS–GD” and “SS–RS” but never defines them. It also does not explain that the present \(m\)-factor operator is a within-epoch prefix when \(m<n\), a full epoch only when \(m=n\), and that \(K\) independent reshuffles yield a power of the averaged epoch operator. By contrast, single shuffling averages powers of a single-permutation operator and is therefore a different object.

**Why it matters**: These distinctions are the entire substance of the modern SS–RS–GD question. A reader could mistakenly think the four- and five-factor theorem compares single shuffle with random reshuffling, or that it directly covers multiple epochs.

**Suggestion**: Add a compact operator dictionary:
\[
P_\sigma=B_{\sigma(n)}\cdots B_{\sigma(1)},\qquad
R=\mathbb E_\sigma P_\sigma,\qquad
W_{\rm RS}=R^K,\qquad
W_{\rm SS}=\mathbb E_\sigma P_\sigma^K,\qquad
W_{\rm GD}=G^{nK},
\]
with \(G=n^{-1}\sum_iB_i\), noting the harmless product-order convention because all permutations are averaged. Then say explicitly: this paper determines \(R\) for product lengths four and five in the unrestricted PSD class; it does not compare \(W_{\rm SS}\) and \(W_{\rm RS}\).

**Severity**: Major expository issue.

### W4: The 2026 optimization context is incomplete

**Problem**: The manuscript cites Peng’s June 2026 preprint but not Liu’s COLT 2026 paper, “Random Reshuffling Dominates Stochastic Gradient Descent,” which proves a convergence-rate dominance result for smooth convex finite sums under reasonable stepsizes after any finite number of epochs. The latter is a different notion of “dominates” from an instance-wise fixed-product operator inequality and uses averaged-iterate/Bregman analysis rather than the Recht–Ré route.

**Why it matters**: A paper dated 30 July 2026 that motivates itself through random reshuffling should tell readers that modern algorithmic theory can establish broad rate advantages even though the unrestricted Recht–Ré operator inequality fails. This prevents the matrix result from being misread as either necessary or sufficient for the current best convergence theory.

**Suggestion**: Add one paragraph contrasting:

1. the present exact fixed-operator, finite-product result;
2. Peng’s conditioned expected-iterate RS–GD operator ordering and SS–RS counterexample;
3. Liu’s smooth-convex convergence-rate dominance for RR versus standard SGD.

The paragraph should emphasize that these statements use different assumptions, algorithms, and performance metrics and therefore are compatible.

**Severity**: Minor to major, depending on the target venue; for a strong interdisciplinary presentation, it should be addressed.

### W5: The stated research frontier is algebraically natural but not the most profitable optimization extension

**Problem**: Section 8 devotes most future-facing attention to incomplete six-factor artifacts. From the optimization perspective, a raw unrestricted \(m=6\) continuation is less consequential than resolving the second-moment operator that controls expected squared error. For \(P=B_{i_m}\cdots B_{i_1}\),
\[
\mathbb E\|Px_0\|^2=x_0^\top\mathbb E[P^\ast P]x_0,
\]
and \(\mathbb E[P^\ast P]\) is not controlled by \(\|\mathbb E P\|\).

**Why it matters**: Mean-square error and expected objective suboptimality are standard optimization metrics. The original Recht–Ré program included a palindromic/second-moment inequality precisely for this reason, and De Sa showed that its unrestricted full-epoch version also eventually fails. Determining its exact status at short lengths, or under conditioning, would connect the certificate machinery to a substantially more important algorithmic quantity.

**Suggestion**: Reframe the future-work hierarchy as:

1. **Immediate**: state the exact finite-horizon expected-iterate corollary already implied by the paper.
2. **Primary new research target**: adapt the orbit/SOS architecture to the palindromic polynomial \(\mathbb E[P^\ast P]\) for \(m=4\) and \(m=5\), seeking exact positive cases, counterexamples, and sharp thresholds.
3. **Conditioned frontier**: if the unrestricted second-moment inequality fails, determine the largest \(\delta_{m,n}\) for which it holds under \((1-\delta)I\preceq B_i\preceq I\), and compare this with Peng’s sufficient \(1/(4n^2+1)\) radius for RS–GD.
4. **Only then**: pursue unrestricted \(m=6\), unless the missing artifacts can be reconstructed cheaply.

**Severity**: Minor for the present theorem, major for maximizing future significance.

---

## Detailed Comments

### Title & Abstract

- The title is accurate and appropriately mathematical. It does not promise an SGD theorem.
- The first sentence of the abstract responsibly says “motivated by comparisons,” but the abstract would be stronger if it named the exact algorithmic object: the spectral norm of the **expected fixed-matrix product**.
- The status paragraph is exemplary. Consider adding one sentence: “The resulting operator comparison concerns the norm of the expected iterate in a fixed linear update model, not expected loss or mean-square error.”

### Introduction

- Section 1 (p. 2) clearly separates the Israel–Krahmer–Ward expectation-of-norms result from the norm-of-average/Loewner statement. The same care should be applied to optimization metrics.
- The status table is useful, but “two-sided norm inequality” should be linked immediately to the without-/with-replacement operator definitions.
- The current introduction gives historical motivation but not a contemporary optimization map. A four- or five-line quadratic-update corollary would materially broaden accessibility without turning the manuscript into an optimization paper.

### Literature Review / Theoretical Framework

- The core matrix-analysis lineage is outside this reviewer’s remit, but the adjacent optimization framing needs at least Yun–Sra–Jadbabaie (2021) and Liu (2026) in addition to Recht–Ré, De Sa, and Peng.
- De Sa (2020) is especially relevant not only for the explicit first-moment witness reproduced here, but also because it distinguishes the first operator inequality, the palindromic second-moment inequality, and a norm-after-summing variant. That taxonomy would help the paper identify exactly which branch it settles.
- The manuscript should avoid the phrase “RS–GD comparison” standing alone: Peng compares expected-iterate operators for a quadratic finite sum under a near-identity matrix condition; Liu compares convergence-rate guarantees for RR and standard SGD under smooth convex assumptions. These are different comparisons.

### Methodology / Research Design

- I do not reassess the exact SOS implementation. From the applications side, the main methodological request is to derive the optimization corollary algebraically rather than rely on prose analogy.
- No experiment is required. The contribution is exact and theoretical. If the authors add the proposed quadratic corollary, the existing rational replay is stronger evidence than a numerical SGD plot would be.
- A useful follow-up computation would be an automated conversion of a matrix witness \(C_i\) into quadratic Hessians \(H_i=I-C_i\), followed by exact verification of the corresponding expected-iterate operators. This should remain a corollary checker, not a new theorem acceptance path.

### Results / Findings

- Theorem 2.2 is cleanly stated. Its immediate optimization translation is:
  - four-step expected-iterate operator comparison for all \(n\geq4\);
  - five-step comparison for all \(n\geq6\);
  - exact five-step diagonal failure at \(n=5\).
- At \(m<n\), the sampling scheme is a prefix of a without-replacement epoch, or equivalently a scheme that resets the pool after every \(m\) draws. It is not yet a statement about the endpoint of a full \(n\)-sample epoch.
- At \(m=n=5\), the exact witness does give a one-epoch result. Scaling by \(1/2\) makes the matrices bona fide PSD contraction updates and yields the constants \(19/512\) versus \(16/512\).
- The theorem does not determine expected squared error because \(\mathbb E[P^\ast P]\neq(\mathbb EP)^\ast(\mathbb EP)\) in general.

### Discussion

- Section 8 contains the right caution but too little explanation. The manuscript would benefit from a three-level boundary:
  1. **Proved here**: a universal spectral-norm inequality for an averaged fixed product.
  2. **Immediate corollary**: worst-case norm of the expected iterate for noiseless quadratic/shared-minimizer linear updates.
  3. **Not proved**: expected squared error, expected loss, nonlinear SGD trajectories, minibatching, momentum/adaptive methods, or a universal practical ordering of sampling schemes.
- The practical implication is not “use random reshuffling for four or five steps.” Rather, the result gives an exact benchmark for a specific bias operator and locates the first unrestricted obstruction.
- The discussion should mention that modern RR guarantees often exploit cancellation of gradient errors, co-coercivity, variance at the optimum, or trajectory-level arguments. Those mechanisms are invisible to a static product-mean inequality.

### Conclusion

- There is no separate conclusion section; Section 8 serves that role. A short concluding paragraph would help state the delta in one sentence: the unrestricted expected-product comparison is completely determined through length five, but the optimization-relevant second-moment and conditioned frontiers remain open.
- The most significant next project is not simply to complete the \(m=6\) files. It is to determine the short-length and conditioned status of \(\mathbb E[P^\ast P]\), using the present machinery.

### References

The following primary references would strengthen the cross-disciplinary bridge:

1. **Recht and Ré (2012)**, [PMLR 23](https://proceedings.mlr.press/v23/recht12.html): gives the least-mean-squares/Kaczmarz motivation and, importantly, distinguishes the averaged product from the reversed-product second moment needed for squared risk.
2. **De Sa (2020)**, [NeurIPS 33](https://proceedings.neurips.cc/paper/2020/hash/42299f06ee419aa5d9d07798b56779e2-Abstract.html): supplies explicit counterexamples to both first- and second-moment conjectures and discusses the role of step size and algorithmic performance.
3. **Yun, Sra, and Jadbabaie (2021)**, [COLT, PMLR 134](https://proceedings.mlr.press/v134/open-problem-yun21a.html): defines the SS–RS–GD expected-iterate operators and motivates conditioning as the optimization-relevant restriction.
4. **Peng (2026)**, [arXiv:2607.22620](https://arxiv.org/abs/2607.22620): resolves the conditioned SS–RS–GD conjecture by refuting SS–RS near identity and proving a sufficient RS–GD radius. Already cited, but its operators should be defined in the manuscript.
5. **Liu (2026)**, [COLT, PMLR 336](https://proceedings.mlr.press/v336/liu26d.html): proves convergence-rate dominance of RR over standard SGD for smooth convex finite sums under reasonable stepsizes and finite epoch counts, illustrating a modern route that does not require the unrestricted Recht–Ré inequality.

Haochen and Sra (2019), Mishchenko, Khaled, and Richtárik (2020), and Ahn, Yun, and Sra (2020) are also useful for broader rate context, but the five references above are sufficient for the specific bridge requested here.

---

## Assumption Audit

### Explicit Assumptions

- The \(A_i\) are fixed PSD Hermitian matrices of arbitrary common dimension.
- Their sum satisfies \(\sum_iA_i\preceq nI\) after homogeneous normalization.
- The parameter \(n\) is an integer in the operator theorem, even though positivity of the reduced blocks is continued over real \(n\) in the stable range.
- The theorem concerns a spectral norm/Loewner-order statement for an averaged ordered product.

These assumptions are mathematically clear and appropriate.

### Implicit Assumptions

1. **A fixed product is a faithful SGD model**: This is exact for common-minimizer quadratics with fixed Hessians and is a local linearization elsewhere. It is not exact for a general nonlinear finite sum because the Hessian/update map changes with the iterate.
2. **The norm of the expected iterate is a convergence metric**: It is a legitimate bias metric, especially for parallel averaging or expected dynamics, but it is not expected distance, expected squared distance, or expected loss.
3. **A short product corresponds to an epoch**: Only when \(m=n\). For \(m<n\), it is a prefix or a reset-after-\(m\)-samples scheme.
4. **Repeated epochs preserve the same comparison**: For independent reshuffling of a fixed linear system, the averaged epoch operator is powered across epochs; this is not true for single shuffling, and nonlinear trajectories do not reduce so simply.

### Paradigmatic Assumptions

The matrix-inequality paradigm looks for a universal instance-wise operator ordering. Modern stochastic-optimization theory often asks a different question: whether one algorithm’s worst-case rate bound dominates another’s under smoothness/convexity assumptions. A universal matrix inequality may fail while a rate theorem remains true because rate analyses exploit co-coercivity, gradient-noise cancellation, averaging, or step-size schedules. The paper should make this paradigm distinction explicit.

---

## Cross-Disciplinary Connections

### Parallel Research

- **Finite-horizon expected dynamics**: The present \(E_{m,n}\) directly describes the expected bias operator for linear updates under a without-replacement prefix.
- **Second-moment dynamics**: Expected squared error is governed by the lifted/palindromic operator \(\mathbb E[P^\ast P]\), often expressible through Kronecker lifts. This is the closest unanswered neighbor to the current theorem.
- **Conditioned SS–RS–GD inequalities**: Near-identity constraints model small stepsizes and well-conditioned quadratic updates; Peng’s result shows that conditioning can restore RS–GD even when unrestricted PSD results fail.
- **Trajectory-level RR theory**: Liu’s 2026 result and earlier finite-epoch analyses obtain RR advantages through convex-analysis tools rather than a universal product ordering.

### Borrowing Opportunities

- Borrow the optimization taxonomy of **bias**, **variance/second moment**, and **objective suboptimality** to label the matrix quantities.
- Use **Kronecker lifting** to encode \(P^\ast P\) as a product acting on a tensor space, then exploit the manuscript’s symmetry machinery there.
- Introduce a **conditioning radius** \(\delta_{m,n}\) and search for exact or certified lower bounds under \((1-\delta)I\preceq B_i\preceq I\).
- Compare an unrestricted sharp threshold in \(m,n\) with a conditioned threshold in \(\delta\); the latter is more likely to inform step-size regimes.

### Methodological Borrowing

The most promising hybrid method is a two-stage exact search:

1. numerically explore symmetry-reduced palindromic/conditioned SOS programs to locate feasible regimes or counterexamples;
2. rationalize only the resulting seeds and certify them with the same exact independent arithmetic paths used here.

For counterexamples, convert any certified contraction matrices directly into quadratic Hessians \(H_i=I-B_i\) and verify the algorithmic operator identity exactly.

---

## Practical Impact

### Real-World Application

The current theorem should not be presented as a practical algorithm-selection rule. Its strongest applied value is foundational: it identifies precisely where a once-influential universal expected-product heuristic holds and fails. It also supplies exact benchmark instances for testing analyses of data-ordering effects.

### Implementation Feasibility

The exact replay is practical for researchers auditing the theorem. Translating the result into an SGD experiment is unnecessary and could obscure the exact claim. A formal quadratic corollary and a small exact checker are sufficient.

### Stakeholders

- Matrix analysts gain resolved low-length cases and a reusable symmetry/SOS architecture.
- Optimization theorists gain exact finite-horizon bias operators and a sharp boundary example.
- Researchers in randomized Kaczmarz and incremental methods gain a precise warning about which performance metric is being ordered.
- Practitioners should not infer that four- or five-sample reshuffling is universally superior in loss or wall-clock time.

---

## Broader Implications

### Ethical Dimensions

There are no material human-subject, privacy, or fairness issues. The AI-use disclosure on p. 9 is appropriately explicit. The more relevant research-integrity issue is semantic overreach from exact computation to algorithmic claims; the manuscript already shows good instincts and needs only a more precise optimization dictionary.

### Social Impact

The social impact is indirect. More reliable distinctions between mathematical operator claims and practical optimizer performance reduce the risk of overstated algorithmic recommendations. The reproducible AI-assisted proof workflow may also be valuable as a model for auditable computer-assisted mathematics.

### Future Directions

The highest-value program is an **exact finite-horizon bias-and-risk hierarchy**:

1. publish the immediate quadratic expected-iterate corollary of the current theorem;
2. determine the palindromic second-moment inequality through lengths four and five;
3. if unrestricted positivity fails, compute sharp or certified conditioning radii;
4. connect those radii to stepsize/Hessian spectra and the RS–GD regime;
5. pursue \(m=6\) only where it advances this hierarchy or can be completed with modest additional reconstruction.

---

## Questions for Authors

1. Will the authors state the exact noiseless-quadratic corollary \(B_i=I-\eta H_i\), explicitly identifying the controlled metric as \(\sup_{\|x_0\|=1}\|\mathbb E x_m\|\) rather than \(\mathbb E\|x_m\|^2\)?
2. Can the authors add the scaled De Sa corollary \(C_i=A_i/2\), yielding the exact one-epoch comparison \(19/512>1/32\) for gradient updates with Hessians \(H_i=I-C_i\)?
3. How do the authors intend readers to relate their \(m\)-prefix operator to \(W_{\rm RS}=R^K\), \(W_{\rm SS}=\mathbb E[P_\sigma^K]\), and \(W_{\rm GD}=G^{nK}\)? A formal operator dictionary would resolve this.
4. Would the current orbit/SOS codebase support a degree-\(2m\) palindromic target \(\mathbb E[P^\ast P]\), perhaps first at \(m=4\), and is that a more informative priority than reconstructing the incomplete unrestricted \(m=6\) data?

---

## Minor Issues

### Language / Grammar

- Section 8, p. 9: define “SS,” “RS,” and “GD” at first use.
- Prefer “random reshuffling (RR)” consistently; “RS” follows the Yun–Sra–Jadbabaie notation but can be confused with “random sampling.”
- In the abstract, “comparisons between sampling with and without replacement” could be sharpened to “comparisons of averaged fixed-matrix products arising in sampling with and without replacement.”

### Citation Format

- Add Yun–Sra–Jadbabaie (2021) and Liu (2026).
- When citing Peng (2026), label it explicitly as an arXiv preprint and state the operator assumptions in the prose.

### Figures and Tables

- No additional figure is needed.
- A one-row-per-object table mapping \(E_{m,n}\), \(R\), \(W_{\rm RS}\), \(W_{\rm SS}\), \(W_{\rm GD}\), and \(\mathbb E[P^\ast P]\) to the associated sampling scheme and performance metric would be more useful than a diagram.

### Layout

- Section 8 combines limitations, current optimization context, and the \(m=6\) artifact audit. Consider short subheadings: “Optimization interpretation,” “Evidence limitations,” and “Six-factor frontier.”

---

## Dimension Scores

These uncalibrated rubric scores are ordinal indicators relative to a strong specialist venue, not acceptance probabilities.

| Dimension | Score (0–100) | Descriptor | Notes |
|---|---:|---|---|
| Originality (20%) | 87 | Strong | Exact all-\(n\) closure through length five and sharp five-factor threshold are clear advances. |
| Methodological Rigor (25%) | 84 | Strong | Exact certificate architecture and replay are unusually substantial; core-method audit is delegated to the methodology reviewer. |
| Evidence Sufficiency (25%) | 76 | Strong/Adequate boundary | Sufficient for the matrix theorem, but the optimization interpretation is asserted only informally and lacks the readily derivable corollary. |
| Argument Coherence (15%) | 72 | Adequate | The mathematical argument is coherent; the motivation-to-limitation bridge is incomplete. |
| Writing Quality (15%) | 78 | Strong | Precise technical prose overall; adjacent-field terminology is underdefined. |
| Literature Integration (optional) | 72 | Adequate | Good matrix lineage and timely Peng citation, but missing key operator definitions and the COLT 2026 rate result. |
| Significance & Impact (optional) | 78 | Strong | High foundational value; impact would increase materially with the exact quadratic corollary and a risk-oriented frontier. |
| **Weighted Average** | **79.9** | **Minor Revision** | Correctable interpretive gaps prevent an as-is recommendation despite a strong core result. |

---

## Highest-Value Research Extension

The most profitable extension is **not a standalone brute-force \(m=6\) continuation**. It is a certified hierarchy connecting the current expected-product theorem to actual optimization metrics:

1. **Complete now**: state and exactly verify the finite-horizon quadratic expected-iterate corollary, including the scaled five-matrix witness with \(19/512>16/512\).
2. **New theorem target**: determine the short-length status of the palindromic second-moment inequality
   \[
   \mathbb E_{\rm wo}[P^\ast P]\preceq_{\|\cdot\|}
   \mathbb E_{\rm wr}[P^\ast P]
   \]
   for \(m=4\) and \(m=5\), because this governs worst-case expected squared error.
3. **If unrestricted positivity fails**: determine the sharp or best certified \(\delta_{m,n}\) under \((1-\delta)I\preceq B_i\preceq I\), directly linking the result to stepsize and conditioning and creating a quantitative bridge to Peng’s RS–GD theorem.

This program uses the paper’s strongest technical asset—the symmetry-reduced exact SOS machinery—on the quantity that stochastic-optimization readers most need.
