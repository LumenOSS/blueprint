# CAP-REPOSITORIES Repositories by trust

<!-- BEGIN GENERATED: header (just render) -->
Each layer is its own repository and the unit of trust for its CI identities.

Layer L0 · domain: delivery
<!-- END GENERATED: header -->

## Purpose

Separate the code that defines who may change the platform from the code that changes it, so each repository can be trusted for exactly what it holds.

## Why

With workload identity federation a credential trusts a repository, so the repository is the unit of trust ([P2](../principles.md#p2-repositories-are-split-by-trust-state-is-split-by-blast-radius)). A monorepo would let anyone who can edit a pipeline reach every identity. Pinned recipes keep the result the same on any machine and any CI host ([P19](../principles.md#p19-every-task-is-a-pinned-host-independent-recipe)).

## Interfaces

- Bootstrap repository: state store and CI identities, applied by dispatch.
- Platform repository: shared stacks and the tenant registry, applied on merge.
- Modules repository: tagged releases consumed by the others.
- Product repositories: code, jobs and their deployment unit, one per product.

## Notes

Two remotes are normal: a repository can be mirrored on a second host and carry that host's CI definition beside the first. Only the wrapper differs; every step is a recipe.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-REPOSITORIES.1 | MUST | Bootstrap, platform, modules and each product are separate repositories. | List the repositories; each layer and each product has exactly one. |
| CAP-REPOSITORIES.2 | MUST | Each federated credential trusts exactly one repository, so a change in one repository cannot obtain another's identity. | Export every federated credential subject; each names one repository and one protected environment. |
| CAP-REPOSITORIES.3 | MUST | Every task runs as a recipe in a pinned toolchain, invoked the same way on a workstation and in CI; CI definitions only call recipes. | Inspect the CI definitions: every step is a toolchain bootstrap or a recipe invocation. |
| CAP-REPOSITORIES.4 | MUST | Published history is never rewritten; a correction is a new change on top. | The protected branch refuses force-pushes. |
| CAP-REPOSITORIES.5 | SHOULD | A repository can be hosted on more than one CI host without code changes beyond a thin CI wrapper. | The repository carries the CI definition of each host it targets, and each calls the same recipes. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Git with two remotes<br/>Azure Pipelines<br/>Nix flake + just |
| [oss](../implementations/oss.yaml) | Git with two remotes<br/>Forgejo Actions<br/>Nix flake + just |
<!-- END GENERATED: implementations -->
