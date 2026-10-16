# LumenOSS Blueprint

<!-- The landing page. The build turns each "##" section into a grid of
cards: each "###" heading is a card, the comment under it names its icon,
and the link in its last paragraph is its button. The first paragraph is
the lead, and the links after it are the buttons under it. -->

A blueprint for an education management information system: the domain it records, the rules for handling its data, and the governed platform that holds it. The architecture stays fixed; the implementation is yours to choose.

[Get started](../docs/getting-started.md) · [View on GitHub](https://github.com/LumenOSS/blueprint)

## Start with the concepts

### What is an EMIS

<!-- icon: circle-info -->

The system an education authority uses to know how many learners there are, where, and how they are doing, and the part this blueprint covers.

[Read the definition](../docs/concepts/emis.md)

### The EMIS domain

<!-- icon: graduation-cap -->

What a domain model is, why it is used here, and the main things an EMIS records, in one diagram.

[Meet the model](../docs/concepts/domain.md)

### Data in an EMIS

<!-- icon: lock -->

Sensitive data, masking, access by role and attribute, sharing, and lineage: five ideas to keep in mind.

[Read the primer](../docs/concepts/data.md)

### Terminology

<!-- icon: tag -->

Sensitivity tiers, layers, clauses and roles: what you need to read the specifications.

[Learn the terms](../docs/concepts/terminology.md)

## Specifications

### Principles

<!-- icon: lightbulb -->

The ideas every decision rests on, each with its reason, from CI as the only deployer to collecting data only for a declared purpose.

[Read the principles](../docs/specifications/principles.md)

### Architecture

<!-- icon: worktree -->

C4 diagrams from system context to components, each followed by why it is drawn that way.

[See the diagrams](../docs/specifications/architecture/README.md)

### Capabilities

<!-- icon: list-check -->

Forty-one capabilities, each a contract of testable clauses that name no vendor.

[Browse the contracts](../docs/specifications/capabilities/README.md)

### Domain model

<!-- icon: list -->

Institutions, learners, staff and their relationships, modelled so that every indicator can be counted at a reference date.

[Explore the domain](../docs/specifications/domain/README.md)

### Semantic layer

<!-- icon: scale-balanced -->

Every indicator defined once and served to every dashboard, agent and publication, with dbt in both reference implementations.

[How indicators are defined](../docs/specifications/architecture/semantic-layer.md)

### Standards

<!-- icon: shield -->

The international standards relied on, each linked to its publisher with the edition and the date it was checked.

[See the register](../docs/specifications/standards.md)

## Guides and implementations

### Building an implementation

<!-- icon: code -->

The steps in dependency order, each with a clear point at which it is done.

[Follow the steps](../docs/guides/building.md)

### Implementations

<!-- icon: fork -->

Open source on Kubernetes, or Databricks on Azure, and exactly where the two differ.

[Compare the stacks](../docs/specifications/implementations/README.md)

### Example products

<!-- icon: file-lines -->

Document review and an annual census, each running through every layer of the platform.

[See them work](../docs/guides/products/README.md)

Open source under the Apache License 2.0.
