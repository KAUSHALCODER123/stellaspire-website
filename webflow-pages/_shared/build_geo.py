"""Build the global, country, country+service and India-city pages.

Reads the copy from geo.py, writes <slug>.body.html in the project root and
the finished embed to out/<slug>.html, then writes GEO-PAGES.md with the
title, meta description, canonical and hreflang for each page so they can be
pasted into Webflow page settings.

Usage: python -I _shared/build_geo.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SH = Path(__file__).resolve().parent
sys.path.insert(0, str(SH))
import geo  # noqa: E402

SITE = "https://www.stellaspire.com"
ADDRESS = ('"address":{"@type":"PostalAddress","streetAddress":"WeWork Prestige Central, 36 Infantry Road",'
           '"addressLocality":"Bengaluru","addressRegion":"Karnataka","postalCode":"560001","addressCountry":"IN"}')
PROVIDER = ('{"@type":"EmploymentAgency","name":"Stellaspire","url":"' + SITE + '",'
            '"email":"connect@stellaspire.com",' + ADDRESS + "}")

CITY_ORDER = ["bangalore", "mumbai", "delhi-ncr", "hyderabad", "pune", "chennai", "ahmedabad", "kolkata"]
PAGES = {}        # slug -> dict(path, title, desc, lang)


# ----------------------------------------------------------------- helpers
def cap(t):
    """Upper-case the first letter only. The built-in lower-cases the rest,
    which turns "IT recruitment" into "It recruitment"."""
    return t[:1].upper() + t[1:]


def adj(c):
    """The country as an adjective: "the US" -> "US companies"."""
    return re.sub(r"^the ", "", c["name"])


def crumbs(items):
    """items: list of (label, href or None). The last one is the current page."""
    out = []
    for label, href in items:
        if href:
            out.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            out.append(f"<li><span>{label}</span></li>")
    out[-1] = out[-1].replace("<span>", '<span aria-current="page">')
    return ('      <ol class="breadcrumb" aria-label="Breadcrumb">\n        '
            + "\n        ".join(out) + "\n      </ol>")


def hero(crumb_html, eyebrow, h1a, h1b, lead, short, cta_label, anchor_label, anchor="#roles"):
    return f"""  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero" aria-labelledby="page-heading">
    <div class="container">
{crumb_html}
      <div class="page-hero-grid">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h1 id="page-heading" class="page-title">{h1a} <span class="accent">{h1b}</span></h1>
          <p class="hero-lead">{lead}</p>
          <div class="hero-actions">
            <a class="button" href="/contact">{cta_label} <span aria-hidden="true">&#8599;</span></a>
            <a class="textlink" href="{anchor}">{anchor_label} <span aria-hidden="true">&#8594;</span></a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""


