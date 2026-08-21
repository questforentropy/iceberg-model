# Set ENT — entropy proper

Lab: `ent_scouts.py` (ENT-1..4), first rows cut 2026-08-17. Queued additions: the KS-rate port from the entropy stream's measured instrument (bits/collision on the full contract engine, not the binary chain).

| ID | Row | Verifies |
|---|---|---|
| ENT-1 | EN1 | entropy written per fold = Born H(cos²), memoryless; compressor floored at H — the ledger pays full price for every fold |
| ENT-2 | EN2 | memory or compute, both explode: archive linear in folds; replay-from-genesis linear in time (the C3 storage bill, measured) |
| ENT-3 | EN3 | the arrow is structural: the head hash is an injective accumulator of all history — recurrence would need a hash collision (150k folds, zero repeats) |
| ENT-4 | EN4 | the fold split: 100 pre-states → 2 records (observer cannot invert) BUT full replay is bit-exact (substrate can) — L2 fold, L3 rewind, measured |
| ENT-5 | — | *(queued, parked 2026-08-19)* fold-entropy audit: ledger information NEVER decreases at a fold — ΔI ≥ 0 for every fold type (append-only makes decrease structurally impossible; turn ENT-3's argument into a per-fold measurement) |
| ENT-6 | — | *(queued, parked — SPLIT-1)* thread splitting drives the stretch: one high-density thread splits into many low-density threads (γ → microwaves), thread count ↑ → load ↑ → z-rate ↑, extending the EX-16 closed loop — **entropy as the cause of perceived expansion** (user conjecture 2026-08-19) |
| ENT-7 | — | *(queued, parked — SPLIT-2)* elastic vs fold reversibility: elastic interactions invert for free, folds demand H(outcome) compensation bits — the sf-ghosts (XOR+ADD) instrument ported to the contract engine |
