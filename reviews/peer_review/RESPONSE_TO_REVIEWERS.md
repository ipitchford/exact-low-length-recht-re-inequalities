# Response to internal reviewers

> **Historical status note (30 July 2026).** This response records the
> round-1 revision. The later candidate release resolves the distribution
> license, repository, and exact version DOI; see `STATUS.md`. Its statements
> about unresolved mathematics, external review, and journal authorship remain
> current.

We thank the reviewers for adversarial and methodological scrutiny. The paper
and package were revised rather than merely reworded.

## Mathematical exposition

The revision adds explicit orbit-classifier, representation-completeness, and
contraction-degree lemmas; a general balanced-seed continuation theorem; and
a strict statement that rational continuation does not carry positivity.
The m4/m5 claims retain their exact endpoints and assurance boundaries.

## Semantic verification

`scripts/check_semantic_bridge.py` no longer trusts the stored compressed
blocks. It compares canonical keys with literal group actions, enumerates
concrete words, regenerates representation spans and contraction ranks,
checks degree bounds, expands seven concrete certificates, and tests fourteen
full Gram matrices. Four targeted corruptions must fail in normal and
optimized Python.

## Six factors

The round-1 recommendation was to keep the inherited m6 snapshot outside
theorem claims because the uniform representation bases were missing. We
retain that boundary for all-\(n\) and endpoint assertions. A different exact
route became available after review: full \(400\times400\) and
\(585\times585\) seed Gram matrices can be certified directly by integer
characteristic polynomials. Combined with all 2,312 coefficient identities
and genuine balanced averaging, this proves only the arithmetic families
stated in the revised theorem. A separate audit reproduced the computation
and inference.

## Optimization consequence

Following the perspective review, we computed the palindromic second moment
for De Sa's scaled witness. The revised paper proves that reshuffling is worse
in expected-iterate norm but strictly better in one-epoch expected squared
error and average objective. The proof includes an independent-draw transfer
map and a reshuffling subset recursion; the verifier exhausts all paths. The
claim is expressly instance-specific and finite-horizon.

## Reproducibility and anonymity

All acceptance code fails closed under `python -O`; new orbit-order,
indefinite-PSD, and omitted-path fixtures join the original certificate and
semantic mutations. Manifests are complete in both directions and dependencies
are pinned. Superseded named manuscripts and copied source archives were
removed, leaving one anonymous paper.

## Residual limitations

We agree that deterministic replay is not independent reproduction or peer
review. The paper now says so prominently. Discovery logs, unrestricted m6
positivity, endpoint dual semantics, accountable journal authorship, and
external review remain open.
