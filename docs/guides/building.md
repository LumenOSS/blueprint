# Building an implementation

This guide takes you from the blueprint to a running platform, on
whatever stack you choose. The steps are the same whether you're a person
or an agent. Each step ends with a test of whether it's done, and you
should only move on once that test passes.

## 1. Choose the stack and write the binding

Copy the reference binding that's closest to your stack from
[`implementations/`](../specifications/implementations/README.md), or start
from [`schema/binding.schema.json`](../../schema/binding.schema.json). For
each capability, name the components and their SPDX licences. Then give
each clause a status:

- `planned` means you intend to meet it. If how you'll do so isn't
  obvious, say so in `how`.
- `deviation` means you won't meet it. Write down the `consequence`, and
  the control that stands in for it.
- `not-applicable` means the clause's precondition doesn't hold. Write down
  why.

**You're done when** `just binding <your-binding.yaml>` reports no
problems and every deviation names a compensating control.

## 2. Lay out the repositories

Create one repository for each layer, as
[CAP-REPOSITORIES](../specifications/capabilities/cap-repositories.md)
describes. That means one each for bootstrap, platform and modules, and
one for each product. Each repository has a pinned toolchain and a task
runner, and its CI definitions do nothing but call tasks. If your
repositories will live on more than one CI host, add each host's CI
definition alongside the others now.

**You're done when** each repository's check task passes on a clean
clone, both on a workstation and in CI.

## 3. Build in dependency order

Build the capabilities in the order below, which is generated from the
dependencies in the catalogue. You can build a capability once everything
it depends on is built. The bootstrap layer comes first, because every
later apply needs its state store and identities.

For each capability:

