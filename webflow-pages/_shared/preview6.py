"""Write preview6/<slug>.html: each built embed wrapped with the local v6 CSS/JS and Montserrat, for browser checks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "preview6"
OUT.mkdir(exist_ok=True)
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400&family=Montserrat:wght@400;500;600;700&display=swap">')
for p in sorted((ROOT / "out").glob("*.html")):
    doc = ('<!doctype html><html lang="en" class="w-mod-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{p.stem}</title>{FONT}<link rel="stylesheet" href="../_shared/stellaspire-pages-v6.css"></head><body>'
           + p.read_text(encoding="utf-8") + '<script src="../_shared/stellaspire-pages-v6.js"></script></body></html>')
    (OUT / p.name).write_text(doc, encoding="utf-8")
print("ok", len(list(OUT.glob("*.html"))))
