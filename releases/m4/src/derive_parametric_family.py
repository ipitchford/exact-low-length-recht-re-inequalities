#!/usr/bin/env python3
"""Re-derive the all-n orbit functions from the exact n=5 seed certificate.

This is a discovery/provenance script, not needed by the two proof verifiers.
It implements balanced five-block averaging symbolically and confirms that the
result is exactly the published parametric certificate.
"""
from __future__ import annotations
import itertools,json
from collections import OrderedDict
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'certificates';n=sp.symbols('n')

class VerificationError(RuntimeError):
 """Raised when an exact certificate verification condition fails."""

def require(condition,context):
 if not condition:
  raise VerificationError(context)

def words(N):return [()]+[(i,) for i in range(N)]+[(i,j) for i in range(N) for j in range(N)]
def canonical_entry(left,right,stab):
 def one(a,b):
  rel={0:0} if stab else {};nxt=1 if stab else 0;out=[]
  for z in list(a)+[-1]+list(b):
   if z==-1:out.append(-1);continue
   if z not in rel:rel[z]=nxt;nxt+=1
   out.append(rel[z])
  return tuple(out)
 return min(one(left,right),one(right,left))
def orbit_map(stab):
 d=OrderedDict();b=words(6)
 for u in b:
  for v in b:
   q=canonical_entry(u,v,stab)
   if q not in d:d[q]=len(d)
 return d
G=orbit_map(True);H=orbit_map(False)
def reps(om,stab):
 r=[None]*len(om)
 for u in words(6):
  for v in words(6):
   i=om[canonical_entry(u,v,stab)]
   if r[i] is None:r[i]=(u,v)
 return r
GR=reps(G,True);HR=reps(H,False)
def falling(x,k):
 z=sp.Integer(1)
 for j in range(k):z*=x-j
 return z

def expected(u,v,base,stab):
 symbols=sorted(set(u+v+((0,) if stab else ())))
 pos={z:i for i,z in enumerate(symbols)};s=len(symbols);total=sp.Integer(0)
 for colors in itertools.product(range(5),repeat=s):
  counts=[colors.count(a) for a in range(5)]
  weight=sp.prod(falling(n/5,c) for c in counts)
  if weight==0:continue
  um=tuple(colors[pos[z]] for z in u);vm=tuple(colors[pos[z]] for z in v)
  if stab:
   c=colors[pos[0]]
   sw=lambda q:tuple(0 if z==c else c if z==0 else z for z in q)
   value=base[G[canonical_entry(sw(um),sw(vm),True)]]
  else:value=base[59+H[canonical_entry(um,vm,False)]]
  total+=weight*value
 return sp.cancel(total/falling(n,s))

def decode(e):
 num=sum(sp.Integer(a)*n**i for i,a in enumerate(e['numerator_coefficients']))
 return sp.cancel(num/(sp.Integer(e['denominator_constant'])*n**e['denominator_n_power']))
seed=json.load(open(CERT/'base5_seed_certificates.json'));published=json.load(open(CERT/'parametric_orbit_functions.json'))
C=falling(n,4)/falling(sp.Integer(5),4);r=n/5
for which in ('upper','lower'):
 base=[sp.Rational(z) for z in seed[which]['orbit_values']];derived=[]
 for stab,RR in [(True,GR),(False,HR)]:
  for u,v in RR:
   derived.append(sp.factor(sp.cancel(C*r**(-(len(u)+len(v)+1))*expected(u,v,base,stab))))
 target=[decode(e) for e in published[which]['orbit_functions']]
 require(
  len(derived)==len(target),
  f'{which} orbit-function count mismatch: derived={len(derived)}, published={len(target)}',
 )
 for orbit_index,(actual,expected_value) in enumerate(zip(derived,target)):
  residual=sp.cancel(actual-expected_value)
  require(
   residual==0,
   f'{which} orbit function {orbit_index} does not match the published family: residual={residual}',
  )
 print(f'{which}: all 81 orbit functions re-derived exactly from balanced five-block averaging.')
print('DERIVATION VERIFIED.')
