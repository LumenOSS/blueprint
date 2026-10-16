# Indicators

How an EMIS defines, computes and publishes the indicators it reports. The
rules apply to every indicator; the families below show what each kind is
built from.

## What every indicator declares

From [CAP-SEMANTICS.3](../capabilities/cap-semantics.md), each indicator is
defined once, in the [semantic layer](../architecture/semantic-layer.md),
with:

| Question | What the metadata states |
| --- | --- |
| What does it mean? | A stable code and name, what it measures, and how to read high and low values |
| How is it computed? | Numerator and denominator as separate measures over stored counts, the unit, and the reference-date rule |
| How may it be broken down? | The dimensions it can be disaggregated by |
| Where do the counts come from? | Source tables and how often they refresh |
| When can it be published? | The coverage it needs, and the biases it is known to have |
| Who answers for it? | The owning role, and the version of the definition each figure used |

A denominator from outside the system, such as a population estimate by
single year of age, is versioned reference data with its source and
vintage ([CAP-SEMANTICS.5](../capabilities/cap-semantics.md)).

## International definitions

Indicators with an international definition follow the
[UIS Official List of SDG 4 Indicators](https://www.uis.unesco.org/en/methods-and-tools/sdg4-indicators)
(October 2026 edition) and the definitions in the
[UIS Glossary: Education Metadata](https://databrowser.uis.unesco.org/glossary)
(2026); the codes of the twelve global indicators are those of the UN
[global indicator framework](https://unstats.un.org/sdgs/indicators/indicators-list/)
after its 2026 refinement. Each indicator records the edition it follows
([CAP-SEMANTICS.4](../capabilities/cap-semantics.md)), because these lists
change: the October 2026 revision, for example, removed the
pupil–qualified-teacher ratio and redefined 4.c.2 as the pupil–teacher
ratio. The [standards register](../standards.md#education-classifications-and-indicators)
records the editions relied on.

## Families

| Family | Examples | SDG 4 codes | Built from |
| --- | --- | --- | --- |
| Participation | Gross enrolment ratio, total net enrolment rate, out-of-school rate, participation one year before primary | 4.1.4, 4.2.2, 4.2.4, 4.3.2, 4.3.3 | Enrolments at the reference date; population by single year of age (external) |
| Internal efficiency | Promotion, repetition and dropout rates; gross intake ratio to the last grade; over-age for grade; completion | 4.1.2, 4.1.3, 4.1.5 | Enrolments in two consecutive periods, repeaters and progression decisions |
| Learning outcomes | Share of learners reaching minimum proficiency | 4.1.1, 4.1.6 | Assessment results, with the proficiency threshold as reference data |
| Teachers | Pupil–teacher ratio, share of teachers with the minimum qualification, share with the national professional qualification | 4.c.1, 4.c.2, 4.c.3 | Postings, qualifications (classified with ISCED-T) and enrolments at the reference date |
| Facilities | Schools offering basic services; learners receiving school meals | 4.a.1, 4.a.4 | Facility status records and programme participation |
| Equity | Adjusted parity indices by sex, location, wealth and disability | 4.5.1 | Any of the above, disaggregated |
| Finance | Expenditure per student; expenditure by source | 4.5.4, 4.5.6 | Expenditure by function and enrolments |
| Attendance | Attendance rate over a period | National | Attendance sessions and active enrolments |

Three conventions follow from the international definitions:

- **Parity indices are adjusted.** The ratio of one group to another is
  folded so it is symmetrical around 1: if the ratio is above 1 it becomes
  2 minus its inverse. Publications say which form they use.
- **Completion from administrative data is a proxy.** The SDG completion
  rate is defined over a cohort above the intended age and is measured
  mainly by household surveys; an EMIS figure is labelled as a proxy.
- **Out-of-school counts need every level.** A learner enrolled at any
  level is in school, so the learner registry must cover all levels or the
  rate is overstated.

## Worked example: gross enrolment ratio

The gross enrolment ratio for a level is total enrolment in that level,
regardless of age, as a percentage of the population of official school
age for that level.

1. **Gold stores counts** as at the census reference date: learners enrolled
   in each level, by area and sex, with levels mapped to ISCED 2011
   ([CAP-TRANSFORMATION.5](../capabilities/cap-transformation.md),
   [CAP-REFERENCE.4](../capabilities/cap-reference.md)).
2. **The denominator is reference data:** the population of official school
   age by area, sex and single year of age, with its source and vintage
   ([CAP-SEMANTICS.5](../capabilities/cap-semantics.md)).
3. **The semantic layer defines the ratio once,** with its metadata and the
   edition of the definition it follows
   ([CAP-SEMANTICS](../capabilities/cap-semantics.md)).
4. **The snapshot is locked** when the census completeness gate reads CLEAR
   for the area ([CAP-COLLECTION.4](../capabilities/cap-collection.md)).
5. **Publication applies disclosure control,** then the figure is published
   with a permanent identifier and its metadata
   ([CAP-PUBLICATION](../capabilities/cap-publication.md)).
6. **A revision,** whether a late correction or a new population estimate,
   is a new version of the snapshot and of the published table; the earlier
   one stays readable.

Because the ratio is derived from counts and a versioned denominator, the
same definition gives the national figure and every area's figure, and a
change of population estimate is visible as a new version rather than a
silent shift. The ratio can exceed 100 per cent, which is expected when
learners outside the official age are enrolled.
