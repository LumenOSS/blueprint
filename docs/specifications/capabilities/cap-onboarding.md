# CAP-ONBOARDING Tenant onboarding registry

<!-- BEGIN GENERATED: header (just render) -->
One reviewed declaration per product or source generates its identities, grants, schemas and reviewers.

Layer L1 · domain: delivery · depends on: [CAP-DELIVERY](cap-delivery.md), [CAP-CATALOG](cap-catalog.md), [CAP-CIIDENTITY](cap-ciidentity.md).
<!-- END GENERATED: header -->

## Purpose

Turn adding a product or a data source into one reviewed file, from which everything it needs is generated.

## Why

Hand-made identities and grants drift and are never removed. One declaration per tenant gives one place to review access and one place to revoke it ([P5](../principles.md#p5-least-privilege-enumerated)).

## Interfaces

- `tenants/<name>.yaml` in the platform repository: owner role, domain, ingestion method, highest classification, catalogs written and read, operational database, trusted repository.
- Generated: identities, federated credentials, grants, schemas, required reviewers.
- Published outputs per product and environment, consumed by the product's pipeline.

## Notes

The boundary between platform and product: the platform owns anything that crosses a permission boundary; the product owns what is inside its grant.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-ONBOARDING.1 | MUST | Each product or source has one tenant entry declaring its owner role, domain, ingestion method, highest classification, the catalogs it writes and reads, its operational database, and the repository the platform trusts for it. | Every product's resources trace back to exactly one tenant entry. |
| CAP-ONBOARDING.2 | MUST | Identities, grants, schemas and required reviewers are generated from the entry and never created by hand. | A reconciliation diff between generated and live grants is empty. |
| CAP-ONBOARDING.3 | MUST | The platform publishes each product's outputs per environment (endpoints, catalog names, identities, compute IDs) to the product, and a product never reads platform state. | The product's configuration takes these values from published outputs; it has no access to platform state. |
| CAP-ONBOARDING.4 | MUST | Removing a tenant entry removes the access it generated. | Off-boarding test: remove an entry; its identities and grants are gone after apply. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Tenant YAML + OpenTofu (azurerm, databricks providers) |
| [oss](../implementations/oss.yaml) | Tenant YAML + OpenTofu |
<!-- END GENERATED: implementations -->
