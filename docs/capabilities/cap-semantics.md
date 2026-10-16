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
| CAP-SEMANTICS.3 | MUST | Each indicator carries metadata saying what it means and how to read it, how it is computed (numerator and denominator as separate measures, unit, reference-date rule), how it may be broken down, where its counts come from and how often, what coverage it needs before publication, and who owns which version of it. | A check finds no indicator with a missing metadata field. |
| CAP-SEMANTICS.4 | SHOULD | An indicator with an international definition follows the UIS Official List of SDG 4 Indicators and the UIS education glossary, records the edition it follows, and documents any deviation in its metadata. | Indicators that map to international definitions name them; deviations are listed. |
| CAP-SEMANTICS.5 | MUST | A denominator from outside the platform, such as a population estimate by age, is versioned reference data that names its source and vintage. | Indicators with external denominators reference a versioned reference table. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [International Standard Classification of Education (ISCED 2011)](../standards.md#education-classifications-and-indicators) | ISCED 2011 (published 2012) with Operational Manual (2015); amendment due 2027 | adopt |
| [Global indicator framework for the Sustainable Development Goals](../standards.md#education-classifications-and-indicators) | After 2026 refinement (UN Statistical Commission 57th session, March 2026; includes the 2025 Comprehensive Review) | adopt |
| [Official List of SDG 4 Indicators (global and thematic)](../standards.md#education-classifications-and-indicators) | October 2026 (post EDSC-12) | adopt |
| [UIS Glossary - Education Metadata](../standards.md#education-classifications-and-indicators) | 2026 (UIS/2026/ED/IP/32) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog metric views<br/>MetricFlow definitions as source |
| [oss](../implementations/oss.yaml) | MetricFlow |
<!-- END GENERATED: implementations -->
