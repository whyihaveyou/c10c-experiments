"""Vector (SDP) relaxation for discrepancy of the 17x17 certificate.

The relaxation replaces signs x_j in {+-1} by unit vectors v_j and minimizes
max_i ||sum_j a_ij v_j||_2. Its optimum is a rigorous lower bound on the
(discrete) discrepancy, since scalar signs are a special case of unit vectors.
"""
from pathlib import Path
import cvxpy as cp
import numpy as np

source = Path(__file__).parents[1] / "optimizationproblems/constants/10c.md"
text = source.read_text()
block = text.split("## Certificate for the $7/\\sqrt{17}$ lower bound", 1)[1].split("```text", 1)[1].split("```", 1)[0]
A = np.array([[int(x) for x in line.split()] for line in block.splitlines() if line.strip()], dtype=float)
n, d = A.shape
X = cp.Variable((n, n), symmetric=True)  # Gram matrix of unit vectors
constraints = [X >> 0, cp.diag(X) == 1]
t2 = cp.Variable(nonneg=True)
# ||sum_j a_ij v_j||^2 = a_i X a_i^T
for row in A:
    constraints.append(cp.quad_form(row, X) <= t2)
problem = cp.Problem(cp.Minimize(t2), constraints)
problem.solve(solver=cp.SCS, eps=1e-7, max_iters=200000, verbose=False)
print(f"status={problem.status} sdp_vector_bound={np.sqrt(t2.value):.9f} normalized={np.sqrt(t2.value)/np.sqrt(n):.9f}")
