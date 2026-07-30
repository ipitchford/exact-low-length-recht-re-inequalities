# Peer Review Report

## Manuscript Information

- **Title**: Exact Recht–Ré Inequalities Through Product Length Five: Uniform Rational Certificates and a Sharp Five-Factor Threshold
- **Manuscript ID**: Pre-publication candidate; no journal ID assigned
- **Review Date**: 30 July 2026
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role

Editor-in-Chief

### Reviewer Identity

Simulated Editor-in-Chief for a strong specialist matrix-analysis venue, calibrated principally to the *SIAM Journal on Matrix Analysis and Applications* (SIMAX). My editorial expertise is in matrix analysis, applied and numerical linear algebra, and the assessment of exact computer-assisted proofs; the detailed free-algebra and representation-theoretic encoding should additionally be checked by specialist referees. The manuscript is anonymous, so a conventional author-level conflict-of-interest check is not possible at this stage.

### Review Focus

This report assesses journal fit, originality, significance, literature positioning, structural coherence, presentation, and the suitability of the manuscript's claim–evidence boundary. I treat successful exact replay as strong candidate evidence, not as peer review or independent mathematical verification.

---

## Overall Assessment

### Recommendation

- [ ] **Accept** — Can be published directly, only minor formatting changes needed
- [ ] **Minor Revision** — Minor revisions needed, no re-review after revision
- [x] **Major Revision** — Substantial revisions needed, re-review required after revision
- [ ] **Reject** — Not suitable for publication in this journal

### Confidence Score

**4/5 — High confidence.** The central topic and editorial fit are within my expertise. I defer to specialist referees on the completeness of the particular orbit encodings, representation vectors, and free-localizer implementation.

### Summary Assessment

The manuscript gives a unified exact computer-assisted treatment of the Recht–Ré inequality through product length five. It claims the full two-sided four-factor result for every \(n\geq4\), the five-factor upper bound for every \(n\geq5\), the five-factor lower bound for every \(n\geq6\), and sharpness through De Sa's rational \(m=n=5\) counterexample. The mathematical contribution is potentially substantial: it closes the four-factor stratum left open by Lai and Lim and identifies a sharp restoration threshold at five factors. The presentation is compact, coherent, and unusually candid about the limits of executable evidence. The common free-localizer, balanced-block continuation, symmetry reduction, and exact positivity architecture is an attractive unification.

The main obstacle is not the arithmetic precision of the package; it is whether the manuscript exposes enough of the semantic bridge from the universal matrix inequality to the finite machine-checked objects for a specialist reader to audit the proof independently. The paper itself acknowledges this gap on p. 9. In addition, priority positioning is too narrow, and the supplementary package is not yet a permanent, licensed, citable research object with accountable human authorship. I therefore recommend Major Revision rather than rejection: the result appears highly promising, but the proof interface and publication record require substantial completion before a journal can responsibly treat the claims as established.

---

## Strengths

### S1: A potentially important and sharply formulated matrix-analysis result

Theorem 2.2 on pp. 2–3 states a clean exact classification through product length five. In particular, the paper does more than report isolated feasible certificates: it gives an all-\(n\) four-factor theorem, an all-\(n\) five-factor upper theorem, and a sharp lower threshold. The exact eigenvalue \(-285/2<-120\) for the rational \(m=n=5\) family in Section 6.3 (pp. 7–8) gives the five-factor boundary a particularly convincing and memorable form.

### S2: A genuinely unified proof architecture

Sections 3–6 (pp. 3–8) organize both product lengths around the same degree-two free-localizer, the same 59 stabilizer and 22 full-symmetry orbit coordinates, the same affine transversals, and fixed multiplicity blocks of sizes \(8,6,1,1\) and \(4,4,1,1\). This is more conceptually valuable than presenting two unrelated computer certificates. The balanced-block continuation in Section 4 and the fixed representation decomposition in Section 5 make a plausible reusable method visible.

### S3: Exemplary calibration of the evidence boundary

