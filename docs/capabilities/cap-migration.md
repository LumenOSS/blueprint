# CAP-MIGRATION Migration and decommission

Moving between platforms or accounts without loss, with a fallback window and two-role sign-off.

Layer L1 · domain: movement · depends on: [CAP-OPERATIONALDB](cap-operationaldb.md), [CAP-CLASSIFICATION](cap-classification.md).

## Purpose

Move to a new platform, account or region without losing data, and retire the old one safely.

## Why

Copying loses table history; re-binding storage keeps it. A database move is only as good as its verification. A fallback window and two-role sign-off make a cutover reversible until it is proven ([P13](../principles.md#p13-roles-not-names)).

## Interfaces

- A migration plan listing each dataset as re-bound or rebuilt.
- A rehearsed database move with a verification report.
- A retirement tool that refuses untagged objects.

## Notes

Database branches do not survive a dump and restore; recreate them. A deployment unit that declares managed storage takes that storage with it when destroyed.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-MIGRATION.1 | MUST | Lake data is moved by re-binding its storage to the new platform where possible; derived tables are rebuilt by their pipelines rather than copied. | The migration plan lists each dataset as re-bound or rebuilt. |
| CAP-MIGRATION.2 | MUST | An operational database moves by a rehearsed sequence: freeze writes, snapshot, dump, restore in one transaction, verify (row counts, per-table content hashes, sequences, policies, grants, migration ledger), repoint, unfreeze. | The rehearsal and the production run each leave a verification report that matches. |
| CAP-MIGRATION.3 | MUST | After cutover the old platform stays read-only for a fallback window (the reference value is 60 days), with history expiry held, until a restore drill passes on the new one. | Expiry jobs on the old platform are paused for the window; the drill report exists. |
| CAP-MIGRATION.4 | MUST | Cutover, rollback and decommission need sign-off from both the Data Lead and the Technical Lead; either may halt. | The decommission record carries both sign-offs. |
| CAP-MIGRATION.5 | MUST | Before any drop or decommission, each object's provenance is proved from first-hand evidence, audit is archived, and an immutable archive exists with a tested retrieval. Deletion is a plain delete, never a forced one. | The retirement tool refuses objects not tagged simulated or derived; the archive retrieval test has passed. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
