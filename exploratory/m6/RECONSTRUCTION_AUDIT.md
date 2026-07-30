# \(m=6\) orbit reconstruction audit

**Status:** interrupted reconstruction record, 2026-07-30. This note reports
only work actually completed. It is not a certificate, theorem, counterexample,
or PSD verification.

## Scope and source handling

The eight-file snapshot in this directory was treated as read-only during the
reconstruction, apart from adding this requested audit note. No missing
`orbits.pkl` or interpolation-basis file was fabricated, and no manuscript or
release claim was changed.

The three endpoint pickles were not passed to `pickle.load` or `pickle.loads`.
Their bytes were first checked against the SHA-256 values already recorded in
`README.md`, then scanned with `pickletools.genops`. The observed opcode sets
contained only protocol/framing, primitive integer/string/container, memo, and
tuple-building operations. This was a bounded structural scan only; none of
their numerical records was used in the reconstruction below.

## Reconstructed canonicalization

The exact canonical-entry convention in the \(m=4\) and \(m=5\) release
verifiers was located and generalized from words of length at most two to words
of length at most three:

1. form `left + (separator,) + right`;
2. relabel symbols in first-occurrence order;
3. for \(G\), keep the distinguished symbol `0` fixed and assign new labels
   from `1`; for \(H\), assign new labels from `0`;
4. repeat after exchanging `left` and `right`;
5. take the lexicographically smaller encoding, thereby imposing Gram
   symmetry;
6. scan the word basis in the order
   \[
   (),\quad (i),\quad (i,j),\quad (i,j,k),
   \]
   with each Cartesian power lexicographic, and assign an orbit index on first
   occurrence.

This is the same canonical-key formula written independently in both surviving
\(m=6\) block builders. The earlier release implementation is in
`releases/m5/src/derive_parametric_family.py`, lines 22--38, and the \(m=6\)
consumer implementation is in `build_parametric_blocks.py`, lines 51--59.

## Exact orbit counts obtained

The first-occurrence enumeration produced:

| Concrete alphabet size \(N\) | \(G\), stabilizer of `0` | \(H\), full symmetry |
|---:|---:|---:|
| 1 | 10 | 10 |
| 2 | 120 | 64 |
| 3 | 424 | 151 |
| 4 | 690 | 200 |
| 5 | 783 | 210 |
| 6 | 796 | 211 |
| 7 | 797 | 211 |
| 8 | 797 | 211 |

Thus the stable maps have exactly \(797\) \(G\)-orbits and \(211\)
\(H\)-orbits, for a total of \(1008\). The \(H\) map is already stable at
\(N=6\); the \(G\) map gains exactly one orbit between \(N=6\) and \(N=7\) and
is stable thereafter. This independently reproduces the structural
\(796\)-versus-\(797\) feature of the endpoint records without reading their
payloads.

## What the surviving scripts determine about function order

`build_parametric_blocks.py` loads the flat list `Q` from a side's JSON and
uses

```text
off = 0              for G
off = len(G)         for H
Q[off + orbit_index]
```

so the outer split is determined: JSON indices `0..796` are intended for
\(G\), and indices `797..1007` are intended for \(H\).

The scripts also use the reconstructed canonical key to query the missing map.
However, they load the key-to-index dictionaries from the absent `orbits.pkl`;
they do not contain the code that originally assigned the dictionary values.
The \(m=4\) and \(m=5\) releases assign those values by precisely the
first-occurrence scan above, making that ordering the strongest available
reconstruction. It is not yet proven to be the original \(m=6\) within-\(G\)
and within-\(H\) ordering solely by the surviving \(m=6\) files.

## Decisive checks not completed

Neither the upper nor lower 1008-function coefficient-identity system was run
before work was stopped. In particular:

- the 1156 restricted-growth word patterns of lengths \(0\) through \(7\)
  have not yet been generated in a durable verifier;
- the upper JSON has not been checked against all free-word coefficients under
  the reconstructed ordering;
- the lower JSON has not been checked against all free-word coefficients under
  the reconstructed ordering;
- no direct base-\(n=7\) upper PSD test was run;
- no direct base-\(n=8\) lower PSD test was run; and
- the absent seven \(G\) and seven \(H\) interpolation bases still prevent
  reconstruction of the representation blocks by the surviving builders.

Consequently, the current result materially advances the **orbit-count and
finite-\(n\) collision audit**, and fixes a deterministic candidate ordering,
but it does not yet authenticate the within-block ordering of the 1008
functions or establish a Gram identity or PSD statement.

## Next exact step

Generalize the dependency-free \(m=5\) identity construction to degree at most
three, enumerate all 1156 restricted-growth patterns through length seven, and
test the two JSON function lists against every coefficient equation using the
candidate first-occurrence maps. A pass would be strong direct evidence that
the complete flat ordering has been recovered; a first failing row would give
a precise ordering or formula obstruction. That check should precede any PSD
work.
