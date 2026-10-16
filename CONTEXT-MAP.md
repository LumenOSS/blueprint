# Context map

We divide the EMIS domain into bounded contexts. Each context has its own
language, one steward who owns it, and its own catalogs. A context talks
to the others only through interfaces it publishes. You'll find how the
contexts are designed, with their subdomains, aggregates, invariants and
events, in the [domain design](docs/specifications/domain/design.md).
Terms about the blueprint and the platform itself are in the
[glossary](docs/specifications/glossary.md).

## Contexts

- [Reference](docs/specifications/domain/contexts/reference/CONTEXT.md) is the shared kernel of time, codes, geography and registries.
- [People](docs/specifications/domain/contexts/people/CONTEXT.md) records each person once, whatever roles they hold.
- [Institutions](docs/specifications/domain/contexts/institutions/CONTEXT.md) covers institutions, the sites they occupy and the state of those sites.
- [Learning](docs/specifications/domain/contexts/learning/CONTEXT.md) covers enrolment, class membership, attendance, progression and guardianship.
- [Workforce](docs/specifications/domain/contexts/workforce/CONTEXT.md) covers posts and the staff posted to them.
- [Curriculum](docs/specifications/domain/contexts/curriculum/CONTEXT.md) covers programmes, grades, subjects and classes.
- [Assessment](docs/specifications/domain/contexts/assessment/CONTEXT.md) covers tests and examinations, their candidates and their results.
- [Statistics](docs/specifications/domain/contexts/statistics/CONTEXT.md) covers collections, returns, snapshots, indicators and publication.
- [Records](docs/specifications/domain/contexts/records/CONTEXT.md) covers retention, disposal, correction and individual disclosure.
- [Operations](docs/specifications/domain/contexts/operations/CONTEXT.md) covers budgets, assets, entitlement schemes and safety.

## Relationships

Each relationship below is named after the pattern it follows.

- **Reference → every context** is a shared kernel. Every context uses
  code lists, academic periods, reference dates and administrative areas
  unchanged, so every steward reviews a change to them.
- **External registers → People** goes through an anti-corruption layer.
  People reads civil and other registers through an adapter, which
  translates their identifiers and outcomes into People's language. Their
  model never leaks in.
- **People → Learning, Workforce, Records** is an open host service with a
  published language. People publishes a registry interface keyed by the
  person identifier. The other contexts hold only that identifier, never a
  copy of the person.
- **Institutions → Learning, Workforce, Statistics, Operations** is an
  open host service. Other contexts read the institution registry by
  identifier, and occupancy tells them which sites an institution uses.
- **Curriculum → Learning, Assessment** is a customer and supplier
  relationship. Learning and Assessment need programmes, grades and
  subjects, so Curriculum agrees changes with them before releasing them.
- **Learning ↔ Workforce** is a partnership through assignments. A teacher
  teaches a class, and each context owns its own side of that: class
  membership in Learning, the assignment in Workforce. So the two change
  together.
- **Learning, Workforce, Institutions, Assessment → Statistics** is a
  published language. Statistics reads only the counts that each context
  publishes to gold, as at a reference date, together with the semantic
  layer's definitions over them. It never reads their operational
  records.
- **Statistics → international bodies** is a published language too, in
  the formats those bodies define, such as SDMX and the UIS
  questionnaires.
- **Records → every context** is a conformist relationship. Records sets
  the retention, disposal and disclosure rules once, and every context
  applies them unchanged to the records it owns.
- **Other government systems ↔ Workforce, Operations** goes through an
  anti-corruption layer. Exchanges run through declared feeds that
  translate in both directions.
