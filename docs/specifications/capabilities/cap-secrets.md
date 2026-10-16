# CAP-SECRETS Secrets and keys

<!-- BEGIN GENERATED: header (just render) -->
Secrets and keys live in a managed store and are fetched by identity at runtime.

Layer L1 · domain: delivery
<!-- END GENERATED: header -->

## Purpose

The few secrets that remain, and the keys that protect data and state, are held under the platform's control.

## Why

Federation removes most secrets ([P3](../principles.md#p3-federation-not-secrets)), and whatever is left must never depend on one person's key. Some settings can only be chosen when a resource is created and can't be fixed afterwards, so they're decided before the first apply.

## Interfaces

- A managed secret store for each environment, reached through workload identity.
- Encrypted files in repositories, only when their recipients are roles or CI.
- A values file that states each option that can only be set at creation.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-SECRETS.1 | MUST | Secrets are held in a managed secret store; none is committed in plaintext, and any encrypted file in a repository has a recipient set of roles or CI, never one person. | A secret scanner runs on every change; encrypted files list non-personal recipients. |
| CAP-SECRETS.2 | MUST | Settings that can only be chosen at creation, such as customer-managed keys, are decided and recorded before an environment's first apply. | The environment's values file sets each creation-only option explicitly. |
| CAP-SECRETS.3 | SHOULD | Workloads read secrets at runtime using their own identity, so no secret is copied into deployment configuration. | Deployment manifests reference secrets by name, not value. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Azure Key Vault<br/>Key Vault-backed secret scopes |
| [oss](../implementations/oss.yaml) | OpenBao<br/>External Secrets Operator |
<!-- END GENERATED: implementations -->
