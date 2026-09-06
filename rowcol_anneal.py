import numpy as np, cvxpy as cp, math
rng=np.random.default_rng(42); n=8
def score(A):
 X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
 p=cp.Problem(cp.Minimize(z),[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in A]); p.solve(solver='CLARABEL',tol_gap_abs=1e-7,tol_feas=1e-7,tol_gap_rel=1e-7)
 return float(np.sqrt(z.value)/np.sqrt(n))
best=0
for r in range(4):
 A=rng.choice((-1,1),(n,n)); s=score(A)
 for k in range(50):
  B=A.copy(); typ=rng.integers(2); idx=rng.integers(n)
  if typ==0: B[idx,:]*=-1
  else: B[:,idx]*=-1
  q=score(B); T=.08*(1-k/50)+.003
  if q>s or rng.random()<math.exp((q-s)/T): A,s=B,q
  if s>best: best=s
 print(r,s,best)
print('best normalized SDP',best)
