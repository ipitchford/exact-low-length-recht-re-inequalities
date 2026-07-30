# Exact six-factor base-PSD replay receipt

**Replay date:** 30 July 2026  
**Interpreter:** CPython 3.13  
**Exact arithmetic:** `python-flint==0.8.0`  
**Identity arithmetic:** `sympy==1.14.0`

## Commands

From the package root:

```bash
.venv/bin/python releases/m6-balanced/check_parametric_identities.py
.venv/bin/python releases/m6-balanced/certify_base_psd_flint.py
```

The identity verifier passed 1,156 rational coefficient equations for each
of the upper and lower signs.

## Exact PSD results

| Side | Matrix | Base | Size | Rank | Zero coefficients of \(\det(tI+A)\) | Common denominator |
|---|---:|---:|---:|---:|---:|---:|
| upper | \(G\) | 7 | 400 | 399 | 1 | 16941456000000 |
| upper | \(H\) | 7 | 400 | 400 | 0 | 16941456000000 |
| lower | \(G\) | 8 | 585 | 585 | 0 | 262144000000 |
| lower | \(H\) | 8 | 585 | 585 | 0 | 262144000000 |

Every coefficient not forced to vanish was strictly positive. The upper
\(G\) matrix annihilated the exact 400-dimensional all-ones word-evaluation
vector; rank 399 proves that this vector spans its kernel.

FLINT returns the coefficient list of \(\det(xI-A)\) in ascending degree.
The verifier applies the exact alternating-sign conversion to
\(\det(tI+A)\) before testing coefficient signs. The following SHA-256
digests bind the **raw** newline-separated FLINT coefficient lists with no
trailing newline, before that sign conversion:

```text
upper G  c95af891ab9992fd2681af349044732a988ba147db9e43eec4288e2317589f51
upper H  a8bbe7306acc878d612c8d8bd3695a036d35852e3d1257263205ec809a497419
lower G  bd0867a98fd93a7cb624200f7d965cf4983448e0cf30c843d7b7fd7a49729a03
lower H  32e99420c0feb2bbbcd08fdf4e40fc2847ed1ab945620073397b5394d75b6a46
```

An independent clean-environment audit reproduced both exact programs, all
four ranks, both denominators, every sign condition, and every digest. See
`../../reviews/peer_review/m6_balanced_audit.md`.

## Assurance boundary

This receipt establishes deterministic exact replay of the released
certificate. It is not formal proof-assistant verification, independent
external reproduction, journal peer review, an all-\(n\) six-factor result,
or evidence for the quarantined endpoint dual artifacts.
