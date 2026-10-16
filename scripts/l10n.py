#!/usr/bin/env python3
"""Translate the documentation through gettext PO files.

English Markdown is the only source. Each source page has a template
(l10n/templates/<path>.pot) of its translatable strings, and each language
a PO file (l10n/<lang>/<path>.po) holding their translations. Translators
work in the PO files, locally or on a translation platform; the website
build turns complete PO files back into translated pages.

Front matter and fenced code blocks (including diagrams) are kept out of
the templates: they are swapped for placeholders before extraction and
restored after translation, so a translation can never break them.
Decision records and proposals stay in English, the language they were
decided in.

Usage:
  l10n.py update        regenerate templates and merge them into PO files
  l10n.py check         fail if templates or PO files are stale or invalid
  l10n.py status        report translation coverage per language
  l10n.py build OUT     write the translated pages to OUT/<lang>/
"""

import argparse
import filecmp
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
L10N = ROOT / "l10n"
LANGUAGES = L10N / "languages.toml"
WORK = ROOT / "build" / "l10n"

# Pages outside docs/ that are translated, and docs/ sections that are not.
EXTRA_SOURCES = [
    "README.md",
    "CONTEXT-MAP.md",
    "CONTRIBUTING.md",
    "site/home.md",
]
UNTRANSLATED = {"adr", "lips"}

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
FENCED = re.compile(r"^```.*?^```[ \t]*$", re.M | re.S)
KEEP = re.compile(r"<!-- l10n-keep (\d+) -->")
STATS = re.compile(r"(\d+) (translated|fuzzy|untranslated)")
HEADER = (
    'msgid ""\n'
    'msgstr ""\n'
    '"Project-Id-Version: lumenoss-blueprint\\n"\n'
    '"MIME-Version: 1.0\\n"\n'
    '"Content-Type: text/plain; charset=UTF-8\\n"\n'
    '"Content-Transfer-Encoding: 8bit\\n"\n'
)
REVIEW = "X-Review-Status"


def languages() -> dict[str, dict[str, str]]:
    """Returns the target languages (every language but the source)."""
    config = tomllib.loads(LANGUAGES.read_text(encoding="utf-8"))
    return {
        code: spec
        for code, spec in config["languages"].items()
        if code != config["source"]
    }


def sources() -> list[str]:
    """Returns every translated source page, relative to the root."""
    pages = [
        p.relative_to(ROOT).as_posix()
        for p in DOCS.rglob("*.md")
        if p.relative_to(DOCS).parts[0] not in UNTRANSLATED
    ]
    return sorted(pages + EXTRA_SOURCES)


def stem(page: str) -> str:
    """Returns a page's path without its .md suffix."""
    return page.removesuffix(".md")


def protect(text: str) -> tuple[str, list[str]]:
    """Sets front matter aside and numbers the fenced blocks.

    Returns the translatable text and the kept blocks; kept[0] is the
    front matter, or an empty string when the page has none.
    """
    front = FRONT_MATTER.match(text)
    kept = [front.group(0) if front else ""]
    text = text[front.end() :] if front else text

    def keep(match: re.Match[str]) -> str:
        kept.append(match.group(0))
        return f"<!-- l10n-keep {len(kept) - 1} -->"

    return FENCED.sub(keep, text), kept


def restore(text: str, kept: list[str]) -> str:
    """Puts the front matter and fenced blocks back."""
    return kept[0] + KEEP.sub(lambda m: kept[int(m.group(1))], text)


def run(*args: str, cwd: pathlib.Path | None = None) -> str:
    """Runs a command, failing loudly, and returns its standard error."""
    done = subprocess.run(
        args, cwd=cwd, check=True, capture_output=True, text=True
    )
    return done.stderr


def stage_protected(into: pathlib.Path) -> dict[str, list[str]]:
    """Writes the protected form of every source; returns the kept blocks."""
    kept: dict[str, list[str]] = {}
    for page in sources():
        text, kept[page] = protect((ROOT / page).read_text(encoding="utf-8"))
        target = into / page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return kept


def normalise_header(path: pathlib.Path, extra: dict[str, str]) -> None:
    """Replaces a PO file's header with a fixed one, so output is stable.

    Tools stamp headers with dates and versions; dropping them keeps the
    files byte-identical when nothing was translated. Source locations
    lose the staging directory's prefix.
    """
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    entries = [
        b for b in blocks if b.strip() and 'msgid ""\nmsgstr ""' not in b
    ]
    body = "\n\n".join(entries).replace("#: src/", "#: ")
    fields = "".join(f'"{k}: {v}\\n"\n' for k, v in sorted(extra.items()))
    path.write_text(
        HEADER + fields + "\n" + body.rstrip("\n") + "\n", encoding="utf-8"
    )


def header_fields(path: pathlib.Path) -> dict[str, str]:
    """Reads the custom fields of a PO file's header."""
    head = path.read_text(encoding="utf-8").split("\n\n", 1)[0]
    pairs = re.findall(r'^"([A-Za-z-]+): (.*?)\\n"$', head, re.M)
    return dict(pairs)


