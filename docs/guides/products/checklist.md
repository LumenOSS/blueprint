# Product checklist

A product inherits most of its obligations from the platform; this
checklist names the capabilities whose clauses a product must satisfy
itself. Copy it into the product repository and record, for each row, how
the product meets the clauses and where the evidence is. Rows that do not
apply are marked not applicable with a reason, exactly as in a
[binding](../../specifications/implementations/README.md).

| Capability | What the product records |
| --- | --- |
| [CAP-ONBOARDING](../../specifications/capabilities/cap-onboarding.md) | Its tenant entry: owner role, domain, catalogs, highest classification |
| [CAP-MASTERDATA](../../specifications/capabilities/cap-masterdata.md) | Which registries it reads; it never mints identifiers of its own for core resources |
| [CAP-REFERENCE](../../specifications/capabilities/cap-reference.md) | The code lists and dictionary entries for every element it owns |
| [CAP-CLASSIFICATION](../../specifications/capabilities/cap-classification.md) | Classification, provenance, purpose and legal basis for every element it owns |
| [CAP-ACCESS](../../specifications/capabilities/cap-access.md) | Its row scopes and any subject-facing views |
| [CAP-RECORDS](../../specifications/capabilities/cap-records.md) | The record class of each table and file it owns |
| [CAP-QUALITY](../../specifications/capabilities/cap-quality.md) | Its checks, with dimension and severity |
| [CAP-INTEROPERABILITY](../../specifications/capabilities/cap-interoperability.md) | A feed contract for every exchange with another system |
| [CAP-PIPELINE](../../specifications/capabilities/cap-pipeline.md) | How its processing stays idempotent and deterministic |
| [CAP-REVIEW](../../specifications/capabilities/cap-review.md) | Where people decide, and how their decisions are protected |
| [CAP-COLLECTION](../../specifications/capabilities/cap-collection.md) | Its instruments, if it collects returns |
| [CAP-SEMANTICS](../../specifications/capabilities/cap-semantics.md) | The indicators it defines, with their metadata |
| [CAP-PUBLICATION](../../specifications/capabilities/cap-publication.md) | What it publishes, and the disclosure tests |
| [CAP-MODELS](../../specifications/capabilities/cap-models.md) | Any model it uses, with its equity evaluation |
| [CAP-APPS](../../specifications/capabilities/cap-apps.md) | Accessibility and language evidence for its interfaces |

The example products show the checklist filled in by their conformance
steps: [document review](document-review.md) and [annual census](census.md).