def table(rows, heading, intro, eyebrow="Roles we hire", note=None, cols=("Function", "Typical roles", "Seniority")):
    body = "\n".join(f"            <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    note_html = f'\n      <p class="table-note">{note}</p>' if note else ""
    return f"""
  <!-- ============ ROLES ============ -->
  <section id="roles" class="section band-line" aria-labelledby="roles-heading">
    <div class="container">
      <div class="section-top">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h2 id="roles-heading" class="h2">{heading}</h2>
        </div>
        <p class="section-intro">{intro}</p>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr><th scope="col">{cols[0]}</th><th scope="col">{cols[1]}</th><th scope="col">{cols[2]}</th></tr>
          </thead>
          <tbody>
{body}
          </tbody>
        </table>
      </div>{note_html}
    </div>
  </section>
"""


def method(eyebrow, heading, lede, body, link="/how-we-work", link_label="How we run a search"):
    return f"""
  <!-- ============ METHOD BAND ============ -->
  <section class="method" aria-labelledby="method-heading">
    <div class="container method-grid">
      <div>
        <p class="eyebrow eyebrow--light">{eyebrow}</p>
        <h2 id="method-heading" class="method-heading"><span>{heading}</span></h2>
      </div>
      <div>
        <p class="method-lede">{lede}</p>
        <p class="method-body">{body}</p>
        <a class="light-link" href="{link}">{link_label} <span aria-hidden="true">&#8594;</span></a>
      </div>
    </div>
  </section>
"""


def split(eyebrow, heading, body, items, hid="who"):
    lis = "\n".join(f"        <li><strong>{a}</strong> {b}</li>" for a, b in items)
    return f"""
  <!-- ============ WHO IT'S FOR ============ -->
  <section class="section" aria-labelledby="{hid}-heading">
    <div class="container split">
      <div>
        <p class="eyebrow">{eyebrow}</p>
        <h2 id="{hid}-heading" class="h2">{heading}</h2>
        <p class="body-copy">{body}</p>
      </div>
      <ul class="tick-list">
{lis}
      </ul>
    </div>
  </section>
"""


def cards(eyebrow, heading, intro, items, hid="models", band="band-mist"):
    cs = "\n".join(
        f'        <div class="card"><p class="card-meta">{meta}</p><h3 class="card-title">{title}</h3>'
        f'<p class="body-copy">{copy}</p></div>' for meta, title, copy in items)
    return f"""
  <!-- ============ CARDS ============ -->
  <section class="section {band}" aria-labelledby="{hid}-heading">
    <div class="container">
      <div class="section-top">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h2 id="{hid}-heading" class="h2">{heading}</h2>
        </div>
        <p class="section-intro">{intro}</p>
      </div>
      <div class="cards">
{cs}
      </div>
    </div>
  </section>
"""


def chips_band(eyebrow, heading, body, chip_label, chips, related=None, hid="where"):
    chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    rel = ""
    if related:
        rel_html = "".join(f'<a class="chip" href="{h}">{t} &#8594;</a>' for t, h in related)
        rel = f'\n        <p class="eyebrow" style="margin-top:40px">Related</p>\n        <div class="chips">{rel_html}</div>'
    return f"""
  <!-- ============ WHERE ============ -->
  <section class="section" aria-labelledby="{hid}-heading">
    <div class="container split">
      <div>
        <p class="eyebrow">{eyebrow}</p>
        <h2 id="{hid}-heading" class="h2">{heading}</h2>
        <p class="body-copy">{body}</p>
      </div>
      <div>
        <div class="chips" aria-label="{chip_label}">{chip_html}</div>{rel}
      </div>
    </div>
  </section>
"""


def faq(eyebrow, heading, items):
    rows = []
    for i, (q, a) in enumerate(items):
        rows.append(
            f'        <div class="faq-row"><h3 class="faq-question"><button class="faq-button" type="button" '
            f'aria-expanded="true" aria-controls="faq-{i}">{q}<span class="faq-icon" aria-hidden="true">&#8722;</span>'
            f'</button></h3><div id="faq-{i}" class="faq-answer"><p class="body-copy">{a}</p></div></div>')
    return f"""
  <!-- ============ FAQ ============ -->
  <section id="faqs" class="faq" aria-labelledby="faq-heading">
    <div class="container faq-grid">
      <div>
        <p class="eyebrow">{eyebrow}</p>
        <h2 id="faq-heading" class="h2">{heading}</h2>
      </div>
      <div>
{chr(10).join(rows)}
      </div>
    </div>
  </section>
"""


def cta(a, b, copy, label="Start a hiring conversation"):
    return f"""
  <!-- ============ CTA BAND ============ -->
  <section class="cta-band" aria-labelledby="cta-heading">
    <div class="container cta-grid">
      <h2 id="cta-heading" class="cta-title">{a} <span class="is-aqua">{b}</span></h2>
      <div>
        <p class="cta-copy">{copy}</p>
        <div class="cta-actions">
          <a class="button" href="/contact">{label} <span aria-hidden="true">&#8599;</span></a>
          <a class="light-link" href="mailto:connect@stellaspire.com">connect@stellaspire.com</a>
        </div>
      </div>
    </div>
  </section>
"""


def plain(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).replace("&amp;", "&").replace("&#8594;", "").strip()


def ld(service_name, service_type, desc, path, area, crumb, faqs):
    graph = [
        {"@type": "Service", "name": service_name, "serviceType": service_type,
         "provider": json.loads(PROVIDER), "areaServed": area, "description": plain(desc),
         "url": SITE + path},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (h or path)}
            for i, (n, h) in enumerate(crumb)]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": plain(q),
             "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]},
    ]
    return ('\n<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False,
                         separators=(",", ":"))
            + "\n</script>\n")


GENERIC_FAQS = [
    ("How are your fees structured?",
     "A percentage of annual fixed pay for contingency, a staged fee for retained leadership search, and a monthly rate for dedicated team hiring, all agreed in writing before the search starts."),
]


