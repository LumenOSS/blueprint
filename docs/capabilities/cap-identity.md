# CAP-IDENTITY Identity and groups

<!-- BEGIN GENERATED: header (just render) -->
One identity provider for people and groups, synchronised automatically, with break-glass access held apart.

Layer L1 · domain: governance
<!-- END GENERATED: header -->

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
| CAP-IDENTITY.5 | MUST | Administrators and every role that can read identifiable or special-category data (T3, T4) authenticate at NIST SP 800-63-4 authentication assurance level 2 or higher with a phishing-resistant authenticator, such as a WebAuthn passkey; platform administrators and holders of the root of trust authenticate at level 3.<br><br>*Example:* A support officer who can read special-category records signs in with a passkey; a password with a text-message code is refused for that role. | Sign-in policy for those roles requires it; a sign-in without it is refused. |
| CAP-IDENTITY.6 | MUST | Learners, guardians and members of the public authenticate through a separate external identity tenant or portal, and are never members of platform groups. | No platform group contains an external identity. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [NIST SP 800-63-4 Digital Identity Guidelines](../standards.md#identity-security-and-privacy) | SP 800-63-4, final (July 2025) | adopt |
| [Web Authentication](../standards.md#identity-security-and-privacy) | Level 2 or later (Level 3, W3C Recommendation, August 2026) | adopt |
| [OpenID Connect Core 1.0](../standards.md#identity-security-and-privacy) | Core 1.0 incorporating errata set 2; also ISO/IEC 26131:2024 | adopt |
| [OAuth 2.0 Security Best Current Practice](../standards.md#identity-security-and-privacy) | RFC 9700 / BCP 240 (January 2025) | adopt |
| [SCIM 2.0](../standards.md#identity-security-and-privacy) | RFC 7643 and RFC 7644 (2015), with later extensions | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Entra ID<br/>Automatic identity management / SCIM |
| [oss](../implementations/oss.yaml) | Keycloak |
<!-- END GENERATED: implementations -->
