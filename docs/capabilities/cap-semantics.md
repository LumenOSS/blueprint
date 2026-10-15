# CAP-SEMANTICS Semantic layer

Every measure defined once, versioned, and read by every consumer.

Layer L1 · domain: data · depends on: [CAP-TRANSFORMATION](cap-transformation.md).

## Purpose

Define each measure once so it means the same on every dashboard and in every answer.

## Why

A pass rate computed in two places will eventually differ ([P11](../principles.md#p11-reporting-goes-through-a-governed-transformation-layer)).

## Interfaces

- Measure and dimension definitions per domain, in version control.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-SEMANTICS.1 | MUST | Each measure and dimension is defined once, in version control, per domain. | No measure name has two definitions. |
| CAP-SEMANTICS.2 | MUST | Dashboards, natural-language queries and agents read measures through the semantic layer. | Dashboard and agent queries reference semantic-layer objects, not raw gold columns. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog metric views<br/>MetricFlow definitions as source |
| [oss](../implementations/oss.yaml) | MetricFlow |
<!-- END GENERATED: implementations -->
