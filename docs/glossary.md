# Glossary

**Binding.** An implementation's statement of which components provide a
capability, and the status and evidence of each of its clauses. Written as
YAML against [`schema/binding.schema.json`](../schema/binding.schema.json).

**Blueprint.** This repository: the architecture as capabilities and
contracts, independent of any vendor.

**Branch.** A copy-on-write child of a database or catalog that shares
storage with its parent until it diverges. Distinct from a version-control
branch, which this document calls a *change*.

**Capability.** Something the platform must be able to do, named by a stable
`CAP-` identifier, owned by one layer, and defined by its contract.

**Clause.** One numbered requirement in a contract (`CAP-STATE.2`), with a
level (`MUST`, `SHOULD`, `MAY`, as in RFC 2119) and the way conformance is
shown.

**Contract.** The full set of clauses for a capability.

**Data Lead, Technical Lead.** The two roles that share sign-off of trust
changes, cutover, rollback and decommission.

**Deviation.** A clause an implementation will not meet, recorded in its
binding with the consequence. A deviation is a known gap, never a silent one.

**Domain.** A business area that owns its data (for example students,
assessment, finance). Catalogs are named `<domain>_<environment>`.

**Environment.** Every axis that decides which world a change runs in:
catalog and schema, database branch and database, application identity and
configuration, and jobs. An environment is a template plus a values file.

**Implementation.** A concrete stack that meets the blueprint, in its own
repository, with a binding.

**Layer.** A trust level: L0 bootstrap, L1 platform, L2 modules, L3
products. Each layer is its own repository.

**Medallion.** The bronze (as received), silver (conformed) and gold
(consumable) tiers of the transformation layer.

**Operator.** Whoever carries out a procedure, by role.

**Product.** A workload built on the platform, with its own repository, its
own operational database and a tenant entry.

**Provenance.** A governed tag on every table: `real`, `simulated` or
`derived`.

**Steward.** The role accountable for a domain's data and its access
decisions.

**Tenant entry.** A product's or source's one reviewed declaration in the
onboarding registry, from which its identities, grants and schemas are
generated.
