# Specifications

The reference: what the blueprint requires, stated precisely enough to
build against and to test. Read these when you need to know exactly what
is required; the [core concepts](../concepts/README.md) explain why.

| Specification | What it states |
| --- | --- |
| [Principles](principles.md) | The ideas every requirement rests on; when anything else seems to disagree, these state the intent |
| [Capabilities](capabilities/README.md) | Every capability of the platform and its contract: numbered clauses, each with how conformance is shown |
| [Domain](domain/README.md) | What an EMIS holds: domains, resources, modelling rules, bounded contexts and indicators |
| [Architecture](architecture/README.md) | How the parts fit together, at three levels of detail, and the semantic layer |
| [Standards](standards.md) | The international standards relied on, with current editions and publisher links |
| [Implementations](implementations/README.md) | The reference bindings, and the status of every clause in each |
| [Glossary](glossary.md) | Terms about the blueprint and the platform |

The catalogue in `blueprint/catalogue.yaml` is the source of the
capabilities; their contract tables are generated from it.
