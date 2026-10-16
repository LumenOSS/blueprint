# CAP-COLLECTION Periodic data collection

<!-- BEGIN GENERATED: header (just render) -->
Returns collected from institutions on a cycle, validated at entry, attested, gated on completeness and frozen at a reference date.

Layer L3 · domain: product · depends on: [CAP-MASTERDATA](cap-masterdata.md), [CAP-QUALITY](cap-quality.md), [CAP-REFERENCE](cap-reference.md).
<!-- END GENERATED: header -->

## Purpose

Collect periodic returns, such as an annual census, from every institution, and turn them into official figures that can be trusted and revised openly.

## Why

Most system-level indicators are stocks at a reference date. They are only comparable across institutions and years if every institution reports against the same date, the same instrument and the same rules, and if the figures are frozen before they are used ([P18](../principles.md#p18-append-only-records-expand-then-contract-change)).

## Interfaces

- Versioned instruments; returns with states and attestation.
- A completeness gate per area.
- Locked snapshots at the reference date.

## Notes

Connectivity varies widely between institutions; plan for capture that works offline and synchronises later. The [census product](../product/census.md) is the worked example.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-COLLECTION.1 | MUST | Each collection is a versioned instrument declaring its items, validation rules, reference date, collection window and expected respondents drawn from the registry; a committed version is immutable. | Instruments are versioned files; a change after commit creates a new version. |
| CAP-COLLECTION.2 | MUST | Validation runs at entry and again on submission; blocking errors prevent submission, warnings need a reason, and results go back to the respondent in machine-readable form with their severity. | A fixture with a blocking error cannot be submitted; one with a warning requires a reason. |
| CAP-COLLECTION.3 | MUST | A return moves through declared states (not started, in progress, submitted, attested by the head of the institution, queried, accepted, locked), and each transition is an event recording the role that made it. | The event log of a fixture return shows every transition with its role. |
| CAP-COLLECTION.4 | MUST | Figures for an area are released only when its expected respondents balance against accepted returns; otherwise the area reads BLOCKED. | An area with a missing return reads BLOCKED. |
| CAP-COLLECTION.5 | MUST | Official figures are computed from a locked snapshot as at the reference date and carry its version; a revision is a new version with a reason, and both remain readable. | A revised figure shows both versions and the reason. |
| CAP-COLLECTION.6 | MUST | Imputed values are flagged per cell and never mixed silently with reported ones. | Every imputed cell carries a flag in silver and gold. |
| CAP-COLLECTION.7 | SHOULD | Forms are prefilled from the registry and the previous period, so respondents confirm rather than retype. | A second-period fixture opens prefilled. |
| CAP-COLLECTION.8 | SHOULD | Capture works offline and synchronises later; a re-sent return converges on one record. | Submitting the same return twice yields one record. |
| CAP-COLLECTION.9 | SHOULD | Completeness and timeliness per submitting unit are themselves reported measures. | A gold model reports them per unit and period. |
| CAP-COLLECTION.10 | SHOULD | Each stage of a collection names the GSBPM v5.2 sub-process it performs, so the statistical production process can be described in a shared vocabulary. | Collection stages are tagged with GSBPM sub-process codes. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [Education Data Quality Assessment Framework (Ed-DQAF)](../standards.md#metadata-and-data-quality) | 2017 manual, instruments and matrix | reference |
| [UN Fundamental Principles of Official Statistics](../standards.md#official-statistics-and-disclosure-control) | Adopted 1994; endorsed by UN General Assembly resolution 68/261 (2014) | adopt |
| [UN National Quality Assurance Frameworks Manual for Official Statistics](../standards.md#official-statistics-and-disclosure-control) | 2019 (ST/ESA/STAT/SER.M/100) | reference |
| [Generic Statistical Business Process Model](../standards.md#official-statistics-and-disclosure-control) | GSBPM v5.2 (May 2025) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | ODK Central on Azure Container Apps<br/>The census product's return workflow on Lakebase |
| [oss](../implementations/oss.yaml) | ODK Central<br/>The census product's return workflow on PostgreSQL |
<!-- END GENERATED: implementations -->
