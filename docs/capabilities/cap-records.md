# CAP-RECORDS Records lifecycle and data-subject rights

<!-- BEGIN GENERATED: header (just render) -->
Every record has a retention class; archiving, disposal, subject access, rectification and individual disclosure follow declared, audited paths.

Layer L1 · domain: governance · depends on: [CAP-CLASSIFICATION](cap-classification.md), [CAP-MASTERDATA](cap-masterdata.md), [CAP-AUDIT](cap-audit.md).
<!-- END GENERATED: header -->

## Purpose

Keep each record as long as it is needed and no longer, and let people see and correct what is held about them.

## Why

Personal data about children has a lifetime set by law and purpose, not by storage cost. An append-only, branched, backed-up platform keeps copies everywhere unless disposal is designed in. Scheduled disposal is also the one sanctioned exception to [P12](../principles.md#p12-provenance-before-any-drop): real data is never dropped on a guess, and it is removed when its retention ends.

## Interfaces

- A retention schedule in code, by record class.
- A read-only archive for records whose retention trigger has occurred.
- Subject-access, rectification and individual-disclosure requests, each logged.

## Notes

Where history cannot be rewritten (immutable snapshots, backups), encrypt each subject's or partition's data with its own key, and destroy the key at disposal. Set table-history retention, branch lifetimes and backup windows so that none outlives the disposal deadline.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-RECORDS.1 | MUST | A retention schedule in code gives each record class its retention period, trigger event, legal basis and owning role, and every table and file belongs to a record class. | A fitness function finds no table or file without a record class. |
| CAP-RECORDS.2 | MUST | When a record's retention trigger occurs, the record leaves operational use and moves to a read-only archive. | A leaver fixture appears in the archive and is read-only. |
| CAP-RECORDS.3 | MUST | Disposal at the end of retention is a reviewed, audited operation that reaches table history, branches and backups within a stated maximum time; where history cannot be rewritten, per-subject or per-partition keys are destroyed. This is the only path by which real personal data is deleted. | A disposal fixture leaves no readable copy in any store within the stated time; the audit shows the review. |
| CAP-RECORDS.4 | MUST | Any record class kept without limit is listed as such in the schedule, with the reason. | The schedule lists the permanent classes explicitly. |
| CAP-RECORDS.5 | MUST | A subject-access request is answered from the catalog by the person's identifier across all domains, and the answer is reproducible. | Two runs of a subject-access fixture return identical results. |
| CAP-RECORDS.6 | MUST | A rectification is an evented correction that creates a new version, and downstream tables are rebuilt from it. | After a rectification fixture, gold reflects the corrected value and the history shows both. |
| CAP-RECORDS.7 | MUST | Releasing an individual's records to that person, a guardian with verified authority, or an authorised agency is a logged request that records who received what, why, on what basis and how; it is separate from statistical publication, which never releases individual records. | The disclosure register has an entry for each release with all fields. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [ISO/IEC 27701 Privacy information management systems](../standards.md#identity-security-and-privacy) | ISO/IEC 27701:2025, a standalone standard | reference |
| [ISO/IEC 29100 Privacy framework](../standards.md#identity-security-and-privacy) | ISO/IEC 29100:2024 (second edition) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Governed retention tags + Lakeflow Jobs<br/>Delta VACUUM with bounded retention |
| [oss](../implementations/oss.yaml) | Retention policies in table properties + Airflow lifecycle jobs<br/>OpenBao transit keys per partition |
<!-- END GENERATED: implementations -->
