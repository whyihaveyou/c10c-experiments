# C_10c experiments

This directory is external to the `optimizationproblems` checkout, following
its contribution policy for scripts and data. The target is the open issue
[#67](https://github.com/teorth/optimizationproblems/issues/67): numerical SDP
relaxations for the Spencer discrepancy constant.

The first milestone is an exact verifier for the existing 17 x 17 certificate
(the known lower bound `7/sqrt(17)`). Only after that baseline passes should we
compare CVXPY/SCS relaxations on the same matrix and on generated adversarial
systems.

## Initial search result

`search_small.py` samples 30 random 8 x 8 sign matrices, computes exact discrepancy
by exhaustive enumeration, and solves the vector SDP with Clarabel. The best
sample had SDP value `1.732051 = sqrt(3)`, i.e. normalized SDP lower bound
`0.612372`; its exact discrepancy was `2` (`0.707107` normalized). This is a
screening result only, not a new bound for C_10c.

## Structured baseline

`structured_search.py` compares interpretable 8 x 8 families. The Hadamard and
block-Hadamard matrices attain SDP value `sqrt(8)` (normalized `1.0`) while
random samples are lower (`0.366` in one sample). The all-ones matrix has zero
discrepancy. This confirms that orthogonality is SDP-hard relative to random
instances, but still far below the Spencer scale; future candidates should add
correlation without the cancellation symmetry of Hadamard matrices.

## Local search result

`hillclimb.py` performs single-entry flips with an SDP objective. In three
restarts on 8 x 8 matrices it found a candidate with normalized SDP value
`0.649468374`, above the random-search best `0.612372` (but below the
Hadamard baseline `1.0`). Exact enumeration gives discrepancy `2`. This is a
heuristic lead only; it does not improve the universal constant.

## Simulated annealing result

`anneal.py` allows uphill moves while cooling. Three short restarts found an
8 x 8 candidate with normalized SDP value `0.679852164`, improving the
single-flip value `0.649468374`. Exact enumeration of the printed candidate
still gives discrepancy `2`; this remains a heuristic SDP lead, not a certified
improvement to C_10c.

## Dimension-10 trial

`anneal10.py` runs two short simulated-annealing restarts at `n=10`. The best
candidate had normalized SDP value `0.566058125` and exact discrepancy `2`.
This is below the best `n=8` candidate, so the current annealing schedule does
not scale automatically; larger runs need better initialization and block
moves.

## Kronecker lift

`kron_lift.py` forms the Kronecker product of the best 8 x 8 annealing
candidate with the 2 x 2 Hadamard matrix. At 16 x 16 the normalized SDP value
is `0.679852197`, essentially identical to the 8 x 8 value. This lift preserves
the relaxation value rather than amplifying it, so plain Kronecker powering is
not a route to a new universal bound.

## Block perturbation trial

`block_perturb.py` starts from the 16 x 16 block matrix
`[[A,A],[A,-A]]` and flips four entries in 20 trials. The base normalized SDP
value is `0.679852197`; no perturbed candidate improved it. Sparse random
cross-block perturbations therefore appear insufficient at this scale.

## Row/column annealing

`rowcol_anneal.py` tests whole-row and whole-column flips with annealing. Four
restarts at `n=8` reached only `0.5` normalized SDP, substantially below the
entry-wise annealing result. Whole row/column sign flips are largely symmetry
moves for this relaxation and are not promising as a standalone search action.

## 2x2 block annealing

`block2_anneal.py` flips contiguous 2 x 2 blocks under an annealing schedule.
Three restarts reached `0.632455533` normalized SDP, below the entry-wise
annealing record `0.679852164`; this move set is not competitive by itself.

## Covering-code search

`covering_search.py` implements a complement-closed greedy covering-code search.
For small dimensions it recovers the zero-slack cases `n=2,r=0` and `n=4,r=1`,
and finds candidate normalized bounds `1.060660` at `n=5,r=1` and `1.154701`
at `n=6,r=1`. The naive Python implementation becomes slow around `n=7`, so
future work should use bitset acceleration or an ILP/SAT formulation.

## Bitset covering search

`covering_bitset.py` precomputes each Hamming ball as an integer bitset. It
scales through `n=10` in a short run and finds, among others, a complement-
closed `n=9,r=2` cover with 16 centers, yielding candidate `1.25`. These
small-dimensional candidates are below the current `5/sqrt(8)` record, but the
bitset implementation is suitable for extending the search and exporting
explicit center certificates.

## Reproduce the deterministic checks

Create an environment with `python -m pip install -r requirements.txt`, then run
`python run_verifiers.py`.  The command checks both the repository's 17 x 17
certificate and the 8 x 8 Hamming-code certificate independently by exhaustive
enumeration.  SDP screening scripts additionally require a working CVXPY solver.

## Remote exact search

`remote_exact_search.py` uses only NumPy and exhaustively evaluates all $2^n$
sign vectors for each candidate matrix. A 32-seed, 4-restart batch at $n=10$
(found by the supplied 64-core host) repeatedly reached discrepancy 4; no
candidate exceeded the verified 8 x 8 Hamming certificate's discrepancy 5.
This negative result helps calibrate the search before investing in SDP solver
installation on the cluster.

A second dependency-free batch on the supplied 64-core host used $n=11$, 16
seeds, four restarts, and 1500 single-entry flips per restart. Every run's
best exact discrepancy was 3, so this schedule did not approach the 8 x 8
Hamming construction; the raw matrices remain on the host for follow-up.

## Slurm batch record

The 32-seed $n=10$ batch was subsequently run correctly as Slurm array job
`65861886` on `xahcnormal` (one task and 16 CPUs per array element; the login
node only submitted and queried the job). All 32 tasks completed in 9--11 s and
all reached exact discrepancy 4. No candidate improved the existing certificate.

A Slurm array batch `65862318` then tested $n=12$ (32 seeds, 4 restarts, 3000
flips). All 32 completed on `xahcnormal` in 12--14 s and reached discrepancy 4;
no candidate improved the known certificates.
