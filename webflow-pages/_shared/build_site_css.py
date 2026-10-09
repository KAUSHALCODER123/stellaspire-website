"""Bundle the one site stylesheet for upload to Webflow Assets.

site.src.css is the design system. hero-live.css (home motion hero) and
hv.css (page visual panels) are self-contained modules kept as-is.
Output: stellaspire-site.css, minified.

Usage: python -I _shared/build_site_css.py
"""
import re
from pathlib import Path

SH = Path(__file__).resolve().parent


def minify(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


parts = [(SH / f).read_text(encoding="utf-8") for f in ("site.src.css", "hero-live.css", "hv.css")]
css = minify("\n".join(parts))
(SH / "stellaspire-site.css").write_text(css, encoding="utf-8")
print("stellaspire-site.css", len(css), "chars")
