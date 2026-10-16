# CAP-MODELS Governed analytical models

Predictive models, such as early-warning flags, that advise people, are reproducible, and are checked for unequal error before release.

Layer L3 · domain: product · depends on: [CAP-TRANSFORMATION](cap-transformation.md), [CAP-REVIEW](cap-review.md).

## Purpose

Use predictive models, such as early-warning flags, without letting them decide about people.

## Why

A model that flags a child is a statement about that child; it must be reproducible, explainable, checked for unequal error across groups, and always weighed by a person ([P9](../principles.md#p9-determinism), [P10](../principles.md#p10-low-confidence-goes-to-a-person-never-guessed)).

## Interfaces

- A model registry; deterministic batch scoring.
- Flags delivered into the review queue with their signals.

## Notes

Prefer interpretable models; an early-warning signal that a teacher cannot understand will not be acted on well.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-MODELS.1 | MUST | A model is versioned with its training data pinned, scoring is deterministic, and every score records the model version. | Scoring a fixed input twice gives identical scores with the version attached. |
| CAP-MODELS.2 | MUST | A risk flag is advice to a person and never triggers an automatic action on a learner or staff member; the person's decision is recorded with attribution. | No downstream process consumes a flag except the review queue. |
| CAP-MODELS.3 | MUST | Performance and error rates are reported by sex, area, disability and other declared equity dimensions before release and on a schedule; a model whose disparity exceeds its declared bound is not released. | The release record holds the disaggregated evaluation and the bound. |
| CAP-MODELS.4 | SHOULD | Each flag shows the signals that raised it. | The review view lists the contributing signals for each flag. |
| CAP-MODELS.5 | MUST | Before a model that scores learners is released, it is assessed against the UNICEF Guidance on AI and Children, and the assessment is kept with the release. | The release record holds the assessment. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [UNICEF Guidance on AI and Children](../standards.md#identity-security-and-privacy) | Version 3.0 (December 2025) | adopt |
| [ISO/IEC 5259 Data quality for analytics and machine learning](../standards.md#metadata-and-data-quality) | ISO/IEC 5259-1 to -4:2024 | reference |
| [CycloneDX](../standards.md#software-supply-chain) | CycloneDX 1.5 or later (1.7, October 2025; ECMA-424) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Managed MLflow with Unity Catalog model registry |
| [oss](../implementations/oss.yaml) | MLflow<br/>scikit-learn |
<!-- END GENERATED: implementations -->
