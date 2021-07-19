{
  description = "my project description";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        dsmigrator-env = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          python = pkgs.python38;
        };
      in {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            poetry
            dsmigrator-env
            python38Packages.pylint
            python38Packages.black
            python38Packages.nose2
            python38Packages.rope
            pre-commit
          ];
          shellHook = ''
            mkdir -p .vim
            echo '{"python.pythonPath": "${dsmigrator-env}/bin/python", "python.formatting.provider": "black", "coc.preferences.formatOnSaveFiletypes":["python"]}' > .vim/coc-settings.json
            pre-commit install -f --hook-type pre-commit --allow-missing-config
          '';
        };
      });
}
