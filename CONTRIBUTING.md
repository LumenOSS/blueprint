# Contributing

Thank you for helping. We want education authorities to adopt this
blueprint and many teams to build it, so we make every change in the open,
and the tools check it before a person reviews it. This guide tells you
which path your change takes, how to set up, and what a reviewer will look
for.

## Which path does my change take?

| Your change | Path | Example |
| --- | --- | --- |
| A typo, a broken link, clearer wording with the same meaning | An ordinary reviewed change | "Guardian relationshp" → "Guardian relationship" |
| A new or updated example on a clause | An ordinary reviewed change | An example for a clause that has none |
| A newer edition of a standard already in the register | An ordinary reviewed change, with the publisher's link | ISO 639:2023 replacing ISO 639-1:2002 |
| A new, changed or retired clause or capability | A [LIP](docs/lips/lip-0001.md) of type Standards (Contract) | A clause requiring a parity test across serving paths |
| A new term, context, aggregate, invariant or event in the domain | A LIP of type Standards (Domain) | Splitting Statistics into Collection and Publication contexts |
| A change to a schema the bindings or the catalogue use | A LIP of type Standards (Interface) | A new required field in `binding.schema.json` |
| A change to how the project works | A LIP of type Process | Changing the length of Last Call |
| A pattern, a guide or research that changes no requirement | A LIP of type Informational, or an ordinary change to `docs/guides/` | A pattern for reconciling two systems |
| A translation, or a correction to one | An ordinary reviewed change; see [translating](docs/guides/translating.md) | French for a concept page |
| A new language for the documentation | An ordinary reviewed change; see [translating](docs/guides/translating.md#add-a-language) | Adding Portuguese |
| Evidence that an implementation meets a clause | A change to that implementation's repository, moving the clause to `met` | Linking the test that proves CAP-ACCESS.7 |

If you're not sure which path applies, open a discussion and ask. It
costs nothing to start there.

## Proposing a change with a LIP

[LIP-1](docs/lips/lip-0001.md) describes the process in full. In short:

1. Describe the problem in a discussion first.
2. Copy the [template](docs/lips/template.md) to
   `docs/lips/lip-draft-<short-name>.md`, fill in every section, and open
   a change. The editors assign a number.
3. Move it to Review when the text is complete. After that it goes to a
   14-day Last Call, and then the Data Lead and the Technical Lead decide.
4. If it's accepted, we record it as a
   [decision record](docs/adr/README.md) and release it in a catalogue
   version.

Every LIP has a privacy and safeguarding section. Most of the data this
blueprint governs is about children, so tell us what your change does to
it.

## Setting up

Everything runs in the Nix dev shell, and every task is a `just` recipe.
That way your tools are the same as everyone else's.

```sh
nix develop --command just check    # everything a change must pass
nix develop --command just fmt      # format everything in place
nix develop --command just render   # regenerate the generated sections
nix develop .#site --command just site-serve   # preview the website
```

If you use [direnv](https://direnv.net/), run `direnv allow` once and it
will enter the shell for you.

## Making the change

- **Edit the source, not the output.** Clause text, levels, verification
  and examples live in [`blueprint/catalogue.yaml`](blueprint/catalogue.yaml),
  and standards live in [`blueprint/standards.yaml`](blueprint/standards.yaml).
  `just render` writes everything between `BEGIN GENERATED` and
  `END GENERATED` markers, so edit the source and then run it.
- **Let the tools format.** The formatting and lint rules live in the
  configuration files at the root. Run `just fmt` rather than fixing the
  layout by hand. If you think a rule is wrong, change it in its config
  file, in a change of its own.
- **Use the domain language.** Each bounded context keeps its terms in its
  `CONTEXT.md`, and the [context map](CONTEXT-MAP.md) lists them all. Use
  the canonical term, and never a word listed under *Avoid*. If you settle
  a new term, add it to its context's `CONTEXT.md` in the same change.
- **Write clauses that can be checked.** A clause uses MUST, SHOULD or MAY
  in the sense of [BCP 14](https://www.rfc-editor.org/info/bcp14). It says
  what is required, not which product provides it, and its `verify` says
  how a test or a reviewer can check it. If the clause is abstract, add an
  `example`.
- **Cite standards where they're published.** Link to the publisher's own
  page for the edition you rely on, and add it to the standards register.
  Don't cite someone else's summary of it.
- **Write English that translates well.** Use short sentences and plain
  words, and don't put text in images. If you edit a page that has
  translations, run `just l10n-update` in the same change. The
  [translating](docs/guides/translating.md) guide explains why.
- **Name roles, not people.** Write "the Data Lead" or "the steward of the
  learners domain", never a person's name. Don't use real learners, staff
  or institutions in examples either.

## Committing

The repository uses [jj](https://jj-vcs.github.io/jj/), colocated with
Git, but plain Git works too. Keep each change small and about one thing.

Commit messages follow the Angular convention, `type(scope): subject`.
Write the subject in lowercase, in the imperative, in under 72
characters, and use the body to say *why* you made the change. The types
are feat, fix, docs, style, refactor, perf, test, build, ci, chore and
revert. If your change breaks existing bindings, put `BREAKING CHANGE:` in
the footer.

```text
docs(catalogue): illustrate the clauses with brief examples

Several clauses are precise but abstract. Clauses can now carry an
optional example that is not part of the requirement.
```

## Review

A reviewer checks these things, in this order:

1. Does `just check` pass?
2. Did the change take the right path from the table above?
3. Are the clauses testable and product-neutral, and do they use the
   domain language?
4. Were generated sections regenerated rather than edited by hand?
5. Does the change say what it does to learners' and staff members' data,
   and is that acceptable?

Reviews follow Google's
[engineering practices](https://google.github.io/eng-practices/). In
particular, a reviewer approves a change when it makes the blueprint
better, even if it isn't perfect.

## Reporting a security or safeguarding problem

If a problem could expose people's data, please don't open a public
issue about it. Use the code host's private vulnerability reporting for
this repository, or contact the maintainers privately.

## Licence

You make your contribution under the [Apache License 2.0](LICENSE), the
licence of this repository.
