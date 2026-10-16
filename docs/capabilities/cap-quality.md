# CAP-QUALITY Data quality

Checks at every tier; failing data is quarantined, never used.

Layer L3 · domain: data · depends on: [CAP-TRANSFORMATION](cap-transformation.md).

## Purpose

Keep bad data from consumers and keep it visible.

## Why

Data that fails its checks is worse than no data ([P10](../principles.md#p10-low-confidence-goes-to-a-person-never-guessed)). Counting refusals apart from failures tells a bad source from a broken system.

## Interfaces

- Checks per tier; a quarantine with reasons; source contracts.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-QUALITY.1 | MUST | Each tier has checks, and data that fails a blocking check does not reach consumers; it is quarantined with a reason. | Inject a failing row; it appears in quarantine and not in gold. |
| CAP-QUALITY.2 | MUST | Refused input and system failure are counted and reported separately. | Metrics distinguish the two; each has its own alert. |
| CAP-QUALITY.3 | SHOULD | Each source has a declared contract (schema, keys, freshness) checked on arrival. | Change a source's schema in a test; arrival checks fail loudly. |
| CAP-QUALITY.4 | MUST | Every check names the ISO/IEC 25012 data-quality characteristic it measures (for example accuracy, completeness, consistency, credibility or currentness) and its severity. | The check registry has a dimension and severity for every check. |
| CAP-QUALITY.5 | MUST | An error found after load is fixed by a correction request approved by the data's steward; the correction lands as a new version, never an edit in place, and the request is kept with the record. | A correction fixture produces a new version linked to its request; the old version stays readable. |
| CAP-QUALITY.6 | SHOULD | Checks that compare two sources which should agree are declared as blocking or warning. | Each cross-source check states its effect. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [Education Data Quality Assessment Framework (Ed-DQAF)](../standards.md#metadata-and-data-quality) | 2017 manual, instruments and matrix | reference |
| [ISO/IEC 25012 Data quality model](../standards.md#metadata-and-data-quality) | ISO/IEC 25012:2008, confirmed 2025 | adopt |
| [ISO/IEC 25024 Measurement of data quality](../standards.md#metadata-and-data-quality) | ISO/IEC 25024:2015, confirmed 2022 | reference |
| [UN National Quality Assurance Frameworks Manual for Official Statistics](../standards.md#official-statistics-and-disclosure-control) | 2019 (ST/ESA/STAT/SER.M/100) | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | dbt tests and contracts<br/>Lakeflow pipeline expectations<br/>Data Quality Monitoring |
| [oss](../implementations/oss.yaml) | dbt tests and contracts<br/>Great Expectations (GX Core) |
<!-- END GENERATED: implementations -->
