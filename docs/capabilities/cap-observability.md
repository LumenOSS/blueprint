# CAP-OBSERVABILITY Operational telemetry

Per-item metrics, freshness and cost, reaching gold so cost can be told apart from work.

Layer L1 · domain: data

## Purpose

Measure work per item, freshness and cost, so a rise in spend can be told apart from a rise in work.

## Why

A run that crashes mid-item leaves no record unless the record is written first. Process status lies about hung work.

## Interfaces

- Per-item metrics with a default status of crashed.
- Heartbeats; cost per task in gold.

## Notes

Cap on wall time but compare on core time, because wall time moves with topology.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-OBSERVABILITY.1 | MUST | Work records metrics per item, starting with a status of crashed that is overwritten on success, so a crashed item is never silently missing. | Kill a run mid-item; the item's metric reads crashed. |
| CAP-OBSERVABILITY.2 | MUST | Cost is attributable to the task that caused it, and reaches gold beside throughput. | A gold model reports cost per task per period with item counts. |
| CAP-OBSERVABILITY.3 | MUST | Health is judged from heartbeats and fresh output, not from process status. | A hung process with a live status is detected by its stale heartbeat. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | System tables<br/>Azure Monitor / Log Analytics |
| [oss](../implementations/oss.yaml) | OpenTelemetry Collector<br/>Prometheus<br/>Grafana + Loki |
<!-- END GENERATED: implementations -->
