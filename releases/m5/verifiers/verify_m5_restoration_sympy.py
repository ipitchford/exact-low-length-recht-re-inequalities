#!/usr/bin/env python3
"""Exact symbolic verifier for the Recht--Re m=5 restoration certificate.

Requires SymPy.  It reconstructs the orbit equations and representation blocks
from the certificate data; no floating-point arithmetic is used.
"""
from __future__ import annotations
import itertools, json, math, sys
from collections import OrderedDict
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'certificates'
n=sp.symbols('n')
t=sp.symbols('t')

class VerificationError(RuntimeError):
    """Raised when an exact certificate verification condition fails."""

def require(condition, context):
    if not condition:
        raise VerificationError(context)

# ---------- words and symmetry orbits ----------
def words(N:int):
    return [()]+[(i,) for i in range(N)]+[(i,j) for i in range(N) for j in range(N)]

def canonical_entry(left,right,stabilizer):
    def one(a,b):
        seq=list(a)+[-1]+list(b); rel={0:0} if stabilizer else {}; nxt=1 if stabilizer else 0; out=[]
        for s in seq:
            if s==-1: out.append(-1); continue
            if s not in rel: rel[s]=nxt; nxt+=1
            out.append(rel[s])
        return tuple(out)
    return min(one(left,right),one(right,left))

def orbit_map(stabilizer):
    d=OrderedDict(); b=words(6)
    for l in b:
        for r in b:
            k=canonical_entry(l,r,stabilizer)
            if k not in d:d[k]=len(d)
    return d
G_ORB=orbit_map(True); H_ORB=orbit_map(False)
require(
    len(G_ORB)==59 and len(H_ORB)==22,
    f'orbit count mismatch: expected G=59 and H=22, got G={len(G_ORB)} and H={len(H_ORB)}',
)

def rgps(length):
    if length==0:return [()]
    out=[]
    def rec(p,m):
        if len(p)==length:out.append(tuple(p));return
        for v in range(m+2):
            p.append(v);rec(p,max(m,v));p.pop()
    rec([0],0);return out
PATTERNS=sum((rgps(d) for d in range(6)),[])
PI={p:i for i,p in enumerate(PATTERNS)}
require(
    len(PATTERNS)==76,
    f'word-pattern count mismatch: expected 76, got {len(PATTERNS)}',
)

# ---------- load rational functions ----------
def entry_expr(d):
    num=sum(sp.Integer(c)*n**i for i,c in enumerate(d['numerator_coefficients']))
    return sp.cancel(num/(sp.Integer(d['denominator_constant'])*n**int(d['denominator_n_power'])))

param=json.load(open(CERT/'parametric_orbit_functions.json'))
X={w:[entry_expr(e) for e in param[w]['orbit_functions']] for w in ('upper','lower')}

# ---------- exact free-polynomial identities ----------
A0=[[0]*81 for _ in PATTERNS]; A1=[[0]*81 for _ in PATTERNS]
for word in PATTERNS:
    row=PI[word];deg=len(word)
    for ll in range(3):
        rl=deg-ll-1
        if 0<=rl<=2:
            left=tuple(reversed(word[:ll]));c=word[ll];right=word[ll+1:]
            def sw(q):return tuple(c if z==0 else 0 if z==c else z for z in q)
            A0[row][G_ORB[canonical_entry(sw(left),sw(right),True)]]+=1
    for ll in range(3):
        rl=deg-ll
        if 0<=rl<=2:
            left=tuple(reversed(word[:ll]));right=word[ll:]
            A1[row][59+H_ORB[canonical_entry(left,right,False)]]+=1
    for ll in range(3):
        rl=deg-ll-1
        if 0<=rl<=2:
            left=tuple(reversed(word[:ll]));right=word[ll+1:]
            A0[row][59+H_ORB[canonical_entry(left,right,False)]]-=1

for which,sgn in [('upper',-1),('lower',1)]:
    for i,p in enumerate(PATTERNS):
        lhs=sum((sp.Integer(A0[i][j])+n*sp.Integer(A1[i][j]))*X[which][j] for j in range(81))
        rhs=n*(n-1)*(n-2)*(n-3)*(n-4) if p==() else sp.Integer(sgn) if p==(0,1,2,3,4) else sp.Integer(0)
        residual=sp.cancel(lhs-rhs)
        require(
            residual==0,
            f'{which} rational-function identity failed for word pattern {p}: '
            f'residual={sp.factor(residual)}',
        )
