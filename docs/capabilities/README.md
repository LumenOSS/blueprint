# Capabilities

Each capability is something the platform must be able to do, with a
contract of numbered clauses. `MUST`, `SHOULD` and `MAY` are used as in
[BCP 14](https://www.rfc-editor.org/info/bcp14) (RFC 2119 and RFC 8174):
only the upper-case words are requirements. Every clause says how
conformance is shown, so an implementation can prove it rather than claim
it.

The clause text lives in [`blueprint/catalogue.yaml`](../../blueprint/catalogue.yaml);
the tables on each page are generated from it with `just render`.

## How to read a page

- **Purpose** says what the capability is for.
- **Why** gives the reasoning and links the [principles](../principles.md)
  it rests on.
- **Interfaces** names what other capabilities and people use.
- **Notes** record traps found by running the architecture.
- **Contract** is the generated clause table.
- **Implementations** lists the components each reference implementation
  binds to the capability.

## Index

<!-- BEGIN GENERATED: index (just render) -->
### Trust and delivery

Who may change what, with which identity, and how a change reaches an environment.

| Capability | Layer | Summary | Clauses |
| --- | --- | --- | --- |
| [CAP-REPOSITORIES Repositories by trust](cap-repositories.md) | L0 Bootstrap | Each layer is its own repository and the unit of trust for its CI identities. | 5 (4 MUST) |
| [CAP-STATE Infrastructure state](cap-state.md) | L0 Bootstrap | Remote, locked, versioned and encrypted state for every stack, readable only by the identities that own it. | 8 (7 MUST) |
| [CAP-CIIDENTITY CI workload identity](cap-ciidentity.md) | L0 Bootstrap | CI authenticates by federation with short-lived tokens; the root of trust is created once by a person. | 6 (5 MUST) |
| [CAP-DELIVERY Change delivery](cap-delivery.md) | L1 Platform | Every change is reviewed with its plan and applied by CI only, after merge. | 8 (6 MUST) |
| [CAP-MODULES Versioned modules](cap-modules.md) | L2 Modules | Shared building blocks consumed by immutable version, including deterministic naming. | 3 (2 MUST) |
| [CAP-ONBOARDING Tenant onboarding registry](cap-onboarding.md) | L1 Platform | One reviewed declaration per product or source generates its identities, grants, schemas and reviewers. | 4 (4 MUST) |
| [CAP-SECRETS Secrets and keys](cap-secrets.md) | L1 Platform | Secrets and keys live in a managed store and are fetched by identity at runtime. | 3 (2 MUST) |
| [CAP-NETWORK Network isolation](cap-network.md) | L1 Platform | Data services are private; only applications are exposed, behind sign-in. | 4 (3 MUST) |
| [CAP-GUARDRAILS Guardrails and fitness functions](cap-guardrails.md) | L1 Platform | Policy as code on every plan, and scheduled checks that the architecture's properties still hold. | 3 (2 MUST) |

### Data platform core

Where data lives, how it is computed on, and how it reaches the people who use it.

| Capability | Layer | Summary | Clauses |
| --- | --- | --- | --- |
| [CAP-STORAGE Object storage](cap-storage.md) | L1 Platform | Durable object storage for tables and files, isolated per domain catalog. | 5 (5 MUST) |
| [CAP-TABLES Open table format](cap-tables.md) | L1 Platform | Transactional tables in an open format, readable by more than one engine. | 4 (3 MUST) |
| [CAP-CATALOG Catalog and governance plane](cap-catalog.md) | L1 Platform | One catalog of record for tables, files and functions, enforcing grants, tags and policies. | 7 (6 MUST) |
| [CAP-COMPUTE Compute](cap-compute.md) | L1 Platform | Batch, streaming and interactive SQL compute that scales to zero and reads only through the catalog. | 4 (4 MUST) |
| [CAP-OPERATIONALDB Operational database with branching](cap-operationaldb.md) | L1 Platform | Each product's transactional Postgres store, with copy-on-write branches of production. | 7 (6 MUST) |
| [CAP-INGESTION Ingestion](cap-ingestion.md) | L1 Platform | Files, in-place federation and change data capture behind one onboarding step. | 4 (3 MUST) |
| [CAP-INTEROPERABILITY Exchange with other systems](cap-interoperability.md) | L1 Platform | Every feed to or from another system is declared, validated at the edge and reconciled. | 7 (4 MUST) |
| [CAP-ORCHESTRATION Orchestration](cap-orchestration.md) | L3 Products | Declared jobs with bounded runs, safe retries and range re-runs. | 6 (6 MUST) |
| [CAP-TRANSFORMATION Transformation layer](cap-transformation.md) | L3 Products | Versioned, tested models from bronze to silver to gold; the only place measures are computed. | 8 (6 MUST) |
| [CAP-SEMANTICS Semantic layer](cap-semantics.md) | L1 Platform | Every measure defined once, versioned, and read by every consumer. | 5 (4 MUST) |
| [CAP-REPORTING Reporting](cap-reporting.md) | L3 Products | Dashboards and natural-language query over the semantic layer, deployed as code. | 3 (2 MUST) |
| [CAP-APPS Application hosting](cap-apps.md) | L3 Products | Product interfaces deployed by CI, behind sign-in, that say which environment they are in. | 9 (7 MUST) |
| [CAP-QUALITY Data quality](cap-quality.md) | L3 Products | Checks at every tier; failing data is quarantined, never used. | 6 (4 MUST) |
| [CAP-LINEAGE Lineage](cap-lineage.md) | L1 Platform | Which inputs produced which outputs, captured as work runs. | 3 (1 MUST) |
| [CAP-OBSERVABILITY Operational telemetry](cap-observability.md) | L1 Platform | Per-item metrics, freshness and cost, reaching gold so cost can be told apart from work. | 3 (3 MUST) |
| [CAP-MASTERDATA Master data and identifiers](cap-masterdata.md) | L1 Platform | One authoritative registry per core resource, with permanent opaque identifiers and governed duplicate resolution. | 9 (8 MUST) |

### Governance and access

Who may see which rows and columns, how that is recorded, and how data leaves the platform.

| Capability | Layer | Summary | Clauses |
| --- | --- | --- | --- |
| [CAP-IDENTITY Identity and groups](cap-identity.md) | L1 Platform | One identity provider for people and groups, synchronised automatically, with break-glass access held apart. | 6 (6 MUST) |
| [CAP-REFERENCE Reference data and data dictionary](cap-reference.md) | L1 Platform | Governed code lists, a versioned data dictionary and common formats, so every value means the same thing everywhere. | 8 (6 MUST) |
| [CAP-ACCESS Access model](cap-access.md) | L1 Platform | Role decides reach, entitlements decide rows, classification decides columns. | 8 (8 MUST) |
| [CAP-CLASSIFICATION Classification and provenance](cap-classification.md) | L1 Platform | Every table and column is classified by sensitivity and tagged with provenance from the moment it lands. | 7 (7 MUST) |
| [CAP-AUDIT Audit](cap-audit.md) | L1 Platform | Every access and administrative action recorded, retained beyond the platform default, readable by auditors only. | 5 (3 MUST) |
| [CAP-RECORDS Records lifecycle and data-subject rights](cap-records.md) | L1 Platform | Every record has a retention class; archiving, disposal, subject access, rectification and individual disclosure follow declared, audited paths. | 7 (7 MUST) |
| [CAP-SHARING Publication and sharing](cap-sharing.md) | L1 Platform | External parties receive de-identified tables from a publication catalog over an open protocol, each share approved and registered. | 6 (5 MUST) |
| [CAP-PUBLICATION Open statistical publication](cap-publication.md) | L1 Platform | Aggregate statistics published openly with disclosure control, permanent identifiers and open metadata. | 9 (5 MUST) |

### Environments and data movement

How environments are isolated, and how data is backfilled, migrated and retired without loss.

| Capability | Layer | Summary | Clauses |
| --- | --- | --- | --- |
| [CAP-ENVIRONMENTS Environments by branching](cap-environments.md) | L1 Platform | An environment is a template plus values; development is isolated inside production by branching. | 5 (5 MUST) |
| [CAP-BACKFILL Backfill and reprocessing](cap-backfill.md) | L3 Products | Loading history, reprocessing and filling gaps are idempotent, bounded, rehearsed and reconciled. | 8 (8 MUST) |
| [CAP-MIGRATION Migration and decommission](cap-migration.md) | L1 Platform | Moving between platforms or accounts without loss, with a fallback window and two-role sign-off. | 5 (5 MUST) |

### Product patterns

The contracts a product meets so that its pipeline is retryable, its decisions reviewable and its results releasable.

| Capability | Layer | Summary | Clauses |
| --- | --- | --- | --- |
| [CAP-PIPELINE Retryable pipeline](cap-pipeline.md) | L3 Products | Content-addressed, deterministic stages that hand off through storage and can retry while the database is down. | 7 (7 MUST) |
| [CAP-COLLECTION Periodic data collection](cap-collection.md) | L3 Products | Returns collected from institutions on a cycle, validated at entry, attested, gated on completeness and frozen at a reference date. | 10 (6 MUST) |
| [CAP-REVIEW Human review](cap-review.md) | L3 Products | Low-confidence results go to people, whose decisions are leased, durable and never overwritten by machines. | 5 (5 MUST) |
| [CAP-MODELS Governed analytical models](cap-models.md) | L3 Products | Predictive models, such as early-warning flags, that advise people, are reproducible, and are checked for unequal error before release. | 5 (4 MUST) |
| [CAP-RELEASE Reconciliation and release](cap-release.md) | L3 Products | Results are released per unit only when the unit reconciles against its register. | 3 (3 MUST) |
<!-- END GENERATED: index -->
