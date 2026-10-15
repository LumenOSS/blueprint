# Backfill patterns

How to load history, reprocess after a logic change, fill gaps after an
outage, and onboard a source with years of history, without duplicates,
loss, or harm to production. The contract these patterns serve is
[CAP-BACKFILL](../capabilities/cap-backfill.md); section 8 maps each of its
clauses to the invariants that prove it.

The chapter is vendor-neutral. Each pattern ends with a one-line mapping to
(a) an open-source stack and (b) Databricks. Citations are numbered `[n]`
and resolved in the references; sources were checked on 2026-10-15, and
anything marked **[unverified]** was not confirmed against a primary source.

## 1. Scope and vocabulary

A **backfill** is any run that writes data for a period or key range other
than "the newest slice", or that rewrites data already published. This
chapter covers four situations that look different but share mechanics:

| Situation | What changes | Typical size | Main risk |
| --- | --- | --- | --- |
| **S1. Historical load from a legacy system** | A new home for years of old records | Whole history, once | Bad legacy data, wrong mapping, no way to check |
| **S2. Reprocessing after a logic change** | The code, not the inputs | Whole history or a window | Mixed old/new results; consumers see a half-done state |
| **S3. Gap fill after an outage** | Missing input slices | Hours to weeks | Duplicates, or overwriting fresher data |
| **S4. Onboarding a new source with history** | A new input, old and live at once | Years plus a live stream | Seam between the bulk copy and the live feed |

Two systems are in scope: the **analytical platform** (lake/lakehouse
tables, transformations, marts) and the **operational systems** that feed it
or are fed by it (OLTP Postgres and similar). The patterns differ because an
operational database serves live traffic during the backfill and cannot be
taken offline.

**Terms used throughout.**

- *Event time*: when the thing happened in the world. *Processing time*:
  when the system saw it. [1]
- *Valid time*: when a fact is true in the modelled world. *Transaction
  time*: when the database recorded it. A table that keeps both is
  *bitemporal*. [10][11]
- *Slice*: the unit a backfill writes atomically: a partition, a date range,
  a key range, a batch.
- *Natural key*: an identifier that comes from the domain (student ID, sheet
  hash), not a surrogate generated at load time.
- *Logic version*: the identifier of the code and configuration that
  produced a row.

---

## 2. Decision guide

Read the left column, find your situation, and start with the named
patterns. Section numbers point to the pattern catalogue (section 4).

| If you need to... | Use | Avoid | Why |
| --- | --- | --- | --- |
| Re-run a date range of a derived table (S2, S3) | **4.1 Slice replacement** + **4.10 Orchestrated backfill** | Appending the re-run output | Overwriting a whole slice makes the run idempotent; appends double-count |
| Load or correct entities that have stable keys but no time partition | **4.2 Keyed upsert with recency guard** | Blind `UPDATE`/`INSERT` | MERGE on a natural key is idempotent; the guard stops old data clobbering new |
| Pull new and changed rows from a source that has an `updated_at` | **4.3 High-water mark with overlap** — only if you can live with its gaps; else 4.4 | A strict `>` on the last max timestamp | Transaction-start timestamps and clock skew make `updated_at` non-monotonic in commit order |
| Onboard a live OLTP source with full history (S4) | **4.4 Snapshot + log stitching** (DBLog / incremental snapshot) | Snapshot, then "start CDC from now" | The seam between the two loses or duplicates rows unless it is reconciled per key |
| Make an operational service emit history and new events reliably | **4.5 Transactional outbox** | Dual writes to DB and broker | Dual writes are not atomic; outbox is |
| Recompute everything with new logic (S2) without consumers seeing a half-done table | **4.6 Shadow recompute and swap** + **4.12 Logic version stamping** | In-place rewrite of the live table | Readers keep the old answer until the new one is complete and checked |
| Gate any large backfill on quality before anyone sees it | **4.7 Write-audit-publish** on a branch or staging table | Publishing and then testing | Bad data never becomes visible; publishing is a pointer move |
| Prove the backfill is complete and correct | **4.8 Reconciliation** (counts, sums, hashes) and, for logic changes, **parallel-run diff** | "The job succeeded" | Success means the code ran, not that the data is right |
| Read years of history from a production source | **4.9 Throttled, chunked extraction** from a replica or snapshot | One big `SELECT *` on the primary | Long scans starve live traffic and hold back vacuum/replication |
| Late or corrected records keep arriving for closed periods | **4.11 Restatement with lookback** + bitemporal columns | Treating a closed period as frozen forever | Completeness is a heuristic; restatement must be visible and attributable |
| Add or change a column on a busy Postgres table and fill it | **5.1 Expand / backfill in batches / contract** | One `UPDATE` over the whole table | One transaction locks rows, bloats the table and blocks vacuum |
| Rehearse an operational backfill against real data | **5.2 Copy-on-write branch rehearsal** | Rehearsing on a stale, hand-made copy | Branches give production-shaped data at no copy cost |
| Replace a legacy system (S1) | **6.1 Strangler fig** + **6.2 initial load + CDC cutover** + **6.3 parallel run** + **6.4 quarantine** | Big-bang cutover with no fallback | Incremental cutover limits blast radius; the old system remains the fallback |

**Ordering rule of thumb.** Dimensions (and reference data) before facts;
parents before children; within a table, choose oldest-first when later
slices depend on earlier state (SCD type 2, running balances, cumulative
metrics), and newest-first when consumers value recent data most and
slices are independent (section 4.10).

---

## 3. First principles

These are the ideas the patterns rest on. Each is stated as a claim, with
the source it comes from.

### 3.1 Event time is not processing time, and completeness is a guess

Akidau et al. separate *event time* from *processing time* and argue that a
system processing unbounded, out-of-order data "will never know if or when
we have seen all of our data, only that new data will arrive, old data may
be retracted" [1]. The Dataflow Model makes the trade-off explicit with
four questions: *what* is computed, *where* in event time (windows), *when*
in processing time results are emitted (triggers, driven by watermarks), and
*how* refinements relate (discarding, accumulating, or
accumulating-and-retracting panes) [1].

*Consequences for backfills.* (a) Partition by event time, not load time, or
a re-run of "yesterday" means nothing stable. (b) A *watermark* is a
heuristic statement that input for a time range is probably complete;
backfills exist largely because that heuristic is sometimes wrong. (c) When a
backfill changes a previously emitted result, downstream needs either a
replacement of the whole result (discarding/overwrite) or an explicit
retraction. Silent in-place mutation is neither.

### 3.2 The log is the source of truth; tables are projections

Kreps: a log of all changes "from the beginning" is a complete
representation of a dataset; tables and indexes are projections of it, and
can be rebuilt by replaying it [2]. In "Questioning the Lambda
Architecture" he proposes *Kappa* reprocessing: when logic changes, start a
second instance of the job from the beginning of the retained log, write to
a **new** output table, switch readers when it catches up, then delete the
old job and table [3]. This removes the Lambda requirement to maintain the
same logic twice (batch and speed layers) [3][4].

Helland makes the general case: immutable data is what lets distributed
systems coordinate, and updatable stores are layered on immutable files
(LSM trees, copy-on-write) [5].

*Consequence.* Keep raw inputs immutable and retained long enough to replay.
If the raw input is gone, a logic-change backfill (S2) is impossible, and
you are restating from a derived table, which carries forward its errors.

