#!/usr/bin/env python3
"""Check and render the blueprint catalogue and implementation bindings.

The catalogue (blueprint/catalogue.yaml) is the single source of capability
IDs and contract text. Capability pages carry generated sections, so the
text is written once and read where people look for it.

Usage:
  blueprint.py check              validate the catalogue, pages and bindings
  blueprint.py render             regenerate every generated section
  blueprint.py binding FILE...    validate bindings and report coverage
"""

import argparse
import json
import pathlib
import re
import sys
from typing import Any, NotRequired, TypedDict, cast

import jsonschema
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOGUE = ROOT / "blueprint" / "catalogue.yaml"
CAPABILITY_DOCS = ROOT / "docs" / "capabilities"
IMPLEMENTATION_DOCS = ROOT / "docs" / "implementations"
BUILDING_GUIDE = ROOT / "docs" / "building.md"
SCHEMAS = ROOT / "schema"

BEGIN = "<!-- BEGIN GENERATED: {name} (just render) -->"
END = "<!-- END GENERATED: {name} -->"
# Layer numbers are trust levels, not build order: modules (L2) are built
# straight after bootstrap because every stack, bootstrap's included,
# consumes them.
BUILD_RANK = {"L0": 0, "L2": 1, "L1": 2, "L3": 3}
ID_IN_TEXT = re.compile(r"\bCAP-[A-Z]+(?:\.[0-9]+)?\b")


# The shapes below mirror schema/*.schema.json. The schema validates a file
# before any of these types is trusted.


class Clause(TypedDict):
    """One contract clause."""

    id: str
    level: str
    text: str
    verify: str
    retired: NotRequired[str]


class Capability(TypedDict):
    """One capability and its contract."""

    id: str
    name: str
    domain: str
    layer: str
    summary: str
    depends_on: NotRequired[list[str]]
    clauses: list[Clause]


class Named(TypedDict):
    """A layer or a domain."""

    id: str
    name: str
    summary: str


class Catalogue(TypedDict):
    """The whole catalogue."""

    version: str
    layers: list[Named]
    domains: list[Named]
    capabilities: list[Capability]


class Component(TypedDict):
    """A component an implementation binds to a capability."""

    name: str


class ClauseStatus(TypedDict):
    """An implementation's status for one clause."""

    clause: str
    status: str


class Binding(TypedDict):
    """One capability's binding in an implementation."""

    capability: str
    components: list[Component]
    clauses: list[ClauseStatus]


class Implementation(TypedDict):
    """An implementation's identity."""

    name: str


class BlueprintRef(TypedDict):
    """The catalogue version a binding file targets."""

    version: str


class BindingFile(TypedDict):
    """A whole binding file."""

    blueprint: BlueprintRef
    implementation: Implementation
    bindings: list[Binding]


def load_yaml(path: pathlib.Path) -> Any:
    """Parses one YAML file."""
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def schema_errors(document: Any, schema_name: str) -> list[str]:
    """Returns every violation of the named JSON Schema, one per line."""
    schema = cast(
        "dict[str, Any]",
        json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8")),
    )
    validator = jsonschema.Draft202012Validator(schema)
    # The types-jsonschema stub leaves one overload's parameter untyped.
    found = validator.iter_errors(document)  # pyright: ignore[reportUnknownMemberType]
    errors = sorted(found, key=str)
    return [
        f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
        for e in errors
    ]


def page_path(capability_id: str) -> pathlib.Path:
    """Returns the page that documents a capability."""
    return CAPABILITY_DOCS / f"{capability_id.lower()}.md"


def check_catalogue(cat: Catalogue) -> list[str]:
    """Returns the catalogue's internal inconsistencies."""
    problems: list[str] = []
    layers = {layer["id"] for layer in cat["layers"]}
    domains = {domain["id"] for domain in cat["domains"]}
    ids = [c["id"] for c in cat["capabilities"]]
    problems += [
        f"{dup}: duplicate capability id"
        for dup in sorted({i for i in ids if ids.count(i) > 1})
    ]
    known = set(ids)
    for cap in cat["capabilities"]:
        cid = cap["id"]
        if cap["layer"] not in layers:
            problems.append(f"{cid}: unknown layer {cap['layer']}")
        if cap["domain"] not in domains:
            problems.append(f"{cid}: unknown domain {cap['domain']}")
        problems += [
            f"{cid}: depends on unknown {dep}"
            for dep in cap.get("depends_on", [])
            if dep not in known
        ]
        problems += clause_numbering(cap)
        if not page_path(cid).exists():
            page = page_path(cid).relative_to(ROOT)
            problems.append(f"{cid}: missing page {page}")
    return problems + dependency_cycles(cat)


