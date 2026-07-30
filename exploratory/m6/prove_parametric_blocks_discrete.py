#!/usr/bin/env python3
"""Exact integer-n positivity proof by Newton-series coefficients.

After a positive scalar/congruence scaling, every representation block is a
polynomial matrix M(n).  A leading principal determinant p(n) has degree at
most k*d, where d is the largest entry degree.  Exact values at consecutive
integers determine its Newton expansion
    p(N+t)=sum_j Delta^j p(N) * binom(t,j).
Nonnegative forward differences, with p(N)>0, prove p(N+t)>0 for every integer
t>=0.  This avoids symbolic determinant swell while remaining exact.
"""
from __future__ import annotations
import argparse,pickle,json,gzip,math,time
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--side',choices=['upper','lower'],required=True);p.add_argument('--type',choices=['G','H'],required=True);p.add_argument('--block',type=int,required=True);args=p.parse_args();side=args.side;typ=args.type;bi=args.block
rec=pickle.load(open(ROOT/f'paramblock_{side}_{typ}{bi}.pkl','rb'));M=rec['matrix'];meta=rec['meta'];N0=meta['threshold'];m=len(M);limit=m-1 if side=='upper' and typ=='G' and bi==0 else m
# Common positive constant denominator; scale the whole matrix by L.
L=1
for row in M:
 for a in row:
  for z in a:L=math.lcm(L,z.denominator)
MI=[[[z.numerator*(L//z.denominator) for z in a] for a in row] for row in M]
d=max(len(a)-1 for row in MI for a in row);maxdeg=limit*d;samples=maxdeg+2
print('setup',side,typ,bi,'m',m,'limit',limit,'entry degree',d,'degree bound',maxdeg,'L digits',len(str(L)),flush=True)
def peval(a,n):
 z=0
 for c in reversed(a):z=z*n+c
 return z
def leading_dets_at(n):
 A=[[peval(MI[i][j],n) for j in range(m)] for i in range(m)];prev=1;out=[]
 for k in range(limit):
  pivot=A[k][k]
  if pivot<=0:raise AssertionError(('nonpositive sample pivot',n,k+1,pivot))
  out.append(pivot)
  if k==limit-1:break
  for i in range(k+1,m):
   for j in range(k+1,m):
    z=pivot*A[i][j]-A[i][k]*A[k][j]
    if k:
     q,r=divmod(z,prev);assert r==0,(n,k,i,j);z=q
    A[i][j]=z
  prev=pivot
 return out
t0=time.time();values=[[] for _ in range(limit)]
for t in range(samples):
 ds=leading_dets_at(N0+t)
 for k,z in enumerate(ds):values[k].append(z)
 if t%25==0:print('sample',t,'elapsed',time.time()-t0,flush=True)
records=[];total=0;minbits=None
for k,seq0 in enumerate(values,1):
 D=k*d;seq=seq0[:D+2];co=[]
 for j in range(D+1):
  co.append(seq[0]);seq=[seq[i+1]-seq[i] for i in range(len(seq)-1)]
 # Degree bound check: the next forward difference vanishes identically on supplied window.
 assert all(z==0 for z in seq),('degree bound failure',k,D,seq[:3])
 assert co[0]>0 and all(z>=0 for z in co),('negative Newton coefficient',k,min(co))
 while len(co)>1 and co[-1]==0:co.pop()
 total+=len(co);mb=min(z.bit_length() for z in co if z>0);minbits=mb if minbits is None else min(minbits,mb)
 records.append({'order':k,'degree':len(co)-1,'newton_coefficients_scaled':[str(z) for z in co]})
# Verify the exact polynomial kernel for the singular upper G0 block at coefficient level.
kernel=False
if side=='upper' and typ=='G' and bi==0:
 kernel=True;degs=meta['degrees'];mx=max(degs)
 def add(a,b):
  c=[0]*max(len(a),len(b))
  for i,z in enumerate(a):c[i]+=z
  for i,z in enumerate(b):c[i]+=z
  while len(c)>1 and c[-1]==0:c.pop()
  return c
 for i in range(m):
  z=[0]
  for j in range(m):z=add(z,[0]*(mx-degs[j])+MI[i][j])
  assert all(x==0 for x in z)
out={'side':side,'type':typ,'block':bi,'threshold':N0,'matrix_scale':str(L),'entry_degree_bound':d,'kernel_verified':kernel,'minors':records,'newton_coefficients_nonnegative':True}
with gzip.open(ROOT/f'newton_minors_{side}_{typ}{bi}.json.gz','wt') as f:json.dump(out,f,separators=(',',':'))
print('VERIFIED',side,typ,bi,'minors',limit,'Newton coefficients',total,'elapsed',time.time()-t0)
