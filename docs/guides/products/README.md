# Products

A **product** is a workload built on the platform. It has its own
repository, its own operational database and a tenant entry. The two
example products here show how the capabilities work together. Between
them they reach most of the platform, and every implementation runs both
of them to show that it conforms.

| Product | What it exercises |
| --- | --- |
| [Document review](document-review.md) | Scanned documents in, machine verdicts, human review of uncertain results, a release gate against an external register |
| [Annual census](census.md) | Registries, periodic collection from every institution, a completeness gate, indicators as at a reference date, open publication |

When you build a new product, record how it meets its capabilities in the
[product checklist](checklist.md). As with any resource, you can build a
product once the registries and products it refers to exist.
