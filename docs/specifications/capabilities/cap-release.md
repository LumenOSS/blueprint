# CAP-RELEASE Reconciliation and release

<!-- BEGIN GENERATED: header (just render) -->
Results are released per unit only when the unit reconciles against its register.

Layer L3 · domain: product · depends on: [CAP-REVIEW](cap-review.md).
<!-- END GENERATED: header -->

## Purpose

Results are released only when every expected subject is accounted for.

## Why

Once results are released, they can't be taken back. Reconciling them against an external register is the last check before that point.

## Interfaces

- A gate that reads BLOCKED or CLEAR for each release unit.
- A snapshot of the register for each sitting.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-RELEASE.1 | MUST | For each release unit, expected subjects (from an external register) balance against confirmed results; any duplicate, orphan, missing subject, pending identity or absent register reads BLOCKED.<br><br>*Example:* A school's register lists 30 learners; 29 have confirmed results and one has none, so the school reads BLOCKED until the missing one is found or recorded as absent. | Fixtures for each blocking condition read BLOCKED; a balanced unit reads CLEAR. |
| CAP-RELEASE.2 | MUST | Results release only on CLEAR, and a release is recorded as the point after which changes are new versions. | A change after release creates a new version and leaves the released one intact. |
| CAP-RELEASE.3 | MUST | The register is read through an adapter and frozen as an immutable snapshot per sitting; corrections are deterministic, evented operations, never ad-hoc edits. | Each sitting references one snapshot; register corrections appear as events. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | The example product's release gate |
| [oss](../implementations/oss.yaml) | The example product's release gate |
<!-- END GENERATED: implementations -->
