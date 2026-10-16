# Glossary

This glossary covers the terms the blueprint uses for itself and for the platform. You won't find the words of the EMIS domain here, such as institution, learner, enrolment or return. Each bounded context defines those in its own vocabulary, and the [context map](../../CONTEXT-MAP.md) lists the contexts.

**Binding.** An implementation's statement of which components provide each capability, and where it stands on each clause, with evidence. It's written as YAML that follows [`schema/binding.schema.json`](../../schema/binding.schema.json).

**Blueprint.** This repository. It states the architecture as capabilities and contracts, independent of any vendor.

**Branch.** A copy-on-write child of a database or catalog. It shares storage with its parent until the two diverge. Don't confuse it with a version-control branch, which these documents call a *change*.

**Capability.** Something the platform must be able to do. Each has a stable `CAP-` identifier, belongs to one layer, and is defined by its contract.

**Clause.** One numbered requirement in a contract, such as `CAP-STATE.2`. It has a level (`MUST`, `SHOULD` or `MAY`, as in RFC 2119) and says how you show that you meet it.

**Code list.** A governed, versioned set of the values a coded attribute may take. A code that's no longer wanted is retired, never reused.

**Completeness gate.** A check, run before figures are released, that what was received balances against the respondents or subjects that were expected. It reads either BLOCKED or CLEAR.

**Contract.** The full set of clauses for a capability.

**Crosswalk.** A versioned mapping from a local classification to an international one.

**Data dictionary.** The register of every published data element. It follows the ISO/IEC 11179 model and is kept as catalog metadata.

**Data Lead, Technical Lead.** The two roles that share sign-off of changes to trust, cutover, rollback and decommission.

**Deviation.** A clause that an implementation won't meet, recorded in its binding together with the consequence. A deviation is a gap everyone knows about, never a silent one.

**Disaggregation.** Splitting an indicator by a dimension such as sex, age, area or disability.

**Disclosure control.** The rules that stop published statistics from revealing individuals, such as a minimum cell size, secondary suppression and rounding.

**Domain.** A business area that owns its data, for example learners, assessment or finance. Catalogs are named `<domain>_<environment>`.

**Effective dating.** Recording when a relationship was valid (valid-from and valid-to), separately from when it was recorded.

**EMIS.** An education management information system: the system an education authority uses to hold and report data about its institutions, learners and staff. See [what is an EMIS](../concepts/emis.md).

**Environment.** Everything that decides which world a change runs in: the catalog and schema, the database and its branch, the application's identity and configuration, and the jobs. An environment is a template plus a values file.

**Implementation.** A real stack that meets the blueprint. It lives in its own repository and has a binding.

**Layer.** A level of trust: L0 bootstrap, L1 platform, L2 modules and L3 products. Each layer is its own repository.

**Master data.** The authoritative records of core resources, such as institutions, people and posts, that every other record refers to.

**Medallion.** The three tiers of the transformation layer: bronze (data as received), silver (data made consistent) and gold (data ready to use).

**Operator.** Whoever carries out a procedure, named by role.

**Product.** A workload built on the platform. It has its own repository, its own operational database and a tenant entry.

**Provenance.** A governed tag on every table: `real`, `simulated` or `derived`.

**Purpose.** The declared reason a personal-data element is collected or a record is accessed.

**Record class.** A group of records sharing a retention period, trigger event and legal basis.

**Steward.** The role accountable for a domain's data and its access decisions.

**Surrogate identifier.** A permanent identifier that the platform creates and that carries no meaning of its own.

**Tenant entry.** The single reviewed declaration a product or source makes in the onboarding registry. Its identities, grants and schemas are generated from that entry.
