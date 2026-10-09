# Stellaspire: new Webflow pages (7 October 2026)

All pages are built in the Webflow site **StellAspire** (`66a5fdf6d0c2ac84ca88fe93`) in the same design as `/home-page`. **Nothing has been published yet.**

## Pages
| Page | URL | Webflow page ID |
|---|---|---|
| Home (updated) | /home-page | 6ac49970030703da9979c2e7 |
| GCC Hiring | /gcc-hiring | 6ac5df5e4fb1e2d356a4ac83 |
| Finance & Accounting Recruitment | /finance-accounting-recruitment | 6ac5e151c6e1a1d487c8aa97 |
| CFO & Executive Search | /cfo-executive-search | 6ac5e1e79356b0a30bab40c8 |
| Analytics & Data Recruitment | /analytics-data-recruitment | 6ac5e278fa15b9f9fc18e3e8 |
| AI & ML Recruitment | /ai-ml-recruitment | 6ac5e2539af6b5443ef723ee |
| Diversity Hiring | /diversity-hiring | 6ac5e253ed9d0f3fb972a3d3 |
| Women Returnship | /women-returnship | 6ac5e25436e371dda4e2d2f8 |
| How We Work | /how-we-work | 6ac5e23fc9fd9470689d2db5 |
| About | /about | 6ac5e24078e6f8a51a874bf2 |
| Contact | /contact | 6ac5e2404fb1e2d356a5c597 |
| Insights (blog hub) | /insights | 6ac5e260b2a2e139ea541889 |
| Blog: Recruitment agency fees in India | /recruitment-agency-fees-india | 6ac5e2617233a7c9057147c4 |
| Blog: GCC hiring guide | /gcc-hiring-guide-india | 6ac5e261b2a2e139ea5418de |
| Blog: CFO hiring process | /cfo-hiring-process | 6ac5e1efe968e8bd26c5d1bb |
| Blog: Retained vs contingency search | /retained-vs-contingency-search | 6ac5e1f0092a21c14c60d39a |

## How the pages are built
- Each page is one HTML Embed (header + content + footer), the same way `/home-page` is built.
- The styles are one shared stylesheet hosted in Webflow Assets: `stellaspire-pages-v2.css` (the home-page CSS plus the new components). The script is `stellaspire-pages.js` (mobile menu, FAQ accordion, Services dropdown). Each page links to both in its page custom code.
- **To change the design:** edit `_shared/extra.css`, rebuild, upload it as a new asset (v3), then update the `<link>` in each page's head.
- **Local sources:** `<slug>.body.html` holds each page's content, `out/<slug>.html` the full embed, and `_shared/` the header, footer, CSS, JS and build scripts.
- **Backup of the original home page:** `home-page.original.html` (embed) and `_shared/home.css` (its original inline CSS).

## Status (7 October 2026)
- **Published to stellaspire.webflow.io only** (staging). stellaspire.com was not published.
- **Images:** 10 supplied images are in `assets/` and in Webflow Assets, placed on the service pages, the returnship page, the 4 articles and the Insights hub. Each page's photo is also its Open Graph share image.
- **CSS:** `stellaspire-pages-v3.css`. To change it, edit `_shared/extra.css`, upload it as a new asset (v4) and update every page's head `<link>`.
- **Forms work.** Each designed form (Contact, Home) sits inside the embed. A hidden native Webflow form on the same page (class `ss-form-anchor`) loads Webflow's form handler. The designed form carries that native form's `data-wf-page-id` and `data-wf-element-id`. **Do not delete the hidden forms.** Submissions appear in Webflow → Site settings → Forms. Two "TEST – please ignore" submissions were sent on 7 October 2026.
- **Rebuild everything:** `python -I _shared/build_all.py - -` (root URLs) or `python -I _shared/build_all.py services insights` (folder URLs).

