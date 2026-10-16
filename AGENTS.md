# AGENTS.md — agent operating guide

This repository is a **blueprint**: the architecture of a governed data
platform, stated as **capabilities** with testable **contracts**. An
**implementation** binds each capability to components and shows evidence
for each clause; implementations live in their own repositories. Start at
`README.md`; to build an implementation, follow `docs/building.md`.

## Rules of the blueprint

- **The catalogue is the source.** `blueprint/catalogue.yaml` holds every
  capability ID and clause text. Edit it, then run `just render`: contract
  tables, the index, the build order and the implementation matrix are
  generated from it and from `docs/implementations/*.yaml`. Text between
  `BEGIN GENERATED` and `END GENERATED` markers is never edited by hand.
- **A contract is vendor-neutral and testable.** Product names appear only
  in bindings and in "Notes". Each clause says how conformance is shown; an
  idea that cannot be tested is a principle, not a clause.
- **IDs are stable.** Clauses run 1..n and are never renumbered, removed
  or reused; a retired clause stays, with `retired:` saying why.
- **The architecture changes only through a LIP** (`docs/lips/`, process
  in LIP-1); an accepted LIP is recorded as an ADR (`docs/adr/`). Small
  corrections that change no meaning need neither. An implementation that
  cannot meet a clause records a `deviation` in its binding; it does not
  edit the contract.
- **Diagrams are C4 levels 1–3 in Mermaid**, drawn as `flowchart` with step
  edges and subgraph lanes, each followed by "Why it is drawn this way".
  Render with `nix develop .#diagrams --command just diagrams` and look at
  every PNG in `build/` before committing.

## Writing

- **Use the domain language in `CONTEXT.md`.** Each concept has one
  canonical term; the words listed under *Avoid* are not used. When a new
  domain term is settled, add it to `CONTEXT.md` in the same change.

- The repository is meant to be public: roles, never people; no
  organisation, tenant, host or account identifiers from any deployment.
- Google style guides (Markdown, Shell, Python) and engineering practices:
  small focused changes, names that say what a thing is, text that says why.
- Cite primary sources for claims about research or a product's behaviour,
  with the date checked; mark what could not be confirmed as unverified.

## Environment and version control

- Everything runs in the Nix dev shell: `nix develop --command just
  <recipe>`. `just check` is what a change must pass.
- Formatting and linting are the tools' job: `just fmt` fixes, and each
  tool's rules live in its config file at the root. Change a rule in config,
  never by hand-editing around it.
- Jujutsu, colocated with git: `jj describe` then `jj new`. Commits are
  Angular-style: `type(scope): subject`, imperative, lowercase, under 72
  characters, a body saying why, and `BREAKING CHANGE:` in the footer when a
  clause's meaning changes.
- Checks run on Azure Pipelines (`azure-pipelines.yml`). GitHub Actions
  only publishes the documentation website to GitHub Pages
  (`.github/workflows/pages.yml`), using the same `just site` recipe.
- The website is generated from `docs/` by `scripts/site.py` and Hugo
  (`site/`); never edit generated site content, edit the docs.
