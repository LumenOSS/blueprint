# data-platform-blueprint

A reference architecture for a governed data platform, written so that the
architecture stays fixed while the implementation varies. It covers
operational databases, a lakehouse, governance and access, reporting,
backfill and migration, and an example product that exercises all of them.

Each part of the architecture is a **capability** with a **contract** of
numbered, testable clauses that name no vendor. An **implementation** binds
each capability to real components and shows evidence for every clause.
Two reference implementations are planned: one fully open source on
Kubernetes, one on Databricks.

Status: blueprint 0.1.0. Contracts are drafted; no implementation has
evidence yet.

## Map

| Read | For |
| --- | --- |
| [Principles](docs/principles.md) | The 19 ideas the architecture rests on, and why |
| [Architecture](docs/architecture/README.md) | C4 diagrams: context, containers, components |
| [Capabilities](docs/capabilities/README.md) | 34 capabilities and their contracts |
| [Implementations](docs/implementations/README.md) | Reference bindings for open source and Databricks, and where they differ |
| [Building an implementation](docs/building.md) | The steps, in dependency order, with completion criteria |
| [Example product](docs/product/README.md) | A document-review workload that runs through every layer |
| [Backfill patterns](docs/patterns/backfill.md) | Loading history and reprocessing, from published sources |
| [Lessons](docs/patterns/lessons.md) | Failures that shaped the design, as rules |
| [Decision records](docs/adr/README.md) | How and why the architecture changes |
| [Glossary](docs/glossary.md) | The terms used throughout |

## Layout

```text
blueprint/catalogue.yaml   capabilities and clauses: the single source of IDs and text
schema/                    JSON Schemas for the catalogue and for bindings
docs/                      everything above; contract tables are generated
scripts/blueprint.py       checks the catalogue and bindings, renders tables
```

## Develop

Everything runs in the Nix dev shell; tasks are `just` recipes.

```sh
nix develop --command just          # list the recipes
nix develop --command just check    # what every change must pass
nix develop --command just render   # regenerate tables after editing the catalogue
nix develop .#diagrams --command just diagrams   # render diagrams to build/
```

Formatting and linting are done by tools configured at the repository root
(ruff, pyright, markdownlint, yamlfmt, yamllint, biome, shfmt, shellcheck,
nixfmt, lychee). `just fmt` applies the formatters.

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
