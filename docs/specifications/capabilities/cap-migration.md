# CAP-MIGRATION Migration and decommission

<!-- BEGIN GENERATED: header (just render) -->
Moving between platforms or accounts without loss, with a fallback window and two-role sign-off.

Layer L1 · domain: movement · depends on: [CAP-OPERATIONALDB](cap-operationaldb.md), [CAP-CLASSIFICATION](cap-classification.md).
<!-- END GENERATED: header -->

## Purpose

You can move to a new platform, account or region without losing data, and then retire the old one safely.

## Why

Copying tables loses their history, but re-binding the storage keeps it. A database move is only as good as the check that verifies it. A fallback window and sign-off by two roles keep a cutover reversible until it has been proven ([P13](../principles.md#p13-roles-not-names)).

## Interfaces

- A migration plan that lists each dataset as either re-bound or rebuilt.
- A rehearsed database move, with a verification report.
- A retirement tool that refuses to remove objects without tags.

## Notes

Database branches don't survive a dump and restore, so you have to recreate them. If a deployment unit declares managed storage, destroying the unit destroys that storage too.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-MIGRATION.1 | MUST | Lake data is moved by re-binding its storage to the new platform where possible; derived tables are rebuilt by their pipelines rather than copied. | The migration plan lists each dataset as re-bound or rebuilt. |
| CAP-MIGRATION.2 | MUST | An operational database moves by a rehearsed sequence: freeze writes, snapshot, dump, restore in one transaction, verify (row counts, per-table content hashes, sequences, policies, grants, migration ledger), repoint, unfreeze.<br><br>*Example:* Before cutover, a rehearsal restore matches row counts and per-table hashes for every table; the production run must produce the same report. | The rehearsal and the production run each leave a verification report that matches. |
| CAP-MIGRATION.3 | MUST | After cutover the old platform stays read-only for a fallback window (the reference value is 60 days), with history expiry held, until a restore drill passes on the new one. | Expiry jobs on the old platform are paused for the window; the drill report exists. |
| CAP-MIGRATION.4 | MUST | Cutover, rollback and decommission need sign-off from both the Data Lead and the Technical Lead; either may halt. | The decommission record carries both sign-offs. |
| CAP-MIGRATION.5 | MUST | Before any drop or decommission, each object's provenance is proved from first-hand evidence, audit is archived, and an immutable archive exists with a tested retrieval. Deletion is a plain delete, never a forced one. | The retirement tool refuses objects not tagged simulated or derived; the archive retrieval test has passed. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog storage re-binding<br/>pg_dump / pg_restore |
| [oss](../implementations/oss.yaml) | pg_dump / pg_restore<br/>Iceberg register-table |
<!-- END GENERATED: implementations -->
