"""v6 enhancements, applied to the built embeds in out/ (run by build_all.py after the normal build).

- Home: the full-screen motion-graphic hero (animated SP mark, aurora, floating service links, watch button).
- Every page except Contact: a "From our founder" reels section with VideoObject structured data.

Video and poster URLs come from MEDIA (filled in after upload to Webflow Assets).
Before the upload, they point at ../assets/video/ so the local preview works.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SH = ROOT / "_shared"
MEDIA_FILE = SH / "media-urls.json"
MEDIA = json.loads(MEDIA_FILE.read_text(encoding="utf-8")) if MEDIA_FILE.exists() else {}


def url(name):
    return MEDIA.get(name, f"../assets/video/{name}")


VIDEOS = {
    "why": dict(file="stellaspire-why-hire-a-consultant", secs=23, tag="For employers",
                title="Why growing companies bring in a recruitment partner",
                copy="Hiring under investor pressure with a small team? Nikita on when a specialist partner saves you time."),
    "check": dict(file="stellaspire-background-check", secs=35, tag="For employers",
                  title="How we check a candidate before you meet them",
                  copy="Background, motivation and fit: what we verify before a profile reaches your inbox."),
    "resume": dict(file="stellaspire-resume-tips", secs=35, tag="For candidates",
                   title="Is your resume good enough? Quick checks",
                   copy="Spelling slips, match scores and the small fixes that get you the interview call."),
    "jd": dict(file="stellaspire-job-description-tips", secs=36, tag="For candidates",
               title="Read the job description before you apply",
               copy="How to read a JD, reach out to the right people and prepare for the industry."),
}

EMPLOYER = ["why", "check"]
CANDIDATE = ["resume", "jd"]
ALL = EMPLOYER + CANDIDATE

# slug -> (videos, heading, intro, insert-before marker)
PAGES = {
    "gcc-hiring": (EMPLOYER, None, None, '<section class="candidates"'),
    "finance-accounting-recruitment": (EMPLOYER, None, None, '<section class="candidates"'),
    "cfo-executive-search": (EMPLOYER, None, None, '<section class="candidates"'),
    "analytics-data-recruitment": (EMPLOYER, None, None, '<section class="candidates"'),
    "ai-ml-recruitment": (EMPLOYER, None, None, '<section class="candidates"'),
    "diversity-hiring": (EMPLOYER, None, None, '<section class="candidates"'),
    "how-we-work": (EMPLOYER, None, None, '<section class="candidates"'),
    "about": (EMPLOYER, None, None, '<section class="partners"'),
    "women-returnship": (CANDIDATE, "Career advice from our founder.",
                         "Short, practical videos for returners and job seekers, in Hindi and English.", '<section class="candidates"'),
    "insights": (ALL, "Watch: hiring advice in under a minute.",
                 "Quick takes from Nikita for employers and candidates, in Hindi and English.", '<section class="candidates"'),
    "recruitment-agency-fees-india": (EMPLOYER, None, None, '</main>'),
    "gcc-hiring-guide-india": (EMPLOYER, None, None, '</main>'),
    "cfo-hiring-process": (EMPLOYER, None, None, '</main>'),
    "retained-vs-contingency-search": (EMPLOYER, None, None, '</main>'),
    "home-page": (ALL, "Hear it from our founder.",
                  "Under a minute each: how we hire for companies, and how candidates can stand out. In Hindi and English.",
                  '<section id="partners"'),
}
# The geo pages (built by build_geo.py) all take the employer reels, placed
# just before the closing CTA band.
try:
    import geo as _geo
    _GEO = (["geo-global", "geo-global-hire-talent-india", "geo-india"]
            + [f"geo-{k}" for k in _geo.COUNTRIES]
            + [f"geo-{k}-{s}" for k in _geo.COUNTRIES for s in _geo.COUNTRY_SERVICES[k]]
            + [f"geo-city-{k}" for k in _geo.CITIES])
    PAGES.update({s: (EMPLOYER, None, None, '</main>') for s in _GEO})  # GEO PAGES
except ImportError:  # geo.py missing: the other pages still build
    pass


DEFAULT_H = "Hear it from our founder."
DEFAULT_I = "Nikita Agrawal on how we hire, in under a minute. In Hindi and English."


CTA_EMPLOYER = """        <aside class="reel-cta">
          <p class="eyebrow eyebrow--light">Hiring now?</p>
          <p class="reel-cta-title">Tell us about the role and Nikita will take it from there.</p>
          <a class="button" href="/contact">Start a hiring conversation</a>
          <a class="light-link" href="/how-we-work">How we run a search <span aria-hidden="true">→</span></a>
        </aside>"""
CTA_CANDIDATE = """        <aside class="reel-cta">
          <p class="eyebrow eyebrow--light">Looking for your next role?</p>
          <p class="reel-cta-title">See the roles we are hiring for right now.</p>
          <a class="button" href="/jobs">See open roles <span aria-hidden="true">→</span></a>
          <a class="light-link" href="/women-returnship">Women Returnship <span aria-hidden="true">→</span></a>
        </aside>"""


def reel_card(key):
    v = VIDEOS[key]
    mp4, jpg = url(v["file"] + ".mp4"), url(v["file"] + ".jpg")
    return f"""        <article class="reel-card">
          <button class="reel" type="button" data-video="{mp4}" data-title="{v['title']}" aria-label="Play video ({v['secs']} seconds): {v['title']}">
            <img src="{jpg}" alt="" width="540" height="960" loading="lazy" decoding="async">
            <span class="reel-shade"></span>
            <span class="reel-play" aria-hidden="true"></span>
            <span class="reel-meta" aria-hidden="true"><span class="reel-tag">{v['tag']}</span><span>0:{v['secs']:02d}</span></span>
          </button>
          <h3 class="reel-title">{v['title']}</h3>
          <p class="reel-copy">{v['copy']}</p>
        </article>"""


def video_ld(keys):
    items = []
    for k in keys:
        v = VIDEOS[k]
        items.append({
            "@type": "VideoObject", "name": v["title"], "description": v["copy"],
            "thumbnailUrl": url(v["file"] + ".jpg"), "contentUrl": url(v["file"] + ".mp4"),
            "uploadDate": "2026-10-08", "duration": f"PT{v['secs']}S", "inLanguage": ["hi", "en"],
            "publisher": {"@type": "Organization", "name": "Stellaspire", "url": "https://www.stellaspire.com/"},
        })
    return '<script type="application/ld+json">' + json.dumps(
        {"@context": "https://schema.org", "@graph": items}, ensure_ascii=False, separators=(",", ":")) + "</script>"


def reels_section(slug, keys, heading, intro):
    heading, intro = heading or DEFAULT_H, intro or DEFAULT_I
    cls = "reel-row" if len(keys) > 2 else "reel-row reel-row--3"
    cards = "\n".join(reel_card(k) for k in keys)
    if len(keys) == 2:
        cards += "\n" + (CTA_EMPLOYER if keys == EMPLOYER else CTA_CANDIDATE)
    return f"""  <!-- ============ FOUNDER REELS (v6) ============ -->
  <section class="section reels band-line" aria-labelledby="reels-heading">
    <div class="container">
      <div class="section-top">
        <div>
          <p class="eyebrow">From our founder</p>
          <h2 id="reels-heading" class="h2">{heading}</h2>
        </div>
        <p class="section-intro">{intro}</p>
      </div>
      <div class="{cls}">
{cards}
      </div>
    </div>
    {video_ld(keys)}
  </section>