# ------------------------------------------------------------ page writers
def write(slug, path, title, desc, lang, body):
    PAGES[slug] = dict(path=path, title=title, desc=desc, lang=lang)
    (ROOT / f"{slug}.body.html").write_text(body.rstrip() + "\n", encoding="utf-8")


def country_page(key):
    c = geo.COUNTRIES[key]
    svc_links = [(geo.SERVICES[s]["label"], f"{c['path']}/{s}") for s in geo.COUNTRY_SERVICES[key]]
    body = (
        hero(crumbs([("Home", "/home-page"), ("Locations", None), (c["nav"], None)]),
             c["eyebrow"], c["h1_a"], c["h1_b"], c["lead"], c["short"],
             "Start a hiring conversation", "See the roles we hire")
        + split("Who this is for", c["why_h"], c["why_body"], c["why_items"])
        + table(c["roles"], "The roles we fill most often.",
                f"Specialist hiring for {adj(c)}-headquartered teams, from a single search to a full team build.")
        + method("How we work", c["method_h"], c["method_lede"], c["method_body"])
        + cards("Setting it up", c["comp_h"], c["comp_lede"], c["comp_cards"], hid="setup")
        + chips_band("Working hours", c["tz_h"], c["tz_body"], "Overlap", c["tz_chips"],
                     related=svc_links + [("Where we hire in India", "/india")], hid="overlap")
        + faq(f"{c['nav']} hiring questions", f"Questions {c['name']} clients ask.",
              c["faqs"] + GENERIC_FAQS)
        + ld(f"Recruitment for {c['formal']} companies", "Specialist recruitment and executive search",
             c["lead"], c["path"], [c["formal"], "India"],
             [("Home", "/"), (c["nav"], c["path"])], c["faqs"] + GENERIC_FAQS))
    write(f"geo-{key}", c["path"],
          f"{cap(c['kw'])} | Stellaspire",
          plain(c["short"])[:158], c["lang"], body)


def service_page(key, svc):
    c, s = geo.COUNTRIES[key], geo.SERVICES[svc]
    cs = geo.CS[(key, svc)]
    faqs = s["faqs"] + cs["faqs"] + GENERIC_FAQS
    lead = cs["angle"] + " " + s["lead_tail"]
    short = f"Stellaspire works with {adj(c)}-headquartered companies. " + s["short_tail"]
    path = f"{c['path']}/{svc}"
    body = (
        hero(crumbs([("Home", "/home-page"), (c["nav"], c["path"]), (s["label"], None)]),
             f"{cap(s['kw'])} for {c['name']}", f"{s['label']} for {adj(c)} companies.",
             s["h1_b"], lead, short, "Discuss a mandate", "See the roles we hire")
        + f"""
  <!-- ============ WHAT IS DIFFERENT ============ -->
  <section class="section" aria-labelledby="diff-heading">
    <div class="container split">
      <div>
        <p class="eyebrow">Worth knowing</p>
        <h2 id="diff-heading" class="h2">{cs['extra_h']}.</h2>
      </div>
      <div>
        <p class="body-copy">{cs['extra']}</p>
        <a class="textlink" href="{c['path']}">Everything we do for {c['name']} <span aria-hidden="true">&#8594;</span></a>
      </div>
    </div>
  </section>
"""
        + table(s["roles"], "The roles we fill most often.",
                f"{s['label']} for {adj(c)} companies hiring in India.")
        + method("How we work", s["method_h"], s["method_lede"], s["method_body"])
        + faq(f"{s['label']} questions", f"{s['label']} questions.", faqs)
        + ld(f"{s['label']} in India for {c['formal']} companies", s["label"],
             lead, path, [c["formal"], "India"],
             [("Home", "/"), (c["nav"], c["path"]), (s["label"], path)], faqs))
    write(f"geo-{key}-{svc}", path,
          f"{s['label']} in India for {adj(c)} companies | Stellaspire",
          plain(short)[:158], c["lang"], body)


