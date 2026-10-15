# CAP-APPS Application hosting

Product interfaces deployed by CI, behind sign-in, that say which environment they are in.

Layer L3 · domain: data · depends on: [CAP-NETWORK](cap-network.md), [CAP-DELIVERY](cap-delivery.md).

## Purpose

Host product interfaces that are private by default and say which environment they are in.

## Why

A half-switched environment is not partially safe: an application can write to one environment while every label says another. Asking the application which world it believes it is in catches that.

## Interfaces

- A health endpoint reporting target, catalog and schema, database branch and schema version, build version.
- A versioned interface with a pinned snapshot.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-APPS.1 | MUST | Applications sit behind identity-provider sign-in and reach data services privately. | See CAP-NETWORK.1 and CAP-NETWORK.2 for each application host. |
| CAP-APPS.2 | MUST | A health endpoint reports the environment the application believes it is in: target, catalog and schema, database branch and schema version, and build version. | Query the endpoint in each environment; every field matches the environment. |
| CAP-APPS.3 | MUST | Application interfaces are versioned and change additively; a changed shape is a new route. | A pinned interface snapshot is compared in CI; removals fail. |
| CAP-APPS.4 | MUST | Applications are deployed by CI from a versioned image or artefact. | Running versions match a tag; no image is pushed from a workstation. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Azure Container Apps |
| [oss](../implementations/oss.yaml) | Kubernetes Deployment + Gateway API |
<!-- END GENERATED: implementations -->
