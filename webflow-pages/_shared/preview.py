"""Wrap an assembled embed in a full HTML document for local preview."""
import sys
from pathlib import Path
here = Path(__file__).resolve().parent
src = Path(sys.argv[1]); out = Path(sys.argv[2])
head = (here / "head-link.html").read_text(encoding="utf-8")
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       + head + '</head><body>' + src.read_text(encoding="utf-8")
       + '<script src="../_shared/stellaspire-pages-v6.js"></script></body></html>')
out.write_text(doc, encoding="utf-8")
