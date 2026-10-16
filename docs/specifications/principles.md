# Principles

The capability contracts in [`capabilities/`](capabilities/README.md) are
these principles made testable. So if a contract and a principle ever seem
to disagree, trust the principle: it states the intent, and the contract is
the thing that needs fixing.

Each principle comes with the reason we hold it. The reasons come from
running the architecture with real data. Where a reason is a failure that
actually happened, the [lessons](../guides/lessons.md) record it in general
form.

## P1. CI is the only deployer

Every change to infrastructure or to a shared environment goes through a
reviewed change, and CI applies it after merge. That includes grants,
deletions and migrations against a shared database, and the reviewer sees
the plan before approving. A workstation can format, validate, plan, test
and build, but it never applies. Even a deletion takes two changes: first
you adopt the object into code, then you remove it.

**Why.** An apply from a workstation is a second writer. With only one
writer, you get one audit trail and state locking that actually works. If
CI lacks a right it needs, you give CI's identity that right in one
documented bootstrap step. You don't apply by hand instead.

## P2. Repositories are split by trust; state is split by blast radius

The platform has four layers, and each is its own repository. A small
**bootstrap** repository holds the trust anchors. A **platform** repository
holds shared infrastructure and the onboarding registry. A **modules**
repository holds versioned building blocks. And each product has its own
**product** repository. Inside a repository, each stack keeps one state per
environment.

**Why.** With workload identity federation, the repository is the unit of
trust, because a federated credential names exactly one repository. In a
monorepo, anyone who can edit a workflow can reach every identity.
Repository boundaries decide who may change what, and with which identity.
State boundaries limit how much one change can break, and keep things that
change often apart from things that rarely do.

## P3. Federation, not secrets

CI authenticates by exchanging the short-lived token its host issues for a
short-lived platform token. There's no client secret in any repository or
CI variable. Each federated credential trusts one repository and one
protected environment.

**Why.** A workflow running on an unreviewed branch matches no credential,
so it can't obtain a token, and editing a workflow file can't escalate
anyone's access. Binding the credential to an environment rather than a
branch puts the restriction somewhere a pull request can't edit. And since
every mainstream CI host supports federation, the design survives a change
of host.

## P4. The root of trust is made once, by a person, and cannot widen itself

A person creates the identity that creates CI identities, once, and records
it in the bootstrap repository along with its rights and the role of whoever
created it. No identity ever applies the code that declares its own
credentials. Bootstrap applies are started by hand, from the main branch, by
a role on an allow-list, and they apply exactly the plan that was reviewed.

**Why.** An identity that could apply its own trust could add a credential
trusting any repository. That would hand its access to anyone able to merge
there.

## P5. Least privilege, enumerated

Identities hold the narrowest rights they need, on named scopes. A right to
assign roles is limited to a listed set of roles, and adding a role to that
list is a reviewed edit. Grants go to groups, never to people, and groups
own production objects. Every exemption from a data policy is named, with
its reason.

**Why.** A right to assign any role can assign itself owner. And every
exemption from a policy is another path to raw data.

## P6. Branch, never copy

Data reaches a development or test context through copy-on-write branching,
not by copying tables. Development, change testing, point-in-time inspection
and sandboxes are all branches of production with a time to live.
Production itself is a protected branch.

**Why.** A branch gives every change a full, current copy of production in
seconds, and it costs no storage until it diverges. A copied dataset starts
drifting the day it's made, and every copy is one more place where personal
data lives.

## P7. Isolation without a second environment

The architecture works when production is the only funded environment.
Development is isolated inside it, using database branches, development
schemas inside production catalogs that no consumer has grants on, and a
protected production branch. An environment is one template plus one values
file, so if you fund a development environment later, adding it takes one
file and one run.

**Why.** Many public bodies fund production only. The isolation that really
matters can be enforced inside one environment: no development write
reaches production data, and no consumer reads development output.

## P8. Every write is idempotent

Delivery is at-least-once everywhere, so every consumer and every write is
idempotent. A document's identity is the hash of its bytes. Pending work is
worked out again from what exists, rather than tracked in a cursor, so a
retried or overlapping run sees the same work and produces the same result.

**Why.** Retries, redeliveries and overlapping runs are part of normal
operation. Because every write is idempotent, the worst they can do is waste
some effort. They can't make anything wrong.

## P9. Determinism

The same input gives byte-identical output. Where randomness is needed, it's
seeded explicitly for each item from a hash of stable keys, never from the
time or from global state. Unordered collections are sorted before their
order can affect the output, and tests check for byte equality.

**Why.** If people can appeal a result, you have to be able to reproduce it.
Determinism is also what lets you verify a backfill: re-running old input
must give the old output, or else the difference must come from a versioned
change you can point to.

## P10. Low confidence goes to a person, never guessed

When a machine's verdict falls below its confidence threshold, it goes to a
person for review. The thresholds live in one place. It's better to remove a
weak automated reader than to ship its guesses.

**Why.** A low-confidence reading presented as a real one is worse than no
reading at all. At the platform level, the same rule is the quality gate:
data that fails its checks is never used.

## P11. Reporting goes through a governed transformation layer

No report or measure is computed inside an application. Versioned, tested
transformation models read the operational data (bronze, then silver, then
gold), and each measure is defined once, in a semantic layer that every
dashboard, natural-language query and agent reads from.

**Why.** Data is made consistent once, so every consumer shares one
identifier for each entity and one definition for each measure. Operational
tables also carry bookkeeping that no outside reader should depend on.

## P12. Provenance before any drop

