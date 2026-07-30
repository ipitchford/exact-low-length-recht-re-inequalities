#!/usr/bin/env python3
"""Dependency-free exact verifier for the Recht--Re m=4 all-n certificate.

Uses only Python's standard library and fractions.Fraction.  It verifies:
  * the 152 parametric free-polynomial coefficient equations;
  * the advertised 23 upper and 30 lower free rational functions;
  * the representation-block matrices from exact orbit counting;
  * all 51 determinant polynomials and their positive shifted coefficients;
  * the exceptional n=4 certificates and their block positivity.
No floating-point arithmetic is used.
"""
from __future__ import annotations
import itertools,json,math
from collections import OrderedDict
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; CERT=ROOT/'certificates'

class VerificationError(RuntimeError):
    """Raised when an exact certificate verification condition fails."""

def require(condition, context):
    if not condition:
        raise VerificationError(context)

# ---------------- polynomial arithmetic, ascending coefficients ----------------
def tr(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p or [F(0)]
def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return tr(c)
def neg(a):return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def scale(a,c):return tr([x*c for x in a])
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i+j]+=x*y
    return tr(c)
def ppow(a,k):
    z=[F(1)]
    while k:
        if k&1:z=mul(z,a)
        a=mul(a,a);k//=2
    return z
def peval(a,x):
    z=F(0)
    for c in reversed(a):z=z*x+c
    return z
def binom_t(k):
    p=[F(1)]
    for j in range(k):p=mul(p,[F(-j),F(1)])
    return scale(p,F(1,math.factorial(k)))
BINOM=[binom_t(k) for k in range(5)]
def interpolate_t(values):
    cur=[F(v) for v in values];ans=[F(0)]
    for d in range(len(values)):
        ans=add(ans,scale(BINOM[d],cur[0]))
        cur=[cur[i+1]-cur[i] for i in range(len(cur)-1)]
    return tr(ans)
N_POLY=[F(5),F(1)] # n=t+5

def ncoeff_to_t(coeff):
    ans=[F(0)]
    for i,c in enumerate(coeff):ans=add(ans,scale(ppow(N_POLY,i),F(c)))
    return tr(ans)

def det_poly(M):
    m=len(M);dp=[None]*(1<<m);dp[0]=[F(1)]
    for mask in range(1<<m):
        if dp[mask] is None:continue
        i=mask.bit_count()
        if i==m:continue
        for j in range(m):
            if mask>>j&1:continue
            inv=sum(1 for q in range(j+1,m) if mask>>q&1)
            term=mul(dp[mask],M[i][j])
            if inv&1:term=neg(term)
            nm=mask|(1<<j);dp[nm]=term if dp[nm] is None else add(dp[nm],term)
    return tr(dp[-1])

def det_fraction(A):
    A=[list(map(F,row)) for row in A];N=len(A);det=F(1)
    for k in range(N):
        p=next((i for i in range(k,N) if A[i][k]),None)
        if p is None:return F(0)
        if p!=k:A[k],A[p]=A[p],A[k];det=-det
        pivot=A[k][k];det*=pivot
        for i in range(k+1,N):
            q=A[i][k]/pivot
            for j in range(k+1,N):A[i][j]-=q*A[k][j]
    return det

def rank_fraction(A):
    A=[list(map(F,row)) for row in A]
    if not A:return 0
    rows=len(A);cols=len(A[0]);rank=0
    for col in range(cols):
        pivot=next((i for i in range(rank,rows) if A[i][col]),None)
        if pivot is None:continue
        A[rank],A[pivot]=A[pivot],A[rank]
        q=A[rank][col]
        for j in range(col,cols):A[rank][j]/=q
        for i in range(rows):
            if i==rank or not A[i][col]:continue
            q=A[i][col]
            for j in range(col,cols):A[i][j]-=q*A[rank][j]
        rank+=1
        if rank==rows:break
    return rank

# ---------------- symmetry/orbit construction ----------------
def words(N):return [()]+[(i,) for i in range(N)]+[(i,j) for i in range(N) for j in range(N)]
def canonical_entry(left,right,stab):
    def one(a,b):
        seq=list(a)+[-1]+list(b);rel={0:0} if stab else {};nxt=1 if stab else 0;out=[]
        for s in seq:
            if s==-1:out.append(-1);continue
            if s not in rel:rel[s]=nxt;nxt+=1
            out.append(rel[s])
        return tuple(out)
    return min(one(left,right),one(right,left))
def orbit_map(stab):
    d=OrderedDict();b=words(6)
    for l in b:
        for r in b:
            k=canonical_entry(l,r,stab)
            if k not in d:d[k]=len(d)
    return d
