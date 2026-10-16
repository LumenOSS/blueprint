# ADR-0013: Divide the EMIS domain into bounded contexts

**Status:** accepted. **Date:** 2026-10-16. Proposed in
[LIP-2](../lips/lip-0002.md); builds on
[ADR-0008](0008-model-the-emis-domain.md).

## Context

ADR-0008 divided the domain into catalogs and gave it one language. One
language for the whole domain let terms drift (a "programme" of study and
a "programme" of free meals), and nothing stopped one product from reading
another's operational database.

## Decision

- The domain has ten bounded contexts, listed in the
  [context map](../../CONTEXT-MAP.md), each with its own `CONTEXT.md`,
  steward and catalogs. Learning and Statistics are the core subdomains.
- [Domain design](../specifications/domain/design.md) records each context's aggregates,
  invariants and domain events, and is kept in step with the languages.
- Contexts integrate only through published interfaces
  (CAP-INTEROPERABILITY.8) and publish their domain events in a catalogue
  (CAP-INTEROPERABILITY.9). Catalogue 0.4.0.

## Consequences

- A new term belongs to exactly one context; a word used differently in
  two contexts is defined in each and translated at the boundary.
- Products need grants to their own context's operational database only,
  which a test can prove.
- The `programmes` catalog becomes `entitlements`, and the domain model
  gains the `statistics` and `records` catalogs.
