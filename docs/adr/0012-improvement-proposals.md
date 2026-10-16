# ADR-0012: Propose changes as LumenOSS Improvement Proposals

**Status:** accepted. **Date:** 2026-10-16. Amends
[ADR-0001](0001-record-architecture-decisions.md).

## Context

ADR-0001 made every architecture change a decision record. A decision
record states what was decided; it is not a good place to propose a
change, debate it, or track whether implementations have caught up. As
the blueprint opens to outside contributors, changes need a visible path:
where to propose, who decides, how long review lasts, and when a change
counts as done.

## Decision

- Changes to the blueprint are proposed as LumenOSS Improvement Proposals
  (LIPs), following the process in [LIP-1](../lips/lip-0001.md): numbered
  documents with a public lifecycle (Draft, Review, Last Call, Accepted,
  Active), required sections including privacy and safeguarding, and
  headers checked by `just check`.
- Decision records are kept. When a LIP is accepted, the maintainers write
  a decision record that cites it, and the LIP records the decision
  record's number.
- Small corrections that change no meaning need neither.

## Consequences

- Every architecture change has two documents: the LIP, which carries the
  argument, and the decision record, which states the outcome briefly and
  permanently.
- The Data Lead and the Technical Lead decide at the end of Last Call;
  either may block, with the reason recorded.