def city_page(key):
    ci = geo.CITIES[key]
    name = ci["name"]
    others = [(geo.CITIES[k]["name"], geo.CITIES[k]["slugpath"]) for k in CITY_ORDER if k != key][:5]
    market_items = [(p.split(".")[0] + ".", p.split(".", 1)[1].strip()) for p in ci["market"]]
    body = (
        hero(crumbs([("Home", "/home-page"), ("India", "/india"), (name, None)]),
             f"{cap(ci['kw'])}", f"{cap(ci['kw'])}.", ci["h1_b"],
             ci["lead"], ci["short"], "Start a hiring conversation", "See the roles we hire")
        + split(f"The {name} market", ci["market_h"],
                f"Three things decide whether a {name} search closes.", market_items, hid="market")
        + table(ci["sectors"], f"Who we hire for in {name}.",
                f"The sectors and role families we run searches in across {name}.",
                eyebrow="Sectors and roles", cols=("Sector", "Typical roles", "Seniority"))
        + method(f"Hiring in {name}", ci["market_h"].replace(" actually looks like.", " rewards."),
                 f"We shortlist for {name} on commute and employer fit as well as skill.",
                 f"Every profile carries current pay in INR, notice period and an honest note on the gaps. If a brief is priced below what {name} pays today, we say so in week one.")
        + chips_band("Where we hire", f"Across {name}.",
                     f"We run searches across the main business districts and the industrial belt around {name}.",
                     "Business districts", ci["hubs"],
                     related=others + [("All India locations", "/india")], hid="hubs")
        + faq(f"{name} hiring questions", f"{name} hiring questions.", ci["faqs"] + GENERIC_FAQS)
        + ld(f"Recruitment agency in {name}", "Specialist recruitment and executive search",
             ci["lead"], ci["slugpath"], name,
             [("Home", "/"), ("India", "/india"), (name, ci["slugpath"])],
             ci["faqs"] + GENERIC_FAQS))
    write(f"geo-city-{key}", ci["slugpath"],
          f"{cap(ci['kw'])} | Finance, Data &amp; AI Hiring | Stellaspire",
          plain(ci["short"])[:158], "en-IN", body)


def india_hub():
    city_cards = [(geo.CITIES[k]["name"], cap(geo.CITIES[k]["kw"]),
                   plain(geo.CITIES[k]["lead"])[:150] + "...") for k in CITY_ORDER]
    cs = "\n".join(
        f'        <a class="card" href="{geo.CITIES[k]["slugpath"]}"><p class="card-meta">{geo.CITIES[k]["name"]}</p>'
        f'<h3 class="card-title">{cap(geo.CITIES[k]["kw"])}</h3>'
        f'<p class="body-copy">{plain(geo.CITIES[k]["market"][0])[:135]}&#8230;</p>'
        f'<span class="textlink">Hiring in {geo.CITIES[k]["name"]} <span aria-hidden="true">&#8594;</span></span></a>'
        for k in CITY_ORDER)
    faqs = [
        ("Which Indian cities do you hire in?",
         "Bengaluru, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai, Ahmedabad and Kolkata, run from our Bengaluru base with candidates met locally."),
        ("Does pay differ much between Indian cities?",
         "A great deal for the same role, so we benchmark by city and by the specific employers competing for the person."),
        ("Which city should we put a new team in?",
         "Bengaluru for technology and AI depth, Hyderabad and Pune for cost and retention, Mumbai for financial services, Ahmedabad for offshore accounting, Chennai for manufacturing finance."),
    ]
    body = (
        hero(crumbs([("Home", "/home-page"), ("India", None)]),
             "Recruitment across India", "Recruitment agency in India.",
             "Finance, data and AI hiring in eight cities.",
             "Finance, accounting, analytics, AI and leadership talent across India's eight main hiring markets, priced against the city rather than a national average.",
             "Stellaspire hires finance, accounting, analytics, AI and leadership talent across Bengaluru, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai, Ahmedabad and Kolkata, with pay benchmarked city by city.",
             "Start a hiring conversation", "Choose a city", anchor="#cities")
        + f"""
  <!-- ============ CITIES ============ -->
  <section id="cities" class="section band-line" aria-labelledby="cities-heading">
    <div class="container">
      <div class="section-top">
        <div>
          <p class="eyebrow">Where we hire</p>
          <h2 id="cities-heading" class="h2">Eight markets, priced separately.</h2>
        </div>
        <p class="section-intro">The same role can differ by half again between Bengaluru and Kolkata. Pick the city you are hiring in.</p>
      </div>
      <div class="cards">
{cs}
      </div>
    </div>
  </section>
"""
        + method("Why city matters", "A national salary band is a guess.",
                 "We benchmark against the employers competing for your candidate, in your city.",
                 "Pay, notice periods, attrition and commute tolerance all move city by city. Every search we open starts with the city before the role.")
        + chips_band("For global teams", "Hiring into India from abroad.",
                     "If your head office is outside India, start from the country page: entity, payroll, time zones and compliance.",
                     "Countries", [geo.COUNTRIES[k]["nav"] for k in geo.COUNTRIES],
                     related=[(geo.COUNTRIES[k]["nav"], geo.COUNTRIES[k]["path"]) for k in geo.COUNTRIES],
                     hid="global")
        + faq("India hiring questions", "India hiring questions.", faqs + GENERIC_FAQS)
        + ld("Recruitment agency in India", "Specialist recruitment and executive search",
             "Finance, accounting, analytics, AI and leadership hiring across eight Indian cities.",
             "/india", "IN", [("Home", "/"), ("India", "/india")], faqs + GENERIC_FAQS))
    write("geo-india", "/india", "Recruitment agency in India | Finance, Data &amp; AI Hiring | Stellaspire",
          "Stellaspire hires finance, accounting, analytics, AI and leadership talent across Bengaluru, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai, Ahmedabad and Kolkata.",
          "en-IN", body)