"""


def hero_html():
    why = VIDEOS["why"]
    mark = MEDIA.get("stellaspire-logo-s.webp", "../assets/stellaspire-logo-s.webp")
    return f"""<!-- ============ HERO (v6 motion graphic: a live search) ============ -->
  <section class="hero hero--live" data-stage="1" aria-labelledby="hero-heading">
    <div class="container hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">We take hiring personally.</p>
        <h1 id="hero-heading" class="hero-title">
          <span class="line">Finance, analytics and leadership.</span>
          <span class="line">Hired with care.</span>
        </h1>
        <p class="hero-lead">A women-led recruitment partner for GCCs and growth companies. Selective, hands-on searches, from the first conversation to the right fit.</p>
        <div class="hero-actions">
          <a class="button" href="#hire-talent">Start a hiring conversation <span aria-hidden="true">↗</span></a>
          <button class="hero-watch" type="button" data-open-reel="hero-reel" data-title="{why['title']}"><span class="hero-watch-icon" aria-hidden="true"></span><span>Why companies call us <small>0:{why['secs']} · Short video</small></span></button>
        </div>
      </div>

      <!-- Motion graphic: an illustrative, anonymised search moving from brief to offer. Decorative, so hidden from screen readers. -->
      <div class="hero-scene" aria-hidden="true">
        <div class="scene-3d">
          <div class="ls-card">
            <div class="ls-top"><span class="ls-live"><i></i>Live search</span><span class="ls-count">01 / 03</span></div>
            <p class="ls-role">Chief Financial Officer</p>
            <p class="ls-client">Series C fintech · Bengaluru</p>
            <div class="ls-tags"><span>Finance leadership</span><span>Confidential</span></div>
            <ol class="ls-stages"><li>Brief</li><li>Market map</li><li>Shortlist</li><li>Offer</li></ol>
            <div class="ls-bar"><i></i></div>
            <ul class="ls-rows"></ul>
            <div class="ls-foot"><img src="{mark}" alt="" width="24" height="34"><span><b>Stellaspire</b>Specialist search team</span><span class="ls-balanced">Gender-balanced shortlist</span></div>
          </div>
          <div class="ls-toast"><span class="ls-tick"></span><span><b>Offer accepted</b><small>CFO · Series C fintech</small></span></div>
          <div class="ls-chip ls-chip--a"><span>✓</span> Hand-picked, not keyword-matched</div>
        </div>
      </div>
    </div>

    <dialog id="hero-reel" class="reel-dialog" aria-label="{why['title']}">
      <button class="reel-dialog-close" type="button" aria-label="Close video">×</button>
      <video data-src="{url(why['file'] + '.mp4')}" poster="{url(why['file'] + '.jpg')}" controls playsinline preload="none"></video>
    </dialog>
  </section>"""


CDN = "https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/"
ARTICLES = {
    "recruitment-agency-fees-india": ("Buyer guide", "How Much Does a Recruitment Agency Charge in India?",
                                      CDN + "6ac5e8d79356b0a30badce8c_blog-recruitment-agency-fees-india.jpg"),
    "gcc-hiring-guide-india": ("GCC hiring", "GCC Hiring in India: The Complete 2026 Guide",
                               CDN + "6ac5e8d72a8a316be947258c_blog-gcc-hiring-guide-india.jpg"),
    "cfo-hiring-process": ("Finance leadership", "CFO Hiring Process: A Step-by-Step Guide",
                           CDN + "6ac5e8d8b35fcf2a547929d5_blog-cfo-hiring-process.jpg"),
    "retained-vs-contingency-search": ("Buyer guide", "Retained vs Contingency Executive Search in India",
                                       CDN + "6ac5e8d804edb2f7e2a16b35_blog-retained-vs-contingency-search.jpg"),
}


def share_bar(slug):
    page = f"https://www.stellaspire.com/{slug}"
    title = ARTICLES[slug][1]
    from urllib.parse import quote
    return (f'\n        <div class="share-bar"><span>Share</span>'
            f'<a class="share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url={quote(page, safe="")}" target="_blank" rel="noopener noreferrer">LinkedIn<span class="sr-only"> (opens in a new tab)</span></a>'
            f'<a class="share-btn" href="https://wa.me/?text={quote(title + " " + page, safe="")}" target="_blank" rel="noopener noreferrer">WhatsApp<span class="sr-only"> (opens in a new tab)</span></a>'
            f'<button class="share-btn" type="button" data-share-copy>Copy link</button></div>')


def related_section(slug):
    cards = []
    for other, (eyebrow, title, img) in ARTICLES.items():
        if other == slug:
            continue
        cards.append(f"""        <a class="related-card" href="/{other}">
          <img src="{img}" alt="" width="1600" height="840" loading="lazy" decoding="async">
          <span class="related-body"><span class="eyebrow">{eyebrow}</span><span class="related-title">{title}</span><span class="related-more">Read the guide →</span></span>
        </a>""")
    return f"""  <!-- ============ KEEP READING (v6) ============ -->
  <section class="related" aria-labelledby="related-heading">
    <div class="container">
      <div class="section-top"><h2 id="related-heading" class="h2">Keep reading.</h2><a class="textlink" href="/insights">All insights <span aria-hidden="true">→</span></a></div>
      <div class="related-grid">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

