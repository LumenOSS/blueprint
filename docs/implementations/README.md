# Implementations

An implementation binds each capability to components and shows, clause by
clause, how it meets the contract. Two reference implementations are
planned, each in its own repository:

| Implementation | Runtime | Binding |
| --- | --- | --- |
| Open source | Any Kubernetes cluster, through OpenTofu and Helm; kind or k3d on a laptop | [`oss.yaml`](oss.yaml) |
| Databricks | Azure Databricks and Azure, through OpenTofu and Declarative Automation Bundles | [`databricks.yaml`](databricks.yaml) |

The files here are the reference bindings each implementation starts from.
Every clause is `planned` until the implementation shows evidence and moves
it to `met`. A clause that cannot be met is a `deviation` with its
consequence, so a gap is always written down. Check a binding with
`just binding <file>`.

## Components by capability

<!-- BEGIN GENERATED: matrix (just render) -->
| Capability | databricks | oss |
| --- | --- | --- |
| [CAP-REPOSITORIES](../capabilities/cap-repositories.md) Repositories by trust | Git with two remotes<br/>Azure Pipelines<br/>Nix flake + just | Git with two remotes<br/>Forgejo Actions<br/>Nix flake + just |
| [CAP-STATE](../capabilities/cap-state.md) Infrastructure state | OpenTofu<br/>azurerm backend<br/>Azure Key Vault | OpenTofu<br/>S3 backend on Ceph RGW<br/>OpenBao transit |
| [CAP-CIIDENTITY](../capabilities/cap-ciidentity.md) CI workload identity | Entra workload identity federation<br/>Databricks OAuth federation policies | CI OIDC token<br/>OpenBao JWT auth<br/>Kubernetes projected service-account tokens |
| [CAP-DELIVERY](../capabilities/cap-delivery.md) Change delivery | Azure Pipelines<br/>Declarative Automation Bundles | Forgejo Actions<br/>Argo CD |
| [CAP-MODULES](../capabilities/cap-modules.md) Versioned modules | OpenTofu modules in a tagged repository | OpenTofu modules in a tagged repository |
| [CAP-ONBOARDING](../capabilities/cap-onboarding.md) Tenant onboarding registry | Tenant YAML + OpenTofu (azurerm, databricks providers) | Tenant YAML + OpenTofu |
| [CAP-SECRETS](../capabilities/cap-secrets.md) Secrets and keys | Azure Key Vault<br/>Key Vault-backed secret scopes | OpenBao<br/>External Secrets Operator |
| [CAP-NETWORK](../capabilities/cap-network.md) Network isolation | VNet injection + secure cluster connectivity<br/>Private Link (front end and back end)<br/>Network connectivity configurations<br/>NAT gateway | Cilium<br/>Gateway API + oauth2-proxy |
| [CAP-GUARDRAILS](../capabilities/cap-guardrails.md) Guardrails and fitness functions | Azure Policy<br/>Conftest on tofu plans<br/>Lakeflow Jobs | OPA Gatekeeper<br/>Conftest<br/>Airflow |
| [CAP-STORAGE](../capabilities/cap-storage.md) Object storage | ADLS Gen2 | Ceph RGW via Rook |
| [CAP-TABLES](../capabilities/cap-tables.md) Open table format | Delta Lake with UniForm | Apache Iceberg |
| [CAP-CATALOG](../capabilities/cap-catalog.md) Catalog and governance plane | Unity Catalog | Lakekeeper<br/>Trino + OPA |
| [CAP-COMPUTE](../capabilities/cap-compute.md) Compute | Serverless jobs compute<br/>Serverless SQL warehouse | Apache Spark 4 via Kubeflow spark-operator<br/>Trino<br/>DuckDB |
| [CAP-OPERATIONALDB](../capabilities/cap-operationaldb.md) Operational database with branching | Lakebase Postgres | CloudNativePG<br/>CSI volume snapshots on Ceph RBD<br/>pgroll |
| [CAP-INGESTION](../capabilities/cap-ingestion.md) Ingestion | Auto Loader<br/>Lakehouse Federation<br/>Lakeflow Connect | Debezium on Kafka via Strimzi<br/>Trino connectors<br/>Landing bucket + pipeline |
| [CAP-INTEROPERABILITY](../capabilities/cap-interoperability.md) Exchange with other systems | Azure API Management<br/>Schema validation at the landing edge | Envoy Gateway<br/>Schema validation at the landing edge |
| [CAP-ORCHESTRATION](../capabilities/cap-orchestration.md) Orchestration | Lakeflow Jobs | Apache Airflow 3 |
| [CAP-TRANSFORMATION](../capabilities/cap-transformation.md) Transformation layer | dbt (v1, Python) with dbt-databricks<br/>dbt task in Lakeflow Jobs | dbt (v1, Python)<br/>dbt-trino adapter |
| [CAP-SEMANTICS](../capabilities/cap-semantics.md) Semantic layer | dbt semantic layer (dbt 1.12 or later, latest YAML spec)<br/>MetricFlow<br/>Unity Catalog metric views via the dbt-databricks metric_view materialisation | dbt semantic layer (dbt 1.12 or later, latest YAML spec)<br/>MetricFlow<br/>Generated saved-query models |
| [CAP-REPORTING](../capabilities/cap-reporting.md) Reporting | AI/BI dashboards<br/>Genie | Apache Superset |
| [CAP-APPS](../capabilities/cap-apps.md) Application hosting | Azure Container Apps | Kubernetes Deployment + Gateway API |
| [CAP-QUALITY](../capabilities/cap-quality.md) Data quality | dbt tests and contracts<br/>Lakeflow pipeline expectations<br/>Data Quality Monitoring | dbt tests and contracts<br/>Great Expectations (GX Core) |
| [CAP-LINEAGE](../capabilities/cap-lineage.md) Lineage | Unity Catalog lineage | OpenLineage |
| [CAP-OBSERVABILITY](../capabilities/cap-observability.md) Operational telemetry | System tables<br/>Azure Monitor / Log Analytics | OpenTelemetry Collector<br/>Prometheus<br/>Grafana + Loki |
| [CAP-MASTERDATA](../capabilities/cap-masterdata.md) Master data and identifiers | Registry services on Lakebase<br/>Splink on Spark | Registry services on PostgreSQL (CloudNativePG)<br/>Splink |
| [CAP-IDENTITY](../capabilities/cap-identity.md) Identity and groups | Entra ID<br/>Automatic identity management / SCIM | Keycloak |
| [CAP-REFERENCE](../capabilities/cap-reference.md) Reference data and data dictionary | Unity Catalog comments, tags and a reference catalog<br/>Versioned code-list tables (dbt seeds) | OpenMetadata<br/>Versioned code-list tables (dbt seeds) |
| [CAP-ACCESS](../capabilities/cap-access.md) Access model | Unity Catalog ABAC policies<br/>Entitlement table in a reference catalog | Entitlement table in Iceberg<br/>OPA policies for Trino |
| [CAP-CLASSIFICATION](../capabilities/cap-classification.md) Classification and provenance | Governed tags<br/>Data classification | Lakekeeper table properties + OPA |
| [CAP-AUDIT](../capabilities/cap-audit.md) Audit | system.access.audit<br/>Diagnostic settings to Log Analytics | Audit sources<br/>Iceberg audit tables on object-locked storage |
| [CAP-RECORDS](../capabilities/cap-records.md) Records lifecycle and data-subject rights | Governed retention tags + Lakeflow Jobs<br/>Delta VACUUM with bounded retention | Retention policies in table properties + Airflow lifecycle jobs<br/>OpenBao transit keys per partition |
| [CAP-SHARING](../capabilities/cap-sharing.md) Publication and sharing | Delta Sharing<br/>Publication catalog | Delta Sharing reference server |
| [CAP-PUBLICATION](../capabilities/cap-publication.md) Open statistical publication | CKAN on Azure Container Apps<br/>Publication catalog | CKAN<br/>Parquet and CSV renderings from publication tables |
| [CAP-ENVIRONMENTS](../capabilities/cap-environments.md) Environments by branching | OpenTofu values files<br/>Lakebase branches<br/>Development schemas in production catalogs | OpenTofu values files<br/>CloudNativePG branch clusters<br/>Iceberg branches or dev namespaces |
| [CAP-BACKFILL](../capabilities/cap-backfill.md) Backfill and reprocessing | Lakeflow Jobs backfill runs<br/>Delta replaceWhere / MERGE<br/>Shallow clones | Airflow 3 backfills<br/>Iceberg branches<br/>dbt microbatch |
| [CAP-MIGRATION](../capabilities/cap-migration.md) Migration and decommission | Unity Catalog storage re-binding<br/>pg_dump / pg_restore | pg_dump / pg_restore<br/>Iceberg register-table |
| [CAP-PIPELINE](../capabilities/cap-pipeline.md) Retryable pipeline | The example product's stages on Lakeflow Jobs | The example product's stages on Airflow + Spark/Python |
| [CAP-COLLECTION](../capabilities/cap-collection.md) Periodic data collection | ODK Central on Azure Container Apps<br/>The census product's return workflow on Lakebase | ODK Central<br/>The census product's return workflow on PostgreSQL |
| [CAP-REVIEW](../capabilities/cap-review.md) Human review | The example product's review service on Lakebase | The example product's review service on Postgres |
| [CAP-MODELS](../capabilities/cap-models.md) Governed analytical models | Managed MLflow with Unity Catalog model registry | MLflow<br/>scikit-learn |
| [CAP-RELEASE](../capabilities/cap-release.md) Reconciliation and release | The example product's release gate | The example product's release gate |
<!-- END GENERATED: matrix -->

