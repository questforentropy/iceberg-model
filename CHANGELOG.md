# Changelog

## Unreleased

Repository restructure (2026-08-21): `model/` added (version card + the three
layer descriptions - the card is now the single source of truth for the
version triplet, and CI reads its expected-red line); `exams/` renamed to
`tests/` with version-independent `definitions/` and generated `results/`
that now record the declared criterion and measured detail beside each status.

## solaris-1.0.0 - 2026-08-20

First release: Iceberg manifest 1, reference instance Solaris, canonical
configuration (sprinkled 3-sphere). Examination record: 150 rows - 147 pass,
3 pre-registered red (GR-34..36, the kinematics-only verdict). The paper
(`paper/the-iceberg-model.md`) is the manifest of record.
