# Round 1 clean-room hostile audit

**Reviewer role:** clean-room adversarial mathematical reviewer  
**Date:** 30 July 2026  
**Scope restriction honored:** I inspected only `paper/`, `releases/`,
`scripts/`, `tests/`, `exploratory/`, `README.md`, `REPRODUCIBILITY.md`,
`STATUS.md`, and `AUTHORSHIP_AND_DISCLOSURE.md`. I did not read, list, search,
or glob `reviews/` or `publication/`. This report was written directly to the
requested destination.

## Recommendation

**Mathematical recommendation: conditional pass. Publication recommendation:
do not release the current snapshot until the integrity and traceability
blockers below are repaired and a clean release-qualifying replay passes.**

I did not falsify the claimed \(m=4\) or \(m=5\) theorem chain. The
free-localizer encoding, orbit classification, representation-block coverage,
balanced-block continuation, interpolation degree bound, shifted-minor
positivity argument, exceptional endpoints, and normalization step survived
the attacks described below. The result should nevertheless remain described
as a computer-assisted candidate theorem until an external expert independently
reconstructs the reduction.

The exact expected-iterate corollary from the De Sa matrices is valid with the
specific scaling
\[
C_i=A_i/2,\qquad H_i=I-C_i,\qquad
f_i(x)=\tfrac12x^{\mathsf T}H_i x,\qquad \eta=1.
\]
It is not valid if the unscaled \(A_i\) are called unit-step update matrices or
if the operator-norm comparison is silently upgraded to a comparison of
expected losses for random reshuffling versus with-replacement SGD.

## Principal theorem-chain audit

The paper's logical chain is:

1. Normalize arbitrary PSD inputs to \(\sum_i A_i\preceq nI\)
   (`paper/exact_recht_re_through_five.tex:104-145`).
2. Represent \((n)_m\mp e_{m,n}\) as degree-two free localizers with PSD Gram
   matrices (`paper/exact_recht_re_through_five.tex:149-192`).
3. Obtain the parametric identities from balanced \(b=m+1\) seeds and rational
   continuation (`paper/exact_recht_re_through_five.tex:217-265`).
4. Prove Gram positivity through complete symmetry multiplicity blocks and
   positive shifted leading minors (`paper/exact_recht_re_through_five.tex:305-398`).
5. Supply separate exact certificates at \(m=4,n=4\) and for the
   \(m=5,n=5\) upper bound, plus De Sa's exact lower counterexample
   (`paper/exact_recht_re_through_five.tex:400-461`).

Each implication in that chain is mathematically sound, subject to the
certificate data replaying as claimed.

### 1. Semantic encoding attack

**Attack.** I tried to find a mismatch among the free word \(u^*gv\), reversal
of the left basis word, the distinguished generator in \(G_i\), the
\(n-\sum_i x_i\) slack localizer, transpose identification of symmetric Gram
entries, and the sign of \(e_{m,n}\).

**Result.** No mismatch was found.

- Direct permutation actions give exactly 59 point-stabilizer Gram-entry
  orbits and 22 full-symmetry orbits.
- Concrete words through degree five give exactly 76 equality-pattern classes.
- An uncompressed concrete-word expansion of all seven seed/endpoint
  certificates equals the intended target polynomial exactly, rather than
  merely matching the compressed 76-row system.
- Four injected semantic faults—an omitted word pattern, a merged orbit, a
  corrupted exceptional vector, and an omitted block—were all rejected in
  both normal and optimized Python.
- I separately evaluated the certificates on noncommuting exact rational
  \(2\times2\) PSD substitutions with positive definite slack. Exact equality
  held for both signs at \(m=4,n=4,5,6\), for the upper sign at
  \(m=5,n=5\), and for both signs at \(m=5,n=6,7\).

The direct semantic checker's relevant independent constructions are in
`scripts/check_semantic_bridge.py:180-500`; its concrete certificate and full
Gram tests are in `scripts/check_semantic_bridge.py:361-498`.

### 2. Group-representation and positivity attack

**Attack.** I tried to find an untested isotypic component, a small-\(n\)
representation collision, a test vector outside the claimed irrep, or a
singular block incorrectly accepted from a zero determinant.

**Result.** No such fault was found.