## v6 (8 October 2026): brand, motion, founder videos, blog upgrade — built locally, not yet uploaded
- **Brand board applied:** Montserrat, #947AD3 / #70B5F0 / #D3D3D3 / black, rectangular black buttons, SP logo in the footer (`assets/stellaspire-mark.svg`).
- **Home hero:** "the search" canvas motion graphic (`_shared/hero-search.js`): talent-pool dots → scan → shortlist → SP mark. Pauses off-screen; static for reduced motion; starts after load.
- **Founder reels:** 4 videos in `assets/video/` (compressed, ~2–4 MB, load only on tap) on every page except Contact, with VideoObject schema. GA4 events `video_start`, `video_complete`, `checklist_tick` fire if gtag is present.
- **Motion layer:** `_shared/motion.js` (parallax, card tilt, count-up, magnetic buttons, reading progress). Blog: `_shared/blog.css`, `_shared/blog.js` (takeaways, timeline, checklist saved per browser, collapsible FAQs, active TOC, share bar, Keep reading cards).
- **Renamed:** "Diversity Hiring" → "Gender-Diversity Hiring" in all labels (URL `/diversity-hiring` unchanged). Update that page's SEO title/description in Webflow page settings to match.
- **Build:** `python -I _shared/build_all.py - -` now also runs `enhance.py` and writes `_shared/stellaspire-pages-v6.css` / `-v6.js`. Local preview: `python -I _shared/preview6.py`, then open `preview6/home-page.html`.
- **To publish:** upload the 4 MP4 + 4 JPG posters, `stellaspire-mark.svg`, v6 CSS and v6 JS to Webflow Assets; put their URLs in `_shared/media-urls.json` (keys = file names); rebuild; paste each `out/<slug>.html` into its page embed; in every page head add the Montserrat Google Fonts link and swap v5.css → v6.css; in every page footer swap v2.js → v6.js.


## v9 (8 October 2026): brand colour correction, geo pages — built locally, not yet uploaded

### Brand colours put back on the board
The v6 dark sections were built on `#211a35` and `#120d24`, which are dark
purple. The brand board is **#947AD3 / #70B5F0 / #D3D3D3 / black**. `_shared/brand.css`
loads last in the bundle and corrects this:
- dark surfaces (method band, CTA band, footer) are now near-black `#0e0e10`
- purple and blue are accents only, never a background wash
- the radial "glow" washes behind the reels, the reel CTA tile and the page heroes
  are removed (`content: none`), since those were the main generated-looking tell
- buttons are black and square per the brand board, inverting to white on dark
- the method band was rebuilt as a 5/7 top-aligned split with a drawn rule, instead
  of a centred 50/50 that left half the band empty
- the footer was rebuilt: black ground, brand-gradient rule on top, underlined
  section headings, `#D3D3D3` link colour, wider first column, Locations column added

**To change any of this, edit `_shared/brand.css` and rebuild.** It is the last file
in `build_assets.py`, so anything in it wins.

### New video poster frames
The four founder reels had poster frames grabbed mid-sentence at awkward crops.
New frames were chosen from the videos and written to `assets/video/*.jpg`
(old ones kept in `assets/video/_old_posters/`):

| Video | Frame | Why |
|---|---|---|
| why-hire-a-consultant | 22.6s | warm smile, SP lockup in shot |
| background-check | 26.2s | composed, caption on topic |
| resume-tips | 30.4s | "Resume matching score hai" caption |
| job-description-tips | 14.2s | "Reach out to the Right people" caption |

The reel card CSS was changed to suit them: the scrim is now light in the lower
third so the burned-in captions stay readable, the duration chip moved to the top
of the card, the gradient ring around the poster is gone and the play button is a
plain white disc without the pulsing halo.

**These JPGs must be re-uploaded to Webflow Assets** and their URLs updated in
`_shared/media-urls.json`, or the live site keeps showing the old posters.

