# Exact Low-Length Recht--Ré Inequalities

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21709239.svg)](https://doi.org/10.5281/zenodo.21709239)

> **Status: anonymous unrefereed candidate computer-assisted manuscript,
> version 1.0.0-candidate.**
> Exact fresh-extraction replay and internal adversarial audits passed. This
> is not formal proof-assistant verification, independent external
> reproduction, expert acceptance, or journal peer review.

This repository contains one unified paper and its exact replication package.
It consolidates sequential OpenAI GPT-5.6 Sol and Anthropic Fable work
recovered from the local source folder, repairs the original verifier
acceptance logic, and extends the research in two directions: exact
six-factor balanced families and an exact bias--mean-square reversal for
quadratic optimization.

## Persistent identifiers

- **Exact version DOI:** [10.5281/zenodo.21709239](https://doi.org/10.5281/zenodo.21709239)
- **All-versions concept DOI:** [10.5281/zenodo.21709238](https://doi.org/10.5281/zenodo.21709238)
- **GitHub repository:** [ipitchford/exact-low-length-recht-re-inequalities](https://github.com/ipitchford/exact-low-length-recht-re-inequalities)
- **Candidate release:** [`v1.0.0-candidate`](https://github.com/ipitchford/exact-low-length-recht-re-inequalities/releases/tag/v1.0.0-candidate)
- **Release certificate:** a separate hash-bound JSON asset accompanying the
  archive, paper, and replay transcript
- **Public readback receipt:** [`PUBLICATION_READBACK.json`](PUBLICATION_READBACK.json)

GitHub published the immutable prerelease at `2026-07-30T20:43:50Z`; Zenodo
registered the archival record at `2026-07-30T20:46:19.604522Z`. The receipt
records the public identifiers, Git objects, asset hashes, and unauthenticated
cross-host verification. None of this post-publication metadata was
retroactively inserted into the immutable tag archive or certificate.

## Main results

For positive semidefinite Hermitian \(A_1,\ldots,A_n\) with
\(\sum_iA_i\preceq nI\), let \(E_{m,n}(A)\) be the sum of all ordered
products with \(m\) distinct indices and let
\((n)_m=n(n-1)\cdots(n-m+1)\).

| Length | Exact candidate result |
|---|---|
| \(m=4\) | \(-(n)_4I\preceq E_{4,n}\preceq(n)_4I\) for every \(n\ge4\) |
| \(m=5\) upper | \(E_{5,n}\preceq(n)_5I\) for every \(n\ge5\) |
| \(m=5\) lower | \(-(n)_5I\preceq E_{5,n}\) for every \(n\ge6\); De Sa's rational \(n=5\) witness proves the threshold sharp |
| \(m=6\) upper | \(E_{6,n}\preceq(n)_6I\) whenever \(7\mid n\) |
| \(m=6\) lower | \(-(n)_6I\preceq E_{6,n}\) whenever \(8\mid n\) |
| \(m=6\) two-sided | The norm inequality holds whenever \(56\mid n\) |

The six-factor statement is deliberately limited to these arithmetic
families. No nonmultiple result, sharp six-factor threshold, or endpoint
counterexample is claimed.

For De Sa's scaled quadratic witness, the paper also proves an exact
one-epoch metric reversal: reshuffling has a larger norm of the expected
iterate than independent with-replacement sampling,
\(19/512>1/32\), while its complete second-moment operator is strictly
smaller. Hence reshuffling has lower expected squared error and average
quadratic objective for every nonzero initial point on this instance.

## Single paper

The only manuscript is:

- `paper/exact_low_length_recht_re.tex`
- `paper/exact_low_length_recht_re.pdf`

The paper and its PDF metadata identify the author as `Anonymous`. Superseded
degree-specific manuscripts and copied source archives are excluded from this
package.

## Full exact replay

With Python 3.11 or newer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r environment/requirements-lock.txt
.venv/bin/python scripts/replay_all.py --python .venv/bin/python
```

The last line of a release-qualifying run is:

```text
PUBLICATION-CANDIDATE REPLAY: PASS
```

The runner enforces one anonymous source/PDF pair with portable paths,
validates complete bidirectional SHA-256 manifests; scans every acceptance
script for optimization-sensitive assertions; checks citations and claim
inventories; runs the \(m=4,5\) arithmetic implementations and
derivations in normal and optimized modes; replays De Sa's witness and both
quadratic metrics; checks the independent semantic bridge; verifies all 2,312
six-factor identities; computes four exact FLINT characteristic-polynomial
PSD certificates; and requires every mutation fixture to fail explicitly.
The length-six characteristic polynomials can take several minutes.

See `REPRODUCIBILITY.md` for commands, environment, expected boundaries, and
independent-audit guidance.

## Package map

```text
paper/                    one anonymous manuscript and PDF
releases/m4/              exact four-factor certificates and verifiers
releases/m5/              exact five-factor certificates, witness, metrics
releases/m6-balanced/     exact six-factor identity and seed-PSD release
scripts/                  common replay, manifests, semantic checks
tests/                    ordinary, semantic, and extension mutations
environment/              pinned exact-arithmetic dependencies
exploratory/m6/           unresolved all-n blocks and endpoint evidence
provenance/               source hashes and transformation history
reviews/                  adversarial and methodology audit record
publication/              editorial handoff material
```

Machine readers should begin with `AI_INDEX.md`, `AI_INDEX.json`,
`STATUS.md`, and the claim-evidence matrices. Release scope and certificate
semantics are summarized in `RELEASE_NOTES.md` and
`certificate/README.md`.

## Assurance and publication boundary

Successful replay proves that this exact package satisfies its encoded
certificate obligations. It is not formal proof-assistant verification,
fully independent reproduction, expert acceptance, or journal peer review.
The numerical discovery searches were not preserved completely.

The package is distributed under the scoped CC0-1.0 dedication described in
`LICENSE` and `PUBLIC_DOMAIN.md`. Accountable authorship, affiliation,
funding/conflict declarations, target-venue submission, and external expert
review remain unresolved. AI systems are disclosed as research tools, not
authors.
