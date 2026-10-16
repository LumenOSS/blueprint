# Lessons as design rules

Every rule on this page comes from something that went wrong while this
architecture was running with real data. We've written each one in its
general form. Many of the [principles](../specifications/principles.md) and
contract clauses exist because of them. So if a rule looks over-cautious,
it's because not following it once cost us something.

## Measuring and verifying

1. Tuning and measurement harnesses call the real production code path.
   If a required input is missing, they raise an error; they never quietly
   fall back to something else.
2. Calibrate a detector's positive class on independent real-world
   captures, such as different devices and damaged copies, not on clean
   re-renders of the same source.
3. A processing chain carries assumptions about what it's aimed at. When
   you re-aim it, re-validate every stage, because downstream you can't
   tell a signal that was deleted from one that was never there.
4. A mitigation isn't done until a measurement on representative data
   shows that it works.
5. "Deployed" is a claim about the running process. To check it, ask the
   live system for a marker that only the new version emits.
6. Check the thing itself, such as the deployed state or the filled
   tables, and not a status line or a cached plan.
7. Just because the schema accepts a configuration doesn't prove it does
   anything. Read the deployed object back to confirm it, and delete any
   inert configuration that looks as if it's in charge.

## Idempotency, delivery and concurrency

1. Remove duplicates at two independent layers. The orchestrator rejects a
   run identifier it has already seen, and the work itself stops early if
   it finds a terminal state.
2. Write to a temporary location and then move the result into place in
   one atomic step, so a replay never sees half-finished output.
3. In upsert guards, a human decision outranks a redelivery. A guard tests
   the condition that would make the operation wrong, not a status label.
4. Test every migration on a database it has already been applied to,
   because "idempotent" is a claim about the second run. Never cache facts
   about the schema indefinitely.
5. Enforce mutual exclusion in the database, with a unique key, and select
   and acquire in a single statement. Check the lease before the first
   write.
6. Judge health from a heartbeat, not from process statistics. Isolate
   failures item by item, by quarantining the bad item and carrying on, so
   one poisoned input can't jam the whole pipeline.
7. Chain stages by handing work from one to the next, so fallback paths
   can't be reached. A job's timeout is at least the sum of its tasks'
   budgets.
8. With a transactional table format, every statement is a commit. So
   batch work into set-based operations, and keep the work at the end of a
   run to a fixed number of round trips.

## Stores and data of record

1. Before anything empties a store, find out whether it's the source of
   record. Archive what succeeded, send rejects to a dead-letter location
   with a reason, and derive locations from content hashes.
2. Keep one manifest of what a secondary store holds. Derive the sync and
   lag checks from it, and test that every reporting source has something
   writing to it.
3. Reconcile primary and secondary stores. A job reporting success tells
   you nothing about a write it made after its own commit.
4. Never deploy from a tree with uncommitted changes. Alert when data goes
   stale, not only when a job fails.
5. Validate references against the authoritative registry with a foreign
   key. Rather than rewriting bad history, stop new bad records from
   being added.

## Identity, grants and infrastructure as code

1. A declarative permission block is the complete set, so it revokes
   anything it doesn't list. Before you act on a hypothesis, confirm it
   with read-only queries against the live system.
2. An identity isn't configuration. Recreating a resource can create a new
   principal, so pass principals in as parameters, and keep code that
   verifies every layer of grants.
3. Version privileges alongside the schema, including the default
   privileges for objects that future migrations will create.
4. Give a deploy identity exactly the rights it needs to create what it
   deploys, make it the owner of what it deploys, and copy deployment state
   rather than trees of files.
5. Check privileges before the first run under a new identity. A right to
   manage something without the right to create it can turn into a drop
   you can't undo.
6. Declare an explicit dependency between a permission and the first thing
   that uses it. One successful apply may just have been lucky ordering.
7. Plan and apply take their state and path parameters from one shared
   definition. Run the first apply somewhere a failure is cheap.
8. Scope credentials to the single step that needs them.
9. Render environment-specific artefacts from the deployment tool's
   resolved output, and have each service report, on a health endpoint,
   which environment it believes it's in.

## Data protection and provenance

1. Before any destructive drop, prove the provenance of each object
   separately. A schema or a repository isn't a unit of provenance.
2. Write exclusion rules by kind of data, such as spreadsheets or exported
   learner lists, not by file names someone remembers.
3. Normalise external identities once, at the boundary, and enforce the
   normal form with a constraint.

## Failure signalling

1. Make missing data fail loudly, for example with strict undefined
   values, and pin that strictness with a test.
2. Keep "refused bad input" and "system broken" in separate counters and
   separate statuses.
3. A tolerated failure matches, and names, the specific error it
   tolerates.
4. Every path that produces a stored derived value calls the same single
   implementation, and tests exercise the fallback paths.
5. Every recurring job has a quick "nothing to do" exit, taking seconds on
   the cheapest compute. Automation never starts paid compute without
   consent.
