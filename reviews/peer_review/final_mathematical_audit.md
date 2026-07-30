# Final mathematical audit

**Audit date:** 30 July 2026  
**Decision:** Clean; no actionable mathematical or publication-integrity
defect found.

## Scope

Read-only re-review of the final paper source and compiled PDF, focused on the
publication-metadata changes made after the full theorem audit. The comparison
baseline was the previously audited PDF. The new wording identifies the
anonymous public candidate, exact version, repository, DOI, scoped CC0
dedication, certificate, and journal-submission boundary.

## Bound artifacts

- Source: `paper/exact_low_length_recht_re.tex`  
  SHA-256: `3f9279b520fb12a8591a92da750e01e33107566b1336ecb37aedeac4f2c81028`
- PDF: `paper/exact_low_length_recht_re.pdf`  
  SHA-256: `d02949d1a6bd61244a07d0428bec8079a656e78fed17e9bd459ff7d9b120148b`

## Checks and results

- The new edits are confined to release metadata, attribution/disclosure
  wording, and deterministic-PDF primitives. No theorem, equation, numerical
  value, proof, or mathematical citation changed.
- The characteristic-polynomial digest description now specifies
  newline-separated ASCII integers **with no trailing newline**. This matches
  the verifier's exact `"\n".join(...)` serialization.
- The reproducibility sentence now accurately refers to plural release
  receipts, source-archive hashes, manifest bindings, and command/output
  summaries. It introduces no stronger replay or independence claim.
- The current PDF has 21 pages, anonymous author metadata, and no occurrence
  of the user's name. `qpdf --check` reports no syntax or stream-encoding
  error. Consecutive forced builds under the pinned TeX environment produced
  the same PDF SHA-256.
- Text extraction confirms that the four/five-factor thresholds, the
  six-factor \(7\), \(8\), and \(56\) divisibility scope, and the exact
  \(19/512>1/32\) metric reversal remain unchanged.
- The public release label `Anonymous` is explicitly separated from
  accountable journal authorship. AI systems remain disclosed as tools and
  are not listed as authors.
- The version DOI, repository, version string, scoped CC0 statement, and
  detached-certificate boundary are consistent with the machine-readable
  release metadata.
- The prior theorem audit therefore carries over unchanged: the balanced
  continuation scaling, six-factor divisibility inference, characteristic-
  polynomial PSD criterion, De Sa first moment, and one-epoch second-moment
  proposition are unaffected by the final wording pass.

## Assurance boundary

This is an internal exact/read-only audit of a computer-assisted candidate
paper. It is not external peer review, independent external reproduction,
formal proof-assistant verification, or journal acceptance.
