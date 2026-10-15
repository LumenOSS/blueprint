# AGENTS.md — agent operating guide

This repository is a **blueprint**: the architecture of a governed data
platform, stated as **capabilities** with testable **contracts**. It names no
vendor in a contract. An **implementation** binds each capability to real
components and shows evidence for each contract; implementations live in
their own repositories. Start at `README.md`.

## Rules of the blueprint

- **A contract is vendor-neutral.** Product names appear only in
  implementation bindings (`docs/implementations/`) and "as implemented"
  notes.
- **A contract is testable.** Each `MUST` says how conformance is shown.
  A property that cannot be tested is a principle or a pattern, not a contract.
- **IDs are stable.** Capabilities (`CAP-…`) and contract clauses
  (`CAP-….n`) are never renumbered; a retired clause stays, marked retired.
  `blueprint/catalogue.yaml` is the single source of IDs and clause text.
- **The architecture changes only through an ADR** (`docs/adr/`). An
  implementation that cannot meet a clause records a **deviation** in its
  binding, with the consequence; it does not edit the blueprint.
- **Diagrams are C4 levels 1–3 in Mermaid**, drawn as `flowchart` with step
  edges and subgraph lanes, each with a "Why it is drawn this way" note.
  Render with `nix develop .#diagrams --command just diagrams` and look at
  the output before committing.

## Writing

- Public repository: roles, never people; no organisation, tenant, host or
  account identifiers from any real deployment.
- Google style guides (Markdown, Shell, Python) and engineering practices:
  small focused changes, names that say what a thing is, text that says why.
- Cite primary sources for any claim about research or a product's
  behaviour, with a URL and the date it was checked.

## Environment and version control

- Everything runs in the nix dev shell: `nix develop --command just <recipe>`.
  `just --list` is the index; `just check` is what a change must pass.
- Jujutsu, colocated with git: `jj describe` then `jj new`. Commits are
  Angular-style: `type(scope): subject`, imperative, lowercase, under 72
  characters, a body saying why, `BREAKING CHANGE:` in the footer when an ID
  or contract changes meaning.
