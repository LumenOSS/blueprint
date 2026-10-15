# CAP-GUARDRAILS Guardrails and fitness functions

Policy as code on every plan, and scheduled checks that the architecture's properties still hold.

Layer L1 · domain: delivery · depends on: [CAP-DELIVERY](cap-delivery.md).

## Purpose

Stop non-conforming changes at plan time and catch drift from the architecture on a schedule.

## Why

A property that is not checked decays. Fitness functions turn the principles into alarms ([P16](../principles.md#p16-open-formats-storage-separate-from-compute-federate-before-copying), [P12](../principles.md#p12-provenance-before-any-drop)).

## Interfaces

- Policy-as-code evaluated in the plan stage.
- Scheduled checks: tags present, restore by hash, cost per task, no non-CI writer of state.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-GUARDRAILS.1 | MUST | Policies evaluated on every plan reject public endpoints on data services, missing required tags and names that do not follow the naming module. | A deliberately non-conforming plan in a test change is rejected. |
| CAP-GUARDRAILS.2 | MUST | Scheduled fitness functions check that every table carries provenance and classification tags (daily), that a restore reproduces content hashes (quarterly), and that cost per task stays within budget (monthly). | Each check exists, has run on schedule, and alerts when it fails. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
