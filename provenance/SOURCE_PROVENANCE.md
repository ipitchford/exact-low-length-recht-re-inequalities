# Source provenance

## Import boundary

The consolidation began from the local `LaiLim` source folder on 30 July
2026. The
original directory was not a Git repository. It contained:

- an \(m=4\) version 1.0 archive and loose files;
- a hardened \(m=4\) version 1.1 archive;
- an \(m=5\) version 1.0 archive, loose files, and a partial byte-identical
  mirror; and
- an incomplete \(m=6\) working directory, subsequently mined for the
  balanced-family theorem layer.

The publication candidate imports the complete \(m=4\) v1.1 and \(m=5\) v1.0
archives as the authoritative baselines. Loose duplicates and partial mirrors
are not treated as independent evidence.

## Original authoritative artifacts

| Artifact | SHA-256 |
|---|---|
| `Part 1 hardened/recht_re_m4_all_n_exact_bundle_v1.1.zip` | `520d9385e7f0a587776007b785c56899de0c6293eb35645fe099f02d4053c329` |
| `Part 1 hardened/recht_re_m4_all_n(1).pdf` | `4d47624ea830b5aabc6b0a690305b460595ad8f05b0ce3c7e952a9aca4dbc8ba` |
| `Part_2/recht_re_m5_restoration_exact_bundle_v1.0.zip` | `fa2407ebc3d17ae3007720ade08a49da05a10701ada550a2a85be7185bd3d446` |
| `Part_2/recht_re_m5_restoration.pdf` | `c1a7a8e774c683c5c4de5bedb0825840c4e1354d7665bd3cd0b56f9a8fa549f7` |
| `Part_2/recht_re_m5_restoration.tex` | `0f1872c0a01da5da12ec888dbdc79a40b60ef53369f85932dde2d16a98da19a1` |

The original \(m=4\) v1.0 outer `.sha256` sidecar embeds a non-portable
absolute path and therefore does not validate verbatim on this Mac. Its
archive hash was independently recomputed as
`f7ebc1ac185403ca430b75262de29ce9e9aec3b171a9fa61858ecd30c0c27c20`.
The internal manifests of the authoritative v1.1 and v1.0 archives validated
before consolidation.

## Sequential contribution record

The inherited files describe:

- human research direction, with identity withheld from the anonymous package;
- OpenAI GPT-5.6 Sol: mathematical construction, exact certificate code, and
  manuscript drafting; and
- Anthropic Fable: an adversarial audit of earlier \(m=4\) work, recovery of
  the relevant Zhang lifting route, and exact checks at selected fixed values
  of \(n\).

Fable did not audit the complete uniform \(m=4\) minor inventory and did not
audit the \(m=5\) proof. The bundled verifiers are internal executable evidence,
not an external author or reviewer.

## Consolidation transformations

The candidate repository:

1. extracted the authoritative archives;
2. preserved all exact certificate data;
3. replaced optimization-sensitive acceptance assertions with explicit
   verification exceptions;
4. added mutation-based negative controls;
5. corrected and audited bibliographic metadata;
6. added a common replication, provenance, and claim-boundary layer; and
7. reconstructed exact \(m=6\) identities and full seed PSD certificates,
   promoting only the balanced-family theorem layer;
8. added the exact one-epoch bias--mean-square reversal for De Sa's quadratic
   witness; and
9. retained the incomplete all-\(n\) and endpoint \(m=6\) artifacts as a
   separate exploratory boundary.

The copied source archives and legacy manuscripts are intentionally excluded
from the anonymous public package because they embed superseded attribution
and duplicate papers. They remain recoverable from the private local source
folder at the hashes above. The repaired releases have new manifests. Their
provenance is the combination of this record, the original hashes, and the
repository commit history.