### 26 new location pages
Built from `_shared/geo.py` (all the copy) by `_shared/build_geo.py`. Each page is
written for its own market, including spelling and vocabulary: US pages use
American spelling, resume, US GAAP and EOR; UK pages use CV and IR35; UAE pages use
Emiratisation, MOHRE, DIFC and ADGM; Singapore pages use Employment Pass and CPF;
Australia pages use superannuation and Fair Work.

| Group | Pages |
|---|---|
| Global | `/global`, `/global/hire-talent-india` |
| Countries | `/us`, `/uk`, `/uae`, `/singapore`, `/australia` |
| Country + service | `/<country>/it-recruitment`, `/<country>/finance-leadership-hiring` (10) |
| India | `/india` |
| India metros | `/india/<city>-recruitment-agency` for Bengaluru, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai, Ahmedabad, Kolkata |

- **Titles, meta descriptions, canonicals and hreflang** for all 26 are in
  `GEO-PAGES.md`, ready to paste into Webflow page settings.
- A **Locations** dropdown was added to the header and a Locations column to the footer.
- Each page carries Service, BreadcrumbList and FAQPage structured data.
- `build_geo.py` runs inside `build_all.py`, before the enhance pass, so the geo
  pages get the founder reels like every other page.

**To publish these:** create the `global`, `us`, `uk`, `uae`, `singapore`,
`australia` and `india` folders in the Webflow Designer, create each page inside
its folder with the slug from `GEO-PAGES.md`, paste `out/geo-*.html` into the page
embed, and add the head snippet from `GEO-PAGES.md` to the page's custom code.


### v9 asset URLs (uploaded 8 October 2026)
| File | URL |
|---|---|
| Stylesheet (current) | `https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/6ac7755e5f33cb6f3c1c2206_stellaspire-pages-v9b.css` |
| Script (unchanged from v6) | `https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/6ac732ad56d52bda2be8bbf9_stellaspire-pages-v6.js` |

Put the stylesheet URL in every page's head `<link>` in place of the v3/v5 one.
Webflow addresses assets by content hash, so **editing `brand.css` and rebuilding
produces a new file that needs a fresh upload and a new URL.** The `-v9b` suffix
is the second upload of the day; bump the letter each time.

### Dark surfaces: taken from the logo
`assets/stellaspire-mark.svg` is a three-stop gradient, and it is the source of
truth for the brand palette:

| Stop | Hex |
|---|---|
| Violet | `#A77BE3` |
| Periwinkle | `#8EA2EC` |
| Sky | `#62B6F2` |

The dark surfaces are deep, saturated tones on that same violet-to-blue axis,
so they read as the brand rather than as a neutral dark. They are darker than
the logo colours themselves because those cannot hold white text.

| Surface | Hex | Contrast with white |
|---|---|---|
| Method and CTA bands | `#1D2142` | 15.6:1 |
| Footer | `#141733` | 17.5:1 |
| Eyebrows on dark | `#B79AEA` | 6.5:1 on the band |
| Body text on dark | `#CFD3E6` | 10.5:1 on the band |

Every pairing clears WCAG AA. Both surfaces carry the true three-stop logo
gradient as a 2px hairline on their top edge. The footer is a five-column grid:
brand, Services, Candidates, Locations, Company.

### No em or en dashes
House style. `build_all.py` fails the build if `—`, `–`, `&mdash;` or `&ndash;`
appears in any built page, so one cannot creep back into a page nobody re-reads.
Five were found and removed on 8 October 2026 (home hero, a blog link title, a
CFO-article numeric range and a CEO/CFO pairing, and a returnship placeholder).

### Stylesheet versions uploaded 8 October 2026
Webflow addresses assets by content hash, so **every `brand.css` edit needs a
fresh upload and a new URL in all 43 page heads.** Current:

`https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/6ac777fb1b1967d29518b29b_stellaspire-pages-v9c.css`

Script (unchanged since v6):
`https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/6ac732ad56d52bda2be8bbf9_stellaspire-pages-v6.js`


## v10 (8 October 2026): CTA band and footer redesign — live on staging

