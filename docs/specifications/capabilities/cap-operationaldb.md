# CAP-OPERATIONALDB Operational database with branching

<!-- BEGIN GENERATED: header (just render) -->
Each product's transactional Postgres store, with copy-on-write branches of production.

Layer L1 · domain: data · depends on: [CAP-IDENTITY](cap-identity.md).
<!-- END GENERATED: header -->

## Purpose

Each product gets a transactional Postgres database that can be branched for development and testing.

## Why

Branching gives every change a full copy of production without the cost of copying it ([P6](../principles.md#p6-branch-never-copy), [P7](../principles.md#p7-isolation-without-a-second-environment)). There are two gatekeepers, the catalog's policies and the database's policies, and they have to agree, so each is set up together with the other.

## Interfaces

- The Postgres wire protocol and SQL.
- Branches that expire after a set time, and a protected production branch.
- A role for each identity, and row-level security.
- A migration ledger, and a schema check inside the application.

## Notes

If row-level security doesn't admit a database role, that role reads zero rows, without any error. When the catalog reads an operational database, test that its identity is admitted before you rely on it.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-OPERATIONALDB.1 | MUST | The operational database speaks the Postgres protocol and SQL dialect. | The product's migrations and tests run unchanged against it. |
| CAP-OPERATIONALDB.2 | MUST | A branch of production, or of a point in time, is created without copying data first, and carries a time to live.<br><br>*Example:* A developer branches production as it was at 09:00 to test a migration; the branch costs nothing until it diverges and is deleted automatically after seven days. | Create a branch of the production database and time it; it expires on schedule. |
| CAP-OPERATIONALDB.3 | MUST | The production branch is protected from deletion and from writes by development identities. | Negative tests: delete and write as a development identity both fail. |
| CAP-OPERATIONALDB.4 | MUST | Connections authenticate per identity; an application's access is governed by database roles and row-level security, and each catalog policy names its database counterpart or states there is none. | No shared password role is in use; the policy register pairs each catalog policy with its database policy. |
| CAP-OPERATIONALDB.5 | MUST | Migrations are idempotent twice over: a ledger records what ran, and every statement can be run again safely. Schemas change by expand then contract, one phase per migration, and the application refuses to write to a database behind its code.<br><br>*Example:* A migration that adds a column is run twice on a branch in CI; the second run changes nothing, and the application refuses to write to a database still on the previous schema. | CI applies every migration twice to a branch; the application's schema gate is tested against an older database. |
| CAP-OPERATIONALDB.6 | MUST | Committed records survive loss of a node (recovery point zero), and the database can be restored to a point in time. | Restore drill to a point in time, comparing per-table content hashes. |
| CAP-OPERATIONALDB.7 | SHOULD | Analytics read operational data through the catalog or a governed extract, never through a direct connection. | No analytics identity holds a database login. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Lakebase Postgres |
| [oss](../implementations/oss.yaml) | CloudNativePG<br/>CSI volume snapshots on Ceph RBD<br/>pgroll |
<!-- END GENERATED: implementations -->
