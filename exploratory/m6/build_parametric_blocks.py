#!/usr/bin/env python3
"""Build exact polynomial representation blocks by partial-matching orbit counts.

For two word-orbit keys, concrete bulk labels can overlap only through a partial
matching.  Each matching contributes a falling factorial in the bulk size.
This gives exact symbolic block entries without interpolation.
"""
from __future__ import annotations
import argparse,json,pickle,itertools,time
from pathlib import Path
from functools import lru_cache
from collections import defaultdict
from fractions import Fraction as F
import sympy as sp
ROOT=Path(__file__).resolve().parent
CERT_ROOT=ROOT.parents[1]/'releases/m6-balanced'
p=argparse.ArgumentParser();p.add_argument('--side',choices=['upper','lower'],required=True);p.add_argument('--type',choices=['G','H'],required=True);p.add_argument('--block',type=int,required=True);args=p.parse_args();side=args.side;typ=args.type;bi=args.block
n=sp.symbols('n');threshold=7 if side=='upper' else 8
with open(ROOT/'orbits.pkl','rb') as f:G,H,PAT,bw=pickle.load(f)
om=G if typ=='G' else H;off=0 if typ=='G' else len(G)

def trim(a):
 a=list(a)
 while len(a)>1 and a[-1]==0:a.pop()
 return a or [F(0)]
def padd(a,b):
 c=[F(0)]*max(len(a),len(b))
 for i,z in enumerate(a):c[i]+=z
 for i,z in enumerate(b):c[i]+=z
 return trim(c)
def pmul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:c[i+j]+=x*y
 return trim(c)
def pscale(a,c):return trim([z*c for z in a])
def pshift(a,k):return [F(0)]*k+list(a)
def to_coeff(expr):
 P=sp.Poly(sp.expand(expr),n,domain=sp.QQ);out=[F(0)]*(P.degree()+1 if P.degree()>=0 else 1)
 for (e,),c in P.terms():out[e]=F(int(c.p),int(c.q))
 return trim(out)
def to_expr(a):return sum(sp.Rational(z.numerator,z.denominator)*n**i for i,z in enumerate(a))

# Parse q_k(n)=p_k(n)/(c_k n^q_k).
Q=[]
for z in json.load(open(CERT_ROOT/f'm6_{side}_parametric_functions.json'))['functions']:
 f=sp.cancel(sp.sympify(z));num,den=map(sp.expand,sp.fraction(f));D=sp.Poly(den,n,domain=sp.QQ);terms=D.terms();assert len(terms)==1,(z,terms);(qpow,),cc=terms[0];Q.append((to_coeff(num),F(int(cc.p),int(cc.q)),qpow))
rec=pickle.load(open(ROOT/f'interpbasis_{typ}_{bi}.pkl','rb'));keys=rec['keys'];V=[[sp.cancel(sp.sympify(z)) for z in row] for row in rec['functions']];O=len(keys);m=len(V[0]);s=[0,1,2,2,3,3,3][bi]

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
def word_from_key(k,mp):
 return tuple(mp[z] if z>=0 else 0 if z==-10 else 100+(-1-z) for z in k)
@lru_cache(None)
def pair_terms(a,b):
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
# Falling factorials (R)_q, where R=n-s for H and n-1-s for G.
offset=s if typ=='H' else 1+s
FALL=[[F(1)]]
for q in range(1,7):FALL.append(pmul(FALL[-1],[F(-offset-(q-1)),F(1)]))
# Clear the rational primitive-basis denominators columnwise.
col_den=[];degs=[];W=[];supp=[]
for j in range(m):
 den=sp.Integer(1);lens=set()
 for a in range(O):
  if V[a][j]!=0:den=sp.lcm(den,sp.fraction(V[a][j])[1]);lens.add(len(keys[a]))
 assert len(lens)==1;degs.append(lens.pop());den=sp.factor(den);col_den.append(den)
 col=[]
 for a in range(O):
  z=sp.cancel(den*V[a][j]);assert sp.fraction(z)[1]==1;col.append(to_coeff(z))
 W.append(col);supp.append([a for a,z in enumerate(col) if z!=[F(0)]])
print('setup',side,typ,bi,'O',O,'m',m,'supports',min(map(len,supp)),max(map(len,supp)),'degs',degs,flush=True)
M=[[None]*m for _ in range(m)];t0=time.time()
for i in range(m):
 for j in range(i,m):
  power=degs[i]+degs[j]+1;z=[F(0)]
  for a in supp[i]:
   for b in supp[j]:
    ww=pmul(W[i][a],W[j][b])
    for idx,qdist,cnt in pair_terms(a,b):
     qp,qc,qpow=Q[off+idx];assert qpow<=power,(i,j,idx,qpow,power)
     term=pmul(ww,FALL[qdist]);term=pmul(term,qp);term=pshift(term,power-qpow);term=pscale(term,F(cnt,1)/qc);z=padd(z,term)
  M[i][j]=M[j][i]=trim(z)
 if i%5==0:print('row',i,'elapsed',time.time()-t0,flush=True)
out={'side':side,'type':typ,'block':bi,'threshold':threshold,'degrees':degs,'column_denominators':list(map(str,col_den)),'entries':[[{'num':[x.numerator for x in z],'den':[x.denominator for x in z]} for z in row] for row in M]}
pickle.dump({'meta':out,'matrix':M},open(ROOT/f'paramblock_{side}_{typ}{bi}.pkl','wb'));json.dump(out,open(ROOT/f'paramblock_{side}_{typ}{bi}.json','w'),indent=2)
print('saved degree',min(len(z)-1 for row in M for z in row),max(len(z)-1 for row in M for z in row),'cache',pair_terms.cache_info(),'elapsed',time.time()-t0)