print('IDENTITIES: 76 upper and 76 lower orbit equations verified exactly.')

# ---------- representation test vectors ----------
def vector(N,items):
    b=words(N);idx={q:i for i,q in enumerate(b)};a=[0]*len(b)
    for q,c in items:a[idx[q]]+=c
    return a

def vectors_H(N):
    triv=[vector(N,[((),1)]),vector(N,[((i,),1) for i in range(N)]),vector(N,[((i,i),1) for i in range(N)]),vector(N,[((i,j),1) for i in range(N) for j in range(N) if i!=j])]
    a=[0]*N;a[0]=1;a[1]=-1
    std=[vector(N,[((i,),a[i]) for i in range(N)]),vector(N,[((i,i),a[i]) for i in range(N)]),vector(N,[((i,j),a[i]+a[j]) for i in range(N) for j in range(N) if i!=j]),vector(N,[((i,j),a[i]-a[j]) for i in range(N) for j in range(N) if i!=j])]
    q=vector(N,[((0,1),1),((1,0),1),((2,3),1),((3,2),1),((0,2),-1),((2,0),-1),((1,3),-1),((3,1),-1)])
    cyc=vector(N,[((0,1),1),((1,0),-1),((1,2),1),((2,1),-1),((2,0),1),((0,2),-1)])
    return [triv,std,[q],[cyc]]

def vectors_G(N):
    nz=range(1,N)
    triv=[vector(N,[((),1)]),vector(N,[((0,),1)]),vector(N,[((i,),1) for i in nz]),vector(N,[((0,0),1)]),vector(N,[((0,i),1) for i in nz]),vector(N,[((i,0),1) for i in nz]),vector(N,[((i,i),1) for i in nz]),vector(N,[((i,j),1) for i in nz for j in nz if i!=j])]
    a=[0]*N;a[1]=1;a[2]=-1
    std=[vector(N,[((i,),a[i]) for i in nz]),vector(N,[((0,i),a[i]) for i in nz]),vector(N,[((i,0),a[i]) for i in nz]),vector(N,[((i,i),a[i]) for i in nz]),vector(N,[((i,j),a[i]+a[j]) for i in nz for j in nz if i!=j]),vector(N,[((i,j),a[i]-a[j]) for i in nz for j in nz if i!=j])]
    q=vector(N,[((1,2),1),((2,1),1),((3,4),1),((4,3),1),((1,3),-1),((3,1),-1),((2,4),-1),((4,2),-1)])
    cyc=vector(N,[((1,2),1),((2,1),-1),((2,3),1),((3,2),-1),((3,1),1),((1,3),-1)])
    return [triv,std,[q],[cyc]]

def direct_coeff_blocks(N,typ):
    stab=typ=='G'; om=G_ORB if stab else H_ORB; b=words(N); ids=[[om[canonical_entry(l,r,stab)] for r in b] for l in b]
    blocks=vectors_G(N) if stab else vectors_H(N); K=59 if stab else 22;out=[]
    for vs in blocks:
        C=[[[0]*K for _ in vs] for _ in vs]
        for i,u in enumerate(vs):
            iu=[p for p,z in enumerate(u) if z]
            for j,v in enumerate(vs):
                iv=[p for p,z in enumerate(v) if z]
                for p in iu:
                    for q in iv:C[i][j][ids[p][q]]+=u[p]*v[q]
        out.append(C)
    return out

