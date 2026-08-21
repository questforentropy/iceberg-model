# Architecture 1 — the Iceberg manifest

The architecture layer is what the model *is*; it carries the demystification claim. **The
manifest of record is the paper** ([`../paper/the-iceberg-model.md`](../paper/the-iceberg-model.md),
§1–§3) — this file is its structural summary. Changing anything on this page bumps the major
version. The architecture is author-ruled: propose changes via issues (see `CONTRIBUTING.md`).

## Two principles and one coupling

**Principle 1 — the visible layer: a fixed-compute substrate.** Space is a static sprinkle of
compute grains laid down once at genesis; every physical process pays for its steps from a
fixed local budget. Load slows the local rate of everything uniformly — from which time
dilation, gravity (congestion), black holes (asymptotic compute starvation, no singularity),
and the observer-centered horizon (the causality limit of a closed fabric) *emerge as
bookkeeping*, not as installed rules.

**Principle 2 — the hidden layer: an append-only ledger.** A fact is a transaction co-signed
by the participants; there is no master dashboard and no global now. Entanglement is a shared
contract; measurement is settlement (the fold — irreversible for the in-layer observer,
replayable by the substrate); the universal wave function is the contract graph stored
factorized. Pending branches carry amplitudes and interfere until settled — the model's named
residual import.

**The coupling — every write costs budget.** Settlement appends to the record; the record's
growth is the substrate's storage bill. Entropy production therefore *drives* the visible
layer: the global stretch (expansion) is the bill for the growing record, and the shape of the
record-growth curve is the candidate mechanism for dark energy.

## The essence

The claim is **demystification by perspective**: every classic mystery is a question that
quietly assumes a master screen showing "the real state right now." The architecture deletes
the dashboard and puts the observer *inside* — a company with no head office; a house of
warped mirrors. What remains are bookkeeping questions with measured answers, catalogued in
the paper's §5 and examined row by row in `tests/`.
