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
        buildInputs = with pkgs; [ env pkgs.poetry pre-commit ];
        shellHook = ''
          mkdir -p .vim
          echo '{"python.pythonPath": "${env}/bin/python", "python.formatting.provider": "black", "python.formatting.blackPath": "${env}/bin/black", "coc.preferences.formatOnSaveFiletypes":["python"]}' > .vim/coc-settings.json
          pre-commit install -f --hook-type pre-commit --allow-missing-config
        '';
      };
    };
}
