# CAP-NETWORK Network isolation

Data services are private; only applications are exposed, behind sign-in.

Layer L1 · domain: delivery

## Purpose

Keep data services off the public network and expose only applications, behind sign-in.

## Why

Identity is the door; the private network is the floor. Either alone leaves a path open.

## Interfaces

- Private endpoints or in-cluster services for storage, catalog data paths, databases and secrets.
- A gateway with identity-provider sign-in in front of every application.
- Default-deny policies between workloads; one egress point.

## Notes

Record who owns private DNS and any hub network before building, because both are often outside the platform team's control.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-NETWORK.1 | MUST | Storage, catalog data paths, databases and secret stores are reachable only on private network paths. | A policy check on every plan fails a public endpoint on a data service; an external probe of each endpoint fails. |
| CAP-NETWORK.2 | MUST | Only applications are exposed, and only through a gateway that requires identity-provider sign-in. | An unauthenticated request to each public host is redirected to sign-in or refused. |
| CAP-NETWORK.3 | MUST | Traffic is denied by default between workloads; each allowed path is declared. | A workload with no declared path cannot reach a data service. |
| CAP-NETWORK.4 | SHOULD | Outbound traffic leaves through one controlled egress point. | Route tables send internet-bound traffic through the egress point only. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | VNet injection + secure cluster connectivity<br/>Private Link (front end and back end)<br/>Network connectivity configurations<br/>NAT gateway |
| [oss](../implementations/oss.yaml) | Cilium<br/>Gateway API + oauth2-proxy |
<!-- END GENERATED: implementations -->
