# CAP-GUARDRAILS Guardrails and fitness functions

<!-- BEGIN GENERATED: header (just render) -->
Policy as code on every plan, and scheduled checks that the architecture's properties still hold.

Layer L1 · domain: delivery · depends on: [CAP-DELIVERY](cap-delivery.md).
<!-- END GENERATED: header -->

## Purpose

Changes that don't conform are stopped when they're planned, and drift away from the architecture is caught by regular checks.

## Why

A property that nobody checks decays over time. Fitness functions turn the principles into alarms that go off when something drifts ([P16](../principles.md#p16-open-formats-storage-separate-from-compute-federate-before-copying), [P12](../principles.md#p12-provenance-before-any-drop)).

## Interfaces

- Policy as code, evaluated in the plan stage.
- Scheduled checks, for example that tags are present, that a restore matches by hash, the cost of each task, and that nothing but CI writes state.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-GUARDRAILS.1 | MUST | Policies evaluated on every plan reject public endpoints on data services, missing required tags and names that do not follow the naming module. | A deliberately non-conforming plan in a test change is rejected. |
| CAP-GUARDRAILS.2 | MUST | Scheduled fitness functions check that every table carries provenance and classification tags, that a restore reproduces content hashes, and that cost per task stays within budget, each on a declared schedule. | Each check exists, has run on schedule, and alerts when it fails. |
| CAP-GUARDRAILS.3 | SHOULD | The platform's own repositories and every third-party open-source component are assessed with OpenSSF Scorecard on a schedule, and low scores are reviewed. | Scorecard results are recorded per repository and component, with reviews of low scores. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [ISO/IEC 27001 Information security management systems](../standards.md#identity-security-and-privacy) | ISO/IEC 27001:2022 with Amd 1:2024, and ISO/IEC 27002:2022 | reference |
| [NIST Cybersecurity Framework](../standards.md#identity-security-and-privacy) | CSF 2.0 (February 2024) | reference |
| [OpenSSF Scorecard](../standards.md#open-source-health-and-digital-public-goods) | v5 (5.6.0, October 2026) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Azure Policy<br/>Conftest on tofu plans<br/>Lakeflow Jobs |
| [oss](../implementations/oss.yaml) | OPA Gatekeeper<br/>Conftest<br/>Airflow |
<!-- END GENERATED: implementations -->
