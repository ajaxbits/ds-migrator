{
  description = "my project description";

  inputs = {
    unstable.url = "github:NixOS/nixpkgs/nixos-unstable";
    stable.url = "github:NixOS/nixpkgs/nixos-20.09";
  };

  outputs = inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.unstable.legacyPackages.${system};
      env = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ./.;
        python = pkgs.python37;
      };
    in {
      devShell."${system}" = pkgs.mkShell {
        buildInputs = [env pkgs.poetry];
        shellHook = ''
          mkdir -p .vim
          echo '{"python.pythonPath": "${env}/bin/python", "python.formatting.provider": "black", "python.formatting.blackPath": "${env}/bin/black", "coc.preferences.formatOnSaveFiletypes":["python"]}' > .vim/coc-settings.json
        '';
      };
    };
}
