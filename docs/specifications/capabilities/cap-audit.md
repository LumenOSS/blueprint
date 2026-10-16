# CAP-AUDIT Audit

<!-- BEGIN GENERATED: header (just render) -->
Every access and administrative action recorded, retained beyond the platform default, readable by auditors only.

Layer L1 · domain: governance · depends on: [CAP-IDENTITY](cap-identity.md).
<!-- END GENERATED: header -->

## Purpose

The platform keeps a lasting record of who accessed or changed what.

## Why

Platforms usually keep audit records for less time than the law requires, so the records are copied out to a store of their own. Be aware that the text of a query can itself contain personal data.

## Interfaces

- The platform's audit records, copied to a separate store that auditors can read.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-AUDIT.1 | MUST | Every data access and every administrative action is recorded with principal, object, action and time. | A test read and a test grant both appear in audit. |
| CAP-AUDIT.2 | MUST | Audit is copied to a separate store with retention set by policy, beyond the platform's own retention, and is readable only by auditors. | The copy holds records older than the platform's retention; a non-auditor read is refused. |
| CAP-AUDIT.3 | SHOULD | Query text is recorded only when a case needs it, because query text can contain personal data. | Verbose audit is off by default; turning it on is a reviewed change. |
| CAP-AUDIT.4 | MUST | Access to identifiable or special-category records (T3, T4) records a purpose chosen from a declared list, as well as principal, object, action and time.<br><br>*Example:* An officer opens a learner's support plan and chooses the purpose 'case review'; the audit row records the purpose with the officer, the record and the time. | Audit rows for T3 and T4 reads carry a purpose. |
| CAP-AUDIT.5 | SHOULD | Anomalous access to T3 and T4 data (unusual volume, time or scope outside the entitlement) raises an alert. | A simulated out-of-scope read raises an alert. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [ISO/IEC 27001 Information security management systems](../standards.md#identity-security-and-privacy) | ISO/IEC 27001:2022 with Amd 1:2024, and ISO/IEC 27002:2022 | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | system.access.audit<br/>Diagnostic settings to Log Analytics |
| [oss](../implementations/oss.yaml) | Audit sources<br/>Iceberg audit tables on object-locked storage |
<!-- END GENERATED: implementations -->
