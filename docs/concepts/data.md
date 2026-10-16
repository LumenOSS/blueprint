# Data in an EMIS

An EMIS holds many kinds of data, and they are not all handled the same
way. This page names the main kinds, then introduces five ideas about
handling data that the rest of the blueprint builds on. It is a primer:
each idea is explained properly in the specifications, linked at the end
of each section.

## The main kinds of data

| Kind | Examples | Who it is about |
| --- | --- | --- |
| Registries | People, institutions, sites, posts | Each person, institution or post, once |
| Records about individuals | Enrolments, attendance, results, support plans, postings | One learner or staff member |
| Returns and statistics | Census returns, snapshots, indicators | Groups: counts and rates, not individuals |
| Reference data | Code lists, administrative areas, academic calendars, population estimates | Nobody: shared definitions |
| Operations | Budgets, assets, entitlement schemes such as school meals, incidents | Institutions, and sometimes individuals |

Most of the data is about children. That one fact shapes the five ideas
below.

## 1. Some data is sensitive

Not all data needs the same care. A published count of schools per
district harms nobody; a learner's name and address needs protection; a
learner's health condition or a child-protection record needs the most
protection of all, and the law usually says so.

So every table is given a **sensitivity tier**, from public statistics to
special-category personal data, and everything else (who may see it,
where it is stored, whether it may leave the platform) follows from that
tier. The tiers are listed in [terminology](terminology.md#sensitivity-tiers).

In the specifications: [CAP-CLASSIFICATION](../specifications/capabilities/cap-classification.md).

## 2. Show less than the whole

Most people who use EMIS data do not need to know who each person is. A
planner needs counts; an analyst needs patterns. So the platform shows
less than the whole record wherever it can:

- **Masking** hides a column's value from people who do not need it, such
  as showing a birth year instead of a birth date.
- **Pseudonymisation** replaces a name or national number with an
  identifier that cannot be traced back without a separately protected
  key.
- **Aggregation with suppression** publishes counts, and hides counts so
  small that they could identify someone.

These techniques are described in NIST's
[*De-Identifying Government Datasets*](https://csrc.nist.gov/pubs/sp/800/188/final)
(SP 800-188, 2023).

In the specifications: [CAP-ACCESS](../specifications/capabilities/cap-access.md)
and [CAP-PUBLICATION](../specifications/capabilities/cap-publication.md).

## 3. Who can see what: roles and attributes

Two well-known models decide access, and an EMIS needs both.

- **Role-based access control (RBAC)** grants permissions to roles, and
  people hold roles: analysts may query, stewards may approve. It answers
  *what kind of thing may this person do?*
  ([NIST, RBAC](https://csrc.nist.gov/projects/role-based-access-control)).
- **Attribute-based access control (ABAC)** decides from attributes of the
  person, the data and the request: where the person works, how sensitive
  the column is, what the request is for. It answers *which rows and
  columns?*
  ([NIST SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)).

For example, a district officer holds the analyst role (RBAC), so they
may query enrolment; their posting to District B is an attribute, so they
see only District B's learners (ABAC); and the health column is masked
for them because of its sensitivity tier (ABAC again).

In the specifications: [principle P14](../specifications/principles.md#p14-access-is-role--scope--sensitivity)
and [CAP-ACCESS](../specifications/capabilities/cap-access.md).

## 4. Share by publishing, not by copying

Data is shared with other parts of government, with researchers and with
the public. Each copy that leaves the platform is a copy nobody can
correct, delete on schedule or audit. So the blueprint prefers to
**publish**: aggregate statistics openly, and governed access to
de-identified data for named partners, under an agreement and for a
declared purpose. Raw exports of personal data are the exception, and
they are recorded.

In the specifications: [principle P15](../specifications/principles.md#p15-publish-never-export)
and [CAP-SHARING](../specifications/capabilities/cap-sharing.md).

## 5. Know where every number came from

**Lineage** is the record of where data came from and what was done to
it: this indicator was computed from this snapshot, which counted these
returns, which were loaded from these files. Lineage is how you:

- trust a published figure, because you can trace it to its source;
- find everything affected when a source is corrected;
- delete a person's data everywhere it went, when the law requires it.

Lineage is captured automatically as data moves, using the open
[OpenLineage](https://openlineage.io/) standard, rather than written
down by hand afterwards.

In the specifications: [CAP-LINEAGE](../specifications/capabilities/cap-lineage.md).

## Keep in mind

As you read the specifications, these five questions recur:

1. How sensitive is this data?
2. Does this person need the whole record, or less?
3. Which role, and which attributes, allow this access?
4. Can it be published instead of copied?
5. Could we trace this number back to its source?

Next: [terminology](terminology.md).