def update(l10n: pathlib.Path) -> None:
    """Regenerates the templates and merges them into every PO file."""
    templates = l10n / "templates"
    if templates.exists():
        shutil.rmtree(templates)
    with tempfile.TemporaryDirectory() as tmp:
        protected = pathlib.Path(tmp) / "src"
        stage_protected(protected)
        # One conversion over the whole tree: page.md becomes page.pot.
        run(
            "md2po",
            "--pot",
            "--duplicates=merge",
            "--progress=none",
            "-i",
            "src",
            "-o",
            str(templates),
            cwd=pathlib.Path(tmp),
        )
    for page in sources():
        pot = templates / f"{stem(page)}.pot"
        run(
            "msgcat",
            "--add-location=file",
            "--no-wrap",
            "-o",
            str(pot),
            str(pot),
        )
        normalise_header(pot, {})
    wanted = {f"{stem(p)}.po" for p in sources()}
    for code in languages():
        directory = l10n / code
        for po in sorted(directory.rglob("*.po")):
            if po.relative_to(directory).as_posix() not in wanted:
                po.unlink()
        for page in sources():
            pot = templates / f"{stem(page)}.pot"
            po = directory / f"{stem(page)}.po"
            fields = {"Language": code, REVIEW: "unreviewed"}
            if po.exists():
                fields.update(header_fields(po))
                run(
                    "msgmerge",
                    "--quiet",
                    "--update",
                    "--backup=none",
                    "--add-location=file",
                    "--no-wrap",
                    str(po),
                    str(pot),
                )
            else:
                po.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(pot, po)
            normalise_header(po, {k: fields[k] for k in ("Language", REVIEW)})


def statistics(po: pathlib.Path) -> dict[str, int]:
    """Counts translated, fuzzy and untranslated strings in a PO file."""
    report = run("msgfmt", "--statistics", "-o", "/dev/null", str(po))
    counts = {"translated": 0, "fuzzy": 0, "untranslated": 0}
    for number, kind in STATS.findall(report):
        counts[kind] = int(number)
    return counts


def complete(po: pathlib.Path) -> bool:
    """A page is published in a language only when fully translated."""
    counts = statistics(po)
    return counts["translated"] > 0 and not (
        counts["fuzzy"] or counts["untranslated"]
    )


def check() -> int:
    """Fails if any template or PO file is stale, or any PO file invalid."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        fresh = pathlib.Path(tmp) / "l10n"
        shutil.copytree(L10N, fresh)
        update(fresh)
        for path in sorted(fresh.rglob("*.po*")):
            committed = L10N / path.relative_to(fresh)
            if not committed.exists() or not filecmp.cmp(
                path, committed, shallow=False
            ):
                rel = committed.relative_to(ROOT)
                problems.append(f"{rel}: stale; run `just l10n-update`")
        for path in sorted(L10N.rglob("*.po*")):
            if not (fresh / path.relative_to(L10N)).exists():
                rel = path.relative_to(ROOT)
                problems.append(f"{rel}: orphaned; run `just l10n-update`")
    for po in sorted(L10N.rglob("*.po")):
        try:
            run("msgfmt", "--check-format", "-o", "/dev/null", str(po))
        except subprocess.CalledProcessError as error:
            problems.append(f"{po.relative_to(ROOT)}: {error.stderr.strip()}")
    for problem in problems:
        print(problem, file=sys.stderr)
    if not problems:
        print(f"l10n: {len(sources())} pages, {len(languages())} languages")
    return 1 if problems else 0


def status() -> int:
    """Prints translation coverage per language."""
    print("| Language | Pages complete | Strings translated |")
    print("| --- | --- | --- |")
    for code, spec in languages().items():
        pages = done = strings = total = 0
        for page in sources():
            po = L10N / code / f"{stem(page)}.po"
            counts = statistics(po)
            strings += counts["translated"]
            total += sum(counts.values())
            pages += 1
            done += complete(po)
        share = 100 * strings // total if total else 0
        print(f"| {spec['name']} ({code}) | {done} of {pages} | {share}% |")
    return 0


def build(out: pathlib.Path) -> int:
    """Writes every fully translated page to OUT/<lang>/<path>."""
    if out.exists():
        shutil.rmtree(out)
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp)
        kept = stage_protected(work / "src")
        for code in languages():
            # One conversion per language; incomplete pages are dropped.
            run(
                "po2md",
                "--progress=none",
                "-t",
                str(work / "src"),
                "-i",
                str(L10N / code),
                "-o",
                str(work / code),
            )
            for page in sources():
                po = L10N / code / f"{stem(page)}.po"
                if not complete(po):
                    continue
                text = (work / code / page).read_text(encoding="utf-8")
                text = restore(text, kept[page])
                if header_fields(po).get(REVIEW) != "reviewed":
                    text = "<!-- l10n: unreviewed -->\n" + text
                target = out / code / page
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
    return 0


def main() -> int:
    """Runs one subcommand and returns the process exit code."""
    parser = argparse.ArgumentParser(description="Documentation translation.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("update")
    sub.add_parser("check")
    sub.add_parser("status")
    build_parser = sub.add_parser("build")
    build_parser.add_argument("output", type=pathlib.Path)
    args = parser.parse_args()
    if args.command == "update":
        update(L10N)
        return 0
    if args.command == "check":
        return check()
    if args.command == "status":
        return status()
    return build(args.output.resolve())


if __name__ == "__main__":
    sys.exit(main())
