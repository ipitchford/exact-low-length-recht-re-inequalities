# Technical memo: balanced certificate continuation and semantic validation

## Purpose

This memo extracts a general theorem from Section 4 of the unified manuscript and from:

- `releases/m4/src/derive_parametric_family.py`,
- `releases/m5/src/derive_parametric_family.py`,
- the two exact verifier pairs.

The main point is a strict logical separation:

1. **Balanced averaging and rational continuation prove free-polynomial coefficient identities.**
2. **Positive semidefiniteness away from genuine balanced multiples is a separate theorem.**

No gap prevents the identity-continuation theorem below. The current package also contains sufficient data for the \(m=4,5\) positivity claims, but two semantic obligations should be promoted from code/comments to explicit lemmas: exhaustiveness of the representation test vectors and the degree-\(\leq4\) theorem underlying block-coefficient interpolation.

---

## 1. Setup

Let \(\mathbb R\langle x_1,\ldots,x_n\rangle\) be the real free \(*\)-algebra with self-adjoint generators. Let
\[
\mathcal W_{n,\ell}:=\{x_{i_1}\cdots x_{i_d}:0\le d\le\ell\}
\]
be the word basis through length \(\ell\). For a real symmetric matrix \(Q\) indexed by this basis, put
\[
\mathcal L_g(Q):=\sum_{u,v\in\mathcal W_{n,\ell}}Q_{uv}u^*gv.
\]
Write
\[
e_{m,n}:=\sum_{\substack{i_1,\ldots,i_m\in[n]\\\text{all distinct}}}
x_{i_1}\cdots x_{i_m},
\qquad
g_n:=n\mathbf1-\sum_{i=1}^n x_i,
\qquad
(z)_k:=z(z-1)\cdots(z-k+1).
\]

Fix integers
\[
b\ge m,\qquad 2\ell+1\ge m.
\]
For \(\varepsilon\in\{-1,+1\}\), suppose an exact \(b\)-variable seed identity is given:
\[
(b)_m\mathbf1+\varepsilon e_{m,b}
=
\sum_{a=1}^b\mathcal L_{x_a}(G_{b,a}^{\varepsilon})
+\mathcal L_{g_b}(H_b^\varepsilon). \tag{S}
\]
Assume:

- \(G_{b,a}^{\varepsilon}\) is equivariant under relabeling, so the family is determined by one matrix invariant under the stabilizer of its distinguished index;
- \(H_b^\varepsilon\) is \(S_b\)-invariant.

No positivity assumption is required for the identity theorem.

For a finite set \(S\) and a function \(F\) on maps \(S\to[b]\), define the formal balanced-coloring functional
\[
\mathfrak A_{\nu,b,S}[F]
:=
\frac{1}{(\nu)_{|S|}}
\sum_{\phi:S\to[b]}
\left[
\prod_{a=1}^b
\left(\frac{\nu}{b}\right)_{|\phi^{-1}(a)|}
\right]F(\phi)
\in\mathbb Q(\nu). \tag{A}
\]
If \(\nu=br\) with \(r\in\mathbb N\), this is the genuine expectation of \(F(\chi|_S)\) for a uniformly random balanced coloring \(\chi:[\nu]\to[b]\) having \(r\) labels of each color.

For words \(u,v\), let \(S(u,v)\) be their set of distinct letters and \(d=|u|+|v|\). Define
\[
\begin{aligned}
H_{m,\nu}^{\varepsilon}(u,v)
&:=
\frac{(\nu)_m}{(b)_m}
\left(\frac b\nu\right)^{d+1}
\mathfrak A_{\nu,b,S(u,v)}
\!\left[
\phi\mapsto
H_b^\varepsilon(\phi(u),\phi(v))
\right], \tag{H}\\
G_{m,\nu,0}^{\varepsilon}(u,v)
&:=
\frac{(\nu)_m}{(b)_m}
\left(\frac b\nu\right)^{d+1}
\mathfrak A_{\nu,b,S(u,v)\cup\{0\}}
\!\left[
\phi\mapsto
G_{b,\phi(0)}^\varepsilon(\phi(u),\phi(v))
\right]. \tag{G}
\end{aligned}
\]
Here \(\phi\) is applied letterwise, including repeated occurrences. The matrices \(G_{m,\nu,i}^\varepsilon\) are obtained by moving the distinguished label \(0\) to \(i\).

These are exactly the formulas implemented by the two `derive_parametric_family.py` scripts:

- `C = falling(n,m)/falling(b,m)`,
- `r = n/b`,
- `r**(-(len(u)+len(v)+1))`,
- `expected(...)` implements \(\mathfrak A_{\nu,b,S}\).

---

## 2. Paper-ready identity theorem

### Theorem (balanced seed continuation: identity part)

Assume the seed identity **(S)** and equivariance hypotheses above. Suppose equality-pattern coordinates for words of degree at most \(2\ell+1\), stabilizer-orbit coordinates for \(G\), and full-symmetry orbit coordinates for \(H\) have stabilized for all integers \(n\ge N_0\).

Then the entries **(H)** and **(G)** are rational functions of \(\nu\). For every integer \(n\ge N_0\) at which those functions are finite,
\[
(n)_m\mathbf1+\varepsilon e_{m,n}
=
\sum_{i=1}^n\mathcal L_{x_i}(G_{m,n,i}^{\varepsilon})
+\mathcal L_{g_n}(H_{m,n}^{\varepsilon}). \tag{C}
\]
This conclusion is an identity in the free algebra. It does **not** assert that any continued Gram matrix is positive semidefinite.

### Proof

#### Step 1: genuine balanced multiples

Let \(n=br\) with \(r\in\mathbb N\). For a balanced coloring
\(\chi:[n]\to[b]\), set
\[
y_a^\chi:=\frac1r\sum_{\chi(i)=a}x_i.
\]
Substitute \(y_1^\chi,\ldots,y_b^\chi\) into **(S)**, multiply by
\((n)_m/(b)_m\), and average over \(\chi\).

The constant term becomes \((n)_m\mathbf1\). For a fixed ordered tuple
\((i_1,\ldots,i_m)\), expansion of \(e_{m,b}(y^\chi)\) contributes
\[
r^{-m}\,
\mathbf1_{\{\chi(i_1),\ldots,\chi(i_m)\ {\rm distinct}\}}.
\]
If an original index is repeated, the indicator vanishes. If the original indices are distinct, then
\[
\Pr\{\chi(i_1),\ldots,\chi(i_m)\text{ distinct}\}
=\frac{(b)_m r^m}{(n)_m}.
\]
After multiplication by \((n)_m/(b)_m\), the coefficient is one. Thus the averaged left side is
\[
(n)_m\mathbf1+\varepsilon e_{m,n}.
\]

For the constraint localizer,
\[
g_b(y^\chi)
=b\mathbf1-\frac1r\sum_i x_i
=\frac1r g_n(x).
\]
Every basis word contributes one factor \(r^{-1}\) per letter, and the localizing multiplier contributes one further \(r^{-1}\). Consequently the Gram entry indexed by \((u,v)\) carries the factor
\[
r^{-(|u|+|v|+1)}
=\left(\frac bn\right)^{|u|+|v|+1}.
\]
The restriction law of a balanced coloring to the distinct letters in \(u,v\) (and the distinguished multiplier index for \(G\)) is precisely **(A)**. Therefore the averaged right side is exactly the right side of **(C)** with entries **(H)** and **(G)**.

Hence **(C)** holds for every positive multiple \(n=br\).

#### Step 2: rationality

For fixed \(u,v\), formula **(A)** is a finite sum of products of falling-factorial polynomials divided by \((\nu)_{|S|}\). Multiplication by the explicit prefactor in **(H)** or **(G)** leaves a rational function of \(\nu\).

#### Step 3: continuation by equality patterns

Every monomial occurring in **(C)** has degree at most \(2\ell+1\). Once \(n\ge N_0\), coefficients of the \(S_n\)-invariant difference between the two sides are indexed by a fixed finite set of equality patterns. For each pattern, its coefficient is a rational function of \(n\) by Step 2. Step 1 makes that rational function zero at infinitely many integers \(n=br\). It is therefore the zero element of \(\mathbb Q(\nu)\).

Thus every stabilized equality-pattern coefficient vanishes identically. Specializing at any integer \(n\ge N_0\) outside the finite pole set proves **(C)**. \(\square\)

### Package specialization

The package uses \(\ell=2\), hence degree at most five.

- For \(m=4\): \(b=5\), and the theorem derives all 162 upper/lower orbit functions from the two exact \(n=5\) seeds.
- For \(m=5\): \(b=6\), and it derives all 162 functions from the two exact \(n=6\) seeds.
- There are
  \[
  B_0+B_1+\cdots+B_5=1+1+2+5+15+52=76
  \]
  equality patterns, exactly the 76 restricted-growth strings generated by `rgps`.