G_ORB=orbit_map(True);H_ORB=orbit_map(False)
require(
    len(G_ORB)==59 and len(H_ORB)==22,
    f'orbit count mismatch: expected G=59 and H=22, got G={len(G_ORB)} and H={len(H_ORB)}',
)

def rgps(L):
    if L==0:return [()]
    out=[]
    def rec(p,m):
        if len(p)==L:out.append(tuple(p));return
        for z in range(m+2):p.append(z);rec(p,max(m,z));p.pop()
    rec([0],0);return out
PAT=sum((rgps(d) for d in range(6)),[]);PI={p:i for i,p in enumerate(PAT)}
require(len(PAT)==76,f'word-pattern count mismatch: expected 76, got {len(PAT)}')
A0=[[0]*81 for _ in PAT];A1=[[0]*81 for _ in PAT]
for word in PAT:
    row=PI[word];d=len(word)
    for ll in range(3):
        if 0<=d-ll-1<=2:
            left=tuple(reversed(word[:ll]));c=word[ll];right=word[ll+1:]
            sw=lambda q:tuple(c if z==0 else 0 if z==c else z for z in q)
            A0[row][G_ORB[canonical_entry(sw(left),sw(right),True)]]+=1
    for ll in range(3):
        if 0<=d-ll<=2:
            left=tuple(reversed(word[:ll]));right=word[ll:]
            A1[row][59+H_ORB[canonical_entry(left,right,False)]]+=1
    for ll in range(3):
        if 0<=d-ll-1<=2:
            left=tuple(reversed(word[:ll]));right=word[ll+1:]
            A0[row][59+H_ORB[canonical_entry(left,right,False)]]-=1

# ---------------- rational orbit functions and identities ----------------
P=json.load(open(CERT/'parametric_orbit_functions.json'))
def parse_fun(e):
    return [F(z) for z in e['numerator_coefficients']],int(e['denominator_constant']),int(e['denominator_n_power'])
FUN={w:[parse_fun(e) for e in P[w]['orbit_functions']] for w in ('upper','lower')}
for w in ('upper','lower'):
    free=P[w]['free_indices'];expected_free_count=23 if w=='upper' else 30
    require(
        len(free)==expected_free_count,
        f'{w} free-coordinate count mismatch: expected {expected_free_count}, got {len(free)}',
    )
    for i in free:
        require(
            parse_fun(P[w]['free_functions'][str(i)])==FUN[w][i],
            f'{w} free function z_{i} does not match orbit_functions[{i}]',
        )
    for row,patt in enumerate(PAT):
        lhs=[F(0)]
        for j,(num,c,q) in enumerate(FUN[w]):
            a=A0[row][j];b=A1[row][j]
            if not (a or b):continue
            term=mul([F(a),F(b)],[F(z,c) for z in num])
            term=[F(0)]*(4-q)+term
            lhs=add(lhs,term)
        sgn=-1 if w=='upper' else 1
        rhs=mul([F(0)]*4+[F(1)],mul(mul([F(0),F(1)],[-1,1]),mul([-2,1],[-3,1]))) if patt==() else ([F(0)]*4+[F(sgn)] if patt==(0,1,2,3) else [F(0)])
        residual=sub(lhs,rhs)
        require(
            residual==[F(0)],
            f'{w} rational-function identity failed for word pattern {patt}: residual={residual}',
        )
print('IDENTITIES: 152 rational-function equations verified exactly.')

# ---------------- representation vectors and exact coefficient counts ----------------
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
def count_blocks(N,typ,vfun=None):
    stab=typ=='G';om=G_ORB if stab else H_ORB;b=words(N);ids=[[om[canonical_entry(l,r,stab)] for r in b] for l in b]
    blocks=(vfun() if vfun else (vectors_G(N) if stab else vectors_H(N)));K=59 if stab else 22;out=[]
    for vs in blocks:
        C=[[[0]*K for _ in vs] for _ in vs]
        supp=[[i for i,z in enumerate(v) if z] for v in vs]
        for i,u in enumerate(vs):
            for j,v in enumerate(vs):
                for p in supp[i]:
                    up=u[p]
                    for q in supp[j]:C[i][j][ids[p][q]]+=up*v[q]
        out.append(C)
    return out
