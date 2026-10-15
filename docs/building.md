# Building an implementation

How to turn the blueprint into a running platform on a stack of your
choice. The steps are the same for a person and for an agent. Each step ends
on a completion criterion; move on only when it holds.

## 1. Choose the stack and write the binding

Copy the reference binding closest to your stack from
[`implementations/`](implementations/README.md), or start from
[`schema/binding.schema.json`](../schema/binding.schema.json). For each
capability, name the components and their SPDX licences. For each clause,
set a status:

- `planned`: you intend to meet it; say `how` if it is not obvious.
- `deviation`: you will not meet it; write the `consequence` and the control
  that stands in for it.
- `not-applicable`: its precondition does not hold; write why.

**Done when** `just binding <your-binding.yaml>` reports no problems and
every deviation names a compensating control.

## 2. Lay out the repositories

Create one repository per layer, following
[CAP-REPOSITORIES](capabilities/cap-repositories.md): bootstrap, platform,
modules, and one per product. Each has a pinned toolchain and a task
runner, and its CI definitions only call tasks. If the repositories will
live on more than one CI host, put each host's CI definition beside the
others now.

**Done when** each repository's check task passes on a clean clone, on a
workstation and in CI.

## 3. Build in dependency order

Build capabilities in the order below, which is generated from the
dependencies in the catalogue. A capability can be built once everything it
depends on is built. Work within the bootstrap layer comes first because
every later apply needs its state store and identities.

For each capability:

