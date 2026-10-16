# CAP-CIIDENTITY CI workload identity

<!-- BEGIN GENERATED: header (just render) -->
CI authenticates by federation with short-lived tokens; the root of trust is created once by a person.

Layer L0 · domain: delivery
<!-- END GENERATED: header -->

## Purpose

CI can act on the platform without any stored secret, and no identity can widen its own access.

## Why

A stored secret can be copied. A federated token, by contrast, is minted for each run and only for a protected environment ([P3](../principles.md#p3-federation-not-secrets)). The identity that defines all the other identities is the root of trust, so a person creates it once ([P4](../principles.md#p4-the-root-of-trust-is-made-once-by-a-person-and-cannot-widen-itself)). The right to assign roles is limited to a listed set of roles ([P5](../principles.md#p5-least-privilege-enumerated)).

## Interfaces

- The CI host's OIDC token, exchanged for a cloud or platform token.
- Federated credentials whose subject names a repository and a protected environment.
- Separate identities for plan (read-only) and apply in each layer, and a deploy identity and a run-as identity for each product in each environment.

## Notes

Identity providers limit how many federated credentials one identity can have, so count them before you add more. Check the subject format each CI host uses before you rely on it.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-CIIDENTITY.1 | MUST | No long-lived credential for a cloud, data platform or registry exists in any repository or CI variable; CI exchanges its host-issued token for a short-lived one. | Inventory the CI secrets and variables; none is a credential for a platform service. |
| CAP-CIIDENTITY.2 | MUST | A federated credential binds a protected environment, not a branch or tag, so the binding cannot be edited by a change under review.<br><br>*Example:* A credential trusts 'repository data-platform, environment production'; a workflow running on an unreviewed branch is not in that environment, so it cannot obtain a token. | Every credential subject names an environment; every environment restricts which branch may deploy. |
| CAP-CIIDENTITY.3 | MUST | Plan and apply run as different identities, and the plan identity cannot change anything. | Negative test: an apply attempted with the plan identity is denied. |
| CAP-CIIDENTITY.4 | MUST | The identity that creates CI identities is created once by a person, recorded in the bootstrap repository with its rights and its creator's role, and never applies the code declaring its own credentials. | The bootstrap README records the identity; its apply refuses the stack that declares it. |
| CAP-CIIDENTITY.5 | MUST | A right to assign roles is conditioned to an enumerated list of roles on named scopes, never organisation-wide. | Read the role assignment's condition; it lists the assignable roles. |
| CAP-CIIDENTITY.6 | SHOULD | Each product has one deploy identity and one run-as identity per environment. | The tenant registry generates exactly those two per product per environment. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Entra workload identity federation<br/>Databricks OAuth federation policies |
| [oss](../implementations/oss.yaml) | CI OIDC token<br/>OpenBao JWT auth<br/>Kubernetes projected service-account tokens |
<!-- END GENERATED: implementations -->