"""


def _div_end(html, start):
    """Index just past the </div> that closes the <div> opening at `start`."""
    depth, i = 0, start
    while True:
        o, c = html.find("<div", i), html.find("</div>", i)
        if o != -1 and o < c:
            depth, i = depth + 1, o + 4
        else:
            depth, i = depth - 1, c + 6
            if depth == 0:
                return i


def hero_visual(slug, html):
    """Put the page's graphic on the right of the hero, as the second column of .page-hero-grid."""
    from hero_visuals import VISUALS
    if slug not in VISUALS or 'class="hv' in html:
        return html
    grid = html.find('<div class="page-hero-grid">')
    if grid < 0:
        return html
    hero_end = html.find("</section>", grid)
    if "photo-hero" in html[grid:hero_end]:  # the page already has a hero photo in the second column
        return html
    col_end = _div_end(html, html.find("<div", grid + 5))
    visual = VISUALS[slug].replace("{{LOGO}}", MEDIA.get("stellaspire-logo-s.webp", "../assets/stellaspire-logo-s.webp"))
    return html[:col_end] + "\n        " + visual + html[col_end:]


# Photo slots (v7): (page, section marker, media file name, alt text). A slot renders only once its image
# has been uploaded and listed in media-urls.json, so pages never show an empty frame.
SLOTS = [
    ("finance-accounting-recruitment", 'aria-labelledby="process-heading"', "slot-finance-process.webp",
     "A finance hiring manager and a candidate discussing a set of accounts across a meeting table"),
    ("cfo-executive-search", 'aria-labelledby="process-heading"', "slot-cfo-process.webp",
     "A senior finance leader in a quiet one-to-one conversation in a boardroom"),
    ("gcc-hiring", 'aria-labelledby="process-heading"', "slot-gcc-process.webp",
     "An India-based team on a video call with colleagues from their global parent company"),
    ("analytics-data-recruitment", 'aria-labelledby="process-heading"', "slot-analytics-process.webp",
     "An analyst walking two colleagues through a dashboard on a large screen"),
    ("ai-ml-recruitment", 'aria-labelledby="process-heading"', "slot-aiml-process.webp",
     "Two machine learning engineers reviewing model results together at a desk"),
    ("diversity-hiring", 'aria-labelledby="process-heading"', "slot-diversity-process.webp",
     "A diverse interview panel listening to a woman candidate in a bright meeting room"),
    ("how-we-work", 'id="method"', "slot-how-we-work.webp",
     "A recruiter and a hiring manager mapping a search plan on a whiteboard"),
    ("women-returnship", 'aria-labelledby="returners-heading"', "slot-returnship.webp",
     "An experienced woman professional in a friendly first-week conversation with a colleague"),
    ("home-page", 'id="approach"', "slot-home-approach.webp",
     "A recruiter in a one-to-one conversation with a candidate over coffee in a bright office"),
    ("about", 'id="founder"', "slot-about.webp",
     "A small women-led recruitment team working together around a table in a Bengaluru office"),
]


