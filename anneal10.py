import itertools, math, numpy as np, cvxpy as cp
rng=np.random.default_rng(21); n=10
def score(A):
 X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
 p=cp.Problem(cp.Minimize(z),[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in A])
 p.solve(solver='CLARABEL',tol_gap_abs=2e-7,tol_feas=2e-7,tol_gap_rel=2e-7)
 return float(np.sqrt(z.value)/np.sqrt(n))
def exact(A): return min(max(abs(A@x)) for x in itertools.product((-1,1),repeat=n))
best=0; bestA=None
for restart in range(2):
 A=rng.choice((-1,1),(n,n)); s=score(A)
 for k in range(20):
  B=A.copy(); i,j=rng.integers(n,size=2); B[i,j]*=-1; q=score(B); T=.1*(1-k/20)+.01
  if q>s or rng.random()<math.exp((q-s)/T): A,s=B,q
  if s>best: best,bestA=s,A.copy()
 print('restart',restart,'local',s,'global',best)
print('best normalized SDP',best,'exact discrepancy',exact(bestA),'exact normalized',exact(bestA)/np.sqrt(n)); print(bestA)
