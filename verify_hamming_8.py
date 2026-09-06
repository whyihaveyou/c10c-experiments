"""Exhaustive verifier for PR #170's 8x8 Hamming-code certificate."""
from itertools import product
import numpy as np
A=np.array([
[1,1,1,1,1,1,1,0],[1,1,1,-1,-1,-1,-1,0],[1,1,-1,1,-1,-1,1,0],[1,1,-1,-1,1,1,-1,0],
[1,-1,1,1,-1,1,-1,0],[1,-1,1,-1,1,-1,1,0],[1,-1,-1,1,1,-1,-1,0],[1,-1,-1,-1,-1,1,1,0]])
vals=[max(abs(A@x)) for x in product((-1,1),repeat=8)]
assert min(vals)==5
assert {v:vals.count(v) for v in set(vals)} == {5:224,7:32}
print('verified: shape=%s discrepancy=5 distribution={5:224, 7:32}' % (A.shape,))
print('lower bound = 5/sqrt(8) = %.12f' % (5/np.sqrt(8)))
