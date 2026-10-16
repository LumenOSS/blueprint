# CAP-STATE Infrastructure state

<!-- BEGIN GENERATED: header (just render) -->
Remote, locked, versioned and encrypted state for every stack, readable only by the identities that own it.

Layer L0 · domain: delivery · depends on: [CAP-MODULES](cap-modules.md).
<!-- END GENERATED: header -->

## Purpose

The record of what infrastructure exists is kept safe, locked and recoverable, and only the layer that owns it can read it.

## Why

If state is lost or overwritten, the next apply tries to create everything again. Reading another stack's state exposes its whole snapshot, so stacks find each other by deterministic names instead ([P2](../principles.md#p2-repositories-are-split-by-trust-state-is-split-by-blast-radius)).

## Interfaces

- A backend, which is an object store with locking, versioning and access by identity.
- One key for each stack and environment, with product state kept in a location that only product identities can reach.
- A bootstrap recipe that creates the store from nothing and proves it works by writing, reading, comparing and deleting a probe.

## Notes

Keep state apart from lake storage. Object versioning protects state, but it can break table maintenance on a lake store. The two need different protection, so they live in different accounts or buckets.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-STATE.1 | MUST | State is remote, one state per stack per environment, with a lock that blocks a concurrent apply. | Start two plans against one stack; the second waits or fails on the lock. |
| CAP-STATE.2 | MUST | Every state version is recoverable after an overwrite or deletion. | Restore drill: overwrite a test stack's state, recover the prior version, and plan shows no changes. |
| CAP-STATE.3 | MUST | State is encrypted at rest with a key under the platform's control and is reached by identity, never by a shared access key. | Shared-key access to the store is disabled; the encryption key is in the platform's key store. |
| CAP-STATE.4 | MUST | A product's identity cannot read platform or bootstrap state. | Negative test: a read of platform state with a product identity is denied. |
| CAP-STATE.5 | MUST | The state store can be created from an empty account by the bootstrap layer, and its reachability is proven by write, read, compare and delete before first use. | The bootstrap recipe runs against an empty account and its probe reports success. |
| CAP-STATE.6 | MUST | Stacks find each other's resources by deterministic name, not by reading each other's state.<br><br>*Example:* The platform stack finds the state store by the name the naming module derives for it, instead of reading the bootstrap stack's state to learn it. | No stack declares a remote-state data source. |
| CAP-STATE.7 | MUST | A stack that moves between repositories keeps its state key, and its first plan in the new place shows no changes. | The move's review includes a no-change plan. |
| CAP-STATE.8 | SHOULD | State lives apart from lake storage, because the protections each needs (object versioning, lifecycle rules) conflict. | The state store is a separate account or bucket from every lake store. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
No external standard is named for this capability.
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | OpenTofu<br/>azurerm backend<br/>Azure Key Vault |
| [oss](../implementations/oss.yaml) | OpenTofu<br/>S3 backend on Ceph RGW<br/>OpenBao transit |
<!-- END GENERATED: implementations -->
