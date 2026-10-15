# CAP-AUDIT Audit

Every access and administrative action recorded, retained beyond the platform default, readable by auditors only.

Layer L1 · domain: governance · depends on: [CAP-IDENTITY](cap-identity.md).

## Purpose

Keep a durable record of who accessed or changed what.

## Why

Platform audit retention is usually shorter than legal retention, so audit is copied out. Query text can itself contain personal data.

## Interfaces

- Platform audit records, copied to a separate store readable by auditors.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-AUDIT.1 | MUST | Every data access and every administrative action is recorded with principal, object, action and time. | A test read and a test grant both appear in audit. |
| CAP-AUDIT.2 | MUST | Audit is copied to a separate store with retention set by policy, beyond the platform's own retention, and is readable only by auditors. | The copy holds records older than the platform's retention; a non-auditor read is refused. |
| CAP-AUDIT.3 | SHOULD | Query text is recorded only when a case needs it, because query text can contain personal data. | Verbose audit is off by default; turning it on is a reviewed change. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | system.access.audit<br/>Diagnostic settings to Log Analytics |
| [oss](../implementations/oss.yaml) | Audit sources<br/>Iceberg audit tables on object-locked storage |
<!-- END GENERATED: implementations -->
