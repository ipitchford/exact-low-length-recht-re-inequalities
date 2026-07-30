# Submission checklist

## Blocking

- [ ] Accountable human author or authors confirmed.
- [ ] Every human author has reviewed and approved the unified theorem and
      executable evidence.
- [ ] Affiliation, corresponding-author email, and ORCID supplied.
- [ ] CRediT roles recorded.
- [ ] Funding and conflict-of-interest declarations completed.
- [ ] AI-use disclosure adapted to the target venue and factually approved.
- [x] Distribution license chosen (scoped CC0-1.0).
- [x] Public repository URL and exact version DOI assigned.
- [ ] Independent expert mathematical audit completed or explicitly submitted
      as a referee task.
- [ ] Literature search refreshed immediately before submission.

## Artifact

- [x] `scripts/replay_all.py` ends in
      `PUBLICATION-CANDIDATE REPLAY: PASS`.
- [x] Package and release manifests validate from a fresh extraction.
- [x] The unified PDF compiles from source and passes structural PDF checks.
- [x] Normal and optimized Python outputs agree.
- [x] Every mutation control fails explicitly.
- [x] Citation-key audit passes with no missing or orphaned items.
- [x] The \(m=6\) theorem wording is restricted to upper \(7\mid n\), lower
      \(8\mid n\), and two-sided \(56\mid n\).
- [x] The one-epoch metric reversal is described as instance-specific, not a
      universal or asymptotic reshuffling theorem.
- [x] Exactly one anonymous manuscript source and PDF are present.
- [x] No absolute local paths, temporary files, credentials, signed download
      URLs, or untrusted build artifacts are present.

## Editorial

- [ ] Journal class/style and bibliography format applied.
- [ ] Abstract and keywords meet venue limits.
- [ ] Page/word limits checked.
- [ ] Cover letter finalized.
- [x] Data/code availability statement includes repository, DOI, version, and
      license.
- [ ] Supplementary files are named and cross-referenced consistently.
- [ ] Blind-review metadata applied if required.
