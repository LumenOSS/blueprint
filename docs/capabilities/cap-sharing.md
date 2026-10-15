# CAP-SHARING Publication and sharing

External parties receive de-identified tables from a publication catalog over an open protocol, each share approved and registered.

Layer L1 · domain: governance · depends on: [CAP-CATALOG](cap-catalog.md), [CAP-CLASSIFICATION](cap-classification.md), [CAP-TRANSFORMATION](cap-transformation.md).

## Purpose

Let data leave the platform only as de-identified or aggregated tables, approved and registered.

## Why

Sharing protocols do not carry the provider's policies to the recipient, so protection must be in the data ([P15](../principles.md#p15-publish-never-export)).

## Interfaces

- A publication catalog built by the transformation layer.
- An open sharing protocol; a recipient register; a sharing panel.

## Notes

An unsalted hash of an identifier can be reversed by trying every plausible identifier. Use a keyed hash or a surrogate key.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-SHARING.1 | MUST | Data leaves the platform only from a publication catalog of de-identified or aggregated materialised tables. | Every share's objects are in the publication catalog. |
| CAP-SHARING.2 | MUST | Published tables enforce a minimum cell size by test, and replace identifiers with keyed hashes or surrogate keys, never unsalted hashes. | Publication models carry cell-size tests; no identifier column is an unkeyed hash. |
| CAP-SHARING.3 | MUST | Sharing uses an open protocol, with recipients authenticated by federation where possible and otherwise by tokens rotated within a year. | The recipient register lists each recipient's method and token expiry. |
| CAP-SHARING.4 | MUST | Each share is a reviewed change sponsored by a steward, approved by a sharing panel, and listed in a published register. | Every live share traces to an approved change and a register entry. |
| CAP-SHARING.5 | MUST | Shares name explicit tables, never whole schemas, and share no table history. | No share includes a schema; shared tables have history sharing off. |
| CAP-SHARING.6 | SHOULD | Researchers who need finer data work inside the platform, on a project basis, time-boxed. | Research grants carry a project and an expiry. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Delta Sharing<br/>Publication catalog |
| [oss](../implementations/oss.yaml) | Delta Sharing reference server |
<!-- END GENERATED: implementations -->
