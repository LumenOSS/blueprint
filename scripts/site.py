#!/usr/bin/env python3
"""Stage the Markdown documentation as Hugo content for the website.

The documentation is written to read well on a code host: each directory has
a README.md, and pages link to each other with relative .md paths. Hugo
expects _index.md section pages and resolves links by page path. Rather than
keep a second copy, this script derives Hugo content from the docs on every
build:

- README.md becomes _index.md, and the repository README becomes the home
  page; CONTEXT.md becomes the domain-language page.
- The first heading becomes the page title in front matter.
- Relative links to documentation pages become Hugo page paths; links to
  anything else in the repository become links to it on the code host.
- Mermaid code fences become the theme's mermaid shortcode.

Usage:
  site.py OUTPUT_DIR
"""

import argparse
import pathlib
import posixpath
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/LumenOSS/data-platform-blueprint/blob/main"

# Repository files that become pages, and where they live on the site.
EXTRA_PAGES = {
    ROOT / "README.md": "_index.md",
    ROOT / "CONTEXT.md": "domain-language.md",
}

LINK = re.compile(r"(\]\()([^)\s]+)(\))")
FENCE = re.compile(r"^```mermaid\n(.*?)^```$", re.M | re.S)
TITLE = re.compile(r"\A# (.+)\n+")


def site_path(source: pathlib.Path) -> str:
    """Returns the content path, relative to the content root, of a page."""
    if source in EXTRA_PAGES:
        return EXTRA_PAGES[source]
    relative = source.relative_to(DOCS).as_posix()
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


def convert(source: pathlib.Path) -> str:
    """Returns the Hugo content for one Markdown source file."""
    text = source.read_text(encoding="utf-8")
    title = source.stem
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
    escaped = title.replace("\\", "\\\\").replace('"', '\\"')
    return f'---\ntitle: "{escaped}"\n---\n\n{text}'


def main() -> int:
    """Stages every page into the output directory."""
    parser = argparse.ArgumentParser(description="Stage docs as Hugo content.")
    parser.add_argument("output", type=pathlib.Path)
    output = parser.parse_args().output.resolve()
    if output.exists():
        shutil.rmtree(output)
    sources = sorted(DOCS.rglob("*.md")) + sorted(EXTRA_PAGES)
    for source in sources:
        destination = output / site_path(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(convert(source), encoding="utf-8")
    print(f"staged {len(sources)} pages into {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
