# CAP-LINEAGE Lineage

<!-- BEGIN GENERATED: header (just render) -->
Which inputs produced which outputs, captured as work runs.

Layer L1 · domain: data · depends on: [CAP-CATALOG](cap-catalog.md).
<!-- END GENERATED: header -->

## Purpose

The platform records which inputs produced each output.

## Why

Lineage tells you what a change will affect, and where a number came from.

## Interfaces

- Lineage events emitted by jobs and transformations, and collected by the catalog or by a lineage service.

## Notes

You only get lineage where an integration emits it, so keep a list of the jobs that don't.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-LINEAGE.1 | MUST | Table-level lineage is captured automatically for every job and transformation run. | For a gold table, lineage lists its upstream tables without manual entry. |
| CAP-LINEAGE.2 | SHOULD | Column-level lineage is captured where the engine supports it. | For a masked column, lineage shows the source column. |
| CAP-LINEAGE.3 | SHOULD | Lineage is emitted as OpenLineage events, so lineage from different implementations can be compared. | Job runs emit OpenLineage run events. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [OpenLineage](../standards.md#metadata-and-data-quality) | Specification 1.x (1.54.0, 2026) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog lineage |
| [oss](../implementations/oss.yaml) | OpenLineage |
<!-- END GENERATED: implementations -->
