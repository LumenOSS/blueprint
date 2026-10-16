# ADR-0007: Keep delivery independent of the CI host

**Status:** accepted. **Date:** 2026-10-15.

## Context

Organisations change CI hosts, and a repository is often mirrored on more
than one: for example hosted on one service while a public body's own
service is prepared. Logic written in one host's pipeline language has to
be rewritten when the host changes.

## Decision

- Every task is a recipe in a pinned toolchain, run the same way on a
  workstation and in CI. CI definitions only bootstrap the toolchain and
  call recipes.
- A repository may carry the CI definition of each host it targets. A host
  whose definition is present but which should not run it has its pipelines
  disabled, rather than the definition removed.
- Identity is always federation from the host's per-run token, which every
  mainstream host offers.

## Consequences

- Changing host rewrites only a thin wrapper and the federated credential
  subjects ([CAP-REPOSITORIES.5](../specifications/capabilities/cap-repositories.md)).
- Host-specific features (caching, approvals) are used through the wrapper
  only, and each has an equivalent on the other host.
