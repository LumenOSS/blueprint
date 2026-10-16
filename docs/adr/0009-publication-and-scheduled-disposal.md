# ADR-0009: Separate open publication from sharing, and allow scheduled disposal

**Status:** accepted. **Date:** 2026-10-15.

## Context

Two rules from the first version were too narrow for an education system.

- **Sharing.** The blueprint allowed data to leave only through approved,
  authenticated shares of de-identified tables. Education statistics are
  also expected to be public: anyone should be able to read aggregate
  figures, at fine levels of detail, without signing in, from a permanent
  address. And individuals have a right to their own records.
- **Deletion.** The provenance rule (P12) made dropping real data
  deliberately hard. Data-protection law makes deleting personal data at
  the end of its retention period an obligation.

## Decision

- Three channels, each with its own controls:
  1. **Open publication** of T0 aggregates, readable without signing in,
     with disclosure control, permanent identifiers and open metadata
     ([CAP-PUBLICATION](../specifications/capabilities/cap-publication.md)).
  2. **Partner sharing** of de-identified row-level tables, authenticated
     and approved per recipient ([CAP-SHARING](../specifications/capabilities/cap-sharing.md)).
  3. **Individual disclosure** of a person's own records to that person,
     their guardian or an authorised agency, logged and purpose-bound
     ([CAP-RECORDS.7](../specifications/capabilities/cap-records.md)).
- **Scheduled disposal** is the one path by which real personal data is
  deleted: reviewed, audited, and reaching history, branches and backups
  within a stated time ([CAP-RECORDS.3](../specifications/capabilities/cap-records.md)).
  P12 and P15 are restated to say so.

## Consequences

- Publication needs disclosure tests that include secondary suppression,
  because totals can reveal a suppressed cell.
- Append-only history, branches and backups must be designed around a
  disposal deadline; where history cannot be rewritten, data is encrypted
  per subject or partition so that destroying a key disposes of it.
