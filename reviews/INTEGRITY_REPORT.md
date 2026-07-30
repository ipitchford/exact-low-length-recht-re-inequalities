# Research-integrity report

## Disposition

The consolidated package is suitable as an anonymous public unrefereed
candidate after a clean final replay. Its scoped CC0-1.0 dedication and exact
version DOI resolve the public-distribution layer. It is not journal-
submission-ready until accountable authorship, venue declarations, and
external mathematical review are supplied.

## Imported verifier defect and repair

The original m4/m5 acceptance programs expressed load-bearing checks as
Python `assert` statements. Optimized Python removes those statements, and
one-field corruptions were therefore falsely accepted. The candidate replaces
them with explicit `VerificationError` conditions, scans all acceptance code
for assertions, runs every proof path normally and with `-O`, and requires
mutated identities, minors, seeds, endpoints, semantic encodings, orbit
ordering, PSD criteria, and path counts to fail explicitly.

This was an evidence-implementation defect, not evidence against the theorem
statements.

## Semantic and independence boundary

The standard-library and SymPy m4/m5 programs use different arithmetic engines
but share certificate schemas and proof architecture. A separate semantic
checker reconstructs literal permutation actions, concrete words,
representation spans, degree bounds, and full Gram matrices without reading
the compressed representation data. This materially reduces shared-schema
risk but is not a formal proof assistant or an external implementation.

The m6 identity and PSD programs check complementary exact obligations but
share the same canonical orbit encoder. A read-only audit independently
checked the coefficient signs/scaling, FLINT convention, ranks, kernel, and
balanced inference. That audit supports theorem promotion but is not journal
peer review.

## Significant extension

The formerly incomplete m6 snapshot yielded a theorem-grade subpackage without
the missing representation bases: exact full seed matrices are sufficient for
balanced multiples. The released claim is restricted to upper \(7\mid n\),
lower \(8\mid n\), and two-sided \(56\mid n\).

The exact De Sa replay was extended beyond first moments. An independent
subset/transfer derivation and exhaustive enumeration agree that the witness
has worse expected-iterate norm under reshuffling but strictly better
one-epoch second moment in every direction. The paper scopes this as a
finite-horizon instance result.

## Reproducibility and provenance

The historical discovery searches are not reproduced. The authoritative
source archives are recorded by SHA-256 but omitted from the public candidate
because they contain duplicate named manuscripts. Three release manifests
and one package manifest are complete, bidirectional inventories. Original
source material remains recoverable from the private local `LaiLim` source
folder.

## Remaining review targets

External experts should concentrate on:

- completeness of the free-polynomial and representation reductions;
- the general balanced-seed continuation scaling;
- a separate reconstruction of the six-factor orbit maps and seed matrices;
- the characteristic-polynomial PSD criterion as implemented;
- the De Sa optimization translation; and
- whether the literature positioning and priority language are complete at
  submission time.
