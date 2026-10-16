# CAP-RELEASE Reconciliation and release

<!-- BEGIN GENERATED: header (just render) -->
Results are released per unit only when the unit reconciles against its register.

Layer L3 · domain: product · depends on: [CAP-REVIEW](cap-review.md).
<!-- END GENERATED: header -->

## Purpose

Release results only when every expected subject is accounted for.

## Why

A release is the point of no return; reconciliation against an external register is the last check before it.

## Interfaces

- A gate that reads BLOCKED or CLEAR per release unit.
- Register snapshots per sitting.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-RELEASE.1 | MUST | For each release unit, expected subjects (from an external register) balance against confirmed results; any duplicate, orphan, missing subject, pending identity or absent register reads BLOCKED. | Fixtures for each blocking condition read BLOCKED; a balanced unit reads CLEAR. |
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