SAMPLES={typ:[count_blocks(N,typ) for N in range(5,10)] for typ in ('G','H')}
# extra point verifies the combinatorial degree<=4 interpolation.
EXTRA={typ:count_blocks(10,typ) for typ in ('G','H')}
C={}
for typ in ('G','H'):
    C[typ]=[]
    for bi in range(4):
        s=len(SAMPLES[typ][0][bi]);K=59 if typ=='G' else 22;block=[[[None]*K for _ in range(s)] for _ in range(s)]
        for i in range(s):
            for j in range(s):
                for k in range(K):
                    vals=[SAMPLES[typ][r][bi][i][j][k] for r in range(5)]
                    block[i][j][k]=interpolate_t(vals)
                    replay_value=peval(block[i][j][k],5)
                    expected_value=EXTRA[typ][bi][i][j][k]
                    require(
                        replay_value==expected_value,
                        f'{typ} block {bi} coefficient ({i},{j}), orbit {k}: '
                        f'n=10 replay mismatch, interpolated={replay_value}, direct={expected_value}',
                    )
        C[typ].append(block)
print('BLOCK COUNTS: degree<=4 interpolation and independent n=10 replay passed.')

# ---------------- seed transversals and exact affine reconstruction ----------------
def verify_seed_transversal(N,side,record,upper):
    E=[[F(A0[i][j]+N*A1[i][j]) for j in range(81)] for i in range(76)]
    b=[F(0)]*76
    b[PI[()]]=F(math.prod(N-j for j in range(4)))
    b[PI[(0,1,2,3)]]=F(-1 if side=='upper' else 1)
    if upper:
        C0=count_blocks(N,'G')[0]
        for i in range(8):
            E.append([F(sum(C0[i][j][k] for j in range(8))) if k<59 else F(0) for k in range(81)])
            b.append(F(0))
    x=[F(z) for z in record['orbit_values']]
    free=list(map(int,record['free_indices']))
    actual_free_values=[x[j] for j in free]
    expected_free_values=[F(z) for z in record['free_values']]
    require(
        actual_free_values==expected_free_values,
        f'{side} n={N} free-coordinate values do not match the full orbit record',
    )
    for equation_index,(row,rhs) in enumerate(zip(E,b)):
        lhs=sum((a*z for a,z in zip(row,x)),F(0))
        require(
            lhs==rhs,
            f'{side} n={N} affine equation {equation_index} failed: lhs={lhs}, rhs={rhs}',
        )
    piv=[j for j in range(81) if j not in set(free)]
    EP=[[row[j] for j in piv] for row in E]
    pivot_rank=rank_fraction(EP)
    require(
        pivot_rank==len(piv),
        f'{side} n={N} complementary-column rank mismatch: expected {len(piv)}, got {pivot_rank}',
    )
    affine_rank=rank_fraction(E)
    require(
        affine_rank==len(piv),
        f'{side} n={N} affine-system rank mismatch: expected {len(piv)}, got {affine_rank}',
    )

SEED_DATA=json.load(open(CERT/'base5_seed_certificates.json'))
verify_seed_transversal(5,'upper',SEED_DATA['upper'],True)
verify_seed_transversal(5,'lower',SEED_DATA['lower'],False)
print('SEED TRANSVERSALS: 23 upper and 30 lower free coordinates reconstruct the exact affine certificates uniquely.')

DEGS={'G':[[0,1,1,2,2,2,2,2],[1,2,2,2,2,2],[2],[2]],'H':[[0,1,2,2],[1,2,2,2],[2],[2]]}
B=json.load(open(CERT/'scaled_block_matrices.json'));D=json.load(open(CERT/'principal_minors.json'))
for w in ('upper','lower'):
    for typ,off,K in [('G',0,59),('H',59,22)]:
        for bi,CB in enumerate(C[typ]):
            key=f'{w}_{typ}{bi}';degs=DEGS[typ][bi];s=len(CB);M=[]
            for i in range(s):
                row=[]
                for j in range(s):
                    z=[F(0)];power=degs[i]+degs[j]+1
                    for k in range(K):
                        if CB[i][j][k]==[F(0)]:continue
                        num,c,q=FUN[w][off+k]
                        require(
                            q<=power,
                            f'{key} entry ({i},{j}), orbit {off+k}: '
                            f'denominator n-power {q} exceeds congruence power {power}',
                        )
                        term=mul(CB[i][j][k],ncoeff_to_t(num));term=mul(term,ppow(N_POLY,power-q));term=scale(term,F(1,c));z=add(z,term)
                    rec=B[key]['entries'][i][j];stored=[F(a,int(rec['denominator'])) for a in rec['numerator_coefficients']]
                    stored=tr(stored)
                    require(
                        z==stored,
                        f'{key} scaled block entry ({i},{j}) mismatch: reconstructed={z}, stored={stored}',
                    )
                    row.append(z)
                M.append(row)
            if key=='upper_G0':
                kv=[ppow(N_POLY,2),N_POLY,N_POLY,[F(1)],[F(1)],[F(1)],[F(1)],[F(1)]]
                for i in range(8):
                    z=[F(0)]
                    for j in range(8):z=add(z,mul(M[i][j],kv[j]))
                    require(
                        z==[F(0)],
                        f'upper_G0 kernel equation failed in row {i}: residual={z}',
                    )
                maxk=7
            else:maxk=s
            for k in range(1,maxk+1):
                det=det_poly([r[:k] for r in M[:k]])
                rec=D[key]['leading_principal_minors'][k-1];stored=[F(a)/int(rec['denominator']) for a in rec['coefficients_ascending_in_t']]
                stored=tr(stored)
                require(
                    det==stored,
                    f'{key} leading principal minor {k} mismatch: reconstructed={det}, stored={stored}',
                )
                nonpositive=[(degree,a) for degree,a in enumerate(det) if a<=0]
                require(
                    not nonpositive,
                    f'{key} leading principal minor {k} has nonpositive shifted coefficients: {nonpositive}',
                )
