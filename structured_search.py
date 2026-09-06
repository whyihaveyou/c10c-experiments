import itertools, numpy as np, cvxpy as cp

def exact(A): return min(max(abs(A@x)) for x in itertools.product((-1,1), repeat=A.shape[1]))
def sdp(A):
 n=A.shape[1]; X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
 c=[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in A]
 p=cp.Problem(cp.Minimize(z),c); p.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8)
 return np.sqrt(z.value)
H2=np.array([[1,1],[1,-1]])
H4=np.kron(H2,H2); H8=np.kron(H4,H2)
ones=np.ones((8,8),int)
rng=np.random.default_rng(1)
matrices={'Hadamard-8':H8,'all-ones':ones,'block-Hadamard':np.block([[H4,H4],[H4,-H4]]),'random-1':rng.choice((-1,1),(8,8)),'random-2':rng.choice((-1,1),(8,8))}
for name,A in matrices.items():
 d=exact(A); v=sdp(A); print(f'{name:16s} exact={d} exact/sqrt8={d/np.sqrt(8):.6f} sdp/sqrt8={v/np.sqrt(8):.6f}')
