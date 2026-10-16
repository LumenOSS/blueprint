# CAP-ACCESS Access model

<!-- BEGIN GENERATED: header (just render) -->
Role decides reach, entitlements decide rows, classification decides columns.

Layer L1 · domain: governance · depends on: [CAP-IDENTITY](cap-identity.md), [CAP-CATALOG](cap-catalog.md), [CAP-CLASSIFICATION](cap-classification.md).
<!-- END GENERATED: header -->

## Purpose

Access is decided from three separate inputs: a person's role, their scope, and the sensitivity of the data.

## Why

Because the three inputs are separate, no single change can widen someone's access on all of them at once ([P14](../principles.md#p14-access-is-role--scope--sensitivity)). Exemptions are listed by name, because each one is a way to reach raw data ([P5](../principles.md#p5-least-privilege-enumerated)).

## Interfaces

- Groups decide reach, an entitlement table decides rows, and classification tags decide columns.
- There is one row-filter function for each class of table, and one mask for each classification.

## Notes

Three kinds of identity can in practice see raw data: anyone exempt from a policy, anyone who holds a manage right, and the catalog administrator. Keep those lists short, and review them.

## Contract

<!-- BEGIN GENERATED: contract (just render) -->
| Clause | Level | Requirement | How conformance is shown |
| --- | --- | --- | --- |
| CAP-ACCESS.1 | MUST | Reach (which catalogs and actions) is granted to identity-provider groups by role. | Every grant's principal is a group mapped to a role. |
| CAP-ACCESS.2 | MUST | Row scope comes from an entitlement table derived from an authoritative feed (for example staff postings), with a validity period, never edited by hand.<br><br>*Example:* An officer posted to District B sees District B's learners; when the posting ends on 31 August, the rows disappear from their queries that day, with no one editing a permission. | The entitlement table is written only by its loader; a manual write is refused. |
| CAP-ACCESS.3 | MUST | Row and column policies only narrow access. Each user and table resolves to exactly one row filter and each column to at most one mask; an ambiguity fails the query rather than choosing.<br><br>*Example:* A user who is a teacher at one school and an officer for a district would match two row filters on the learner table; the query fails until one scope is chosen, rather than silently using the wider one. | Test a user matching two filters; the query fails. |
| CAP-ACCESS.4 | MUST | Only pipeline identities are exempt from policies, each exemption listed with its reason. | The exemption list contains only workload identities, each with a reason. |
| CAP-ACCESS.5 | MUST | Access to identifiable columns is through a time-boxed, audited group. | Membership of the group expires; each grant appears in audit. |
| CAP-ACCESS.6 | MUST | Reach, row scope and classification are each changed by a different owner, so no single change widens access across all three.<br><br>*Example:* Joining the analyst group gives a person reach but no rows until the posting feed gives them a scope, and no special-category columns unless a steward's classification allows them. | The owners of the group declarations, the entitlement feed and the classification rules are different roles. |
| CAP-ACCESS.7 | MUST | Row scope may also come from a relationship (the record is the person's own, or the person is a guardian with verified authority), taken from the authoritative relationship record, effective-dated, and ended when the relationship or the authority ends.<br><br>*Example:* A guardian sees their child's attendance; when a court order ends their authority on 1 March, the next query after that date returns nothing. | Ending a guardian relationship removes access at the next query. |
| CAP-ACCESS.8 | MUST | A view for a data subject or guardian exposes a declared, minimal set of columns per record class; designated special-category fields are excluded from guardian views by default, with the reason recorded.<br><br>*Example:* The guardian view of a learner shows enrolment, attendance and results, but not counselling notes, which are excluded by default with the reason recorded. | Subject-facing views are declared in code with their column lists and exclusions. |
<!-- END GENERATED: contract -->

## Standards

<!-- BEGIN GENERATED: standards (just render) -->
| Standard | Edition | Verdict |
| --- | --- | --- |
| [Role Based Access Control (ANSI/INCITS 359)](../standards.md#identity-security-and-privacy) | INCITS 359-2012 | reference |
| [NIST SP 800-162 Guide to Attribute Based Access Control (ABAC)](../standards.md#identity-security-and-privacy) | January 2014, with updates as of August 2019 | reference |
<!-- END GENERATED: standards -->

## Implementations

<!-- BEGIN GENERATED: implementations (just render) -->
| Implementation | Components |
| --- | --- |
| [databricks](../implementations/databricks.yaml) | Unity Catalog ABAC policies<br/>Entitlement table in a reference catalog |
| [oss](../implementations/oss.yaml) | Entitlement table in Iceberg<br/>OPA policies for Trino |
<!-- END GENERATED: implementations -->
