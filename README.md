# data-platform-blueprint

A reference architecture for the governed data platform behind an
education management information system (EMIS), written so that the
architecture stays fixed while the implementation varies. It covers the
resources an EMIS holds (learners, schools, teachers and staff, enrolment,
attendance, assessment and the indicators reported from them) through
operational databases, a lakehouse, governance and access, reporting,
backfill and migration, and example products that exercise all of them.

Each part of the architecture is a **capability** with a **contract** of
numbered, testable clauses that name no vendor. An **implementation** binds
each capability to real components and shows evidence for every clause.
Two reference implementations are planned: one fully open source on
Kubernetes, one on Databricks.

Status: blueprint 0.3.0. Contracts are drafted; no implementation has
evidence yet.

**New here?** Start with [getting started](docs/getting-started.md): it
gives a reading order for everyone and a track for each role.

## Map

| Read | For |
| --- | --- |
| [Getting started](docs/getting-started.md) | The order to read everything in, by role |
| [Principles](docs/principles.md) | The 21 ideas the architecture rests on, and why |
| [Architecture](docs/architecture/README.md) | C4 diagrams: context, containers, components |
| [Capabilities](docs/capabilities/README.md) | 41 capabilities and their contracts |
| [Implementations](docs/implementations/README.md) | Reference bindings for open source and Databricks, and where they differ |
| [Building an implementation](docs/building.md) | The steps, in dependency order, with completion criteria |
| [Domain model](docs/domain/README.md) | What an EMIS holds: domains, resources, modelling rules, default classification |
| [Indicators](docs/domain/indicators.md) | How indicators are defined, computed and published |
| [Semantic layer](docs/architecture/semantic-layer.md) | Every indicator defined once and served to every consumer; dbt in both implementations |
| [Example products](docs/product/README.md) | Document review and an annual census, each running through every layer, and a checklist for new products |
| [Backfill patterns](docs/patterns/backfill.md) | Loading history and reprocessing, from published sources |
| [Lessons](docs/patterns/lessons.md) | Failures that shaped the design, as rules |
| [Standards](docs/standards.md) | The international standards relied on, with current editions and publisher links |
| [Decision records](docs/adr/README.md) | How and why the architecture changes |
| [Domain language](CONTEXT.md) | The EMIS terms used throughout, with the words to avoid |
| [Glossary](docs/glossary.md) | Terms about the blueprint and the platform |

## Layout

```text
blueprint/catalogue.yaml   capabilities and clauses: the single source of IDs and text
blueprint/standards.yaml   the standards register: editions, publisher links, users
schema/                    JSON Schemas for the catalogue, the register and bindings
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
nix develop .#site --command just site-serve     # preview the website
```

Formatting and linting are done by tools configured at the repository root
(ruff, pyright, markdownlint, yamlfmt, yamllint, biome, shfmt, shellcheck,
nixfmt, lychee). `just fmt` applies the formatters.

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
