#!/usr/bin/env python3
"""Stage the Markdown documentation as Hugo content for the website.

The documentation is written to read well on a code host: each directory has
a README.md, and pages link to each other with relative .md paths. Hugo
expects _index.md section pages and resolves links by page path. Rather than
keep a second copy, this script derives Hugo content from the docs on every
build, once per language:

- README.md becomes _index.md. The repository README becomes an overview
  page and CONTRIBUTING.md the contributing page; CONTEXT-MAP.md becomes
  the section page of the bounded contexts, and each context's CONTEXT.md
  a page in that section.
- The landing page (site/home.md) is plain Markdown: its lead and buttons
  become the hero, and each "##" section a grid of cards.
- The first heading becomes the page title, and the first paragraph its
  description, in front matter. Capability pages are ordered as in the
  catalogue and tagged with their domain and layer; decision records are
  ordered by number; other pages in the order their section's README
  lists them.
- Relative links to documentation pages become Hugo page paths; in a
  translation, a link to a page not yet translated goes to the English
  page. Links to anything else in the repository go to the code host.
- Mermaid code fences become the theme's mermaid shortcode.
- Translated pages come from `l10n.py build`; those not yet reviewed carry
  a note saying so.

It also writes the Hugo language configuration, with each language's menus
labelled from its interface strings (site/i18n/<lang>.toml).

Usage:
  site.py OUTPUT_DIR --base-url URL --translations DIR
"""

import argparse
import dataclasses
import json
import pathlib
import posixpath
import re
import shutil
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
HOME = SITE / "home.md"
MENUS = SITE / "menus.toml"
STRINGS = SITE / "i18n"
LANGUAGES = ROOT / "l10n" / "languages.toml"
CATALOGUE = ROOT / "blueprint" / "catalogue.yaml"
REPO_URL = "https://github.com/LumenOSS/data-platform-blueprint/blob/main"

# Repository files that become pages, and where they live on the site.
EXTRA_PAGES = {
    ROOT / "README.md": "overview.md",
    ROOT / "CONTRIBUTING.md": "contributing.md",
    ROOT / "CONTEXT-MAP.md": "domain/contexts/_index.md",
}

LINK = re.compile(r"(\]\()([^)\s]+)(\))")
FENCE = re.compile(r"^```mermaid\n(.*?)^```$", re.M | re.S)
TITLE = re.compile(r"\A# (.+)\n+")
MARKUP = re.compile(r"\[([^\]]*)\]\([^)]*\)|[*_`]")
CAPABILITY = re.compile(
    r"^  - id: (CAP-[A-Z]+)\n    name: .*\n    domain: (\S+)\n    layer: (L\d)",
    re.M,
)
ADR_NUMBER = re.compile(r"^(\d{4})-")
UNREVIEWED = "<!-- l10n: unreviewed -->\n"
COMMENT = re.compile(r"<!--(?!\s*icon:).*?-->\n*", re.S)
ICON = re.compile(r"<!--\s*icon:\s*(\S+)\s*-->")
LONE_LINK = re.compile(r"\A\[([^\]]+)\]\(([^)\s]+)\)\Z")


@dataclasses.dataclass(frozen=True)
class Language:
    """One language of the site and the pages it has."""

    code: str
    name: str
    rtl: bool
    weight: int
    texts: pathlib.Path | None  # Translated sources; None for the source.
    pages: frozenset[pathlib.Path]  # Source paths available in it.
    base_url: str

    def url(self, ref: str, page: pathlib.Path) -> str:
        """Returns the absolute URL of a page, in English if untranslated."""
        prefix = (
            "" if self.texts is None or page not in self.pages else self.code
        )
        path = posixpath.join("/", prefix, ref.lstrip("/"))
        return self.base_url.rstrip("/") + path.rstrip("/") + "/"

    def text(self, source: pathlib.Path) -> str:
        """Returns a page's Markdown in this language, or in the source."""
        path = source
        if self.texts is not None:
            translated = self.texts / source.relative_to(ROOT)
            path = translated if translated.exists() else source
        return path.read_text(encoding="utf-8")


