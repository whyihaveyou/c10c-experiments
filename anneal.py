import numpy as np, cvxpy as cp, math
rng=np.random.default_rng(12); n=8
def score(A):
 X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
 p=cp.Problem(cp.Minimize(z),[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in A])
 p.solve(solver='CLARABEL',tol_gap_abs=1e-7,tol_feas=1e-7,tol_gap_rel=1e-7)
 return float(np.sqrt(z.value)/np.sqrt(n))
best=0; bestA=None
for restart in range(3):
 A=rng.choice((-1,1),(n,n)); s=score(A)
 for k in range(40):
  B=A.copy(); i,j=rng.integers(n,size=2); B[i,j]*=-1; q=score(B)
  T=.08*(1-k/40)+.005
  if q>s or rng.random()<math.exp((q-s)/T): A,s=B,q
  
  if s>best: best,bestA=s,A.copy()
 print('restart',restart,'local',s,'global',best)
print('best normalized SDP',best); print(bestA)
