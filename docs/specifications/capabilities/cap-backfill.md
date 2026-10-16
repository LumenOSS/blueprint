# CAP-BACKFILL Backfill and reprocessing

<!-- BEGIN GENERATED: header (just render) -->
Loading history, reprocessing and filling gaps are idempotent, bounded, rehearsed and reconciled.

Layer L3 · domain: movement · depends on: [CAP-ORCHESTRATION](cap-orchestration.md), [CAP-ENVIRONMENTS](cap-environments.md), [CAP-QUALITY](cap-quality.md).
<!-- END GENERATED: header -->

## Purpose

You can load history, reprocess data after a change of logic, and fill gaps, without creating duplicates, losing data or harming production.

## Why

Backfills run rarely, often under pressure, and over more data than any other job. That makes them the hardest test of idempotence, determinism and reconciliation ([P8](../principles.md#p8-every-write-is-idempotent), [P9](../principles.md#p9-determinism)). The [backfill patterns](../../guides/backfill.md) describe how to run them.

## Interfaces

- Jobs that declare the range they cover.
- A write-audit-publish sequence.
- A reconciliation report for each partition.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-BACKFILL.1 | MUST | A backfill declares its range and writes by replacing exactly that range or merging on a natural key, so running it twice gives the same result.<br><br>*Example:* Reloading 2019 attendance replaces exactly the 2019 partitions; running it twice leaves identical hashes, and 2020 is untouched. | Run the backfill twice; content hashes of the range match and rows outside it are unchanged. |
| CAP-BACKFILL.2 | MUST | Every output row records the logic version and run that produced it, and event time separately from load time. | Restated rows show the new logic version; event and load time columns are both present. |
| CAP-BACKFILL.3 | MUST | A backfill runs first on a branch or an unpublished copy, is audited there, and is published only after it passes. | The run log shows write, audit and publish steps in that order. |
| CAP-BACKFILL.4 | MUST | A backfill is reconciled against its source by row counts, sums and content hashes per partition. | The reconciliation report exists and matches for every partition. |
| CAP-BACKFILL.5 | MUST | A backfill is bounded and throttled so that production work and the source system keep their service levels. | Production latency and source load stay within objectives during the backfill. |
| CAP-BACKFILL.6 | MUST | A backfill never overwrites fresher data or a human decision.<br><br>*Example:* A backfill from a 2024 extract would mark a learner active, but a reviewer recorded a transfer in 2025; the later human decision stays. | Test with a row updated after the backfill's snapshot and a human-ruled row; both survive. |
| CAP-BACKFILL.7 | MUST | Source rows that fail quality checks are quarantined with a reason, never dropped. | Counts reconcile as loaded plus quarantined equals extracted. |
| CAP-BACKFILL.8 | MUST | Incremental extraction tolerates late commits and clock skew, with an overlap window into an idempotent sink or a cursor in commit order.<br><br>*Example:* A record updated by a long transaction that started before the last extract but committed after it is still picked up, because each run reads an overlap window into an idempotent load. | Commit a row whose timestamp is behind the watermark; it is still loaded. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Lakeflow Jobs backfill runs<br/>Delta replaceWhere / MERGE<br/>Shallow clones |
| [oss](../implementations/oss.yaml) | Airflow 3 backfills<br/>Iceberg branches<br/>dbt microbatch |
<!-- END GENERATED: implementations -->
