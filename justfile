# Every task in this repository is a recipe here, run inside the nix shell:
#
#   nix develop --command just <recipe>
#
# Any CI runs the same recipes the same way. `just --list` is the index.
# Formatting and linting are done by the tools below, configured in their
# own files at the repository root; never by hand.

# The site configuration plus the per-language configuration the build writes.
hugo_config := justfile_directory() / "site/hugo.toml" + "," + justfile_directory() / "build/site/languages.toml"

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
    taplo fmt
    # Formatting can change translated pages, so their templates follow.
    python3 scripts/l10n.py update

# Fail if anything is not formatted.
fmt-check:
    just --fmt --check --unstable
    ruff format --check .
    yamlfmt -lint .
    biome format .
    shfmt --find . | xargs --no-run-if-empty shfmt --diff
    nixfmt --check flake.nix
    taplo fmt --check

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
    taplo lint

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
site base_url="https://lumenoss.github.io/blueprint/": site-icons (site-content base_url)
    hugo build --source site --config "{{ hugo_config }}" --destination ../build/site/public --baseURL "{{ base_url }}" --minify --cleanDestinationDir

# Stage every language's pages and the Hugo language configuration.
[private]
site-content base_url:
    python3 scripts/l10n.py build build/l10n/pages
    python3 scripts/site.py build/site --base-url "{{ base_url }}" --translations build/l10n/pages

# Render the favicons from the logo into site/static (gitignored).
site-icons:
    #!/usr/bin/env bash
    set -euo pipefail
    out=site/static
    mkdir -p "$out"
    logo=site/assets/img/lumenoss.svg
    for size in 16 32; do resvg -w "$size" -h "$size" "$logo" "$out/favicon-${size}x${size}.png"; done
    resvg -w 180 -h 180 "$logo" "$out/apple-touch-icon.png"
    for size in 192 512; do resvg -w "$size" -h "$size" "$logo" "$out/android-chrome-${size}x${size}.png"; done
    magick "$out/favicon-16x16.png" "$out/favicon-32x32.png" "$out/favicon.ico"

# Serve the documentation website locally with live reload.
site-serve: site-icons (site-content "http://localhost:1313/")
    hugo server --source site --config "{{ hugo_config }}" --baseURL "http://localhost:1313/"

# Regenerate the translation templates and merge them into every
# language's PO files. Run after changing any translated page.
l10n-update:
    python3 scripts/l10n.py update

# Show how much of each language is translated.
l10n-status:
    python3 scripts/l10n.py status

# Fail if translation templates or PO files are stale or invalid.
l10n:
    python3 scripts/l10n.py check

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
check: fmt-check lint blueprint l10n links
