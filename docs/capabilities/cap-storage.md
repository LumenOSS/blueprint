# CAP-STORAGE Object storage

<!-- BEGIN GENERATED: header (just render) -->
Durable object storage for tables and files, isolated per domain catalog.

Layer L1 · domain: data
<!-- END GENERATED: header -->

## Purpose

Store tables and files durably, with each domain's data behind its own location and credential.

## Why

Separate locations per domain keep a grant on one domain from reaching another's files. Source files are the evidence behind every derived number, so they are kept as records ([P12](../principles.md#p12-provenance-before-any-drop)).

## Interfaces

- An object API reached by identity.
- One location and credential per domain catalog.
- An archive area for source-of-record files.

## Notes

Object versioning on a lake store can conflict with table maintenance: deleted data files reappear as versions and maintenance cannot reclaim them. Use the table format's history and backups for recovery, and test the combination.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-STORAGE.1 | MUST | Storage exposes an object API reached by identity, with encryption at rest. | Anonymous and shared-key access are refused. |
| CAP-STORAGE.2 | MUST | Each domain catalog has its own storage location and credential, so a grant on one domain never reaches another's files. | A credential for one domain cannot list another domain's location. |
| CAP-STORAGE.3 | MUST | Protection against accidental deletion is configured in a way the table format supports; it never breaks table maintenance. | Maintenance (expiry, vacuum) runs clean, and a deleted table is restored in a drill. |
| CAP-STORAGE.4 | MUST | Source-of-record files are kept in governed storage, tagged as real, with retention set by the data owner. | The archive location carries provenance and retention metadata. |
| CAP-STORAGE.5 | MUST | Object storage and the catalog are backed up on a declared cadence to a geographically separate location, and a scheduled drill restores from backup outside any migration. | The backup schedule is in code; the latest restore drill report compares content hashes and is within its schedule. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | ADLS Gen2 |
| [oss](../implementations/oss.yaml) | Ceph RGW via Rook |
<!-- END GENERATED: implementations -->
