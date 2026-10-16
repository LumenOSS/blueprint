# EMIS

The language of an education management information system: the
institutions, people and relationships an education authority records, and
the statistics it produces from them. Terms about the blueprint and the
platform itself are in [docs/glossary.md](docs/glossary.md).

## Institutions and places

**Institution**:
An organisation registered to provide education, such as a school or
college, identified independently of where it operates.
_Avoid_: School (as the generic term), centre, establishment

**Site**:
A physical location where education takes place, with its buildings and
services.
_Avoid_: Campus, premises, address

**Occupancy**:
The effective-dated link between an institution and a site it operates
from; an institution may occupy several sites and a site may host several
institutions.
_Avoid_: Location assignment

**Facility status**:
The recorded condition and availability of a service at a site, such as
water, power or connectivity, as at a date.
_Avoid_: Infrastructure flag

## People and roles

**Person**:
A human being recorded once in the person registry, whatever roles they
hold.
_Avoid_: Individual, user, record

**Learner**:
A person in the role of someone enrolled, or once enrolled, in education.
_Avoid_: Student, pupil (except inside an official indicator name)

**Staff member**:
A person in the role of someone posted to a post.
_Avoid_: Employee, personnel, worker

**Teacher**:
A staff member posted to a teaching post.
_Avoid_: Educator, instructor

**Guardian**:
A person or a body with legal authority for a learner.
_Avoid_: Parent (unless the authority is parental), caregiver, carer

**Guardian relationship**:
The effective-dated link between a learner and their guardian, which ends
when the legal authority ends.
_Avoid_: Contact, next of kin

**Post**:
An established position at an institution, which exists whether or not
anyone fills it.
_Avoid_: Position, job, vacancy (a vacancy is an unfilled post)

**Posting**:
The effective-dated placement of a staff member in a post, with the share
of full time it represents.
_Avoid_: Assignment (reserved for teaching), appointment, deployment

## Participation

**Programme**:
A coherent course of education at an institution, mapped to a level of the
international classification of education.
_Avoid_: Course, track, stream

**Grade**:
A stage within a programme that a learner normally completes in one
academic year.
_Avoid_: Year group, standard, class

**Class**:
A group of learners taught together in an academic period, which may span
grades.
_Avoid_: Section, homeroom

**Enrolment**:
The effective-dated record of a learner registered at an institution in a
programme and grade for an academic period.
_Avoid_: Registration, admission

**Class membership**:
The effective-dated record of a learner belonging to a class.
_Avoid_: Class enrolment

**Assignment**:
The effective-dated record of a teacher teaching a subject to a class.
_Avoid_: Allocation, timetable slot

**Exit reason**:
Why an enrolment ended: completed, transferred, left the education system,
or deceased; distinct from the enrolment's state.
_Avoid_: Dropout status

**Progression decision**:
The recorded outcome for a learner at the end of an academic period:
promote, repeat, complete or leave.
_Avoid_: Promotion status, result

**Attendance session**:
One recorded occasion on which a learner was expected to be present, with
whether they were.
_Avoid_: Roll call, register mark

## Time

**Academic period**:
A school year, or a term within it, to which enrolments, postings and
results belong.
_Avoid_: Session, semester (unless that is the local term)

**Reference date**:
The date as at which stocks are counted for a collection or an indicator.
_Avoid_: Census day, snapshot date, as-of date

## Collection and statistics

**Collection**:
One cycle of gathering data from respondents with a given instrument.
_Avoid_: Survey, data call

**Census**:
A collection that covers every institution once a year at one reference
date.
_Avoid_: Annual survey, school return

**Instrument**:
The versioned definition of a collection's items, rules, reference date,
window and expected respondents.
_Avoid_: Form, questionnaire, template

**Return**:
One institution's response to an instrument.
_Avoid_: Submission, survey response

**Attestation**:
The head of an institution's confirmation that a return is complete and
correct.
_Avoid_: Sign-off, certification

**Snapshot**:
A locked, versioned copy of data as at a reference date, from which
official figures are computed.
_Avoid_: Extract, dump

**Measure**:
A named calculation over stored counts, defined once.
_Avoid_: Metric, KPI, statistic

**Indicator**:
A measure with published metadata, often one defined internationally.
_Avoid_: KPI, metric

## Records and identity

**Registry**:
The single authoritative store of one kind of master record (institutions,
sites, persons, posts).
_Avoid_: Register, roster, directory, master list

**External register**:
An authoritative list held by another authority, such as a civil register,
read through an adapter.
_Avoid_: Registry (which is ours), source system

**External identifier**:
An identifier issued by another authority and held as an attribute of a
person or institution.
_Avoid_: National ID as a key, reference number

**Data subject**:
The person a record is about.
_Avoid_: Owner, user

**Individual disclosure**:
The release of a person's own records to that person, their guardian or an
authorised agency.
_Avoid_: Export, data request, extract

**Publication**:
The open release of aggregate statistics.
_Avoid_: Open data dump, report, extract
