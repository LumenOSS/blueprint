# CAP-OPERATIONALDB Operational database with branching

<!-- BEGIN GENERATED: header (just render) -->
Each product's transactional Postgres store, with copy-on-write branches of production.

Layer L1 · domain: data · depends on: [CAP-IDENTITY](cap-identity.md).
<!-- END GENERATED: header -->

## Purpose

Give each product a transactional Postgres store that can be branched for development and testing.

## Why

Branching gives every change a full copy of production at no copy cost ([P6](../principles.md#p6-branch-never-copy), [P7](../principles.md#p7-isolation-without-a-second-environment)). Two gatekeepers, catalog policies and database policies, must agree, so each is paired with the other.

## Interfaces

- Postgres wire protocol and SQL.
- Branches with a time to live; a protected production branch.
- Per-identity roles and row-level security.
- A migration ledger and an application-side schema gate.

## Notes

A database role that row-level security does not admit reads zero rows, silently. When the catalog reads an operational database, test that its identity is admitted before relying on it.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-OPERATIONALDB.1 | MUST | The operational database speaks the Postgres protocol and SQL dialect. | The product's migrations and tests run unchanged against it. |
| CAP-OPERATIONALDB.2 | MUST | A branch of production, or of a point in time, is created without copying data first, and carries a time to live. | Create a branch of the production database and time it; it expires on schedule. |
| CAP-OPERATIONALDB.3 | MUST | The production branch is protected from deletion and from writes by development identities. | Negative tests: delete and write as a development identity both fail. |
| CAP-OPERATIONALDB.4 | MUST | Connections authenticate per identity; an application's access is governed by database roles and row-level security, and each catalog policy names its database counterpart or states there is none. | No shared password role is in use; the policy register pairs each catalog policy with its database policy. |
| CAP-OPERATIONALDB.5 | MUST | Migrations are idempotent twice over: a ledger records what ran, and every statement can be run again safely. Schemas change by expand then contract, one phase per migration, and the application refuses to write to a database behind its code. | CI applies every migration twice to a branch; the application's schema gate is tested against an older database. |
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
