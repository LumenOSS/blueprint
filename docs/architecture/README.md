# Architecture

The architecture at three C4 levels: the system in its context (C1), the
containers inside it (C2), and the components of the containers where most
of the design lives (C3). Every box is a capability or a group of
capabilities from the [catalogue](../capabilities/README.md); no box names a
product, because products are an implementation's choice
([implementations](../implementations/README.md)).

Colours follow C4: people dark blue, the system and its containers blue,
external systems grey.

## C1 System context

```mermaid
---
config:
  flowchart:
    curve: step
    nodeSpacing: 40
    rankSpacing: 110
---
flowchart LR
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef ext fill:#999,stroke:#6b6b6b,color:#fff

  subgraph people["People, by role"]
    direction TB
    leads["Data Lead ·<br/>Technical Lead"]:::person
    eng["Engineers"]:::person
    stew["Stewards"]:::person
    users["Analysts · reviewers ·<br/>school and district staff"]:::person
    subjects["Learners · guardians ·<br/>the public"]:::person
  end

  platform["<b>Governed data platform</b><br/>operational databases, lakehouse,<br/>governance, reporting, products"]:::system

  subgraph outside["External systems"]
    direction TB
    idp["Identity provider"]:::ext
    src["Source systems<br/>legacy and operational"]:::ext
    gov["Other government<br/>systems"]:::ext
    ci["CI hosts<br/>one or more remotes"]:::ext
    infra["Cloud or cluster<br/>provider"]:::ext
    recip["External recipients<br/>researchers, other bodies"]:::ext
  end

  leads -->|approve trust changes,<br/>cutover, decommission| ci
  eng -->|propose changes| ci
  ci -->|plan and apply<br/>by federation| platform
  stew -->|own domains,<br/>approve access| platform
  users -->|collect, review,<br/>decide| platform
  subjects -->|own records,<br/>open statistics| platform
  idp -->|people and groups| platform
  src -->|files, federation,<br/>change capture| platform
  gov <-->|declared, reconciled<br/>feeds| platform
  platform -->|runs on| infra
  platform -->|de-identified shares| recip
```

### Why it is drawn this way

