# CAP-CATALOG Catalog and governance plane

<!-- BEGIN GENERATED: header (just render) -->
One catalog of record for tables, files and functions, enforcing grants, tags and policies.

Layer L1 · domain: data · depends on: [CAP-TABLES](cap-tables.md), [CAP-IDENTITY](cap-identity.md).
<!-- END GENERATED: header -->

## Purpose

The catalog is the one place that knows about every dataset, and it decides who may read which rows and columns.

## Why

A policy that one engine enforces and another ignores isn't really a policy. Granting access only to groups keeps it reviewable ([P5](../principles.md#p5-least-privilege-enumerated)), and having one catalog per domain keeps ownership clear and each dataset in one place ([P6](../principles.md#p6-branch-never-copy)).

## Interfaces

- Namespaces, with `<domain>_<env>` catalogs and `<product>_<layer>` schemas inside each domain.
- Grants, governed tags, row filters and column masks.
- Credentials vended to engines.

## Notes

Engines differ in what they enforce. Route protected tables only through the engines that enforce the policies, and deny access to the rest.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-CATALOG.1 | MUST | One catalog of record lists every table, volume of files and function, whichever engine created it. | An inventory of storage locations has no table unknown to the catalog. |
| CAP-CATALOG.2 | MUST | Catalogs are named domain by environment (`<domain>_<env>`); a product is a set of schemas inside its domain, and data shared across domains is promoted to its owning domain and read from there, never copied. | Catalog and schema names match the pattern; no table is a copy of another domain's. |
| CAP-CATALOG.3 | MUST | Grants go only to groups, and production objects are owned by groups. | A query of grants and owners finds no individual user. |
| CAP-CATALOG.4 | MUST | Governed tags (provenance, classification) can be set only by principals granted the right to assign them. | Negative test: an analyst cannot set a classification tag. |
| CAP-CATALOG.5 | MUST | Row filters and column masks are enforced on every read path that serves protected data; an engine that cannot enforce them is denied those tables. | Read a protected table through each engine as a scoped user; each returns only the scoped rows or is refused. |
| CAP-CATALOG.6 | MUST | Engines receive short-lived, scoped storage credentials from the catalog, never long-lived storage keys. | Engine configuration holds no storage key; credentials observed in use expire. |
| CAP-CATALOG.7 | SHOULD | Every authenticated user may browse metadata, so data can be found without being readable. | A user with no data grants can list catalog objects but not read them. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog |
| [oss](../implementations/oss.yaml) | Lakekeeper<br/>Trino + OPA |
<!-- END GENERATED: implementations -->
