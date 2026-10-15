# Principles

The capability contracts in [`capabilities/`](capabilities/README.md) are
these principles made testable. When a contract and a principle seem to
disagree, the principle states the intent and the contract is the bug.

Each principle is followed by why the architecture holds it. The reasons
come from running the architecture with real data; where a reason is a
failure that happened, the [lessons](patterns/lessons.md) record its general
form.

## P1. CI is the only deployer

Every change to infrastructure or to a shared environment, including a
grant, a deletion or a migration against a shared database, is a reviewed
change whose plan the reviewer sees, applied by CI after merge. A
workstation formats, validates, plans, tests and builds; it never applies.
A deletion is two changes: adopt the object into code, then remove it.

**Why.** An apply from a workstation is a second writer. One writer gives
one audit trail and real state locking. When CI lacks a right, the fix is to
give CI's identity that right in one documented bootstrap step, never to
apply by hand.

## P2. Repositories are split by trust; state is split by blast radius

The platform has four layers, each its own repository: a small
**bootstrap** repository holding the trust anchors, a **platform**
repository holding shared infrastructure and the onboarding registry, a
**modules** repository of versioned building blocks, and one **product**
repository per product. Inside a repository, each stack has one state per
environment.

**Why.** With workload identity federation the repository is the unit of
trust: a federated credential names one repository, so in a monorepo anyone
who can edit a workflow reaches every identity. Repository boundaries answer
"who may change what, with which identity"; state boundaries answer blast
radius and change frequency.

## P3. Federation, not secrets

CI authenticates by exchanging the short-lived token its host issues for a
short-lived platform token. No client secret exists in any repository or CI
variable. Each federated credential trusts one repository and one protected
environment.

**Why.** A workflow on an unreviewed branch matches no credential and cannot
obtain a token, so editing a workflow file cannot escalate. Binding to an
environment rather than a branch moves the restriction to a place a pull
request cannot edit. Federation exists on every mainstream CI host, so the
design survives a change of host.

## P4. The root of trust is made once, by a person, and cannot widen itself

The identity that creates CI identities is created once by a person and
recorded in the bootstrap repository with its rights and its creator's role.
No identity applies the code that declares its own credentials. Bootstrap
applies are dispatched by hand, from the main branch, by an allow-listed
role, and apply the exact plan that was reviewed.

**Why.** An identity able to apply its own trust could add a credential
trusting any repository, handing its access to anyone who can merge.

## P5. Least privilege, enumerated

Identities hold the narrowest rights on named scopes. A right to assign
roles is conditioned to a listed set of roles; adding one is a reviewed
edit. Grants go to groups, never to people. Production objects are owned by
groups. Every exemption from a data policy is named with its reason.

**Why.** An unconditioned right to assign roles can assign itself owner.
Each policy exemption is a path to raw data.

## P6. Branch, never copy

Data reaches a development or test context by copy-on-write branching, not
by copying tables. Development, change testing, point-in-time inspection and
sandboxes are branches of production with a time to live. Production is a
protected branch.

**Why.** A branch gives every change a full, current copy of production in
seconds at no storage cost until it diverges. A copied dataset drifts the
day it is made, and every copy is one more place personal data lives.

## P7. Isolation without a second environment

The architecture works with production as the only funded environment.
Development is isolated inside it: database branches, development schemas
inside production catalogs with no consumer grants, and a protected
production branch. An environment is one template plus one values file, so
adding a funded development environment later is one file and one run.

**Why.** Many public bodies fund production only. The isolation that
matters (no development write reaches production data, no consumer reads
development output) can be enforced inside one environment.

## P8. Every write is idempotent

Delivery is at-least-once everywhere, so every consumer and every write is
idempotent. A document's identity is the hash of its bytes. Work that is
pending is recomputed from what exists rather than tracked in a cursor, so
a retried or overlapping run sees the same work and produces the same
result.

**Why.** Retries, redeliveries and overlapping runs are normal operation.
Idempotence makes them wasteful at worst, never wrong.