def global_hub():
    cs = "\n".join(
        f'        <a class="card" href="{geo.COUNTRIES[k]["path"]}"><p class="card-meta">{geo.COUNTRIES[k]["nav"]}</p>'
        f'<h3 class="card-title">{geo.COUNTRIES[k]["h1_a"].rstrip(".")}</h3>'
        f'<p class="body-copy">{plain(geo.COUNTRIES[k]["why_body"])[:140]}&#8230;</p>'
        f'<span class="textlink">Hiring from {geo.COUNTRIES[k]["name"]} <span aria-hidden="true">&#8594;</span></span></a>'
        for k in geo.COUNTRIES)
    faqs = [
        ("Which countries do you work with?",
         "Companies headquartered in the United States, the United Kingdom, the UAE, Singapore and Australia, plus Indian businesses hiring at home."),
        ("Do we need an Indian entity to hire?",
         "No. Most first hires go through an employer of record or our staffing payroll, then move onto your own entity once it exists."),
        ("How long does a search take?",
         "Four to six weeks from brief to signed offer for specialist roles, six to ten for leadership, plus a 60 to 90 day notice period at senior levels."),
    ]
    body = (
        hero(crumbs([("Home", "/home-page"), ("Global", None)]),
             "Hiring in India from anywhere", "Hire talent in India,",
             "from wherever your head office is.",
             "Finance, accounting, analytics, AI and leadership talent in India for companies headquartered in the US, the UK, the UAE, Singapore and Australia.",
             "We run specialist searches in India for global companies: finance, accounting, analytics, AI and leadership. One recruiter per mandate, a shortlist with pay and notice periods written on it, and a working pattern agreed before the search opens.",
             "Start a hiring conversation", "Choose your country", anchor="#countries")
        + f"""
  <!-- ============ COUNTRIES ============ -->
  <section id="countries" class="section band-line" aria-labelledby="countries-heading">
    <div class="container">
      <div class="section-top">
        <div>
          <p class="eyebrow">Where our clients are</p>
          <h2 id="countries-heading" class="h2">Five head-office markets.</h2>
        </div>
        <p class="section-intro">Each page covers the entity and payroll route, the overlap window and the compliance questions your team will ask.</p>
      </div>
      <div class="cards">
{cs}
      </div>
    </div>
  </section>
"""
        + method("What we are good at", "We hire in one country and we know it well.",
                 "Depth in one market beats a logo map of thirty offices.",
                 "We place people in India and nowhere else, so we can tell you what a controller in Hyderabad earns this quarter and why a brief priced on last year's numbers will not close.")
        + cards("How engagements run", "Three ways to work with us.",
                "Commercial and replacement terms are agreed in writing before any search begins.",
                [("Single roles", "Contingency search", "For specialist and mid-senior hires. A fee is payable only when a candidate we introduce joins."),
                 ("Leadership", "Retained search", "For CFOs, finance heads and confidential replacements, with a written market map before the shortlist."),
                 ("Team builds", "Dedicated hiring", "For new centres hiring several roles at once, with one recruiter, a shared hiring plan and a weekly pipeline review.")],
                hid="models")
        + chips_band("Where the hiring happens", "Eight Indian cities.",
                     "Pay, notice periods and attrition differ enough between them that we benchmark city by city.",
                     "Cities", [geo.CITIES[k]["name"] for k in CITY_ORDER],
                     related=[("All India locations", "/india")]
                     + [(geo.CITIES[k]["name"], geo.CITIES[k]["slugpath"]) for k in CITY_ORDER[:4]],
                     hid="cities")
        + faq("Global hiring questions", "Questions global teams ask.", faqs + GENERIC_FAQS)
        + ld("Hire talent in India", "Specialist recruitment and executive search for global companies",
             "Finance, accounting, analytics, AI and leadership hiring in India for companies headquartered in the US, UK, UAE, Singapore and Australia.",
             "/global", ["US", "GB", "AE", "SG", "AU", "IN"],
             [("Home", "/"), ("Global", "/global")], faqs + GENERIC_FAQS))
    write("geo-global", "/global", "Hire talent in India | Global recruitment partner | Stellaspire",
          "Stellaspire hires finance, accounting, analytics, AI and leadership talent in India for companies headquartered in the US, UK, UAE, Singapore and Australia.",
          "en", body)


