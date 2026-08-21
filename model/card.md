# Model card

This file defines **which version of The Iceberg Model this checkout is**. It is the single
source of truth for the version triplet; the tag, `CHANGELOG.md`, and `CITATION.cff` reference
it. A release is a commit where this card changes, tagged with the version below.

```
instance:       Solaris
version:        1.0.0
architecture:   1
implementation: 0
configuration:  0
```

```
expected red: GR-34,GR-35,GR-36
record: tests/results/solaris-1.0.0.md
```

Semantic versioning `<instance> M.m.p`:

| Digit | Layer | Defined in | Bumped when |
|---|---|---|---|
| **M** = 1 | Architecture (the Iceberg manifest) | [`architecture.md`](architecture.md) + the paper | a postulate changes |
| **m** = 0 | Implementation (Solaris's mechanisms) | [`implementation.md`](implementation.md) | a mechanism changes (must re-sit the battery) |
| **p** = 0 | Configuration (parameter values) | [`configuration.md`](configuration.md) | a dial changes (must re-sit the battery) |

The `expected red` line above is read by CI: the examination battery is GREEN if and only if
the failing rows are exactly these pre-registered reds (the paper's "Difficulties", item 4).