- The exact verifiers independently substitute the published rational functions into all 76 upper and 76 lower equations. Therefore the theorem is a derivation of the published families, while the 152 direct rational checks per product length are a logically sufficient identity replay even if the derivation script is ignored.

In the released functions all denominators simplify to a positive integer times a power of \(n\), so every positive integer in the stated stable ranges is pole-free.

---

## 3. Positivity is a separate theorem

### Proposition (soundness after PSD)

Fix an integer \(n\) for which **(C)** holds. If
\[
G_{m,n,i}^{\varepsilon}\succeq0
\quad(1\le i\le n),
\qquad
H_{m,n}^{\varepsilon}\succeq0,
\]
then for every Hermitian PSD tuple satisfying \(\sum_iA_i\preceq nI\),
\[
(n)_m I+\varepsilon E_{m,n}(A)\succeq0.
\]

### Proof

Factor every Gram matrix as \(Q=C^*C\). Since \(A_i\succeq0\) and
\(g_n(A)=nI-\sum_iA_i\succeq0\), each evaluated localizer is a sum of terms \(f(A)^*A_if(A)\) or \(f(A)^*g_n(A)f(A)\), hence is PSD. Evaluate **(C)**. \(\square\)

### What balanced averaging itself proves

At a genuine multiple \(n=br\), PSD of the seed matrices implies PSD of the transported matrices: they are positive scalar multiples of averages of congruences of the seed Gram matrices. This is an ordinary convexity argument.

### What rational continuation does not prove

For a nonmultiple \(n\), \(\nu/b\) is not an integer color-class size. The factors
\[
\left(\frac{\nu}{b}\right)_k
\]
in **(A)** are algebraic interpolation weights, not probabilities, and need not all be nonnegative. Therefore neither rational identity continuation nor positivity at infinitely many multiples implies PSD at intervening integers.

The package correctly supplies a different proof:

1. decompose \(G\) and \(H\) into fixed multiplicity blocks;
2. scale each block by a positive diagonal congruence;
3. verify exact leading-principal-minor polynomials with positive coefficients in \(n-b\);
4. handle the one singular upper \(G\) block by its explicit kernel and positive \(7\times7\) principal block.

The exceptional \(m=4,n=4\) and upper \(m=5,n=5\) cases are separate certificates and do not follow from the continuation theorem.

---

## 4. Minimal semantic-checker obligations

The following obligations are sufficient to close the shared-schema risk identified in the domain review.

### O1. Basis and degree coverage

1. Define the basis as every word of length \(0,1,2\), in a canonical order.
2. Prove that localizers by \(x_i\) and \(g_n\) have degree at most five.
3. Enumerate every equality pattern of lengths \(0,\ldots,5\) by restricted-growth strings.
4. Check the count \(76=\sum_{d=0}^5 B_d\).

This proves that the coefficient system has not omitted a possible monomial pattern.

### O2. Orbit classifier correctness

For a pair of words \((u,v)\), the current `canonical_entry`:

1. concatenates \(u\), a separator, and \(v\);
2. relabels symbols by order of first occurrence;
3. preassigns the distinguished label \(0\) for the stabilizer case;
4. identifies \((u,v)\) with \((v,u)\) because Gram matrices are symmetric.

The checker or paper must prove:

> Two symmetric Gram entries have the same key if and only if they are in the same \(S_n\)-orbit (for \(H\)) or \(S_{n-1}\)-orbit fixing \(0\) (for \(G\)).

A pair of length-\(\le2\) words contains at most four movable labels. Hence:

- the \(H\)-orbit classification is stable for \(n\ge4\);
- the \(G\)-classification is stable for \(n\ge5\).

Exhaustive key generation must return 22 and 59 respectively.

### O3. Coefficient-extraction soundness

Generate the matrices called `A0` and `A1` directly from:

\[
\sum_i\mathcal L_{x_i}(G_i)+\mathcal L_{n-\sum_i x_i}(H).
\]

For each of the 76 patterns, check separately:

- every split \(u^*x_iv\) with \(|u|,|v|\le2\);
- the \(n\mathcal L_1(H)\) contribution;
- the \(-\sum_i\mathcal L_{x_i}(H)\) contribution;
- the target constant and all-distinct word coefficients.

This is already implemented, but a schema-level test should derive the pattern key independently from the Gram-orbit key.

### O4. Representation decomposition and test-vector exhaustiveness

