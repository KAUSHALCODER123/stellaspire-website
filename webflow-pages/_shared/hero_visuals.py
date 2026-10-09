"""Page-hero graphics (v7). One small, decorative, page-specific visual per inner page.

Each replaces the text aside on the right of the page hero; the aside's text is moved below the hero
(see enhance.py) so it stays on the page for search engines and readers. Motion is CSS-only (hv.css).
"""


def rows(items):
    return "".join(
        f'<li style="--i:{i}"><span class="hv-ic">{ic}</span><span><b>{t}</b><small>{s}</small></span></li>'
        for i, (ic, t, s) in enumerate(items))


def steps(items, done=0):
    return "".join(f'<li style="--i:{i}"><span class="hv-step"></span><b>{t}</b></li>' for i, t in enumerate(items))


def card(top, body, chip=None, cls=""):
    chip_html = f'<div class="hv-chip">{chip}</div>' if chip else ""
    return (f'<div class="hv {cls}" aria-hidden="true"><div class="hv-card">'
            f'<p class="hv-top"><span class="hv-dot"></span>{top}</p>{body}</div>{chip_html}</div>')


FINANCE = card("Roles we fill", '<ul class="hv-list hv-cycle">' + rows([
    ("CA", "Chartered Accountant", "Reporting, statutory, audit"),
    ("FC", "Financial Controller", "Close, controls, compliance"),
    ("FP", "FP&amp;A Lead", "Budgets, forecasts, business partnering"),
    ("TX", "Tax Manager", "Direct and indirect tax"),
    ("TR", "Treasury Manager", "Cash, banking, FX"),
    ("FH", "Finance Head", "Team and board reporting"),
]) + "</ul>", "✓ Assessed by people who know finance")

CFO = card("Confidential search", '<p class="hv-title">Chief Financial Officer</p><p class="hv-sub">Retained · Board-level mandate</p>'
           '<ol class="hv-steps hv-seq">' + steps([
               "Mandate agreed with the board", "Market mapped, discreetly", "Shortlist of leaders presented",
               "Board and CEO interviews", "Offer and 90-day plan"]) + "</ol>", "✓ Discreet from first call to offer")

GCC = card("GCC team build", '<div class="hv-cities">' + "".join(
    f'<span style="--i:{i}"><i></i>{c}</span>' for i, c in enumerate(
        ["Bengaluru", "Hyderabad", "Pune", "Chennai", "Delhi NCR", "Mumbai"])) + "</div>"
    '<p class="hv-label">Hiring plan</p><div class="hv-stack">'
    '<span style="--w:30%;--i:0">Finance ops</span><span style="--w:24%;--i:1">FP&amp;A</span>'
    '<span style="--w:28%;--i:2">Analytics</span><span style="--w:18%;--i:3">Leaders</span></div>'
    '<p class="hv-note">From the first hire to a full India team</p>', "Finance · Analytics · Leadership")

ANALYTICS = card("Candidate scorecard", '<p class="hv-title">Head of Analytics</p>'
                 '<ul class="hv-bars">' + "".join(
                     f'<li style="--w:{w}%;--i:{i}"><span>{t}</span><i></i></li>' for i, (t, w) in enumerate([
                         ("SQL &amp; data modelling", 92), ("Python &amp; statistics", 84), ("BI &amp; visualisation", 88),
                         ("Experimentation", 76), ("Storytelling with data", 90)])) + "</ul>"
                 '<svg class="hv-spark" viewBox="0 0 300 60" preserveAspectRatio="none"><path d="M0 50 L40 44 L80 46 L120 32 L160 36 L200 22 L240 26 L300 8"/></svg>',
                 "✓ Technical depth and business sense")

