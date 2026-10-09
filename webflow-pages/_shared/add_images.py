"""Insert the supplied photos into the page bodies (idempotent: skips pages already done)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CDN = "https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/"

IMG = {
    "gcc": ("6ac5e8d5fbfe8afe5ca1773d_stellaspire-gcc-hiring-team.jpg", 1586, 992,
            "A woman team lead presenting analytics on a screen to two colleagues in a Bengaluru office at sunset"),
    "cfo": ("6ac5e8d5b2a2e139ea55de76_stellaspire-cfo-executive-search.jpg", 1000, 1250,
            "A senior woman finance executive reviewing documents in a bright boardroom overlooking the city"),
    "fin": ("6ac5e8d647485411ecbfc711_stellaspire-finance-accounting-recruitment.jpg", 1586, 992,
            "Two finance professionals reviewing a spreadsheet together on a laptop in a modern office"),
    "data": ("6ac5e8d7fbfe8afe5ca17848_stellaspire-analytics-data-team.jpg", 1586, 992,
             "A woman data scientist explaining a chart on a whiteboard to two colleagues"),
    "div": ("6ac5e8d7fbfe8afe5ca17875_stellaspire-diversity-hiring-team.jpg", 1586, 992,
            "A gender-balanced group of professionals of different ages in conversation in an office lounge"),
    "ret": ("6ac5e8d7fbfe8afe5ca17894_stellaspire-women-returnship.jpg", 1000, 1250,
            "A woman professional walking confidently into a bright modern office with her bag"),
    "fees": ("6ac5e8d79356b0a30badce8c_blog-recruitment-agency-fees-india.jpg", 1600, 840,
             "A notebook, calculator, pen and printed offer letter on a light desk"),
    "gccg": ("6ac5e8d72a8a316be947258c_blog-gcc-hiring-guide-india.jpg", 1600, 840,
             "A Bengaluru tech park with glass office towers at dusk"),
    "cfop": ("6ac5e8d8b35fcf2a547929d5_blog-cfo-hiring-process.jpg", 1600, 840,
             "An empty chair at the head of a boardroom table with a folder placed in front of it"),
    "ret2": ("6ac5e8d804edb2f7e2a16b35_blog-retained-vs-contingency-search.jpg", 1600, 840,
             "A king and a pawn chess piece on a marble surface"),
}


def img(key, eager=False, cls=""):
    f, w, h, alt = IMG[key]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{CDN}{f}" alt="{alt}" width="{w}" height="{h}" {load} decoding="async">'


def band(key):
    return ('\n  <!-- ============ PHOTO ============ -->\n'
            '  <div class="container photo-band">\n'
            f'    <figure class="photo photo-wide">{img(key, eager=True)}</figure>\n'
            '  </div>\n')


def edit(slug, fn):
    p = ROOT / f"{slug}.body.html"
    s = p.read_text(encoding="utf-8")
    if "6ac5e8d" in s:
        print("skip (done)", slug)
        return
    s2 = fn(s)
    assert s2 != s, slug
    p.write_text(s2, encoding="utf-8")
    print("edited", slug)


def after_hero(key):
    def fn(s):
        i = s.find("</section>", s.find('class="page-hero"')) + len("</section>")
        return s[:i] + "\n" + band(key) + s[i:]
    return fn


for slug, key in [("gcc-hiring", "gcc"), ("finance-accounting-recruitment", "fin"),
                  ("analytics-data-recruitment", "data"), ("ai-ml-recruitment", "data"),
                  ("diversity-hiring", "div")]:
    edit(slug, after_hero(key))


def cfo(s):
    # Portrait beside the "Who this is for" copy (left column), so the 4:5 image is not cropped.
    anchor = s.find("</p>", s.find('id="who-heading"'))
    anchor = s.find("</p>", anchor + 4) + 4  # after the body-copy paragraph
    fig = f'\n        <figure class="photo photo-portrait">{img("cfo")}</figure>'
    return s[:anchor] + fig + s[anchor:]


edit("cfo-executive-search", cfo)


def returnship(s):
    a = s.find('<figure class="photo"')
    b = s.find("</figure>", a) + len("</figure>")
    return s[:a] + f'<figure class="photo photo-portrait photo-hero">{img("ret", eager=True)}</figure>' + s[b:]


edit("women-returnship", returnship)


def article(key):
    def fn(s):
        i = s.find("</section>", s.find('class="article-hero"'))
        # close position: inside the hero container, after .article-head
        j = s.rfind("</div>", 0, i)  # closes .container
        fig = f'      <figure class="photo article-cover">{img(key, eager=True)}</figure>\n    '
        return s[:j] + fig + s[j:]
    return fn


for slug, key in [("recruitment-agency-fees-india", "fees"), ("gcc-hiring-guide-india", "gccg"),
                  ("cfo-hiring-process", "cfop"), ("retained-vs-contingency-search", "ret2")]:
    edit(slug, article(key))


def hub(s):
    a = s.find('<article class="featured-article">') + len('<article class="featured-article">')
    cover = f'\n          <a class="featured-cover" href="/gcc-hiring-guide-india" tabindex="-1" aria-hidden="true">{img("gccg")}</a>'
    return s[:a] + cover + s[a:]


edit("insights", hub)
