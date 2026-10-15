# CAP-BACKFILL Backfill and reprocessing

Loading history, reprocessing and filling gaps are idempotent, bounded, rehearsed and reconciled.

Layer L3 · domain: movement · depends on: [CAP-ORCHESTRATION](cap-orchestration.md), [CAP-ENVIRONMENTS](cap-environments.md), [CAP-QUALITY](cap-quality.md).

## Purpose

Load history, reprocess after a logic change, and fill gaps without duplicates, data loss or harm to production.

## Why

Backfills run rarely, under pressure, over more data than anything else; they are where idempotence, determinism and reconciliation are tested hardest ([P8](../principles.md#p8-every-write-is-idempotent), [P9](../principles.md#p9-determinism)). See the [backfill patterns](../patterns/backfill.md).

## Interfaces

- Range-declared jobs; write-audit-publish; a reconciliation report per partition.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-BACKFILL.1 | MUST | A backfill declares its range and writes by replacing exactly that range or merging on a natural key, so running it twice gives the same result. | Run the backfill twice; content hashes of the range match and rows outside it are unchanged. |
| CAP-BACKFILL.2 | MUST | Every output row records the logic version and run that produced it, and event time separately from load time. | Restated rows show the new logic version; event and load time columns are both present. |
| CAP-BACKFILL.3 | MUST | A backfill runs first on a branch or an unpublished copy, is audited there, and is published only after it passes. | The run log shows write, audit and publish steps in that order. |
| CAP-BACKFILL.4 | MUST | A backfill is reconciled against its source by row counts, sums and content hashes per partition. | The reconciliation report exists and matches for every partition. |
| CAP-BACKFILL.5 | MUST | A backfill is bounded and throttled so that production work and the source system keep their service levels. | Production latency and source load stay within objectives during the backfill. |
| CAP-BACKFILL.6 | MUST | A backfill never overwrites fresher data or a human decision. | Test with a row updated after the backfill's snapshot and a human-ruled row; both survive. |
| CAP-BACKFILL.7 | MUST | Source rows that fail quality checks are quarantined with a reason, never dropped. | Counts reconcile as loaded plus quarantined equals extracted. |
| CAP-BACKFILL.8 | MUST | Incremental extraction tolerates late commits and clock skew, with an overlap window into an idempotent sink or a cursor in commit order. | Commit a row whose timestamp is behind the watermark; it is still loaded. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Lakeflow Jobs backfill runs<br/>Delta replaceWhere / MERGE<br/>Shallow clones |
| [oss](../implementations/oss.yaml) | Airflow 3 backfills<br/>Iceberg branches<br/>dbt microbatch |
<!-- END GENERATED: implementations -->