## P9. Determinism

The same input yields byte-identical output. Randomness, where needed, is
seeded explicitly per item from a hash of stable keys, never from time or
global state. Unordered collections are sorted before order can affect
output. Tests assert byte equality.

**Why.** Results that can be appealed must be reproducible. Determinism is
also what makes a backfill verifiable: re-running old input must reproduce
old output, or the difference must be attributable to a versioned change.

## P10. Low confidence goes to a person, never guessed

A machine verdict below its confidence threshold is routed to human review.
Thresholds live in one place. Removing a weak automated reader is better than
shipping its guesses.

**Why.** A low-confidence read presented as a read is worse than no read.
The same rule at platform level is the quality gate: data that fails its
checks is never used.

## P11. Reporting goes through a governed transformation layer

No report or metric is computed in an application. Operational data is read
by versioned, tested transformation models (bronze, silver, gold), and each
measure is defined once in a semantic layer that every dashboard,
natural-language query and agent reads.

**Why.** Conformance happens once, so every consumer shares one identifier
per entity and one definition per measure. Operational tables carry
bookkeeping no outside reader should depend on.

## P12. Provenance before any drop

Every table carries a governed provenance tag: `real`, `simulated` or
`derived`. Simulated data lives only in sandbox catalogs. Before anything is
dropped, each object's provenance is proved one by one from first-hand
evidence: its comment, the change that created it, its loader. A schema, a
repository or a summary is not evidence. Recoverable drops are preferred to
cascading ones.

**Why.** A schema believed to be simulated can hold real records beside
simulated ones, and nothing on a table says which is which unless a tag
does.

## P13. Roles, not names

Documents, diagrams and configuration name roles, never people. Authority
belongs to roles: the **Data Lead** and the **Technical Lead** share
sign-off of cutover, rollback and decommission; either may halt; a
decommission needs both.

**Why.** Knowledge and authority held by named individuals leave with them.
A role can be reassigned without editing the system.

## P14. Access is role × scope × sensitivity

Identity-provider groups decide reach (which catalogs and actions). An
entitlement table derived from an authoritative feed decides row scope. A
governed classification tag decides column visibility. Each of the three is
changed by a different owner.

**Why.** No single change can widen access across all three.

## P15. Publish, never export

External parties receive only de-identified or aggregated tables from a
separate publication catalog, over an open sharing protocol, each share
approved and registered. Researchers who need finer data work inside the
platform, per project and time-boxed. Nothing leaves as a file attachment.

**Why.** Sharing does not carry access policies to the recipient, so
protection must be in the published data itself. An emailed extract has no
record, no revocation and no way to tell whether two analyses used the same
data.

## P16. Open formats, storage separate from compute, federate before copying

Data at rest is in open formats. Compute scales to zero. A source that
cannot move is queried in place before anything is copied; change data
capture is used only where a copy is worth its cost; a custom extract is the
last resort. A periodic exit test proves the data can be read without the
current vendor.

**Why.** Portability is a property that decays unless it is tested.

## P17. Measure; do not reconstruct from memory

Claims about a live system are measured, with the command and result
recorded. A green status is not evidence; read the rows. Every error and its
mitigation is appended to an append-only error log.

**Why.** The costliest mistakes are confident reconstructions. A policy that
silently returns zero rows looks exactly like a working read that found
nothing.

## P18. Append-only records, expand-then-contract change

Published artefacts, policy versions, decisions and events are append-only;
rollback is re-pointing. Schemas evolve by expand, then contract; one
migration is one phase. Interfaces evolve additively; a changed shape is a
new route.

**Why.** Anything rewritten in place loses the evidence of what was true
before, and a contract change that is not additive breaks a running reader.

## P19. Every task is a pinned, host-independent recipe

Every repository pins its toolchain and has a task runner. Every task,
locally and in CI, is one recipe invoked the same way, and CI definitions
only call recipes.

**Why.** The same commit produces the same tools and the same result on any
machine, and changing CI host rewrites only a thin wrapper.