def site_path(source: pathlib.Path) -> str:
    """Returns the content path, relative to the content root, of a page."""
    if source in EXTRA_PAGES:
        return EXTRA_PAGES[source]
    relative = source.relative_to(DOCS).as_posix()
    if source.name == "CONTEXT.md":
        return posixpath.dirname(relative) + ".md"
    if source.name == "README.md":
        return posixpath.join(posixpath.dirname(relative), "_index.md")
    return relative


def page_ref(content_path: str) -> str:
    """Returns the Hugo page path that GetPage resolves for a content file."""
    stem = content_path.removesuffix(".md")
    if stem.endswith("_index"):
        stem = stem.removesuffix("_index").rstrip("/")
    return "/" + stem


def is_page(path: pathlib.Path) -> bool:
    """Whether a repository path is a page of the website."""
    return path.suffix == ".md" and (
        path in EXTRA_PAGES or DOCS in path.parents
    )


def rewrite_link(source: pathlib.Path, target: str, lang: Language) -> str:
    """Maps one Markdown link target from the docs to the site."""
    if re.match(r"^[a-z]+:", target) or target.startswith("#"):
        return target
    path, _, fragment = target.partition("#")
    resolved = (source.parent / path).resolve()
    suffix = f"#{fragment}" if fragment else ""
    if is_page(resolved):
        ref = page_ref(site_path(resolved))
        if lang.texts is None or resolved in lang.pages:
            return ref + suffix
        return lang.url(ref, resolved) + suffix
    in_repo = resolved.relative_to(ROOT).as_posix()
    return f"{REPO_URL}/{in_repo}{suffix}"


def capability_order() -> dict[str, tuple[int, str, str]]:
    """Maps each capability page name to its catalogue position, domain, layer.

    Read with a pattern rather than a YAML parser so the site build needs no
    Python packages; the catalogue's own checks guarantee its layout.
    """
    text = CATALOGUE.read_text(encoding="utf-8")
    return {
        f"{m.group(1).lower()}.md": (i + 1, m.group(2), m.group(3))
        for i, m in enumerate(CAPABILITY.finditer(text))
    }


def description(body: str) -> str:
    """Returns the first prose paragraph as plain text, for page cards."""
    for raw in body.split("\n\n"):
        # Generated blocks wrap their text in comment markers; read through.
        lines = [ln for ln in raw.splitlines() if not ln.startswith("<!--")]
        block = "\n".join(lines).strip()
        skip = ("#", "|", "```", "{{", "-", "Layer L", "**Status:**")
        if not block or block.startswith(skip):
            continue
        text = MARKUP.sub(lambda m: m.group(1) or "", " ".join(block.split()))
        text = text.replace("`", "")
        if len(text) > 220:
            text = text[:220].rsplit(" ", 1)[0].rstrip(",;:") + "…"
        return text
    return ""


def front_matter(fields: dict[str, object]) -> str:
    """Renders front matter; JSON values are valid YAML."""
    lines = [
        f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fields.items()
    ]
    return "---\n" + "\n".join(lines) + "\n---\n\n"


def split_header(text: str) -> tuple[dict[str, str], str]:
    """Splits simple YAML front matter (key: value lines) from the body.

    LIP headers are flat, so a line parser is enough and keeps the site
    build free of Python packages.
    """
    if not text.startswith("---\n"):
        return {}, text
    header, body = text[4:].split("\n---\n", 1)
    fields: dict[str, str] = {}
    for line in header.splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields, body.lstrip("\n")


def readme_order(source: pathlib.Path) -> int | None:
    """Returns a page's position among the links of its section's README.

    A section's README lists its pages in reading order, so the site
    orders them the same way without a second list to maintain.
    """
    readme = source.parent / "README.md"
    if source.name == "README.md" or not readme.exists():
        return None
    targets = [
        (readme.parent / m.group(2).partition("#")[0]).resolve()
        for m in LINK.finditer(readme.read_text(encoding="utf-8"))
    ]
    resolved = source.resolve()
    return targets.index(resolved) + 1 if resolved in targets else None


