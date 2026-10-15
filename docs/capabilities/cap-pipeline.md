# CAP-PIPELINE Retryable pipeline

Content-addressed, deterministic stages that hand off through storage and can retry while the database is down.

Layer L3 · domain: product · depends on: [CAP-ORCHESTRATION](cap-orchestration.md), [CAP-STORAGE](cap-storage.md).

## Purpose

Build processing stages that can be retried, overlapped and re-run without being wrong.

## Why

Delivery is at-least-once; content addressing makes overlap wasteful instead of wrong ([P8](../principles.md#p8-every-write-is-idempotent), [P9](../principles.md#p9-determinism)). Keeping the database out of every stage but one lets the rest retry through a database outage.

## Interfaces

- Storage folders as hand-off points; one job per stage.
- A provenance record per item.

## Notes

A stage that keeps an index in memory must run with concurrency one, or concurrent runs miss matches across each other silently.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-PIPELINE.1 | MUST | An input's identity is the hash of its bytes; duplicates and re-deliveries converge on one record. | Submit the same file twice under different names; one record results. |
| CAP-PIPELINE.2 | MUST | The same input produces byte-identical output; any randomness is seeded per item from a hash of stable keys. | Process a fixed corpus twice; outputs are byte-identical. |
| CAP-PIPELINE.3 | MUST | Each stage is its own job, triggered by the output of the stage before it, so no stage can outrun its predecessor. | The job graph has one job per stage with storage-arrival triggers. |
| CAP-PIPELINE.4 | MUST | Pending work is recomputed from what exists, never consumed from a queue on read, so a failed run strands nothing. | Kill a run mid-way; the next run processes the remainder. |
| CAP-PIPELINE.5 | MUST | Writes are atomic (write to a temporary name, then move), so a reader never sees a partial output. | Code review and a fault-injection test find no partial files. |
| CAP-PIPELINE.6 | MUST | Only the publishing stage connects to the operational database; every other stage can retry while it is unavailable. | With the database unreachable, upstream stages complete. |
| CAP-PIPELINE.7 | MUST | Each item carries a provenance record of every stage that touched it, with versions; a missing stage reads as absent, never invented. | Every published item has a provenance record with a field per stage. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
