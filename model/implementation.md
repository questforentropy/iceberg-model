# Implementation 0 — Solaris's mechanisms

The implementation layer names the concrete mechanisms realizing each architectural principle.
Changing any mechanism bumps the minor version and requires re-sitting the full examination
battery. Several implementations may legally coexist as branches, each with its own record.

## Mechanism choices (implementation 0)

| Mechanism | Choice | Evidence rows |
|---|---|---|
| Load composition | **linear**: local rate c = 1/(1+L) | GR-1..33 |
| Budget exchange | wave-type neighbor exchange with memory (ballistic at c; statics Poisson) | GR-6, FLU-6 |
| Settlement rule | **double-entry**: two signatures per fact → Born statistics from the signature ladder | QM-30..31 |
| Randomness | chain-fed: every draw consumes the current head hash (the ledger is its own dice) | SUB-11..15 |
| Flux sector | derived, not painted: moving demand drags a budget circulation | FLU-6..8 |
| Scheduler | eager settlement loop (the lazy/await swap is the queued ablation) | SUB-22 (queued) |

**Known implementation candidate:** the **compounding composition law** c = e^(−Φ) (rates
multiply — each shell taxes the already-taxed rate). Measured on this codebase (GR-37..39):
β = 1 recovered (the +17% Mercury deviation of the linear law closes to +0.7%), γ = 1 kept, no
coordinate horizon. Its adoption as the default would be **implementation 1** (Solaris 1.1.0)
and re-sits the battery on its own branch first.

## Row-ID ↔ lab map

Row IDs are positional in print order (see `../tests/README.md`); the runner's `SETS` table in
`../labs/run_exams.py` fixes the lab order per set. For this implementation:

| Set | Labs (in numbering order) |
|---|---|
| SUB | `smoke_test.py` (SUB-1..10) · `chain_randomness_scout.py` (SUB-11..15) · `uwf_scout.py` (SUB-16..18) · `uwf_scout2.py` (SUB-19..21) |
| QM | `qm_tests.py` (QM-1..9) · `ch_retake.py` (QM-10..29) · `born_settlement_scout.py` (QM-30..31) · `lg_scout.py` (QM-32..33) |
| QX | `x_exams.py` (QX-1..10) · `tsirelson_scout.py` (QX-11..12) |
| ST | `spacetime_tests.py` (ST-1..4) |
| GR | `v2_gravity_scout.py` (GR-1..4) · `v2_gravity_scout2.py` (GR-5..6) · `w1_why_fall.py` (GR-7..8) · `cow_exam.py` (GR-9..12) · `length_scouts.py` (GR-13..15) · `sphere_gr_scout.py` (GR-16..22) · `gr_tier_b.py` (GR-23..28) · `gr_ripples_3d.py` (GR-29) · `gr_3d.py` (GR-30..33) · `gr_first_law.py` (GR-34..36) · `gr_compounding.py` (GR-37..39) |
| EN | `noether_scouts.py` (EN-1..4) · `unruh_scout.py` (EN-5..6) |
| EX | `v3_expansion_scout.py` (EX-1..3) · `m2_breathing_fabric.py` (EX-4..8) · `m3_closed_fabric.py` (EX-9..11) · `h1_ball_horizon.py` (EX-12..14) · `ex_closed_loop.py` (EX-15..17) |
| DS | `discreteness_scout.py` (DS-1..2) · `ds_fineness_blur.py` (DS-3) |
| ENT | `ent_scouts.py` (ENT-1..4) |
| FLU | `fluid_scouts.py` (FLU-1..5) · `fluid_scouts2.py` (FLU-6..8) |
| BH | `bh_scouts.py` (BH-1..3) · `bh_scouts2.py` (BH-4..6) |

## Build-ladder decoder

Names like **V1..V5** appearing in lab filenames and docstrings are the *internal build stages*
through which implementation 0 was developed — history, not release versions:

- **V1** — the first ledger engine and the quantum suite (contracts, settlement, CHSH).
- **V2** — gravity as congestion (`v2_gravity_scout*.py`).
- **V3** — expansion as the storage bill; the engine recognized as a Madelung fluid.
- **V4** — the flowing fabric: flux derived, dumb-hole horizons, the 3D port.
- **V5** — the *proposed* ball ledger (surface = compute screen, interior = archived history);
  never built — it changes a postulate, so it would be **architecture 2**, not a build stage.

The historical build-ladder records (`v1..v4`) are retained in the project's archive; the
released record for this implementation is `../tests/results/solaris-1.0.0.md`.
