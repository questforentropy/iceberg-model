# The examination harness — approach and notation

Every claim the model makes is a numbered examination row. This file is the one place the
conventions are defined; the per-set files (`sub.md`, `qm.md`, …) carry only the set's
description and its row table.

## Numbering

Rows are numbered **SET-N** (QM-1, GR-37, …), **positional in lab print order**: the runner
walks the set's labs in their registered order and numbers the printed rows sequentially.
Consequently rows are **append-only** — new labs and new checks are added at the end, and
**IDs are never renumbered**. A row ID that has appeared in any recorded results table is
frozen forever.

## Statuses

| Status | Meaning |
|---|---|
| **PASS** | earned: the declared pass mark was met |
| **FAIL** | the declared mark was not met — **kept on the books** (see below) |
| **PASS\*** | passes *by construction*: an imported piece of physics guarantees it; the row is kept to say so |
| **IMPORTED** | a disclosure, not a pass: the behaviour is true because it was imported |
| **BANKED** | delegated: the evidence lives in the referenced row |
| **MERGED** | absorbed into another row (the referenced row carries the check) |
| **QUEUED** | defined, not yet run — the definition (with its pass mark) precedes the lab |
| **N/A** | subject absent in the model version being examined |

## The three house rules

1. **Declare-before-run.** Every row's pass mark is written down before the lab first runs,
   and may be made harder afterwards but never softer.
2. **Define-before-sit.** A new physics question enters as a QUEUED row with a declared mark
   before any model version attempts it.
3. **Failures are findings.** A pre-registered mark that is not met stays **red** in the
   record — it is never tuned away or deleted. Some rows exist precisely to record a
   *predicted* failure (marked as such in the row text); others record honest negative
   results. The current record carries three deliberate reds (GR-34..36: the model's
   dynamical hole does not obey Schwarzschild thermodynamics — the kinematics-only verdict).

## Running

```
python labs/run_exams.py all                      # run everything
python labs/run_exams.py QM GR                    # run sets by name
... --record solaris-1.0.0                        # also (re)generate exams/results/<name>.md
... --expect-red GR-34,GR-35,GR-36                # CI gate: exit 0 iff the reds are EXACTLY these
```

## Results files

One file per recorded campaign in `exams/results/`, named by the instance's semantic version
(`solaris-1.0.0.md`, …). Files named `v1..v4` are the historical build-ladder records of the
first implementation, kept as history.
