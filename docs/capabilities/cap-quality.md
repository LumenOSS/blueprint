# CAP-QUALITY Data quality

Checks at every tier; failing data is quarantined, never used.

Layer L3 · domain: data · depends on: [CAP-TRANSFORMATION](cap-transformation.md).

## Purpose

Keep bad data from consumers and keep it visible.

## Why

Data that fails its checks is worse than no data ([P10](../principles.md#p10-low-confidence-goes-to-a-person-never-guessed)). Counting refusals apart from failures tells a bad source from a broken system.

## Interfaces

- Checks per tier; a quarantine with reasons; source contracts.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-QUALITY.1 | MUST | Each tier has checks, and data that fails a blocking check does not reach consumers; it is quarantined with a reason. | Inject a failing row; it appears in quarantine and not in gold. |
| CAP-QUALITY.2 | MUST | Refused input and system failure are counted and reported separately. | Metrics distinguish the two; each has its own alert. |
| CAP-QUALITY.3 | SHOULD | Each source has a declared contract (schema, keys, freshness) checked on arrival. | Change a source's schema in a test; arrival checks fail loudly. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | dbt tests and contracts<br/>Lakeflow pipeline expectations<br/>Data Quality Monitoring |
| [oss](../implementations/oss.yaml) | dbt tests and contracts<br/>Great Expectations (GX Core) |
<!-- END GENERATED: implementations -->
