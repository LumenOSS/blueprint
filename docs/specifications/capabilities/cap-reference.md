# CAP-REFERENCE Reference data and data dictionary

<!-- BEGIN GENERATED: header (just render) -->
Governed code lists, a versioned data dictionary and common formats, so every value means the same thing everywhere.

Layer L1 · domain: governance · depends on: [CAP-CATALOG](cap-catalog.md).
<!-- END GENERATED: header -->

## Purpose

Make every coded value, definition and format mean the same thing across systems, years and reports.

## Why

Comparisons over time and between places only hold when codes are stable and definitions are versioned. A reused code or a silently redefined element turns a trend into an artefact. Crosswalks to international classifications let national figures be reported internationally without changing how institutions record them.

## Interfaces

- Versioned code lists with owners and validity periods.
- A data dictionary in the catalog for every published element.
- Crosswalks from local classifications to international ones.
- A versioned administrative geography.

## Notes

Ordinal scales are codes with documented bounds, never free text.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-REFERENCE.1 | MUST | Every coded attribute references a governed code list with an owner, a version and a validity period; a code is retired, never reused or redefined.<br><br>*Example:* Version 3 of the exit-reason list has TRF for 'transferred to another institution'. Version 4 keeps TRF as it was and adds TRA for 'transferred abroad', rather than widening TRF, which would silently change what every past TRF row means. | A check finds no coded column without a code list and no code redefined across versions. |
| CAP-REFERENCE.2 | MUST | Changes to code lists and element definitions are reviewed changes approved by the owning steward; each is versioned and announced to the people who use it before it takes effect.<br><br>*Example:* Adding an exit reason 'home education' is a reviewed change approved by the learners steward, published as a new version of the list, and announced before institutions can use it. | Each code-list or definition change traces to an approved change and a notice. |
| CAP-REFERENCE.3 | MUST | Every published element is registered in the catalog's data dictionary following the ISO/IEC 11179 model: the concept it represents and its definition, its value domain (data type, format and code list), and its registration status, version and steward.<br><br>*Example:* The element 'date of birth' is registered once, with its definition, type, format, validation rule and steward; every table that carries it points to that entry. | A fitness function finds no gold column with missing dictionary fields. |
| CAP-REFERENCE.4 | MUST | Local classifications carry versioned crosswalks to the international classifications used for reporting (ISCED 2011 for levels of education, ISCED-F 2013 for fields, ISCED-T 2021 for teacher-training programmes), and each crosswalk is tested to map every local code.<br><br>*Example:* A local 'grade 9' maps to ISCED 2011 level 2 (lower secondary) in the 2026 crosswalk; a test fails if any local grade has no mapping. | Each crosswalk's test maps every local code. |
| CAP-REFERENCE.5 | MUST | Administrative geography is versioned: a boundary change creates a new version and keeps the old, so a time series can be restated on either.<br><br>*Example:* Two districts merge in 2027. Boundary version 2027 has one district and version 2026 keeps both, so a 2025 enrolment trend can be shown on either. | Two boundary versions coexist and each resolves its own codes. |
| CAP-REFERENCE.6 | MUST | Value formats are fixed in the data dictionary and enforced at entry and at load: timestamps follow RFC 3339 with an explicit offset (with RFC 9557 time-zone names where local civil time matters); amounts are fixed-point decimals with an ISO 4217 currency code; telephone numbers follow ITU-T E.164; countries use ISO 3166-1; languages use BCP 47 tags; text is UTF-8 in Unicode Normalization Form C; coordinates declare their reference system.<br><br>*Example:* A fee is stored as 1500.00 with its ISO 4217 currency code, a telephone number as +15551234567, and an attendance mark as 2026-10-16T08:05:00+01:00[Europe/Lisbon]. | Each format in the dictionary has a validation rule used at entry and at load. |
| CAP-REFERENCE.7 | SHOULD | A value outside its code list is quarantined with a reason rather than coerced to a catch-all code.<br><br>*Example:* A return gives an institution type that is not on the list; the row goes to quarantine with 'unknown code' instead of being stored as 'other'. | An unknown-code fixture lands in quarantine. |
| CAP-REFERENCE.8 | SHOULD | Code lists maintained by outside agencies (countries, currencies, languages) are loaded on a schedule, versioned, and recorded with their source and retrieval date. | Each external code list has a load job and a recorded source and retrieval date. |
| CAP-REFERENCE.9 | MUST | Every code in a code list has a label in each official language the authority declares, tagged with a BCP 47 language tag; where a label is missing, interfaces show the label in a declared default language, never the bare code.<br><br>*Example:* The exit reason TRF has labels 'Transferred to another institution' (en), 'Transféré dans un autre établissement' (fr) and 'منقول إلى مؤسسة أخرى' (ar). A new code added without its Arabic label is reported before the list's new version is published. | A check lists every code that lacks a label in a declared language, and runs before a code-list version is published. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [RFC 3339 Date and Time on the Internet](../standards.md#data-representation) | RFC 3339 (2002), as updated by RFC 9557 (2024) | adopt |
| [RFC 9557 Internet Extended Date/Time Format](../standards.md#data-representation) | RFC 9557 (April 2024) | adopt |
| [ISO 8601-1 Date and time](../standards.md#data-representation) | ISO 8601-1:2019 with Amd 1:2022 | reference |
| [ITU-T E.164 international numbering plan](../standards.md#data-representation) | E.164 (02/26), approved 2026-02-13 | adopt |
| [ISO 3166-1 Country codes](../standards.md#data-representation) | ISO 3166-1:2020; code list as maintained by the ISO 3166 Maintenance Agency | adopt |
| [ISO 4217 Currency codes](../standards.md#data-representation) | ISO 4217:2015; code tables as maintained by the maintenance agency | adopt |
| [BCP 47 Language tags](../standards.md#data-representation) | RFC 5646 and RFC 4647, with the IANA Language Subtag Registry | adopt |
| [ISO 639 Language codes](../standards.md#data-representation) | ISO 639:2023, which replaced the former parts 1 to 5 | reference |
| [Unicode Standard and normalization (UAX 15)](../standards.md#data-representation) | Unicode 18.0.0 (2026) | adopt |
| [International Standard Classification of Education (ISCED 2011)](../standards.md#education-classifications-and-indicators) | ISCED 2011 (published 2012) with Operational Manual (2015); amendment due 2027 | adopt |
| [ISCED Fields of Education and Training (ISCED-F 2013)](../standards.md#education-classifications-and-indicators) | ISCED-F 2013 (published 2014); comprehensive revision due 2027 | adopt |
| [International Standard Classification of Teacher Training Programmes (ISCED-T 2021)](../standards.md#education-classifications-and-indicators) | ISCED-T 2021 (published 2022) | adopt |
| [ISCED revision (amendment of ISCED 2011, revision of ISCED-F 2013)](../standards.md#education-classifications-and-indicators) | In progress; task forces 2026; target 44th UNESCO General Conference (2027) | track |
| [Common Education Data Standards (CEDS)](../standards.md#open-data-and-exchange) | Version 14 (official release on the CEDS GitHub, March–April 2026); the ceds.ed.gov downloads still offer Version 13 | reference |
| [1EdTech Competencies and Academic Standards Exchange (CASE)](../standards.md#open-data-and-exchange) | 1.1 (January 2025) | adopt |
| [ISO/IEC 11179 Metadata registries](../standards.md#metadata-and-data-quality) | ISO/IEC 11179-1:2023 and 11179-3:2023 | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog comments, tags and a reference catalog<br/>Versioned code-list tables (dbt seeds) |
| [oss](../implementations/oss.yaml) | OpenMetadata<br/>Versioned code-list tables (dbt seeds) |
<!-- END GENERATED: implementations -->
