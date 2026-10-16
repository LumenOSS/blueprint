# CAP-PUBLICATION Open statistical publication

<!-- BEGIN GENERATED: header (just render) -->
Aggregate statistics published openly with disclosure control, permanent identifiers and open metadata.

Layer L1 · domain: governance · depends on: [CAP-SEMANTICS](cap-semantics.md), [CAP-CLASSIFICATION](cap-classification.md), [CAP-REFERENCE](cap-reference.md).
<!-- END GENERATED: header -->

## Purpose

Publish aggregate education statistics openly, safely and permanently.

## Why

Open statistics are how the public, researchers and partners hold an education system to account, and they are only trusted if they are the same figures used inside government, stable over time, and safe from re-identification ([P15](../principles.md#p15-publish-never-export)). Partner sharing of row-level, de-identified data is a different channel with different controls ([CAP-SHARING](cap-sharing.md)).

## Interfaces

- A publication register and portal.
- Publication tables with disclosure tests.
- Bulk files, a query interface and readable renderings generated from the same tables.

## Notes

Suppressing a small cell is not enough on its own: if row and column totals are published, the suppressed value can be recomputed. Secondary suppression or rounding closes that gap.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-PUBLICATION.1 | MUST | Only T0 aggregates are published openly; open datasets may be read without signing in, are rate-limited, and each is listed in a publication register. | Every open dataset is T0 and has a register entry. |
| CAP-PUBLICATION.2 | MUST | Published tables apply disclosure control using methods from the Handbook on Statistical Disclosure Control: a minimum cell size, secondary suppression so suppressed cells cannot be derived, and rounding or perturbation where declared, with small populations treated as high risk. The method is published as metadata.<br><br>*Example:* A table shows 3 learners with a given disability in one school. That cell is suppressed, and so is one more cell in the same row and the same column, so the 3 cannot be recovered by subtracting from the totals. | Publication models carry disclosure tests, including a test that suppressed cells cannot be recomputed from totals. |
| CAP-PUBLICATION.3 | MUST | Each published dataset has a permanent identifier and stable address; new periods are appended, and a revision is a new version with the previous one still retrievable.<br><br>*Example:* The 2025 enrolment table keeps its identifier after a correction; version 2 becomes current, and version 1 can still be downloaded. | An earlier version of a revised dataset can still be fetched by its identifier. |
| CAP-PUBLICATION.4 | MUST | Published datasets carry DCAT 3 metadata, with schema.org Dataset markup on each landing page and CSV on the Web metadata beside every CSV file, all generated from the data dictionary; they use the governed code lists and attach the metadata of every indicator they contain. | A metadata validator passes on every published dataset. |
| CAP-PUBLICATION.5 | SHOULD | Bulk files, a query interface and human-readable renderings are all generated from the same publication table. | Each output names the publication table it was rendered from. |
| CAP-PUBLICATION.6 | MUST | Geospatial outputs are published as GeoJSON (RFC 7946) or through OGC API – Features with a declared coordinate reference system; locations of institutions may be published, locations of people never are. | No published dataset contains a person's location. |
| CAP-PUBLICATION.7 | SHOULD | Statistics exchanged with international bodies use SDMX 3.0 or later, or SDMX 2.1 where the receiving agency requires it. | International returns are produced in the declared exchange format. |
| CAP-PUBLICATION.8 | SHOULD | Differential privacy is used only where it fits (query services over the same base data, or synthetic files) and is evaluated and documented following NIST SP 800-226, stating the unit of privacy and the total privacy-loss budget. | Each differentially private release records its unit, budget and evaluation. |
| CAP-PUBLICATION.9 | SHOULD | The international education questionnaires (the UIS Survey of Formal Education) are completed from gold through the semantic layer, not assembled by hand. | Each questionnaire table traces to semantic-layer measures. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [RFC 7946 GeoJSON](../standards.md#open-data-and-exchange) | RFC 7946 (August 2016) | adopt |
| [OGC API – Features](../standards.md#open-data-and-exchange) | Parts 1 to 3 (Core 1.0.1, CRS by Reference 1.0.1, Filtering 1.0.0) | reference |
| [Global indicator framework for the Sustainable Development Goals](../standards.md#education-classifications-and-indicators) | After 2026 refinement (UN Statistical Commission 57th session, March 2026; includes the 2025 Comprehensive Review) | adopt |
| [Official List of SDG 4 Indicators (global and thematic)](../standards.md#education-classifications-and-indicators) | October 2026 (post EDSC-12) | adopt |
| [UIS Survey of Formal Education (and UIS-OECD-Eurostat UOE collection)](../standards.md#education-classifications-and-indicators) | Annual cycle; documented in the February 2026 Data Refresh background document | adopt |
| [UN Fundamental Principles of Official Statistics](../standards.md#official-statistics-and-disclosure-control) | Adopted 1994; endorsed by UN General Assembly resolution 68/261 (2014) | adopt |
| [Handbook on Statistical Disclosure Control](../standards.md#official-statistics-and-disclosure-control) | Second edition (2025; online edition 2026) | adopt |
| [NIST SP 800-226 Guidelines for Evaluating Differential Privacy Guarantees](../standards.md#official-statistics-and-disclosure-control) | Final, March 2025 | reference |
| [Data Catalog Vocabulary (DCAT)](../standards.md#open-data-and-exchange) | DCAT Version 3, W3C Recommendation (August 2024) | adopt |
| [DCAT Application Profile (DCAT-AP)](../standards.md#open-data-and-exchange) | DCAT-AP 3.0.1 (October 2025) | reference |
| [schema.org Dataset](../standards.md#open-data-and-exchange) | schema.org 30.1 (September 2026) | adopt |
| [CSV on the Web (CSVW)](../standards.md#open-data-and-exchange) | W3C Recommendations (December 2015) | adopt |
| [SDMX](../standards.md#open-data-and-exchange) | SDMX 3.0 or later (3.1, May 2025); 2.1 where the receiving agency requires it | adopt |
| [International Open Data Charter principles](../standards.md#open-data-and-exchange) | Six principles (2015) | reference |
| [FAIR Guiding Principles](../standards.md#open-data-and-exchange) | Wilkinson et al., Scientific Data 3, 160018 (2016) | reference |
| [EN 301 549 Accessibility requirements for ICT products and services](../standards.md#accessibility-and-localisation) | V4.1.1 (September 2026), aligned with WCAG 2.2; V3.2.1 where a procurement rule cites it | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | CKAN on Azure Container Apps<br/>Publication catalog |
| [oss](../implementations/oss.yaml) | CKAN<br/>Parquet and CSV renderings from publication tables |
<!-- END GENERATED: implementations -->