def convert(
    source: pathlib.Path,
    lang: Language,
    order: dict[str, tuple[int, str, str]],
) -> str:
    """Returns the Hugo content for one Markdown source file."""
    raw = lang.text(source)
    unreviewed = raw.startswith(UNREVIEWED)
    header, text = split_header(raw.removeprefix(UNREVIEWED))
    title = source.stem
    if "lip" in header:
        title = f"LIP-{header['lip']}: {header['title']}"
        if source.name == "template.md":
            title = "LIP template"
    match = TITLE.match(text)
    if match:
        title = match.group(1).strip()
        text = text[match.end() :]
    text = LINK.sub(
        lambda m: (
            m.group(1) + rewrite_link(source, m.group(2), lang) + m.group(3)
        ),
        text,
    )
    text = FENCE.sub(
        lambda m: "{{< mermaid >}}\n" + m.group(1) + "{{< /mermaid >}}", text
    )
    fields: dict[str, object] = {"title": title}
    summary = description(text)
    if summary:
        fields["description"] = summary
    if source.parent.name == "capabilities" and source.name in order:
        weight, domain, layer = order[source.name]
        fields["weight"] = weight
        fields["tags"] = [domain, layer]
    if "lip" in header and source.name != "template.md":
        fields["weight"] = int(header["lip"])
        fields["tags"] = [header.get("status", ""), header.get("type", "")]
    adr = ADR_NUMBER.match(source.name)
    if source.parent.name == "adr" and adr:
        fields["weight"] = int(adr.group(1))
    position = readme_order(source)
    if "weight" not in fields and position is not None:
        fields["weight"] = position
    if unreviewed:
        text = "{{< l10n-note >}}\n\n" + text
    return front_matter(fields) + text


def flat(text: str) -> str:
    """Joins text a translation tool wrapped across lines."""
    return " ".join(text.split())


def card_url(target: str, lang: Language) -> str:
    """Returns the absolute URL a landing-page link points to."""
    if re.match(r"^[a-z]+:", target):
        return target
    resolved = (HOME.parent / target).resolve()
    return lang.url(page_ref(site_path(resolved)), resolved)


def home(lang: Language) -> str:
    """Builds the landing page from its plain-Markdown source.

    The first paragraph is the hero's lead and the links in the next one
    its buttons. Each "##" section becomes a grid of cards: a "###"
    heading starts a card, an icon comment names its icon, and a paragraph
    that is a single link is its button and ends it.
    """
    text = COMMENT.sub("", lang.text(HOME).removeprefix(UNREVIEWED))
    match = TITLE.match(text)
    title = match.group(1).strip() if match else "Home"
    blocks = [
        b.strip() for b in text[match.end() if match else 0 :].split("\n\n")
    ]
    blocks = [b for b in blocks if b]
    lead, buttons, rest = blocks[0], blocks[1], blocks[2:]
    hero = [
        {
            "label": flat(label),
            "url": card_url(target, lang),
            "style": "primary" if i == 0 else "outline",
        }
        for i, (label, target) in enumerate(
            re.findall(r"\[([^\]]+)\]\(([^)\s]+)\)", buttons)
        )
    ]
    fields: dict[str, object] = {
        "title": title,
        "heroCaption": "LumenOSS",
        "heroLead": " ".join(lead.split()),
        "heroButtons": hero,
    }
    out: list[str] = []
    cards: list[str] = []
    card: dict[str, str] | None = None

    def flush() -> None:
        if cards:
            # The theme lays grids out in three or four columns.
            columns = 4 if len(cards) % 4 == 0 else 3
            out.append(f'{{{{< feature-grid columns="{columns}" >}}}}')
            out.extend(cards)
            out.append("{{< /feature-grid >}}")
            cards.clear()

    for block in rest:
        if block.startswith("## "):
            flush()
            out.append(block)
        elif block.startswith("### "):
            card = {"title": flat(block[4:]), "icon": "lightbulb", "body": ""}
        elif card is not None and (icon := ICON.fullmatch(block)):
            card["icon"] = icon.group(1)
        elif card is not None and (link := LONE_LINK.match(block)):
            # Raw-string (backtick) parameters, so quotation marks in a
            # translation cannot end an attribute early.
            attrs = (
                f"icon=`{card['icon']}` title=`{card['title']}` "
                f"url=`{card_url(link.group(2), lang)}` "
                f"label=`{flat(link.group(1))}` headingLevel=`h3`"
            )
            cards.append(
                f"{{{{< feature {attrs} >}}}}\n{card['body'].strip()}\n"
                "{{< /feature >}}"
            )
            card = None
        elif card is not None:
            card["body"] += flat(block) + "\n"
        else:
            flush()
            out.append(block)
    flush()
    return front_matter(fields) + "\n\n".join(out) + "\n"