def global_india_page():
    faqs = [
        ("What does it cost to hire in India?",
         "It varies more by city and function than most head offices expect, so we benchmark each role against the specific employers competing for the person."),
        ("What is a normal notice period?",
         "Thirty days at junior levels, 60 to 90 at manager level and above, and sometimes longer in financial services."),
        ("Can an India team work our hours?",
         "The UK, the UAE and Singapore overlap comfortably, Australia works from its afternoon onwards, and the US needs a 2pm to 11pm IST shift."),
    ]
    body = (
        hero(crumbs([("Home", "/home-page"), ("Global", "/global"), ("Hire talent in India", None)]),
             "Hiring in India", "Hire talent in India.",
             "What it costs, how long it takes, what goes wrong.",
             "Entity and payroll, the real cost by city, notice periods, the overlap window and the four things that make an India hire fail.",
             "You can hire in India without an entity, and a specialist finance or data search takes four to six weeks plus a 60 to 90 day notice period. Cost varies more by city than most head offices expect, and the most common failure is a shift expectation nobody put in the brief.",
             "Start a hiring conversation", "Read the practical bits", anchor="#roles")
        + split("The honest version", "Four things that make an India hire fail.",
                "None of them are about the candidate pool, which is deep. They are about the brief.",
                [("A salary band set on a national average.",
                  "Pay moves by half again between Bengaluru and Kolkata for the same role."),
                 ("A shift expectation discovered at offer stage.",
                  "Put the working pattern in the brief and test every shortlisted person against it."),
                 ("No senior person on the ground.",
                  "Hire the supervisor first."),
                 ("Planning around a 30-day notice period.",
                  "Sixty to ninety days is normal at manager level and above.")],
                hid="fail")
        + table([("Finance &amp; accounting", "Controller, R2R lead, statutory and group reporting, chartered accountants", "Manager to Director"),
                 ("FP&amp;A", "FP&amp;A manager, business finance partner, commercial finance", "Analyst to Senior Manager"),
                 ("Data &amp; analytics", "Analytics manager, data engineer, BI lead, data scientist", "Senior IC to Head"),
                 ("AI &amp; ML", "ML engineer, applied scientist, LLM and platform engineers", "Senior IC to Lead"),
                 ("Technology", "Backend, full-stack, cloud, DevOps, engineering manager", "Mid to Director"),
                 ("Leadership", "India site head, country finance head, CFO", "Director to CFO")],
                "What we hire, and what we do not.",
                "We stay inside finance, accounting, analytics, AI and the engineering around them. Outside that, we refer you on.")
        + method("The part people underestimate", "Notice periods change your whole plan.",
                 "Sixty to ninety days is normal, and that is after a four to six week search.",
                 "Work backwards from the start date you need: a specialist hire that opens in January is usually at a desk in April. We put the realistic joining date on the shortlist, next to the pay.")
        + cards("Getting set up", "Entity, payroll and the first offer.",
                "Most clients make their first hires before the Indian entity exists.",
                [("Fastest start", "Employer of record", "Your hire is employed by a licensed Indian provider and works for you. Set-up takes days."),
                 ("Scaling up", "Your own entity", "A private limited company plus a payroll provider, worth it from roughly the fifth hire."),
                 ("Either route", "What goes in the offer", "Cost to company, provident fund, gratuity, notice period and the joining bonus that is market for the role.")],
                hid="setup")
        + chips_band("Where the hiring happens", "Pick the city before the role.",
                     "Function, cost and retention all point to different cities. Each city page covers its employer set and what drives pay there.",
                     "Cities", [geo.CITIES[k]["name"] for k in CITY_ORDER],
                     related=[("All India locations", "/india")]
                     + [(geo.COUNTRIES[k]["nav"], geo.COUNTRIES[k]["path"]) for k in geo.COUNTRIES],
                     hid="cities")
        + faq("Hiring in India", "What head offices ask us.", faqs + GENERIC_FAQS)
        + ld("Hire talent in India", "Recruitment and executive search in India for global companies",
             "What it costs to hire in India, how long a search takes, entity and payroll routes, notice periods and the four things that make an India hire fail.",
             "/global/hire-talent-india", ["US", "GB", "AE", "SG", "AU", "IN"],
             [("Home", "/"), ("Global", "/global"), ("Hire talent in India", "/global/hire-talent-india")],
             faqs + GENERIC_FAQS))
    write("geo-global-hire-talent-india", "/global/hire-talent-india",
          "Hire talent in India: cost, timeline and how it works | Stellaspire",
          "What it costs to hire in India, how long a search takes, whether you need an entity, notice periods and the four things that make an India hire fail.",
          "en", body)


