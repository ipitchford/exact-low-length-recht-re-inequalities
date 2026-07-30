# Unified exact replay receipt

**Candidate version:** 1.0.0-candidate  
**Replay date:** 30 July 2026  
**Platform:** macOS  
**Interpreter:** CPython 3.13.5  
**Dependencies:** SymPy 1.14.0, mpmath 1.3.0, python-flint 0.8.0  
**Canonical result:** `PUBLICATION-CANDIDATE REPLAY: PASS`

## Canonical command

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r environment/requirements-lock.txt
.venv/bin/python scripts/replay_all.py --python .venv/bin/python
```

## Exact results bound by the replay

- m4: 152 coefficient identities, 162 orbit functions, 51 minor records,
  775 positive shifted coefficients, both \(n=4\) endpoints, and all three
  exact replay paths passed in normal and optimized Python.
- m5: 152 identities, 162 orbit functions, 51 minor records, 929 positive
  shifted coefficients, the upper \(n=5\) endpoint, and all three exact replay
  paths passed in both modes.
- De Sa witness: five rational PSD matrices, mean \(I\), all 120 products,
  eigenvalue \(-285/2<-120\), and the \(19/512>1/32\) expected-iterate
  reversal passed exactly.
- Second moment: all 120 reshuffling and 3,125 independent paths yielded
  \[
  M_{\rm RR}=\frac{1435}{1048576}P_\perp+
  \frac{421}{131072}P_{\mathbf1},
  \]
  \[
  M_{\rm WR}=\frac{365}{65536}P_\perp+
  \frac{91}{8192}P_{\mathbf1},
  \]
  with a strictly positive projector gap.
- m6 identity layer: 1,156 rational equations passed for each sign.
- m6 seed PSD: upper \(G,H\) at \(n=7\) had ranks 399 and 400 at size 400;
  lower \(G,H\) at \(n=8\) had rank 585 at size 585. Every
  \(\det(tI+A)\) coefficient had the required sign, the upper all-ones kernel
  passed, and all four raw characteristic-list digests matched.
- Semantic bridge: literal group actions, all concrete word patterns,
  representation spans/ranks, finite-difference degree bounds, seven concrete
  identities, and fourteen exact full-Gram LDL tests passed.
- Negative controls: certificate-field, semantic, m6 coordinate-order,
  indefinite-PSD, and omitted-path fixtures were explicitly rejected in
  normal and optimized Python.
- Environment, citation keys, claim inventories, acceptance-code safety,
  package hygiene, three child manifests, and the root package manifest
  passed.

## Source lineage

The authoritative inherited archives were identified before consolidation:

```text
m4 v1.1  520d9385e7f0a587776007b785c56899de0c6293eb35645fe099f02d4053c329
m5 v1.0  fa2407ebc3d17ae3007720ade08a49da05a10701ada550a2a85be7185bd3d446
```

The copied archives and their duplicate named manuscripts are not included in
the anonymous package. See `provenance/SOURCE_PROVENANCE.md`.

## Independent read-only audits

- Domain, methodology, optimization-perspective, clean-room, and adversarial
  round-1 reports found no m4/m5 theorem falsification and drove the semantic
  and packaging revisions.
- `reviews/peer_review/m6_balanced_audit.md` independently reproduced the
  six-factor identities, FLINT conventions, all ranks/digests, upper kernel,
  and balanced inference.
- A separate exact implementation reproduced both second-moment operators and
  their positive-definite gap.
- The post-revision mathematical audit found no actionable defect and
  confirmed a clean anonymous 21-page PDF.

## Assurance boundary

This receipt records deterministic replay of the specified package. It is not
formal verification, independent external reproduction, accountable
authorship, expert acceptance, publication-priority proof, or journal peer
review. Historical numerical discovery and unrestricted six-factor
positivity remain outside the reproduced claims.
