#!/usr/bin/env python3
"""Stage the Markdown documentation as Hugo content for the website.

The documentation is written to read well on a code host: each directory has
a README.md, and pages link to each other with relative .md paths. Hugo
expects _index.md section pages and resolves links by page path. Rather than
keep a second copy, this script derives Hugo content from the docs on every
build:

- README.md becomes _index.md. The repository README becomes an overview
  page and CONTRIBUTING.md the contributing page; CONTEXT-MAP.md becomes
  the section page of the bounded contexts, and each context's CONTEXT.md
  a page in that section. The landing page itself is site content
  (site/home.md), copied as it is.
- The first heading becomes the page title, and the first paragraph its
  description, in front matter. Capability pages are ordered as in the
  catalogue and tagged with their domain and layer; decision records are
  ordered by number.
- Relative links to documentation pages become Hugo page paths; links to
  anything else in the repository become links to it on the code host.
- Mermaid code fences become the theme's mermaid shortcode.

Usage:
  site.py OUTPUT_DIR
"""

import argparse
import json
import pathlib
import posixpath
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
HOME = ROOT / "site" / "home.md"
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


def rewrite_link(source: pathlib.Path, target: str) -> str:
    """Maps one Markdown link target from the docs to the site."""
    if re.match(r"^[a-z]+:", target) or target.startswith("#"):
        return target
    path, _, fragment = target.partition("#")
    resolved = (source.parent / path).resolve()
    suffix = f"#{fragment}" if fragment else ""
    is_page = resolved.suffix == ".md" and (
        resolved in EXTRA_PAGES or DOCS in resolved.parents
    )
    if is_page:
        return page_ref(site_path(resolved)) + suffix
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
    source: pathlib.Path, order: dict[str, tuple[int, str, str]]
) -> str:
    """Returns the Hugo content for one Markdown source file."""
    header, text = split_header(source.read_text(encoding="utf-8"))
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
        lambda m: m.group(1) + rewrite_link(source, m.group(2)) + m.group(3),
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
    return front_matter(fields) + text


def main() -> int:
    """Stages every page into the output directory."""
    parser = argparse.ArgumentParser(description="Stage docs as Hugo content.")
    parser.add_argument("output", type=pathlib.Path)
    output = parser.parse_args().output.resolve()
    if output.exists():
        shutil.rmtree(output)
    order = capability_order()
    sources = sorted(DOCS.rglob("*.md")) + sorted(EXTRA_PAGES)
    for source in sources:
        destination = output / site_path(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(convert(source, order), encoding="utf-8")
    shutil.copyfile(HOME, output / "_index.md")
    print(f"staged {len(sources)} pages into {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
