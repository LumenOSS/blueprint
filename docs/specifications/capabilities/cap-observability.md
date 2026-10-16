# CAP-OBSERVABILITY Operational telemetry

<!-- BEGIN GENERATED: header (just render) -->
Per-item metrics, freshness and cost, reaching gold so cost can be told apart from work.

Layer L1 · domain: data
<!-- END GENERATED: header -->

## Purpose

The platform measures the work done on each item, how fresh the data is, and what it costs, so you can tell a rise in spending from a rise in work.

## Why

If a run crashes partway through an item, nothing is recorded unless the record was written first. And a process's status can say it's running when the work has actually hung.

## Interfaces

- Metrics for each item, whose status is crashed by default.
- Heartbeats, and the cost of each task in gold.

## Notes

Cap runs by wall time, but compare them by core time, because wall time changes with the topology.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-OBSERVABILITY.1 | MUST | Work records metrics per item, starting with a status of crashed that is overwritten on success, so a crashed item is never silently missing. | Kill a run mid-item; the item's metric reads crashed. |
| CAP-OBSERVABILITY.2 | MUST | Cost is attributable to the task that caused it, and reaches gold beside throughput. | A gold model reports cost per task per period with item counts. |
| CAP-OBSERVABILITY.3 | MUST | Health is judged from heartbeats and fresh output, not from process status. | A hung process with a live status is detected by its stale heartbeat. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | System tables<br/>Azure Monitor / Log Analytics |
| [oss](../implementations/oss.yaml) | OpenTelemetry Collector<br/>Prometheus<br/>Grafana + Loki |
<!-- END GENERATED: implementations -->
