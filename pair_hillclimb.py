import numpy as np, cvxpy as cp
rng=np.random.default_rng(7); n=8
def score(A):
 X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
 p=cp.Problem(cp.Minimize(z),[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in A])
 p.solve(solver='CLARABEL',tol_gap_abs=1e-7,tol_feas=1e-7,tol_gap_rel=1e-7)
 return float(np.sqrt(z.value)/np.sqrt(n))
best=0
for restart in range(5):
 A=rng.choice((-1,1),(n,n)); s=score(A)
 for step in range(30):
  inds=rng.choice(n*n,2,replace=False); B=A.copy()
  for q in inds: B[q//n,q%n]*=-1
  q=score(B)
  if q>s: A,s=B,q
  best=max(best,s)
 print(f'restart={restart} best_local={s:.9f} global={best:.9f}')
print('best normalized SDP',best)
