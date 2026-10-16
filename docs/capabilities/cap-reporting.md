# CAP-REPORTING Reporting

<!-- BEGIN GENERATED: header (just render) -->
Dashboards and natural-language query over the semantic layer, deployed as code.

Layer L3 · domain: data · depends on: [CAP-SEMANTICS](cap-semantics.md).
<!-- END GENERATED: header -->

## Purpose

Show governed numbers to people, each seeing only what they may see.

## Why

Dashboards are code so they move between environments without hand edits; environment literals in a dashboard make it report another environment's numbers.

## Interfaces

- Dashboards as code, rendered per environment.
- Natural-language query over the semantic layer.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-REPORTING.1 | MUST | Dashboards are deployed as code, rendered per environment from the deployment tool's resolved output. | Each dashboard's source is in a repository; no environment-specific literal is in it. |
| CAP-REPORTING.2 | MUST | A dashboard shows each viewer only the rows and columns that viewer may see, or runs as a declared identity whose access is the dashboard's audience. | Open a dashboard as two scoped users; each sees their own scope. |
| CAP-REPORTING.3 | SHOULD | Natural-language query is offered over the semantic layer, showing the query it ran. | Every answer displays its generated query. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [Unicode CLDR](../standards.md#accessibility-and-localisation) | CLDR 48.2 (March 2026) | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | AI/BI dashboards<br/>Genie |
| [oss](../implementations/oss.yaml) | Apache Superset |
<!-- END GENERATED: implementations -->
