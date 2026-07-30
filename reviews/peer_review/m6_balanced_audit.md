# Independent audit of the six-factor balanced-multiples result

**Review date:** 30 July 2026  
**Scope:** the \(m=6\) identity and base-positivity programs, both parametric
JSON records, Theorem 3.1 (balanced seed continuation), the six-factor section,
and parts (5)--(6) of the main theorem.  
**Review mode:** theorem-promotion / methodology audit; manuscript and source
were treated as read-only.  
**Confidence:** 4/5.

## Recommendation

**Promotion to a candidate theorem is defensible**, provided the claim remains
exactly restricted to

\[
\text{upper bound when }7\mid n,\qquad
\text{lower bound when }8\mid n,
\]

and hence the two-sided norm inequality when \(56\mid n\).

I found no mathematical defect in the coefficient identity, the base-PSD
certification, or the balanced-lifting implication. The result is materially
stronger than an exploratory observation: it is an exact computer-assisted
proof from two rational seed certificates. It is not an all-\(n\) six-factor
theorem, does not establish a sharp threshold, and gives no endpoint
counterexample.

Before publication, the quantification in parts (5)--(6) of the main theorem
should be made explicit, the executable paths and status language should be
made consistent with the promoted claim, and the exact environment should be
pinned. These are required presentation and reproducibility corrections, not
repairs to the mathematical implication.

## Exact replays

### Rational identity layer

Command:

```text
../replication-venv/bin/python exploratory/m6/check_parametric_identities.py
```

Observed result:

```text
M6 UPPER: 1,156 exact rational coefficient identities passed.
M6 LOWER: 1,156 exact rational coefficient identities passed.
M6 IDENTITY LAYER: PASS (NON-RELEASE; POSITIVITY UNCHECKED)
```

### Base-PSD layer

The project environment did not initially contain `python-flint`. I therefore
ran the stated version in an isolated transient environment:

```text
uv run --isolated --python 3.13 --with python-flint==0.8.0 \
  exploratory/m6/certify_base_psd_flint.py
```

Observed exact results:

| Side | Matrix | Base | Size | Rank | Zero coefficients of \(\det(tI+A)\) | Characteristic-list SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| upper | \(G\) | 7 | 400 | 399 | 1 | `c95af891ab9992fd2681af349044732a988ba147db9e43eec4288e2317589f51` |
| upper | \(H\) | 7 | 400 | 400 | 0 | `a8bbe7306acc878d612c8d8bd3695a036d35852e3d1257263205ec809a497419` |
| lower | \(G\) | 8 | 585 | 585 | 0 | `bd0867a98fd93a7cb624200f7d965cf4983448e0cf30c843d7b7fd7a49729a03` |
| lower | \(H\) | 8 | 585 | 585 | 0 | `32e99420c0feb2bbbcd08fdf4e40fc2847ed1ab945620073397b5394d75b6a46` |

The common positive denominators were
`16941456000000` and `262144000000`, exactly as reported in the paper.
The four digests also agree with the paper.

## 1. Pattern construction, signs, and scaling

### Pattern count

`restricted_growth_strings(k)` starts with label \(0\) and permits at each
step every existing label plus one new label. It therefore enumerates set
partitions of a \(k\)-letter word exactly once. For localizers on words of
length at most three, the maximum degree is

\[
3+1+3=7.
\]

The required number of equality patterns is consequently

\[
\sum_{k=0}^{7}B_k
=1+1+2+5+15+52+203+877
=1156,
\]

matching both the implementation and the manuscript.

### Coefficient expansion

For a canonical word pattern, the executable reconstructs precisely the three
parts of

\[
\sum_i\mathcal L_{x_i}(G_i)+\mathcal L_{n-\sum_i x_i}(H):
\]

1. a \(G\) contribution for every split
   \(u^*x_i v\), with the inserted letter transposed with canonical label
   \(0\) so that it becomes the distinguished \(G\)-letter;
2. \(+nH\) for every split \(u^*v\), from the constant term of \(g_n\);
3. \(-H\) for every split \(u^*x_i v\), from
   \(-\sum_i x_i\).

The reversal of the prefix is correct because coefficients of a Gram
localizer are indexed by \(u^*gv\), not \(ugv\).

