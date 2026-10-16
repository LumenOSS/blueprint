# Glossary

Terms about the blueprint and the platform. The language of the EMIS domain itself (institution, learner, enrolment, return and so on) is in the language of each bounded context, listed in the [context map](../../CONTEXT-MAP.md).

**Binding.** An implementation's statement of which components provide a capability, and the status and evidence of each of its clauses. Written as YAML against [`schema/binding.schema.json`](../../schema/binding.schema.json).

**Blueprint.** This repository: the architecture as capabilities and contracts, independent of any vendor.

**Branch.** A copy-on-write child of a database or catalog that shares storage with its parent until it diverges. Distinct from a version-control branch, which this document calls a *change*.

**Capability.** Something the platform must be able to do, named by a stable `CAP-` identifier, owned by one layer, and defined by its contract.

**Clause.** One numbered requirement in a contract (`CAP-STATE.2`), with a level (`MUST`, `SHOULD`, `MAY`, as in RFC 2119) and the way conformance is shown.

**Code list.** A governed, versioned set of allowed values for a coded attribute. A code is retired, never reused.

**Completeness gate.** A check that expected respondents or subjects balance against what was received before figures are released; it reads BLOCKED or CLEAR.

**Contract.** The full set of clauses for a capability.

**Crosswalk.** A versioned mapping from a local classification to an international one.

**Data dictionary.** The register of every published data element, modelled on ISO/IEC 11179 and held as catalog metadata.

**Data Lead, Technical Lead.** The two roles that share sign-off of trust changes, cutover, rollback and decommission.

**Deviation.** A clause an implementation will not meet, recorded in its binding with the consequence. A deviation is a known gap, never a silent one.

**Disaggregation.** Splitting an indicator by a dimension such as sex, age, area or disability.

**Disclosure control.** Rules that stop published statistics revealing individuals: minimum cell size, secondary suppression and rounding.

**Domain.** A business area that owns its data (for example learners, assessment, finance). Catalogs are named `<domain>_<environment>`.

**Effective dating.** Recording when a relationship was valid (valid-from, valid-to) separately from when it was recorded.

**EMIS.** Education management information system: the system an education authority uses to hold and report data about institutions, learners and staff. See [what is an EMIS](../concepts/emis.md).

**Environment.** Every axis that decides which world a change runs in: catalog and schema, database branch and database, application identity and configuration, and jobs. An environment is a template plus a values file.

**Implementation.** A concrete stack that meets the blueprint, in its own repository, with a binding.

**Layer.** A trust level: L0 bootstrap, L1 platform, L2 modules, L3 products. Each layer is its own repository.

**Master data.** The authoritative records of core resources (institutions, people, posts) that every other record refers to.

**Medallion.** The bronze (as received), silver (conformed) and gold (consumable) tiers of the transformation layer.

**Operator.** Whoever carries out a procedure, by role.

**Product.** A workload built on the platform, with its own repository, its own operational database and a tenant entry.

**Provenance.** A governed tag on every table: `real`, `simulated` or `derived`.

**Purpose.** The declared reason a personal-data element is collected or a record is accessed.

**Record class.** A group of records sharing a retention period, trigger event and legal basis.

**Steward.** The role accountable for a domain's data and its access decisions.

**Surrogate identifier.** An opaque, permanent identifier minted by the platform that encodes nothing.

**Tenant entry.** A product's or source's one reviewed declaration in the onboarding registry, from which its identities, grants and schemas are generated.
