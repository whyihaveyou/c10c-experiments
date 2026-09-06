"""Bitset-accelerated complement-closed covering-code search."""
import random, math

def search(n,r,restarts=100):
 N=1<<n; ALL=(1<<N)-1; full=(1<<n)-1
 balls=[]
 for c in range(N):
  m=0
  for y in range(N):
   if bin(c^y).count("1")<=r: m|=1<<y
  balls.append(m | ((1<<N)-1 if False else 0))
 best=None
 for _ in range(restarts):
  uncovered=ALL; centers=[]
  while uncovered and len(centers)<2*n:
   cand=[c for c in range(N) if c not in centers and (c^full) not in centers]
   random.shuffle(cand)
   c=max(cand,key=lambda x:bin(((balls[x]|balls[x^full]) & uncovered)).count("1"))
   centers += [c,c^full]; uncovered &= ~(balls[c]|balls[c^full])
  if not uncovered and (best is None or len(centers)<len(best)): best=centers
 return best
for n in range(2,13):
 for r in range(n//2+1):
  c=search(n,r,30)
  if c: print(f'n={n} r={r} centers={len(c)} candidate={(n-2*r)/math.sqrt(max(n,len(c))):.9f}')
