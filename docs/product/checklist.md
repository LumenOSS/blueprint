# Product checklist

A product inherits most of its obligations from the platform; this
checklist names the capabilities whose clauses a product must satisfy
itself. Copy it into the product repository and record, for each row, how
the product meets the clauses and where the evidence is. Rows that do not
apply are marked not applicable with a reason, exactly as in a
[binding](../implementations/README.md).

| Capability | What the product records |
| --- | --- |
| [CAP-ONBOARDING](../capabilities/cap-onboarding.md) | Its tenant entry: owner role, domain, catalogs, highest classification |
| [CAP-MASTERDATA](../capabilities/cap-masterdata.md) | Which registries it reads; it never mints identifiers of its own for core resources |
| [CAP-REFERENCE](../capabilities/cap-reference.md) | The code lists and dictionary entries for every element it owns |
| [CAP-CLASSIFICATION](../capabilities/cap-classification.md) | Classification, provenance, purpose and legal basis for every element it owns |
| [CAP-ACCESS](../capabilities/cap-access.md) | Its row scopes and any subject-facing views |
| [CAP-RECORDS](../capabilities/cap-records.md) | The record class of each table and file it owns |
| [CAP-QUALITY](../capabilities/cap-quality.md) | Its checks, with dimension and severity |
| [CAP-INTEROPERABILITY](../capabilities/cap-interoperability.md) | A feed contract for every exchange with another system |
| [CAP-PIPELINE](../capabilities/cap-pipeline.md) | How its processing stays idempotent and deterministic |
| [CAP-REVIEW](../capabilities/cap-review.md) | Where people decide, and how their decisions are protected |
| [CAP-COLLECTION](../capabilities/cap-collection.md) | Its instruments, if it collects returns |
| [CAP-SEMANTICS](../capabilities/cap-semantics.md) | The indicators it defines, with their metadata |
| [CAP-PUBLICATION](../capabilities/cap-publication.md) | What it publishes, and the disclosure tests |
| [CAP-MODELS](../capabilities/cap-models.md) | Any model it uses, with its equity evaluation |
| [CAP-APPS](../capabilities/cap-apps.md) | Accessibility and language evidence for its interfaces |

The example products show the checklist filled in by their conformance
steps: [document review](document-review.md) and [annual census](census.md).
