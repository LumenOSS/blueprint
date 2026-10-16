# CAP-MODULES Versioned modules

<!-- BEGIN GENERATED: header (just render) -->
Shared building blocks consumed by immutable version, including deterministic naming.

Layer L2 · domain: delivery
<!-- END GENERATED: header -->

## Purpose

Repositories share building blocks without sharing state or identity, and names are predictable.

## Why

Because names are deterministic, stacks can find each other without reading each other's state ([CAP-STATE.6](cap-state.md)). Because modules are pinned by tag, a change to a module only reaches a stack through that stack's own reviewed change.

## Interfaces

- Module sources pinned by tag or digest.
- A naming module that produces `<type>-<project>-<environment>-<region>-<instance>`, with a compact form for resources that don't allow hyphens, along with the standard set of tags.

## Notes

Many resource names can't be changed once the resource exists, so treat any change to a name the module produces as a breaking change.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-MODULES.1 | MUST | Modules are consumed by an immutable version reference, never a branch. | Every module source pins a tag or digest. |
| CAP-MODULES.2 | MUST | A naming module derives every resource name and tag set deterministically from type, project, environment, region and instance. | The module's tests assert the same inputs give the same names. |
| CAP-MODULES.3 | SHOULD | Module versions follow semantic versioning; a change to any output that alters a resource name is a major version. | The module's changelog marks name changes as breaking. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [OpenSSF Scorecard](../standards.md#open-source-health-and-digital-public-goods) | v5 (5.6.0, October 2026) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | OpenTofu modules in a tagged repository |
| [oss](../implementations/oss.yaml) | OpenTofu modules in a tagged repository |
<!-- END GENERATED: implementations -->
