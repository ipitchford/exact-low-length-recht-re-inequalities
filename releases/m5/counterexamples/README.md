# Exact \(m=n=5\) lower-bound counterexample

`verify_n5_lower_counterexample.py` reconstructs the explicit rational family
from Christopher M. De Sa, “Random Reshuffling is Not Always Better,” NeurIPS
2020.

For \(n=5\), define \(y_k\in\mathbb Q^5\) by

\[
(y_k)_k=\frac25,\qquad (y_k)_i=-\frac1{10}\quad(i\ne k),
\]

and

\[
A_k=I+\mathbf1y_k^{\mathsf T}+y_k\mathbf1^{\mathsf T}.
\]

Because \(\mathbf1^{\mathsf T}y_k=0\) and
\(y_k^{\mathsf T}y_k=1/5\), \(A_k\) has eigenvalues \(2,0\) on
\(\operatorname{span}\{\mathbf1,y_k\}\) and eigenvalue \(1\) on its
orthogonal complement. Hence every \(A_k\) is positive semidefinite. Their
arithmetic mean is \(I\).

Exact enumeration of all \(5!=120\) products gives

\[
\frac1{120}E_{5,5}(A)
=\frac{29}{64}\left(I-\frac15J\right)
-\frac{19}{16}\frac15J.
\]

Thus the all-ones direction has eigenvalue \(-19/16\), and \(E_{5,5}\)
has eigenvalue \(-285/2<-120=-(5)_5\). This is an exact, explicit failure of
the lower Loewner bound. Together with the candidate lower theorem for every
integer \(n\ge6\), it makes the restoration threshold sharp without relying
only on a numerical SDP optimum.

## Exact quadratic metric reversal

Put \(C_i=A_i/2\) and \(H_i=I-C_i\). These are contraction updates and PSD
Hessians with average update \(I/2\). For one epoch, the verifier checks

\[
\|\mathbb E_{\rm RR}P\|=\frac{19}{512}>
\frac1{32}=\|\mathbb E_{\rm WR}P\|.
\]

It then exhaustively enumerates the 120 reshuffling paths and all
\(5^5=3125\) independent length-five paths. With
\(P_{\mathbf1}=J/5\) and \(P_\perp=I-P_{\mathbf1}\), it obtains

\[
\mathbb E_{\rm RR}[P^{\mathsf T}P]
=\frac{1435}{1048576}P_\perp
+\frac{421}{131072}P_{\mathbf1},
\]

\[
\mathbb E_{\rm WR}[P^{\mathsf T}P]
=\frac{365}{65536}P_\perp
+\frac{91}{8192}P_{\mathbf1}.
\]

Their difference is

\[
\frac{4405}{1048576}P_\perp
+\frac{1035}{131072}P_{\mathbf1}\succ0.
\]

Thus this exact witness ranks the methods oppositely under bias norm and
one-epoch mean-square error. Because the average objective is
\(\|x\|^2/4\), reshuffling also has strictly lower expected objective after
that epoch for every nonzero starting point. This is an instance-specific
finite-horizon result, not a universal or asymptotic reshuffling theorem.

Primary source:
<https://proceedings.neurips.cc/paper/2020/hash/42299f06ee419aa5d9d07798b56779e2-Abstract.html>
