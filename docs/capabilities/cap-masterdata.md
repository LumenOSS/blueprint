# CAP-MASTERDATA Master data and identifiers

<!-- BEGIN GENERATED: header (just render) -->
One authoritative registry per core resource, with permanent opaque identifiers and governed duplicate resolution.

Layer L1 · domain: data · depends on: [CAP-CATALOG](cap-catalog.md), [CAP-OPERATIONALDB](cap-operationaldb.md).
<!-- END GENERATED: header -->

## Purpose

Keep one authoritative record of each institution, person and post, with an identifier that never changes and never means anything.

## Why

Every EMIS indicator counts people and institutions, so a duplicated learner or a mis-keyed school is a wrong number everywhere it is used. An identifier that carries meaning breaks when the meaning changes, and copies whatever it carries into every table that references it. An opaque identifier minted once avoids both. Duplicate resolution reuses the review pattern: suspected duplicates are sets that a person decides, and a merge is reversible ([P8](../principles.md#p8-every-write-is-idempotent), [P10](../principles.md#p10-low-confidence-goes-to-a-person-never-guessed)).

## Interfaces

- Registries for institutions (and their sites), people (learners, guardians, staff) and posts.
- A separate, more sensitive table of identifiers issued by other authorities.
- Adapters to external authoritative registers, recording each verification outcome.
- A duplicate-review queue whose decisions are merges with redirects.

## Notes

Keep the post (an established position) apart from the person who fills it, and the enrolment apart from the learner; most workforce and participation indicators depend on those relationships, not on the people alone. See the [domain model](../domain/README.md).

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-MASTERDATA.1 | MUST | Each core resource (institution, site, person, post) has one authoritative registry with one owning steward; other domains reference it by identifier and never copy it. | Every reference to a core resource is a foreign key to its registry. |
| CAP-MASTERDATA.2 | MUST | Identifiers are opaque, permanent surrogates minted by one authority, never reused, and carry no meaning about the thing they identify. | The identifier pattern is declared and tested; no part of an identifier can be decoded into an attribute. |
| CAP-MASTERDATA.3 | MUST | Identifiers issued by other authorities are attributes in a separate identifier table with type, issuer and validity, classified at least T3, and never used as keys or carried into gold or shared tables. | No gold or shared table has an external-identifier column. |
| CAP-MASTERDATA.4 | MUST | A learner keeps one identifier across institutions, levels and years; the institution belongs to the enrolment, not to the identifier. | A transfer fixture keeps the learner's identifier. |
| CAP-MASTERDATA.5 | MUST | Duplicate detection is deterministic and explainable; uncertain matches go to a person; a merge keeps a surviving identifier and a redirect from each retired one, is audited, and can be reversed. Nothing is deleted. | A merge and unmerge fixture round-trips; references to a retired identifier resolve to the survivor. |
| CAP-MASTERDATA.6 | MUST | Verification against an external authoritative register goes through an adapter, and its outcome (verified, unverified or mismatch, with date and method) is recorded per record, never inferred. | Each verified record carries an outcome, date and method. |
| CAP-MASTERDATA.7 | MUST | Changes to an institution (renaming, merger, split, closure, change of ownership) are effective-dated events that keep its history. | A merger fixture leaves both histories queryable. |
| CAP-MASTERDATA.8 | MUST | A status that ends a person's participation (deceased, left the system) stops outreach and relationship-based access without deleting history. | A fixture with that status receives no notices and grants no guardian access. |
| CAP-MASTERDATA.9 | SHOULD | Identifiers that people transcribe by hand carry a check digit. | The identifier generator and validator implement the check digit. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [Unicode Standard and normalization (UAX 15)](../standards.md#data-representation) | Unicode 18.0.0 (2026) | adopt |
| [RFC 9562 Universally Unique IDentifiers](../standards.md#data-representation) | RFC 9562 (May 2024), obsoleting RFC 4122 | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Registry services on Lakebase<br/>Splink on Spark |
| [oss](../implementations/oss.yaml) | Registry services on PostgreSQL (CloudNativePG)<br/>Splink |
<!-- END GENERATED: implementations -->
