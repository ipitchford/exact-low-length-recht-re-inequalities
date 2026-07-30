<!-- SPDX-License-Identifier: CC0-1.0 -->

# Outer release certificate

The publication certificate is generated after the immutable Git tag and
tracked-file archive exist. It is therefore distributed beside the archive,
not stored inside the archive whose digest it records.

The certificate binds:

- repository, tag, and exact commit;
- version DOI and Zenodo record URL;
- tracked-file ZIP, anonymous paper PDF, and complete replay transcript;
- every ZIP member and Unix mode against the complete tagged Git tree;
- the complete root package manifest and paper-source hashes;
- exact replay verdict and runtime versions; and
- explicit assurance and non-inference statements.

`scripts/issue_release_certificate.py` creates the canonical JSON certificate
and SHA-256 sidecar. `scripts/verify_release_certificate.py` checks the
certificate against downloaded assets and, when available, a local repository
or extracted package.

The certificate authenticates the stated byte relationships through its
persistent GitHub and Zenodo publication context. It is not a digital
signature, mathematical proof, external reproduction, or peer review. The
detached SHA-256 sidecar detects accidental certificate changes but does not
identify or authenticate a signer.