def photo_slots(slug, html):
    """Put each slot photo in a full-width band after its section, not inside the two-column grid."""
    for page, marker, name, alt in SLOTS:
        local = ROOT / "assets" / "slots" / name
        if page != slug or f'data-slot="{name}"' in html or not (name in MEDIA or local.exists()):
            continue
        src = MEDIA.get(name, f"../assets/slots/{name}")
        s = html.find(marker)
        if s < 0:
            continue
        end = html.find("</section>", s)
        if end < 0:
            continue
        end += len("</section>")
        band = (f'\n\n  <div class="container photo-band">\n    <figure class="photo photo-slot photo-wide" data-slot="{name}">'
                f'<img src="{src}" alt="{alt}" width="1200" height="500" loading="lazy" decoding="async"></figure>\n  </div>')
        html = html[:end] + band + html[end:]
    return html


def enhance(slug, html):
    html = hero_visual(slug, html)
    html = photo_slots(slug, html)
    if slug in ARTICLES and "share-bar" not in html:
        meta = html.find('class="article-meta"')
        tag = "div" if html.rfind("<div", 0, meta) > html.rfind("<p", 0, meta) else "p"
        m = html.find(f"</{tag}>", meta) + len(f"</{tag}>")
        html = html[:m] + share_bar(slug) + html[m:]
        k = html.find('</main>')
        html = html[:k] + related_section(slug).lstrip() + "  " + html[k:]
    html = html.replace("{{MARK}}", MEDIA.get("stellaspire-logo-s.webp", "../assets/stellaspire-logo-s.webp"))
    if slug == "home-page":
        a = html.find("<!-- ============ HERO ============ -->")
        b = html.find("</section>", a) + len("</section>")
        assert a > 0 and b > a, "home hero not found"
        html = html[:a] + hero_html() + html[b:]
    if slug in PAGES and "FOUNDER REELS" not in html:
        keys, h, i, marker = PAGES[slug]
        k = html.find(marker)
        if k < 0:
            k = html.find("</main>")
        assert k > 0, f"{slug}: marker {marker} not found and no </main>"
        html = html[:k] + reels_section(slug, keys, h, i).lstrip() + "  " + html[k:]
    return html


if __name__ == "__main__":
    for p in sorted((ROOT / "out").glob("*.html")):
        s = p.read_text(encoding="utf-8")
        p.write_text(enhance(p.stem, s), encoding="utf-8")
        print(f"{p.name:40} {len(p.read_text(encoding='utf-8')):6}")
