# LumenOSS Blueprint

A blueprint for an education management information system (EMIS). It
describes the domain an EMIS records, the rules for handling its data, and
the governed data platform that holds it. The architecture stays the same
wherever you build it; only the implementation changes.

It covers everything an EMIS holds, from learners, schools, teachers and
staff to enrolment, attendance, assessment and the indicators reported
from them. It follows that data through operational databases, a
lakehouse, governance and access, reporting, backfill and migration, and
it includes example products that use all of them.

We describe each part of the architecture as a **capability**. Each
capability has a **contract**, which is a list of numbered clauses that
you can test and that name no vendor. An **implementation** connects each
capability to real components and shows evidence for every clause. We
plan two reference implementations: one entirely open source on
Kubernetes, and one on Databricks.

<!-- BEGIN GENERATED: status (just render) -->
Status: blueprint 0.5.0, with 41 capabilities and 246 clauses. Contracts are drafted; no implementation has evidence yet.
<!-- END GENERATED: status -->

If you're new here, start with [getting started](docs/getting-started.md).
It suggests an order to read things in, and a path for each role.

## How the blueprint changes

Anyone can propose a change, by writing a **LumenOSS Improvement
Proposal (LIP)**. A LIP is a numbered document that moves through its
stages in the open: Draft, then Review, then a 14-day Last Call, and then
a decision. It works the same way as the IETF's RFCs, Python's PEPs,
Bitcoin's BIPs, Ethereum's EIPs and Cardano's CIPs. Because the blueprint
governs data about children, every proposal says what it does to learners'
data. When a LIP is accepted, we write it up as a decision record and
release it in a new catalogue version.

[LIP-1](docs/lips/lip-0001.md) describes the process, and you can start
from the [template](docs/lips/template.md). Not every change needs a LIP,
though. [CONTRIBUTING.md](CONTRIBUTING.md) tells you which changes do and
which are ordinary reviewed changes, how to set up, and what reviewers
look for.

## Map

| Read | For |
| --- | --- |
| [Getting started](docs/getting-started.md) | The order to read everything in, by role |
| [Core concepts](docs/concepts/README.md) | What an EMIS is, its domain, its data, and the terms used throughout |
| [Specifications](docs/specifications/README.md) | What is required: principles, capabilities, domain, architecture, standards |
| [Guides](docs/guides/README.md) | How to build an implementation, run products and load history |
| [Principles](docs/specifications/principles.md) | The 22 ideas the architecture rests on, and why |
| [Architecture](docs/specifications/architecture/README.md) | C4 diagrams: context, containers, components |
| [Capabilities](docs/specifications/capabilities/README.md) | 41 capabilities and their contracts |
| [Implementations](docs/specifications/implementations/README.md) | Reference bindings for open source and Databricks, and where they differ |
| [Building an implementation](docs/guides/building.md) | The steps, in dependency order, with completion criteria |
| [Domain model](docs/specifications/domain/README.md) | What an EMIS holds: domains, resources, modelling rules, default classification |
| [Indicators](docs/specifications/domain/indicators.md) | How indicators are defined, computed and published |
| [Semantic layer](docs/specifications/architecture/semantic-layer.md) | Every indicator defined once and served to every consumer; dbt in both implementations |
| [Example products](docs/guides/products/README.md) | Document review and an annual census, each running through every layer, and a checklist for new products |
| [Backfill patterns](docs/guides/backfill.md) | Loading history and reprocessing, from published sources |
| [Lessons](docs/guides/lessons.md) | Failures that shaped the design, as rules |
| [Standards](docs/specifications/standards.md) | The international standards relied on, with current editions and publisher links |
| [Contributing](CONTRIBUTING.md) | Which path a change takes, setting up, writing and review |
| [Improvement proposals](docs/lips/README.md) | How to propose a change, and every LIP so far |
| [Decision records](docs/adr/README.md) | What was decided, and why |
| [Context map](CONTEXT-MAP.md) | The bounded contexts of the EMIS domain and their language, with the words to avoid |
| [Domain design](docs/specifications/domain/design.md) | Subdomains, aggregates, invariants and domain events |
| [Glossary](docs/specifications/glossary.md) | Terms about the blueprint and the platform |

## Layout

```text
blueprint/catalogue.yaml   capabilities and clauses: the single source of IDs and text
blueprint/standards.yaml   the standards register: editions, publisher links, users
schema/                    JSON Schemas for the catalogue, the register and bindings
l10n/                      translations of the docs, as gettext PO files per language
docs/                      everything above; contract tables are generated
scripts/blueprint.py       checks the catalogue and bindings, renders tables
```

## Develop

Everything runs in the Nix dev shell, and every task is a `just` recipe.

```sh
nix develop --command just          # list the recipes
nix develop --command just check    # what every change must pass
nix develop --command just render   # regenerate tables after editing the catalogue
nix develop .#diagrams --command just diagrams   # render diagrams to build/
nix develop .#site --command just site-serve     # preview the website
```

Tools configured at the repository root do the formatting and linting:
ruff, pyright, markdownlint, yamlfmt, yamllint, biome, shfmt, shellcheck,
nixfmt and lychee. Run `just fmt` to apply the formatters.

## Licence

The blueprint is released under the Apache License 2.0. See
[LICENSE](LICENSE).
