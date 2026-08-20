# The Iceberg Model

A two-layer computational toy architecture in which the classic mysteries of
quantum mechanics and relativity stop being mysterious: a **fixed-compute
substrate** whose load bookkeeping makes spacetime, gravity, and expansion
emerge, and an **append-only ledger** holding the state - entanglement as a
shared contract, measurement as settlement, the universal wave function
stored factorized. The claim is mechanism sufficiency, not empirical
adequacy: we are not claiming to have built the universe on a laptop.

**The paper is the model's manifest:** [`paper/the-iceberg-model.md`](paper/the-iceberg-model.md).
Further papers will join it as the model evolves.

## Run the examinations

```
pip install -r requirements.txt
python labs/run_exams.py all --record v4 --expect-red GR-34,GR-35,GR-36
```

Expected: **150 rows - 147 pass and exactly 3 red.** The red rows (GR-34..36)
are pre-registered findings kept deliberately (the paper's "Difficulties with
the theory", item 4): their pass marks were declared before the first run and
never softened. Row definitions live in `exams/tests/`; the recorded table in
`exams/results/`. Individual sets run by name: `python labs/run_exams.py QM GR`.

## Versions and branches

Semantic versioning `<instance> M.m.p`: **M** = architecture (manifest) major,
**m** = implementation iteration, **p** = configuration revision.

- **`main`** carries the reference instance, **Solaris** - the active main
  implementation. Releases are tags (`solaris-1.0.0`), each a citable snapshot.
- **`exp/*` branches** carry implementation or configuration experiments; an
  experiment merges to `main` (bumping m or p) only after sitting the full
  examination battery.
- A future second named instance would get its own long-lived branch; an
  architecture change bumps M on `main`.

## Licenses

Code: [MIT](LICENSE). Paper and documentation: [CC BY 4.0](LICENSE-docs.md).
Clone, fork, and build on it - with attribution.

## Contributing

Issues are open - the most valuable kind names a behaviour this model cannot
reproduce. See [CONTRIBUTING.md](CONTRIBUTING.md).
