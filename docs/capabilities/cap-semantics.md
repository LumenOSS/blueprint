# CAP-SEMANTICS Semantic layer

<!-- BEGIN GENERATED: header (just render) -->
Every measure defined once, beside the models that produce its counts, and served to every consumer from that one definition.

Layer L1 · domain: data · depends on: [CAP-TRANSFORMATION](cap-transformation.md).
<!-- END GENERATED: header -->

## Purpose

Define each measure once so it means the same on every dashboard and in every answer.

## Why

A pass rate computed in two places will eventually differ ([P11](../principles.md#p11-reporting-goes-through-a-governed-transformation-layer)).

## Interfaces

- Measure and dimension definitions per domain, in version control.

See [the semantic layer](../architecture/semantic-layer.md) for how one
definition is served to every consumer, and the portable-subset rules.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-SEMANTICS.1 | MUST | Each measure and dimension is defined once, in version control, per domain. | No measure name has two definitions. |
| CAP-SEMANTICS.2 | MUST | Dashboards, natural-language queries and agents read measures through the semantic layer. | Dashboard and agent queries reference semantic-layer objects, not raw gold columns. |
| CAP-SEMANTICS.3 | MUST | Each indicator carries metadata saying what it means and how to read it, how it is computed (numerator and denominator as separate measures, unit, reference-date rule), how it may be broken down, where its counts come from and how often, what coverage it needs before publication, and who owns which version of it. | A check finds no indicator with a missing metadata field. |
| CAP-SEMANTICS.4 | SHOULD | An indicator with an international definition follows the UIS Official List of SDG 4 Indicators and the UIS education glossary, records the edition it follows, and documents any deviation in its metadata. | Indicators that map to international definitions name them; deviations are listed. |
| CAP-SEMANTICS.5 | MUST | A denominator from outside the platform, such as a population estimate by age, is versioned reference data that names its source and vintage. | Indicators with external denominators reference a versioned reference table. |
| CAP-SEMANTICS.6 | MUST | Measure and indicator definitions live in the same versioned project as the transformation models that produce their counts, are changed in the same review, and are validated in CI. | CI runs the semantic layer's validation on every change. |
| CAP-SEMANTICS.7 | MUST | Published indicators use a portable subset of definitions (simple counts and sums, ratios, and derived expressions without time offsets), each indicator a ratio of additive counts on one gold table; any other construct has a recorded, tested mapping for each serving engine. | A CI lint lists every definition outside the portable subset with its mapping. |
| CAP-SEMANTICS.8 | MUST | Every artefact a consumer reads (engine-native metric objects, saved-query tables, dashboard datasets) is generated from the definitions by CI, never written by hand. | Generated artefacts carry a marker and are reproduced byte for byte by the generator. |
| CAP-SEMANTICS.9 | MUST | A parity test runs every saved query through every serving path and requires identical results. | The parity report lists each saved query and serving path with a match. |
| CAP-SEMANTICS.10 | SHOULD | Definitions can be exported in an open semantic interchange format once a released version is supported by the producing and consuming tools. | The export runs in CI and validates against the format's schema. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [International Standard Classification of Education (ISCED 2011)](../standards.md#education-classifications-and-indicators) | ISCED 2011 (published 2012) with Operational Manual (2015); amendment due 2027 | adopt |
| [Global indicator framework for the Sustainable Development Goals](../standards.md#education-classifications-and-indicators) | After 2026 refinement (UN Statistical Commission 57th session, March 2026; includes the 2025 Comprehensive Review) | adopt |
| [Official List of SDG 4 Indicators (global and thematic)](../standards.md#education-classifications-and-indicators) | October 2026 (post EDSC-12) | adopt |
| [UIS Glossary - Education Metadata](../standards.md#education-classifications-and-indicators) | 2026 (UIS/2026/ED/IP/32) | adopt |
| [Apache Ossie (Open Semantic Interchange)](../standards.md#open-data-and-exchange) | Specification 0.1.1 (December 2025); 0.2 in development; Apache incubating project | track |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | dbt semantic layer (dbt 1.12 or later, latest YAML spec)<br/>MetricFlow<br/>Unity Catalog metric views via the dbt-databricks metric_view materialisation |
| [oss](../implementations/oss.yaml) | dbt semantic layer (dbt 1.12 or later, latest YAML spec)<br/>MetricFlow<br/>Generated saved-query models |
<!-- END GENERATED: implementations -->