The boxed statement on p. 1 and the reproducibility boundary on p. 9 explicitly distinguish exact replay, shared-schema redundancy, derivation cross-checks, independent audit, and peer review. Section 8 also avoids turning a matrix inequality result into an unjustified universal claim about random reshuffling. This is excellent scientific practice and should be preserved in the revision.

### S4: Strong exact-reproducibility design

Section 7 (pp. 8–9) enumerates exact replay obligations rather than merely saying that “code is available.” The accompanying read-only package contains two arithmetic implementations per product length, seed-to-family derivations, exact endpoint checks, manifests, pinned dependencies, and mutation controls that fail closed under both ordinary and optimized Python. This is materially stronger than a floating-point SDP transcript and is well aligned with SIMAX's interest in reproducible computational work.

### S5: Concise and readable integration of proof, computation, and limitations

The 15-page paper has a clear progression from normalization and the main theorem to the common certificate architecture, continuation, positivity, endpoints, replay, and limitations. The status table on p. 2 and the replay-obligation table on p. 9 orient the reader effectively. The typography is clean, and the main narrative is not overwhelmed by the large certificate data.

---

## Weaknesses

### W1: The load-bearing theorem-to-certificate interface is not yet sufficiently self-contained

**Problem**: Section 3.1 (p. 4) says that the concrete orbit maps and test vectors are part of the released certificates, while Section 5 (pp. 6–7) moves from representation decompositions and multiplicity counts to positivity of reconstructed blocks without defining the actual symmetry-adapted vectors or proving that the encoded orbit equations exhaust all free monomials. Section 7 then correctly concedes that exact replay does not by itself establish that the encoded coefficient patterns and representation test vectors cover the intended mathematical objects (p. 9).

**Why it matters**: This is the central logical hinge of a computer-assisted proof. Exact arithmetic can prove that a finite encoding is internally consistent while still checking the wrong orbit map, omitting an isotypic component, or using incorrectly normalized test vectors. A specialist journal needs a reader-auditable argument that the finite objects checked by the programs are equivalent to the universal operator statement.

**Suggestion**: Add a formal “verification specification” section or appendix that (i) defines the canonical word-pattern and orbit maps; (ii) constructs and normalizes the symmetry-adapted vectors; (iii) proves that they span every required isotypic component, including the small-\(n\) endpoint changes; (iv) states a finite verification theorem listing the exact machine obligations whose satisfaction implies Proposition 3.1 and Theorem 2.2; and (v) works through at least one representative coefficient identity and one nontrivial block from raw orbit data to determinant positivity. Pseudocode may accompany, but should not replace, the mathematical completeness argument.

**Severity**: Major

### W2: The replication object is not yet publication-stable or citable

**Problem**: Section 9 (p. 10) says that the code and data “accompany this manuscript,” but neither the paper nor the package currently supplies a public permanent URL or DOI, a final release identifier, a distribution license, or a top-level immutable hash tied to the manuscript. The package also contains inherited Linux replay receipts while the consolidation documentation reports a fresh macOS environment; the provenance is explainable but not yet presented as one final archival receipt.

**Why it matters**: The result depends materially on external machine-readable certificates. If those data cannot be cited and retrieved in an immutable form, the published proof is not durably auditable. This also prevents a credible request for the SIMAX reproducibility badge.

**Suggestion**: Deposit a frozen release in a DOI-bearing archive such as Zenodo and, if a public Git repository is used, also preserve the exact submitted snapshot. Add a software/data citation, license, commit or release tag, whole-package SHA-256 manifest, final clean-environment replay receipt, and explicit mapping from each theorem clause to the archived files. Distinguish inherited source receipts from the final consolidation replay. State whether all badge-relevant parameters and negative controls are included.

**Severity**: Major

### W3: Literature positioning and priority support are too narrow for the size of the claim

**Problem**: The background on p. 2 is lucid but the paper has only nine references. It does not discuss nearby noncommutative AGM variants such as the work of Albar, Junge, and Zhao, nor the subsequent SS–RS–GD matrix-inequality formulation of Yun, Sra, and Jadbabaie. More recent random-reshuffling analyses are mentioned only through one 2026 preprint. The phrase “remaining cases through product length five” therefore rests on a narrow documented search.

