"""Apply the home-page updates to the original embed and write out/home-page.html."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
s = (root / "home-page.original.html").read_text(encoding="utf-8")
hdr = (root / "_shared/header.html").read_text(encoding="utf-8").strip()
ftr = (root / "_shared/footer.html").read_text(encoding="utf-8").strip()


def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)


# Shared header and footer
a = s.find('<a class="skip-link"')
b = s.find("</header>") + len("</header>")
s = s[:a] + hdr + s[b:]
s = s[: s.find("<!-- ============ FOOTER ============ -->")] + ftr

# Expertise rows link to the new service pages
rep('<a class="row-arrow" href="#hire-talent" aria-label="Discuss Finance &amp; Leadership hiring">',
    '<a class="row-arrow" href="/finance-accounting-recruitment" aria-label="Explore Finance &amp; Leadership hiring">')
rep('<a class="row-arrow" href="#hire-talent" aria-label="Discuss Data &amp; Analytics hiring">',
    '<a class="row-arrow" href="/analytics-data-recruitment" aria-label="Explore Data &amp; Analytics hiring">')
rep('<a class="row-arrow" href="#hire-talent" aria-label="Discuss GCC hiring">',
    '<a class="row-arrow" href="/gcc-hiring" aria-label="Explore GCC hiring">')
row_close = s.find("</div>", s.find('aria-label="Explore GCC hiring"')) + len("</div>")
chips = """
      <div class="chips" style="padding-top:30px;border-top:1px solid var(--line)" aria-label="More services">
        <a class="chip" href="/cfo-executive-search">CFO &amp; Executive Search →</a>
        <a class="chip" href="/ai-ml-recruitment">AI &amp; ML →</a>
        <a class="chip" href="/diversity-hiring">Gender-Diversity Hiring →</a>
        <a class="chip" href="/women-returnship">Women Returnship →</a>
      </div>"""
s = s[:row_close] + chips + s[row_close:]

# Method band, founder block
rep('<a class="light-link" href="#approach">Explore our approach',
    '<a class="light-link" href="/how-we-work">Explore our approach')
rep('<a class="textlink" href="https://www.linkedin.com/in/nikitaagrawal18/"',
    '<div class="candidate-actions"><a class="textlink" href="/about">About Stellaspire <span aria-hidden="true">→</span></a>\n        '
    '<a class="textlink" href="https://www.linkedin.com/in/nikitaagrawal18/"')
j = s.find("</a>", s.find("Meet Nikita on LinkedIn")) + 4
s = s[:j] + "</div>" + s[j:]

# Candidates
k = s.find("</div>", s.find('href="https://recruitcrm.io/jobs/Stellaspire"', s.find('id="candidates"')))
s = s[:k] + '  <a class="textlink" href="/women-returnship">Women Returnship <span aria-hidden="true">→</span></a>\n        ' + s[k:]
rep('<p class="small-note">Both links open Recruit CRM in a new tab.</p>',
    '<p class="small-note">Talent Pool and Active Opportunities open Recruit CRM in a new tab.</p>')

# Insights
rep('href="https://www.stellaspire.com/blogs">View All Insights', 'href="/insights">View All Insights')
s = s.replace("https://www.stellaspire.com/post/", "/post/")
last = s.rfind("</article>", 0, s.find("<!-- ============ FAQ")) + len("</article>")
s = s[:last] + """
          <article class="support-row">
            <p class="eyebrow">GCC hiring</p>
            <h3 class="support-title"><a class="article-link" href="/gcc-hiring-guide-india">GCC Hiring in India: The Complete 2026 Guide <span aria-hidden="true">↗</span></a></h3>
          </article>""" + s[last:]

# Enquiry form: Webflow-processed structure
f0 = s.find("<!-- TODO: this form has no backend")
f1 = s.find("</form>", f0) + len("</form>")
form = """<!-- Webflow processes this embedded form (w-form structure). Test a submission after publishing. -->
      <div class="w-form">
      <form id="wf-form-Home-Hiring-Brief" name="wf-form-Home-Hiring-Brief" data-name="Home Hiring Brief" method="get" data-wf-page-id="6ac49970030703da9979c2e7" data-wf-element-id="580e6e1b-956d-76a0-604b-7087ec54f99d">
        <label class="field-label" for="name">Your name *</label>
        <input class="field" id="name" name="Name" data-name="Name" type="text" maxlength="256" autocomplete="name" required>

        <label class="field-label" for="email">Work email *</label>
        <input class="field" id="email" name="Email" data-name="Email" type="email" maxlength="256" autocomplete="email" required>

        <label class="field-label" for="company">Company *</label>
        <input class="field" id="company" name="Company" data-name="Company" type="text" maxlength="256" autocomplete="organization" required>

        <label class="field-label" for="need">Hiring need *</label>
        <textarea class="field" id="need" name="Hiring-Need" data-name="Hiring Need" maxlength="5000" rows="4" placeholder="Role, team context and what you are looking for" required></textarea>

        <label class="field-label" for="phone">Phone <span class="optional">(optional)</span></label>
        <input class="field" id="phone" name="Phone" data-name="Phone" type="tel" maxlength="256" autocomplete="tel">

        <label class="field-label" for="interest">Service interest <span class="optional">(optional)</span></label>
        <select class="field" id="interest" name="Service-Interest" data-name="Service Interest">
          <option value="">Select a service</option>
          <option>Finance &amp; Accounting</option>
          <option>CFO &amp; Executive Search</option>
          <option>GCC Hiring</option>
          <option>Analytics &amp; Data</option>
          <option>AI &amp; ML</option>
          <option>Gender-Diversity Hiring</option>
          <option>Women Returnship</option>
          <option>Other</option>
        </select>

        <input class="button" type="submit" value="Send Hiring Brief" data-wait="Sending...">
      </form>
      <div class="w-form-done" tabindex="-1" role="region" aria-label="Form success"><div>Thank you. We have your brief and will reply shortly.</div></div>
      <div class="w-form-fail" tabindex="-1" role="region" aria-label="Form failure"><div>Something went wrong. Please email connect@stellaspire.com.</div></div>
      </div>"""
s = s[:f0] + form + s[f1:]

# Organization + WebSite schema
schema = """<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
{"@type":"EmploymentAgency","@id":"https://www.stellaspire.com/#org","name":"Stellaspire","url":"https://www.stellaspire.com/","logo":"https://cdn.prod.website-files.com/66a5fdf6d0c2ac84ca88fe93/6886351f114ee66a92aad258_WhatsApp-Image-2025-05-07-at-14.24.03.jpeg","email":"connect@stellaspire.com","slogan":"We take hiring personally.","founder":{"@type":"Person","name":"Nikita Agrawal","jobTitle":"Founder & CEO","sameAs":"https://www.linkedin.com/in/nikitaagrawal18/"},"address":{"@type":"PostalAddress","streetAddress":"WeWork Prestige Central, 36 Infantry Road","addressLocality":"Bengaluru","addressRegion":"Karnataka","postalCode":"560001","addressCountry":"IN"},"areaServed":"IN","sameAs":["https://www.linkedin.com/company/stellaspire/"]},
{"@type":"WebSite","url":"https://www.stellaspire.com/","name":"Stellaspire","publisher":{"@id":"https://www.stellaspire.com/#org"}}
]}
</script>
</main>"""
s = s.replace("</main>", schema, 1)

(root / "out/home-page.html").write_text(s, encoding="utf-8")
print(len(s), "chars;", s.count("<h1"), "h1")
