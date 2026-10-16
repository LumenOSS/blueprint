# CAP-TRANSFORMATION Transformation layer

<!-- BEGIN GENERATED: header (just render) -->
Versioned, tested models from bronze to silver to gold; the only place measures are computed.

Layer L3 · domain: data · depends on: [CAP-COMPUTE](cap-compute.md), [CAP-CATALOG](cap-catalog.md).
<!-- END GENERATED: header -->

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
| CAP-TRANSFORMATION.3 | MUST | No measure or report value is computed in an application; applications select and format gold. | A test forbids the application's reporting code from opening a database connection to operational tables. |
| CAP-TRANSFORMATION.4 | MUST | Development runs write to development schemas inside the production catalog, which no consumer is granted. | Development schemas carry no consumer grants. |
| CAP-TRANSFORMATION.5 | SHOULD | Gold stores counts and sums, not ratios, so measures re-aggregate correctly.<br><br>*Example:* Gold stores 'enrolled 412' and 'population 455', not '90.5 per cent', so a district figure is the sum of counts divided once, not an average of school percentages. | Review gold columns; ratios are computed in the semantic layer. |
| CAP-TRANSFORMATION.6 | MUST | Silver keeps effective-dated history for every relationship that changes over time (enrolment, posting, guardianship, programme), with valid-from, valid-to and recorded-at, and gold is computed as at a declared reference date.<br><br>*Example:* An enrolment valid from 2025-09-01 to 2026-03-15 is counted by a census with reference date 2026-02-01 and not by one dated 2026-10-01. | Silver relationship tables carry the three time columns; each gold model names its reference-date rule. |
| CAP-TRANSFORMATION.7 | MUST | A document about one record, such as a certificate, transcript or letter, may be produced by an application from operational data; any aggregate it prints (a rank, an average) comes from gold or the semantic layer.<br><br>*Example:* A transcript lists one learner's results straight from operational data, but the class average printed on it comes from the semantic layer. | Document templates read aggregates only through the semantic layer or gold. |
| CAP-TRANSFORMATION.8 | SHOULD | Credentials issued about a single record, such as certificates and transcripts, are W3C Verifiable Credentials 2.0, using Open Badges 3.0 or CLR 2.0 where they fit. | An issued credential fixture verifies with a standard verifier. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [1EdTech Comprehensive Learner Record 2.0 and Open Badges 3.0](../standards.md#open-data-and-exchange) | CLR 2.0 (doc 1.1, October 2025); Open Badges 3.0 (doc 1.4.5, June 2026) | adopt |
| [European Learning Model (European Digital Credentials for Learning)](../standards.md#open-data-and-exchange) | ELM 3.3 (2025) | reference |
| [Verifiable Credentials Data Model](../standards.md#open-data-and-exchange) | VC Data Model 2.0, W3C Recommendation (May 2025) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | dbt (v1, Python) with dbt-databricks<br/>dbt task in Lakeflow Jobs |
| [oss](../implementations/oss.yaml) | dbt (v1, Python)<br/>dbt-trino adapter |
<!-- END GENERATED: implementations -->
