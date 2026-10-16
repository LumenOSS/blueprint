# CAP-ACCESS Access model

Role decides reach, entitlements decide rows, classification decides columns.

Layer L1 · domain: governance · depends on: [CAP-IDENTITY](cap-identity.md), [CAP-CATALOG](cap-catalog.md), [CAP-CLASSIFICATION](cap-classification.md).

## Purpose

Decide access from three independent inputs: role, scope and sensitivity.

## Why

No single change can widen access across all three ([P14](../principles.md#p14-access-is-role--scope--sensitivity)). Exemptions are named because each is a path to raw data ([P5](../principles.md#p5-least-privilege-enumerated)).

## Interfaces

- Groups for reach; an entitlement table for rows; classification tags for columns.
- One row-filter function per class of table; masks per classification.

## Notes

Anyone exempt from a policy, any holder of a manage right, and the catalog administrator effectively see raw data. Keep those lists short and reviewed.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-ACCESS.1 | MUST | Reach (which catalogs and actions) is granted to identity-provider groups by role. | Every grant's principal is a group mapped to a role. |
| CAP-ACCESS.2 | MUST | Row scope comes from an entitlement table derived from an authoritative feed (for example staff postings), with a validity period, never edited by hand. | The entitlement table is written only by its loader; a manual write is refused. |
| CAP-ACCESS.3 | MUST | Row and column policies only narrow access. Each user and table resolves to exactly one row filter and each column to at most one mask; an ambiguity fails the query rather than choosing. | Test a user matching two filters; the query fails. |
| CAP-ACCESS.4 | MUST | Only pipeline identities are exempt from policies, each exemption listed with its reason. | The exemption list contains only workload identities, each with a reason. |
| CAP-ACCESS.5 | MUST | Access to identifiable columns is through a time-boxed, audited group. | Membership of the group expires; each grant appears in audit. |
| CAP-ACCESS.6 | MUST | Reach, row scope and classification are each changed by a different owner, so no single change widens access across all three. | The owners of the group declarations, the entitlement feed and the classification rules are different roles. |
| CAP-ACCESS.7 | MUST | Row scope may also come from a relationship (the record is the person's own, or the person is a guardian with verified authority), taken from the authoritative relationship record, effective-dated, and ended when the relationship or the authority ends. | Ending a guardian relationship removes access at the next query. |
| CAP-ACCESS.8 | MUST | A view for a data subject or guardian exposes a declared, minimal set of columns per record class; designated special-category fields are excluded from guardian views by default, with the reason recorded. | Subject-facing views are declared in code with their column lists and exclusions. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog ABAC policies<br/>Entitlement table in a reference catalog |
| [oss](../implementations/oss.yaml) | Entitlement table in Iceberg<br/>OPA policies for Trino |
<!-- END GENERATED: implementations -->