1. Build it through the CI pipeline, never by hand
   ([P1](principles.md#p1-ci-is-the-only-deployer)).
2. Run each clause's verification as written in its contract.
3. Record the evidence (a test, a query and its output, a CI run) in the
   binding and change the clause's status to `met`.

**Done when** every `MUST` clause of the capability is `met`, or is a
recorded deviation.

<!-- BEGIN GENERATED: order (just render) -->
| Step | Capability | Layer | Depends on |
| --- | --- | --- | --- |
| 1 | [CAP-REPOSITORIES](capabilities/cap-repositories.md) Repositories by trust | L0 | — |
| 2 | [CAP-CIIDENTITY](capabilities/cap-ciidentity.md) CI workload identity | L0 | — |
| 3 | [CAP-MODULES](capabilities/cap-modules.md) Versioned modules | L2 | — |
| 4 | [CAP-STATE](capabilities/cap-state.md) Infrastructure state | L0 | CAP-MODULES |
| 5 | [CAP-DELIVERY](capabilities/cap-delivery.md) Change delivery | L1 | CAP-CIIDENTITY, CAP-STATE |
| 6 | [CAP-SECRETS](capabilities/cap-secrets.md) Secrets and keys | L1 | — |
| 7 | [CAP-NETWORK](capabilities/cap-network.md) Network isolation | L1 | — |
| 8 | [CAP-GUARDRAILS](capabilities/cap-guardrails.md) Guardrails and fitness functions | L1 | CAP-DELIVERY |
| 9 | [CAP-STORAGE](capabilities/cap-storage.md) Object storage | L1 | — |
| 10 | [CAP-TABLES](capabilities/cap-tables.md) Open table format | L1 | CAP-STORAGE |
| 11 | [CAP-OBSERVABILITY](capabilities/cap-observability.md) Operational telemetry | L1 | — |
| 12 | [CAP-IDENTITY](capabilities/cap-identity.md) Identity and groups | L1 | — |
| 13 | [CAP-CATALOG](capabilities/cap-catalog.md) Catalog and governance plane | L1 | CAP-TABLES, CAP-IDENTITY |
| 14 | [CAP-ONBOARDING](capabilities/cap-onboarding.md) Tenant onboarding registry | L1 | CAP-DELIVERY, CAP-CATALOG, CAP-CIIDENTITY |
| 15 | [CAP-COMPUTE](capabilities/cap-compute.md) Compute | L1 | CAP-CATALOG |
| 16 | [CAP-OPERATIONALDB](capabilities/cap-operationaldb.md) Operational database with branching | L1 | CAP-IDENTITY |
| 17 | [CAP-INGESTION](capabilities/cap-ingestion.md) Ingestion | L1 | CAP-ONBOARDING, CAP-CATALOG |
| 18 | [CAP-LINEAGE](capabilities/cap-lineage.md) Lineage | L1 | CAP-CATALOG |
| 19 | [CAP-CLASSIFICATION](capabilities/cap-classification.md) Classification and provenance | L1 | CAP-CATALOG |
| 20 | [CAP-ACCESS](capabilities/cap-access.md) Access model | L1 | CAP-IDENTITY, CAP-CATALOG, CAP-CLASSIFICATION |
| 21 | [CAP-AUDIT](capabilities/cap-audit.md) Audit | L1 | CAP-IDENTITY |
| 22 | [CAP-ENVIRONMENTS](capabilities/cap-environments.md) Environments by branching | L1 | CAP-OPERATIONALDB, CAP-CATALOG |
| 23 | [CAP-MIGRATION](capabilities/cap-migration.md) Migration and decommission | L1 | CAP-OPERATIONALDB, CAP-CLASSIFICATION |
| 24 | [CAP-ORCHESTRATION](capabilities/cap-orchestration.md) Orchestration | L3 | CAP-COMPUTE, CAP-DELIVERY |
| 25 | [CAP-TRANSFORMATION](capabilities/cap-transformation.md) Transformation layer | L3 | CAP-COMPUTE, CAP-CATALOG |
| 26 | [CAP-SEMANTICS](capabilities/cap-semantics.md) Semantic layer | L1 | CAP-TRANSFORMATION |
| 27 | [CAP-SHARING](capabilities/cap-sharing.md) Publication and sharing | L1 | CAP-CATALOG, CAP-CLASSIFICATION, CAP-TRANSFORMATION |
| 28 | [CAP-REPORTING](capabilities/cap-reporting.md) Reporting | L3 | CAP-SEMANTICS |
| 29 | [CAP-APPS](capabilities/cap-apps.md) Application hosting | L3 | CAP-NETWORK, CAP-DELIVERY |
| 30 | [CAP-QUALITY](capabilities/cap-quality.md) Data quality | L3 | CAP-TRANSFORMATION |
| 31 | [CAP-BACKFILL](capabilities/cap-backfill.md) Backfill and reprocessing | L3 | CAP-ORCHESTRATION, CAP-ENVIRONMENTS, CAP-QUALITY |
| 32 | [CAP-PIPELINE](capabilities/cap-pipeline.md) Retryable pipeline | L3 | CAP-ORCHESTRATION, CAP-STORAGE |
| 33 | [CAP-REVIEW](capabilities/cap-review.md) Human review | L3 | CAP-OPERATIONALDB, CAP-AUDIT |
| 34 | [CAP-RELEASE](capabilities/cap-release.md) Reconciliation and release | L3 | CAP-REVIEW |
<!-- END GENERATED: order -->

## 4. Run the example product

Deploy the [example product](product/README.md) and run its conformance
steps. It exercises the product capabilities and, through them, most of the
platform.

**Done when** all six conformance steps pass and their evidence is in the
binding.

## 5. Keep it conforming

- Scheduled fitness functions keep checking what was proved once
  ([CAP-GUARDRAILS.2](capabilities/cap-guardrails.md)).
- When the blueprint's version changes, read its changelog, update the
  binding's `blueprint.version`, and set the status of every new or changed
  clause.
- Re-check component licences at each upgrade.

**Done when** the binding validates against the current catalogue and no
fitness function is failing.

## Changing the blueprint itself

An implementation that finds a clause wrong, untestable or missing proposes
a change to the blueprint through an [ADR](adr/README.md). It never edits
the contract to fit itself.
