# CAP-APPS Application hosting

<!-- BEGIN GENERATED: header (just render) -->
Product interfaces deployed by CI, behind sign-in, that say which environment they are in.

Layer L3 · domain: data · depends on: [CAP-NETWORK](cap-network.md), [CAP-DELIVERY](cap-delivery.md).
<!-- END GENERATED: header -->

## Purpose

Product interfaces are hosted so that they're private by default and can say which environment they're running in.

## Why

An environment that has only been half switched isn't half safe. An application can write to one environment while every label on it says another. If you ask the application which environment it believes it's in, you catch that.

## Interfaces

- A health endpoint that reports the target, the catalog and schema, the database branch and schema version, and the build version.
- A versioned interface, with a pinned snapshot of it.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-APPS.1 | MUST | Applications sit behind identity-provider sign-in and reach data services privately. | See CAP-NETWORK.1 and CAP-NETWORK.2 for each application host. |
| CAP-APPS.2 | MUST | A health endpoint reports the environment the application believes it is in: target, catalog and schema, database branch and schema version, and build version.<br><br>*Example:* GET /healthz returns the target, catalog and schema, database branch, schema version and build, so an operator can ask an application which environment it is in. | Query the endpoint in each environment; every field matches the environment. |
| CAP-APPS.3 | MUST | Application interfaces are versioned and change additively; a changed shape is a new route. | A pinned interface snapshot is compared in CI; removals fail. |
| CAP-APPS.4 | MUST | Applications are deployed by CI from a versioned image or artefact. | Running versions match a tag; no image is pushed from a workstation. |
| CAP-APPS.5 | MUST | Interfaces used by staff, learners, guardians or the public meet WCAG 2.2 Level AA (also published as ISO/IEC 40500:2025), checked automatically in CI and by a manual audit for each release. | An automated accessibility check runs in CI; manual audit findings are tracked. |
| CAP-APPS.6 | SHOULD | User-facing text is externalised and translatable, so an interface can be offered in more than one language. | No user-facing string is hard-coded outside the translation files. |
| CAP-APPS.7 | SHOULD | Data-capture paths work over low bandwidth and tolerate intermittent connectivity. | Capture flows are tested under throttled and interrupted network conditions. |
| CAP-APPS.8 | MUST | Applications that handle T3 or T4 data meet OWASP ASVS 5.0 Level 2. | The application's verification report cites the requirement identifiers it meets. |
| CAP-APPS.9 | MUST | Applications sign users in with OpenID Connect through the identity provider, and every OAuth deployment follows the OAuth 2.0 Security Best Current Practice (RFC 9700). | The sign-in configuration is reviewed against RFC 9700; implicit and password grants are disabled. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [BCP 47 Language tags](../standards.md#data-representation) | RFC 5646 and RFC 4647, with the IANA Language Subtag Registry | adopt |
| [GNU gettext PO files](../standards.md#accessibility-and-localisation) | GNU gettext 1.0 | adopt |
| [Unicode CLDR](../standards.md#accessibility-and-localisation) | CLDR 48.2 (March 2026) | reference |
| [Age appropriate design - a code of practice for online services (Children's code)](../standards.md#identity-security-and-privacy) | In force 2 September 2020 (conformance from 2 September 2021); guidance updated for the Data (Use and Access) Act 2025 | reference |
| [OpenAPI Specification](../standards.md#open-data-and-exchange) | OpenAPI 3.1 or later (3.2.1, September 2026) | adopt |
| [OpenID Connect Core 1.0](../standards.md#identity-security-and-privacy) | Core 1.0 incorporating errata set 2; also ISO/IEC 26131:2024 | adopt |
| [OAuth 2.0 Security Best Current Practice](../standards.md#identity-security-and-privacy) | RFC 9700 / BCP 240 (January 2025) | adopt |
| [OWASP Application Security Verification Standard](../standards.md#identity-security-and-privacy) | ASVS 5.0.0 (May 2025) | adopt |
| [Web Content Accessibility Guidelines](../standards.md#accessibility-and-localisation) | WCAG 2.2 Level AA (W3C Recommendation, December 2024 version); also ISO/IEC 40500:2025 | adopt |
| [EN 301 549 Accessibility requirements for ICT products and services](../standards.md#accessibility-and-localisation) | V4.1.1 (September 2026), aligned with WCAG 2.2; V3.2.1 where a procurement rule cites it | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Azure Container Apps |
| [oss](../implementations/oss.yaml) | Kubernetes Deployment + Gateway API |
<!-- END GENERATED: implementations -->
