# CAP-IDENTITY Identity and groups

One identity provider for people and groups, synchronised automatically, with break-glass access held apart.

Layer L1 · domain: governance

## Purpose

Make the organisation's identity provider the one source of people and groups.

## Why

Local users and groups drift from the organisation. Renamed groups do not propagate reliably, so names are frozen.

## Interfaces

- Automatic user and group provisioning (for example SCIM) into every service.
- Group declarations in the platform repository.
- Two break-glass accounts.

## Notes

Membership refresh can lag by minutes in browsers and longer in jobs. Indirect administrator paths exist on most clouds; list them.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-IDENTITY.1 | MUST | The organisation's identity provider is the only source of users, groups and membership, synchronised to every platform service automatically. | No platform service has a locally created user or group except break-glass accounts. |
| CAP-IDENTITY.2 | MUST | Group names are frozen once created, because renames do not propagate reliably. | The group declarations forbid renames (a rename is a new group plus migration). |
| CAP-IDENTITY.3 | MUST | Two break-glass accounts exist, outside the identity provider's normal sign-in, protected by hardware keys, monitored on every use. | Sign-in by either account raises an alert. |
| CAP-IDENTITY.4 | MUST | Indirect administrator paths (a directory role that becomes a platform administrator, a resource role that grants workspace administration) are closed or monitored. | The access review lists each such path and its control. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