def menus(code: str, strings: dict[str, dict[str, str]]) -> str:
    """Renders one language's menus, labelled in that language."""
    config = tomllib.loads(MENUS.read_text(encoding="utf-8"))
    lines: list[str] = []
    for menu, items in config.items():
        for item in items:
            lines.append(f"  [[languages.{code}.menus.{menu}]]")
            label = strings.get(f"menu-{item['identifier']}", {})
            entry = {**item, "name": label.get("other", item["name"])}
            for key, value in entry.items():
                lines.append(
                    f"    {key} = {json.dumps(value, ensure_ascii=False)}"
                )
    return "\n".join(lines)


def load_languages(
    translations: pathlib.Path, base_url: str, sources: list[pathlib.Path]
) -> list[Language]:
    """Reads the languages and finds the pages each one has."""
    config = tomllib.loads(LANGUAGES.read_text(encoding="utf-8"))
    out: list[Language] = []
    for weight, (code, spec) in enumerate(config["languages"].items(), 1):
        texts = None if code == config["source"] else translations / code
        pages = frozenset(
            s
            for s in sources
            if texts is None or (texts / s.relative_to(ROOT)).exists()
        )
        out.append(
            Language(
                code=code,
                name=spec["name"],
                rtl=spec.get("direction") == "rtl",
                weight=weight,
                texts=texts,
                pages=pages,
                base_url=base_url,
            )
        )
    return out


def language_config(langs: list[Language], content: pathlib.Path) -> str:
    """Renders the Hugo configuration for every language."""
    lines = [f'defaultContentLanguage = "{langs[0].code}"', ""]
    for lang in langs:
        path = STRINGS / f"{lang.code}.toml"
        strings = (
            tomllib.loads(path.read_text(encoding="utf-8"))
            if path.exists()
            else {}
        )
        lines += [
            f"[languages.{lang.code}]",
            f"  label = {json.dumps(lang.name, ensure_ascii=False)}",
            f'  locale = "{lang.code}"',
            f"  weight = {lang.weight}",
            f'  contentDir = "{content / lang.code}"',
        ]
        # The header shows a short title from the interface strings; the
        # landing page carries the full one.
        title = strings.get("site-title", {}).get("other")
        if title:
            lines.append(f"  title = {json.dumps(title, ensure_ascii=False)}")
        if lang.rtl:
            lines += [
                '  direction = "rtl"',
                f"  [languages.{lang.code}.params]",
                "    rtl = true",
            ]
        lines += [menus(lang.code, strings), ""]
    return "\n".join(lines)


def main() -> int:
    """Stages every page of every language into the output directory."""
    parser = argparse.ArgumentParser(description="Stage docs as Hugo content.")
    parser.add_argument("output", type=pathlib.Path)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--translations", type=pathlib.Path, required=True)
    args = parser.parse_args()
    output: pathlib.Path = args.output.resolve()
    content = output / "content"
    if content.exists():
        shutil.rmtree(content)
    order = capability_order()
    sources = sorted(DOCS.rglob("*.md")) + sorted(EXTRA_PAGES)
    langs = load_languages(args.translations.resolve(), args.base_url, sources)
    for lang in langs:
        for source in sorted(lang.pages):
            destination = content / lang.code / site_path(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                convert(source, lang, order), encoding="utf-8"
            )
        # An untranslated landing page is shown in the source language.
        (content / lang.code).mkdir(parents=True, exist_ok=True)
        (content / lang.code / "_index.md").write_text(
            home(lang), encoding="utf-8"
        )
        print(f"{lang.code}: staged {len(lang.pages)} pages")
    (output / "languages.toml").write_text(
        language_config(langs, content), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
