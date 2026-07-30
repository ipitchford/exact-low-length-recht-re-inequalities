<!-- SPDX-License-Identifier: CC0-1.0 -->

# AI evidence index

This file routes human and machine readers to the exact claim, proof, replay,
and limitation records. It does not assess mathematical truth beyond the
stated evidence.

## Canonical reading order

1. `paper/exact_low_length_recht_re.pdf` -- the sole manuscript.
2. `STATUS.md` -- release status and non-claims.
3. `reviews/CLAIM_EVIDENCE_MATRIX.md` -- claim-to-evidence map.
4. `REPRODUCIBILITY.md` and `REPLAY_RECEIPT_2026-07-30.md` -- complete replay.
5. `releases/m4/`, `releases/m5/`, and `releases/m6-balanced/` -- exact
   certificates and specialized verifiers.
6. `scripts/check_semantic_bridge.py` -- concrete group-action and
   representation-map reconstruction.
7. `tests/` -- required rejection controls.
8. `provenance/SOURCE_PROVENANCE.md` and `reviews/` -- source lineage and
   internal audit record.

## Claim classes

| ID | Claim | Evidence |
|---|---|---|
| C1 | Two-sided four-factor inequality for every \(n\ge4\) | exact parametric certificates, endpoint certificates, semantic bridge |
| C2 | Five-factor upper inequality for every \(n\ge5\) | exact parametric and endpoint certificates |
| C3 | Five-factor lower inequality for every \(n\ge6\) | exact parametric certificates |
| C4 | Failure of the five-factor lower inequality at \(n=5\) | De Sa rational witness, all 120 products, exact eigenvalue |
| C5 | Six-factor upper inequality whenever \(7\mid n\) | 1,156 identities, exact \(n=7\) seed PSD, balanced continuation |
| C6 | Six-factor lower inequality whenever \(8\mid n\) | 1,156 identities, exact \(n=8\) seed PSD, balanced continuation |
| C7 | Two-sided six-factor inequality whenever \(56\mid n\) | conjunction of C5 and C6 |
| C8 | One-epoch bias--mean-square reversal on the five-matrix witness | exact first moment, all 120 reshuffling paths, all \(5^5\) independent paths |

## Non-inference rules

- A matching hash establishes byte identity, not mathematical correctness.
- A passing certificate checker does not alone validate its encoding.
- Mutation rejection strengthens a verifier audit but does not prove the
  verifier correct.
- The six-factor result does not cover nonmultiples of seven or eight.
- The optimization result is instance-specific and one-epoch.
- Internal model cross-checks are not independent external reproduction.
- A DOI, GitHub release, or public archive does not constitute peer review.

The canonical machine-readable form is `AI_INDEX.json`.