Every table carries a governed provenance tag: `real`, `simulated` or
`derived`. Simulated data lives only in sandbox catalogs. Before anything is
dropped, you prove each object's provenance, one object at a time, from
first-hand evidence: its comment, the change that created it, and its
loader. A schema, a repository or someone's summary isn't evidence. And
where you have a choice, prefer a drop you can recover from to one that
cascades.

There's only one way to remove real personal data, and that's scheduled
disposal at the end of its retention period, reviewed and audited
([CAP-RECORDS](capabilities/cap-records.md)).

**Why.** A schema everyone believes is simulated can hold real records next
to simulated ones, and nothing on a table tells you which is which unless a
tag does. Scheduled disposal is the opposite case. Keeping data about
children longer than its purpose needs is a harm in itself, so disposal has
its own approved path rather than being an exception to this one.

## P13. Roles, not names

Documents, diagrams and configuration name roles, never people. Authority
belongs to roles too. The **Data Lead** and the **Technical Lead** share
sign-off of cutover, rollback and decommission. Either of them may halt one,
and a decommission needs both.

**Why.** When knowledge and authority belong to named individuals, they
leave when those people do. A role can be handed to someone else without
editing the system.

## P14. Access is role × scope × sensitivity

Identity-provider groups decide reach, meaning which catalogs a person can
use and what they can do there. An entitlement table, derived from an
authoritative feed, decides which rows they see. A governed classification
tag decides which columns they see. A different owner changes each of the
three.

**Why.** Because the three have different owners, no single change can
widen access across all of them.

## P15. Publish, never export

Aggregate statistics are published openly for anyone to read, with
disclosure control and permanent identifiers. Partners who need row-level
data get only de-identified tables, from a separate publication catalog,
over an open sharing protocol, and each share is approved and registered.
Researchers who need finer data work inside the platform, on a project that
has a time limit. A person's own records reach them, or their guardian,
through a logged disclosure tied to a purpose. Nothing leaves as an ad-hoc
file attachment.

**Why.** Access policies don't travel with shared data, so the protection
has to be built into the published data itself. An emailed extract leaves
no record, can't be revoked, and gives you no way to tell whether two
analyses used the same data.

**Grounded in** the [UN Fundamental Principles of Official Statistics](standards.md#official-statistics-and-disclosure-control) and the [International Open Data Charter](standards.md#open-data-and-exchange).

## P16. Open formats, storage separate from compute, federate before copying

Data at rest is kept in open formats, and compute scales to zero. If a
source can't move, you query it where it is before copying anything. Change
data capture is only for cases where a copy is worth what it costs, and a
custom extract is the last resort. A periodic exit test proves that the data
can be read without the current vendor.

**Why.** Portability wears away unless you test for it.

## P17. Measure; do not reconstruct from memory

Any claim about a live system is measured, and the command and its result
are recorded. A green status isn't evidence, so read the rows. Every error,
with its mitigation, is added to an append-only error log.

**Why.** The most expensive mistakes are confident reconstructions. A policy
that silently returns zero rows looks exactly like a working query that
found nothing.

## P18. Append-only records, expand-then-contract change

Published artefacts, policy versions, decisions and events are append-only,
so rolling back means pointing at an earlier version. Schemas change by
expanding first and contracting later, and each migration is one of those
phases. Interfaces only grow by addition, so a changed shape becomes a new
route.

**Why.** Anything rewritten in place loses the evidence of what used to be
true. And a contract change that isn't additive breaks readers that are
already running.

## P19. Every task is a pinned, host-independent recipe

Every repository pins its toolchain and has a task runner. Each task, both
locally and in CI, is one recipe that you run the same way everywhere, and
CI definitions do nothing except call recipes.

**Why.** The same commit gives the same tools and the same result on any
machine, and moving to a different CI host only means rewriting a thin
wrapper.

## P20. Collect for a declared purpose

Every personal-data element has a declared purpose and legal basis, an
owner, and at least one process or measure that uses it. If nothing uses an
element, it's proposed for removal at its periodic review. Special-category
data is collected only where its purpose requires it.

**Why.** An education system can ask for almost anything about a child and
their family, and every element it collects is one more to protect, keep
and eventually dispose of. Declaring the purpose up front is what lets you
answer for decisions about minimisation, retention and access.

**Grounded in** the purpose-legitimacy and data-minimisation principles of [ISO/IEC 29100](standards.md#identity-security-and-privacy) and the people-first data practices of the [Principles for Digital Development](standards.md#open-source-health-and-digital-public-goods).

## P21. The education authority runs its own platform

Each platform instance is run by the education authority whose data it
holds, on infrastructure the authority controls or contracts for directly.

**Why.** Responsibility for learners' data can't be delegated away, and an
authority that doesn't control where its data lives can't answer for it.

**Grounded in** the [Principles for Digital Development](standards.md#open-source-health-and-digital-public-goods), and aiming to meet the [Digital Public Goods Standard](standards.md#open-source-health-and-digital-public-goods).

## P22. Every language is a first language

The platform and its documentation work in more than one language. Text is
written once, in a source language, and translated through translation
files, never by copying pages. Every coded value has a label in each
official language, and right-to-left scripts are laid out right to left. If
a translation has fallen behind its source, it isn't shown, and readers see
the source instead.

**Why.** Many education authorities work in more than one official
language. The people an EMIS serves, such as guardians, teachers and the
public, shouldn't need a second language to read their own data or the rules
that govern it. Translations kept as copies of pages drift without anyone
noticing, but translations kept as files of strings show exactly what
changed.

**Grounded in** [BCP 47](standards.md#data-representation) language tags, [Unicode CLDR](standards.md#accessibility-and-localisation) locale data and the [GNU gettext PO](standards.md#accessibility-and-localisation) translation format.
