import numpy as np, cvxpy as cp
rng=np.random.default_rng(33); n=8
A=np.array([[-1,-1,-1,-1,1,1,-1,1],[1,-1,1,-1,-1,1,-1,1],[-1,-1,1,-1,-1,-1,1,1],[-1,-1,1,-1,1,1,-1,-1],[1,1,-1,-1,1,1,-1,-1],[1,-1,-1,1,-1,-1,1,-1],[1,-1,1,1,1,-1,1,1],[-1,-1,1,1,1,-1,1,-1]])
def score(B):
 m=B.shape[0]; X=cp.Variable((m,m),symmetric=True); z=cp.Variable(nonneg=True)
 p=cp.Problem(cp.Minimize(z),[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in B]); p.solve(solver='CLARABEL',tol_gap_abs=2e-6,tol_feas=2e-6,tol_gap_rel=2e-6)
 return float(np.sqrt(z.value)/np.sqrt(m))
B=np.block([[A,A],[A,-A]]); best=score(B); print('base',best)
for k in range(20):
 C=B.copy()
 for _ in range(4):
  i,j=rng.integers(16,size=2); C[i,j]*=-1
 q=score(C)
 if q>best: best=q; B=C; print('improved',k,best)
print('best',best)
