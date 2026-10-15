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
    shfmt --find . | xargs --no-run-if-empty shellcheck
    statix check .
    deadnix --fail .

# Check that every link inside the repository resolves (no network).
links:
    lychee "**/*.md"

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
check: fmt-check lint links
