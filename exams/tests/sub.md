# Set SUB — substrate & ledger mechanics

Labs, in numbering order: `smoke_test.py` (SUB-1..10), `chain_randomness_scout.py` (SUB-11..15), `uwf_scout.py` (SUB-16..18), `uwf_scout2.py` (SUB-19..21).

| ID | Row | Verifies |
|---|---|---|
| SUB-1 | S1a | determinism: same genesis → bit-identical transcript |
| SUB-2 | S1b | sensitivity: different genesis → different transcript |
| SUB-3 | S2 | causal DAG integrity: all hashes recompute; parents precede children |
| SUB-4 | S3a | CHSH from the shared contract reaches 2√2 |
| SUB-5 | S3b | LHV control stays ≤ 2 (the harness can see the classical ceiling) |
| SUB-6 | S3c | PR-box control reaches 4 (the harness can see the algebraic ceiling) |
| SUB-7 | S4 | no-signalling: each party's marginal deaf to the partner's setting |
| SUB-8 | S5 | measurement-order invariance (no preferred frame in settlement) |
| SUB-9 | S6 | no-conspiracy: settings re-hashed from own history, uncorrelated with the pair seed |
| SUB-10 | S7 | ancestry audit: correlated outcomes with NO in-layer causal path between the measurements |
| SUB-11 | R1 | chain-fed randomness (P6 amended): determinism survives head-fed draws |
| SUB-12 | R2 | CHSH intact when every draw consumes the current head hash |
| SUB-13 | R3 | no-signalling intact under head-fed draws |
| SUB-14 | R4 | order invariance intact under head-fed draws |
| SUB-15 | R5 | no-conspiracy intact under head-fed draws (ledger = its own dice) |
| SUB-16 | U1 | (`uwf_scout.py`) the ledger IS the universal wave function stored factorized: random circuit universes run as global 2^n table vs contract DAG (merge = tensor, settlement = re-factorize), event-keyed draws → outcomes bit-identical, re-tensored DAG = Ψ entry-by-entry (~1e-15) |
| SUB-17 | U2 | sparsity: settlements keep live storage well under 2^n (measured: mean peak 55 amps vs 256 global; 97% of universes never reach global size) — pay 2^k only where entanglement lives |
| SUB-18 | U3 | the Everett corner: never settle → contracts merge to ONE 2^n factor equal to the textbook table exactly — universal Ψ is the DAG's settlement-free limit |
| SUB-19 | SN1 | (`uwf_scout2.py`) the snapshot isomorphism (Chandy–Lamport): two valid cuts → DIFFERENT instantaneous Ψ (min gap 0.316) yet IDENTICAL settled records 20/20; two linear extensions of one cut → same Ψ (the cut is bookkeeping, the record is physics); freeze-now wall-clock snapshot violates conservation 20/20 (in-flight records missed), consistent snapshot conserves 20/20 — **no global now, measured** |
| SUB-20 | SC1 | the entanglement phase diagram: pre-registered singleton law 1−r CONFIRMED (0.85/0.85, 0.74/0.75); pre-registered r_c = 1 REFUTED — gel onsets between r = 0.25 and 0.5 (merges pick particles → multiplicative kernel, ER giant-component physics; the failed prediction is the finding); subcritical tail exponential (R² 0.974); pure-merge limit → one cluster of N — **many-worlds is the gel phase; a settling world stays sol** |
| SUB-21 | SC2 | the linear-storage law + THE STORAGE TRANSITION: cheap phase S = c(r)·N with c(0.05)=2.00, c(0.1)=2.02 (R² 1.0000, stable across N within 1%); linearity needs the size tail to beat 2^k (slope > ln 2) — slope 2.18 at r=0.1 vs 0.78 at r=0.2 where storage is directly fluctuation-dominated (a second threshold BEFORE percolation); labeled toy extrapolation: N=10^80 → ~10^82 bits, UNDER the Bekenstein 10^122 ceiling, vs the flat table's 10^(3×10^79) numbers |
| SUB-22 | — | *(queued — the scheduler ablation, user insight 2026-08-20)* the scheduler is not load-bearing: re-run the battery with a cooperative single-threaded await runtime (settlement computed when awaited = lazy) in place of the eager loop → statistics identical; eager vs deferred settlement = two SCHEDULERS of one architecture, indistinguishable in-layer (extends SUB-8/14 order invariance, SN1 linear extensions, QM-21 delayed choice into a full implementation swap) |
