# Contributing

The model is structured in three layers, and so are contributions:

1. **Architecture** (the postulates; the paper's sections 1-3): author-ruled.
   Propose changes via issues; architecture PRs are discussion-only.
2. **Implementations** (mechanisms): proposable. An implementation PR must
   (a) define its examination rows FIRST, with pass marks declared before any
   result exists (append-only row IDs, never renumber), and (b) sit the full
   battery: `python labs/run_exams.py all --expect-red GR-34,GR-35,GR-36`
   must come back GREEN (all rows pass except exactly the declared reds).
3. **Configurations** (parameter values): fork and experiment freely; a config
   PR needs only the battery gate.

**Current phase: issues open, pull requests by invitation.** The most useful
issue names a measured behaviour of quantum mechanics, relativity, or
cosmology that this model cannot reproduce - candidate examination rows are
how this model grows.

House rules: pass marks are never softened after a run; failures are findings
and stay on the books; every number in a claim must be printed by code in
this repository.
