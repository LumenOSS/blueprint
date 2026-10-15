# CAP-MODULES Versioned modules

Shared building blocks consumed by immutable version, including deterministic naming.

Layer L2 · domain: delivery

## Purpose

Share building blocks across repositories without sharing state or identity, and make names predictable.

## Why

Deterministic names let stacks find each other without reading state ([CAP-STATE.6](cap-state.md)). Pinning by tag means a module change reaches a stack only through that stack's own reviewed change.

## Interfaces

- Module sources pinned by tag or digest.
- A naming module: `<type>-<project>-<environment>-<region>-<instance>`, with a compact form where a resource forbids hyphens, plus the standard tag set.

## Notes

Many resource names cannot change after creation. Treat any change to a name output as breaking.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-MODULES.1 | MUST | Modules are consumed by an immutable version reference, never a branch. | Every module source pins a tag or digest. |
| CAP-MODULES.2 | MUST | A naming module derives every resource name and tag set deterministically from type, project, environment, region and instance. | The module's tests assert the same inputs give the same names. |
| CAP-MODULES.3 | SHOULD | Module versions follow semantic versioning; a change to any output that alters a resource name is a major version. | The module's changelog marks name changes as breaking. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
