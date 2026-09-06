import numpy as np, cvxpy as cp
rng=np.random.default_rng(4); n=8
def score(A):
 X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
 p=cp.Problem(cp.Minimize(z),[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in A])
 p.solve(solver='CLARABEL',tol_gap_abs=1e-7,tol_feas=1e-7,tol_gap_rel=1e-7)
 return float(np.sqrt(z.value)/np.sqrt(n))
bestA=rng.choice((-1,1),(n,n)); best=score(bestA)
for restart in range(3):
 A=rng.choice((-1,1),(n,n)); s=score(A)
 for step in range(20):
  i,j=rng.integers(n,size=2); B=A.copy(); B[i,j]*=-1; q=score(B)
  if q>s: A,s=B,q
  if s>best: best,bestA=s,A.copy(); print(f'best restart={restart} step={step} normalized_sdp={best:.9f}')
print('final',best)
print(bestA)
