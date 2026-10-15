# CAP-SECRETS Secrets and keys

Secrets and keys live in a managed store and are fetched by identity at runtime.

Layer L1 · domain: delivery

## Purpose

Hold the few secrets that remain, and the keys that protect data and state, under the platform's control.

## Why

Federation removes most secrets ([P3](../principles.md#p3-federation-not-secrets)); what remains must never depend on one person's key. Creation-only settings cannot be fixed later, so they are decided before the first apply.

## Interfaces

- A managed secret store per environment, reached by workload identity.
- Encrypted files in repositories only with a recipient set of roles or CI.
- A values file that states each creation-only option.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-SECRETS.1 | MUST | Secrets are held in a managed secret store; none is committed in plaintext, and any encrypted file in a repository has a recipient set of roles or CI, never one person. | A secret scanner runs on every change; encrypted files list non-personal recipients. |
| CAP-SECRETS.2 | MUST | Settings that can only be chosen at creation, such as customer-managed keys, are decided and recorded before an environment's first apply. | The environment's values file sets each creation-only option explicitly. |
| CAP-SECRETS.3 | SHOULD | Workloads read secrets at runtime using their own identity, so no secret is copied into deployment configuration. | Deployment manifests reference secrets by name, not value. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
