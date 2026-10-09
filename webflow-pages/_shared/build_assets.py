"""Bundle the shared stylesheet and script for upload to Webflow Assets.

stellaspire-site.css    = site.src.css (design system) + motion.css + hero-live.css + hv.css + blog.css, minified
stellaspire-pages-v6.js = stellaspire-pages-v2.js + motion.js + hero-live.js + blog.js

Order matters: site.src.css sets the tokens, type and layout; the modules after it
own their own components (motion/reels, home hero, hero panels, articles).
"""
import re
from pathlib import Path

SH = Path(__file__).resolve().parent

CSS_PARTS = ("site.src.css", "motion.css", "hero-live.css", "hv.css", "blog.css")
JS_PARTS = ("stellaspire-pages-v2.js", "motion.js", "hero-live.js", "blog.js")


def minify(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


css = minify("\n".join((SH / f).read_text(encoding="utf-8") for f in CSS_PARTS))
(SH / "stellaspire-site.css").write_text(css, encoding="utf-8")
js = "\n\n".join((SH / f).read_text(encoding="utf-8").rstrip() for f in JS_PARTS) + "\n"
(SH / "stellaspire-pages-v6.js").write_text(js, encoding="utf-8")
print("stellaspire-site.css", len(css), "chars; stellaspire-pages-v6.js", len(js), "chars")