AIML = card("AI &amp; ML talent map",
            '<svg class="hv-net" viewBox="0 0 320 190">'
            '<g class="hv-links">'
            '<path d="M40 40 L160 30 M40 40 L160 95 M40 95 L160 30 M40 95 L160 95 M40 95 L160 160 M40 150 L160 95 M40 150 L160 160'
            ' M160 30 L280 60 M160 95 L280 60 M160 95 L280 130 M160 160 L280 130"/></g>'
            '<g class="hv-nodes"><circle cx="40" cy="40" r="7"/><circle cx="40" cy="95" r="7"/><circle cx="40" cy="150" r="7"/>'
            '<circle cx="160" cy="30" r="9"/><circle cx="160" cy="95" r="9"/><circle cx="160" cy="160" r="9"/>'
            '<circle cx="280" cy="60" r="11"/><circle cx="280" cy="130" r="11"/></g></svg>'
            '<div class="hv-tags"><span>LLMs &amp; NLP</span><span>MLOps</span><span>Computer vision</span><span>Applied research</span><span>AI product</span></div>',
            "✓ Hands-on builders, not buzzwords")

DIVERSITY = card("Shortlist", '<p class="hv-title">Finance Controller</p>'
                 '<div class="hv-people">' + "".join(
                     f'<span class="{c}" style="--i:{i}"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 4-7 8-7s7 2 8 7"/></svg></span>'
                     for i, c in enumerate(["w", "m", "w", "m", "w", "m"])) + "</div>"
                 '<p class="hv-legend"><span class="w"></span>Women <span class="m"></span>Men</p>'
                 '<ul class="hv-checks"><li>Same criteria for every candidate</li><li>Structured interviews</li><li>Wider search, not a lower bar</li></ul>',
                 "✓ Gender-balanced shortlist")

RETURNSHIP = card("Your career, restarted",
                  '<svg class="hv-time" viewBox="0 0 320 120">'
                  '<path class="t1" d="M10 80 H110"/><path class="t2" d="M110 80 H190"/><path class="t3" d="M190 80 C230 80 250 40 310 30"/>'
                  '<circle cx="10" cy="80" r="6"/><circle cx="110" cy="80" r="6"/><circle class="glow" cx="190" cy="80" r="8"/><circle cx="310" cy="30" r="6"/></svg>'
                  '<div class="hv-time-labels"><span>Your experience</span><span>Career break</span><span>Restart</span><span>Grow</span></div>'
                  '<ul class="hv-checks"><li>Roles that value what you already know</li><li>Support through every interview</li></ul>',
                  "✓ For experienced women professionals")

HOW = card("A Stellaspire search", '<ol class="hv-steps hv-seq hv-seq--six">' + steps([
    "Align the brief", "Map the market", "Assess candidates", "Present a considered shortlist",
    "Coordinate interviews", "Close the offer and onboard"]) + "</ol>", "✓ One accountable partner throughout")

ABOUT = ('<div class="hv hv--about" aria-hidden="true"><div class="hv-orb"><img src="{{LOGO}}" alt="" width="120" height="170"></div>'
         '<span class="hv-pill" style="--i:0">Women-led</span><span class="hv-pill" style="--i:1">Bengaluru</span>'
         '<span class="hv-pill" style="--i:2">Finance · Analytics · Leadership</span><span class="hv-pill" style="--i:3">Gender-balanced shortlists</span></div>')

INSIGHTS = ('<div class="hv hv--stack" aria-hidden="true">'
            '<div class="hv-paper" style="--i:0"><small>Buyer guide</small><b>Recruitment agency fees in India</b></div>'
            '<div class="hv-paper" style="--i:1"><small>GCC hiring</small><b>The complete GCC hiring guide</b></div>'
            '<div class="hv-paper" style="--i:2"><small>Finance leadership</small><b>The CFO hiring process</b></div>'
            '<div class="hv-paper" style="--i:3"><small>Buyer guide</small><b>Retained vs contingency search</b></div></div>')

VISUALS = {
    "finance-accounting-recruitment": FINANCE,
    "cfo-executive-search": CFO,
    "gcc-hiring": GCC,
    "analytics-data-recruitment": ANALYTICS,
    "ai-ml-recruitment": AIML,
    "diversity-hiring": DIVERSITY,
    "women-returnship": RETURNSHIP,
    "how-we-work": HOW,
    "about": ABOUT,
    "insights": INSIGHTS,
}
