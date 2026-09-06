"""Greedy/random search for complement-closed covering codes."""
import itertools, random, math

def bits(n): return list(range(1<<n))
def dist(a,b): return bin(a^b).count("1")
def comp(x,n): return x ^ ((1<<n)-1)
def greedy(n,r,restarts=200):
 U=set(bits(n)); best=None
 for _ in range(restarts):
  uncovered=set(U); centers=[]
  while uncovered and len(centers)<2*n:
   candidates=[x for x in U if x not in centers and comp(x,n) not in centers]
   random.shuffle(candidates)
   x=max(candidates,key=lambda z: sum(dist(z,y)<=r or dist(comp(z,n),y)<=r for y in uncovered))
   centers += [x,comp(x,n)]
   uncovered={y for y in uncovered if dist(y,x)>r and dist(y,comp(x,n))>r}
  if not uncovered and (best is None or len(centers)<len(best)): best=centers
 return best
for n in range(2,13):
 for r in range(0,n//2+1):
  c=greedy(n,r,40)
  if c:
   d=n-2*r; val=d/math.sqrt(max(n,len(c)))
   print(f'n={n:2d} r={r} centers={len(c):2d} candidate={val:.9f}')
