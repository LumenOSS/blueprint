# CAP-COLLECTION Periodic data collection

<!-- BEGIN GENERATED: header (just render) -->
Returns collected from institutions on a cycle, validated at entry, attested, gated on completeness and frozen at a reference date.

Layer L3 · domain: product · depends on: [CAP-MASTERDATA](cap-masterdata.md), [CAP-QUALITY](cap-quality.md), [CAP-REFERENCE](cap-reference.md).
<!-- END GENERATED: header -->

## Purpose

The platform collects periodic returns from every institution, such as an annual census, and turns them into official figures that people can trust and that are revised in the open.

## Why

Most system-level indicators count something as it stood on a reference date. You can only compare them across institutions and years if every institution reports for the same date, on the same instrument and under the same rules, and if the figures are frozen before anyone uses them ([P18](../principles.md#p18-append-only-records-expand-then-contract-change)).

## Interfaces

- Versioned instruments, and returns that move through states and are attested.
- A completeness gate for each area.
- Snapshots locked at the reference date.

## Notes

Connectivity varies a great deal between institutions, so plan for data capture that works offline and synchronises later. The [census product](../../guides/products/census.md) is the worked example.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-COLLECTION.1 | MUST | Each collection is a versioned instrument declaring its items, validation rules, reference date, collection window and expected respondents drawn from the registry; a committed version is immutable.<br><br>*Example:* The 2026 census fixes the reference date at 1 October, opens for the month of October, and expects a return from every institution active in the registry on 1 October. | Instruments are versioned files; a change after commit creates a new version. |
| CAP-COLLECTION.2 | MUST | Validation runs at entry and again on submission; blocking errors prevent submission, warnings need a reason, and results go back to the respondent in machine-readable form with their severity.<br><br>*Example:* An enrolment more than half as large again as the institution's recorded capacity is a warning that needs a reason; a negative count blocks submission. | A fixture with a blocking error cannot be submitted; one with a warning requires a reason. |
| CAP-COLLECTION.3 | MUST | A return moves through declared states (not started, in progress, submitted, attested by the head of the institution, queried, accepted, locked), and each transition is an event recording the role that made it. | The event log of a fixture return shows every transition with its role. |
| CAP-COLLECTION.4 | MUST | Figures for an area are released only when its expected respondents balance against accepted returns; otherwise the area reads BLOCKED.<br><br>*Example:* District A has 98 of its 100 returns accepted, so it reads BLOCKED and its figures wait; District B is complete and releases. | An area with a missing return reads BLOCKED. |
| CAP-COLLECTION.5 | MUST | Official figures are computed from a locked snapshot as at the reference date and carry its version; a revision is a new version with a reason, and both remain readable. | A revised figure shows both versions and the reason. |
| CAP-COLLECTION.6 | MUST | Imputed values are flagged per cell and never mixed silently with reported ones.<br><br>*Example:* For an institution that did not respond, last year's enrolment is carried forward, and every carried-forward cell is flagged as imputed in the published table. | Every imputed cell carries a flag in silver and gold. |
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
