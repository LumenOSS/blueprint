# CAP-COMPUTE Compute

Batch, streaming and interactive SQL compute that scales to zero and reads only through the catalog.

Layer L1 · domain: data · depends on: [CAP-CATALOG](cap-catalog.md).

## Purpose

Run batch, streaming and interactive work without idle cost, and only through the catalog.

## Why

Compute that scales to zero makes production-only budgets workable. Reading only through the catalog keeps every read governed.

## Interfaces

- Job compute for pipelines; a SQL endpoint for interactive queries.
- Workload identities for every job.

## Notes

A query's timeout is its service objective. Probing with a long timeout hides the finding.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-COMPUTE.1 | MUST | Compute scales to zero when idle. | Billing or node metrics show no compute between scheduled work. |
| CAP-COMPUTE.2 | MUST | Jobs run as non-human identities. | Every job's run-as principal is a workload identity. |
| CAP-COMPUTE.3 | MUST | Engines read and write data only through the catalog. | Direct storage paths are refused to engine identities. |
| CAP-COMPUTE.4 | MUST | Interactive queries behind an application meet a declared latency objective (the reference value is 5 seconds at p95), and the timeout is that objective, not a longer probe. | Measured p95 for the application's queries over a week. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Serverless jobs compute<br/>Serverless SQL warehouse |
| [oss](../implementations/oss.yaml) | Apache Spark 4 via Kubeflow spark-operator<br/>Trino<br/>DuckDB |
<!-- END GENERATED: implementations -->
