"""Build every page embed into out/, applying folder URLs and the active nav state.

Usage: python -I _shared/build_all.py [services_folder] [articles_folder]
Pass "-" for a folder to keep those pages at the site root.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SH = ROOT / "_shared"

SERVICES = ["finance-accounting-recruitment", "cfo-executive-search", "gcc-hiring",
            "analytics-data-recruitment", "ai-ml-recruitment", "diversity-hiring"]
ARTICLES = ["recruitment-agency-fees-india", "gcc-hiring-guide-india",
            "cfo-hiring-process", "retained-vs-contingency-search"]
OTHER = ["women-returnship", "how-we-work", "about", "contact", "insights", "jobs"]

svc_folder = sys.argv[1] if len(sys.argv) > 1 else "-"
art_folder = sys.argv[2] if len(sys.argv) > 2 else "-"

PATHS = {s: (f"/{svc_folder}/{s}" if svc_folder != "-" else f"/{s}") for s in SERVICES}
PATHS.update({a: (f"/{art_folder}/{a}" if art_folder != "-" else f"/{a}") for a in ARTICLES})

# Which top-level nav link is "current" for each page
NAV_CURRENT = {"how-we-work": "/how-we-work", "about": "/about", "insights": "/insights", "jobs": "/jobs"}
NAV_CURRENT.update({a: "/insights" for a in ARTICLES})


def rewrite(html):
    for slug, path in PATHS.items():
        html = re.sub(rf'href="/{re.escape(slug)}(?=["#?])', f'href="{path}', html)
        html = re.sub(rf'https://www\.stellaspire\.com/{re.escape(slug)}(?=["#?/]|\\")',
                      f"https://www.stellaspire.com{path}", html)
    return html


def mark_current(html, slug):
    target = NAV_CURRENT.get(slug)
    if target:
        html = html.replace(f'<a class="nav-link" href="{target}">',
                            f'<a class="nav-link" href="{target}" aria-current="page">', 1)
    return html


for slug in SERVICES + ARTICLES + OTHER:
    out = ROOT / "out" / f"{slug}.html"
    subprocess.run([sys.executable, "-I", str(SH / "build.py"), str(ROOT / f"{slug}.body.html"), str(out)],
                   check=True, stdout=subprocess.DEVNULL)
    s = out.read_text(encoding="utf-8")
    s = mark_current(rewrite(s), slug)
    out.write_text(s, encoding="utf-8")

subprocess.run([sys.executable, "-I", str(SH / "update_home.py")], check=True, stdout=subprocess.DEVNULL)
home = ROOT / "out" / "home-page.html"
home.write_text(rewrite(home.read_text(encoding="utf-8")).replace(
    '<a class="textlink" href="https://recruitcrm.io/jobs/Stellaspire" target="_blank" rel="noopener noreferrer">View Active Opportunities <span aria-hidden="true">↗</span><span class="sr-only">(opens in a new tab)</span></a>',
    '<a class="textlink" href="/jobs">View open roles <span aria-hidden="true">→</span></a>').replace(
    "Talent Pool and Active Opportunities open Recruit CRM in a new tab.",
    "The talent pool form opens Recruit CRM in a new tab."), encoding="utf-8")

# the global, country and India-city pages (they go through enhance too)
subprocess.run([sys.executable, "-I", str(SH / "build_geo.py")], check=True, stdout=subprocess.DEVNULL)

# v6: motion hero on home + founder reels on every page except Contact
sys.path.insert(0, str(SH))
from enhance import enhance  # noqa: E402
for p in (ROOT / "out").glob("*.html"):
    p.write_text(rewrite(enhance(p.stem, p.read_text(encoding="utf-8"))), encoding="utf-8")
subprocess.run([sys.executable, "-I", str(SH / "build_assets.py")], check=True)


# House style: no em or en dashes anywhere in the published copy. Fail loudly
# rather than letting one slip into a page nobody re-reads.
DASHES = {"—": "em dash", "–": "en dash", "&mdash;": "&mdash;", "&ndash;": "&ndash;"}
bad = []
for p in sorted((ROOT / "out").glob("*.html")):
    s = p.read_text(encoding="utf-8")
    for ch, name in DASHES.items():
        if ch in s:
            i = s.index(ch)
            bad.append(f"{p.name}: {name} in ...{s[max(0, i - 60):i + 60]}...")
if bad:
    raise SystemExit("Dashes found in built pages:\n" + "\n".join(bad))

for p in sorted((ROOT / "out").glob("*.html")):
    print(f"{p.name:40} {len(p.read_text(encoding='utf-8')):6}")
print("paths:", PATHS)