def clause_numbering(cap: Capability) -> list[str]:
    """Clauses run 1..n with no gaps.

    A retired clause stays in place, so a gap means an ID was deleted and
    could later be reused with a different meaning.

    Args:
      cap: The capability to check.

    Returns:
      The numbering problems found.
    """
    problems: list[str] = []
    numbers: list[int] = []
    for clause in cap["clauses"]:
        prefix, _, number = clause["id"].partition(".")
        if prefix != cap["id"]:
            problems.append(f"{clause['id']}: belongs under {prefix}")
        numbers.append(int(number))
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append(f"{cap['id']}: clauses must run 1..n, got {numbers}")
    return problems


def dependency_cycles(cat: Catalogue) -> list[str]:
    """Returns every dependency cycle among capabilities."""
    graph = {c["id"]: c.get("depends_on", []) for c in cat["capabilities"]}
    state: dict[str, str] = {}
    problems: list[str] = []

    def visit(node: str, path: list[str]) -> None:
        state[node] = "open"
        for dep in graph.get(node, []):
            if state.get(dep) == "open":
                cycle = " -> ".join([*path, dep])
                problems.append(f"dependency cycle: {cycle}")
            elif dep not in state:
                visit(dep, [*path, dep])
        state[node] = "done"

    for node in sorted(graph):
        if node not in state:
            visit(node, [node])
    return problems


def check_references(cat: Catalogue) -> list[str]:
    """Returns every CAP id written in the docs that does not exist."""
    known = {c["id"] for c in cat["capabilities"]}
    known |= {cl["id"] for c in cat["capabilities"] for cl in c["clauses"]}
    problems: list[str] = []
    for path in sorted(ROOT.glob("**/*.md")):
        relative = path.relative_to(ROOT)
        if relative.parts[0] == "build":
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines, 1):
            problems += [
                f"{relative}:{n}: unknown id {ref}"
                for ref in ID_IN_TEXT.findall(line)
                if ref not in known
            ]
    return problems


def load_binding(path: pathlib.Path) -> tuple[BindingFile | None, list[str]]:
    """Loads a binding file, or returns its schema violations."""
    doc = load_yaml(path)
    errors = schema_errors(doc, "binding.schema.json")
    if errors:
        return None, [f"{path.name}: {e}" for e in errors]
    return cast("BindingFile", doc), []


def binding_problems(
    path: pathlib.Path, cat: Catalogue
) -> tuple[list[str], str]:
    """Validates one binding file against the catalogue.

    Args:
      path: The binding file.
      cat: The catalogue it must match.

    Returns:
      The problems found, and a one-line summary of clause statuses.
    """
    doc, problems = load_binding(path)
    if doc is None:
        return problems, ""
    name = path.name
    if doc["blueprint"]["version"] != cat["version"]:
        problems.append(
            f"{name}: written against {doc['blueprint']['version']}, "
            f"catalogue is {cat['version']}"
        )
    caps = {c["id"]: c for c in cat["capabilities"]}
    statuses: dict[str, dict[str, str]] = {}
    for binding in doc["bindings"]:
        cid = binding["capability"]
        if cid not in caps:
            problems.append(f"{name}: {cid} is not in the catalogue")
            continue
        if cid in statuses:
            problems.append(f"{name}: {cid} bound twice")
        own = {cl["id"] for cl in caps[cid]["clauses"]}
        problems += [
            f"{name}: {st['clause']} is not a clause of {cid}"
            for st in binding["clauses"]
            if st["clause"] not in own
        ]
        statuses[cid] = {
            st["clause"]: st["status"] for st in binding["clauses"]
        }
    problems += unbound(name, cat, statuses)
    counts: dict[str, int] = {}
    for seen in statuses.values():
        for status in seen.values():
            counts[status] = counts.get(status, 0) + 1
    summary = ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    return problems, f"{name}: {summary}"


