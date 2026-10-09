"""Rewrite repeated, template-sounding copy on the inner pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

METHOD = {
    "ai-ml-recruitment": "AI hires who have shipped to production.",
    "analytics-data-recruitment": "Good analysts can explain the numbers.",
    "cfo-executive-search": "Confidential searches, run by one person from start to finish.",
    "diversity-hiring": "A wider search, with the same bar for everyone.",
    "finance-accounting-recruitment": "Finance hires judged on the work they have done.",
    "gcc-hiring": "People who can work with the parent company and build the India team.",
    "how-we-work": "Most searches stall at the brief, so that is where we start.",
    "women-returnship": "Matching returners with employers who want them.",
}

FAQ = {
    "ai-ml-recruitment": "AI hiring questions.",
    "analytics-data-recruitment": "Data hiring questions.",
    "cfo-executive-search": "CFO search questions.",
    "diversity-hiring": "Diversity hiring questions.",
    "finance-accounting-recruitment": "Finance hiring questions.",
    "gcc-hiring": "GCC hiring questions.",
    "how-we-work": "Questions about working with us.",
    "contact": "Before you get in touch.",
}

PHRASES = [
    ("For teams that need insight, not just dashboards.", "For teams that need answers from their data."),
    ("technical finance capability, not only screen CVs", "technical finance skills properly"),
    ("Why a finance specialist, not a generalist agency?", "Why use a finance specialist?"),
    ("the capability to build teams, not only on technical skill", "the capability to build teams, as well as technical skill"),
    ("Capability, not only cost.", "Capability as well as cost."),
    ("based on the talent you need, not only on cost", "based on the talent you need as well as cost"),
    ("build teams, not only manage delivery", "build teams as well as manage delivery"),
    ("Production experience, not only research,", "Production experience as well as research,"),
    ("informal conversations, not only formal interviews", "informal conversations as well as formal interviews"),
    ("Building a GCC team in India? Let’s map it together.", "Planning a GCC team in India? Talk to us."),
]

for p in sorted(ROOT.glob("*.body.html")):
    slug = p.name[: -len(".body.html")]
    s = p.read_text(encoding="utf-8")
    before = s
    if slug in METHOD:
        s, n = re.subn(r'(<h2[^>]*class="method-heading"[^>]*>).*?(</h2>)',
                       lambda m: f"{m.group(1)}<span>{METHOD[slug]}</span>{m.group(2)}", s, count=1, flags=re.S)
        assert n == 1, slug
    if slug in FAQ:
        s, n = re.subn(r'(<h2[^>]*class="h2"[^>]*>)Before<br>we begin\.(</h2>)', rf"\g<1>{FAQ[slug]}\g<2>", s)
        assert n == 1, (slug, "faq")
    for old, new in PHRASES:
        s = s.replace(old, new)
    if s != before:
        p.write_text(s, encoding="utf-8")
        print("updated", slug)
