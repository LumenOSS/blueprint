# CAP-CLASSIFICATION Classification and provenance

Every table and column is classified by sensitivity and tagged with provenance from the moment it lands.

Layer L1 · domain: governance · depends on: [CAP-CATALOG](cap-catalog.md).

## Purpose

Label every table by sensitivity and provenance from the moment it lands.

## Why

Tags added at gold come too late to protect bronze. Provenance tags make drops provable ([P12](../principles.md#p12-provenance-before-any-drop)).

## Interfaces

- Governed `classification` (T0–T4) and `provenance` (real, simulated, derived) tags.
- A default policy for unclassified data; a separate catalog for T4.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-CLASSIFICATION.1 | MUST | Every table carries a classification (T0 public aggregate, T1 internal, T2 de-identified, T3 identifiable, T4 special category) and a provenance (real, simulated, derived). | The daily fitness function finds no untagged table. |
| CAP-CLASSIFICATION.2 | MUST | Data not yet classified is blocked by default until classification has run. | A new unclassified table is unreadable by analysts. |
| CAP-CLASSIFICATION.3 | MUST | T4 data lives in its own catalog and storage, and each grant on it is approved by its steward. | T4 tables exist only in the T4 catalog; its grants trace to approvals. |
| CAP-CLASSIFICATION.4 | MUST | Tags are applied where data enters (landing and bronze), not added at gold. | Bronze tables carry the tags. |
| CAP-CLASSIFICATION.5 | MUST | Simulated data lives only in sandbox catalogs, and derived data is built only from tagged tables. | No table tagged simulated is outside a sandbox catalog. |
| CAP-CLASSIFICATION.6 | MUST | Attributes follow a default classification by kind: data that identifies or locates a person is at least T3; special-category data under the applicable data-protection law, and child-protection and wellbeing records, are T4. Exceptions are recorded with a reason. | A check compares column classifications with the default table and lists exceptions. |
| CAP-CLASSIFICATION.7 | MUST | Every personal-data element declares its purpose and legal basis in the catalog; an element with no consuming process or measure at its periodic review is proposed for removal. | A report lists personal-data elements without a purpose or without a consumer. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [UN CRC General Comment No. 25 on children's rights in relation to the digital environment](../standards.md#identity-security-and-privacy) | 2021 | adopt |
| [Guidelines on Children's Data Protection in an Education Setting](../standards.md#identity-security-and-privacy) | Adopted by the Committee of Convention 108, November 2020 | reference |
| [ISO/IEC 29100 Privacy framework](../standards.md#identity-security-and-privacy) | ISO/IEC 29100:2024 (second edition) | adopt |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Governed tags<br/>Data classification |
| [oss](../implementations/oss.yaml) | Lakekeeper table properties + OPA |
<!-- END GENERATED: implementations -->
