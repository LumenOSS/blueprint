# Contributing

Thank you for helping. This blueprint is meant to be adopted by education
authorities and built by many teams, so every change is made in the open
and checked by machine before a person reviews it. This guide says which
path a change takes, how to set up, and what a reviewer will look for.

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
| A pattern, a guide or research that changes no requirement | A LIP of type Informational, or an ordinary change to `docs/patterns/` | A pattern for reconciling two systems |
| Evidence that an implementation meets a clause | A change to that implementation's repository, moving the clause to `met` | Linking the test that proves CAP-ACCESS.7 |

If you are unsure, open a discussion and ask; it costs nothing to start
there.

## Proposing a change with a LIP

The process is in [LIP-1](docs/lips/lip-0001.md); in short:

1. Describe the problem in a discussion first.
2. Copy the [template](docs/lips/template.md) to
   `docs/lips/lip-draft-<short-name>.md`, fill in every section, and open
   a change. The editors assign a number.
3. Move it to Review when the text is complete; it then goes to a 14-day
   Last Call and a decision by the Data Lead and the Technical Lead.
4. An accepted LIP is recorded as a [decision record](docs/adr/README.md)
   and released in a catalogue version.

Every LIP has a privacy and safeguarding section. The data this blueprint
governs is mostly about children; say what your change does to it.

## Setting up

Everything runs in the Nix dev shell, and every task is a `just` recipe,
so your tools match everyone else's.

```sh
nix develop --command just check    # everything a change must pass
nix develop --command just fmt      # format everything in place
nix develop --command just render   # regenerate the generated sections
nix develop .#site --command just site-serve   # preview the website
```

With [direnv](https://direnv.net/), `direnv allow` enters the shell for you.

## Making the change

- **Edit the source, not the output.** Clause text, levels, verification
  and examples live in [`blueprint/catalogue.yaml`](blueprint/catalogue.yaml);
  standards in [`blueprint/standards.yaml`](blueprint/standards.yaml).
  Anything between `BEGIN GENERATED` and `END GENERATED` markers is
  written by `just render`; edit the source and run it.
- **Let the tools format.** Formatting and lint rules live in the
  configuration files at the root. Run `just fmt` rather than fixing
  layout by hand; if a rule is wrong, change the rule in its config file,
  in its own change.
- **Use the domain language.** Each bounded context's terms are in its
  `CONTEXT.md`, listed in the [context map](CONTEXT-MAP.md). Use the
  canonical term, never a word under *Avoid*. A new term goes into its
  context's `CONTEXT.md` in the same change.
- **Write clauses that can be checked.** A clause uses MUST, SHOULD or MAY
  in the sense of [BCP 14](https://www.rfc-editor.org/info/bcp14), says
  what is required rather than which product provides it, and has a
  `verify` that a test or a reviewer can apply. Add an `example` when the
  clause is abstract.
- **Cite standards where they are published.** Link the publisher's own
  page for the edition you rely on, and add it to the standards register,
  rather than citing a summary of it.
- **Name roles, not people.** Write "the Data Lead", "the steward of the
  learners domain", never a person's name, and no real learners, staff or
  institutions in examples.

## Committing

The repository uses [jj](https://jj-vcs.github.io/jj/) colocated with Git;
plain Git works too. Keep each change small and about one thing.

Commit messages follow the Angular convention: `type(scope): subject`,
with a lowercase, imperative subject under 72 characters, and a body that
says *why*. Types are feat, fix, docs, style, refactor, perf, test, build,
ci, chore and revert. Put `BREAKING CHANGE:` in the footer when a change
breaks existing bindings.

```text
docs(catalogue): illustrate the clauses with brief examples

Several clauses are precise but abstract. Clauses can now carry an
optional example that is not part of the requirement.
```

## Review

A reviewer checks, in order:

1. `just check` passes.
2. The change took the right path from the table above.
3. Clauses are testable, product-neutral and use the domain language.
4. Generated sections were regenerated, not edited.
5. The effect on learners' and staff members' data is stated and
   acceptable.

Reviews follow Google's
[engineering practices](https://google.github.io/eng-practices/): a change
is approved when it improves the blueprint, even if it is not perfect.

## Reporting a security or safeguarding problem

Do not open a public issue for a problem that could expose people's data.
Use the code host's private vulnerability reporting for this repository,
or contact the maintainers privately.

## Licence

Contributions are made under the [Apache License 2.0](LICENSE), the
licence of this repository.
