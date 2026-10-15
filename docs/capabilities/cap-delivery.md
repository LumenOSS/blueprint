# CAP-DELIVERY Change delivery

Every change is reviewed with its plan and applied by CI only, after merge.

Layer L1 · domain: delivery · depends on: [CAP-CIIDENTITY](cap-ciidentity.md), [CAP-STATE](cap-state.md).

## Purpose

Make every change to a shared environment reviewed, visible as a plan, and applied by one writer.

## Why

One writer gives one audit trail and real locking ([P1](../principles.md#p1-ci-is-the-only-deployer)). Deletion through code keeps the record of what was removed and why. Migrating the database before deploying the code that needs it avoids a release that cannot run.

## Interfaces

- Change review showing the plan artefact.
- Apply stage consuming that artefact after merge, or by dispatch for trust anchors.
- Version tags as the only release trigger.

## Notes

When CI lacks a right, give CI's identity the right in one documented bootstrap step. A workstation apply is a second writer, not a shortcut.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-DELIVERY.1 | MUST | Every change to infrastructure or a shared environment, including grants, migrations and deletions, is a reviewed change whose plan is shown in the review. | Sample merged changes; each carries the plan CI produced for it. |
| CAP-DELIVERY.2 | MUST | Only CI applies. Apply recipes refuse to run anywhere else. | Run an apply recipe on a workstation; it refuses before contacting any API. |
| CAP-DELIVERY.3 | MUST | CI applies the saved plan that was reviewed, not a fresh one. | The apply step consumes the plan artefact produced by the plan step. |
| CAP-DELIVERY.4 | MUST | A trust-anchor change is dispatched by hand from the main branch by an allow-listed role, after approval by both the Data Lead and the Technical Lead. | The bootstrap pipeline checks the actor against its allow-list before any credential is issued; its environment requires two approvals. |
| CAP-DELIVERY.5 | MUST | A deletion is two changes: adopt the object into code, then remove it. | Every removal of a resource in history is preceded by a change that imported it or created it. |
| CAP-DELIVERY.6 | MUST | A database is migrated before the code that needs it is deployed; a release is a version tag, and an infrastructure change alone never changes what version runs. | Pipeline order runs migrations first; deployments take the image version from a tag. |
| CAP-DELIVERY.7 | SHOULD | A scheduled fitness check fails if any state was written by an identity other than CI. | The check reads the last writer of each state version and alerts on a non-CI principal. |
<!-- END GENERATED: contract -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
No implementation binds this capability yet.
<!-- END GENERATED: implementations -->
