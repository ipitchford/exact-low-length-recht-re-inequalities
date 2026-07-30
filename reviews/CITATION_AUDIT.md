# Citation audit

Audit date: 30 July 2026.

## Primary-source checks

| Work | Role in the manuscripts | Verified record |
|---|---|---|
| Recht and Ré (2012) | Original noncommutative AGM conjecture and stochastic-sampling motivation | PMLR 23, 2012: <https://proceedings.mlr.press/v23/recht12.html> |
| Lai and Lim (2020) | Free-SOS/SDP framework, \(m=n=5\) lower counterexample, and stated open questions | PMLR 119, 2020: <https://proceedings.mlr.press/v119/lai20a.html> |
| De Sa (2020) | Explicit rational \(m=n=5\) matrix counterexample and exact lower eigenvalue | NeurIPS 33, 2020: <https://proceedings.neurips.cc/paper/2020/hash/42299f06ee419aa5d9d07798b56779e2-Abstract.html> |
| Zhang (2018) | Balanced-block lifting at integer multiples, Lemma 3.1 | ELA 34; DOI `10.13001/1081-3810.3555`: <https://journals.uwyo.edu/index.php/ela/article/view/1879> |
| Gatermann and Parrilo (2004) | Symmetry reduction of semidefinite programs | DOI `10.1016/j.jpaa.2003.12.011` |
| Helton, Klep, and McCullough (2012) | Convex free semialgebraic sets / Positivstellensatz context | DOI `10.1016/j.aim.2012.04.028` |
| Peyrl and Parrilo (2008) | Numerical-to-exact SOS certificate recovery | DOI `10.1016/j.tcs.2008.09.025` |
| Israel, Krahmer, and Ward (2016) | Related three-matrix AGM inequality | DOI `10.1016/j.laa.2015.09.013` |

## Material corrections

The imported \(m=4\) manuscript cited
`10.1016/j.laa.2015.09.027` for Israel–Krahmer–Ward. That DOI points to an
unrelated Riccati-equation paper. The correct DOI is
`10.1016/j.laa.2015.09.013`; the candidate source is corrected.

The inherited \(m=5\) prose called Lai–Lim's \(m=n=5\) evidence an “exact
SDP/Farkas argument.” Their paper reports numerical SDP and approximate
certificate/objective values while drawing the infeasibility conclusion. The
candidate uses calibrated wording and cites the primary paper directly.

De Sa's independent 2020 construction supplies an explicit rational witness.
The candidate release now reconstructs its five PSD matrices and all 120
products exactly, so sharpness no longer rests only on unreplayed numerical
SDP evidence.

The official arXiv title for Albar--Junge--Zhao, arXiv:1803.02435, prints
“opertors.” The bibliography silently normalizes that evident typographical
error to “operators”; this is an editorial normalization, not a different
work.

## Priority boundary

Targeted searches found no obvious earlier all-\(n\) \(m=4\) result or
five-factor restoration theorem as of the audit date. This is only a
non-detection result. A submission-ready manuscript should repeat searches by
theorem statement, author, citation graph, and recent preprint date immediately
before submission.

## Citation-coverage action

Every bibliography item in a final manuscript should be cited in the body for
a specific mathematical role. The imported \(m=4\) paper had several orphan
items; the imported \(m=5\) paper had one. The candidate sources should be
rechecked with a citation-key linter after final edits.
