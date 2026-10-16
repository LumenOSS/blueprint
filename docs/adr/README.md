# Architecture decision records

Each record says what was decided, why, and what follows from it. Changes
are proposed and debated as [LumenOSS Improvement Proposals](../lips/README.md);
when one is accepted, its outcome is recorded here and cites the LIP.
Records are append-only: a decision is changed by a new record that
supersedes the old one, and the old one stays.

| ADR | Decision | Status |
| --- | --- | --- |
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-capabilities-contracts-and-bindings.md) | State the architecture as capabilities, contracts and bindings | Accepted |
| [0003](0003-repositories-by-trust.md) | Split repositories by trust layer | Accepted |
| [0004](0004-isolation-by-branching.md) | Isolate development by branching inside production | Accepted |
| [0005](0005-access-by-role-scope-sensitivity.md) | Decide access by role, scope and sensitivity | Accepted |
| [0006](0006-open-tables-with-an-exit-test.md) | Keep tables in open formats and prove it with an exit test | Accepted |
| [0007](0007-ci-host-independence.md) | Keep delivery independent of the CI host | Accepted |
| [0008](0008-model-the-emis-domain.md) | Model the EMIS domain in the blueprint | Accepted |
| [0009](0009-publication-and-scheduled-disposal.md) | Separate open publication from sharing, and allow scheduled disposal | Accepted |
| [0010](0010-one-person-registry.md) | Record each person once; roles are relationships | Accepted |
| [0011](0011-dbt-semantic-layer.md) | Use the dbt semantic layer in both reference implementations | Accepted |
| [0012](0012-improvement-proposals.md) | Propose changes as LumenOSS Improvement Proposals | Accepted |
| [0013](0013-bounded-contexts.md) | Divide the EMIS domain into bounded contexts | Accepted |
| [0014](0014-internationalisation-and-localisation.md) | Translate through PO files, and label codes in every official language | Accepted |

New records copy [`template.md`](template.md) and take the next number.
