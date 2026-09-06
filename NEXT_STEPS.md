# Next research steps for C_10c

## Current status

- Existing record: `7/sqrt(17) ~= 1.697749` for sign matrices.
- PR #170 proposes `5/sqrt(8) ~= 1.767767` using an allowed `{-1,0,1}` matrix; exhaustive verification is in `verify_hamming_8.py`.
- Our SDP/search experiments have not produced a universal-bound improvement.

## Prioritized work

1. Verify the interpretation of `A in [-1,1]^(n x n)` with the maintainers after PR #170; distinguish the general and sign-matrix variants explicitly.
2. Build a covering-code enumerator for lengths `n <= 20`, including complement-closed codes, to search for further certified lower bounds.
3. Use SDP only as a screening objective; every candidate must pass exact enumeration or a hand-checkable covering argument.
4. Keep code/data external to the main repository and pin releases with a checksum.
5. Submit a Markdown-only PR updating the constant page, README table, Recent progress, and bibliography.

## Publication threshold

A routine correction or finite certificate needs only a repository PR. A new
construction or method should additionally have a technical note or arXiv
preprint with the proof, search method, and reproducibility package. A journal
paper is appropriate only after the result is mathematically novel beyond the
finite certificate itself.
