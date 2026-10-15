# CAP-INGESTION Ingestion

Files, in-place federation and change data capture behind one onboarding step.

Layer L1 · domain: data · depends on: [CAP-ONBOARDING](cap-onboarding.md), [CAP-CATALOG](cap-catalog.md).

## Purpose

Bring data in by the cheapest method that works, without losing or duplicating any of it.

## Why

Federation avoids a copy; change capture is worth its cost only for some sources ([P16](../principles.md#p16-open-formats-storage-separate-from-compute-federate-before-copying)). Landing as a queue keeps the source of record safe and failures visible ([P8](../principles.md#p8-every-write-is-idempotent)).

## Interfaces

- A landing area with archive and quarantine.
- Federated (foreign) catalogs.
- Change data capture into bronze.

## Notes

An archive sweep copies, verifies size, then unlinks, and leaves alone anything it cannot account for.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-INGESTION.1 | MUST | Three ingestion methods are offered behind one onboarding step: files to a landing area, federation in place, and change data capture. The method is a value in the tenant entry. | Each method has a tenant entry in use or a test entry that plans cleanly. |
| CAP-INGESTION.2 | MUST | A landing area is a queue, not a store: accepted inputs move to a content-addressed archive after verification, and refused inputs move to quarantine with a reason. Nothing is deleted without a verified archive copy. | After a run, landing holds only unprocessed files; every quarantined file has a reason sidecar. |
| CAP-INGESTION.3 | MUST | Ingestion tolerates at-least-once delivery: a re-delivered input converges on the existing record by content hash or natural key. | Deliver the same input twice; row counts do not change. |
| CAP-INGESTION.4 | SHOULD | A source is federated in place before it is copied; change data capture is used where a copy is worth its cost; a custom extract is the last resort. | The tenant entry records why the chosen method was chosen. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Auto Loader<br/>Lakehouse Federation<br/>Lakeflow Connect |
| [oss](../implementations/oss.yaml) | Debezium on Kafka via Strimzi<br/>Trino connectors<br/>Landing bucket + pipeline |
<!-- END GENERATED: implementations -->
