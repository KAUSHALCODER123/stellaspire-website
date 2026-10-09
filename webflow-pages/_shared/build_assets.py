"""Bundle the shared stylesheet and script for upload to Webflow Assets.

stellaspire-pages-v6.css = home.css + extra.css + motion.css (minified)
stellaspire-pages-v6.js  = stellaspire-pages-v2.js + motion.js
"""
import re
from pathlib import Path

SH = Path(__file__).resolve().parent


def minify(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


css = minify("\n".join((SH / f).read_text(encoding="utf-8") for f in ("home.css", "extra.css", "motion.css", "hero-live.css", "hv.css", "blog.css", "brand.css")))
(SH / "stellaspire-pages-v6.css").write_text(css, encoding="utf-8")
js = "\n\n".join((SH / f).read_text(encoding="utf-8").rstrip()
                 for f in ("stellaspire-pages-v2.js", "motion.js", "hero-live.js", "blog.js")) + "\n"
(SH / "stellaspire-pages-v6.js").write_text(js, encoding="utf-8")
print("css", len(css), "js", len(js))
