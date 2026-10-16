# CAP-ORCHESTRATION Orchestration

Declared jobs with bounded runs, safe retries and range re-runs.

Layer L3 · domain: data · depends on: [CAP-COMPUTE](cap-compute.md), [CAP-DELIVERY](cap-delivery.md).

## Purpose

Run declared jobs on schedules and arrivals, with bounded runs that drain backlogs on their own.

## Why

Unbounded runs either finish early or are killed mid-flight, and neither predicts the next. A budget plus a finishing step that re-queues remaining work keeps throughput without manual triggers.

## Interfaces

- Job declarations in the product repository.
- Schedule, file-arrival and upstream-completion triggers.
- Range re-runs with a concurrency limit.

## Notes

Size the per-run cap from a measured median item time, not a configured one, and treat a missing cap as uncapped rather than stopped.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-ORCHESTRATION.1 | MUST | Jobs are declared in the product's repository and deployed by CI. | No job exists in an environment without a declaration in a repository. |
| CAP-ORCHESTRATION.2 | MUST | Jobs can be triggered by schedule, by file arrival and by the completion of upstream work. | Each trigger type is exercised by a test job. |
| CAP-ORCHESTRATION.3 | MUST | Each run has a budget. Work beyond the budget is re-triggered by a finishing step that re-queues only if work remains and the run made progress, and a run with nothing to do exits within seconds on the cheapest compute. | Feed more work than one budget allows; the backlog drains without manual triggers, and an empty run costs seconds. |
| CAP-ORCHESTRATION.4 | MUST | Retries are safe because every task is idempotent; the orchestrator also rejects a duplicate run identifier. | Re-run a completed task; outputs are byte-identical. |
| CAP-ORCHESTRATION.5 | MUST | A job can be re-run for a declared range of partitions, with a limit on concurrent runs. | Run a range backfill; only the declared partitions change. |
| CAP-ORCHESTRATION.6 | MUST | Alerts fire on data freshness, not only on job failure. | Stop an upstream source; a freshness alert fires within its window. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Lakeflow Jobs |
| [oss](../implementations/oss.yaml) | Apache Airflow 3 |
<!-- END GENERATED: implementations -->
