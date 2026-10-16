# Standards

The external standards the blueprint relies on, each linked to its
publisher's own page, with the edition relied on and its verdict:

- **adopt:** named in a contract clause;
- **reference:** a recommended method or background;
- **track:** watched, not yet relied on.

The register is [`blueprint/standards.yaml`](../../blueprint/standards.yaml);
this page and the "Standards" section of each capability page are generated
from it. Every entry was last checked on the date in the register. Entries
checked as `catalogue` were confirmed from the publisher's catalogue
listing because the publisher's page blocks automated reading; confirm them
on the page before relying on the exact edition.

## How standards are cited

- **Cite a dated edition with an "or later" rule** where newer editions
  stay compatible (for example "OpenAPI 3.1 or later"), so a patch release
  does not invalidate a clause.
- **Separate the standard from its code list.** Country, currency and
  language codes change between editions through their maintenance
  agencies; each code list is loaded on a schedule, versioned, and recorded
  with its source and retrieval date
  ([CAP-REFERENCE](capabilities/cap-reference.md)).
- **Prefer free, testable profiles in clauses** (RFC 3339 rather than the
  whole of ISO 8601), and cite the broader standard as background.
- **Re-check the register at least once a year.** A new edition is a
  reviewed change to the register and, where it changes a clause, an ADR.

## Register