- **Changes reach the platform only through CI.** Engineers and leads act
  on the CI host, never on the platform directly
  ([P1](../principles.md#p1-ci-is-the-only-deployer)). The edge from people
  to the platform is for using it, not changing it.
- **CI hosts are plural.** A repository can live on more than one host; the
  architecture depends on federation, which every mainstream host offers,
  not on any one host ([CAP-REPOSITORIES.5](../capabilities/cap-repositories.md)).
- **Recipients are outside the boundary.** Data leaves only as
  de-identified publication ([P15](../principles.md#p15-publish-never-export)).
- **The identity provider is the organisation's,** not the platform's
  ([CAP-IDENTITY.1](../capabilities/cap-identity.md)). Learners, guardians
  and the public sign in separately and never join platform groups
  ([CAP-IDENTITY.6](../capabilities/cap-identity.md)).
- **Exchanges with other government systems run both ways** and are each
  declared and reconciled ([CAP-INTEROPERABILITY](../capabilities/cap-interoperability.md)).

## C2 Containers: trust and delivery

Each row is a layer and a repository. Every arrow from a repository to an
identity is a CI run that exchanges the CI host's per-run token for that
identity (federation); no arrow starts on a workstation.

```mermaid
---
config:
  flowchart:
    curve: step
    nodeSpacing: 40
    rankSpacing: 90
---
flowchart LR
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef box fill:#438dd5,stroke:#2e6295,color:#fff

  leads["Data Lead ·<br/>Technical Lead"]:::person

  subgraph L0["L0 Bootstrap: dispatch only, two approvals"]
    direction LR
    boot["Bootstrap<br/>repository"]:::box
    bootid["Bootstrap<br/>identity"]:::box
    state[("State store<br/>locked, versioned,<br/>encrypted")]:::box
    cids["CI identities<br/>and their federated<br/>credentials"]:::box
  end

  subgraph L1["L1 Platform: apply on merge"]
    direction LR
    plat["Platform repository<br/>stacks + tenant registry"]:::box
    platid["Platform<br/>identity"]:::box
    shared["Shared infrastructure<br/>network, secrets, catalog,<br/>storage, compute, guardrails"]:::box
  end

  subgraph L3["L3 Product: inside its tenant boundary"]
    direction LR
    prod["Product repository<br/>code, jobs, models, app"]:::box
    prodid["Product deploy<br/>identity"]:::box
    pres["Product resources<br/>schemas, jobs, app,<br/>database branches"]:::box
  end

  subgraph L2["L2 Modules: consumed by tag"]
    mods["Modules repository<br/>naming, building blocks"]:::box
  end

  leads -->|dispatch| boot
  boot -->|CI run| bootid
  bootid --> state
  bootid --> cids
  cids -.->|trusts one repository| platid
  cids -.->|trusts one repository| prodid
  plat -->|CI run| platid
  platid --> shared
  shared -->|grants, schemas,<br/>published outputs| pres
  prod -->|CI run| prodid
  prodid --> pres
  mods -.->|tagged source| plat
  mods -.->|tagged source| prod
```

### Why it is drawn this way

- **Rows are trust levels, and each row is a repository**
  ([P2](../principles.md#p2-repositories-are-split-by-trust-state-is-split-by-blast-radius)).
  A row's identity cannot act in another row, because its federated
  credential trusts one repository only.
- **The bootstrap row alone is dispatched by people.** It declares who CI
  is, so a merge alone must never change it
  ([P4](../principles.md#p4-the-root-of-trust-is-made-once-by-a-person-and-cannot-widen-itself)).
- **The platform reaches products only through what it generates from the
  tenant registry:** grants, schemas and published outputs. The product
  never reads platform state ([CAP-ONBOARDING.3](../capabilities/cap-onboarding.md)).
- **Modules and trust are dashed:** modules are source code and credentials
  are declarations, neither is a runtime call.

## C2 Containers: the data platform

```mermaid
---
config:
  flowchart:
    curve: step
    nodeSpacing: 40
    rankSpacing: 100
---
flowchart LR
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef box fill:#438dd5,stroke:#2e6295,color:#fff
  classDef ext fill:#999,stroke:#6b6b6b,color:#fff

  src["Source systems"]:::ext
  idp["Identity provider"]:::ext
  users["Analysts ·<br/>reviewers"]:::person
  recip["External<br/>recipients"]:::ext

  subgraph ingest["Ingestion"]
    direction TB
    landing[("Landing<br/>queue")]:::box
    archive[("Archive<br/>source of record")]:::box
    quar[("Quarantine")]:::box
  end

  subgraph product["Product"]
    direction TB
    reg[("Registries<br/>institutions, people,<br/>posts")]:::box
    collect["Collection<br/>returns and<br/>attestation"]:::box
    app["Product app<br/>behind sign-in"]:::box
    pipe["Pipeline jobs"]:::box
    oltp[("Operational DB<br/>Postgres, branched")]:::box
  end

  subgraph lake["Lakehouse"]
    direction TB
    catalog["Catalog<br/>grants, tags,<br/>row filters, masks"]:::box
    tables[("Open tables<br/>bronze · silver · gold")]:::box
    compute["Compute<br/>jobs and SQL"]:::box
    models["Transformation<br/>models + tests"]:::box
  end

  subgraph serve["Serving"]
    direction TB
    sem["Semantic layer"]:::box
    bi["Dashboards ·<br/>NL query"]:::box
    pub[("Publication<br/>catalog")]:::box
    portal["Open data<br/>portal"]:::box
  end

  subgraph gov["Governance"]
    direction TB
    audit[("Audit copy")]:::box
    ent[("Entitlements")]:::box
  end

  src -->|files| landing
  src -->|federation / CDC| catalog
  landing --> pipe
  pipe --> archive
  pipe --> quar
  pipe --> oltp
  app --> oltp
  users --> app
  oltp -->|read-only registration<br/>or governed extract| catalog
  catalog --> tables
  compute --> catalog
  models --> compute
  tables --> sem
  sem --> bi
  users --> bi
  models -->|de-identified| pub
  pub -->|open sharing protocol| recip
  pub --> portal
  collect --> oltp
  reg --> oltp
  users --> collect
  idp --> catalog
  ent --> catalog
  catalog --> audit
```

### Why it is drawn this way

- **The catalog sits in the middle** because every read and write of
  analytical data goes through it, which is what makes one set of policies
  enough ([CAP-CATALOG](../capabilities/cap-catalog.md),
  [CAP-COMPUTE.3](../capabilities/cap-compute.md)).
- **Landing feeds the pipeline, and the pipeline feeds archive and
  quarantine:** landing is a queue, not a store
  ([CAP-INGESTION.2](../capabilities/cap-ingestion.md)).
- **The product app talks only to its operational database.** Analytics
  reach that database through the catalog, never by a direct connection
  ([CAP-OPERATIONALDB.7](../capabilities/cap-operationaldb.md)).
- **Dashboards read the semantic layer, not tables,** so a measure has one
  definition ([P11](../principles.md#p11-reporting-goes-through-a-governed-transformation-layer)).
- **Publication is a separate store fed only by models,** so nothing reaches
  a recipient without passing through de-identification
  ([CAP-SHARING.1](../capabilities/cap-sharing.md)). Open statistics leave
  through the portal after disclosure control
  ([CAP-PUBLICATION](../capabilities/cap-publication.md)).
- **Registries and collection sit with the products** because they are
  operational: they hold the authoritative records and returns that
  everything downstream counts ([CAP-MASTERDATA](../capabilities/cap-masterdata.md),
  [CAP-COLLECTION](../capabilities/cap-collection.md)).

## C3 Components: access decision

How the catalog decides what one query returns.

```mermaid
---
config:
  flowchart:
    curve: step
    nodeSpacing: 40
    rankSpacing: 100
---
flowchart LR
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef box fill:#85bbf0,stroke:#5d82a8,color:#000
  classDef ext fill:#999,stroke:#6b6b6b,color:#fff

  user["Analyst"]:::person
  idp["Identity provider"]:::ext
  feed["Authoritative feed<br/>e.g. staff postings"]:::ext

  subgraph owners["Inputs, each with a different owner"]
    direction TB
    groups["Groups<br/>owner: platform team"]:::box
    ent[("Entitlement table<br/>owner: feed loader")]:::box
    tags["Classification tags<br/>owner: stewards"]:::box
  end

  subgraph decide["Decision, per query"]
    direction TB
    reach["Reach<br/>grants on catalog,<br/>schema, table"]:::box
    rows["Row filter<br/>one per table class"]:::box
    cols["Column masks<br/>one per classification"]:::box
    exempt["Exemption list<br/>pipeline identities only,<br/>each with a reason"]:::box
  end

  result["Rows and columns<br/>returned"]:::box
  audit[("Audit record")]:::box

  idp --> groups
  feed --> ent
  user --> reach
  groups --> reach
  reach --> rows
  ent --> rows
  rows --> cols
  tags --> cols
  exempt -.-> rows
  cols --> result
  result --> audit
```

### Why it is drawn this way

- **Three inputs, three owners**
  ([P14](../principles.md#p14-access-is-role--scope--sensitivity)): the
  platform team owns groups, a loader owns entitlements, stewards own
  classification. No one change widens all three
  ([CAP-ACCESS.6](../capabilities/cap-access.md)).
- **The decision is a chain that only narrows.** Reach admits the table;
  the row filter and masks can only remove from it
  ([CAP-ACCESS.3](../capabilities/cap-access.md)).
- **The exemption list is dashed and short.** Every entry is a path to raw
  data ([CAP-ACCESS.4](../capabilities/cap-access.md)).

## C3 Components: product pipeline

The example product's processing, from file to released result. The
[document-review product](../product/document-review.md) describes it in full.

```mermaid
---
config:
  flowchart:
    curve: step
    nodeSpacing: 35
    rankSpacing: 80
---
flowchart LR
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef box fill:#85bbf0,stroke:#5d82a8,color:#000
  classDef store fill:#438dd5,stroke:#2e6295,color:#fff

  landing[("Landing")]:::store

  subgraph nodb["Stages without a database connection"]
    direction LR
    norm["Normalise<br/>key = hash of bytes"]:::box
    fp["Fingerprint<br/>flag likely duplicates"]:::box
    read["Read<br/>measure, decide,<br/>score confidence"]:::box
  end

  subgraph withdb["The one stage with a database connection"]
    direction TB
    publish["Publish<br/>verdicts, events,<br/>provenance"]:::box
  end

  oltp[("Operational DB")]:::store
  review["Review queue<br/>leased items"]:::box
  reviewer["Reviewer"]:::person
  gate["Release gate<br/>BLOCKED / CLEAR"]:::box
  register[("Register<br/>snapshot")]:::store
  archive[("Archive")]:::store

  landing --> norm --> fp --> read --> publish
  publish --> oltp
  publish --> archive
  oltp --> review
  reviewer --> review
  review --> oltp
  oltp --> gate
  register --> gate
```

### Why it is drawn this way

- **Stages are separate jobs joined by storage,** so a stage cannot outrun
  the one before it, and each can be retried alone
  ([CAP-PIPELINE.3](../capabilities/cap-pipeline.md)).
- **Only publish touches the database.** The three stages before it keep
  working while the database is unavailable
  ([CAP-PIPELINE.6](../capabilities/cap-pipeline.md)).
- **Review sits beside the pipeline, not in it.** People decide at their own
  pace, and their decisions outrank any re-run
  ([CAP-REVIEW.3](../capabilities/cap-review.md)).
- **The gate reads both the database and the register snapshot,** because
  release needs the expected subjects as well as the results
  ([CAP-RELEASE.1](../capabilities/cap-release.md)).