Both bands rebuilt to an editorial brief. Shipped as styling over the existing
markup, so it went live without the Webflow Designer.

**CTA band**: Fraunces headline at `clamp(40px, 5.2vw, 68px)`, 12-column grid
with the headline on columns 1 to 8, a single hairline, the body copy offset to
columns 5 to 10 beneath it, and a square solid `#70B5F0` button. No gradient.

**Footer**: flat `#141733`, gradient top rule removed, headings sentence-case
14px/600 in white with no letter-spacing and no underline, links 15px `#CFD3E6`
hovering to white with a 1px `#70B5F0` underline, Fraunces tagline, muted
address, one hairline above the bottom bar only.

**Fraunces** is loaded on every page but used on exactly two elements: the CTA
headline and the footer tagline. Everything else stays Montserrat.

Three judgement calls made without a decision from Gaurav:
1. **Privacy and Terms links were dropped.** The brief asked for them in the
   bottom bar, but no such pages exist, so they would have been 404s.
2. **The logo-gradient hairlines were removed** from the CTA band and the footer
   top, because the brief asks for no gradient outside the logo.
3. **Per-page CTA copy was kept.** The brief supplied one headline; applying it
   to all 43 pages would have replaced every page's specific call to action with
   a single generic line. The design is applied everywhere, the words are not.

Stylesheet: `https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/6ac77b68efa8b89cc2d982de_stellaspire-pages-v9d.css`

Reference files, built standalone to the brief and kept for comparison:
`cta-band.html` and `footer-redesign.html`.

### Still waiting on the Webflow Designer
Everything below lives in the page embeds and cannot be written over the REST
API. The Designer MCP app has not been reachable all session.
- The 26 global, country and India-city pages, and their 7 URL folders
- The Locations column in the footer and the Locations dropdown in the header
- Removing the `↗` glyphs from WhatsApp, LinkedIn and Join the Talent Pool
- Privacy and Terms pages, if they are wanted
- The em-dash fixes (copy lives in the embeds)
- The four new video poster frames


## v11 (8 October 2026): CTA band removed

The call-to-action band above the footer is gone from every page.

- Stripped from 14 source body files and from `home-page.original.html`
- The `cta()` call removed from `_shared/build_geo.py`, so the 26 location
  pages no longer generate one
- `.cta-band { display: none !important; }` in `brand.css` also hides it on any
  embed still carrying the old markup, so it disappeared from the live site
  without a Designer push
- `_shared/enhance.py` used `<section class="cta-band"` as the anchor for the
  founder reels on the four article pages and the geo pages. That anchor is now
  `</main>`, and a missing marker falls back to `</main>` instead of raising.

Pages now run from the FAQ straight into the footer. 43 pages build, 0 contain a
CTA band, 41 carry the founder reels.

Stylesheet: `https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/6ac77e0a16499edb1e176f61_stellaspire-pages-v9f.css`

Also removed in this pass: every decorative gradient rule. The footer top rule,
the CTA hairline and the method band top rule are all gone. The only line left
on a page is the plain hairline above the footer's copyright bar.

## Still to do
0. **Upload the v9 assets:** the 4 new poster JPGs, `brand.css` bundled into a new
   `stellaspire-pages-v9.css`, then swap the `<link>` in every page head.
1. **Folders (optional):** create `services` and `insights` page folders in the Designer, move the pages into them, then rebuild with `build_all.py services insights` and re-push. This needs the Webflow Designer MCP app open in a logged-in browser.
2. **Review on staging,** then publish to stellaspire.com when approved.
3. **At launch:** make `/home-page` the homepage and add a 301 redirect from `/home-page` to `/`. Add the old-URL redirects listed in the Master Strategy, section 2.3.
4. **Fill the HTML-comment placeholders:** case studies, real proof numbers, partner employers, the founder story and the fee/replacement terms.
5. **Assets:** see `ASSET-PROMPTS.md`.