def interpolate_coeff_blocks(typ):
    samples=[direct_coeff_blocks(N,typ) for N in range(6,11)]
    out=[]
    for bi in range(4):
        s=len(samples[0][bi]);K=59 if typ=='G' else 22;C=[[[0]*K for _ in range(s)] for _ in range(s)]
        for i in range(s):
            for j in range(s):
                for k in range(K):
                    C[i][j][k]=sp.interpolate([(N,sp.Integer(samples[N-6][bi][i][j][k])) for N in range(6,11)],n)
        out.append(C)
    # Independent extra point; degree <=4 follows from at most four freely summed indices.
    check=direct_coeff_blocks(11,typ)
    for bi,C in enumerate(out):
        for i in range(len(C)):
            for j in range(len(C)):
                for k in range(len(C[i][j])):
                    residual=sp.expand(C[i][j][k].subs(n,11)-check[bi][i][j][k])
                    require(
                        residual==0,
                        f'{typ} block {bi} coefficient ({i},{j}), orbit {k}: '
                        f'n=11 replay residual={residual}',
                    )
    return out

C_G=interpolate_coeff_blocks('G');C_H=interpolate_coeff_blocks('H')
print('BLOCK COEFFICIENTS: exact degree<=4 interpolation and independent n=11 check passed.')

# ---------- seed transversals and exact affine reconstruction ----------
def verify_seed_transversal(N,which,record,upper):
    E=sp.Matrix([[sp.Integer(A0[i][j]+N*A1[i][j]) for j in range(81)] for i in range(76)])
    b=sp.zeros(76,1)
    b[PI[()]]=sp.Integer(math.prod(N-j for j in range(5)))
    b[PI[(0,1,2,3,4)]]=sp.Integer(-1 if which=='upper' else 1)
    if upper:
        C0=direct_coeff_blocks(N,'G')[0]
        K=sp.Matrix([[sp.Integer(sum(C0[i][j][k] for j in range(8))) if k<59 else 0 for k in range(81)] for i in range(8)])
        E=E.col_join(K);b=b.col_join(sp.zeros(8,1))
    x=sp.Matrix([sp.Rational(z) for z in record['orbit_values']])
    free=list(map(int,record['free_indices']))
    actual_free_values=[x[j] for j in free]
    expected_free_values=[sp.Rational(z) for z in record['free_values']]
    require(
        actual_free_values==expected_free_values,
        f'{which} n={N} free-coordinate values do not match the full orbit record',
    )
    affine_residual=E*x-b
    require(
        affine_residual==sp.zeros(E.rows,1),
        f'{which} n={N} affine equations failed: residual={list(affine_residual)}',
    )
    piv=[j for j in range(81) if j not in set(free)]
    pivot_rank=E[:,piv].rank()
    require(
        pivot_rank==len(piv),
        f'{which} n={N} complementary-column rank mismatch: expected {len(piv)}, got {pivot_rank}',
    )
    affine_rank=E.rank()
    require(
        affine_rank==len(piv),
        f'{which} n={N} affine-system rank mismatch: expected {len(piv)}, got {affine_rank}',
    )

seed=json.load(open(CERT/'base6_seed_certificates.json'))
verify_seed_transversal(6,'upper',seed['upper'],True)
verify_seed_transversal(6,'lower',seed['lower'],False)
endpoint=json.load(open(CERT/'n5_upper_certificate.json'))
verify_seed_transversal(5,'upper',endpoint['upper'],True)
print('SEED TRANSVERSALS: 23 upper and 30 lower free coordinates reconstruct the exact affine certificates uniquely.')

