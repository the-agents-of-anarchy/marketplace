"""fill-setup.py: write one server's setup file from this skill's cloud-init template.

The template's SSH_PUBLIC_KEY_PLACEHOLDER becomes the public half of ~/.ssh/estafette_lab.

usage: python3 -I fill-setup.py <output path>
"""
import pathlib
import sys

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(2)
here = pathlib.Path(__file__).resolve().parent
key = (pathlib.Path.home() / ".ssh" / "estafette_lab.pub").read_text().strip()
text = (here / "cloud-init.template.yaml").read_text()
assert text.count("SSH_PUBLIC_KEY_PLACEHOLDER") == 1
pathlib.Path(sys.argv[1]).write_text(text.replace("SSH_PUBLIC_KEY_PLACEHOLDER", key))
print("written", sys.argv[1])
