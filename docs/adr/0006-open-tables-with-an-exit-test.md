# ADR-0006: Keep tables in open formats and prove it with an exit test

**Status:** accepted. **Date:** 2026-10-15.

## Context

A platform's data outlives its vendors. Formats that only one engine can
read turn a vendor change into a migration. Open table formats exist and
are supported across engines, but portability decays unless it is
exercised.

## Decision

- Tables use an open, specified format with atomic commits, schema
  evolution and time travel.
- Every table is readable by at least two independent engines, and a
  periodic exit test reads a sample of gold tables with an engine other
  than the one that wrote them and compares counts and hashes.

## Consequences

- The open-source reference implementation uses Apache Iceberg, which
  every open-source catalog serves through the Iceberg REST protocol.
- The Databricks reference implementation uses Delta Lake with UniForm, so
  the same tables are readable as Iceberg.
- The exit test is a scheduled job with a cost
  ([CAP-TABLES.2](../capabilities/cap-tables.md)).
