# CAP-CLASSIFICATION Classification and provenance

<!-- BEGIN GENERATED: header (just render) -->
Every table and column is classified by sensitivity and tagged with provenance from the moment it lands.

Layer L1 · domain: governance · depends on: [CAP-CATALOG](cap-catalog.md).
<!-- END GENERATED: header -->

## Purpose

Every table is labelled with its sensitivity and its provenance from the moment it lands.

## Why

Tags added at gold come too late to protect the data in bronze. Provenance tags are what let you prove a table is safe to drop ([P12](../principles.md#p12-provenance-before-any-drop)).

## Interfaces

- Governed `classification` (T0–T4) and `provenance` (real, simulated, derived) tags.
- A default policy for data that hasn't been classified yet, and a separate catalog for T4.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-CLASSIFICATION.1 | MUST | Every table carries a classification (T0 public aggregate, T1 internal, T2 de-identified, T3 identifiable, T4 special category) and a provenance (real, simulated, derived). | The daily fitness function finds no untagged table. |
| CAP-CLASSIFICATION.2 | MUST | Data not yet classified is blocked by default until classification has run.<br><br>*Example:* A table loaded from a partner arrives unclassified; analysts cannot read it until classification has run and a steward has confirmed it as T3. | A new unclassified table is unreadable by analysts. |
| CAP-CLASSIFICATION.3 | MUST | T4 data lives in its own catalog and storage, and each grant on it is approved by its steward. | T4 tables exist only in the T4 catalog; its grants trace to approvals. |
| CAP-CLASSIFICATION.4 | MUST | Tags are applied where data enters (landing and bronze), not added at gold. | Bronze tables carry the tags. |
| CAP-CLASSIFICATION.5 | MUST | Simulated data lives only in sandbox catalogs, and derived data is built only from tagged tables. | No table tagged simulated is outside a sandbox catalog. |
| CAP-CLASSIFICATION.6 | MUST | Attributes follow a default classification by kind: data that identifies or locates a person is at least T3; special-category data under the applicable data-protection law, and child-protection and wellbeing records, are T4. Exceptions are recorded with a reason.<br><br>*Example:* A column of birth dates is T3 by default and a column of health conditions T4; classifying the birth dates lower requires a recorded reason. | A check compares column classifications with the default table and lists exceptions. |
| CAP-CLASSIFICATION.7 | MUST | Every personal-data element declares its purpose and legal basis in the catalog; an element with no consuming process or measure at its periodic review is proposed for removal.<br><br>*Example:* The element 'guardian occupation' has had no consuming report or process for a year, so its review proposes removing it. | A report lists personal-data elements without a purpose or without a consumer. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [UN CRC General Comment No. 25 on children's rights in relation to the digital environment](../standards.md#identity-security-and-privacy) | 2021 | adopt |
| [Guidelines on Children's Data Protection in an Education Setting](../standards.md#identity-security-and-privacy) | Adopted by the Committee of Convention 108, November 2020 | reference |
| [ISO/IEC 29100 Privacy framework](../standards.md#identity-security-and-privacy) | ISO/IEC 29100:2024 (second edition) | adopt |
| [NIST SP 800-162 Guide to Attribute Based Access Control (ABAC)](../standards.md#identity-security-and-privacy) | January 2014, with updates as of August 2019 | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Governed tags<br/>Data classification |
| [oss](../implementations/oss.yaml) | Lakekeeper table properties + OPA |
<!-- END GENERATED: implementations -->
