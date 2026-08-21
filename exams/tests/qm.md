# Set QM — the quantum exam

Labs, in numbering order: `qm_tests.py` (QM-1..9), `ch_retake.py` (QM-10..29 = the CH-01..CH-19 retake of episode #3's suite), `born_settlement_scout.py` (QM-30..31), `lg_scout.py` (QM-32..33).

| ID | Row | Verifies |
|---|---|---|
| QM-1 | C0 | singlet correlation E(d) = −cos d at all angle gaps + CHSH at 2√2 |
| QM-2 | Q1 | repeatability: same-axis remeasurement always agrees |
| QM-3 | Q2 | post-measurement blurring: Z,X,Z chain agrees at 1/2 |
| QM-4 | Q4 | a which-path record kills interference (visibility → 0) |
| QM-5 | Q5 | GHZ/Mermin M = 4 exactly, every round (LHV best: 2) |
| QM-6 | Q6 | monogamy: Toner bound S_AB + S_AC ≤ 4 across GHZ/singlet/W |
| QM-7 | Q7 | no-signalling across all setting pairs |
| QM-8 | Q8 | record consistency: ledger read = re-measurement, for every reader |
| QM-9 | Q9 | consensus spread (quantum-Darwinism ring): monotone coverage, reversal cost = replicas |
| QM-10 | CH-01 | Born statistics: P = cos² to tolerance |
| QM-11 | CH-02 | frame shift leaves statistics invariant |
| QM-12 | CH-03 | marginal independent of partner's measurement context |
| QM-13 | CH-04 | superposition (V ≈ 1) vs mixture (V ≈ 0) distinguished |
| QM-14 | CH-05 | harmonic purity: no higher harmonics in the fringe |
| QM-15 | CH-06 | exact null at φ = π (PASS\* — exact because amplitudes are imported) |
| QM-16 | CH-07 | visibility law V(η) = cos(η/2) |
| QM-17 | CH-08 | recorded pattern = average of single-path patterns |
| QM-18 | CH-09 | repeatability (BANKED = QM-2) |
| QM-19 | CH-09b | 3-step chain = product of conditionals (Markov property) |
| QM-20 | CH-10 | post-measurement blurring (BANKED = QM-3) |
| QM-21 | CH-11 | early-drawn vs late-drawn choice indistinguishable (delayed choice) |
| QM-22 | CH-12 | silent detector still collapses (null-outcome measurement) |
| QM-23 | CH-13 | quantum eraser: sorting restores anti-phased fringes |
| QM-24 | CH-14 | complementarity: V² + D² = 1 |
| QM-25 | CH-15 | no-signalling (BANKED = SUB-7 + QM-7) |
| QM-26 | CH-16 | CHSH = 2√2 (PASS\* — THE MACHINE'S UNFINISHED ROW; passes because the correlation rule is imported) |
| QM-27 | CH-17 | apparatus recoil (MERGED into QM-24: the apparatus IS the record qubit) |
| QM-28 | CH-18 | complex-unitary observer view (IMPORTED — disclosure, not a pass) |
| QM-29 | CH-19 | no joint block: unentangled watcher gains nothing, visibility stays 1 |
| QM-30 | DE1 | (`born_settlement_scout.py`) the signature ladder: 1 signer ∝ \|α\| (wrong), 2 signers = Born, 3 ∝ \|α\|³ (wrong) — the square comes from dyadic settlement |
| QM-31 | DE2 | full QM battery with the Born line replaced by double-entry settlement — everything passes; residual import = norm-linear acceptance per signer |
| QM-32 | LG1 | (`lg_scout.py`) Leggett–Garg watcher controls capped at 1: passive rotor sits exactly ON the ceiling (gaps ≤ 90°); ledger settled at all three checkpoints writes a diary of triples, K = 2cos t − cos²t ≤ 1 |
| QM-33 | LG2 | temporal Bell violation by the fold: two checkpoints per run, three batches, settlement re-preparation → K = 2cos t − cos 2t, 3/2 at 60° (temporal Tsirelson) — identical under the double-entry sampler (article #11 cross-link) |
