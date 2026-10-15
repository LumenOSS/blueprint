# CAP-STATE Infrastructure state

Remote, locked, versioned and encrypted state for every stack, readable only by the identities that own it.

Layer L0 · domain: delivery · depends on: [CAP-MODULES](cap-modules.md).

## Purpose

Keep the record of what infrastructure exists safe, locked and recoverable, and readable only by the layer that owns it.

## Why

Lost or overwritten state turns the next apply into a recreation. Reading another stack's state exposes its whole snapshot, so stacks find each other by deterministic name instead ([P2](../principles.md#p2-repositories-are-split-by-trust-state-is-split-by-blast-radius)).

## Interfaces

- Backend: an object store with locking, versioning and identity-based access.
- One key per stack and environment; product state in a location product identities alone can reach.
- A bootstrap recipe that creates the store from nothing and proves it with a write, read, compare, delete probe.

## Notes

Keep state apart from lake storage: object versioning protects state but can break table maintenance on a lake store. The two need different protections, so they live in different accounts or buckets.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-STATE.1 | MUST | State is remote, one state per stack per environment, with a lock that blocks a concurrent apply. | Start two plans against one stack; the second waits or fails on the lock. |
| CAP-STATE.2 | MUST | Every state version is recoverable after an overwrite or deletion. | Restore drill: overwrite a test stack's state, recover the prior version, and plan shows no changes. |
| CAP-STATE.3 | MUST | State is encrypted at rest with a key under the platform's control and is reached by identity, never by a shared access key. | Shared-key access to the store is disabled; the encryption key is in the platform's key store. |
| CAP-STATE.4 | MUST | A product's identity cannot read platform or bootstrap state. | Negative test: a read of platform state with a product identity is denied. |
| CAP-STATE.5 | MUST | The state store can be created from an empty account by the bootstrap layer, and its reachability is proven by write, read, compare and delete before first use. | The bootstrap recipe runs against an empty account and its probe reports success. |
| CAP-STATE.6 | MUST | Stacks find each other's resources by deterministic name, not by reading each other's state. | No stack declares a remote-state data source. |
| CAP-STATE.7 | MUST | A stack that moves between repositories keeps its state key, and its first plan in the new place shows no changes. | The move's review includes a no-change plan. |
| CAP-STATE.8 | SHOULD | State lives apart from lake storage, because the protections each needs (object versioning, lifecycle rules) conflict. | The state store is a separate account or bucket from every lake store. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | OpenTofu<br/>azurerm backend<br/>Azure Key Vault |
| [oss](../implementations/oss.yaml) | OpenTofu<br/>S3 backend on Ceph RGW<br/>OpenBao transit |
<!-- END GENERATED: implementations -->
