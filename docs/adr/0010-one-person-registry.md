# ADR-0010: Record each person once; roles are relationships

**Status:** accepted. **Date:** 2026-10-15.

## Context

The same human being often appears in an education system in more than
one role: a teacher is also a guardian of a learner; a former learner
becomes a member of staff; a guardian of one child is a staff member at
another institution. Modelling learners, staff and guardians as separate
registries records that person several times, with separate identifiers,
separate external identifiers and separate corrections, and makes it
impossible to answer a subject-access request completely or to apply one
retention decision to one person.

## Decision

- A single person registry, owned by the `people` domain, holds each
  person once with their identity attributes; their external identifiers
  sit beside it in a more sensitive table.
- *Learner*, *staff member* and *guardian* are roles held through
  relationships: enrolment, posting and guardian relationship, owned by
  the `learners` and `workforce` domains.
- A guardian may also be a body with legal authority (for example a
  child-protection agency), which is recorded as an organisation, not a
  person.

## Consequences

- Duplicate detection, merging and verification run once per person, not
  once per role ([CAP-MASTERDATA](../specifications/capabilities/cap-masterdata.md)).
- A subject-access request or a disposal reaches every role a person has
  held ([CAP-RECORDS](../specifications/capabilities/cap-records.md)).
- Access rules must not leak across roles: being a staff member grants
  nothing about one's own children's records except through the guardian
  relationship, and the reverse.
- The `people` domain is the most sensitive registry in the platform and
  is classified accordingly.