The target signs are also correct:

- upper: \((n)_6-e_{6,n}\), hence coefficient \(-1\) on the unique
  all-distinct pattern \((0,1,2,3,4,5)\);
- lower: \((n)_6+e_{6,n}\), hence coefficient \(+1\);
- constant pattern: \((n)_6\);
- all other patterns: zero.

As a sensitivity check, I swapped two unequal upper \(G\)-coordinates in
memory. The checker rejected the mutation at the first nonconstant pattern,
with a nonzero rational residual. Thus the recovered coordinate order is
material to the identity test.

**Finding:** pass.

## 2. JSON \(G/H\) ordering

The reconstructed orbit scan is:

1. words in degree-then-lexicographic order through degree three;
2. pairs in lexicographic nested-loop order;
3. first-occurrence canonical orbit numbering;
4. transpose identification by the lexicographically smaller of
   \((u,v)\) and \((v,u)\);
5. for \(G\), label \(0\) fixed and all movable labels numbered from \(1\).

It yields 797 point-stabilizer orbits and 211 full-symmetry orbits. These are
stable at the seed sizes: a pair of degree-three words uses at most six
movable labels, so \(G\) stabilizes at \(n=7\), while \(H\) is already stable
at \(n=6\).

Both surviving block builders consume the flat JSON list as

```text
G = Q[0:797],  H = Q[797:1008].
```

Moreover, index 797 is the constant \(H\)-entry and satisfies

\[
z_{797}(n)=(n-1)_5.
\]

This value is forced independently by the constant coefficient:
\(nH_{\varnothing,\varnothing}=(n)_6\).

The complete 1,156-equation pass for each sign is much stronger than the
single fingerprint: it authenticates the recovered within-\(G\) and
within-\(H\) ordering against every free-word equality pattern. The two JSON
files retain their previously recorded SHA-256 values:

```text
upper f0db80568847c91ef075fa49640205d07d96c96b22f3b706cd0db62066cabb6c
lower a24bf15495988840bb3cd30bcde4a1de5528a1d6633f32295c2deb9d50a9a186
```

I also checked all 2,016 entries: every reduced denominator is a positive
integer times \(n^q\), \(0\le q\le6\), and neither base has a pole.

**Finding:** pass.

## 3. Exact characteristic-polynomial PSD criterion

For a real symmetric matrix \(A\) with eigenvalues \(\lambda_i\),

\[
\det(tI+A)=\prod_i(t+\lambda_i).
\]

If \(A\succeq0\), all coefficients are elementary symmetric polynomials in
nonnegative numbers and are nonnegative. Conversely, if some
\(\lambda_i<0\), then \(t=-\lambda_i>0\) is a positive root. A monic
polynomial with all coefficients nonnegative is strictly positive for every
\(t>0\), a contradiction. Symmetry is essential because it ensures the
eigenvalues, and hence these roots, are real.

FLINT returns coefficients of \(\det(xI-A)\) in ascending degree. For a
matrix of size \(s\), the code converts coefficient \(c_d\) by

\[
q_d=(-1)^{s+d}c_d,
\]

which is exactly the coefficient of \(t^d\) in \(\det(tI+A)\). I confirmed
the API ordering and sign conversion on independent \(2\times2\) positive
definite, indefinite, and singular examples.

Clearing denominators multiplies each rational Gram matrix by a strictly
positive scalar, so it preserves positive semidefiniteness and rank.

**Finding:** pass.

## 4. Rank and kernel handling

The exact rank computations show:

- upper \(G_7\): corank one;
- upper \(H_7\): positive definite;
- lower \(G_8,H_8\): positive definite.

The coefficient criterion already proves PSD. Rank then identifies the
nullity exactly. For the sole singular matrix, I independently multiplied the
full integer \(G_7\) matrix by the 400-dimensional all-ones word-evaluation
vector. Every row sum is exactly zero. Together with rank 399, this proves
that this expected equality vector spans the entire kernel.

The current PSD executable checks rank and the number of zero coefficients,
but it does not explicitly check this kernel vector. Adding the exact row-sum
check would improve semantic diagnostics, although it is not needed for the
PSD conclusion.

