# Every task in this repository is a recipe here, run inside the nix shell:
#
#   nix develop --command just <recipe>
#
# Any CI runs the same recipes the same way. `just --list` is the index.
# Formatting and linting are done by the tools below, configured in their
# own files at the repository root; never by hand.

set shell := ["bash", "-euo", "pipefail", "-c"]

# List the recipes.
default:
    @just --list

# Format everything in place.
fmt:
    just --fmt --unstable
    ruff format .
    ruff check --fix .
    markdownlint-cli2 --fix "**/*.md"
    yamlfmt .
    biome format --write .
    shfmt --find . | xargs --no-run-if-empty shfmt --write
    nixfmt flake.nix

# Fail if anything is not formatted.
fmt-check:
    just --fmt --check --unstable
    ruff format --check .
    yamlfmt -lint .
    biome format .
    shfmt --find . | xargs --no-run-if-empty shfmt --diff
    nixfmt --check flake.nix

# Run every linter and the type checker.
lint:
    ruff check .
    pyright
    markdownlint-cli2 "**/*.md"
    yamllint --strict .
    biome lint .
    check-jsonschema --check-metaschema schema/*.json
    shfmt --find . | xargs --no-run-if-empty shellcheck
    actionlint
    statix check .
    deadnix --fail .

# Check that every link inside the repository resolves (no network).
links:
    lychee "**/*.md"

# Validate the catalogue, the capability pages and the reference bindings.
blueprint:
    python3 scripts/blueprint.py check

# Regenerate the generated sections (contract tables, index, matrix).
render:
    python3 scripts/blueprint.py render

# Validate implementation binding files and report their coverage.
binding +files:
    python3 scripts/blueprint.py binding {{ files }}

# Build the documentation website into build/site/public.
# Run in the site shell: nix develop .#site --command just site
site base_url="https://lumenoss.github.io/data-platform-blueprint/":
    python3 scripts/site.py build/site/content
    hugo build --source site --contentDir ../build/site/content --destination ../build/site/public --baseURL "{{ base_url }}" --minify --cleanDestinationDir

# Serve the documentation website locally with live reload.
site-serve:
    python3 scripts/site.py build/site/content
    hugo server --source site --contentDir ../build/site/content --baseURL "http://localhost:1313/"

# Render every Mermaid diagram to build/ as PNG, to look at before committing.
# Run in the diagrams shell: nix develop .#diagrams --command just diagrams
diagrams:
    #!/usr/bin/env bash
    set -euo pipefail
    find docs -name '*.md' -print0 | while IFS= read -r -d '' f; do
      grep -q '^```mermaid' "$f" || continue
      out="build/${f%.md}"
      mkdir -p "$(dirname "$out")"
      mmdc --quiet -e png -s 2 -i "$f" -o "$out.md"
    done
    echo "rendered into build/"

# Everything a change must pass.
check: fmt-check lint blueprint links