**Why it matters**: The paper's editorial significance depends on being the first exact resolution of the stated four- and five-factor strata and on clearly distinguishing this Loewner/norm formulation from related symmetrized, termwise-norm, conditioned, and optimization-specific inequalities. An incomplete related-work section makes both novelty and readership relevance difficult to assess.

**Suggestion**: Add a dedicated related-work subsection organized by inequality type and logical implication. Include the closest noncommutative AGM variants and post-2020 random-reshuffling formulations, state exactly why none proves the present theorem, and document a refreshed priority search through the submission date. Avoid a categorical first-priority claim unless the search supports it.

**Severity**: Major

### W4: The applied significance for SIMAX readers needs a clearer, carefully bounded account

**Problem**: The abstract and Section 1 motivate the problem through sampling without replacement, while Section 8 correctly explains that the theorem does not establish a universal optimization advantage. What remains underdeveloped is the positive “so what?” statement: beyond closing two strata, what structural lesson does the sharp \(m=5\) threshold provide for matrix analysis or stochastic-iteration theory?

**Why it matters**: SIMAX explicitly welcomes theoretical work with potential impact on applications. The manuscript fits matrix theory, but the application-facing value is presently mostly historical motivation plus a limitation.

**Suggestion**: Add a short discussion that distinguishes direct consequences from research implications. Explain how the four-factor validity and five-factor restoration constrain finite-epoch product comparisons, what the counterexample teaches about lower versus upper Loewner behavior, and why the common certificate architecture may be useful for other symmetrized noncommutative inequalities. Preserve the present caution against claiming an unconditional algorithmic ordering.

**Severity**: Minor

### W5: Accountable authorship and required submission declarations are unresolved

**Problem**: Section 9 (p. 10) states that accountable human authors “must” review and accept the manuscript before submission; authorship, CRediT roles, funding, competing interests, affiliation, contact information, and the license remain unresolved. Anonymous display is compatible with a blinded manuscript, but absence of an accountable author in the submission record is not.

**Why it matters**: This is a non-negotiable publication-integrity condition. A journal cannot submit AI systems to authorship obligations or accept a manuscript for which no human accepts responsibility for the claims and released code.

**Suggestion**: Before submission, identify the accountable human author or authors, obtain documented approval of the theorem, proof text, code, data, and AI-use disclosure, and complete all journal declarations. Retain the transparent AI-contribution statement, but adapt it to the target journal's policy and the work actually reviewed by the human authors.

**Severity**: Critical administrative gate

---

## Detailed Comments

### Journal Fit

- The topic falls within SIMAX's stated remit of matrix theory, analysis, applications, and computation, including theoretical work with potential impact on applications. The result is also relevant to readers interested in noncommutative inequalities, positive semidefinite matrices, and exact computational linear algebra.
- The exact certificate package is a positive fit with SIMAX's reproducibility initiative, provided it is placed in a permanent public or journal-hosted archive and fully documented.
- The principal fit risk is that the manuscript currently reads partly as a free-algebra/SOS certificate report and only briefly articulates its matrix-analysis and applied-linear-algebra implications. If that connection is not strengthened, *Linear Algebra and its Applications* may be an equally or more natural venue.
- **First-impression score**: 8/10. The theorem and sharp threshold immediately attract attention; the unresolved proof interface prevents a higher editorial readiness score.

### Originality

- Subject to a refreshed priority check, the all-\(n\) four-factor theorem and the exact five-factor restoration/sharpness result constitute a clear, nonincremental advance over the status described by Lai and Lim.
- The common certificate architecture is itself a secondary methodological contribution. The manuscript should state whether this unification is new to the present work or merely an exposition of two independently found certificates.
- The paper should separate three originality claims: the theorem, the uniform balanced-block/SOS method, and the hardened executable verification package.

### Significance