## How components are chosen

A component is acceptable when it meets its capability's contract and the
principles; beyond that the choice belongs to the implementation. Two
principles weigh most: data stays in open formats and portable
([P16](../principles.md#p16-open-formats-storage-separate-from-compute-federate-before-copying)),
and it stays where the education authority controls it
([P21](../principles.md#p21-the-education-authority-runs-its-own-platform)).
For the health of an open-source component, use a public assessment rather
than judgement alone; see [standards](../standards.md#open-source-health-and-digital-public-goods).

## How the open-source build differs

Most capabilities have an open-source equivalent. Where the open-source
stack cannot provide a property Databricks provides, the binding says so
and the blueprint names the control that stands in for it. Checked on
2026-10-15:

| Property | Databricks | Open source | Control in the open-source binding |
| --- | --- | --- | --- |
| Row filters and masks in every engine | Unity Catalog enforces them across SQL, serverless and shared Spark | Only Trino enforces them, through OPA; OSS Spark, DuckDB and PyIceberg do not | Protected tables are served only through Trino; other engines are denied them ([CAP-CATALOG.5](../capabilities/cap-catalog.md)) |
| One governance plane | Grants, policies, lineage and audit in one catalog | Grants in the catalog, row policy in OPA, BI policy in Superset, audit in several sources | Policy as code in one repository, tested in CI; audit collected centrally |
| Instant database branches | Lakebase copy-on-write branches at any point in time | A new Postgres instance from a copy-on-write volume snapshot; point in time needs WAL replay | Branches take minutes, not seconds ([CAP-OPERATIONALDB.2](../capabilities/cap-operationaldb.md)) |
| Automatic lineage | Captured for all governed compute | Only where an OpenLineage integration exists | A job without lineage is a defect ([CAP-LINEAGE.1](../capabilities/cap-lineage.md)) |
| Managed table maintenance | Predictive optimisation | Compaction and snapshot expiry are scheduled jobs | A maintenance job per warehouse, with alerts |
| Scale to zero | Serverless compute | Spark jobs scale per run; the Trino coordinator stays up | Recorded as a deviation from [CAP-COMPUTE.1](../capabilities/cap-compute.md) |
| Push provisioning of groups | SCIM or automatic identity management | Keycloak passes groups in sign-in tokens | Short token lifetimes and session revocation on leaving |
| Attested private endpoints | Private Link and network connectivity configurations | NetworkPolicy and flow logs | Connectivity tests in CI; flow logs kept as audit |

Open-source licences moved a lot in 2025 and 2026. MinIO's community
edition is archived, Soda Core moved to ELv2, and HashiCorp Vault and
Redpanda are source-available. Every component in a binding carries its
SPDX licence, and the licence is checked again at each upgrade.