print('POSITIVITY n>=5: block construction, 51 exact determinants, positive coefficients, and kernel passed.')

# ---------------- n=4 exact certificates ----------------
def vectors_G4():
    N=4;nz=range(1,N)
    triv=[vector(N,[((),1)]),vector(N,[((0,),1)]),vector(N,[((i,),1) for i in nz]),vector(N,[((0,0),1)]),vector(N,[((0,i),1) for i in nz]),vector(N,[((i,0),1) for i in nz]),vector(N,[((i,i),1) for i in nz]),vector(N,[((i,j),1) for i in nz for j in nz if i!=j])]
    a=[0]*N;a[1]=1;a[2]=-1
    std=[vector(N,[((i,),a[i]) for i in nz]),vector(N,[((0,i),a[i]) for i in nz]),vector(N,[((i,0),a[i]) for i in nz]),vector(N,[((i,i),a[i]) for i in nz]),vector(N,[((i,j),a[i]+a[j]) for i in nz for j in nz if i!=j]),vector(N,[((i,j),a[i]-a[j]) for i in nz for j in nz if i!=j])]
    sign=vector(N,[((1,2),1),((2,1),-1),((2,3),1),((3,2),-1),((3,1),1),((1,3),-1)])
    return [triv,std,[sign]]
def matmul(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0)) for j in range(len(B[0]))] for i in range(len(A))]
def transpose(A):return [list(r) for r in zip(*A)]
N4=json.load(open(CERT/'n4_orbit_certificates.json'))
CG4=count_blocks(4,'G',vectors_G4);CH4=count_blocks(4,'H')
for w in ('upper','lower'):
    x=[F(z) for z in N4[w]['orbit_values']];sgn=-1 if w=='upper' else 1
    for row,patt in enumerate(PAT):
        lhs=sum((F(A0[row][j]+4*A1[row][j])*x[j] for j in range(81)),F(0))
        rhs=F(24) if patt==() else F(sgn) if patt==(0,1,2,3) else F(0)
        require(
            lhs==rhs,
            f'n=4 {w} endpoint identity failed for word pattern {patt}: lhs={lhs}, rhs={rhs}',
        )
    for typ,off,K,blocks in [('G',0,59,CG4),('H',59,22,CH4)]:
        for bi,CB in enumerate(blocks):
            s=len(CB);M=[[sum((F(CB[i][j][k])*x[off+k] for k in range(K)),F(0)) for j in range(s)] for i in range(s)]
            if w=='upper' and typ=='G' and bi==0:
                kernel_residual=[sum(M[i],F(0)) for i in range(8)]
                require(
                    all(z==0 for z in kernel_residual),
                    f'n=4 upper G0 all-ones kernel failed: residual={kernel_residual}',
                )
                Pm=[[F(1) if i==j else F(0) for j in range(7)] for i in range(7)]+[[-F(1)]*7]
                M=matmul(transpose(Pm),matmul(M,Pm));s=7
            for k in range(1,s+1):
                determinant=det_fraction([r[:k] for r in M[:k]])
                require(
                    determinant>0,
                    f'n=4 {w} {typ}{bi} leading principal minor {k} is not positive: {determinant}',
                )
print('n=4: exact identities and all rational Sylvester tests passed.')
print('VERIFIED (stdlib): Recht--Re m=4 holds for every integer n>=4.')
