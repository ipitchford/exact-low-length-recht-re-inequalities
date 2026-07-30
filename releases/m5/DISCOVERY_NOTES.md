# Discovery and reconstruction notes

The proof search used the symmetry-reduced affine Gram system. Numerical feasibility supplied only approximate values for a selected transversal of free orbit coordinates. Those coordinates were rounded to a small rational grid; every remaining coordinate was then reconstructed by exact rational linear algebra and accepted only after exact identity and positivity checks.

During release hardening, an unpublished working directory was lost in a runtime reset. The `n=6` upper and lower seeds in this archive were subsequently rediscovered from the defining affine system and positivity constraints rather than recovered from that snapshot. They are a different exact feasible point. Their six-block continuations again satisfy all identities and yield the same uniform positivity structure. This accidental second construction is useful provenance evidence, but it is not treated as an independent audit because the reconstruction used the same mathematical architecture.

The release deliberately separates discovery from proof:

- no numerical solver is called by `verify.sh`;
- the exact seeds are fully printed and machine-readable;
- all affine ranks, identities, blocks, determinants, and kernels are recomputed;
- `derive_parametric_family.py` rederives the complete family from the exact seeds alone.
