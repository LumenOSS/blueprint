# ADR-0014: Translate through PO files, and label codes in every official language

**Status:** accepted. **Date:** 2026-10-16. Proposed in
[LIP-3](../lips/lip-0003.md).

## Context

The blueprint and the platforms built from it serve people who work in
different languages. Retrofitting languages is costly, and translations
kept as copies drift silently.

## Decision

- Principle [P22](../specifications/principles.md#p22-every-language-is-a-first-language):
  every language is a first language.
- Clause CAP-REFERENCE.9: every code has a label in each official
  language, tagged with BCP 47. Catalogue 0.5.0.
- The documentation is translated through gettext PO files generated
  from the English pages; a page is published in a language only when
  fully translated. The first languages are French, Spanish and Arabic.

## Consequences

- Editing a translated English page changes PO files in the same change,
  and that page shows in English in each language until its translator
  catches up.
- The website is multilingual, with right-to-left layout for Arabic.
- Diagram labels are not yet translated; a later proposal can extract
  them.