Prove, with ranges,
\[
\mathcal W_n
\cong4[n]\oplus4[n-1,1]\oplus[n-2,2]\oplus[n-2,1,1]
\quad(n\ge4),
\]
and
\[
\mathcal W_n\!\downarrow S_{n-1}
\cong8[n-1]\oplus6[n-2,1]\oplus[n-3,2]\oplus[n-3,1,1]
\quad(n\ge5).
\]

For each explicit vector family in `vectors_H` and `vectors_G`, check:

1. the trivial vectors span all 4 or 8 invariant copies;
2. the six/four standard vectors are images of one nonzero standard vector under linearly independent intertwiners;
3. `q` is a nonzero vector of type \([n-2,2]\) or \([n-3,2]\);
4. `cyc` is a nonzero vector of type \([n-2,1,1]\) or \([n-3,1,1]\);
5. the cyclic group spans have the dimensions given by the hook-length formula.

Since symmetric-group irreducibles are absolutely real, an invariant symmetric matrix is a direct sum \(B_\lambda\otimes I_{V_\lambda}\). The contractions used in the verifier are positive diagonal congruences of the multiplicity matrices \(B_\lambda\), so their PSD is equivalent to PSD of the full Gram matrix.

The commutant-dimension checks
\[
\frac{8\cdot9}{2}+\frac{6\cdot7}{2}+1+1=59,
\qquad
\frac{4\cdot5}{2}+\frac{4\cdot5}{2}+1+1=22
\]
then certify that no invariant symmetric block is missing.

### O5. Polynomial degree bound for block contractions

This is the most important currently implicit lemma.

Every coefficient of
\[
v_i(n)^{\mathsf T}Q(n)v_j(n)
\]
with respect to a fixed orbit variable is a signed count of assignments of at most four freely summed labels satisfying finitely many equality and inequality constraints. Partition those assignments by their equality pattern. Each class has cardinality
\[
c\,(n-c_0)_s,\qquad s\le4,
\]
for an integer \(c\). Hence each contraction coefficient is a polynomial in \(n\) of degree at most four.

This lemma makes five exact evaluations sufficient to interpolate the coefficient polynomial. The sixth evaluation at \(n=10\) or \(11\) is then a redundancy check.

Without this lemma, five-point interpolation plus one additional point does not prove the block formula for all \(n\).

A stronger checker would derive these coefficient polynomials directly by symbolic equality-pattern counting, eliminating interpolation entirely.

### O6. Stored-block and positivity obligations

For every side, matrix type, and irreducible block:

1. contract the orbit functions with the semantically validated test vectors;
2. check equality with the stored scaled block;
3. verify symmetry;
4. recompute every leading principal minor;
5. verify the positive denominator and every shifted coefficient;
6. for the singular upper block, verify the kernel, positive leading block, and congruence to \(A\oplus0\).

### O7. Endpoint separation

At \(m=4,n=4\), use the actual \(S_4/S_3\) decomposition, where the stable stabilizer types merge. At \(m=5,n=5\), use the separate upper seed. Endpoint acceptance must not invoke the stable parametric blocks.

---

## 5. Gaps and recommended manuscript insertion

### No gap in balanced identity continuation

The seed-to-family scripts implement the theorem above exactly, and the proof uses only finite balanced averaging plus the elementary fact that a rational function vanishing at infinitely many points is zero. The manuscript can state this as a theorem now.

### Remaining semantic gaps before the all-\(n\) PSD proof is fully paper-auditable

1. **Test-vector exhaustiveness is encoded but not proved.** The displayed representation decompositions give the right multiplicities, and the vectors are plausible symmetry-adapted representatives, but the paper does not prove that the concrete `q`, `cyc`, and standard families realize and exhaust those copies.
2. **The block-coefficient degree bound is only a code comment.** The interpolation step is rigorous only after the degree-\(\le4\) counting lemma in O5 is proved.
3. **Orbit canonicalization is duplicated, not independently specified.** Both verifiers share the same `canonical_entry` logic. A mathematical definition and an independent schema test would close this risk.

These are repairable exposition/checker gaps, not evidence that the theorem is false.

### Minimal paper insertion

The manuscript needs only:

1. the theorem and proof in Section 2 above;
2. a lemma giving O2's orbit-classifier bijection and stable ranges;
3. a lemma giving O4's test-vector exhaustiveness;
4. the degree-\(\le4\) counting lemma in O5;
5. a sentence explicitly stating that PSD at nonmultiples is supplied solely by the exact block-minor certificates.

That insertion would materially strengthen both the theorem's conceptual significance and its semantic auditability without printing the large certificate tables.