**Finding:** pass, with one recommended nonessential diagnostic.

## 5. Balanced lifting and theorem inference

At \(n=br\), choose a uniformly random balanced coloring
\(\chi:[n]\to[b]\) and substitute

\[
y_a=\frac1r\sum_{\chi(i)=a}x_i.
\]

For any fixed ordered distinct \(m\)-tuple,

\[
\Pr(\text{its colors are distinct})
=\frac{(b)_m r^m}{(n)_m}.
\]

The substituted word contributes \(r^{-m}\); multiplying the seed identity
by \((n)_m/(b)_m\) therefore gives coefficient one on every distinct word and
zero on repeated-index words. Also

\[
g_b(y)=b-\frac1r\sum_i x_i=\frac1r g_n(x).
\]

Every transported Gram matrix is a positive scalar multiple of an average of
congruences of a seed Gram matrix. Hence PSD at the seed, unlike rational
continuation alone, genuinely implies PSD at balanced multiples.

Applying this construction gives:

- upper seed \(b=7\) \(\Rightarrow\)
  \(e_{6,n}\preceq(n)_6 I\) for \(7\mid n\);
- lower seed \(b=8\) \(\Rightarrow\)
  \(-(n)_6 I\preceq e_{6,n}\) for \(8\mid n\);
- both bounds when \(\operatorname{lcm}(7,8)=56\mid n\).

The normalization lemma then converts the two Loewner bounds to the claimed
two-sided norm inequality. No positivity conclusion follows at nonmultiples,
even though the rational coefficient identities continue there.

**Finding:** pass.

## Falsification attempts and residual assurance boundary

I specifically tested or inspected the following failure modes:

- wrong Bell-pattern range or omission of degree seven;
- reversal error in \(u^*gv\);
- upper/lower sign reversal;
- incorrect \(G/H\) offset;
- wrong within-\(G\) ordering, by an in-memory mutation;
- poles or nonpositive denominator scalings at the seed;
- reversed FLINT coefficient order;
- an indefinite matrix passing the coefficient-sign rule;
- an unaccounted upper kernel;
- use of rational continuation, rather than balanced congruence averaging, to
  infer positivity.

None falsified the result.

The remaining assurance limits are:

1. the identity and PSD programs share the same `canonical_entry` and
   first-occurrence orbit implementation, so they are complementary exact
   checks, not fully independent implementations;
2. the historical numerical discovery and derivation of the 1,008 functions
   are not reproduced, although derivation history is not logically required
   once the exact certificate is verified;
3. the absent representation bases still block all-\(n\) positivity;
4. the endpoint pickle records do not prove counterexamples or sharpness;
5. this audit is not independent journal peer review or formal verification.

## Required pre-publication corrections

1. **Quantifier wording.** In main-theorem parts (5)--(6), replace the
   potentially ambiguous use of \(\mathcal E_{6,7r}(A)\) and
   \(\mathcal E_{6,8r}(A)\) after initially quantifying
   \(A_1,\ldots,A_n\) with explicit clauses “if \(n=7r\)” and “if
   \(n=8r\),” or quantify the matrix tuples separately.
2. **Path/status consistency.** The manuscript cites
   `releases/m6-balanced/...`, whereas the audited files were under
   `exploratory/m6/...` at review time and still described themselves as
   non-release. Relocate or cite them consistently and update the status text
   only after the exact replay is in the release runner.
3. **Environment pinning.** Add `python-flint==0.8.0` to the replication
   environment and make the full base-PSD command part of the package replay.
4. **Digest wording.** The reported digests hash FLINT's raw coefficient list
   for \(\det(xI-A)\), before the alternating-sign conversion to
   \(\det(tI+A)\). State this explicitly to avoid ambiguity.
5. **Recommended robustness.** Add record-side/base metadata checks, hash
   checks, the exact all-ones upper-\(G\) kernel check, and a coordinate-order
   mutation fixture. These strengthen diagnostics but are not missing
   mathematical premises.

## Final judgment

The six-factor arithmetic-progression clauses can be retained as a theorem in
the anonymous candidate paper after the required wording and packaging
corrections above. The exact evidence supports no broader \(m=6\) statement
than the two progressions and their \(56\)-divisible intersection.
