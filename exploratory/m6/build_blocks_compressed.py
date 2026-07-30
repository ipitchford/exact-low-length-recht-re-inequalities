#!/usr/bin/env python3
from __future__ import annotations
import argparse,pickle,itertools,math,ast
from pathlib import Path
from functools import lru_cache
from collections import defaultdict
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--n',type=int,required=True);p.add_argument('--out',required=True);args=p.parse_args();N=args.n
with open(ROOT/'orbits.pkl','rb') as f:G,H,PAT,bw=pickle.load(f)

def canon(left,right,stab):
 def enc(a,b):
  rel={0:0} if stab else {};nxt=1 if stab else 0;out=[]
  for z in list(a)+[-999]+list(b):
   if z==-999:out.append(-1);continue
   if z not in rel:rel[z]=nxt;nxt+=1
   out.append(rel[z])
  return tuple(out)
 return min(enc(left,right),enc(right,left))
def rbulk(k):
 z=[x for x in k if x>=0];return max(z)+1 if z else 0
def word_from_key(k,mp):return tuple(mp[z] if z>=0 else 0 if z==-10 else 100+(-1-z) for z in k)
def falling(R,q):return math.prod(R-j for j in range(q))
allmaps=[];meta=[];kernel_G0=None
for typ,om in [('G',G),('H',H)]:
 for bi in range(7):
  rec=pickle.load(open(ROOT/f'interpbasis_{typ}_{bi}.pkl','rb'));keys=rec['keys'];V=np.array([[float(sp.sympify(z).subs({'n':N})) for z in row] for row in rec['functions']]);O,m=V.shape;s=[0,1,2,2,3,3,3][bi];R=N-s if typ=='H' else N-1-s
  @lru_cache(None)
  def terms(a,b):
   ka,kb=keys[a],keys[b];ra,rb=rbulk(ka),rbulk(kb);start=1 if typ=='G' else 0;agg=defaultdict(int)
   for h in range(min(ra,rb)+1):
    for As in itertools.combinations(range(ra),h):
     for Bs in itertools.combinations(range(rb),h):
      for perm in itertools.permutations(As):
       mt=dict(zip(Bs,perm));am={i:start+i for i in range(ra)};nxt=start+ra;bm={}
       for j in range(rb):
        if j in mt:bm[j]=am[mt[j]]
        else:bm[j]=nxt;nxt+=1
       idx=om[canon(word_from_key(ka,am),word_from_key(kb,bm),typ=='G')];agg[(idx,ra+rb-h)]+=1
   return tuple((idx,q,c) for (idx,q),c in agg.items())
  supp=[[a for a in range(O) if abs(V[a,j])>1e-15] for j in range(m)];C=np.zeros((m,m,len(om)))
  for i in range(m):
   for j in range(i,m):
    z=np.zeros(len(om))
    for a in supp[i]:
     for b in supp[j]:
      w=V[a,i]*V[b,j]
      for idx,q,c in terms(a,b):z[idx]+=w*c*falling(R,q)
    C[i,j]=z;C[j,i]=z
  sizes=np.array([falling(R,rbulk(k)) for k in keys],dtype=float);Gram=V.T@(sizes[:,None]*V);ev,U=np.linalg.eigh((Gram+Gram.T)/2);assert ev[0]>1e-9,(typ,bi,ev[0]);T=(U*(1/np.sqrt(ev)))@U.T;C=np.einsum('ai,abk,bj->ijk',T,C,T,optimize=True);C=(C+C.transpose(1,0,2))/2
  # In the unnormalised trivial G block, the all-ones word vector has
  # coordinate vector 1.  After the congruence V -> V T its coordinate
  # vector is k=T^{-1}1.  Store it: both the equality-kernel equations
  # and the corank-one quotient must use k rather than the coordinate ones.
  if typ=='G' and bi==0:
   kernel_G0=np.linalg.solve(T,np.ones(m))
   assert np.max(np.abs(V@T@kernel_G0-1.0))<1e-9
  allmaps.append(C);meta.append((typ,bi,s,(),m));print(typ,bi,m,'gram',ev[0],ev[-1],flush=True)
assert kernel_G0 is not None
np.savez_compressed(ROOT/args.out,**{f'C{i}':z for i,z in enumerate(allmaps)},meta=np.array([repr(z) for z in meta]),kernel_G0=kernel_G0);print('saved',ROOT/args.out)
