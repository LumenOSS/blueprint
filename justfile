# Every task in this repository is a recipe here, run inside the nix shell:
#
#   nix develop --command just <recipe>
#
# Any CI runs the same recipes the same way. `just --list` is the index.

set shell := ["bash", "-euo", "pipefail", "-c"]

# List the recipes.
default:
    @just --list

# Lint the Markdown.
lint-md:
    markdownlint-cli2 "**/*.md"

# Lint the YAML.
lint-yaml:
    yamllint --strict .

# Check that every link inside the repository resolves (no network).
links:
    lychee --offline --no-progress --include-fragments "**/*.md"

# Lint the shell scripts, if any.
lint-sh:
    #!/usr/bin/env bash
    set -euo pipefail
    shopt -s nullglob
    scripts=(scripts/*.sh)
    if (( ${#scripts[@]} )); then shellcheck "${scripts[@]}"; fi

# Fail if the Nix files are not formatted.
fmt-check:
    nixfmt --check flake.nix

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
check: fmt-check lint-md lint-yaml links lint-sh
