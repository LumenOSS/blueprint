# Lessons as design rules

Each rule below comes from a failure that happened while running this
architecture with real data, stated in its general form. They are the
reasons behind many of the [principles](../principles.md) and contract
clauses; when a rule looks over-cautious, it is because its absence once
cost something.

## Measuring and verifying

1. Tuning and measurement harnesses call the real production code path. A
   missing required input raises; it never falls back silently.
2. Calibrate a detector's positive class on independent real-world captures
   (different devices, damaged copies), not on clean re-renders of the same
   source.
3. A processing chain encodes assumptions about its target. Re-validate
   every stage when re-aiming it, because deleted signal and absent signal
   look the same downstream.
4. No mitigation counts as done until a measurement on representative data
   shows its effect.
5. "Deployed" is a claim about the running process. Verify it by asking the
   live system for a marker only the new version emits.
6. Check the artefact itself (deployed state, filled tables), never a status
   line or a cached plan.
7. A configuration the schema accepts is not proof of behaviour. Read the
   deployed object back to confirm it, and delete inert configuration that
   looks authoritative.

## Idempotency, delivery and concurrency

1. Deduplicate at two independent layers: the orchestrator rejects a
   duplicate run identifier, and the work short-circuits on terminal state.
2. Write to a temporary location and move into place atomically, so a replay
   never sees a half-finished output.
3. Human decisions outrank redeliveries in upsert guards. Guards test the
   condition that makes an operation wrong, not a status label.
4. Test every migration on a database it has already been applied to;
   "idempotent" is a claim about the second run. Never cache schema facts
   indefinitely.
5. Enforce mutual exclusion in the database: a unique key, and select and
   acquire in one statement. Check the lease before the first write.
6. Judge health from a heartbeat, not from process statistics. Isolate
   per-item failures (quarantine and continue) so one poisoned input cannot
   wedge the pipeline.
7. Chain stages by hand-off so fallback paths are unreachable. A job's
   timeout is at least the sum of its tasks' budgets.
8. Each statement against a transactional table format is a commit. Batch
   into set-based operations and keep tail work at a constant number of
   round trips.

## Stores and data of record

1. Before anything empties a store, establish whether it is the source of
   record. Archive successes, dead-letter rejects with a reason, and derive
   locations from content hashes.
2. Keep one manifest of what a secondary store carries, derive sync and lag
   checks from it, and test that every reporting source has a writer.
3. Reconcile primary and secondary stores. A job's success says nothing
   about a write it made after its own commit.
4. Never deploy from an uncommitted tree. Alert on data freshness, not only
   on job failure.
5. Validate references against the authoritative registry with a foreign
   key. Constrain bad history going forward rather than rewriting it.

## Identity, grants and infrastructure as code

1. A declarative permission block is the complete set: it revokes whatever
   it does not list. Confirm a hypothesis with read-only queries against the
   live system before acting on it.
2. An identity is not configuration. Recreating a resource can mint a new
   principal, so parameterise principals and keep code that verifies every
   layer of grants.
3. Version privileges alongside the schema, including default privileges for
   objects that future migrations create.
4. Size a deploy identity for what it must create, make it the owner of what
   it deploys, and copy deployment state rather than file trees.
5. Check privileges before the first run under a new identity. A right to
   manage without a right to create is a drop with no undo.
6. Declare an explicit dependency between a permission and its first use.
   One green apply may have been lucky ordering.
7. Plan and apply share their state and path parameters from one definition.
   Run the first apply where failure is cheap.
8. Scope credentials to the single step that needs them.
9. Render environment-specific artefacts from the deployment tool's resolved
   output, and expose on a health endpoint the environment each service
   believes it is in.

## Data protection and provenance

1. Prove provenance per object before any destructive drop. A schema or a
   repository is not a unit of provenance.
2. Write exclusion rules by kind of data (spreadsheets, exported learner lists), not
   by remembered file names.
3. Normalise external identities once, at the boundary, and enforce the
   normal form with a constraint.

## Failure signalling

1. Make missing data loud (strict undefined) and pin the strictness with a
   test.
2. Keep "refused bad input" and "system broken" in separate counters and
   statuses.
3. A tolerated failure matches and names the specific error it tolerates.
4. Every path that produces a stored derived value calls one
   implementation, and fallback paths are exercised by tests.
5. Every recurring job has a seconds-long "nothing to do" exit on the
   cheapest compute. Automation never starts paid compute without consent.