### 3.3 Functional data engineering: pure tasks over immutable partitions

Beauchemin (2018) applies functional programming to batch pipelines [6]:
tasks are *pure* (same inputs give the same output, no side effects beyond
writing their own target), *idempotent*, and write *immutable partitions*
that are replaced whole, never mutated. Raw data goes in a *persistent
staging area* kept indefinitely so any partition can be recomputed;
slowly changing dimensions are handled by snapshotting dimensions per
partition rather than mutating rows. With these rules, a backfill is just
running the same task for older partitions.

### 3.4 Idempotency and exactly-once *effects*

Delivery across a network is at-least-once in practice; "exactly once"
is achieved as an *effect* by making the write idempotent [7][8]. Helland
defines idempotence as an operation whose repetition has the same effect as
doing it once, and argues it is a requirement in any system that retries
messages [7]. Practical ways to get it:

- **Deterministic keys.** Derive the row key from the content or the
  domain (natural key, or a hash of stable fields), never from load time or
  a sequence assigned during the load. A retried load then produces the same
  keys and a MERGE or overwrite makes it a no-op.
- **Slice replacement.** Replace the whole slice atomically (section 4.1).
- **Commit tokens.** Record the (job id, slice id or version) inside the
  same atomic commit as the data, and skip a commit whose token is already
  present. Delta Lake's `txnAppId`/`txnVersion` options do exactly this:
  a write with a version at or below the last recorded one for that app id
  is ignored [16].

### 3.5 Determinism of transformations

A backfill is only comparable to the original run if the transformation is
deterministic: same inputs and same logic version produce byte-identical
(or at least row-identical) outputs. Sources of non-determinism to remove:
wall-clock reads (`now()`), unseeded randomness, iteration over unordered
containers, `LIMIT` without `ORDER BY`, floating-point aggregation order,
"latest" lookups resolved at run time rather than as of the slice's event
time, and dependence on the run date rather than the slice date. Determinism
is what makes parallel-run diffs (section 4.8) meaningful: any diff is then
caused by logic or input, not noise. (First principles; no single source.)

### 3.6 Bitemporal modelling

Snodgrass distinguishes *valid time* (when a fact holds in reality) from
*transaction time* (when the database knew it) and shows how to model,
query and correct both in SQL [10]. SQL:2011 standardised application-time
period tables (valid time), system-versioned tables (transaction time) and
bitemporal tables combining both [11].

*Why backfills need it.* A backfill that corrects history is a *transaction
time* event about *valid time* facts. Without both axes you cannot answer
"what did we report for March, as of the April board meeting?", and a
restatement erases the evidence of what was previously published. Lakehouse
table formats give you transaction time for free at table granularity (time
travel to a snapshot) but not per row; per-row `recorded_at` /
`superseded_at` columns are needed when consumers must see corrections
explicitly.

### 3.7 Slowly changing dimensions

