# CAP-ENVIRONMENTS Environments by branching

<!-- BEGIN GENERATED: header (just render) -->
An environment is a template plus values; development is isolated inside production by branching.

Layer L1 · domain: movement · depends on: [CAP-OPERATIONALDB](cap-operationaldb.md), [CAP-CATALOG](cap-catalog.md).
<!-- END GENERATED: header -->

## Purpose

Development and testing are isolated from production, whether or not you can fund a second environment.

## Why

Isolation means that no development write reaches production data, and no consumer reads development output. Database branches and schemas without grants give you that inside a single environment ([P7](../principles.md#p7-isolation-without-a-second-environment)).

## Interfaces

- A template, and one values file for each environment.
- A database branch for each change, and development schemas that expire after a set time.

## Notes

A database branch doesn't branch object storage. A branch that wrote files would write them into production storage, so each branch gets its own storage and reads production storage read-only.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-ENVIRONMENTS.1 | MUST | An environment is one template plus one values file, and every axis agrees which environment it is: catalog and schema, database branch and database, application identity and configuration, and jobs. | Each application's health endpoint (CAP-APPS.2) matches its values file. |
| CAP-ENVIRONMENTS.2 | MUST | Without a funded development environment, development is isolated inside production: database branches, and development schemas in production catalogs with no consumer grants. | Development objects exist only as branches and ungranted schemas. |
| CAP-ENVIRONMENTS.3 | MUST | A branch never writes to production object storage. Branches use their own storage, and may read production storage only through a read-only path.<br><br>*Example:* A developer's branch can read production's scanned documents to test a change, but an upload attempted from the branch is refused. | A write to production storage from a branch's identity is refused. |
| CAP-ENVIRONMENTS.4 | MUST | Each change under review gets its own branch and development schemas with a time to live, removed when the change merges. | After merge, the change's branch and schemas are gone. |
| CAP-ENVIRONMENTS.5 | MUST | Grants and identities are declared per environment; the same configuration never implies the same securable. | Each environment's grants are listed separately in its plan. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | OpenTofu values files<br/>Lakebase branches<br/>Development schemas in production catalogs |
| [oss](../implementations/oss.yaml) | OpenTofu values files<br/>CloudNativePG branch clusters<br/>Iceberg branches or dev namespaces |
<!-- END GENERATED: implementations -->
