import itertools, numpy as np, cvxpy as cp
rng=np.random.default_rng(0)
def exact(A):
 n=A.shape[1]; return min(max(abs(A@x)) for x in itertools.product((-1,1), repeat=n))
def sdp(A):
 n=A.shape[1]; X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
 cons=[X>>0,cp.diag(X)==1]
 for a in A: cons += [cp.quad_form(a,X)<=z]
 p=cp.Problem(cp.Minimize(z),cons); p.solve(solver='CLARABEL',tol_gap_abs=1e-7,tol_feas=1e-7,tol_gap_rel=1e-7)
 return float(np.sqrt(z.value))
best=[]
for k in range(30):
 n=8; A=rng.choice((-1,1),size=(n,n)); d=exact(A); v=sdp(A)
 best.append((v/np.sqrt(n),d/np.sqrt(n),d,v,A))
best.sort(reverse=True,key=lambda x:x[0])
for i,(q,e,d,v,A) in enumerate(best[:5]): print(f'#{i}: sdp/sqrt(n)={q:.6f}, exact/sqrt(n)={e:.6f}, exact={d}, sdp={v:.6f}')
