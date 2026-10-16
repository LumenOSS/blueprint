# Data in an EMIS

An EMIS holds many kinds of data, and we don't handle them all the same
way. This page names the main kinds, and then introduces five ideas about
handling data that the rest of the blueprint builds on. Think of it as a
primer. The specifications explain each idea properly, and you'll find a
link to them at the end of each section.

## The main kinds of data

| Kind | Examples | Who it is about |
| --- | --- | --- |
| Registries | People, institutions, sites, posts | Each person, institution or post, once |
| Records about individuals | Enrolments, attendance, results, support plans, postings | One learner or staff member |
| Returns and statistics | Census returns, snapshots, indicators | Groups, as counts and rates rather than individuals |
| Reference data | Code lists, administrative areas, academic calendars, population estimates | Nobody, because these are shared definitions |
| Operations | Budgets, assets, entitlement schemes such as school meals, incidents | Institutions, and sometimes individuals |

Most of this data is about children, and that one fact shapes the five
ideas below.

## 1. Some data is sensitive

Not all data needs the same care. A published count of schools in each
district harms nobody. A learner's name and address need protecting. A
learner's health condition, or a child-protection record, needs the most
protection of all, and the law usually says so.

So we give every table a **sensitivity tier**, on a scale that runs from
public statistics to special-category personal data. Everything else
follows from that tier: who may see the table, where it's stored, and
whether it may leave the platform. You'll find the tiers listed in
[terminology](terminology.md#sensitivity-tiers).

To go further, read [CAP-CLASSIFICATION](../specifications/capabilities/cap-classification.md).

## 2. Show less than the whole

Most people who use EMIS data don't need to know who each person is. A
planner needs counts, and an analyst needs patterns. So wherever it can,
the platform shows less than the whole record. It has three main ways of
doing that:

- **Masking** hides the value in a column from people who don't need it.
  For example, it might show a birth year instead of a full birth date.
- **Pseudonymisation** replaces a name or a national number with an
  identifier that nobody can trace back to the person without a key, and
  that key is protected separately.
- **Aggregation with suppression** publishes counts, but hides any count
  so small that it could identify someone.

NIST describes these techniques in
[*De-Identifying Government Datasets*](https://csrc.nist.gov/pubs/sp/800/188/final)
(SP 800-188, 2023).

To go further, read [CAP-ACCESS](../specifications/capabilities/cap-access.md)
and [CAP-PUBLICATION](../specifications/capabilities/cap-publication.md).

## 3. Who can see what: roles and attributes

There are two well-known models for deciding who can access what, and an
EMIS needs both of them.

- **Role-based access control (RBAC)** grants permissions to roles, and
  people hold roles. Analysts may run queries, for instance, and stewards
  may approve access. RBAC answers the question *what kind of thing may
  this person do?*
  ([NIST, RBAC](https://csrc.nist.gov/projects/role-based-access-control)).
- **Attribute-based access control (ABAC)** decides from attributes of the
  person, the data and the request, such as where the person works, how
  sensitive a column is, and what the request is for. ABAC answers the
  question *which rows and columns?*
  ([NIST SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)).

Here's how they work together. A district officer holds the analyst role,
so they may query enrolment; that's RBAC. They're posted to District B,
and that posting is an attribute, so they see only District B's learners;
that's ABAC. And the health column is masked for them because of its
sensitivity tier, which is ABAC again.

To go further, read [principle P14](../specifications/principles.md#p14-access-is-role--scope--sensitivity)
and [CAP-ACCESS](../specifications/capabilities/cap-access.md).

## 4. Share by publishing, not by copying

An EMIS shares data with other parts of government, with researchers and
with the public. But every copy that leaves the platform is a copy that
nobody can correct, delete on schedule, or audit. So the blueprint
prefers to **publish**. It publishes aggregate statistics openly, and it
gives named partners governed access to de-identified data, under an
agreement and for a declared purpose. Raw exports of personal data are
the exception, and when they happen, they're recorded.

To go further, read [principle P15](../specifications/principles.md#p15-publish-never-export)
and [CAP-SHARING](../specifications/capabilities/cap-sharing.md).

## 5. Know where every number came from

**Lineage** is the record of where data came from and what was done to
it. For example, it might tell you that an indicator was computed from a
particular snapshot, which counted certain returns, which in turn were
loaded from certain files. Lineage is what lets you:

- trust a published figure, because you can trace it back to its source;
- find everything that's affected when a source is corrected;
- delete a person's data everywhere it went, when the law requires it.

The platform captures lineage automatically as data moves, using the open
[OpenLineage](https://openlineage.io/) standard. Nobody has to write it
down by hand afterwards.

To go further, read [CAP-LINEAGE](../specifications/capabilities/cap-lineage.md).

## Keep in mind

As you read the specifications, you'll find the same five questions
coming up again and again:

1. How sensitive is this data?
2. Does this person need the whole record, or less?
3. Which role, and which attributes, allow this access?
4. Can it be published instead of copied?
5. Could we trace this number back to its source?

Next: [terminology](terminology.md).
