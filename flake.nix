{
  description = "Lightweight typing speed commandline tool";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;

        typetest-cli = python.pkgs.buildPythonApplication {
          pname = "typetest-cli";
          version = "1.2.4";
          pyproject = true;

          src = ./.;

          build-system = [python.pkgs.setuptools];

          dependencies = [python.pkgs.rich];

          pythonImportsCheck = ["typetest_cli"];
        };
      in {
        packages = {
          default = typetest-cli;
          typetest-cli = typetest-cli;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            (python.withPackages (ps:
              with ps; [
                rich
                setuptools
                twine
                build
              ]))
          ];
        };
      }
    );
}