<!-- BEGIN GENERATED: register (just render) -->
### Requirement language

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [BCP 14 (RFC 2119 and RFC 8174)](https://www.rfc-editor.org/info/bcp14)<br/>IETF | RFC 2119 (1997) with RFC 8174 (2017) | The meaning of MUST, SHOULD and MAY; only the upper-case forms are normative. | adopt | — |

### Data representation

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [RFC 3339 Date and Time on the Internet](https://www.rfc-editor.org/info/rfc3339)<br/>IETF | RFC 3339 (2002), as updated by RFC 9557 (2024) | The strict, testable profile of ISO 8601 used for every stored or exchanged timestamp, with an explicit offset. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [RFC 9557 Internet Extended Date/Time Format](https://www.rfc-editor.org/info/rfc9557)<br/>IETF | RFC 9557 (April 2024) | Adds the time-zone name to a timestamp where local civil time matters, such as a school day or an examination sitting. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [ISO 8601-1 Date and time](https://www.iso.org/standard/70907.html)<br/>ISO | ISO 8601-1:2019 with Amd 1:2022 | The underlying date and time standard that RFC 3339 profiles. | reference | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [ITU-T E.164 international numbering plan](https://www.itu.int/rec/T-REC-E.164-202602-I/en)<br/>ITU-T | E.164 (02/26), approved 2026-02-13 | The form in which telephone numbers are stored and exchanged. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [ISO 3166-1 Country codes](https://www.iso.org/standard/72482.html)<br/>ISO | ISO 3166-1:2020; code list as maintained by the ISO 3166 Maintenance Agency | Country codes; the code list is loaded on a schedule with its retrieval date. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [ISO 4217 Currency codes](https://www.iso.org/iso-4217-currency-codes.html)<br/>ISO | ISO 4217:2015; code tables as maintained by the maintenance agency | The currency of every amount of money, stored as a decimal with its code. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [BCP 47 Language tags](https://www.rfc-editor.org/info/bcp47)<br/>IETF | RFC 5646 and RFC 4647, with the IANA Language Subtag Registry | Tags for languages of instruction, home languages and interface locales. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md), [CAP-APPS](capabilities/cap-apps.md) |
| [ISO 639 Language codes](https://www.iso.org/standard/74575.html)<br/>ISO | ISO 639:2023, which replaced the former parts 1 to 5 | The language code sets underlying BCP 47 subtags. | reference | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [Unicode Standard and normalization (UAX 15)](https://www.unicode.org/versions/Unicode18.0.0/)<br/>Unicode Consortium | Unicode 18.0.0 (2026) | Text is stored as UTF-8 in Normalization Form C, so names compare reliably in duplicate detection. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md), [CAP-MASTERDATA](capabilities/cap-masterdata.md) |
| [RFC 9562 Universally Unique IDentifiers](https://www.rfc-editor.org/info/rfc9562)<br/>IETF | RFC 9562 (May 2024), obsoleting RFC 4122 | Opaque surrogate identifiers; version 7 keeps index locality. | reference | [CAP-MASTERDATA](capabilities/cap-masterdata.md) |

### Education classifications and indicators

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [International Standard Classification of Education (ISCED 2011)](https://www.uis.unesco.org/en/methods-and-tools/isced)<br/>UNESCO Institute for Statistics | ISCED 2011 (published 2012) with Operational Manual (2015); amendment due 2027 | Levels of education programmes and attainment for international comparison. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md), [CAP-SEMANTICS](capabilities/cap-semantics.md) |
| [ISCED Fields of Education and Training (ISCED-F 2013)](https://www.uis.unesco.org/en/methods-and-tools/isced)<br/>UNESCO Institute for Statistics | ISCED-F 2013 (published 2014); comprehensive revision due 2027 | Fields of study for programmes and qualifications. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [International Standard Classification of Teacher Training Programmes (ISCED-T 2021)](https://unesdoc.unesco.org/ark:/48223/pf0000383023_eng)<br/>UNESCO Institute for Statistics | ISCED-T 2021 (published 2022) | Classifying teacher-training programmes and qualifications for SDG 4.c reporting. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [ISCED revision (amendment of ISCED 2011, revision of ISCED-F 2013)](https://www.uis.unesco.org/en/methods-and-tools/isced/revision)<br/>UNESCO Institute for Statistics | In progress; task forces 2026; target 44th UNESCO General Conference (2027) | Future edition of the classifications the crosswalks map to. | track | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [Global indicator framework for the Sustainable Development Goals](https://unstats.un.org/sdgs/indicators/indicators-list/)<br/>UN Statistics Division (IAEG-SDGs) | After 2026 refinement (UN Statistical Commission 57th session, March 2026; includes the 2025 Comprehensive Review) | Official codes and wording of the 12 global SDG 4 indicators. | adopt | [CAP-SEMANTICS](capabilities/cap-semantics.md), [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [Official List of SDG 4 Indicators (global and thematic)](https://www.uis.unesco.org/en/methods-and-tools/sdg4-indicators)<br/>UNESCO Institute for Statistics | October 2026 (post EDSC-12) | Codes, wording and benchmark flags for SDG 4 thematic indicators. | adopt | [CAP-SEMANTICS](capabilities/cap-semantics.md), [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [UIS Glossary - Education Metadata](https://databrowser.uis.unesco.org/glossary)<br/>UNESCO Institute for Statistics | 2026 (UIS/2026/ED/IP/32) | Definitions and calculation methods of education indicators. | adopt | [CAP-SEMANTICS](capabilities/cap-semantics.md) |
| [UIS Survey of Formal Education (and UIS-OECD-Eurostat UOE collection)](http://uis.unesco.org/uis-questionnaires)<br/>UNESCO Institute for Statistics | Annual cycle; documented in the February 2026 Data Refresh background document | The international questionnaires an EMIS must be able to complete from gold. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [LASER national education statistical capacity assessment](https://www.uis.unesco.org/en/methods-and-tools/laser)<br/>UNESCO Institute for Statistics | Global report 2025 (maturity model) | Maturity model for a country's education data ecosystem. | reference | — |

### Metadata and data quality

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [Education Data Quality Assessment Framework (Ed-DQAF)](https://emis.uis.unesco.org/tools-and-reports)<br/>UNESCO Institute for Statistics | 2017 manual, instruments and matrix | External assessment of an administrative education data system. | reference | [CAP-QUALITY](capabilities/cap-quality.md), [CAP-COLLECTION](capabilities/cap-collection.md) |
| [ISO/IEC 11179 Metadata registries](https://www.iso.org/standard/78914.html)<br/>ISO/IEC | ISO/IEC 11179-1:2023 and 11179-3:2023 | The model of the data dictionary: concept, value domain and data element, with registration status and steward. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [ISO/IEC 25012 Data quality model](https://www.iso.org/standard/35736.html)<br/>ISO/IEC | ISO/IEC 25012:2008, confirmed 2025 | The vocabulary of quality characteristics each check names. | adopt | [CAP-QUALITY](capabilities/cap-quality.md) |
| [ISO/IEC 25024 Measurement of data quality](https://www.iso.org/standard/35749.html)<br/>ISO/IEC | ISO/IEC 25024:2015, confirmed 2022 | How each quality characteristic becomes a measure. | reference | [CAP-QUALITY](capabilities/cap-quality.md) |
| [ISO/IEC 5259 Data quality for analytics and machine learning](https://www.iso.org/standard/81092.html)<br/>ISO/IEC | ISO/IEC 5259-1 to -4:2024 | Quality measures for the training and scoring data of governed models. | reference | [CAP-MODELS](capabilities/cap-models.md) |
| [OpenLineage](https://openlineage.io/docs/)<br/>LF AI & Data Foundation | Specification 1.x (1.54.0, 2026) | A vendor-neutral format for lineage events, so implementations produce comparable lineage. | adopt | [CAP-LINEAGE](capabilities/cap-lineage.md) |

### Official statistics and disclosure control

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [UN Fundamental Principles of Official Statistics](https://unstats.un.org/unsd/dnss/gp/fundprinciples.aspx)<br/>United Nations Statistics Division | Adopted 1994; endorsed by UN General Assembly resolution 68/261 (2014) | The principles official education statistics follow, including that individual data serve statistical purposes only. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md), [CAP-COLLECTION](capabilities/cap-collection.md), P15 |
| [UN National Quality Assurance Frameworks Manual for Official Statistics](https://unstats.un.org/unsd/methodology/dataquality/un-nqaf/)<br/>United Nations Statistics Division | 2019 (ST/ESA/STAT/SER.M/100) | A quality framework for statistics drawn from administrative sources such as an EMIS. | reference | [CAP-QUALITY](capabilities/cap-quality.md), [CAP-COLLECTION](capabilities/cap-collection.md) |
| [Generic Statistical Business Process Model](https://unece.org/statistics/modernstats/gsbpm)<br/>UNECE | GSBPM v5.2 (May 2025) | The phase vocabulary for statistical production; each collection and release stage names its phase. | adopt | [CAP-COLLECTION](capabilities/cap-collection.md) |
| [Handbook on Statistical Disclosure Control](https://sdctools.github.io/HandbookSDC/)<br/>Centre of Excellence on Statistical Disclosure Control | Second edition (2025; online edition 2026) | The methods for suppression, rounding and perturbation (including the Cell Key Method) applied to published tables. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [NIST SP 800-226 Guidelines for Evaluating Differential Privacy Guarantees](https://csrc.nist.gov/pubs/sp/800/226/final)<br/>NIST | Final, March 2025 | How to decide on, and document, differential privacy for query services or synthetic data. | reference | [CAP-PUBLICATION](capabilities/cap-publication.md) |

### Open data and exchange

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [RFC 7946 GeoJSON](https://www.rfc-editor.org/info/rfc7946)<br/>IETF | RFC 7946 (August 2016) | Open format for published locations and boundaries, with WGS 84 as its fixed reference system. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [OGC API – Features](https://ogcapi.ogc.org/features/)<br/>Open Geospatial Consortium | Parts 1 to 3 (Core 1.0.1, CRS by Reference 1.0.1, Filtering 1.0.0) | A standard web interface for querying published institution locations. | reference | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [Common Education Data Standards (CEDS)](https://ceds.ed.gov/)<br/>US National Center for Education Statistics | Version 14 (official release on the CEDS GitHub, March–April 2026); the ceds.ed.gov downloads still offer Version 13 | Open vocabulary of education data elements for the data dictionary. | reference | [CAP-REFERENCE](capabilities/cap-reference.md), [CAP-INTEROPERABILITY](capabilities/cap-interoperability.md) |
| [1EdTech OneRoster](https://www.imsglobal.org/spec/oneroster/v1p2)<br/>1EdTech | 1.2 (September 2022) | Rosters, enrolments and results between the EMIS and learning tools. | adopt | [CAP-INTEROPERABILITY](capabilities/cap-interoperability.md) |
| [1EdTech Competencies and Academic Standards Exchange (CASE)](https://www.imsglobal.org/spec/case/v1p1)<br/>1EdTech | 1.1 (January 2025) | Publishing curriculum outcomes and competency frameworks with stable identifiers. | adopt | [CAP-REFERENCE](capabilities/cap-reference.md) |
| [1EdTech Comprehensive Learner Record 2.0 and Open Badges 3.0](https://www.imsglobal.org/spec/clr/v2p0)<br/>1EdTech | CLR 2.0 (doc 1.1, October 2025); Open Badges 3.0 (doc 1.4.5, June 2026) | Learner-held records and achievements as verifiable credentials. | adopt | [CAP-TRANSFORMATION](capabilities/cap-transformation.md) |
| [European Learning Model (European Digital Credentials for Learning)](https://europass.europa.eu/en/news/latest-developments-european-learning-model)<br/>European Commission (Europass) | ELM 3.3 (2025) | EU model for qualifications and verifiable learning credentials. | reference | [CAP-TRANSFORMATION](capabilities/cap-transformation.md) |
| [Data Catalog Vocabulary (DCAT)](https://www.w3.org/TR/vocab-dcat-3/)<br/>W3C | DCAT Version 3, W3C Recommendation (August 2024) | Catalogue metadata for published datasets, including dataset series and versions. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [DCAT Application Profile (DCAT-AP)](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)<br/>SEMIC | DCAT-AP 3.0.1 (October 2025) | Which DCAT properties to fill, and with which vocabularies. | reference | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [schema.org Dataset](https://schema.org/Dataset)<br/>schema.org | schema.org 30.1 (September 2026) | Dataset markup on landing pages, generated from the DCAT record, so datasets are found by search. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/)<br/>W3C | W3C Recommendations (December 2015) | Column-level metadata shipped beside every published CSV file. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [SDMX](https://sdmx.org/standards-2/)<br/>SDMX sponsors | SDMX 3.0 or later (3.1, May 2025); 2.1 where the receiving agency requires it | Exchange of statistics and their structures with international bodies. | adopt | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [International Open Data Charter principles](https://opendatacharter.org/principles/)<br/>Open Data Charter | Six principles (2015) | The policy basis for publishing open by default, timely and comparable. | reference | [CAP-PUBLICATION](capabilities/cap-publication.md), P15 |
| [FAIR Guiding Principles](https://www.gofair.foundation/fair-principles)<br/>GO FAIR | Wilkinson et al., Scientific Data 3, 160018 (2016) | Findable, accessible, interoperable and reusable data, as a checklist for publication. | reference | [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [Apache Ossie (Open Semantic Interchange)](https://github.com/apache/ossie)<br/>Apache Software Foundation (incubating) | Specification 0.1.1 (December 2025); 0.2 in development; Apache incubating project | An open format for exchanging semantic definitions between tools, which could replace the per-engine generators. | track | [CAP-SEMANTICS](capabilities/cap-semantics.md) |
| [OpenAPI Specification](https://spec.openapis.org/oas/v3.2.1.html)<br/>OpenAPI Initiative | OpenAPI 3.1 or later (3.2.1, September 2026) | Machine-readable contracts for request-response interfaces. | adopt | [CAP-INTEROPERABILITY](capabilities/cap-interoperability.md), [CAP-APPS](capabilities/cap-apps.md) |
| [JSON Schema](https://json-schema.org/specification)<br/>JSON Schema | Draft 2020-12 | Payload and data-contract schemas, and the blueprint's own schemas. | adopt | [CAP-INTEROPERABILITY](capabilities/cap-interoperability.md) |
| [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/v3.1.0)<br/>AsyncAPI Initiative | AsyncAPI 3.x (3.1.0, January 2026) | Machine-readable contracts for evented interfaces. | adopt | [CAP-INTEROPERABILITY](capabilities/cap-interoperability.md) |
| [CloudEvents](https://cloudevents.io/)<br/>CNCF | CloudEvents 1.0.2 | A common envelope for events, whose id and source give the idempotency key. | adopt | [CAP-INTEROPERABILITY](capabilities/cap-interoperability.md), [CAP-PIPELINE](capabilities/cap-pipeline.md) |
| [ODRL Information Model](https://www.w3.org/TR/odrl-model/)<br/>W3C | ODRL 2.2, W3C Recommendation (2018) | Machine-readable terms of a data-sharing agreement, alongside the DCAT record. | reference | [CAP-SHARING](capabilities/cap-sharing.md) |
| [Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model-2.0/)<br/>W3C | VC Data Model 2.0, W3C Recommendation (May 2025) | Tamper-evident digital certificates and transcripts issued about a single record; Open Badges 3.0, CLR 2.0 and the European Learning Model build on it. | adopt | [CAP-TRANSFORMATION](capabilities/cap-transformation.md) |

### Identity, security and privacy

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [UNICEF Guidance on AI and Children](https://www.unicef.org/innocenti/reports/policy-guidance-ai-children)<br/>UNICEF Innocenti | Version 3.0 (December 2025) | Child-rights requirements for any model that scores or profiles learners. | adopt | [CAP-MODELS](capabilities/cap-models.md) |
| [Data Governance for EdTech (landscape review and policy recommendations)](https://www.unicef.org/innocenti/media/11616/file/UNICEF-Innocenti-Data-Governance-Education-Technology-Summary-2025.pdf)<br/>UNICEF Innocenti (with UNESCO and the Global Privacy Assembly) | 2025 | Terms for sharing learner data with vendors and third parties. | adopt | [CAP-SHARING](capabilities/cap-sharing.md) |
| [UN CRC General Comment No. 25 on children's rights in relation to the digital environment](https://www.ohchr.org/en/documents/general-comments-and-recommendations/general-comment-no-25-2021-childrens-rights-relation)<br/>UN Committee on the Rights of the Child (OHCHR) | 2021 | Rights basis for classifying and protecting learner data. | adopt | [CAP-CLASSIFICATION](capabilities/cap-classification.md) |
| [Age appropriate design - a code of practice for online services (Children's code)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-code/)<br/>UK Information Commissioner's Office | In force 2 September 2020 (conformance from 2 September 2021); guidance updated for the Data (Use and Access) Act 2025 | Design standards for learner- and guardian-facing services. | reference | [CAP-APPS](capabilities/cap-apps.md) |
| [Guidelines on Children's Data Protection in an Education Setting](https://www.coe.int/web/data-protection/-/protect-children-s-personal-data-in-education-setting-)<br/>Council of Europe | Adopted by the Committee of Convention 108, November 2020 | Intergovernmental guidelines on children's data protection specific to education. | reference | [CAP-CLASSIFICATION](capabilities/cap-classification.md), [CAP-SHARING](capabilities/cap-sharing.md) |
| [NIST SP 800-63-4 Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/4/final)<br/>NIST | SP 800-63-4, final (July 2025) | Assurance levels and the definition of a phishing-resistant authenticator. | adopt | [CAP-IDENTITY](capabilities/cap-identity.md) |
| [Web Authentication](https://www.w3.org/TR/webauthn-3/)<br/>W3C | Level 2 or later (Level 3, W3C Recommendation, August 2026) | Passkeys and security keys as the phishing-resistant authenticator. | adopt | [CAP-IDENTITY](capabilities/cap-identity.md) |
| [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)<br/>OpenID Foundation | Core 1.0 incorporating errata set 2; also ISO/IEC 26131:2024 | Sign-in to applications through the identity provider. | adopt | [CAP-IDENTITY](capabilities/cap-identity.md), [CAP-APPS](capabilities/cap-apps.md) |
| [OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/info/rfc9700)<br/>IETF | RFC 9700 / BCP 240 (January 2025) | The security baseline every OAuth deployment conforms to. | adopt | [CAP-IDENTITY](capabilities/cap-identity.md), [CAP-APPS](capabilities/cap-apps.md) |
| [SCIM 2.0](https://datatracker.ietf.org/wg/scim/documents/)<br/>IETF | RFC 7643 and RFC 7644 (2015), with later extensions | Automatic provisioning of users and groups from the authoritative directory. | adopt | [CAP-IDENTITY](capabilities/cap-identity.md) |
| [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)<br/>OWASP | ASVS 5.0.0 (May 2025) | Testable security requirements for applications that handle identifiable data. | adopt | [CAP-APPS](capabilities/cap-apps.md) |
| [ISO/IEC 27001 Information security management systems](https://www.iso.org/standard/27001)<br/>ISO/IEC | ISO/IEC 27001:2022 with Amd 1:2024, and ISO/IEC 27002:2022 | The operator's management system, to which the capability clauses map as evidence. | reference | [CAP-GUARDRAILS](capabilities/cap-guardrails.md), [CAP-AUDIT](capabilities/cap-audit.md) |
| [ISO/IEC 27701 Privacy information management systems](https://www.iso.org/standard/27701)<br/>ISO/IEC | ISO/IEC 27701:2025, a standalone standard | The operator's privacy management system for personal data. | reference | [CAP-RECORDS](capabilities/cap-records.md) |
| [ISO/IEC 29100 Privacy framework](https://www.iso.org/standard/85938.html)<br/>ISO/IEC | ISO/IEC 29100:2024 (second edition) | Privacy vocabulary and principles, including purpose legitimacy and data minimisation. | adopt | [CAP-RECORDS](capabilities/cap-records.md), [CAP-CLASSIFICATION](capabilities/cap-classification.md), P20 |
| [Role Based Access Control (ANSI/INCITS 359)](https://csrc.nist.gov/projects/role-based-access-control)<br/>NIST (project page for the ANSI/INCITS standard) | INCITS 359-2012 | The role-based model behind reach: permissions are granted to roles, and people hold roles. | reference | [CAP-ACCESS](capabilities/cap-access.md) |
| [NIST SP 800-162 Guide to Attribute Based Access Control (ABAC)](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)<br/>NIST | January 2014, with updates as of August 2019 | The attribute-based model behind row scope and column visibility, decided from attributes of the person, the data and the request. | reference | [CAP-ACCESS](capabilities/cap-access.md), [CAP-CLASSIFICATION](capabilities/cap-classification.md) |
| [NIST SP 800-188 De-Identifying Government Datasets](https://csrc.nist.gov/pubs/sp/800/188/final)<br/>NIST | Final, September 2023 | Techniques and governance for de-identifying data before it is shared or published, including masking and pseudonymisation. | reference | [CAP-SHARING](capabilities/cap-sharing.md), [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)<br/>NIST | CSF 2.0 (February 2024) | An outcome-based risk framework to which the capabilities can be mapped. | reference | [CAP-GUARDRAILS](capabilities/cap-guardrails.md) |

### Software supply chain

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [Supply-chain Levels for Software Artifacts (SLSA)](https://slsa.dev/spec/v1.2/)<br/>OpenSSF | SLSA v1.2 (November 2025) | Build provenance for every deployable artefact. | adopt | [CAP-DELIVERY](capabilities/cap-delivery.md) |
| [SPDX](https://spdx.github.io/spdx-spec/v3.0.1/)<br/>Linux Foundation | SPDX 2.3 or later (3.0.1, December 2024) | Software bill of materials and licence identifiers; either SPDX or CycloneDX satisfies the clause. | adopt | [CAP-DELIVERY](capabilities/cap-delivery.md) |
| [CycloneDX](https://cyclonedx.org/specification/overview/)<br/>OWASP / Ecma International | CycloneDX 1.5 or later (1.7, October 2025; ECMA-424) | Software bill of materials; also describes models, which suits governed models. | adopt | [CAP-DELIVERY](capabilities/cap-delivery.md), [CAP-MODELS](capabilities/cap-models.md) |

### Accessibility and localisation

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [Unicode CLDR](https://cldr.unicode.org/index/downloads)<br/>Unicode Consortium | CLDR 48.2 (March 2026) | Locale data for formatting numbers, dates and currencies at display time; formatted values are never stored. | reference | [CAP-APPS](capabilities/cap-apps.md), [CAP-REPORTING](capabilities/cap-reporting.md) |
| [Web Content Accessibility Guidelines](https://www.w3.org/TR/WCAG22/)<br/>W3C | WCAG 2.2 Level AA (W3C Recommendation, December 2024 version); also ISO/IEC 40500:2025 | The accessibility level every interface used by staff, learners, guardians or the public meets. | adopt | [CAP-APPS](capabilities/cap-apps.md) |
| [EN 301 549 Accessibility requirements for ICT products and services](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/)<br/>ETSI / CEN / CENELEC | V4.1.1 (September 2026), aligned with WCAG 2.2; V3.2.1 where a procurement rule cites it | Accessibility of documents and software as well as web pages, for procurement and published files. | reference | [CAP-APPS](capabilities/cap-apps.md), [CAP-PUBLICATION](capabilities/cap-publication.md) |
| [WCAG 3.0](https://www.w3.org/TR/wcag-3.0/)<br/>W3C | W3C Working Draft (September 2026) | The next accessibility guidelines; not yet stable enough for a clause. | track | — |

### Open-source health and digital public goods

| Standard | Edition | Use | Verdict | Used by |
| --- | --- | --- | --- | --- |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard)<br/>OpenSSF | v5 (5.6.0, October 2026) | An automated assessment of an open-source repository's security practices, for components and for the blueprint's own repositories. | adopt | [CAP-GUARDRAILS](capabilities/cap-guardrails.md), [CAP-MODULES](capabilities/cap-modules.md) |
| [Digital Public Goods Standard](https://www.digitalpublicgoods.net/standard)<br/>Digital Public Goods Alliance | v1.1.6 (September 2024) | Criteria for open software and data recognised as digital public goods, which the blueprint aims to meet. | reference | P21 |
| [Principles for Digital Development](https://digitalprinciples.org/)<br/>Principles for Digital Development | 2024 refresh (nine principles) | Endorsed principles for public digital programmes, including people-first data practices and building for sustainability. | reference | P20, P21 |
<!-- END GENERATED: register -->
