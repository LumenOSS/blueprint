# CAP-TABLES Open table format

<!-- BEGIN GENERATED: header (just render) -->
Transactional tables in an open format, readable by more than one engine.

Layer L1 · domain: data · depends on: [CAP-STORAGE](cap-storage.md).
<!-- END GENERATED: header -->

## Purpose

Tabular data is held in an open, transactional format that more than one engine can read.

## Why

Open formats keep the data readable even without the current vendor, and the exit test proves it ([P16](../principles.md#p16-open-formats-storage-separate-from-compute-federate-before-copying)). Holding table history for a set time is what makes a fallback window possible.

## Interfaces

- An open table format with atomic commits, schema evolution and time travel.
- Retention settings for each table, declared in code.

## Notes

Each statement against a transactional table is a commit, with its own metadata cost, so write in batches.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-TABLES.1 | MUST | Tables use an open, specified format with atomic commits, schema evolution and time travel. | The format's specification is public; a commit is atomic under concurrent writers. |
| CAP-TABLES.2 | MUST | Every table is readable by at least two independent engines. | Exit test: read a sample of gold tables with an engine other than the one that wrote them; counts and hashes match. |
| CAP-TABLES.3 | MUST | History retention is configurable per table and can be held during a fallback window. | Retention settings are declared in code; a hold suspends expiry. |
| CAP-TABLES.4 | SHOULD | Writers batch into set-based operations, because each statement is a commit. | Pipeline code issues one write per batch, not per row. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Delta Lake with UniForm |
| [oss](../implementations/oss.yaml) | Apache Iceberg |
<!-- END GENERATED: implementations -->
