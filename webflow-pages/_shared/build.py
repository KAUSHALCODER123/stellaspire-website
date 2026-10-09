"""Assemble a page embed: header + <main> body + footer.

Usage: python -I build.py <body.html> <out.html>
The body file holds everything that goes inside <main id="main-content">.
Prints the character count so it can be checked against Webflow's embed limit.
"""
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
body = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
html = (
    (here / "header.html").read_text(encoding="utf-8").strip()
    + '\n\n<main id="main-content">\n'
    + body
    + "\n</main>\n"
    + (here / "footer.html").read_text(encoding="utf-8").rstrip()
)
Path(sys.argv[2]).write_text(html, encoding="utf-8")
print(len(html), "chars")
