# ADR-0002: State the architecture as capabilities, contracts and bindings

**Status:** accepted. **Date:** 2026-10-15.

## Context

The architecture has to hold across environments that use different
vendors, or none. An architecture described through its products is
rewritten whenever a product changes; one described only in prose cannot be
checked.

## Decision

- The architecture is a set of **capabilities**, each with a **contract** of
  numbered clauses (`MUST`, `SHOULD`, `MAY`), each clause saying how
  conformance is shown. Contracts name no vendor.
- [`blueprint/catalogue.yaml`](../../blueprint/catalogue.yaml) is the single
  source of capability IDs and clause text. IDs are never renumbered or
  reused; a retired clause stays, marked retired.
- An **implementation** states its components and the status and evidence of
  every clause in a **binding** file validated by
  [`schema/binding.schema.json`](../../schema/binding.schema.json). A clause
  it cannot meet is a recorded deviation with its consequence.
- The catalogue follows semantic versioning: a new `MUST` or a changed
  meaning is a major version; a new capability or `SHOULD` is minor.

## Consequences

- Swapping a component changes one binding, not the blueprint.
- Conformance is a list of verifications, so it can be automated and
  audited.
- Writing a clause that can be tested is harder than writing a principle;
  untestable ideas stay as principles.
