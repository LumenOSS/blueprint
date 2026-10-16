# ADR-0008: Model the EMIS domain in the blueprint

**Status:** accepted. **Date:** 2026-10-15.

## Context

The blueprint's first version described the platform under an education
management information system, but not the system itself. An EMIS has
needs a generic data platform does not state: one authoritative record per
institution and person, identifiers that survive transfers and boundary
changes, code lists shared by every institution, periodic collection from
thousands of respondents, indicators computed as at a reference date,
records that must eventually be disposed of, and people who are entitled to
see their own data.

## Decision

- Add a [domain model](../specifications/domain/README.md): domains, core resources,
  modelling rules, default classification and build order.
- Add capabilities for master data and identifiers, reference data and the
  data dictionary, periodic collection, records lifecycle and data-subject
  rights, open publication, exchange with other systems, and governed
  analytical models.
- Extend existing capabilities where the EMIS adds obligations: access by
  relationship, purpose of access, default classification by kind of
  attribute, quality dimensions and correction requests, indicator
  metadata, effective-dated history, accessible and translatable
  interfaces.
- Add two principles: collect for a declared purpose (P20), and the
  education authority runs its own platform (P21).
- Release this as catalogue 0.2.0. Before 1.0.0 the catalogue is
  pre-release, and a minor version may add `MUST` clauses, as semantic
  versioning allows for 0.y versions; from 1.0.0 the rule in
  [ADR-0002](0002-capabilities-contracts-and-bindings.md) applies in full.

## Consequences

- An implementation now has to model the domain, not only run the
  platform; the census product exercises most of the new capabilities.
- Existing bindings gain clauses in `planned` status until evidence exists.
- Country-specific code lists and terms stay out of the blueprint; the
  blueprint fixes the rules, an implementation supplies the lists.
