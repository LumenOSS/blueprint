# CAP-ORCHESTRATION Orchestration

<!-- BEGIN GENERATED: header (just render) -->
Declared jobs with bounded runs, safe retries and range re-runs.

Layer L3 · domain: data · depends on: [CAP-COMPUTE](cap-compute.md), [CAP-DELIVERY](cap-delivery.md).
<!-- END GENERATED: header -->

## Purpose

Declared jobs run on schedules and when data arrives, and each run is bounded, so backlogs drain on their own.

## Why

A run with no limit either finishes early or is killed partway through, and neither tells you what the next run will do. Giving each run a budget, plus a final step that re-queues whatever is left, keeps work flowing without anyone triggering it by hand.

## Interfaces

- Job declarations in the product repository.
- Triggers on a schedule, on file arrival and on completion of upstream work.
- Re-runs over a range, with a limit on concurrency.

## Notes

Set the cap for each run from the median time per item you've actually measured, not a configured guess. If the cap is missing, treat the run as uncapped, not as stopped.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-ORCHESTRATION.1 | MUST | Jobs are declared in the product's repository and deployed by CI. | No job exists in an environment without a declaration in a repository. |
| CAP-ORCHESTRATION.2 | MUST | Jobs can be triggered by schedule, by file arrival and by the completion of upstream work. | Each trigger type is exercised by a test job. |
| CAP-ORCHESTRATION.3 | MUST | Each run has a budget. Work beyond the budget is re-triggered by a finishing step that re-queues only if work remains and the run made progress, and a run with nothing to do exits within seconds on the cheapest compute.<br><br>*Example:* A run may process 400 pages in its time budget; with 1,000 waiting, it processes 400 and re-queues itself, and the backlog drains without anyone triggering it. | Feed more work than one budget allows; the backlog drains without manual triggers, and an empty run costs seconds. |
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