The decompositions
\[
\mathcal W_n\cong
4[n]\oplus4[n-1,1]\oplus[n-2,2]\oplus[n-2,1,1]
\]
and
\[
\mathcal W_n\!\downarrow S_{n-1}\cong
8[n-1]\oplus6[n-2,1]\oplus[n-3,2]\oplus[n-3,1,1]
\]
have the correct total dimensions and predict the symmetric commutant
dimensions \(22\) and \(59\). Explicit group-orbit spans of the supplied
representatives cover the whole word space; their contraction rows have full
commutant rank. The \(S_3\) collision at the \(m=4,n=4\) endpoint is correctly
handled by the separate \(8,6,1\) decomposition.

The singular upper \(G\)-trivial block is also treated correctly. Its leading
\(7\times7\) block is positive definite, and the displayed kernel vector has
nonzero final coordinate, so the full block is congruent to \(A\oplus0\);
there is no determinant-only inference.

As an additional smoke test, I constructed the full \(G\) and \(H\) matrices
and numerically diagonalized them at stable and nonmultiple values through
\(n=11\). No negative eigenvalue appeared; the upper \(G\) matrix had exactly
the expected one numerical zero mode. This numerical check is not part of the
exact acceptance evidence.

### 3. Balanced continuation attack

**Attack.** I rederived the normalization in the lift, focusing on the most
likely off-by-\(b/n\) error.

**Result.** The continuation factor is correct.

For \(n=br\), each substituted word letter contributes \(r^{-1}=b/n\), and
the degree-one localizer contributes one additional such factor. Therefore an
entry indexed by words of total degree \(d\) carries
\((b/n)^{d+1}\). For \(H\), the extra factor also appears directly from
\[
b-\sum_a y_a=(b/n)\left(n-\sum_i x_i\right).
\]
For \(G\), it comes from the central \(y_a\) and the balanced-color
conditioning on the distinguished original letter. The probability
\[
\Pr(\text{the \(m\) fixed indices receive distinct colors})
=\frac{(b)_m r^m}{(n)_m}
\]
then cancels the product expansion and the factor
\((n)_m/(b)_m\) exactly.

The continued entries have denominators only of the form \(c n^q\), so there
is no pole on the asserted stable ranges \(n\ge5\) and \(n\ge6\). Identity on
infinitely many multiples therefore extends rationally to all specializations
in those ranges. The paper appropriately keeps positivity separate from this
identity continuation.

### 4. Interpolation attack

**Attack.** I tried to invalidate the use of five samples plus an out-of-sample
check for block-contraction polynomials.

**Result.** The degree bound is justified.

A contraction coefficient is a signed count of assignments involving at most
four free labels, because it pairs two words of length at most two. It is
therefore a linear combination of falling-factorial polynomials of degree at
most four. Exact fifth finite differences vanish across eight stable sizes in
the semantic checker (`scripts/check_semantic_bridge.py:998-1045`). Thus the
degree-four interpolation is not an unsupported empirical fit. The stored
scaled blocks and all 51 leading minors per product length are then recomputed
from the orbit functions, and strict positivity of every coefficient in
\(n-b\) proves positivity for the full real half-line \(n\ge b\).

### 5. Normalization attack

**Attack.** I checked whether the normalized Loewner theorem really implies
the original norm inequality for arbitrary PSD tuples.

**Result.** It does.

For \(S=\sum_iA_i\) and \(t=\|S\|/n\), positivity of \(S\) gives
\(S\preceq\|S\|I\), hence \(\sum_i(A_i/t)\preceq nI\). Homogeneity gives the
factor \(t^m\). Reversal of ordered distinct tuples makes \(E_{m,n}\)
Hermitian, so the two Loewner inequalities are equivalent to its operator-norm
bound. The \(t=0\) case is trivial because all PSD summands vanish.

## De Sa scaling and the expected-iterate corollary

The exact counterexample replay verifies that each unscaled \(A_i\) has
spectrum \(\{0,1,1,1,2\}\), that their mean is \(I\), and that
\[
R_A:=\frac1{120}E_{5,5}(A)
=\frac{29}{64}P_\perp-\frac{19}{16}P,
\qquad P=\frac15\mathbf1\mathbf1^{\mathsf T}.
\]
See `releases/m5/counterexamples/verify_n5_lower_counterexample.py:97-215`.

The valid optimization translation is the one now checked exactly in
`releases/m5/counterexamples/verify_n5_lower_counterexample.py:218-305`:
\[
C_i=A_i/2,\qquad H_i=I-C_i.
\]
Then \(C_i\) and \(H_i\) are PSD with spectra
\(\{0,\tfrac12,1\}\), \(\overline C=I/2\), and
\(\overline H=I/2\). Unit-step component-gradient updates for
\(f_i(x)=\tfrac12x^{\mathsf T}H_i x\) are exactly \(x\leftarrow C_i x\).

