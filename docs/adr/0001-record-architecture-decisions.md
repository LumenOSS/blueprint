# ADR-0001: Record architecture decisions

**Status:** accepted; amended by [ADR-0012](0012-improvement-proposals.md).
**Date:** 2026-10-15.

## Context

The blueprint is meant to be built by people and agents who were not
present when it was designed. A contract without its reasons gets
"simplified" by the first person who does not know why a clause exists.

## Decision

Every change to the architecture (a principle, a capability, a clause's
meaning) is made by a decision record in this directory, in the format of
[`template.md`](template.md). Records are append-only.

## Consequences

- A reader can find why any clause exists.
- Changing the architecture costs one short document, which is the point.
