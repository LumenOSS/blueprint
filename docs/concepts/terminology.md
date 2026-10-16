# Terminology

The specifications use a handful of classifications over and over. Learn
these and the rest of the blueprint reads easily. Every other term is in
the [glossary](../specifications/glossary.md) or in the vocabulary of its
bounded context, listed in the [context map](../../CONTEXT-MAP.md).

## Sensitivity tiers

Every table is tagged with one tier. The tier decides who may see it,
where it is stored and whether it may be published.

| Tier | Name | EMIS example | In short |
| --- | --- | --- | --- |
| T0 | Public aggregate | Enrolment by district, published | Anyone may see it |
| T1 | Internal | The list of institutions and their facilities | Staff of the authority |
| T2 | De-identified | Learner records with names removed and identifiers replaced | Approved analysts and partners |
| T3 | Identifiable | A learner's name, birth date and enrolment | Only those with a need and the right scope |
| T4 | Special category | Health, disability, child-protection records | Named people, each grant approved by a steward, in separate storage |

Defined in [CAP-CLASSIFICATION](../specifications/capabilities/cap-classification.md).

## Provenance

Every table also says where its data came from: **real** (about real
people and institutions), **simulated** (made up, for testing) or
**derived** (computed from other tables). Nothing is deleted until its
provenance is proven.

## Bronze, silver and gold

Data passes through three stages on its way to being used:

| Stage | Holds | Example |
| --- | --- | --- |
| Bronze | Data exactly as received | A census return file, unchanged |
| Silver | Data checked and made consistent | Returns with codes validated and institutions matched to the registry |
| Gold | Data ready to use | Enrolment counts by grade and district, as at census day |

Reports and indicators read only from gold.

## Reference date and academic period

- An **academic period** is a school year or term.
- A **reference date** is the single day a statistic describes, such as
  census day. Counting "as at" one date is what makes figures comparable.

## Layers

The platform is built in four layers, each trusted less than the one
below and each in its own repository.

| Layer | Name | Holds |
| --- | --- | --- |
| L0 | Bootstrap | The root of trust, made once by a person |
| L1 | Platform | Shared storage, compute, catalog, identity and governance |
| L2 | Modules | Reusable building blocks |
| L3 | Products | Workloads such as a census or document review |

## Capabilities, clauses and bindings

- A **capability** is something the platform must be able to do, such as
  `CAP-ACCESS`.
- Its **contract** is a list of numbered **clauses**, such as
  `CAP-ACCESS.7`. Each clause has a level: **MUST** (required), **SHOULD**
  (required unless there is a recorded reason) or **MAY** (optional), in
  the sense of [BCP 14](https://www.rfc-editor.org/info/bcp14). Each says
  how conformance is shown.
- An **implementation** is a real platform that meets the contracts. Its
  **binding** gives every clause a status:

| Status | Means |
| --- | --- |
| planned | Not yet shown |
| met | Shown, with evidence |
| deviation | Will not be met; the consequence is recorded |
| not-applicable | Does not apply, with the reason |

## Roles

Documents name roles, never people.

| Role | Responsible for |
| --- | --- |
| Data Lead | What data is held and released; shares sign-off with the Technical Lead |
| Technical Lead | How the platform is built and run; shares sign-off with the Data Lead |
| Steward | One domain's data, and who may see it |
| Platform team | Identity groups, shared infrastructure and the delivery pipeline |
| Operator | Whoever carries out a procedure |

## Domains and environments

- A **domain** is an area of data with one steward, such as `learners`
  or `workforce`. Each is a catalog.
- An **environment** is a separate world for a change to run in, such as
  production or a developer's branch. Catalogs are named
  `<domain>_<environment>`, for example `learners_prod`.

You are ready for the [specifications](../specifications/README.md).
