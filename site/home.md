# LumenOSS Blueprint

<!-- The landing page. The build turns each "##" section into a grid of
cards: each "###" heading is a card, the comment under it names its icon,
and the link in its last paragraph is its button. The first paragraph is
the lead, and the links after it are the buttons under it. -->

A blueprint for an education management information system. It describes the domain the system records, the rules for handling its data, and the governed platform that holds it. The architecture stays the same, and you choose how to implement it.

[Get started](../docs/getting-started.md) · [View on GitHub](https://github.com/LumenOSS/blueprint)

## Start with the concepts

### What is an EMIS

<!-- icon: circle-info -->

An education authority uses an EMIS to know how many learners it has, where they are and how they're doing. Find out what that involves, and which part of it this blueprint covers.

[Read the definition](../docs/concepts/emis.md)

### The EMIS domain

<!-- icon: graduation-cap -->

Learn what a domain model is and why we use one, then see the main things an EMIS records in a single diagram.

[Meet the model](../docs/concepts/domain.md)

### Data in an EMIS

<!-- icon: lock -->

Five ideas to keep in mind as you read on: sensitive data, masking, access by role and by attribute, sharing, and lineage.

[Read the primer](../docs/concepts/data.md)

### Terminology

<!-- icon: tag -->

The sensitivity tiers, layers, clauses and roles you'll need to know before you read the specifications.

[Learn the terms](../docs/concepts/terminology.md)

## Specifications

### Principles

<!-- icon: lightbulb -->

The ideas that every decision rests on, each with its reason. They range from CI being the only deployer to collecting data only for a declared purpose.

[Read the principles](../docs/specifications/principles.md)

### Architecture

<!-- icon: worktree -->

C4 diagrams that go from the system's context down to its components, each followed by an explanation of why it's drawn that way.

[See the diagrams](../docs/specifications/architecture/README.md)

### Capabilities

<!-- icon: list-check -->

Forty-one capabilities. Each one is a contract made of clauses that you can test and that name no vendor.

[Browse the contracts](../docs/specifications/capabilities/README.md)

### Domain model

<!-- icon: list -->

How we model institutions, learners, staff and the relationships between them, so that you can count every indicator at a reference date.

[Explore the domain](../docs/specifications/domain/README.md)

### Semantic layer

<!-- icon: scale-balanced -->

We define each indicator once and serve it to every dashboard, agent and publication. Both reference implementations use dbt for this.

[How indicators are defined](../docs/specifications/architecture/semantic-layer.md)

### Standards

<!-- icon: shield -->

The international standards the blueprint relies on. Each one links to its publisher, with the edition we use and the date we last checked it.

[See the register](../docs/specifications/standards.md)

## Guides and implementations

### Building an implementation

<!-- icon: code -->

The steps to build an implementation, in the order their dependencies require. Each step tells you clearly when it's done.

[Follow the steps](../docs/guides/building.md)

### Implementations

<!-- icon: fork -->

Build it from open-source components on Kubernetes, or on Databricks in Azure, and see exactly where the two differ.

[Compare the stacks](../docs/specifications/implementations/README.md)

### Example products

<!-- icon: file-lines -->

Document review and an annual census, two products that each run through every layer of the platform.

[See them work](../docs/guides/products/README.md)

The blueprint is open source, under the Apache License 2.0.
