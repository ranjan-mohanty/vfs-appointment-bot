
with import <nixpkgs> {};
{
     pythonEnv = stdenv.mkDerivation {
       name = "python-env";
       buildInputs = [
         (python39.withPackages (ps: [ps.numpy ps.twilio ps.selenium]))
         ];
     };
}