# ------------------------------------------------------------------- build
def main():
    global_hub()
    global_india_page()
    for k in geo.COUNTRIES:
        country_page(k)
        for s in geo.COUNTRY_SERVICES[k]:
            service_page(k, s)
    india_hub()
    for k in CITY_ORDER:
        city_page(k)

    # assemble each embed, then apply the American spelling pass on /us pages
    us_slugs = {"geo-us"} | {f"geo-us-{s}" for s in geo.COUNTRY_SERVICES["us"]}
    for slug in PAGES:
        out = ROOT / "out" / f"{slug}.html"
        subprocess.run([sys.executable, "-I", str(SH / "build.py"),
                        str(ROOT / f"{slug}.body.html"), str(out)], check=True, stdout=subprocess.DEVNULL)
        s = out.read_text(encoding="utf-8")
        if slug in us_slugs:
            for a, b in geo.SPELL_US:
                s = s.replace(a, b)
        out.write_text(s, encoding="utf-8")

    # the head snippets, for Webflow page settings
    alts = {k: geo.COUNTRIES[k]["path"] for k in geo.COUNTRIES}
    lines = ["# Geo pages: Webflow page settings",
             "",
             "One block per page. Paste the title and description into the page's SEO settings,",
             "and the `<link>` tags into the page's custom code (head).",
             "",
             "The country pages are alternates of each other, so they all carry the same hreflang set.",
             ""]
    hreflang = "\n".join(
        f'<link rel="alternate" hreflang="{geo.COUNTRIES[k]["lang"]}" href="{SITE}{p}">' for k, p in alts.items())
    hreflang += f'\n<link rel="alternate" hreflang="en-IN" href="{SITE}/india">'
    hreflang += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/global">'
    for slug, d in PAGES.items():
        lines += [f"## {d['path']}", "",
                  f"- **Slug / folder:** `{d['path']}`  (Webflow: create the folder, then the page)",
                  f"- **Title:** {d['title']}",
                  f"- **Description:** {d['desc']}",
                  f"- **Language:** `{d['lang']}`",
                  f"- **Embed:** `out/{slug}.html`", "",
                  "```html",
                  f'<link rel="canonical" href="{SITE}{d["path"]}">']
        if slug.startswith("geo-") and slug.count("-") == 1 and slug[4:] in geo.COUNTRIES or slug in ("geo-global", "geo-india"):
            lines.append(hreflang)
        lines += ["```", ""]
    (ROOT / "GEO-PAGES.md").write_text("\n".join(lines), encoding="utf-8")

    for slug, d in PAGES.items():
        n = len((ROOT / "out" / f"{slug}.html").read_text(encoding="utf-8"))
        print(f"{d['path']:42} {slug:34} {n:6}")
    print(len(PAGES), "geo pages")


if __name__ == "__main__":
    main()
