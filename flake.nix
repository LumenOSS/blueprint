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
        # Checks: what every change must pass. Small, so CI caches it cheaply.
        default = pkgs.mkShell {
          packages = with pkgs; [
            just
            jq
            (python3.withPackages (ps: [
              ps.pyyaml
              ps.jsonschema
            ]))
            markdownlint-cli2
            yamllint
            lychee
            shellcheck
            nixfmt-rfc-style
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

      formatter = forAllSystems (pkgs: pkgs.nixfmt-rfc-style);
    };
}
