# Context map

The EMIS domain is divided into bounded contexts. Each has its own
language, one owning steward and its own catalogs, and talks to the
others only through published interfaces. How the contexts are designed
(subdomains, aggregates, invariants and events) is in
[domain design](docs/specifications/domain/design.md). Terms about the blueprint
and the platform itself are in [glossary](docs/specifications/glossary.md).

## Contexts

- [Reference](docs/specifications/domain/contexts/reference/CONTEXT.md): the shared kernel of time, codes, geography and registries
- [People](docs/specifications/domain/contexts/people/CONTEXT.md): each person recorded once, whatever roles they hold
- [Institutions](docs/specifications/domain/contexts/institutions/CONTEXT.md): institutions, the sites they occupy and the state of those sites
- [Learning](docs/specifications/domain/contexts/learning/CONTEXT.md): enrolment, class membership, attendance, progression and guardianship
- [Workforce](docs/specifications/domain/contexts/workforce/CONTEXT.md): posts and the staff posted to them
- [Curriculum](docs/specifications/domain/contexts/curriculum/CONTEXT.md): programmes, grades, subjects and classes
- [Assessment](docs/specifications/domain/contexts/assessment/CONTEXT.md): tests and examinations, candidates and results
- [Statistics](docs/specifications/domain/contexts/statistics/CONTEXT.md): collections, returns, snapshots, indicators and publication
- [Records](docs/specifications/domain/contexts/records/CONTEXT.md): retention, disposal, correction and individual disclosure
- [Operations](docs/specifications/domain/contexts/operations/CONTEXT.md): budgets, assets, entitlement schemes and safety

## Relationships

- **Reference → every context**: shared kernel. Code lists, academic
  periods, reference dates and administrative areas are used unchanged by
  all contexts; a change to them is reviewed by every steward.
- **External registers → People**: anti-corruption layer. Civil and other
  registers are read through an adapter that translates their identifiers
  and outcomes into People's language; their model never leaks in.
- **People → Learning, Workforce, Records**: open host service with a
  published language. People publishes a registry interface keyed by the
  person identifier; the other contexts hold only that identifier, never a
  copy of the person.
- **Institutions → Learning, Workforce, Statistics, Operations**: open host
  service. The institution registry is read by identifier; occupancy tells
  other contexts which sites an institution uses.
- **Curriculum → Learning, Assessment**: customer and supplier. Learning
  and Assessment need programmes, grades and subjects; Curriculum agrees
  changes with them before releasing them.
- **Learning ↔ Workforce**: partnership through assignments. A class is
  taught by a teacher; each context owns its own side (class membership,
  assignment) and they change together.
- **Learning, Workforce, Institutions, Assessment → Statistics**: published
  language. Statistics reads only the counts each context publishes to
  gold, as at a reference date, and the semantic layer's definitions over
  them; it never reads their operational records.
- **Statistics → international bodies**: published language, in the
  formats those bodies define (for example SDMX and the UIS
  questionnaires).
- **Records → every context**: conformist policies. Retention, disposal
  and disclosure rules are set once by Records and applied unchanged by
  every context to the records it owns.
- **Other government systems ↔ Workforce, Operations**: anti-corruption
  layer. Exchanges run through declared feeds that translate both ways.
