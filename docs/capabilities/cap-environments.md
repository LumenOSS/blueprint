# CAP-ENVIRONMENTS Environments by branching

An environment is a template plus values; development is isolated inside production by branching.

Layer L1 · domain: movement · depends on: [CAP-OPERATIONALDB](cap-operationaldb.md), [CAP-CATALOG](cap-catalog.md).

## Purpose

Isolate development and testing from production, with or without a second funded environment.

## Why

Isolation means no development write reaches production data and no consumer reads development output; branches and ungranted schemas give that inside one environment ([P7](../principles.md#p7-isolation-without-a-second-environment)).

## Interfaces

- A template and one values file per environment.
- Per-change database branches and development schemas with a time to live.

## Notes

A database branch does not branch object storage. A branch that writes files would write them into production storage, so branches get their own storage and read production storage read-only.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-ENVIRONMENTS.1 | MUST | An environment is one template plus one values file, and every axis agrees which environment it is: catalog and schema, database branch and database, application identity and configuration, and jobs. | Each application's health endpoint (CAP-APPS.2) matches its values file. |
| CAP-ENVIRONMENTS.2 | MUST | Without a funded development environment, development is isolated inside production: database branches, and development schemas in production catalogs with no consumer grants. | Development objects exist only as branches and ungranted schemas. |
| CAP-ENVIRONMENTS.3 | MUST | A branch never writes to production object storage. Branches use their own storage, and may read production storage only through a read-only path. | A write to production storage from a branch's identity is refused. |
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