- Closing a named open four-factor case and determining an exact five-factor threshold is significant within this specialized line of matrix inequalities.
- The result is likely to be of strong subfield interest rather than broad discipline-wide impact unless the revised discussion shows transferable consequences of the certificate architecture.
- De Sa's explicit rational counterexample materially improves the story because the sharpness boundary no longer depends on unreplayed numerical SDP/Farkas evidence.

### Structural Coherence

- The sequence of Sections 2–7 is strong: theorem, certificate language, continuation, positivity, endpoints, replay.
- The paper lacks a conventional conclusion. Section 8 is a limitations/frontier section and Section 9 consists of disclosures. Add a concise conclusion before the disclosures that restates the mathematical delta, the sharp boundary, and the next mathematically justified questions.
- Appendix A prints all four-factor free functions, whereas Appendix B prints five-factor seed and endpoint transversals rather than the corresponding parametric functions. Explain this asymmetry and state an explicit principle for what must appear in print versus the executable supplement.
- Consider moving most of the incomplete \(m=6\) inventory from Section 8 to supplementary provenance. A brief frontier paragraph is useful, but detailed counts of missing exploratory files are not part of the proved result.

### Title & Abstract

- The title is accurate and appropriately specific. “Exact computer-assisted Recht–Ré inequalities…” would make the proof mode explicit at first sight, although the current subtitle and abstract already do so.
- The abstract states all theorem thresholds and the principal certificate mechanism. A source-level count places it at approximately 249 words, effectively at SIMAX's 250-word ceiling; trim it to leave a safe formatting margin.
- The many certificate counts demonstrate exactness but crowd the abstract. One sentence could instead foreground the conceptual contribution and move some counts to the main text.
- Keywords and Mathematics Subject Classification codes are absent and are required for a SIMAX submission.

### Introduction

- The exact-status table on p. 2 is highly effective.
- The distinction between termwise/expectation-of-norms results and the present norm-of-average/Loewner statement is important and well made.
- The introduction should end with a numbered contributions paragraph and a clearer roadmap separating the human argument from the machine-verification layer.

### Literature Review / Theoretical Framework

- The core lineage—Recht and Ré, Lai and Lim, Zhang, free Positivstellensatz, symmetry reduction, and rational SOS reconstruction—is present.
- The theoretical framework would benefit from a short diagram or table distinguishing: original Recht–Ré norm inequality, its normalized two-sided Loewner form, related symmetrized AGM inequalities, termwise-norm inequalities, and conditioned optimization comparisons.
- Add and discuss the closest omitted literature rather than merely increasing the bibliography count.

### Methodology / Research Design

- Exact rational arithmetic and avoidance of floating-point acceptance tolerances are appropriate for the claim.
- The two implementations provide useful redundancy, but the paper correctly states that they share schema and proof architecture. Do not relabel them “independent verifiers” without qualification.
- The revised paper should explicitly state which obligations were independently re-derived and which are shared. A small independence matrix would be useful.
- Specialist referees should verify the degree bounds in the rational continuation, the completeness and normalization of the representation vectors, and the endpoint changes in the stabilizer decomposition.

### Results / Findings

- Theorem 2.2 is clear and well normalized.
- The \(m=n=5\) rational construction is a model endpoint argument: the PSD spectrum, mean identity, symmetrized product, and violating eigenvalue are all stated.
- The key positivity result would be more persuasive in print if one representative determinant polynomial were displayed in full, including its shifted positive-coefficient expansion, rather than reporting only aggregate counts.

### Discussion

- The limitations discussion is exceptionally responsible.
- Add a positive, bounded implications discussion as requested in W4.
- Clarify whether the incomplete \(m=6\) material generated any mathematically defensible conjecture. If not, archive it without allowing it to distract from the completed \(m\leq5\) paper.

### Conclusion

- A distinct conclusion is needed. It should not claim independent verification, formal proof, or a universal random-reshuffling advantage.
- It should state the exact solved region, the sharp five-factor exception, the reusable methodological idea, and the two most important open mathematical questions.

### References

- Bibliographic metadata for the nine cited items appears internally consistent, but the coverage is too narrow.
- Convert the final bibliography to the target journal's style and use a proper bibliography database for submission.
- Refresh the 2026 Peng preprint citation at submission and specify the version used.