DEGS={'G':[[0,1,1,2,2,2,2,2],[1,2,2,2,2,2],[2],[2]],'H':[[0,1,2,2],[1,2,2,2],[2],[2]]}
block_data=json.load(open(CERT/'principal_minors.json'))
for which in ('upper','lower'):
    blocks=[]
    for typ,off,K,Cs in [('G',0,59,C_G),('H',59,22,C_H)]:
        for bi,C in enumerate(Cs):
            s=len(C);M=sp.zeros(s);deg=DEGS[typ][bi]
            for i in range(s):
                for j in range(s):
                    val=sum(C[i][j][k]*X[which][off+k] for k in range(K))
                    M[i,j]=sp.factor(sp.cancel(sp.expand_func(n**(deg[i]+deg[j]+1)*val)))
                    denominator=sp.denom(M[i,j])
                    require(
                        n not in denominator.free_symbols,
                        f'{which}_{typ}{bi} entry ({i},{j}) retains n in denominator: {denominator}',
                    )
            require(
                M==M.T,
                f'{which}_{typ}{bi} reconstructed block is not symmetric',
            )
            blocks.append((typ,bi,M))
    for typ,bi,M in blocks:
        key=f'{which}_{typ}{bi}'
        maxk=7 if key=='upper_G0' else M.rows
        if key=='upper_G0':
            kernel=sp.Matrix([n**2,n,n,1,1,1,1,1])
            kernel_residual=[sp.cancel(z) for z in M*kernel]
            require(
                all(z==0 for z in kernel_residual),
                f'upper_G0 kernel equation failed: residual={kernel_residual}',
            )
        for k in range(1,maxk+1):
            det=sp.factor(sp.cancel(M[:k,:k].det(method='domain-ge')))
            num,den=sp.fraction(det)
            poly=sp.Poly(sp.expand(num.subs(n,t+6)),t,domain=sp.QQ)
            asc=list(reversed(poly.all_coeffs()))
            nonpositive=[(degree,c) for degree,c in enumerate(asc) if c<=0]
            require(
                den>0 and not nonpositive,
                f'{key} leading principal minor {k} has denominator={den} '
                f'and nonpositive shifted coefficients={nonpositive}',
            )
            rec=block_data[key]['leading_principal_minors'][k-1]
            require(
                str(den)==rec['denominator'],
                f'{key} leading principal minor {k} denominator mismatch: '
                f'reconstructed={den}, stored={rec["denominator"]}',
            )
            stored_coefficients=rec['coefficients_ascending_in_t']
            reconstructed_coefficients=[str(c) for c in asc]
            require(
                reconstructed_coefficients==stored_coefficients,
                f'{key} leading principal minor {k} coefficient mismatch: '
                f'reconstructed={reconstructed_coefficients}, stored={stored_coefficients}',
            )
print('POSITIVITY n>=6: 51 determinant polynomials and the upper kernel verified exactly.')

# ---------- exact endpoint: upper inequality at n=5 ----------
def rat(s):return sp.Rational(s)
n5=json.load(open(CERT/'n5_upper_certificate.json'))
x=[rat(z) for z in n5['upper']['orbit_values']]
for i,p in enumerate(PATTERNS):
    lhs=sum((sp.Integer(A0[i][j])+5*sp.Integer(A1[i][j]))*x[j] for j in range(81))
    rhs=120 if p==() else -1 if p==(0,1,2,3,4) else 0
    require(
        lhs==rhs,
        f'n=5 upper endpoint identity failed for word pattern {p}: lhs={lhs}, rhs={rhs}',
    )
blocks=[]
for typ,off,K in [('G',0,59),('H',59,22)]:
    for bi,C in enumerate(direct_coeff_blocks(5,typ)):
        sz=len(C);M=sp.zeros(sz)
        for i in range(sz):
            for j in range(sz):M[i,j]=sum(sp.Integer(C[i][j][k])*x[off+k] for k in range(K))
        blocks.append((typ,bi,M))
for typ,bi,M in blocks:
    if typ=='G' and bi==0:
        kernel_residual=M*sp.ones(8,1)
        require(
            kernel_residual==sp.zeros(8,1),
            f'n=5 upper G0 all-ones kernel failed: residual={list(kernel_residual)}',
        )
        P=sp.Matrix.vstack(sp.eye(7),-sp.ones(1,7));M=P.T*M*P
    for k in range(1,M.rows+1):
        determinant=M[:k,:k].det(method='domain-ge')
        require(
            determinant>0,
            f'n=5 upper {typ}{bi} leading principal minor {k} is not positive: {determinant}',
        )
print('n=5 UPPER ENDPOINT: exact identity, kernel, and rational Sylvester tests passed.')

seed=json.load(open(CERT/'base6_seed_certificates.json'))
for which in ('upper','lower'):
    specialized=[sp.cancel(z.subs(n,6)) for z in X[which]]
    expected_seed=[sp.Rational(q) for q in seed[which]['orbit_values']]
    require(
        specialized==expected_seed,
        f'{which} parametric family does not specialize to the n=6 seed',
    )
print('SEED: parametric family specializes exactly to both n=6 certificates.')
print('VERIFIED: Recht--Re m=5 upper bound holds for n>=5 and both bounds hold for n>=6.')
