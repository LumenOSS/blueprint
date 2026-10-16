# Architecture

This page draws the architecture at three levels, using the C4 model. C1
shows the system in its context. C2 shows the containers inside it. C3 goes
into the components of the containers where most of the design lives.

Every box is a capability, or a group of capabilities, from the
[catalogue](../capabilities/README.md). You won't see any product names,
because choosing products is up to each implementation
([implementations](../implementations/README.md)).

The colours follow C4 conventions. People are dark blue, the system and its
containers are blue, and external systems are grey.

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

- Changes reach the platform only through CI. Engineers and leads work on
  the CI host, never on the platform directly
  ([P1](../principles.md#p1-ci-is-the-only-deployer)). So when you see an
  arrow from people to the platform, it means they use it, not that they
  change it.
- There can be more than one CI host. A repository can live on several
  hosts, because the architecture depends on federation, which every
  mainstream host offers, rather than on any one of them
  ([CAP-REPOSITORIES.5](../capabilities/cap-repositories.md)).
- Recipients sit outside the boundary, because data only leaves as a
  de-identified publication ([P15](../principles.md#p15-publish-never-export)).
- The identity provider belongs to the organisation, not to the platform
  ([CAP-IDENTITY.1](../capabilities/cap-identity.md)). Learners, guardians
  and the public sign in separately, and they never join platform groups
  ([CAP-IDENTITY.6](../capabilities/cap-identity.md)).
- Exchanges with other government systems run in both directions, and each
  one is declared and reconciled
  ([CAP-INTEROPERABILITY](../capabilities/cap-interoperability.md)).

## C2 Containers: trust and delivery

Each row here is a layer, and each layer is a repository. An arrow from a
repository to an identity is a CI run. The run exchanges the token the CI
host gives it for that identity, which is what federation means. Notice
that no arrow starts on a workstation.

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

- The rows are levels of trust, and each row is a repository
  ([P2](../principles.md#p2-repositories-are-split-by-trust-state-is-split-by-blast-radius)).
  One row's identity can't act in another row, because its federated
  credential trusts only one repository.
- Only the bootstrap row is started by people. It declares who CI is, so a
  merge on its own must never change it
  ([P4](../principles.md#p4-the-root-of-trust-is-made-once-by-a-person-and-cannot-widen-itself)).
- The platform reaches products only through what it generates from the
  tenant registry, meaning grants, schemas and published outputs. The
  product never reads the platform's state
  ([CAP-ONBOARDING.3](../capabilities/cap-onboarding.md)).
- The lines for modules and for trust are dashed because neither is a call
  at run time. Modules are source code, and credentials are declarations.

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

- The catalog sits in the middle because every read and write of
  analytical data goes through it. That's why one set of policies is
  enough ([CAP-CATALOG](../capabilities/cap-catalog.md),
  [CAP-COMPUTE.3](../capabilities/cap-compute.md)).
- Landing feeds the pipeline, and the pipeline feeds the archive and
  quarantine, because landing is a queue rather than a place to keep things
  ([CAP-INGESTION.2](../capabilities/cap-ingestion.md)).
- The product app talks only to its own operational database. Analytics
  reach that database through the catalog, never over a direct connection
  ([CAP-OPERATIONALDB.7](../capabilities/cap-operationaldb.md)).
- Dashboards read the semantic layer rather than tables, so each measure
  has one definition
  ([P11](../principles.md#p11-reporting-goes-through-a-governed-transformation-layer)).
  The [semantic layer](semantic-layer.md) page shows how that one
  definition reaches every consumer.
- Publication is a separate store, and only models write to it, so nothing
  reaches a recipient without going through de-identification
  ([CAP-SHARING.1](../capabilities/cap-sharing.md)). Open statistics leave
  through the portal after disclosure control
  ([CAP-PUBLICATION](../capabilities/cap-publication.md)).
- Registries and collection sit with the products because they're
  operational. They hold the authoritative records and returns that
  everything downstream counts
  ([CAP-MASTERDATA](../capabilities/cap-masterdata.md),
  [CAP-COLLECTION](../capabilities/cap-collection.md)).

## C3 Components: access decision

This is how the catalog decides what a single query returns.

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

- There are three inputs, and each has a different owner
  ([P14](../principles.md#p14-access-is-role--scope--sensitivity)). The
  platform team owns the groups, a loader owns the entitlements, and
  stewards own the classification. So no single change can widen all three
  ([CAP-ACCESS.6](../capabilities/cap-access.md)).
- The decision is a chain, and each step can only narrow it. Reach lets
  you at the table, and then the row filter and masks can only take things
  away ([CAP-ACCESS.3](../capabilities/cap-access.md)).
- The exemption list is dashed and kept short, because every entry on it
  is a path to raw data ([CAP-ACCESS.4](../capabilities/cap-access.md)).

## C3 Components: product pipeline

This is how the example product processes a file, from the moment it
arrives to the released result. The
[document-review product](../../guides/products/document-review.md) page
describes it in full.

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

- The stages are separate jobs joined by storage. So a stage can't get
  ahead of the one before it, and you can retry each one on its own
  ([CAP-PIPELINE.3](../capabilities/cap-pipeline.md)).
- Only the publish stage touches the database. The three stages before it
  keep working even when the database is unavailable
  ([CAP-PIPELINE.6](../capabilities/cap-pipeline.md)).
- Review sits beside the pipeline rather than inside it. People decide at
  their own pace, and their decisions outrank any re-run
  ([CAP-REVIEW.3](../capabilities/cap-review.md)).
- The gate reads both the database and the register snapshot, because
  before anything is released it needs to know which subjects were
  expected, as well as the results
  ([CAP-RELEASE.1](../capabilities/cap-release.md)).
