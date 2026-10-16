# CAP-INTEROPERABILITY Exchange with other systems

<!-- BEGIN GENERATED: header (just render) -->
Every feed to or from another system is declared, validated at the edge and reconciled.

Layer L1 · domain: data · depends on: [CAP-ONBOARDING](cap-onboarding.md), [CAP-CATALOG](cap-catalog.md).
<!-- END GENERATED: header -->

## Purpose

Exchange data with the other systems an education authority depends on, without losing track of what went where.

## Why

An EMIS is one system among several, and errors cluster at the joins. Declaring every feed, validating at the edge and reconciling both directions turns those joins into checked contracts instead of informal transfers ([P16](../principles.md#p16-open-formats-storage-separate-from-compute-federate-before-copying)).

## Interfaces

- Feed entries in the onboarding registry.
- Versioned interfaces with machine-readable contracts.
- Edge validation with reject reports; per-period reconciliation.

## Notes

Any two systems that should agree can be reconciled with the release-gate pattern: a period reads BLOCKED until the counts on both sides balance.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-INTEROPERABILITY.1 | MUST | Every exchange with another system is a feed contract in the onboarding registry, naming its counterpart, purpose, schema, schedule, owning steward and the agreement that governs it. | Every live feed traces to a registry entry. |
| CAP-INTEROPERABILITY.2 | MUST | Inbound feeds from other systems are validated at the edge against a published schema before landing, and a reject report goes back to the sender.<br><br>*Example:* A partner feed arrives with a malformed date column; it is refused at the edge, and the sender receives a report naming the row and the rule it broke. | A malformed fixture is rejected with a report and never lands. |
| CAP-INTEROPERABILITY.3 | MUST | Outbound feeds are reconciled with their recipient by counts and hashes for each period.<br><br>*Example:* Each month the outbound feed is compared with the recipient's own count and hash; a mismatch opens an incident. | Each outbound feed has a reconciliation record per period. |
| CAP-INTEROPERABILITY.4 | MUST | Systems of record expose versioned interfaces that change additively, each described in OpenAPI 3.1 or later, with payload schemas in JSON Schema 2020-12. | A pinned contract is compared in CI; removals fail. |
| CAP-INTEROPERABILITY.5 | SHOULD | Exchanged records use a recognised open education data standard where one exists: 1EdTech OneRoster 1.2 for class lists and results, 1EdTech CASE 1.1 for curriculum frameworks, and CEDS as the reference vocabulary for data elements. | Each feed names the standard it maps to, or why none applies. |
| CAP-INTEROPERABILITY.6 | SHOULD | Feed health (arrival, lag, reject rate, latency) is measured per feed and reaches gold. | A gold model reports feed health per feed and period. |
| CAP-INTEROPERABILITY.7 | SHOULD | Evented interfaces are described in AsyncAPI 3 and carry a CloudEvents envelope whose id and source form the idempotency key. | Each evented feed has an AsyncAPI document; a replayed event with the same id and source changes nothing. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [Common Education Data Standards (CEDS)](../standards.md#open-data-and-exchange) | Version 14 (official release on the CEDS GitHub, March–April 2026); the ceds.ed.gov downloads still offer Version 13 | reference |
| [1EdTech OneRoster](../standards.md#open-data-and-exchange) | 1.2 (September 2022) | adopt |
| [OpenAPI Specification](../standards.md#open-data-and-exchange) | OpenAPI 3.1 or later (3.2.1, September 2026) | adopt |
| [JSON Schema](../standards.md#open-data-and-exchange) | Draft 2020-12 | adopt |
| [AsyncAPI Specification](../standards.md#open-data-and-exchange) | AsyncAPI 3.x (3.1.0, January 2026) | adopt |
| [CloudEvents](../standards.md#open-data-and-exchange) | CloudEvents 1.0.2 | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Azure API Management<br/>Schema validation at the landing edge |
| [oss](../implementations/oss.yaml) | Envoy Gateway<br/>Schema validation at the landing edge |
<!-- END GENERATED: implementations -->
