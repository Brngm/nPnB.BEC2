{ pkgs ? import <nixpkgs> {} }:

with pkgs;

stdenv.mkDerivation rec {
  pname = "nPnB-QUICK-BEC";
  version = "0.1";
  src = ./.;
  buildInputs = [ cmake ];
  installPhase = ''
    mkdir -p $out/bin
    mv "libnPnB-QUICK-BEC.so" $out/bin/
  '';
}
