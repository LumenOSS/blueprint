# CAP-COMPUTE Compute

<!-- BEGIN GENERATED: header (just render) -->
Batch, streaming and interactive SQL compute that scales to zero and reads only through the catalog.

Layer L1 · domain: data · depends on: [CAP-CATALOG](cap-catalog.md).
<!-- END GENERATED: header -->

## Purpose

The platform runs batch, streaming and interactive work without paying for idle time, and it reads data only through the catalog.

## Why

Compute that scales to zero is what makes a production-only budget workable. Reading only through the catalog means every read is governed.

## Interfaces

- Job compute for pipelines, and a SQL endpoint for interactive queries.
- A workload identity for every job.

## Notes

A query's timeout is its service objective. If you probe with a long timeout, you hide the very thing you were trying to find.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-COMPUTE.1 | MUST | Compute scales to zero when idle. | Billing or node metrics show no compute between scheduled work. |
| CAP-COMPUTE.2 | MUST | Jobs run as non-human identities. | Every job's run-as principal is a workload identity. |
| CAP-COMPUTE.3 | MUST | Engines read and write data only through the catalog. | Direct storage paths are refused to engine identities. |
| CAP-COMPUTE.4 | MUST | Interactive queries behind an application meet a declared latency objective (the reference value is 5 seconds at p95), and the timeout is that objective, not a longer probe. | Measured p95 for the application's queries over a week. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Serverless jobs compute<br/>Serverless SQL warehouse |
| [oss](../implementations/oss.yaml) | Apache Spark 4 via Kubeflow spark-operator<br/>Trino<br/>DuckDB |
<!-- END GENERATED: implementations -->
