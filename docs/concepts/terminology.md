# Terminology

The specifications use a handful of classifications over and over. Once
you know them, the rest of the blueprint is much easier to read. You'll
find every other term either in the
[glossary](../specifications/glossary.md) or in the vocabulary of its
bounded context, which the [context map](../../CONTEXT-MAP.md) lists.

## Sensitivity tiers

We tag every table with one tier. The tier decides who may see the
table, where it's stored, and whether it may be published.

| Tier | Name | EMIS example | In short |
| --- | --- | --- | --- |
| T0 | Public aggregate | Enrolment by district, published | Anyone may see it |
| T1 | Internal | The list of institutions and their facilities | Staff of the authority |
| T2 | De-identified | Learner records with names removed and identifiers replaced | Approved analysts and partners |
| T3 | Identifiable | A learner's name, birth date and enrolment | Only those with a need and the right scope |
| T4 | Special category | Health, disability, child-protection records | Named people, each grant approved by a steward, in separate storage |

The tiers are defined in [CAP-CLASSIFICATION](../specifications/capabilities/cap-classification.md).

## Provenance

Every table also says where its data came from. Its provenance is
**real** if the data is about real people and institutions, **simulated**
if it was made up for testing, or **derived** if it was computed from
other tables. We don't delete anything until its provenance is proven.

## Bronze, silver and gold

Data passes through three stages on its way to being used.

| Stage | Holds | Example |
| --- | --- | --- |
| Bronze | Data exactly as received | A census return file, unchanged |
| Silver | Data checked and made consistent | Returns with codes validated and institutions matched to the registry |
| Gold | Data ready to use | Enrolment counts by grade and district, as at census day |

Reports and indicators only ever read from gold.

## Reference date and academic period

An **academic period** is a school year or a term.

A **reference date** is the single day that a statistic describes, such
as census day. Counting everything "as at" one date is what makes figures
comparable.

## Layers

The platform is built in four layers. Each layer is trusted less than
the one below it, and each lives in its own repository.

| Layer | Name | Holds |
| --- | --- | --- |
| L0 | Bootstrap | The root of trust, made once by a person |
| L1 | Platform | Shared storage, compute, catalog, identity and governance |
| L2 | Modules | Reusable building blocks |
| L3 | Products | Workloads such as a census or document review |

## Capabilities, clauses and bindings

A **capability** is something the platform must be able to do, such as
`CAP-ACCESS`.

Each capability has a **contract**, which is a list of numbered
**clauses**, such as `CAP-ACCESS.7`. Every clause has a level, used in the
sense of [BCP 14](https://www.rfc-editor.org/info/bcp14). **MUST** means
it's required. **SHOULD** means it's required unless there's a recorded
reason not to. **MAY** means it's optional. Every clause also says how you
show that you conform to it.

An **implementation** is a real platform that meets the contracts. Its
**binding** gives every clause one of these statuses:

| Status | Means |
| --- | --- |
| planned | Not yet shown |
| met | Shown, with evidence |
| deviation | Will not be met; the consequence is recorded |
| not-applicable | Does not apply, with the reason |

## Roles

Our documents name roles, never people.

| Role | Responsible for |
| --- | --- |
| Data Lead | What data is held and released; shares sign-off with the Technical Lead |
| Technical Lead | How the platform is built and run; shares sign-off with the Data Lead |
| Steward | One domain's data, and who may see it |
| Platform team | Identity groups, shared infrastructure and the delivery pipeline |
| Operator | Whoever carries out a procedure |

## Domains and environments

A **domain** is an area of data that has one steward, such as `learners`
or `workforce`. Each domain is a catalog.

An **environment** is a separate world for a change to run in, such as
production or a developer's branch. Catalogs are named
`<domain>_<environment>`, for example `learners_prod`.

You're now ready for the [specifications](../specifications/README.md).
