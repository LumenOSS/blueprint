# Specifications

This is the reference part of the blueprint. It says what the blueprint
requires, precisely enough for you to build against it and test what you've
built. Turn to it when you need to know exactly what's required. If you want
to know why, the [core concepts](../concepts/README.md) explain.

| Specification | What it states |
| --- | --- |
| [Principles](principles.md) | The ideas every requirement rests on. If anything else seems to disagree with them, the principles state the intent. |
| [Capabilities](capabilities/README.md) | Everything the platform must be able to do, each with a contract of numbered clauses that say how you show you meet them |
| [Domain](domain/README.md) | What an EMIS holds: its domains, resources and modelling rules, its bounded contexts and its indicators |
| [Architecture](architecture/README.md) | How the parts fit together, at three levels of detail, and how the semantic layer works |
| [Standards](standards.md) | The international standards the blueprint relies on, with their current editions and links to their publishers |
| [Implementations](implementations/README.md) | The reference bindings, and where each one stands on every clause |
| [Glossary](glossary.md) | The terms the blueprint uses for itself and for the platform |

The capabilities come from one file, the catalogue in
`blueprint/catalogue.yaml`. Their contract tables are generated from it, so
that's the place to change them.
