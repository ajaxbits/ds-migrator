#!/bin/bash

sh <(curl -L https://github.com/numtide/nix-flakes-installer/releases/download/nix-3.0pre20200804_ed52cf6/install)
. $(eval echo ~$USER)/.nix-profile/etc/profile.d/nix.sh
mkdir -p ~/.config/nix

echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
