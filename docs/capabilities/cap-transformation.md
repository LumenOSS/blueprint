# CAP-TRANSFORMATION Transformation layer

Versioned, tested models from bronze to silver to gold; the only place metrics are computed.

Layer L3 · domain: data · depends on: [CAP-COMPUTE](cap-compute.md), [CAP-CATALOG](cap-catalog.md).

## Purpose

Compute every reported number in one versioned, tested place.

## Why

Conformance once means every consumer shares one identifier and one definition ([P11](../principles.md#p11-reporting-goes-through-a-governed-transformation-layer)).

## Interfaces

- Versioned models in bronze, silver and gold.
- Tests run in CI.
- Development schemas for development runs.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-TRANSFORMATION.1 | MUST | Models are versioned SQL (or equivalent) in bronze, silver and gold tiers, with tests that run in CI. | CI builds and tests the models on every change. |
| CAP-TRANSFORMATION.2 | MUST | Conformance happens once, in silver: each entity has one identifier shared by every consumer. | Gold models join on silver identifiers only. |
| CAP-TRANSFORMATION.3 | MUST | No metric or report value is computed in an application; applications select and format gold. | A test forbids the application's reporting code from opening a database connection to operational tables. |
| CAP-TRANSFORMATION.4 | MUST | Development runs write to development schemas inside the production catalog, which no consumer is granted. | Development schemas carry no consumer grants. |
| CAP-TRANSFORMATION.5 | SHOULD | Gold stores counts and sums, not ratios, so measures re-aggregate correctly. | Review gold columns; ratios are computed in the semantic layer. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | dbt (v1, Python) with dbt-databricks<br/>dbt task in Lakeflow Jobs |
| [oss](../implementations/oss.yaml) | dbt (v1, Python)<br/>dbt-trino adapter |
<!-- END GENERATED: implementations -->
