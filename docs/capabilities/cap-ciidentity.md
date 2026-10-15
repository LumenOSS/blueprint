# CAP-CIIDENTITY CI workload identity

CI authenticates by federation with short-lived tokens; the root of trust is created once by a person.

Layer L0 · domain: delivery

## Purpose

Let CI act on the platform without any stored secret, and make sure no identity can widen its own access.

## Why

A stored secret can be copied; a federated token is minted per run and only for a protected environment ([P3](../principles.md#p3-federation-not-secrets)). The identity that defines identities is the root of trust and is created by a person once ([P4](../principles.md#p4-the-root-of-trust-is-made-once-by-a-person-and-cannot-widen-itself)). Role assignment rights are conditioned to a list ([P5](../principles.md#p5-least-privilege-enumerated)).

## Interfaces

- The CI host's OIDC token, exchanged for a cloud or platform token.
- Federated credentials whose subject names a repository and a protected environment.
- Separate plan (read-only) and apply identities per layer; a deploy and a run-as identity per product per environment.

## Notes

Count credentials before adding them: identity providers cap federated credentials per identity. Verify the subject format of each CI host before relying on it.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-CIIDENTITY.1 | MUST | No long-lived credential for a cloud, data platform or registry exists in any repository or CI variable; CI exchanges its host-issued token for a short-lived one. | Inventory the CI secrets and variables; none is a credential for a platform service. |
| CAP-CIIDENTITY.2 | MUST | A federated credential binds a protected environment, not a branch or tag, so the binding cannot be edited by a change under review. | Every credential subject names an environment; every environment restricts which branch may deploy. |
| CAP-CIIDENTITY.3 | MUST | Plan and apply run as different identities, and the plan identity cannot change anything. | Negative test: an apply attempted with the plan identity is denied. |
| CAP-CIIDENTITY.4 | MUST | The identity that creates CI identities is created once by a person, recorded in the bootstrap repository with its rights and its creator's role, and never applies the code declaring its own credentials. | The bootstrap README records the identity; its apply refuses the stack that declares it. |
| CAP-CIIDENTITY.5 | MUST | A right to assign roles is conditioned to an enumerated list of roles on named scopes, never organisation-wide. | Read the role assignment's condition; it lists the assignable roles. |
| CAP-CIIDENTITY.6 | SHOULD | Each product has one deploy identity and one run-as identity per environment. | The tenant registry generates exactly those two per product per environment. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
