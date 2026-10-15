# CAP-LINEAGE Lineage

Which inputs produced which outputs, captured as work runs.

Layer L1 · domain: data · depends on: [CAP-CATALOG](cap-catalog.md).

## Purpose

Record which inputs produced each output.

## Why

Lineage answers what a change will affect and where a number came from.

## Interfaces

- Lineage events emitted by jobs and transformations, collected by the catalog or a lineage service.

## Notes

Lineage exists only where an integration emits it. List the jobs without it.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-LINEAGE.1 | MUST | Table-level lineage is captured automatically for every job and transformation run. | For a gold table, lineage lists its upstream tables without manual entry. |
| CAP-LINEAGE.2 | SHOULD | Column-level lineage is captured where the engine supports it. | For a masked column, lineage shows the source column. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