1. Build it through the CI pipeline, never by hand
   ([P1](../specifications/principles.md#p1-ci-is-the-only-deployer)).
2. Run each clause's verification, exactly as its contract describes.
3. Record the evidence in the binding, whether that's a test, a query and
   its output, or a CI run, and change the clause's status to `met`.

**You're done when** every `MUST` clause of the capability is `met`, or is
a recorded deviation.

<!-- BEGIN GENERATED: order (just render) -->
| Step | Capability | Layer | Depends on |
| --- | --- | --- | --- |
| 1 | [CAP-REPOSITORIES](../specifications/capabilities/cap-repositories.md) Repositories by trust | L0 | — |
| 2 | [CAP-CIIDENTITY](../specifications/capabilities/cap-ciidentity.md) CI workload identity | L0 | — |
| 3 | [CAP-MODULES](../specifications/capabilities/cap-modules.md) Versioned modules | L2 | — |
| 4 | [CAP-STATE](../specifications/capabilities/cap-state.md) Infrastructure state | L0 | CAP-MODULES |
| 5 | [CAP-DELIVERY](../specifications/capabilities/cap-delivery.md) Change delivery | L1 | CAP-CIIDENTITY, CAP-STATE |
| 6 | [CAP-SECRETS](../specifications/capabilities/cap-secrets.md) Secrets and keys | L1 | — |
| 7 | [CAP-NETWORK](../specifications/capabilities/cap-network.md) Network isolation | L1 | — |
| 8 | [CAP-GUARDRAILS](../specifications/capabilities/cap-guardrails.md) Guardrails and fitness functions | L1 | CAP-DELIVERY |
| 9 | [CAP-STORAGE](../specifications/capabilities/cap-storage.md) Object storage | L1 | — |
| 10 | [CAP-TABLES](../specifications/capabilities/cap-tables.md) Open table format | L1 | CAP-STORAGE |
| 11 | [CAP-OBSERVABILITY](../specifications/capabilities/cap-observability.md) Operational telemetry | L1 | — |
| 12 | [CAP-IDENTITY](../specifications/capabilities/cap-identity.md) Identity and groups | L1 | — |
| 13 | [CAP-CATALOG](../specifications/capabilities/cap-catalog.md) Catalog and governance plane | L1 | CAP-TABLES, CAP-IDENTITY |
| 14 | [CAP-ONBOARDING](../specifications/capabilities/cap-onboarding.md) Tenant onboarding registry | L1 | CAP-DELIVERY, CAP-CATALOG, CAP-CIIDENTITY |
| 15 | [CAP-COMPUTE](../specifications/capabilities/cap-compute.md) Compute | L1 | CAP-CATALOG |
| 16 | [CAP-OPERATIONALDB](../specifications/capabilities/cap-operationaldb.md) Operational database with branching | L1 | CAP-IDENTITY |
| 17 | [CAP-INGESTION](../specifications/capabilities/cap-ingestion.md) Ingestion | L1 | CAP-ONBOARDING, CAP-CATALOG |
| 18 | [CAP-INTEROPERABILITY](../specifications/capabilities/cap-interoperability.md) Exchange with other systems | L1 | CAP-ONBOARDING, CAP-CATALOG |
| 19 | [CAP-LINEAGE](../specifications/capabilities/cap-lineage.md) Lineage | L1 | CAP-CATALOG |
| 20 | [CAP-MASTERDATA](../specifications/capabilities/cap-masterdata.md) Master data and identifiers | L1 | CAP-CATALOG, CAP-OPERATIONALDB |
| 21 | [CAP-REFERENCE](../specifications/capabilities/cap-reference.md) Reference data and data dictionary | L1 | CAP-CATALOG |
| 22 | [CAP-CLASSIFICATION](../specifications/capabilities/cap-classification.md) Classification and provenance | L1 | CAP-CATALOG |
| 23 | [CAP-ACCESS](../specifications/capabilities/cap-access.md) Access model | L1 | CAP-IDENTITY, CAP-CATALOG, CAP-CLASSIFICATION |
| 24 | [CAP-AUDIT](../specifications/capabilities/cap-audit.md) Audit | L1 | CAP-IDENTITY |
| 25 | [CAP-RECORDS](../specifications/capabilities/cap-records.md) Records lifecycle and data-subject rights | L1 | CAP-CLASSIFICATION, CAP-MASTERDATA, CAP-AUDIT |
| 26 | [CAP-ENVIRONMENTS](../specifications/capabilities/cap-environments.md) Environments by branching | L1 | CAP-OPERATIONALDB, CAP-CATALOG |
| 27 | [CAP-MIGRATION](../specifications/capabilities/cap-migration.md) Migration and decommission | L1 | CAP-OPERATIONALDB, CAP-CLASSIFICATION |
| 28 | [CAP-ORCHESTRATION](../specifications/capabilities/cap-orchestration.md) Orchestration | L3 | CAP-COMPUTE, CAP-DELIVERY |
| 29 | [CAP-TRANSFORMATION](../specifications/capabilities/cap-transformation.md) Transformation layer | L3 | CAP-COMPUTE, CAP-CATALOG |
| 30 | [CAP-SEMANTICS](../specifications/capabilities/cap-semantics.md) Semantic layer | L1 | CAP-TRANSFORMATION |
| 31 | [CAP-SHARING](../specifications/capabilities/cap-sharing.md) Publication and sharing | L1 | CAP-CATALOG, CAP-CLASSIFICATION, CAP-TRANSFORMATION |
| 32 | [CAP-PUBLICATION](../specifications/capabilities/cap-publication.md) Open statistical publication | L1 | CAP-SEMANTICS, CAP-CLASSIFICATION, CAP-REFERENCE |
| 33 | [CAP-REPORTING](../specifications/capabilities/cap-reporting.md) Reporting | L3 | CAP-SEMANTICS |
| 34 | [CAP-APPS](../specifications/capabilities/cap-apps.md) Application hosting | L3 | CAP-NETWORK, CAP-DELIVERY |
| 35 | [CAP-QUALITY](../specifications/capabilities/cap-quality.md) Data quality | L3 | CAP-TRANSFORMATION |
| 36 | [CAP-BACKFILL](../specifications/capabilities/cap-backfill.md) Backfill and reprocessing | L3 | CAP-ORCHESTRATION, CAP-ENVIRONMENTS, CAP-QUALITY |
| 37 | [CAP-PIPELINE](../specifications/capabilities/cap-pipeline.md) Retryable pipeline | L3 | CAP-ORCHESTRATION, CAP-STORAGE |
| 38 | [CAP-COLLECTION](../specifications/capabilities/cap-collection.md) Periodic data collection | L3 | CAP-MASTERDATA, CAP-QUALITY, CAP-REFERENCE |
| 39 | [CAP-REVIEW](../specifications/capabilities/cap-review.md) Human review | L3 | CAP-OPERATIONALDB, CAP-AUDIT |
| 40 | [CAP-MODELS](../specifications/capabilities/cap-models.md) Governed analytical models | L3 | CAP-TRANSFORMATION, CAP-REVIEW |
| 41 | [CAP-RELEASE](../specifications/capabilities/cap-release.md) Reconciliation and release | L3 | CAP-REVIEW |
<!-- END GENERATED: order -->

## 4. Run the example products

Deploy the [example products](products/README.md) and run their
conformance steps. Document review exercises the pipeline, review and
release capabilities, and the annual census exercises master data,
collection, indicators and publication. Between them, they reach most of
the platform.

**You're done when** the conformance steps of both products pass and
their evidence is in the binding.

## 5. Keep it conforming

Proving a clause once isn't enough, so keep checking:

- Scheduled fitness functions keep re-checking what you've already proved
  ([CAP-GUARDRAILS.2](../specifications/capabilities/cap-guardrails.md)).
- When the blueprint's version changes, read its changelog, update the
  binding's `blueprint.version`, and set a status for every new or changed
  clause.
- Re-check your components' licences at each upgrade.

**You're done when** the binding validates against the current catalogue
and no fitness function is failing.

## Changing the blueprint itself

If you find that a clause is wrong, can't be tested, or is missing,
propose a change to the blueprint through a [LIP](../lips/lip-0001.md),
which is recorded as an [ADR](../adr/README.md) once accepted. Don't edit
the contract to fit your implementation.
