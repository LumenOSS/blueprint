# ADR-0005: Decide access by role, scope and sensitivity

**Status:** accepted. **Date:** 2026-10-15.

## Context

Public-sector data, such as education data, is read by people whose reach
depends on their role (analyst, steward, school leader) and whose scope
depends on where they work (one institution, one district, the whole system). A
single list of grants cannot express both without one grant per person and
place, and it cannot express that some columns are more sensitive than
others.

## Decision

Three inputs, each owned by a different role:

1. **Reach** from identity-provider groups, by role, owned by the platform
   team.
2. **Row scope** from an entitlement table derived from an authoritative
   feed (for example staff postings), owned by its loader, never edited by
   hand.
3. **Column visibility** from a governed classification tag (T0 public
   aggregate to T4 special category), owned by stewards.

Policies only narrow. Exemptions are limited to pipeline identities, each
with a reason. Identifiable columns are visible only through a time-boxed,
audited group. T4 data lives in its own catalog and storage.

## Consequences

- No single change widens access across all three inputs
  ([CAP-ACCESS.6](../specifications/capabilities/cap-access.md)).
- Where an engine cannot enforce row filters and masks, it is denied the
  protected tables ([CAP-CATALOG.5](../specifications/capabilities/cap-catalog.md)).
- The entitlement feed's owner becomes a dependency of the platform and
  must be named.
