import os, numpy as np
n=int(os.environ.get('N','10')); steps=int(os.environ.get('STEPS','2000')); seed=int(os.environ.get('SEED','0')); rng=np.random.default_rng(seed)
S=np.array([[(1 if (m>>j)&1 else -1) for j in range(n)] for m in range(1<<n)],dtype=np.int16)
def val(A): return int(np.min(np.max(np.abs(S@A.T),axis=1)))
best=0; bestA=None
for restart in range(4):
 A=rng.choice((-1,1),(n,n)).astype(np.int16); v=val(A)
 for k in range(steps):
  i,j=rng.integers(n,size=2); A[i,j]*=-1; q=val(A)
  if q>=v or rng.random()<0.002: v=q
  else: A[i,j]*=-1
  if v>best: best,bestA=v,A.copy()
print(f'n={n} seed={seed} discrepancy={best}',flush=True)
print(bestA.tolist(),flush=True)
