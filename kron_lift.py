import numpy as np, cvxpy as cp
A=np.array([[-1,-1,-1,-1,1,1,-1,1],[1,-1,1,-1,-1,1,-1,1],[-1,-1,1,-1,-1,-1,1,1],[-1,-1,1,-1,1,1,-1,-1],[1,1,-1,-1,1,1,-1,-1],[1,-1,-1,1,-1,-1,1,-1],[1,-1,1,1,1,-1,1,1],[-1,-1,1,1,1,-1,1,-1]])
H=np.array([[1,1],[1,-1]]); B=np.kron(A,H); n=B.shape[1]
X=cp.Variable((n,n),symmetric=True); z=cp.Variable(nonneg=True)
p=cp.Problem(cp.Minimize(z),[X>>0,cp.diag(X)==1]+[cp.quad_form(a,X)<=z for a in B])
p.solve(solver='CLARABEL',tol_gap_abs=1e-6,tol_feas=1e-6,tol_gap_rel=1e-6)
print('shape',B.shape,'normalized SDP',float(np.sqrt(z.value)/np.sqrt(n)))
