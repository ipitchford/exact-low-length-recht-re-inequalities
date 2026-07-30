# Reproducibility guide

## Reproduced proof obligations

The package deterministically replays:

- all rational free-polynomial coefficient identities for \(m=4,5,6\);
- canonical orbit counts and affine transversals;
- all fixed representation blocks and 102 leading-principal-minor records
  for \(m=4,5\);
- equality-forced kernels and exceptional \(n=4,5\) certificates;
- seed-to-family derivations for \(m=4,5\);
- De Sa's five rational PSD matrices and all 120 distinct products;
- the exact first-moment and one-epoch second-moment quadratic comparisons;
- the 797+211 six-factor orbit coordinates and 2,312 identities;
- four exact full-matrix six-factor seed PSD certificates, including ranks,
  coefficient signs, kernel, denominators, and characteristic fingerprints;
- exactly one anonymous manuscript source/PDF pair with no local-path leakage;
- complete package/release SHA-256 inventories; and
- known-bad mutations under both normal and optimized Python.

No theorem acceptance condition uses floating-point arithmetic or a
tolerance.

## Not reproduced

The historical SDP searches, complete solver environments, and exploration
logs that discovered the rational seeds were not preserved. The package
replays proof certificates, not discovery. The \(m=4,5\) implementations use
different arithmetic engines but share proof conventions; the \(m=6\)
identity and PSD programs check complementary obligations and share an orbit
encoder. None constitutes fully independent external reproduction.

## Tested environment

```text
macOS
CPython 3.13.5
SymPy 1.14.0
mpmath 1.3.0
python-flint 0.8.0
```

The exact dependency pins are in `environment/requirements-lock.txt`.

## Release-qualifying replay

From the package root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r environment/requirements-lock.txt
.venv/bin/python scripts/replay_all.py --python .venv/bin/python
```

The final line must be exactly:

```text
PUBLICATION-CANDIDATE REPLAY: PASS
```

`--skip-mutations` is a development shortcut and ends with an explicit
`NOT RELEASE-QUALIFYING` status. The default per-command timeout is 600
seconds; the exact six-factor PSD stage receives at least 900 seconds.

## Individual exact commands

```bash
.venv/bin/python releases/m4/verifiers/verify_all_n_stdlib.py
.venv/bin/python releases/m4/verifiers/verify_all_n_sympy.py
.venv/bin/python releases/m4/src/derive_parametric_family.py

.venv/bin/python releases/m5/verifiers/verify_m5_restoration_stdlib.py
.venv/bin/python releases/m5/verifiers/verify_m5_restoration_sympy.py
.venv/bin/python releases/m5/src/derive_parametric_family.py
.venv/bin/python releases/m5/counterexamples/verify_n5_lower_counterexample.py

.venv/bin/python releases/m6-balanced/check_parametric_identities.py
.venv/bin/python releases/m6-balanced/certify_base_psd_flint.py
```

The mutation suites are:

```bash
.venv/bin/python tests/negative_controls.py \
  --m4-root releases/m4 --m5-root releases/m5 \
  --python .venv/bin/python
.venv/bin/python tests/semantic_negative_controls.py \
  --python .venv/bin/python
.venv/bin/python tests/extended_negative_controls.py \
  --python .venv/bin/python
```

## Manifests

`MANIFEST.sha256` in each release lists every allowed release file exactly
once. `PACKAGE_MANIFEST.sha256` lists every allowed package file and includes
the child manifests. Validation is bidirectional: unlisted files, stale
entries, duplicate/unsafe paths, empty manifests, and digest mismatches fail.

Rebuild only after an authorized edit:

```bash
.venv/bin/python scripts/rebuild_manifests.py
```

## Outer release certificate

The immutable tag archive cannot contain a certificate that includes the
archive's own digest without creating a circular definition. The release
therefore carries a detached JSON certificate and SHA-256 sidecar beside the
ZIP, PDF, and complete replay transcript. After downloading those assets:

The release ZIP itself is built from the annotated tag, with fixed timestamps,
ordering, compression, and Unix modes:

```bash
python3 scripts/build_release_archive.py \
  --output /outside/the/repository/exact-low-length-recht-re-inequalities-v1.0.0-candidate.zip
```

The builder checks every archived byte and mode against both the complete root
manifest and the tagged Git tree.

```bash
python3 scripts/verify_release_certificate.py \
  --certificate publication-certificate-v1.0.0-candidate.json \
  --sidecar publication-certificate-v1.0.0-candidate.json.sha256 \
  --archive exact-low-length-recht-re-inequalities-v1.0.0-candidate.zip \
  --paper exact-low-length-recht-re-inequalities-v1.0.0-candidate.pdf \
  --replay-log release-replay-v1.0.0-candidate.txt \
  --source-root /path/to/extracted/archive/exact-low-length-recht-re-inequalities-v1.0.0-candidate \
  --repository /path/to/git/clone
```

The final line must be:

```text
PUBLICATION CERTIFICATE: PASS (annotated tag, full Git tree, complete manifest/archive, subjects, and exact replay)
```

This check establishes the declared byte, mode, manifest, and annotated-tag
relationships. The sidecar is a checksum, not a signer identity or digital
signature. Neither establishes mathematical correctness, formal verification,
independent reproduction, or peer review.

## Paper build

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  exact_low_length_recht_re.tex
```

The release process also applies `qpdf --check`, inspects PDF metadata and
text for anonymity, and visually reviews rendered pages.

## Exploratory boundary

`scripts/audit_m6_snapshot.py` never deserializes the three inherited pickle
files. It hashes them and reports the 15 inputs still missing from the
all-\(n\) representation-block program. Those artifacts are not used by the
balanced-family theorem or its replay.

## Recommended external audit

An independent group should derive the free-localizer reductions without
copying the package code, reconstruct at least one \(m=4,5\) symmetry block,
rebuild the \(m=6\) seed matrices with a separate orbit implementation, check
the balanced-coloring scaling, reproduce the De Sa second moments through an
independent recurrence, and retain known-negative controls. Such work should
be described as independent reproduction only if source, implementation, and
review ownership are genuinely separate.
