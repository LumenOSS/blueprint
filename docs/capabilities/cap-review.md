# CAP-REVIEW Human review

Low-confidence results go to people, whose decisions are leased, durable and never overwritten by machines.

Layer L3 · domain: product · depends on: [CAP-OPERATIONALDB](cap-operationaldb.md), [CAP-AUDIT](cap-audit.md).

## Purpose

Route uncertain results to people and keep their decisions safe from machines and from each other.

## Why

A low-confidence guess is worse than no answer ([P10](../principles.md#p10-low-confidence-goes-to-a-person-never-guessed)). Mutual exclusion belongs in the database, where one statement can claim an item.

## Interfaces

- A review queue; leases as database keys; typed attribution of decisions.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-REVIEW.1 | MUST | A result below its confidence threshold is routed to review with a reason code; thresholds live in one configuration module. | Grep finds thresholds only in the configuration module; a low-confidence fixture lands in review. |
| CAP-REVIEW.2 | MUST | A reviewer claims an item with a lease held as a database key; claim is one statement, expiry is judged at read time, and a commit requires a live lease checked before its first write. | A race test with concurrent sessions yields exactly one holder. |
| CAP-REVIEW.3 | MUST | A human decision outranks any machine re-delivery or re-run; guards test the condition that would make a write wrong, not a status label. | Re-run the pipeline over a reviewed item; the human decision is unchanged. |
| CAP-REVIEW.4 | MUST | Decisions are reversed by a compensating action that keeps both records; nothing is deleted. | Undo a decision; both the decision and its reversal are present. |
| CAP-REVIEW.5 | MUST | Each decision records its kind of attribution (automatic, affirmed, corrected, backfilled) so reporting can tell who or what decided. | Reporting groups decisions by attribution. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | The example product's review service on Lakebase |
| [oss](../implementations/oss.yaml) | The example product's review service on Postgres |
<!-- END GENERATED: implementations -->
