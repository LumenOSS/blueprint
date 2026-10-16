# CAP-SHARING Publication and sharing

<!-- BEGIN GENERATED: header (just render) -->
External parties receive de-identified tables from a publication catalog over an open protocol, each share approved and registered.

Layer L1 · domain: governance · depends on: [CAP-CATALOG](cap-catalog.md), [CAP-CLASSIFICATION](cap-classification.md), [CAP-TRANSFORMATION](cap-transformation.md).
<!-- END GENERATED: header -->

## Purpose

Data leaves the platform only as de-identified or aggregated tables, each approved and registered. This page covers sharing row-level data with partners. Open aggregate statistics are covered by [CAP-PUBLICATION](cap-publication.md), and a person's own records by [CAP-RECORDS.7](cap-records.md).

## Why

Sharing protocols don't carry the provider's policies over to the recipient, so the protection has to be in the data itself ([P15](../principles.md#p15-publish-never-export)).

## Interfaces

- A publication catalog, built by the transformation layer.
- An open sharing protocol, a register of recipients, and a sharing panel.

## Notes

An identifier hashed without a salt can be reversed by trying every plausible identifier. Use a keyed hash or a surrogate key instead.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-SHARING.1 | MUST | Data leaves the platform only from a publication catalog of de-identified or aggregated materialised tables. | Every share's objects are in the publication catalog. |
| CAP-SHARING.2 | MUST | Published tables enforce a minimum cell size by test, and replace identifiers with keyed hashes or surrogate keys, never unsalted hashes.<br><br>*Example:* A published identifier is a keyed hash, so someone holding a list of learner numbers cannot hash the list and match it; an unsalted hash would allow exactly that. | Publication models carry cell-size tests; no identifier column is an unkeyed hash. |
| CAP-SHARING.3 | MUST | Sharing uses an open protocol, with recipients authenticated by federation where possible and otherwise by tokens rotated within a year. | The recipient register lists each recipient's method and token expiry. |
| CAP-SHARING.4 | MUST | Each share is a reviewed change sponsored by a steward, approved by a sharing panel, and listed in a published register. | Every live share traces to an approved change and a register entry. |
| CAP-SHARING.5 | MUST | Shares name explicit tables, never whole schemas, and share no table history. | No share includes a schema; shared tables have history sharing off. |
| CAP-SHARING.6 | SHOULD | Researchers who need finer data work inside the platform, on a project basis, time-boxed. | Research grants carry a project and an expiry. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [Data Governance for EdTech (landscape review and policy recommendations)](../standards.md#identity-security-and-privacy) | 2025 | adopt |
| [Guidelines on Children's Data Protection in an Education Setting](../standards.md#identity-security-and-privacy) | Adopted by the Committee of Convention 108, November 2020 | reference |
| [ODRL Information Model](../standards.md#open-data-and-exchange) | ODRL 2.2, W3C Recommendation (2018) | reference |
| [NIST SP 800-188 De-Identifying Government Datasets](../standards.md#identity-security-and-privacy) | Final, September 2023 | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Delta Sharing<br/>Publication catalog |
| [oss](../implementations/oss.yaml) | Delta Sharing reference server |
<!-- END GENERATED: implementations -->