Kimball's SCD types [12]: type 1 overwrites the attribute (history lost);
type 2 adds a row with effective dates (history kept); type 3 adds a
"previous value" column; types 0, 4, 5, 6 and 7 are variants and hybrids
(DT #152). For backfills the rule is: **a type 2 dimension must be
backfilled in event-time order**, because each new version closes the
previous one. Loading out of order either produces overlapping validity
ranges or requires a rebuild of the key's whole history. A safe alternative
is to rebuild the full type 2 history for affected keys from the immutable
change log in one pass (Beauchemin's "dimension snapshots" [6] give the
same result without ordering constraints).

### 3.8 Recompute versus incremental maintenance

The view-maintenance literature frames the choice: a derived table can be
fully recomputed, or maintained incrementally from deltas of its inputs
[13]. Incremental maintenance is cheaper per change but is only correct for
certain classes of view (for example, aggregates that are self-maintainable
under inserts, but not always under deletes or updates), and it accumulates
any past error. Full recompute is always correct relative to its inputs and
logic but costs proportional to history size.

*Rule.* Normal operation may be incremental; **a logic change (S2) requires
recompute** of every slice the change affects, because incremental
maintenance applies the new logic only to new deltas. Many orchestration
tools (dbt `--full-refresh`, microbatch with an explicit range) are
interfaces to this choice [21][22].

---

## 4. Pattern catalogue: analytical platform

Each pattern uses the same fields: **Problem**, **Forces**, **Solution**,
**Consequences**, **Verification**, **Sources**, and **Maps to** (a)
open-source stack, (b) Databricks.

### 4.1 Slice replacement (partition overwrite)

**Problem.** Re-running a time slice of a derived table (S2, S3) must not
double-count or leave stale rows.

**Forces.** Appends are cheap but not idempotent. Row-level deletes before
insert are two operations and can half-fail. Readers must never see the
slice empty or doubled.

**Solution.** Treat the slice (partition or predicate range) as the unit of
work. Compute the full slice, then atomically replace exactly that slice in
one commit: `INSERT OVERWRITE` with dynamic partition overwrite, or an
overwrite with an explicit predicate (`replaceWhere`). The predicate must be
the same one the computation used to select inputs.

**Consequences.** Re-runs are idempotent and order-independent across
slices. The slice must be computable from inputs alone (pure task, 3.3). It
does not suit tables without a natural slice. Danger: in Spark's default
**static** overwrite mode, an `INSERT OVERWRITE` without a `PARTITION`
clause replaces **all** partitions; Iceberg's docs show it dropping every
row in the table while writing one day [17]. Use dynamic mode or an
explicit predicate, always. Iceberg recommends `MERGE INTO` over dynamic
overwrite because overwritten scope can change if partitioning evolves [17].

**Verification.** Row count and checksum of the slice before and after;
assert that rows outside the predicate are unchanged (compare snapshot
diffs: the commit must touch only files of that slice); run the backfill
twice and assert identical outputs.

**Sources.** [6][16][17].

**Maps to.** (a) Spark + Iceberg with
`spark.sql.sources.partitionOverwriteMode=dynamic`, or Delta
`replaceWhere`; dbt `insert_overwrite` strategy. (b) Delta `replaceWhere`
/ `INSERT INTO ... REPLACE WHERE`, dynamic partition overwrite; Delta
`txnAppId`/`txnVersion` for commit-level idempotency.

### 4.2 Keyed upsert with recency guard

**Problem.** Loading or correcting entities identified by a key (students,
schools, sheets), where the backfill may carry older versions than what is
already there.

**Forces.** MERGE is idempotent only if keys are deterministic. A backfill
running alongside live ingestion can overwrite a fresher row with a stale
one. Duplicate keys in the source make MERGE fail or be non-deterministic.

**Solution.** `MERGE` on the **natural key**. Add a **recency guard** to the
update clause: update only if the incoming version is newer by a monotonic
version field (source LSN, source commit sequence, record version), e.g.
`WHEN MATCHED AND s.src_version > t.src_version THEN UPDATE`. Deduplicate
the source per key first (keep the highest version) so at most one source
row matches each target row. For deletes, carry tombstones with a version
rather than inferring deletion from absence.

**Consequences.** Safe to run concurrently with live ingestion and safe to
repeat. Requires a trustworthy version field; wall-clock `updated_at` is a
weak substitute (see 4.3). MERGE rewrites files containing matched rows, so
large backfills via MERGE can be slower than slice replacement.

**Verification.** For a sample of keys, assert the target holds the
max-version row from all sources. Re-run and assert zero changed rows. Count
of keys in target = count of distinct keys in sources minus tombstoned.

**Sources.** [7][17]; Iceberg notes MERGE requires at most one source row
per target row [17].

**Maps to.** (a) Iceberg/Delta `MERGE INTO`; dbt incremental `merge` with
`unique_key`; Postgres `INSERT ... ON CONFLICT (key) DO UPDATE ... WHERE
excluded.v > t.v`. (b) Delta `MERGE INTO`; Lakeflow declarative pipelines'
`AUTO CDC` / `APPLY CHANGES` with a sequencing column does the same guarded
upsert **[mapping not re-checked against current docs]**.

### 4.3 High-water-mark incremental extract (with overlap)

**Problem.** Pull only new or changed rows from a source table.

**Forces.** Cheap and simple; needs only an `updated_at` or monotonically
increasing id. But commit order is not timestamp order.

**Solution.** Record the high-water mark (HWM) after each successful load.
Next run reads `updated_at >= HWM - overlap`, deduplicates on key and
version, and upserts (4.2). Advance the HWM only after the write commits,
and only to `min(max_seen, now - safety_lag)`. Prefer a commit-ordered
cursor where the source has one (log sequence number, Postgres `xmin`-based
cursors, a sequence assigned at commit by an outbox).

**Consequences.** Without overlap, rows are lost: in Postgres, `now()`
returns the *start time of the transaction* [18], so a long transaction that
starts at 10:00 and commits at 10:05 writes `updated_at = 10:00`; if the
extractor ran at 10:02 and advanced its HWM to 10:02, the row is never seen.
Clock skew across application servers has the same effect [9]. Hard deletes
are invisible to HWM extraction. Overlap creates duplicates, so the sink
must be idempotent (4.2).

**Verification.** Periodic full-key reconciliation between source and sink
(4.8): count and key-set comparison per day. Alert if the HWM stops moving
or moves backward.

**Sources.** [9][18]; first principles.

**Maps to.** (a) Airflow/Dagster task with a stored cursor; dbt incremental
models with `is_incremental()` filter on `>=` and a lookback. (b) Same in
Lakeflow Jobs; prefer Lakeflow Connect CDC for databases where available.

### 4.4 Snapshot and log stitching (onboarding a live source)

**Problem.** Onboard a live OLTP source with years of history (S4): you need
a full copy plus every change after it, with no gap and no lost update at
the seam, and without locking the source.

**Forces.** A consistent full snapshot of a big table takes hours. Locking
tables for that time is not acceptable. Starting CDC "after" the snapshot
leaves a gap; starting it "before" creates overlaps that must be resolved
per key. Snapshot must be resumable.

**Solution.** DBLog (Netflix) [14]: keep the change-log stream running
continuously. Snapshot the table in **chunks** ordered by primary key. For
each chunk, write a *low watermark* event into the log (via a small
watermark table in the source), select the chunk, write a *high watermark*.
When the log reader reaches the high watermark, it drops from the chunk any
row whose key appeared in log events between low and high, because the log
event is newer, and emits the rest of the chunk before continuing. No locks,
the log never stalls, and chunks can be paused and resumed. Debezium's
incremental snapshots implement the same algorithm, triggered by inserting
an `execute-snapshot` signal (optionally with an `additional-conditions`
filter) into a signalling table; chunk size defaults to 1,024 rows and
progress is stored in connector offsets so the snapshot resumes after a
crash [15][19].

**Consequences.** Requires primary keys. Consumers see a mix of `read` and
`update` events for the same key in non-obvious order, so downstream must
be an idempotent keyed upsert (4.2) [15]. Adds a watermark/signal table to
the source schema. Can also re-snapshot a subset (a table, a key range) to
repair a gap, which makes it a gap-fill tool (S3) as well as an onboarding
tool.

**Verification.** After snapshot completion, reconcile row count and a key
hash per table (or per key range) between source (read from a replica at a
known LSN) and sink (4.8). Check that the replication slot lag returned to
baseline.

**Sources.** [14][15][19].

**Maps to.** (a) Debezium on Kafka/Kafka Connect or Debezium Server →
Iceberg/Delta via MERGE; Postgres logical replication slots. (b) Lakeflow
Connect for supported databases (it manages the initial snapshot and CDC);
otherwise Debezium into a landing zone and declarative-pipeline CDC upsert
**[Lakeflow Connect internals not verified]**.

### 4.5 Transactional outbox

**Problem.** An operational service must publish its changes (and, for
onboarding, its history) to the platform reliably.

**Forces.** Writing to the database and to a broker are two non-atomic
operations ("dual write"); either can fail after the other succeeds.
Distributed transactions are rarely available or desirable.

**Solution.** Write the business change and an event row to an `outbox`
table **in the same database transaction**. A relay (poller or log-based
CDC on the outbox table) publishes outbox rows in commit order [20]. For
history, the service (or a one-off job) writes synthetic "snapshot" events
for existing entities into the same outbox, keyed and versioned like live
events, so history and live use one path.

**Consequences.** At-least-once: the relay can publish a row twice after a
crash, so consumers must be idempotent [20]. Ordering is preserved per
aggregate. The outbox needs pruning. Developers can forget to write the
event.

**Verification.** Consumers record the last processed event id per
aggregate; reconcile counts of outbox rows versus consumed events per day.

**Sources.** [20][14] (DBLog's motivation section rejects dual writes for
the same reason).

**Maps to.** (a) Postgres outbox table + Debezium outbox event router.
(b) Lakebase table as outbox + CDC/sync to Delta **[Lakebase-to-Delta sync
mechanics not re-verified here]**.

### 4.6 Shadow recompute and swap (blue/green tables)

**Problem.** Recompute a whole table with new logic (S2) without consumers
seeing a half-updated mix of old and new results, and with a way back.

**Forces.** In-place rewrites expose partial states and destroy the old
answer. Recompute takes time; live data keeps arriving during it.

**Solution.** Kreps' Kappa reprocessing generalised [3]: run the new logic
from the beginning of retained input into a **new** table (or a branch,
4.7), let it catch up with live input, compare it with the old output
(4.8), then switch consumers by an atomic pointer change (a view
redefinition, a catalog alias, a branch fast-forward, or a table rename).
Keep the old table for a defined fallback window, then drop it.

**Consequences.** Double storage and compute during the overlap. Readers
see either all-old or all-new. Requires that raw inputs are retained (3.2).
Consumers that cached results need a restatement notice (4.11).

**Verification.** Parallel-run diff (4.8): every difference between old and
new must be explained by the logic change. A diff of zero on the slices
the change should not affect is a strong regression test.

**Sources.** [3][2][4].

**Maps to.** (a) New Iceberg table or branch, swap via view or catalog
rename; dbt with a versioned model (`v2`) and a view that points at the
active version. (b) Delta table per version, consumers read through a
Unity Catalog view; swap by `CREATE OR REPLACE VIEW`.

### 4.7 Write-audit-publish (WAP) on a branch

**Problem.** A backfill writes a lot of data; any defect becomes visible to
consumers the moment it commits.

**Forces.** Quality checks need the data written somewhere first. Copying
data to staging and back doubles I/O. Publication should be atomic.

**Solution.** **Write** to an isolated version of the table (a branch, a
staging table, or a hidden snapshot); **audit** it with data-quality checks
and reconciliation; **publish** by an atomic metadata operation. The pattern
was popularised by Netflix (DataWorks Summit 2017, "Whoops, the numbers are
wrong! Scaling data quality @ Netflix") **[unverified]**.
In Iceberg: set `write.wap.enabled=true`, create an audit branch, set
`spark.wap.branch`, write, validate, then
`CALL system.fast_forward('db.t', 'main', 'audit-branch')` [21a]. Nessie
extends branches to **multi-table** commits, so a backfill that touches a
dimension and its fact tables publishes atomically across all of them [23].

**Consequences.** Publication is a pointer move, so rollback is too.
Branches have retention; the audit branch must not expire before publish.
Single-table branches do not give cross-table atomicity; consumers may see
the new dimension with the old facts unless you publish together or use a
multi-table catalog.

**Verification.** The audit step is the verification: schema checks,
null/uniqueness constraints, reconciliation totals, distribution drift
against the previous version. Deequ-style declarative constraints run as
aggregation queries are one systematic form [24].

**Sources.** [21a][23][24]; Netflix talk **[unverified]**.

**Maps to.** (a) Iceberg branches + `fast_forward`; Nessie for multi-table;
lakeFS is an alternative for file-level branching. (b) Delta has no table
branches: use a **shallow clone** as the write target, audit it, then
publish with `replaceWhere`/MERGE or a view swap. Note shallow clones
reference source files and break if the source is `VACUUM`ed [25]. Delta
time travel gives rollback after publish.

### 4.8 Reconciliation and parallel-run diff

**Problem.** Proving a backfill is complete and correct.

**Forces.** Full row-by-row comparison across systems is expensive. Legacy
and new systems encode things differently (types, time zones, codes). Job
success says nothing about data.

**Solution.** Three tiers, cheapest first:

1. **Counts** per slice (date, school, source file) in source and target.
2. **Control totals**: sums of additive measures, min/max of keys and
   timestamps, count of distinct keys, per slice.
3. **Hashes**: per-row hash of the canonicalised business columns, then an
   order-independent aggregate (e.g. sum or XOR of row hashes, or a Merkle
   tree over key ranges) per slice; drill into mismatching slices only.

For logic changes, run old and new logic in parallel on the same inputs and
**diff** outputs per key; classify each difference as expected (caused by
the change) or a defect. GitHub's Scientist library applies the same idea to
code paths in production; Stripe used it while migrating hundreds of
millions of subscription records [26][27].

**Consequences.** Canonicalisation must be agreed (trim, case, time zone,
decimal scale), or every row mismatches. Hash tiers miss nothing they cover
but say nothing about columns excluded from the hash. Reconciliation must
read the source at a known consistent point (a replica at an LSN, a frozen
extract), or it races live writes.

**Verification.** The reconciliation report is itself an artefact: stored
with the backfill run id, logic version and the source position it was
computed against.

**Sources.** [24][26][27]; Fowler/Thoughtworks on parallel running [28].

**Maps to.** (a) SQL queries or a diffing tool over both sides; Great
Expectations / Deequ / dbt tests for constraints. (b) Same via Databricks
SQL; Lakehouse Federation lets one query read the legacy database and Delta
side by side **[federation coverage of a given legacy DB not verified]**.

### 4.9 Throttled, chunked extraction (protect the source)

**Problem.** Reading years of history from a production database or a
rate-limited API without hurting live users.

**Forces.** Big scans evict cache, saturate I/O, and on MVCC databases a
long-running read transaction holds back vacuum and can bloat tables. APIs
enforce rate limits. A failed eight-hour extract that restarts from zero is
wasteful.

**Solution.** Read from a **replica**, a **snapshot/backup restore**, or a
**branch** (5.2) instead of the primary. Split the work into **chunks** by
primary-key range (not `OFFSET`), each a short transaction; persist the last
completed chunk so the job resumes. **Throttle** on feedback signals:
replication lag, source CPU/latency, API `429`/`Retry-After`, and back off
exponentially. Make throttle parameters adjustable while running. gh-ost is
the reference design: pausable, throttles on replica lag and custom checks,
with chunk size and max lag changeable at runtime [29]. Stripe avoided
production queries entirely by backfilling from offline Hadoop snapshots
[27].

**Consequences.** Slower wall-clock time, by design. Chunked reads are not
a single consistent snapshot; combine with log stitching (4.4) or read from
a frozen copy when you need consistency.

**Verification.** Monitor source latency and replica lag during the run;
the backfill should be invisible on production dashboards. Reconcile per
chunk.

**Sources.** [27][29][14].

**Maps to.** (a) Airflow/Dagster with pools or concurrency limits; reads
from a Postgres read replica. (b) Lakeflow Jobs with limited concurrency;
read from a Lakebase child branch or read replica, not the production
branch's primary compute.

### 4.10 Dependency-aware orchestrated backfill

**Problem.** A backfill spans many slices and many dependent tables; it
must run in the right order, at bounded concurrency, and resume after
partial failure.

**Forces.** Downstream slices depend on upstream slices. Unbounded
parallelism starves production schedules. Some slices are independent and
can run in any order; some (SCD2, running totals) cannot.

**Solution.** Let the orchestrator own the backfill as a first-class object:

- **Airflow 3**: backfills are created through CLI, API or UI and run by the
  scheduler; a `reprocess_behavior` of `none`, `failed` or `completed`
  decides whether existing runs are re-run; a backfill-level
  `max_active_runs` bounds concurrency independently of the DAG's own
  limit; `--run-backwards` processes newest first; dry-run lists the
  intervals [30].
- **Dagster**: partitioned assets with a `BackfillPolicy`:
  `single_run()` processes a partition range in one run (efficient for
  Spark/warehouse engines; code must read `partition_key_range`), while
  `multi_run(max_partitions_per_run=n)` bounds each run; multi-asset
  backfills follow the asset graph when partitioning is compatible [31][32].
- **dbt** (≥1.9): `microbatch` incremental strategy with `event_time`,
  `batch_size`, `begin`, `lookback`; targeted backfills by
  `--event-time-start/--event-time-end`; `dbt retry` re-runs only failed
  batches; batches are independent and may run concurrently; times are UTC
  [22]. `--full-refresh` rebuilds an incremental model from scratch [21].

Order: **reference data and dimensions before facts**; within a table,
**oldest-first** when a slice depends on the previous slice's state,
**newest-first** when slices are independent and recent data is most
valuable (users get useful results sooner, and a stopped backfill leaves
the oldest, least-used data missing rather than the newest).

**Consequences.** The orchestrator's unit (a run per logical date) must
match the data's unit (a slice); otherwise the backfill is not idempotent.
Backfill concurrency must be budgeted against production schedules.

**Verification.** Dry-run lists exactly the intended slices. After the run,
the orchestrator's state (all slices succeeded) agrees with the data's
state (reconciliation per slice).

**Sources.** [21][22][30][31][32].

**Maps to.** (a) Airflow 3 backfill / Dagster partitions / dbt microbatch.
(b) Lakeflow Jobs **backfill runs** trigger one job run per interval over a
range, optionally in parallel, overriding job parameters; the job must use
those parameters to select its slice [33]; dbt tasks in Lakeflow Jobs for
microbatch.

### 4.11 Late data and restatement

**Problem.** Records keep arriving for periods already reported (S3), or a
correction changes a published number.

**Forces.** Consumers want stable numbers. Completeness is a heuristic
(3.1). Regulators or boards may need to know what was reported when.

**Solution.** (1) Reprocess a **lookback** window on every run (dbt
`lookback`, Airflow interval overlap), so lateness within the window is
absorbed automatically [22]. (2) Beyond the window, late data triggers an
explicit **restatement**: a backfill of the affected slices through the
normal path (4.1/4.10), recorded as an event. (3) Keep **transaction time**
on published outputs (table snapshots at minimum; row-level `recorded_at`
or bitemporal columns where consumers need to see corrections) [10][11].
(4) Publish a restatement log: which slices, why, old and new totals,
logic version.

**Consequences.** Numbers change after publication, visibly and with a
reason. Lookback costs compute every run.

**Verification.** For each restated slice, the restatement log shows old
and new control totals and links to the run id; time travel to the
pre-restatement snapshot reproduces the old number.

**Sources.** [1][10][11][22].

**Maps to.** (a) dbt microbatch `lookback`; Iceberg tags to pin
"as-reported" snapshots. (b) Delta time travel and table history; dbt
microbatch; a restatement log table.

### 4.12 Logic version stamping

**Problem.** After a backfill, outputs produced by different code coexist;
nobody can tell which rows came from which logic.

**Forces.** Partial backfills are normal. Debugging and audit require
attribution.

**Solution.** Stamp every output row (or at least every slice) with the
**logic version** (pipeline version string or code commit) and the **run
id**. Treat a change that alters outputs as a version bump (semantic
versioning or equivalent), and make the backfill scope "all slices whose
stamped version is older than the target version". Store run metadata
(inputs' versions/snapshot ids, logic version, parameters) in a run table.

**Consequences.** A cheap query answers "is the backfill complete?":
`SELECT count(*) WHERE logic_version <> :target`. Restated results become
attributable. Costs one or two columns.

**Verification.** Invariant check after every backfill: no slice in the
target range carries a stale version.

**Sources.** First principles; aligns with lineage practice (OpenLineage
run facets) **[not cited to a specific spec section]**.

**Maps to.** (a) A column set by the job from its build version; dbt
`invocation_id` and a project var. (b) Same; Unity Catalog lineage gives
table/column lineage but not per-row logic version, so the column is still
needed.

### 4.13 Schema evolution during a backfill

**Problem.** The schema of source or target changes while a long backfill
is running, or history contains old schema versions.

**Forces.** Old records lack new fields; renamed fields break positional
loaders; type widening is safe, narrowing is not.

**Solution.** Freeze the target schema for the duration of a backfill, or
apply only additive changes (new nullable columns, type widening) that both
old and new code tolerate (expand/contract, 5.1). Map each historical
source schema version explicitly to the target schema with a versioned
mapping; do not rely on positional or "by name, best effort" merges.
Configure incremental tools to fail on unexpected schema change rather than
silently drop columns (dbt `on_schema_change: fail`) **[unverified]**.

**Consequences.** A schema change mid-backfill becomes a planned step, not
a surprise. Table formats that support column ids (Iceberg, Delta column
mapping) make renames safe.

**Verification.** Schema snapshot taken at backfill start equals the one at
the end, or differs only by recorded additive changes.

**Sources.** [34]; first principles.

**Maps to.** (a) Iceberg schema evolution by column id; dbt
`on_schema_change`. (b) Delta schema evolution (`mergeSchema`), column
mapping mode for renames.

---

## 5. Pattern catalogue: operational databases

### 5.1 Expand, backfill in batches, contract

**Problem.** Add or change a column on a large, busy table and fill it for
existing rows without downtime.

**Forces.** Most `ALTER TABLE` forms take an `ACCESS EXCLUSIVE` lock [35].
A single `UPDATE` over millions of rows is one long transaction: it holds
row locks, creates a dead tuple per row, and holds back vacuum. Application
versions old and new run side by side during deploys.

**Solution.** Parallel change (expand / migrate / contract) [36]:

1. **Expand.** Add the new column as nullable, or with a *non-volatile*
   default, which in modern Postgres does not rewrite the table [35]. Set a
   short `lock_timeout` on the DDL so a blocked `ALTER` fails fast instead
   of queueing all traffic behind it. Deploy code that writes both old and
   new forms.
2. **Backfill in batches.** Update by primary-key ranges of a few thousand
   rows, each in its own short transaction, sleeping between batches and
   throttling on replication lag (4.9). Make each batch idempotent
   (`WHERE new_col IS NULL`). Record progress.
3. **Constrain without long locks.** Add constraints `NOT VALID`, then
   `VALIDATE CONSTRAINT`, which takes only `SHARE UPDATE EXCLUSIVE` [35].
   Build indexes `CONCURRENTLY`.
4. **Migrate reads**, then **contract**: stop writing the old form, drop it
   once nothing reads it.

Tools automate this. **pgroll** serves old and new schema versions at once
through views, backfills new columns in batches, keeps old and new columns
in sync with triggers during the migration, and supports start / complete /
rollback [37]. **gh-ost** (MySQL) copies into a ghost table while tailing
the binlog, throttles, and supports `--test-on-replica` [29]. Stripe's
four-step dual-write migration is the application-level version [27].

**Consequences.** Several deploys instead of one. A window in which both
forms must be kept consistent. Triggers (pgroll) add write overhead.

**Verification.** `SELECT count(*) WHERE new_col IS NULL` reaches zero;
spot-check equivalence of old and new forms; monitor lock waits and
replication lag during the run.

**Sources.** [27][29][35][36][37].

**Maps to.** (a) Postgres + pgroll, or hand-written batches from Airflow /
Dagster / a migration tool. (b) Lakebase is Postgres: the same applies;
run migrations through CI against a branch first (5.2).

### 5.2 Rehearse on a copy-on-write branch

**Problem.** An operational backfill or migration must be tested against
production-shaped data, at production size, before it touches production.

**Forces.** Full copies of big databases are slow and expensive; stale
copies hide the very edge cases that break migrations; testing on
production is risky.

**Solution.** Create a **copy-on-write branch** of the production database
(at the current point or a past point in time), run the migration and
backfill there, measure duration, lock waits and output, then run the same
script against production. Neon and Databricks Lakebase branches share
storage pages with the parent and only store changes; creation time does
not depend on database size and does not load the parent [38][39].

**Consequences.** Rehearsal becomes routine. Branch compute differs from
production compute, so timings are indicative, not exact. Branches contain
production data, so access to them needs the same controls as production.

**Verification.** Rehearsal produces the same row counts and checks that
the production run will be held to; production run is aborted if it
diverges materially from the rehearsal.

**Sources.** [38][39].

**Maps to.** (a) Neon branches; for vanilla Postgres, restore a snapshot
or use a ZFS/LVM clone. (b) Lakebase branches; the same pattern for Delta
is a shallow clone (4.7).

### 5.3 Logical replication for initial sync

**Problem.** Seed a new Postgres (or move to a new cluster) with an
existing database's data, then keep it in sync until cutover.

**Solution.** Create a publication on the source and a subscription on the
target. By default the subscription **copies existing table data** and then
streams changes; temporary table-synchronization slots are created for the
initial copy and dropped when it completes [40]. Cut over when lag is near
zero: stop writes on the source, wait for lag to reach zero, switch
writers, keep the old side as fallback.

**Consequences.** Schema (DDL) is not replicated; apply it on both sides.
Sequences need resetting at cutover. Initial copy of large tables loads the
source; replication slots hold WAL if the subscriber falls behind and can
fill the source's disk.

**Verification.** Per-table row counts and hash reconciliation at a
quiesced point before cutover (4.8).

**Sources.** [40].

**Maps to.** (a) Postgres native logical replication. (b) Lakebase
supports Postgres logical replication for inbound sync **[not verified for
the current Lakebase release]**.

---

## 6. Pattern catalogue: legacy migration

### 6.1 Strangler fig

**Problem.** Replace a legacy system that holds years of history without a
risky big-bang cutover.

**Solution.** Build the new system beside the old one and move behaviour
and data across in increments, keeping transitional architecture (adapters,
event interception) that lets both coexist; retire the old parts as they
stop being used [41][28]. For data: migrate one domain, one region or one
cohort at a time; each increment uses 6.2–6.4.

**Consequences.** Temporary code that will be deleted; a longer period
with two systems. Each increment is small enough to roll back.

**Sources.** [41][28].

### 6.2 Initial load plus CDC cutover (or frozen source)

**Problem.** Move history and keep up with ongoing changes until cutover.

**Solution.** Two variants:

- **Live source.** Snapshot-and-log stitching (4.4) or logical replication
  (5.3): bulk-load history, stream changes, reconcile, cut over when lag
  is near zero.
- **Frozen source.** When the legacy system has no usable change log, agree
  a **freeze point**: the legacy system becomes read-only (or a
  point-in-time extract is taken), history up to the freeze is loaded,
  reconciled and signed off, then writers switch to the new system. Any
  write after the freeze goes only to the new system.

**Consequences.** Frozen-source cutovers need a write outage or a business
process pause, but are simplest to verify: there is one fixed source
state to reconcile against. Live cutovers avoid the outage but must
reconcile a moving target at a known log position.

**Verification.** Reconciliation (4.8) at the freeze point or at a recorded
log position; sign-off recorded with the report.

**Sources.** [14][15][40]; first principles.

### 6.3 Parallel run and fallback window

**Problem.** Building confidence that the new system produces the same (or
intentionally different) results as the legacy one.

**Solution.** For a defined period, run both systems on the same inputs and
compare outputs (4.8). Fowler/Thoughtworks describe parallel running as the
way to let the business confirm key numbers match before relying on the
new system [28]. Keep the legacy system available, read-only or
shadow-updated, for a **fallback window** after cutover, with a tested
procedure to switch back. Define in advance the exit criteria (e.g. N
consecutive cycles with zero unexplained diffs) and the end date of the
fallback window.

**Consequences.** Running two systems costs effort; without an end date,
parallel runs never end.

**Sources.** [26][27][28].

### 6.4 Quarantine, provenance and PII minimisation

**Problem.** Legacy data is messy, and the backfill must not silently drop
bad rows, lose where data came from, or copy more personal data than
needed.

**Solution.**

- **Quarantine, do not drop.** Rows that fail validation go to a
  quarantine table with the raw record, the failing rule, and the run id.
  Counts reconcile as `loaded + quarantined = extracted`. Triage
  quarantined rows: fix the mapping, fix at source, or accept with a
  recorded reason.
- **Provenance per row.** Carry `source_system`, `source_key`,
  `source_extract_id` (or file hash) and `loaded_by_run` on every loaded
  row, so any value can be traced to its origin, and loaded history is
  distinguishable from natively created data.
- **PII minimisation.** Decide per column whether it is needed in the new
  system. Drop, pseudonymise (keyed hash with a managed secret) or
  generalise before the data lands, not after; data in a landing zone or
  quarantine table is still data held. Apply the same retention rules to
  quarantine and backup copies.

**Consequences.** More tables to manage; but every row is accounted for
and every value is traceable.

**Verification.** `extracted = loaded + quarantined` per slice; no row in
target lacks provenance columns; a column inventory shows each PII field's
treatment.

**Sources.** First principles; quarantine is the standard dead-letter /
"expectations" approach (e.g. Lakeflow declarative pipeline expectations,
Deequ) [24].

---

## 7. Failure modes and anti-patterns

| # | Failure mode | Mechanism | Prevented by |
| --- | --- | --- | --- |
| F1 | **Duplicate loads** | Retried or re-run job appends again; keys assigned at load time differ between runs | Slice replacement (4.1), keyed MERGE on deterministic keys (4.2), commit tokens (3.4) |
| F2 | **Watermark gaps** | HWM on `updated_at`; long transactions stamp start time but commit later [18]; app servers' clocks skew [9]; HWM advanced before the write committed | Overlap + idempotent sink (4.3); commit-ordered cursor (LSN, outbox sequence); log-based CDC (4.4) |
| F3 | **Missed deletes** | HWM extraction cannot see hard deletes | Log-based CDC, tombstones, periodic key-set reconciliation |
| F4 | **Backfill overwrites fresher data** | Backfill with old snapshot runs MERGE without a version guard while live ingestion continues | Recency guard on a monotonic version (4.2); DBLog-style conflict resolution (4.4) |
| F5 | **Accidental full-table overwrite** | Static `INSERT OVERWRITE` with no partition clause replaces every partition [17] | Dynamic overwrite mode or explicit predicate; WAP (4.7); snapshot diff check that only intended files changed |
| F6 | **Backfill starves production** | Unbounded concurrency; scans on primary; long transactions block vacuum | Throttling and chunking (4.9); orchestrator concurrency limits (4.10); replica or branch reads |
| F7 | **Silent truncation / data loss** | String/decimal narrowing, schema merge dropping unknown columns, rows failing a filter disappearing | Strict schema checks (4.13); quarantine (6.4); `extracted = loaded + quarantined` |
| F8 | **Timezone shifts** | Naive timestamps reinterpreted in a different session zone; DST boundaries; event-time partitions computed in local time on one side and UTC on the other | Store instants as UTC with explicit zone; fix session time zone; dbt microbatch requires UTC [22]; reconcile per-day counts at both day boundaries |
| F9 | **Mixed-logic outputs** | Partial backfill leaves old and new logic results side by side, unlabelled | Logic version stamping (4.12); shadow and swap (4.6) |
| F10 | **SCD2 corruption** | Dimension history loaded out of order; overlapping validity ranges | Oldest-first ordering or full per-key rebuild (3.7) |
| F11 | **Facts before dimensions** | Facts loaded before their dimension rows exist; lookups fall to "unknown" and are never revisited | Dimensions first (4.10); late-arriving dimension handling with re-keying |
| F12 | **Incremental model never recomputed** | Logic change deployed to an incremental model without a full refresh; only new slices use the new logic | Recompute rule (3.8); version stamping (4.12) |
| F13 | **Non-deterministic re-run** | `now()`, unseeded randomness, unordered iteration, run-date instead of slice-date | Determinism (3.5); double-run equality test |
| F14 | **Shallow copy invalidated** | Shallow clone's source vacuumed; branch expired before publish [25] | Retention checks before publish; deep copy for long-lived targets |
| F15 | **Replication slot fills disk** | Subscriber or CDC consumer stalls; source retains WAL | Slot lag alerts; maximum slot WAL size; tested teardown |

---

## 8. Invariants every backfill must satisfy

Each invariant is stated as a check that can be automated. `B` is a
backfill run; `R` its target range of slices or keys. The contract clauses
rest on them as follows.

| Clause | Invariants |
| --- | --- |
| CAP-BACKFILL.1 | 1 Idempotence, 3 Scope |
| CAP-BACKFILL.2 | 7 Attribution, 13 Time zone (event time kept apart from load time) |
| CAP-BACKFILL.3 | 9 Atomic visibility, 10 Reversibility |
| CAP-BACKFILL.4 | 4 Completeness, 5 Accuracy |
| CAP-BACKFILL.5 | 11 Source protection |
| CAP-BACKFILL.6 | 6 No regression of freshness |
| CAP-BACKFILL.7 | 4 Completeness, 8 Provenance |
| CAP-BACKFILL.8 | 6 No regression of freshness (see failure mode F2) |

1. **Idempotence.** Running `B` twice over `R` produces a target state equal
   to running it once (compare per-slice content hashes).
2. **Determinism.** Running `B` with the same inputs and logic version on
   two occasions produces identical outputs (per-slice hash equality).
3. **Scope.** `B` modifies no row outside `R` (snapshot diff of the commit
   touches only files/rows in `R`; per-slice hashes outside `R` unchanged).
4. **Completeness.** For every slice in `R`: `count(source) =
   count(target) + count(quarantine) + count(explicitly excluded)`.
5. **Accuracy.** For every slice in `R`, control totals of additive
   measures and the aggregate row hash over canonicalised business columns
   match between source and target, or every mismatch is listed and
   explained.
6. **No regression of freshness.** For every key, the target's source
   version after `B` is ≥ its version before `B`.
7. **Attribution.** Every row in `R` carries the logic version and run id
   that produced it, and `count(rows in R with logic_version ≠ target) = 0`
   when `B` completes.
8. **Provenance.** Every row loaded from another system carries its source
   system, source key and extract identifier; none is null.
9. **Atomic visibility.** Consumers observe either the pre-`B` or the
   post-`B` state of each published unit (slice, table, or table set), never
   a partial one (published via overwrite commit, branch fast-forward or
   view swap).
10. **Reversibility.** The pre-`B` state is recoverable for a declared
    window (snapshot id, tag, retained old table, or branch), and the
    restore procedure has been exercised.
11. **Source protection.** During `B`, source latency and replication lag
    stay within declared thresholds; `B` paused automatically when they did
    not.
12. **Ordering.** For each table, every dimension (and reference table) that
    `R`'s facts reference was complete for `R` before the facts were
    loaded; type 2 dimensions were processed in event-time order.
13. **Time zone.** Per-day counts in source and target agree when both are
    bucketed in UTC.
14. **Restatement record.** If `B` changed any previously published value,
    the restatement log has an entry with slices, reason, old and new
    totals, and logic versions.
15. **PII.** Every personal-data column in the target is on the approved
    inventory with its treatment; quarantine and landing copies follow the
    same retention.

---

## 9. References

1. T. Akidau, R. Bradshaw, C. Chambers, S. Chernyak, R. J.
   Fernández-Moctezuma, R. Lax, S. McVeety, D. Mills, F. Perry, E. Schmidt,
   S. Whittle. "The Dataflow Model: A Practical Approach to Balancing
   Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order
   Data Processing." PVLDB 8(12), 2015. <https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf>
   pp. 1792–1803. DOI 10.14778/2824032.2824076.
2. J. Kreps. "The Log: What every software engineer should know about
   real-time data's unifying abstraction." LinkedIn Engineering, 16 Dec 2013.
   <https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying>
3. J. Kreps. "Questioning the Lambda Architecture." O'Reilly Radar, 2 Jul
   2014. <https://www.oreilly.com/radar/questioning-the-lambda-architecture/>
4. <a id="ref-4"></a>N. Marz, J. Warren. *Big Data: Principles and best practices of scalable
   realtime data systems.* Manning, 2015 (Lambda architecture). **[not
   re-checked]**
5. P. Helland. "Immutability Changes Everything." CIDR 2015.
   <https://ceres.cs.umd.edu/818/papers/immutability.pdf> (also ACM Queue
   13(9), 2015).
6. M. Beauchemin. "Functional Data Engineering — a modern paradigm for batch
   data processing." 8 Jan 2018.
   <https://maximebeauchemin.medium.com/functional-data-engineering-a-modern-paradigm-for-batch-data-processing-2327ec32c42a>
   (page returned 403 to automated fetch; date and content confirmed via
   search and secondary listings; summary here from the article's widely
   cited principles).
7. P. Helland. "Idempotence Is Not a Medical Condition." ACM Queue 10(4),
   2012. DOI 10.1145/2181796.2187821. <https://queue.acm.org/detail.cfm?id=2187821>
8. P. Helland. "The Is Have It: Identity, Immutability, Idempotence, and
   Interchangeability Form the Backbone of Distributed Computing." CIDR
   2019. <https://vldb.org/cidrdb/2019/the-is-have-it-identity-immutability-idempotence-and-interchangeability-form-the-backbone-of-distributed-computing.html>
9. <a id="ref-9"></a>M. Kleppmann. *Designing Data-Intensive Applications.* O'Reilly, 2017;
   ch. 8 "Unreliable clocks", ch. 11 on CDC and event logs. **[chapter
   numbers from memory]**
10. R. T. Snodgrass. *Developing Time-Oriented Database Applications in
    SQL.* Morgan Kaufmann, 2000. Free PDF from the author:
    <https://smsf.cs.arizona.edu/~rts/tdbbook.pdf>
11. K. Kulkarni, J.-E. Michels. "Temporal features in SQL:2011." SIGMOD
    Record 41(3):34–43, 2012. DOI 10.1145/2380776.2380786.
    <https://sigmodrecord.org/2012/09/30/temporal-features-in-sql2011/>
12. Kimball Group. "Design Tip #152: Slowly Changing Dimension Types 0, 4,
    5, 6 and 7." Feb 2013.
    <https://www.kimballgroup.com/2013/02/design-tip-152-slowly-changing-dimension-types-0-4-5-6-7/>
    ; R. Kimball, M. Ross, *The Data Warehouse Toolkit*, 3rd ed., Wiley,
    2013.
13. A. Gupta, I. S. Mumick. "Maintenance of Materialized Views: Problems,
    Techniques, and Applications." IEEE Data Engineering Bulletin 18(2):3–18,
    1995. dblp: <https://dblp.org/rec/journals/debu/GuptaM95> ; author copy
    (third-party host): <http://www.cs.duke.edu/~haohe/paper/gupta95maintenance.pdf>
14. A. Andreakis, I. Papapanagiotou. "DBLog: A Watermark Based
    Change-Data-Capture Framework." arXiv:2010.12597, 2020.
    <https://arxiv.org/abs/2010.12597>
15. Debezium. "Incremental Snapshots in Debezium." 7 Oct 2021.
    <https://debezium.io/blog/2021/10/07/incremental-snapshots/> (introduced
    in Debezium 1.6).
16. Delta Lake documentation. "Table batch reads and writes" (selective
    overwrite `replaceWhere`, dynamic partition overwrite, idempotent writes
    `txnAppId`/`txnVersion`). <https://docs.delta.io/latest/delta-batch.html>
17. Apache Iceberg documentation. "Spark Writes" (MERGE INTO vs INSERT
    OVERWRITE; static vs dynamic overwrite).
    <https://iceberg.apache.org/docs/latest/spark-writes/> (source:
    <https://github.com/apache/iceberg/blob/main/docs/docs/spark-writes.md>)
18. PostgreSQL documentation. "Date/Time Functions and Operators", §9.9.5
    Current Date/Time. <https://www.postgresql.org/docs/current/functions-datetime.html>
19. Debezium documentation. "Sending signals to a Debezium connector."
    <https://debezium.io/documentation/reference/stable/configuration/signalling.html>
20. C. Richardson. "Pattern: Transactional outbox." microservices.io.
    <https://microservices.io/patterns/data/transactional-outbox.html>
21. dbt documentation. "Configure incremental models" (`--full-refresh`,
    `on_schema_change`). <https://docs.getdbt.com/docs/build/incremental-models>
    **[unverified]**

    21a. Apache Iceberg documentation. "Branching and Tagging" (Audit
    Branch). <https://iceberg.apache.org/docs/latest/branching/> ; procedure
    `fast_forward`: <https://iceberg.apache.org/docs/latest/spark-procedures/>
22. dbt documentation. "About microbatch incremental models" (dbt ≥1.9).
    <https://docs.getdbt.com/docs/build/incremental-microbatch>
23. Project Nessie. "Transactions." <https://projectnessie.org/guides/transactions/> ;
    Iceberg–Nessie integration: <https://iceberg.apache.org/docs/1.9.0/nessie/>
24. S. Schelter, D. Lange, P. Schmidt, M. Celikel, F. Biessmann, A.
    Grafberger. "Automating Large-Scale Data Quality Verification." PVLDB
    11(12):1781–1794, 2018. DOI 10.14778/3229863.3229867.
    <https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf>
25. Databricks documentation. "Clone a table on Databricks" (shallow vs
    deep clone; VACUUM caveat). <https://docs.databricks.com/aws/en/delta/clone>
26. GitHub. Scientist: a Ruby library for carefully refactoring critical
    paths. <https://github.com/github/scientist>
27. J. Xu. "Online migrations at scale." Stripe Engineering, 2 Feb 2017.
    <https://stripe.com/blog/online-migrations>
28. I. Cartwright, R. Horn, J. Lewis. "Patterns of Legacy Displacement."
    martinfowler.com. <https://martinfowler.com/articles/patterns-legacy-displacement/>
    (incl. "Divert the Flow", "Transitional Architecture").
29. S. Noach (GitHub). "gh-ost: GitHub's online schema migration tool for
    MySQL." 1 Aug 2016.
    <https://github.blog/engineering/infrastructure/gh-ost-github-s-online-migration-tool-for-mysql/>
30. Apache Airflow documentation. "Backfill."
    <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html>
31. Dagster documentation. "Backfilling data."
    <https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data>
32. Dagster API. `BackfillPolicy` (`single_run`, `multi_run(max_partitions_per_run)`).
    <https://docs.dagster.io/_modules/dagster/_core/definitions/backfill_policy>
33. Databricks documentation. "Backfill jobs" (Lakeflow Jobs backfill runs).
    <https://docs.databricks.com/aws/en/jobs/backfill-jobs> ; announcement:
    <https://www.databricks.com/blog/announcing-backfill-runs-lakeflow-jobs-higher-quality-downstream-data>
34. Apache Iceberg documentation. "Schema evolution" (column-id based).
    <https://iceberg.apache.org/docs/latest/evolution/> **[not re-fetched]**
35. PostgreSQL documentation. "ALTER TABLE" (lock levels; non-volatile
    defaults without rewrite; `NOT VALID` / `VALIDATE CONSTRAINT`).
    <https://www.postgresql.org/docs/current/sql-altertable.html>
36. D. Sato. "Parallel Change." martinfowler.com, 13 May 2014.
    <https://martinfowler.com/bliki/ParallelChange.html>
37. Xata. pgroll: zero-downtime, reversible schema migrations for Postgres.
    <https://github.com/xataio/pgroll>
38. Neon documentation. "Branching." <https://neon.com/docs/introduction/branching>
39. Databricks documentation. "Branches" (Lakebase, copy-on-write).
    <https://docs.databricks.com/aws/en/oltp/projects/branches>
40. PostgreSQL documentation. "Logical Replication — Subscription" (initial
    data copy, table synchronization slots).
    <https://www.postgresql.org/docs/current/logical-replication-subscription.html>
41. M. Fowler. "Strangler Fig Application" (originally 2004 **[original date
    unverified]**; updated 22 Aug 2024). <https://martinfowler.com/bliki/StranglerFigApplication.html>

Further reading (not cited above): T. Akidau, S. Chernyak, R. Lax,
*Streaming Systems*, O'Reilly, 2018; Netflix Technology Blog, "DBLog: A
Generic Change-Data-Capture Framework" (2019) **[URL not verified]**.

<!-- Each citation [n] links to its reference's primary source. -->

[1]: https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf
[2]: https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying
[3]: https://www.oreilly.com/radar/questioning-the-lambda-architecture/
[4]: #ref-4
[5]: https://ceres.cs.umd.edu/818/papers/immutability.pdf
[6]: https://maximebeauchemin.medium.com/functional-data-engineering-a-modern-paradigm-for-batch-data-processing-2327ec32c42a
[7]: https://queue.acm.org/detail.cfm?id=2187821
[8]: https://vldb.org/cidrdb/2019/the-is-have-it-identity-immutability-idempotence-and-interchangeability-form-the-backbone-of-distributed-computing.html
[9]: #ref-9
[10]: https://smsf.cs.arizona.edu/~rts/tdbbook.pdf
[11]: https://sigmodrecord.org/2012/09/30/temporal-features-in-sql2011/
[12]: https://www.kimballgroup.com/2013/02/design-tip-152-slowly-changing-dimension-types-0-4-5-6-7/
[13]: https://dblp.org/rec/journals/debu/GuptaM95
[14]: https://arxiv.org/abs/2010.12597
[15]: https://debezium.io/blog/2021/10/07/incremental-snapshots/
[16]: https://docs.delta.io/latest/delta-batch.html
[17]: https://iceberg.apache.org/docs/latest/spark-writes/
[18]: https://www.postgresql.org/docs/current/functions-datetime.html
[19]: https://debezium.io/documentation/reference/stable/configuration/signalling.html
[20]: https://microservices.io/patterns/data/transactional-outbox.html
[21]: https://docs.getdbt.com/docs/build/incremental-models
[21a]: https://iceberg.apache.org/docs/latest/branching/
[22]: https://docs.getdbt.com/docs/build/incremental-microbatch
[23]: https://projectnessie.org/guides/transactions/
[24]: https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf
[25]: https://docs.databricks.com/aws/en/delta/clone
[26]: https://github.com/github/scientist
[27]: https://stripe.com/blog/online-migrations
[28]: https://martinfowler.com/articles/patterns-legacy-displacement/
[29]: https://github.blog/engineering/infrastructure/gh-ost-github-s-online-migration-tool-for-mysql/
[30]: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html
[31]: https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data
[32]: https://docs.dagster.io/_modules/dagster/_core/definitions/backfill_policy
[33]: https://docs.databricks.com/aws/en/jobs/backfill-jobs
[34]: https://iceberg.apache.org/docs/latest/evolution/
[35]: https://www.postgresql.org/docs/current/sql-altertable.html
[36]: https://martinfowler.com/bliki/ParallelChange.html
[37]: https://github.com/xataio/pgroll
[39]: https://docs.databricks.com/aws/en/oltp/projects/branches
[40]: https://www.postgresql.org/docs/current/logical-replication-subscription.html
