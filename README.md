# Opinion Network Formation — Team MATlab

DPCN Assignment 1, IIIT Hyderabad. We build **four networks** from one class survey
(96 responses, 60 Likert statements across Technology, Education, Society & Ethics, Environment)
and compare what each one reveals.

**Report:** [`report/report.pdf`](report/report.pdf) — the single, self-contained team report.
**Interactive portal:** open [`index.html`](index.html) in a browser for the figures and the D3 visualisers.

## The four networks

| | Network | Nodes | An edge means | Size | By |
|---|---|---|---|---|---|
| A | Student–student agreement | 91 students | the pair agrees more than two random classmates would | 2,026 edges | Mayank Kar |
| B | Student–question extremes | 89 students + 60 questions | the student holds an extreme view on the question | 2,362 edges | Tanush Garg |
| C | Question–question projection | 60 questions | some student holds extreme views on both questions | complete graph K₆₀ | Tanush Garg |
| D | Question–question correlation | 60 questions | the two statements are answered in step (Spearman ρ > 0.35) | 188 edges | Amish Goyal |

**A — student–student (`Student Network/`).** Answers are scored pairwise (2 for a match, 1 for the same
side of the scale), then corrected for chance agreement, since 80% of answers are on the agree side and raw
agreement links everyone to everyone. Sparsified two ways (a global cutoff sweep, and each student's two
strongest edges) and measured against ER graphs: small-world, broad degree distribution, no scale-free tail.
Centrality separates emphatic answerers from "typical" ones, and the per-topic networks show agreement is
topic-specific.

**B — student–question extremes (`Extreme Bipartite Network/`).** Keeps only Strongly Agree / Strongly
Disagree answers. Bipartite density 0.44, one connected component, question degrees bounded but overdispersed
(γ̂ = 0.750, dispersion 3.75), so no scale-free mega-hubs.

**C — question–question projection (`Extreme Bipartite Network/`).** Projecting B onto the questions gives the
complete graph: every pair of questions shares at least one student with extreme views on both. The weighted
projection gives the anchors (E15, E11, V13), and Molloy–Reed (κ = 59) plus a robustness simulation show
targeted attack is indistinguishable from random failure.

**D — question–question correlation (`Question Network/`).** Spearman correlations between all 1,770 question
pairs, thresholded at ρ > 0.35. Environmental and ethical statements form the core, S09/S13/T12 bridge the
clusters, Louvain finds six mixed modules, and section assortativity of 0.304 shows beliefs do not follow the
survey's own sections. 13 questions stay isolated — the ones the class divides on idiosyncratically.

## Layout

```
clean.py                       shared cleaning: Likert -> -2..+2, drops the 5 empty responses (91 students)
Survey_Results_UC.csv          raw survey data
survey_clean.csv               cleaned data written by clean.py
report/report.tex|.pdf         the team report
index.html                     interactive portal
Student Network/               Network A: student_network.ipynb + student_plots/
Extreme Bipartite Network/     Networks B and C: main.ipynb + extreme_plots/ + Visualizers/
Question Network/              Network D: question_network.ipynb + figures
student_plots, question_plots, bipartite_plots
                               symlinks, so LaTeX can reach folders whose names contain spaces
```

`clean.py` lives at the repository root; `Student Network/` and `Question Network/` each hold a small shim of
the same name so their notebooks can `from clean import load_survey` unchanged. Networks A and D use it;
Network B applies its own 1–5 mapping and extremes filter.

## Reproducing

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace "Student Network/student_network.ipynb"
cd report && pdflatex report.tex && pdflatex report.tex
```

Running a notebook regenerates that network's figures in place; the report picks them up on the next build.

## Contributions

- **Mayank Kar** — Network A, the shared `clean.py`, and the team report in `report/`.
- **Tanush Garg** — Networks B and C, and the interactive D3 visualisers.
- **Amish Goyal** — Network D, the repository setup and its per-network layout, and `index.html`.
