# Exploratory six-factor all-\(n\) and endpoint work

The theorem-grade part of the inherited six-factor snapshot has been promoted
to `../../releases/m6-balanced`. That release exactly proves:

- the upper bound on multiples of 7;
- the lower bound on multiples of 8; and
- the two-sided norm inequality on multiples of 56.

This directory now contains only unresolved extensions:

1. representation-block builders aimed at positivity for every stable
   integer \(n\); and
2. three dual-looking endpoint records whose mathematical implication has not
   been reconstructed.

Nothing here is used by a theorem acceptance path.

## Missing all-\(n\) inputs

The exact block builder still lacks:

```text
orbits.pkl
interpbasis_G_0.pkl ... interpbasis_G_6.pkl
interpbasis_H_0.pkl ... interpbasis_H_6.pkl
```

These 15 files are required to generate the 28 parametric block records and
their Newton-minor positivity records. Their absence prevents a claim at
nonmultiples of 7 or 8, despite the released rational identities holding at
stable pole-free integers.

The exploratory builders now read the promoted rational function JSON from
`../../releases/m6-balanced`; they still cannot run without the inputs above.
`probe_base_psd.py` is floating-point reconnaissance only and is superseded at
the two seeds by the exact FLINT release verifier.

## Endpoint records

| File | SHA-256 | Putative role |
|---|---|---|
| `upper_dual_G.pkl` | `1b950e706aef2cfda6fd386ef4d96c2074e6aeb12939f58a2b2f85990b2ff128` | upper \(n=6\) SOS obstruction |
| `lower_dual_G.pkl` | `32887c4d6419cf67f471437b096697ea43d54810a02c0afb2ff6dc321c37c4df` | lower \(n=6\) SOS obstruction |
| `n7_lower_dual_G.pkl` | `fa8ce8394ceaa553bd8e93084afcd9e5eafdc56b834b6a5e8b96133912b4e4ba` | lower \(n=7\) SOS obstruction |

The affine systems, objective sign convention, and semantic implication are
missing. An obstruction to this truncated free-SOS ansatz is not by itself a
counterexample to the matrix inequality. No endpoint failure or sharp
six-factor threshold is claimed.

## Safe pickle boundary

Pickle is executable. The package audit hashes these files but never
deserializes them. A prior bounded opcode scan at the listed hashes found only
primitive-container opcodes, but the public acceptance path deliberately
does not rely on that result. Any future release should convert recovered
records to canonical non-executable JSON and add schema, identity, positivity,
objective, and mutation checks.

## Most valuable next work

1. Reconstruct the 15 missing representation inputs from transparent,
   non-pickle generators.
2. Produce all 28 exact blocks and prove every integer-\(n\) minor condition.
3. Reconstruct the endpoint dual affine systems and determine whether they
   imply only SOS infeasibility or actual finite-dimensional failure.
4. Seek explicit rational matrix witnesses for any claimed endpoint failure.
5. Build a genuinely separate orbit implementation for external reproduction.

See `RECONSTRUCTION_AUDIT.md` for the pre-promotion ordering audit.
