# ADR-0003: Split repositories by trust layer

**Status:** accepted. **Date:** 2026-10-15.

## Context

With workload identity federation, a cloud or platform credential trusts a
repository (and an environment in it), not a person or a secret. In a
single repository, anyone who can change a pipeline definition can reach
every identity that repository is trusted with. Landing-zone toolkits and
public-sector platforms studied for this design split their code along
privilege lines.

## Decision

Four layers, each its own repository:

- **L0 Bootstrap:** the state store and the CI identities. Applied only by
  manual dispatch from the main branch by an allow-listed role, after two
  approvals.
- **L1 Platform:** shared infrastructure, governance and the tenant
  onboarding registry. Applied on merge.
- **L2 Modules:** versioned building blocks consumed by tag.
- **L3 Products:** one repository per product, deploying only inside the
  boundary its tenant entry grants.

Inside a repository, state is split per stack and environment.

## Consequences

- A compromised product pipeline cannot reach platform or bootstrap
  identities ([CAP-REPOSITORIES.2](../capabilities/cap-repositories.md)).
- The root of trust is made once by a person and recorded
  ([CAP-CIIDENTITY.4](../capabilities/cap-ciidentity.md)).
- More repositories to keep in step; modules and published outputs are how
  they share without sharing state.