---

## Questions for Authors

1. Can the authors supply a human-readable completeness proof showing that the 76 canonical word-pattern equations and the listed symmetry-adapted test vectors cover every coefficient and every irreducible component required for arbitrary finite-dimensional Hermitian substitutions?
2. Which parts of the theorem-to-certificate reduction were derived independently of the released JSON schema, and which parts are merely rechecked by different arithmetic engines?
3. After surveying the omitted noncommutative AGM and random-reshuffling literature, what is the narrowest priority claim the authors can substantiate for the four-factor theorem, the five-factor restoration threshold, and the balanced-block certificate method?
4. Who will accept accountable authorship, and where—under what license, DOI, version tag, and whole-package hash—will the exact submitted certificate package be archived?

---

## Minor Issues

### Language / Grammar

- The prose is generally strong and needs only light copyediting.
- On pp. 8–9, long filesystem paths interrupt the prose and wrap awkwardly. Use consistent `\path{}` formatting or move detailed paths to a table/supplement.
- Consider replacing “remaining cases through product length five” with a formulation that explicitly refers to the stated Recht–Ré two-sided inequality, to avoid implying resolution of every related noncommutative AGM variant.

### Citation Format

- The raw URLs in the reference list should be adapted to SIAM style, with DOI links preferred where available.
- Add version/date information for the 2026 arXiv preprint.
- Cite the archived software and certificate dataset as research outputs in their own right.

### Figures and Tables

- The two existing tables are useful and legible.
- A compact proof-obligation flow diagram—from normalized operator inequality to free identity, orbit coordinates, representation blocks, shifted minors, and endpoints—would materially improve accessibility.
- If no diagram is added, provide an equivalent numbered verification-specification table.

### Layout

- Add keywords, MSC codes, an abbreviated running title of at most 50 characters, and the target journal's standard macros before submission.
- The p. 1 evidence-boundary box is valuable, but journal layout may be cleaner if it becomes a short “Computer-assisted proof status” subsection immediately after the introduction.
- The abstract should be shortened modestly from its current near-limit length.

---

## Dimension Scores

The scores are calibrated to a strong specialist venue and are ordinal rather than empirically calibrated acceptance probabilities.

| Dimension | Score (0–100) | Descriptor | Notes |
|---|---:|---|---|
| Originality (20%) | 86 | Strong | Potentially resolves a genuine open four-factor case and gives a sharp five-factor threshold; priority audit remains incomplete. |
| Methodological Rigor (25%) | 75 | Strong | Exact rational architecture and hardened replay are substantial, but the semantic completeness argument is insufficiently exposed in the paper. |
| Evidence Sufficiency (25%) | 72 | Adequate | Rich exact internal evidence; no external reproduction, public immutable archive, or fully reader-auditable encoding bridge yet. |
| Argument Coherence (15%) | 80 | Strong | Clear theorem-to-architecture narrative; a conclusion and verification-specification bridge are missing. |
| Writing Quality (15%) | 83 | Strong | Precise, compact, and candid; some certificate-density and submission-format issues remain. |
| Literature Integration (optional) | 64 | Adequate | Core lineage is present, but nearby AGM variants and later reshuffling formulations are omitted. |
| Significance & Impact (optional) | 82 | Strong | High specialist significance if verified; broader applied implications need clearer bounded articulation. |
| **Weighted Average** | **78.4** | **Minor by numerical rubric; Major Revision after non-averagable gates** | The aggregate score cannot cancel the load-bearing proof-interface and archival/accountability requirements. |

---

## Recommendation to Peer Reviewers

I recommend that the methodology referee independently reconstruct at least one coefficient orbit and one representation block from the manuscript definitions rather than from verifier helper functions. The domain referee should audit the symmetric-group decomposition, small-\(n\) endpoint changes, and literature priority. A stochastic-optimization perspective referee should assess whether the application discussion is both useful and appropriately bounded. All referees should preserve the manuscript's explicit distinction between exact replay and independent mathematical validation.