def unbound(
    name: str, cat: Catalogue, statuses: dict[str, dict[str, str]]
) -> list[str]:
    """Returns capabilities and live MUST clauses a binding leaves out."""
    problems: list[str] = []
    for cap in cat["capabilities"]:
        if cap["id"] not in statuses:
            problems.append(f"{name}: {cap['id']} is not bound")
            continue
        problems += [
            f"{name}: MUST clause {cl['id']} has no status"
            for cl in cap["clauses"]
            if cl["level"] == "MUST"
            and "retired" not in cl
            and cl["id"] not in statuses[cap["id"]]
        ]
    return problems


# Rendering ------------------------------------------------------------------


def replace_generated(text: str, name: str, body: str) -> str:
    """Replaces the body of the named generated block in a page."""
    begin, end = BEGIN.format(name=name), END.format(name=name)
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise ValueError(f"no generated block named {name!r}")
    return pattern.sub(lambda _: f"{begin}\n{body}\n{end}", text)


def separator(columns: int) -> str:
    """Returns a table's header separator in the form the formatter keeps."""
    return "|" + " --- |" * columns


def cell(text: str) -> str:
    """Flattens text into one Markdown table cell."""
    return " ".join(text.split()).replace("|", "\\|")


def contract_table(cap: Capability) -> str:
    """Renders a capability's clauses as a Markdown table."""
    rows = [
        "| Clause | Level | Requirement | How conformance is shown |",
        separator(4),
    ]
    for cl in cap["clauses"]:
        text = cell(cl["text"])
        if "retired" in cl:
            text = f"~~{text}~~ Retired: {cell(cl['retired'])}"
        verify = cell(cl["verify"])
        rows.append(f"| {cl['id']} | {cl['level']} | {text} | {verify} |")
    return "\n".join(rows)


def capability_index(cat: Catalogue) -> str:
    """Renders the capability index, grouped by domain."""
    layer_names = {layer["id"]: layer["name"] for layer in cat["layers"]}
    out: list[str] = []
    for domain in cat["domains"]:
        out += [
            f"### {domain['name']}",
            "",
            cell(domain["summary"]),
            "",
            "| Capability | Layer | Summary | Clauses |",
            separator(4),
        ]
        for cap in cat["capabilities"]:
            if cap["domain"] != domain["id"]:
                continue
            link = f"[{cap['id']} {cell(cap['name'])}]({cap['id'].lower()}.md)"
            layer = f"{cap['layer']} {layer_names[cap['layer']]}"
            musts = sum(1 for cl in cap["clauses"] if cl["level"] == "MUST")
            clauses = f"{len(cap['clauses'])} ({musts} MUST)"
            out.append(
                f"| {link} | {layer} | {cell(cap['summary'])} | {clauses} |"
            )
        out.append("")
    return "\n".join(out).rstrip()


def components(binding_file: BindingFile, capability_id: str) -> str:
    """Names the components a binding file binds to one capability."""
    for binding in binding_file["bindings"]:
        if binding["capability"] == capability_id:
            return "<br/>".join(cell(c["name"]) for c in binding["components"])
    return "—"


def implementation_matrix(cat: Catalogue, files: list[BindingFile]) -> str:
    """Renders capabilities against implementations, naming components."""
    names = [f["implementation"]["name"] for f in files]
    out = [
        "| Capability | " + " | ".join(names) + " |",
        separator(len(names) + 1),
    ]
    for cap in cat["capabilities"]:
        link = f"[{cap['id']}](../capabilities/{cap['id'].lower()}.md)"
        cells = " | ".join(components(f, cap["id"]) for f in files)
        out.append(f"| {link} {cell(cap['name'])} | {cells} |")
    return "\n".join(out)


def page_implementations(cap: Capability, files: list[BindingFile]) -> str:
    """Renders, for one capability page, what each implementation binds."""
    if not files:
        return "No implementation binds this capability yet."
    rows = ["| Implementation | Components |", separator(2)]
    for f in files:
        name = f["implementation"]["name"]
        link = f"[{name}](../implementations/{name}.yaml)"
        rows.append(f"| {link} | {components(f, cap['id'])} |")
    return "\n".join(rows)


