{
  description = "data-platform-blueprint: one toolchain for every task, on every platform";

  # nixpkgs-unstable, pinned by flake.lock, so a laptop and CI resolve the
  # same store paths. Bump deliberately with `nix flake update`, in its own
  # change. Everything here is in the public binary cache.
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      # Windows runs this under WSL, which is x86_64-linux or aarch64-linux.
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (pkgs: {
        # Every file type has a formatter, a linter and a language server,
        # and every rule lives in that tool's config file at the repository
        # root. Formatting is the tool's job, never a hand edit: `just fmt`
        # fixes, `just check` verifies. Editors pick the servers up from
        # this shell (e.g. via direnv).
        default = pkgs.mkShell {
          packages = with pkgs; [
            just
            # Python: ruff formats and lints (ruff.toml), pyright type-checks
            # and serves the editor (pyrightconfig.json).
            (python3.withPackages (ps: [
              ps.pyyaml
              ps.jsonschema
              ps.types-pyyaml
              ps.types-jsonschema
            ]))
            ruff
            pyright
            # Markdown: markdownlint-cli2 lints and fixes
            # (.markdownlint-cli2.yaml); marksman serves the editor; lychee
            # checks links offline.
            markdownlint-cli2
            marksman
            lychee
            # YAML: yamlfmt formats (.yamlfmt.yaml), yamllint lints
            # (.yamllint.yaml), yaml-language-server validates against the
            # schemas named in each file's modeline.
            yamlfmt
            yamllint
            yaml-language-server
            # JSON: biome formats and lints (biome.json); check-jsonschema
            # validates the schemas against their metaschema.
            biome
            check-jsonschema
            # Shell: shfmt formats (.editorconfig), shellcheck lints
            # (.shellcheckrc), bash-language-server serves the editor.
            shfmt
            shellcheck
            bash-language-server
            # GitHub Actions: actionlint checks workflow files.
            actionlint
            # Nix: nixfmt formats, statix and deadnix lint, nil serves the
            # editor.
            nixfmt
            statix
            deadnix
            nil
          ];
        };

        # Website: Hugo builds the documentation site; Go fetches the theme
        # as a Hugo module. Only the site build needs them.
        site = pkgs.mkShell {
          packages = with pkgs; [
            just
            hugo
            go
            git
            python3
          ];
        };

        # Diagrams: rendering Mermaid pulls in a headless browser, which no
        # check needs, so it lives in its own shell.
        diagrams = pkgs.mkShell {
          packages = with pkgs; [
            just
            mermaid-cli
          ];
        };
      });

      formatter = forAllSystems (pkgs: pkgs.nixfmt);
    };
}