Because reversal bijects the 120 permutations, the convention for whether
updates multiply on the left or right does not change the average. One
random-reshuffling epoch has expected operator
\[
R_C=2^{-5}R_A
=\frac{29}{2048}P_\perp-\frac{19}{512}P,
\]
whereas five independent with-replacement expected updates have operator
\[
(\overline C)^5=\frac1{32}I.
\]
Consequently
\[
\|R_C\|=\frac{19}{512}>\frac1{32}
=\|(\overline C)^5\|,
\]
and on the all-ones direction the expected reshuffled iterate is
\(-19/512\) times the initial vector, versus \(1/32\) with replacement.
**The expected-iterate corollary is therefore valid.**

This is an expected-operator/expected-iterate comparison. It does not by itself
compare \(\mathbb E\|x_{\mathrm{RR}}\|\) with
\(\mathbb E\|x_{\mathrm{WR}}\|\), nor
\(\mathbb E f(x_{\mathrm{RR}})\) with
\(\mathbb E f(x_{\mathrm{WR}})\). If a deterministic five-step full-gradient
comparison is desired, Jensen does yield
\[
\mathbb E F(x_{\mathrm{RR}})
\ge \tfrac14\|\mathbb E x_{\mathrm{RR}}\|^2
> \tfrac14\|x_{\mathrm{GD}}\|^2
=F(x_{\mathrm{GD}})
\]
for an all-ones initial vector and
\(F(x)=\frac15\sum_i f_i(x)=\tfrac14\|x\|^2\). That is a different,
explicitly scoped corollary.

## Concrete blockers

### B1. Current manifests fail and do not yet bind the repaired release

Running

```text
python3 scripts/replay_all.py --timeout 60 --skip-mutations
```

on the audit snapshot reported SHA-256 mismatches in both release manifests,
including the edited READMEs, manuscripts, derivation scripts, verifiers, and
claim matrices. This alone blocks publication of the current snapshot. Rebuild
the manifests only after all review-driven edits are complete, then run the
full release-qualifying replay.

The existing `releases/m5/MANIFEST.sha256` also ends without either file under
`counterexamples/`, even though the counterexample and optimization translation
are load-bearing for sharpness and the expected-iterate claim. The deterministic
manifest rebuild script appears capable of including them, but the regenerated
manifest must be checked explicitly.

### B2. The \(m=5\) claim-evidence matrix is stale

`releases/m5/CLAIM_EVIDENCE_MATRIX.md:15` still identifies Lai and Lim's
unreplayed numerical obstruction as the sharpness evidence. The unified paper
instead correctly makes the exact De Sa replay load-bearing. Update that row to
name the exact counterexample script, the projector identity, and the
\(-285/2\) eigenvalue. If the expected-iterate corollary is retained, add a
separate row for the \(C_i=A_i/2\), \(H_i=I-C_i\) scaling and the
\(19/512>1/32\) comparison.

### B3. The expected-iterate claim is checked in code but not yet explained in
the publication-facing prose

The unified manuscript proves the matrix counterexample but does not state the
optimization translation. The counterexample README likewise stops at the
lower Loewner failure. If the expected-iterate corollary is intended as a
publication claim, state the component quadratics, average-objective
convention, unit step size, scaling, multiplication-order reversal argument,
and the precise distinction between expected iterate and expected loss.

### B4. This audit did not complete the advertised SymPy replay in its system
interpreter

The standard-library verifiers passed for \(m=4\) and \(m=5\) in both normal
and optimized modes, as did the semantic bridge and De Sa replay. The system
Python used for this audit did not contain SymPy, so the SymPy verifiers and
seed-to-family programs failed at import. This is an environment limitation,
not a mathematical discrepancy, but the final release must demonstrate the
documented pinned-environment command from a clean environment and must run
the full mutation suite rather than `--skip-mutations`.

## Final assessment

No critical mathematical defect was found. In particular:

- the \(m=4\) two-sided theorem for every integer \(n\ge4\) survived;
- the \(m=5\) upper theorem for \(n\ge5\) and lower theorem for \(n\ge6\)
  survived;
- the exact \(m=n=5\) lower failure is correctly established by De Sa's
  rational matrices;
- the threshold \(n=6\) is sharp; and
- the carefully scaled expected-iterate corollary is valid.

The current files are not yet a release-ready artifact because their manifests
and claim-evidence traceability lag the repaired code and prose. After those
items are fixed, require a clean full replay, including both arithmetic
implementations and all mutation controls, before changing the status from
pre-publication candidate.