def build_order(cat: Catalogue) -> list[Capability]:
    """Orders capabilities so each comes after everything it depends on.

    Among capabilities that are ready, BUILD_RANK decides (bootstrap, then
    modules, then platform, then products), then catalogue order, so the
    result is deterministic. The catalogue check has already refused cycles.

    Args:
      cat: The catalogue.

    Returns:
      Every capability, dependencies first.
    """
    position = {c["id"]: i for i, c in enumerate(cat["capabilities"])}
    done: set[str] = set()
    ordered: list[Capability] = []
    pending = list(cat["capabilities"])
    while pending:
        ready = min(
            (
                c
                for c in pending
                if all(d in done for d in c.get("depends_on", []))
            ),
            key=lambda c: (BUILD_RANK[c["layer"]], position[c["id"]]),
        )
        ordered.append(ready)
        done.add(ready["id"])
        pending.remove(ready)
    return ordered


def build_order_table(cat: Catalogue) -> str:
    """Renders the build order as a numbered table."""
    rows = ["| Step | Capability | Layer | Depends on |", separator(4)]
    for step, cap in enumerate(build_order(cat), 1):
        link = f"[{cap['id']}](capabilities/{cap['id'].lower()}.md)"
        deps = ", ".join(cap.get("depends_on", [])) or "—"
        rows.append(
            f"| {step} | {link} {cell(cap['name'])} | {cap['layer']} | {deps} |"
        )
    return "\n".join(rows)


def reference_bindings() -> list[BindingFile]:
    """Loads the reference binding files that pass their schema."""
    files: list[BindingFile] = []
    for path in sorted(IMPLEMENTATION_DOCS.glob("*.yaml")):
        doc, _ = load_binding(path)
        if doc is not None:
            files.append(doc)
    return files


def render(cat: Catalogue, *, write: bool) -> list[pathlib.Path]:
    """Regenerates every generated block; returns the paths that changed."""
    changed: list[pathlib.Path] = []

    def update(path: pathlib.Path, name: str, body: str) -> None:
        old = path.read_text(encoding="utf-8")
        new = replace_generated(old, name, body)
        if new != old:
            changed.append(path.relative_to(ROOT))
            if write:
                path.write_text(new, encoding="utf-8")

    files = reference_bindings()
    for cap in cat["capabilities"]:
        page = page_path(cap["id"])
        if page.exists():
            update(page, "contract", contract_table(cap))
            update(page, "implementations", page_implementations(cap, files))
    update(CAPABILITY_DOCS / "README.md", "index", capability_index(cat))
    update(BUILDING_GUIDE, "order", build_order_table(cat))
    if files:
        update(
            IMPLEMENTATION_DOCS / "README.md",
            "matrix",
            implementation_matrix(cat, files),
        )
    return changed


def main() -> int:
    """Runs one subcommand and returns the process exit code."""
    parser = argparse.ArgumentParser(description="Blueprint catalogue tool.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("render")
    sub.add_parser("binding").add_argument(
        "files", nargs="+", type=pathlib.Path
    )
    args = parser.parse_args()
    command = cast("str", args.command)

    raw = load_yaml(CATALOGUE)
    errors = schema_errors(raw, "catalogue.schema.json")
    if errors:
        print("\n".join(f"catalogue: {e}" for e in errors))
        return 1
    cat = cast("Catalogue", raw)

    if command == "render":
        for path in render(cat, write=True):
            print(f"rendered {path}")
        return 0

    if command == "binding":
        problems: list[str] = []
        for f in cast("list[pathlib.Path]", args.files):
            found, summary = binding_problems(f, cat)
            problems += found
            print(summary)
        print("\n".join(problems))
        return 1 if problems else 0

    problems = check_catalogue(cat) + check_references(cat)
    for path in sorted(IMPLEMENTATION_DOCS.glob("*.yaml")):
        problems += binding_problems(path, cat)[0]
    problems += [
        f"{p}: generated section is stale; run `just render`"
        for p in render(cat, write=False)
    ]
    if problems:
        print("\n".join(problems))
        return 1
    clauses = sum(len(c["clauses"]) for c in cat["capabilities"])
    print(
        f"blueprint {cat['version']}: {len(cat['capabilities'])} capabilities,"
        f" {clauses} clauses, consistent"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
