# ADR-0004: Isolate development by branching inside production

**Status:** accepted. **Date:** 2026-10-15.

## Context

Many public bodies fund a production environment and nothing else. A
separate development environment that is not funded drifts: its data goes
stale, its schema falls behind, and tests pass against something that no
longer resembles production. Copy-on-write branching of databases and
tables gives a full, current copy of production in seconds to minutes, at
no storage cost until it diverges.

## Decision

- Development and change testing happen on branches of production: a
  database branch per change with a time to live, and development schemas
  inside production catalogs with no consumer grants.
- The production branch is protected.
- A branch never writes production object storage. Database branching does
  not branch object storage, so a branch gets its own storage and may read
  production's only through a read-only path.
- An environment is one template and one values file, so a funded
  development environment can be added later as one more values file.

## Consequences

- Tests run against production's shape and size.
- Branches hold production data, so they need production's access controls.
- Where branching is slower (a new database instance from a volume
  snapshot), branches take minutes; the contract does not require seconds
  ([CAP-OPERATIONALDB.2](../specifications/capabilities/cap-operationaldb.md)).
