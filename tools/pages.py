"""Page builders. Each returns a page dict for lib.layout()."""
from lib import (CONFIG, e, picture, icon, img_url, abs_url, btn_appraisal, btn_call, cta_pair,
                 cta_band, breadcrumbs_html, breadcrumb_schema, faq_html, faq_schema,
                 service_schema, org_ref, note_placeholder, AREAS)
import content as C


def booking_url(home):
    return home["booking_url"].replace("{BOOKING_BASE}", CONFIG["BOOKING_BASE"].rstrip("/"))


def sample_flag(item, what):
    if item.get("placeholder"):
        note_placeholder(what)
        return '<span class="sample-flag">Sample</span>' if CONFIG["STAGING"] else ""
    return ""


# ===========================================================================
# Reusable modules
# ===========================================================================
PILLARS = [
    ("care", "Property Care", "Hotel-standard housekeeping, regular inspections and maintenance handled before it becomes a problem. Your home stays as good as the day it was photographed.", "/services/property-care/"),
    ("performance", "Performance", "Dynamic pricing, revenue management and distribution across the channels that matter, overseen by people who know the local market.", "/services/performance/"),
    ("representation", "Representation", "Professional photography, considered listing copy and presentation that does justice to your home and attracts the right guests.", "/services/#representation"),
    ("freedom", "Freedom", "We take on the guests, the changeovers and the contractors. You keep the income and the ownership, without the day-to-day.", "/services/#freedom"),
]


def pillars_html(links=True):
    out = ['<div class="pillars">']
    for ic, title, text, href in PILLARS:
        link = f'<a class="link-arrow" href="{href}">Learn more<span class="visually-hidden"> about {title}</span></a>' if links else ""
        out.append(f'<div class="pillar reveal">{icon(ic, "pillar__icon")}<h3>{title}</h3><p>{text}</p>{link}</div>')
    out.append("</div>")
    return "".join(out)


def testimonials_html(context, limit=3):
    items = [t for t in C.TESTIMONIALS if context in t["contexts"]][:limit]
    if not items:
        return ""
    out = ['<div class="testimonials">']
    for t in items:
        flag = sample_flag(t, "Owner testimonials")
        out.append(f'''<figure class="quote reveal"><div class="quote__mark" aria-hidden="true">&ldquo;</div>
<blockquote><p class="mb-0">{e(t["quote"])}</p></blockquote>
<figcaption>{e(t["name"])}, {e(t["detail"])}{flag}</figcaption></figure>''')
    out.append("</div>")
    return "".join(out)


def testimonials_section(context, heading="What owners say", tint=True):
    block = testimonials_html(context)
    if not block:
        return ""
    return f'''<section class="section {'section--tint' if tint else ''}" aria-labelledby="t-{context}">
<div class="wrap"><div class="section-head"><span class="eyebrow">Owner stories</span><h2 id="t-{context}">{heading}</h2></div>{block}</div></section>'''


def case_feature_html(cs, heading_level="h3"):
    flag = sample_flag(cs, "Case studies and their figures")
    stats = "".join(f"<div><strong>{e(v)}</strong><span>{e(l)}</span></div>" for v, l in cs["stats"])
    return f'''<article class="case-feature reveal">
<div class="case-feature__media">{picture(cs["image"], "", "(max-width: 860px) 100vw, 50vw")}</div>
<div class="case-feature__body">
<span class="eyebrow">Case study · {e(cs["service"])}{flag}</span>
<{heading_level}>{e(cs["title"])}</{heading_level}>
<p class="muted">{e(cs["short"])}</p>
<div class="case-stats">{stats}</div>
<a class="link-arrow" href="/case-studies/{cs["slug"]}/">Read the case study</a>
</div></article>'''


def case_section(context, tint=False):
    cs = next((c for c in C.CASE_STUDIES if context in c["contexts"]), None)
    if not cs:
        return ""
    return f'''<section class="section {'section--tint' if tint else ''}" aria-label="Case study"><div class="wrap">
<div class="section-head section-head--row"><div><span class="eyebrow">Owner success</span><h2>Results that speak for themselves</h2></div>
<a class="link-arrow" href="/case-studies/">All case studies</a></div>
{case_feature_html(cs)}</div></section>'''


def home_card(h, sizes="(max-width: 640px) 100vw, (max-width: 1000px) 50vw, 33vw"):
    sample_flag(h, "Properties on Our Homes (names, details, photos, booking links)")
    cats = " ".join(h["categories"])
    badge = '<span class="home-card__badge">Featured</span>' if h.get("featured") else ""
    return f'''<a class="home-card reveal" href="/our-homes/{h["slug"]}/" data-cats="{cats}">
<div class="home-card__media">{picture(h["images"][0], "", sizes)}{badge}</div>
<div class="home-card__loc">{e(h["location"])}</div>
<h3>{e(h["name"])}</h3>
<div class="home-card__meta"><span>Sleeps {h["sleeps"]}</span><span>{h["bedrooms"]} bedroom{'s' if h["bedrooms"] != 1 else ''}</span><span>{e(h["dogs"])}</span></div>
</a>'''


def steps_html(steps, dark=False):
    out = ['<ol class="steps">']
    for t, d in steps:
        out.append(f'<li class="step reveal"><h3>{t}</h3><p>{d}</p></li>')
    out.append("</ol>")
    return "".join(out)


STEPS = [
    ("Request an appraisal", "Tell us about your home. It takes a couple of minutes, and there's no obligation."),
    ("Talk it through", "We'll be in touch within 48 hours to understand your goals and, where it helps, visit the property."),
    ("Your proposal", "A clear recommendation on the right service, what your home could achieve and how we'd present it."),
    ("Launch and beyond", "We prepare, photograph and list your home, then look after everything from the first booking on."),
]


def article_card(a):
    sample_flag(a, "Journal articles")
    return f'''<a class="article-card reveal" href="/journal/{a["slug"]}/">
{picture(a["image"], "", "(max-width: 640px) 100vw, 33vw")}
<span class="article-card__cat">{C.JOURNAL_CATEGORIES[a["category"]]}</span>
<h3>{e(a["title"])}</h3><p>{e(a["excerpt"])}</p></a>'''


FULL_LIST = ["Guest communication, check-in and support", "Housekeeping, linen and changeovers", "Inspections and maintenance coordination", "Pricing, revenue and distribution", "Photography and listing management", "Clear monthly owner statements"]
BRM_LIST = ["Pricing strategy and dynamic rates", "Listing creation and optimisation", "Channel and calendar management", "Guest enquiries and booking communication", "Performance reporting"]


def services_cards(location):
    full = "".join(f"<li>{x}</li>" for x in FULL_LIST)
    brm = "".join(f"<li>{x}</li>" for x in BRM_LIST)
    return f'''<div class="grid grid--2">
<div class="service-card service-card--flagship reveal"><span class="tag">Our flagship service</span>
<h3>Full Management</h3><p>Everything handled, so your home earns while you get on with life. We look after the guests, the property and the numbers.</p>
<ul class="checklist">{full}</ul>
<div class="btn-row">{btn_appraisal(location + "_full", "light", "Request an appraisal", "full-management")}<a class="link-arrow" href="/services/full-management/">Explore Full Management</a></div></div>
<div class="service-card reveal"><span class="tag">For hands-on owners</span>
<h3>Bookings &amp; Revenue Management</h3><p>You look after the home; we fill the calendar at the right price. Ideal for owners who live nearby and have housekeeping in place.</p>
<ul class="checklist">{brm}</ul>
<div class="btn-row">{btn_appraisal(location + "_brm", "outline", "Request an appraisal", "bookings-revenue-management")}<a class="link-arrow" href="/services/bookings-revenue-management/">Explore Bookings &amp; Revenue</a></div></div>
</div>'''


def areas_html():
    return '''<div class="areas">
<div class="area"><span class="area__tag">Our home ground</span><h3>Peak District</h3><p>The Hope Valley, Edale, Castleton, Bakewell and the villages in between. We know its seasons, its events and the guests it draws.</p></div>
<div class="area"><span class="area__tag">Also covering</span><h3>Derbyshire</h3><p>From the Derbyshire Dales to the market towns and countryside around the edge of the National Park.</p></div>
<div class="area"><span class="area__tag">Also covering</span><h3>South Yorkshire</h3><p>Sheffield's western fringe and the countryside that rolls into the Peak, a short hop for city-break and walking guests alike.</p></div>
</div>'''


def local_section():
    return f'''<section class="section section--dark dark" aria-labelledby="local-h">
<div class="wrap"><div class="split split--reverse" style="margin-bottom:clamp(48px,6vw,80px)">
<div class="split__media split__media--landscape">{picture("hills", "Rolling green hills above a village of stone houses and slate roofs", "(max-width: 860px) 100vw, 50vw")}</div>
<div><span class="eyebrow">Local expertise</span><h2 id="local-h">We know these hills, villages and the guests who love them</h2>
<p class="lede">Local knowledge shapes everything we do: when to raise prices, which weekends sell out first, which trades turn up on a Sunday, and what guests want from a stay in the Peak.</p>
<a class="link-arrow" href="/about/">About Staycay</a></div></div>
{areas_html()}</div></section>'''


OWNER_FAQS = [
    ("How much does Staycay charge?", "Our fees depend on the service you choose, the property and what's involved in looking after it, so we don't publish a one-size-fits-all rate. After your appraisal we'll give you a clear proposal with nothing hidden."),
    ("My home is already listed on Airbnb or Booking.com. Can you take it on?", "Yes. Many owners come to us with an existing listing. We'll review how it's performing today and talk you through how we'd take it on."),
    ("Can I still use my home myself?", "Of course. You can keep dates for your own stays, and we'll talk through how to plan them around the busiest periods."),
    ("Which areas do you cover?", "We specialise in the Peak District, and also manage homes across Derbyshire and South Yorkshire. If you're just outside these areas, ask us anyway."),
    ("Do you take on homes that aren't holiday lets yet?", "Yes. We can help you get a home ready to let, from presentation and photography to setting up listings and pricing."),
    ("Do you take every property?", "No. We focus on high-quality homes we're confident we can do justice to, which is how we keep standards high for owners and guests."),
]


# ===========================================================================
# HOME
# ===========================================================================
def page_home():
    featured = [h for h in C.HOMES if h.get("featured")][:3]
    articles = C.ARTICLES[:3]
    body = f'''
<section class="hero" aria-labelledby="hero-h">
  <div class="hero__media">{picture("hero", "A row of honey-coloured stone cottages with stone-tiled roofs along a cobbled lane", "100vw", eager=True)}</div>
  <div class="wrap hero__content">
    <span class="eyebrow">Holiday home management · Peak District</span>
    <h1 id="hero-h">Exceptional homes. <em>Exceptionally managed.</em></h1>
    <p class="lede">Staycay is a specialist manager of high-quality holiday homes across the Peak District, Derbyshire and South Yorkshire. We look after the home, the guests and the numbers, so your property performs as it should and you get your time back.</p>
    {cta_pair("home_hero", dark=True)}
    <p class="hero__guest">Planning a stay? <a href="/our-homes/" data-track="guest_route" data-track-location="home_hero">Explore our homes</a></p>
  </div>
</section>

<section class="trust" aria-label="Staycay at a glance">
  <div class="wrap trust__grid">
    <div class="trust__item"><div class="trust__num">75+</div><div class="trust__label">holiday homes in our care</div></div>
    <div class="trust__item"><div class="trust__num">3 years</div><div class="trust__label">managing homes across the region</div></div>
    <div class="trust__item"><div class="trust__num">48 hrs</div><div class="trust__label">to respond to every appraisal request</div></div>
    <div class="trust__item"><div class="trust__num">Local</div><div class="trust__label">Peak District, Derbyshire and South Yorkshire</div></div>
  </div>
</section>

<section class="section" aria-labelledby="intro-h">
  <div class="wrap split">
    <div class="split__media reveal">{picture("armchair", "A sunlit cottage sitting room with a checked armchair, panelled walls and a window onto the garden", "(max-width: 860px) 100vw, 50vw")}{picture("lamp", "", "25vw", cls="inset")}</div>
    <div class="reveal">
      <span class="eyebrow">A specialist, not a generalist</span>
      <h2 id="intro-h">Looking after the Peak District's finest holiday homes</h2>
      <p class="lede">We don't try to manage everything. We focus on characterful, well-kept homes in one of Britain's best-loved landscapes, and look after each one as if it were our own.</p>
      <p>That focus means sharper pricing, higher standards and guests who come back year after year. It also means owners deal with a team that knows their home, rather than a call centre.</p>
      <div class="btn-row" style="margin-top:28px">{btn_appraisal("home_intro")}<a class="link-arrow" href="/for-owners/">Why owners choose us</a></div>
    </div>
  </div>
</section>

<section class="section section--tint" aria-labelledby="pillars-h">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">How we look after your home</span><h2 id="pillars-h">Four promises behind every home we manage</h2></div>
    {pillars_html()}
  </div>
</section>

<section class="section" aria-labelledby="services-h">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Our services</span><h2 id="services-h">Two ways to work with us</h2><p class="lede">Most owners choose Full Management. If you'd rather keep looking after the home yourself, our Bookings &amp; Revenue service handles the commercial side.</p></div>
    {services_cards("home_services")}
  </div>
</section>

<section class="section section--dark dark" aria-labelledby="how-h">
  <div class="wrap">
    <div class="section-head section-head--row"><div><span class="eyebrow">How it works</span><h2 id="how-h">From first conversation to first booking</h2></div><a class="link-arrow" href="/how-it-works/">Our approach</a></div>
    {steps_html(STEPS)}
  </div>
</section>

{case_section("home")}

<section class="section section--tint" aria-labelledby="homes-h">
  <div class="wrap">
    <div class="section-head section-head--row"><div><span class="eyebrow">For guests</span><h2 id="homes-h">A curated collection of places to stay</h2><p class="lede">Chosen for character, comfort and setting, and cared for to the same standard.</p></div><a class="link-arrow" href="/our-homes/" data-track="guest_route" data-track-location="home_collection">View all homes</a></div>
    <div class="grid grid--3">{"".join(home_card(h) for h in featured)}</div>
  </div>
</section>

{testimonials_section("home", tint=False)}

{local_section()}

<section class="section" aria-labelledby="journal-h">
  <div class="wrap">
    <div class="section-head section-head--row"><div><span class="eyebrow">Journal</span><h2 id="journal-h">Notes for owners and guests</h2></div><a class="link-arrow" href="/journal/">Read the Journal</a></div>
    <div class="grid grid--3">{"".join(article_card(a) for a in articles)}</div>
  </div>
</section>

{cta_band(location="home_final")}
'''
    schema = [
        {"@context": "https://schema.org", "@type": "Organization", "name": CONFIG["BRAND"], "url": CONFIG["SITE_URL"] + "/",
         "slogan": CONFIG["TAGLINE"], "email": CONFIG["ENQUIRY_EMAIL"],
         "description": "Specialist manager of high-quality holiday homes in the Peak District, Derbyshire and South Yorkshire.",
         "areaServed": [{"@type": "Place", "name": a} for a in AREAS]},
        {"@context": "https://schema.org", "@type": "WebSite", "name": CONFIG["BRAND"], "url": CONFIG["SITE_URL"] + "/"},
    ]
    return {"path": "/", "title": "Holiday Home Management in the Peak District | Staycay Management",
            "description": "Specialist holiday let management for high-quality homes across the Peak District, Derbyshire and South Yorkshire. Request a free property appraisal.",
            "body": body, "overlay": True, "schema": schema}


# ===========================================================================
# FOR OWNERS
# ===========================================================================
def compare_table():
    rows = [
        ("Pricing strategy and dynamic rates", True, True),
        ("Listing creation, optimisation and distribution", True, True),
        ("Guest enquiries and booking communication", True, True),
        ("Performance reporting", True, True),
        ("Guest support during the stay", True, False),
        ("Housekeeping, linen and changeovers", True, False),
        ("Inspections and maintenance coordination", True, False),
        ("Professional photography and presentation", True, False),
        ("Monthly owner statements", True, False),
    ]
    tick = '<span class="yes" role="img" aria-label="Included"></span>'
    dash = '<span class="no" role="img" aria-label="Not included"></span>'
    body = "".join(f"<tr><th scope=\"row\">{r}</th><td>{tick if a else dash}</td><td>{tick if b else dash}</td></tr>" for r, a, b in rows)
    return f'''<div class="compare-wrap"><table class="compare"><caption class="visually-hidden">What's included in each service</caption>
<thead><tr><th scope="col"><span class="visually-hidden">Service</span></th><th scope="col">Full Management</th><th scope="col">Bookings &amp; Revenue</th></tr></thead>
<tbody>{body}</tbody></table></div>'''


def page_owners():
    crumbs = [("Home", "/"), ("For Owners", "/for-owners/")]
    fit = ["You own a high-quality home in the Peak District, Derbyshire or South Yorkshire", "You want strong returns without running it yourself", "You care about how your home is presented and looked after", "You're tired of managing guests, cleaners and calendars from a distance", "You're new to holiday letting and want to get it right from the start"]
    body = f'''
<section class="page-hero page-hero--split">
  <div class="wrap">
    <div>{breadcrumbs_html(crumbs)}
      <span class="eyebrow">For owners</span>
      <h1>Your holiday home, looked after properly</h1>
      <p class="lede">Whether you already let your home or you're thinking about it for the first time, we take care of the work and the detail, so it performs well and stays in excellent condition.</p>
      {cta_pair("owners_hero")}
    </div>
    <div class="page-hero__media">{picture("roses", "Climbing roses around a leaded window in an old stone cottage wall", "(max-width: 860px) 100vw, 45vw", eager=True)}</div>
  </div>
</section>

<section class="section section--tint" aria-labelledby="fit-h">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Is Staycay right for you?</span><h2 id="fit-h">We work best with owners who care about their homes as much as we do</h2>
      <p class="lede">Our owners range from families with a much-loved second home to investors with several properties. What they share is a home worth showing off, and a wish for it to be run well.</p></div>
    <div class="reveal"><ul class="checklist">{"".join(f"<li>{x}</li>" for x in fit)}</ul></div>
  </div>
</section>

<section class="section" aria-labelledby="pillars-h">
  <div class="wrap"><div class="section-head"><span class="eyebrow">What you can expect</span><h2 id="pillars-h">Four promises behind every home we manage</h2></div>{pillars_html()}</div>
</section>

<section class="section section--tint" aria-labelledby="compare-h">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Choosing a service</span><h2 id="compare-h">Full Management or Bookings &amp; Revenue?</h2><p class="lede">Full Management is our flagship service and the right choice for most owners. Bookings &amp; Revenue suits owners who want to keep looking after the home themselves.</p></div>
    {compare_table()}
    <div class="btn-row mt-l"><a class="link-arrow" href="/services/full-management/">Full Management</a><a class="link-arrow" href="/services/bookings-revenue-management/">Bookings &amp; Revenue Management</a></div>
  </div>
</section>

<section class="section section--dark dark" aria-labelledby="how-h">
  <div class="wrap"><div class="section-head section-head--row"><div><span class="eyebrow">How it works</span><h2 id="how-h">Four simple steps</h2></div><a class="link-arrow" href="/how-it-works/">Our approach in detail</a></div>{steps_html(STEPS)}</div>
</section>

{case_section("owners")}
{testimonials_section("owners")}

<section class="section" aria-labelledby="faq-h">
  <div class="wrap wrap--narrow"><div class="section-head"><span class="eyebrow">Questions</span><h2 id="faq-h">Owner questions, answered</h2></div>{faq_html(OWNER_FAQS)}</div>
</section>

{cta_band(location="owners_final")}
'''
    return {"path": "/for-owners/", "title": "For Holiday Home Owners | Staycay Management",
            "description": "Holiday let management for owners in the Peak District, Derbyshire and South Yorkshire. Full Management or Bookings & Revenue support. Request an appraisal.",
            "body": body, "schema": [breadcrumb_schema(crumbs), faq_schema(OWNER_FAQS)]}


# ===========================================================================
# SERVICES HUB + SERVICE PAGES
# ===========================================================================
def page_services():
    crumbs = [("Home", "/"), ("Services", "/services/")]
    sections = [
        ("property-care", "care", "Property Care", "Standards you can see, every stay", "Your home is your asset and our reputation. We set clear housekeeping standards, inspect regularly and coordinate maintenance quickly, using trusted local trades.", ["Hotel-standard housekeeping and linen", "Regular property inspections", "Planned and reactive maintenance coordination", "Restocking and guest essentials"], "/services/property-care/", "castlecombe-wide", "A row of well-kept stone cottages on a cobbled lane"),
        ("performance", "performance", "Performance", "Pricing and revenue, managed properly", "We price every night individually against local demand, keep your home visible on the channels that matter, and report clearly on how it's performing.", ["Dynamic pricing and minimum-stay strategy", "Distribution across the right channels", "Calendar and availability management", "Clear performance reporting"], "/services/performance/", "flint-cottage", "A flint and brick cottage with a lavender-filled front garden on a sunny day"),
        ("representation", "representation", "Representation", "Presented as it deserves to be", "Guests choose with their eyes. We arrange professional photography, write listing copy that captures what makes your home special, and advise on the details that make a stay memorable.", ["Professional photography", "Listing copy and presentation", "Styling and guest-experience advice", "Inclusion in our curated collection where it fits"], None, "roses", "Climbing roses around a leaded window in an old stone cottage wall"),
        ("freedom", "freedom", "Freedom", "All of the reward, none of the running around", "Guest messages at midnight, changeovers on a bank holiday, a boiler on a Sunday. We handle it, so owning a holiday home feels like owning a holiday home again.", ["One point of contact who knows your home", "Guest communication around the clock", "Owner stays planned around peak periods", "Monthly statements without the admin"], None, "farm-autumn", "A flint and brick farmhouse among autumn trees, behind a meadow of wildflowers"),
    ]
    blocks = []
    for i, (anchor, ic, title, h, text, items, href, img, alt) in enumerate(sections):
        rev = " split--reverse" if i % 2 else ""
        tint = " section--tint" if i % 2 == 0 else ""
        more = f'<a class="link-arrow" href="{href}">More about {title}</a>' if href else ""
        blocks.append(f'''<section class="section{tint}" id="{anchor}" aria-labelledby="{anchor}-h"><div class="wrap split{rev}">
<div class="split__media split__media--landscape reveal">{picture(img, alt, "(max-width: 860px) 100vw, 50vw")}</div>
<div class="reveal">{icon(ic, "pillar__icon")}<span class="eyebrow" style="display:block">{title}</span><h2 id="{anchor}-h">{h}</h2><p class="lede">{text}</p>
<ul class="checklist">{"".join(f"<li>{x}</li>" for x in items)}</ul>{more}</div></div></section>''')
    body = f'''
<section class="page-hero">
  <div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">Services</span><h1>Management built around your home</h1>
  <p class="lede">Two services, one standard. Choose complete peace of mind with Full Management, or keep the hands-on side yourself with Bookings &amp; Revenue Management.</p></div>
</section>
<section class="section" style="padding-top:0" aria-label="Our services"><div class="wrap">{services_cards("services_hub")}</div></section>
<section class="section section--dark dark" aria-labelledby="pillars-h"><div class="wrap"><div class="section-head"><span class="eyebrow">The Staycay standard</span><h2 id="pillars-h">Four pillars, applied to every home</h2></div>{pillars_html(links=False)}</div></section>
{"".join(blocks)}
{cta_band(location="services_final")}
'''
    return {"path": "/services/", "title": "Holiday Let Management Services | Staycay Management",
            "description": "Full Management and Bookings & Revenue Management for holiday homes in the Peak District, Derbyshire and South Yorkshire. Property care, pricing, presentation.",
            "body": body, "schema": [breadcrumb_schema(crumbs)]}


def service_page(slug, name, title, desc, h1, lede, hero_img, hero_alt, groups, who, faqs, context, service_key, extra=""):
    path = f"/services/{slug}/"
    crumbs = [("Home", "/"), ("Services", "/services/"), (name, path)]
    group_html = "".join(f'<div class="reveal"><h3>{g}</h3><ul class="checklist">{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for g, items in groups)
    body = f'''
<section class="page-hero page-hero--image">
  <div class="hero__media">{picture(hero_img, hero_alt, "100vw", eager=True)}</div>
  <div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">{name}</span><h1>{h1}</h1><p class="lede">{lede}</p>{cta_pair(slug + "_hero", dark=True, service=service_key)}</div>
</section>
<section class="section" aria-labelledby="inc-h"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What's included</span><h2 id="inc-h">Everything you'd expect, done properly</h2></div>
  <div class="grid grid--{len(groups) if len(groups) < 4 else 2}">{group_html}</div>
</div></section>
<section class="section section--tint" aria-labelledby="who-h"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">Who it's for</span><h2 id="who-h">{who[0]}</h2><p class="lede">{who[1]}</p></div>
  <div class="reveal"><ul class="checklist">{"".join(f"<li>{x}</li>" for x in who[2])}</ul></div>
</div></section>
{extra}
<section class="section section--dark dark" aria-labelledby="how-h"><div class="wrap"><div class="section-head"><span class="eyebrow">Getting started</span><h2 id="how-h">How it works</h2></div>{steps_html(STEPS)}</div></section>
{case_section(context)}
{testimonials_section(context)}
<section class="section" aria-labelledby="faq-h"><div class="wrap wrap--narrow"><div class="section-head"><span class="eyebrow">Questions</span><h2 id="faq-h">{name}: your questions</h2></div>{faq_html(faqs)}</div></section>
{cta_band(location=slug + "_final", service=service_key)}
'''
    return {"path": path, "title": title, "description": desc, "body": body,
            "schema": [breadcrumb_schema(crumbs), service_schema(name, desc, path), faq_schema(faqs)]}


def page_full_management():
    return service_page(
        "full-management", "Full Management",
        "Full Holiday Let Management, Peak District | Staycay Management",
        "Complete holiday home management in the Peak District, Derbyshire and South Yorkshire: guests, housekeeping, maintenance, pricing and reporting, all handled.",
        "Full Management: everything handled",
        "Our flagship service. We look after the guests, the home and the numbers, so your property performs as it should without taking over your life.",
        "armchair-wide", "A sunlit cottage sitting room with a checked armchair and a window onto the garden",
        [("Guests", ["Enquiries, bookings and arrival information", "Guest support throughout the stay", "Reviews and follow-up"]),
         ("Your home", ["Housekeeping, linen and changeovers", "Regular inspections", "Maintenance with trusted local trades"]),
         ("Revenue", ["Dynamic pricing against local demand", "Distribution across the right channels", "Professional photography and listing"]),
         ("Reporting", ["Monthly owner statements", "Clear performance updates", "One point of contact who knows your home"])],
        ("Owners who want the reward without the running around", "Full Management is for owners who want their home run to a high standard and their time back, whether they live down the road or the other side of the world.",
         ["You live some distance from the property", "You don't want to be on call for guests and contractors", "You want consistent standards without checking them yourself", "You see your home as an investment and want it run like one"]),
        [("What does Full Management cost?", "Fees depend on the property and what's involved in looking after it. We'll set everything out clearly in your proposal after the appraisal."),
         ("Who looks after housekeeping?", "We organise and check housekeeping, linen and changeovers to our standards, so every guest arrives to the same experience."),
         ("Can I keep dates for myself?", "Yes. Owner stays are easy to arrange, and we'll help you plan them around the busiest periods."),
         ("How do I know how my home is performing?", "You'll receive clear monthly statements and can speak to your point of contact at any time.")],
        "full-management", "full-management")


def page_brm():
    return service_page(
        "bookings-revenue-management", "Bookings & Revenue Management",
        "Holiday Let Bookings & Revenue Management | Staycay Management",
        "Expert pricing, listings and bookings for holiday homes in the Peak District, Derbyshire and South Yorkshire, for owners who look after the home themselves.",
        "Bookings &amp; Revenue Management",
        "You look after the home and the welcome. We handle pricing, listings and bookings, so your calendar is fuller and every night is priced right.",
        "castlecombe-wide", "A row of well-kept stone cottages on a cobbled lane",
        [("Pricing", ["Dynamic nightly rates", "Seasonal and event-led strategy", "Minimum-stay rules to close gaps"]),
         ("Listings &amp; distribution", ["Listing creation and optimisation", "Channel and calendar management", "Presentation advice"]),
         ("Bookings &amp; reporting", ["Guest enquiries and booking communication", "Performance reporting", "Regular strategy reviews"])],
        ("Owners who enjoy the hands-on side", "Bookings &amp; Revenue Management suits owners who live nearby, have reliable housekeeping and enjoy welcoming guests, but want expert help with the commercial side.",
         ["You live near the property", "You already have housekeeping in place", "You want more bookings at better rates", "You'd like the option to move to Full Management later"]),
        [("What's the difference from Full Management?", "With Bookings &amp; Revenue Management you keep responsibility for housekeeping, maintenance and guests during their stay. We handle pricing, listings, distribution and bookings."),
         ("Can I switch to Full Management later?", "Yes. Many owners start with one service and move to the other as their circumstances change."),
         ("Which booking channels do you use?", "We'll recommend the right mix for your home during the appraisal, including Staycay's own direct-booking site.")],
        "bookings-revenue", "bookings-revenue-management")


def page_property_care():
    path = "/services/property-care/"
    crumbs = [("Home", "/"), ("Services", "/services/"), ("Property Care", path)]
    desc = "Holiday home housekeeping, inspections and maintenance in the Peak District, Derbyshire and South Yorkshire. High standards, local trades, every stay."
    faqs = [("How often do you inspect properties?", "Every home is checked at each changeover, with regular, more detailed inspections through the year. We'll agree the schedule with you."),
            ("Who carries out maintenance?", "We work with trusted local trades and keep you informed. You stay in control of significant decisions and spend.")]
    body = f'''
<section class="page-hero page-hero--split"><div class="wrap">
  <div>{breadcrumbs_html(crumbs)}<span class="eyebrow">Property Care</span><h1>Standards you can see, every stay</h1>
  <p class="lede">Your home is your asset, and our reputation. We look after it with clear standards, regular inspections and maintenance handled before small things become big ones.</p>{cta_pair("care_hero", service="full-management")}</div>
  <div class="page-hero__media">{picture("lamp", "A turned wooden lamp glowing on a side table beside a stone wall", "(max-width: 860px) 100vw, 45vw", eager=True)}</div>
</div></section>
<section class="section section--tint" aria-labelledby="stand-h"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How we care for homes</span><h2 id="stand-h">Three layers of care</h2></div>
  <div class="grid grid--3">
    <div class="reveal"><h3>Standards</h3><p>Clear housekeeping and presentation standards for every home, checked at each changeover, from the linen to the welcome.</p></div>
    <div class="reveal"><h3>Inspections</h3><p>Regular, detailed inspections through the year, so we spot wear and small faults before guests do.</p></div>
    <div class="reveal"><h3>Maintenance</h3><p>Reactive and planned maintenance with trusted local trades, with you informed and in control of bigger decisions.</p></div>
  </div></div></section>
{case_section("property-care")}
<section class="section" aria-labelledby="faq-h"><div class="wrap wrap--narrow"><div class="section-head"><h2 id="faq-h">Property Care questions</h2></div>{faq_html(faqs)}</div></section>
{cta_band(location="care_final", service="full-management")}
'''
    return {"path": path, "title": "Holiday Home Property Care & Maintenance | Staycay Management", "description": desc, "body": body,
            "schema": [breadcrumb_schema(crumbs), service_schema("Property Care", desc, path), faq_schema(faqs)]}


def page_performance():
    path = "/services/performance/"
    crumbs = [("Home", "/"), ("Services", "/services/"), ("Performance", path)]
    desc = "Holiday let pricing, revenue management and distribution in the Peak District, Derbyshire and South Yorkshire. Every night priced against local demand."
    faqs = [("How do you set prices?", "We price each night against local demand, seasonality, events and booking pace, and review strategy regularly rather than setting rates once a year."),
            ("Will you list my home on Airbnb and Booking.com?", "We'll recommend the right mix of channels for your home, alongside Staycay's direct-booking site."),
            ("How will I know it's working?", "You'll get clear reporting on bookings, revenue and how your home compares with the season before.")]
    body = f'''
<section class="page-hero page-hero--split"><div class="wrap">
  <div>{breadcrumbs_html(crumbs)}<span class="eyebrow">Performance</span><h1>Pricing, revenue and distribution, managed properly</h1>
  <p class="lede">The difference between a good year and a great one is usually made in the detail: the right price for every night, the right channels and the right minimum stays.</p>{cta_pair("performance_hero")}</div>
  <div class="page-hero__media">{picture("cotswold-house", "A honey-coloured stone house with stone-tiled roof and tall chimneys", "(max-width: 860px) 100vw, 45vw", eager=True)}</div>
</div></section>
<section class="section section--tint" aria-labelledby="perf-h"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we do</span><h2 id="perf-h">Three levers, pulled together</h2></div>
  <div class="grid grid--3">
    <div class="reveal"><h3>Pricing</h3><p>Nightly rates that move with demand: school holidays, local events, weekends and short-notice gaps.</p></div>
    <div class="reveal"><h3>Revenue</h3><p>Minimum-stay rules, gap-filling and length-of-stay strategy that lift income across the whole year, not just the summer.</p></div>
    <div class="reveal"><h3>Distribution</h3><p>Your home in the right places, with accurate calendars, strong listings and Staycay's own direct-booking site.</p></div>
  </div></div></section>
{case_section("performance")}
<section class="section" aria-labelledby="faq-h"><div class="wrap wrap--narrow"><div class="section-head"><h2 id="faq-h">Performance questions</h2></div>{faq_html(faqs)}</div></section>
{cta_band(location="performance_final")}
'''
    return {"path": path, "title": "Holiday Let Pricing & Revenue Management | Staycay Management", "description": desc, "body": body,
            "schema": [breadcrumb_schema(crumbs), service_schema("Holiday let revenue management", desc, path), faq_schema(faqs)]}


# ===========================================================================
# HOW IT WORKS
# ===========================================================================
def page_how():
    crumbs = [("Home", "/"), ("How It Works", "/how-it-works/")]
    detailed = [
        ("Request an appraisal", "Tell us about your home: where it is, its size and how it's let today. It takes a couple of minutes, and there's no obligation. Prefer to talk first? Book a 15-minute call."),
        ("Talk it through", "We'll be in touch within 48 hours. We'll ask about your goals, how you use the home and what's working or not, and arrange to visit if it helps."),
        ("Your proposal", "You'll receive a clear recommendation: which service fits, what your home could achieve, how we'd present it and what happens next."),
        ("Launch and beyond", "We prepare the home, arrange photography, build the listing and set pricing. Then we look after guests, the property and reporting, every stay."),
    ]
    principles = [("Selective", "We take on homes we're confident we can do justice to, so every owner gets real attention."),
                  ("Local", "Our knowledge of the Peak District, Derbyshire and South Yorkshire shapes pricing, presentation and care."),
                  ("Transparent", "Clear proposals, clear statements and a named point of contact. No surprises."),
                  ("Long-term", "We think in seasons and years: protecting your home, its reviews and its reputation.")]
    faqs = [OWNER_FAQS[0], OWNER_FAQS[1], ("How long does it take to get started?", "It depends on the home and what's needed to get it ready. We'll give you a realistic timeline in your proposal.")]
    body = f'''
<section class="page-hero"><div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">Our approach</span><h1>How it works</h1>
<p class="lede">A straightforward path from first conversation to a home that's fully booked and beautifully looked after.</p>{cta_pair("how_hero")}</div></section>
<section class="section section--tint" aria-labelledby="steps-h"><div class="wrap"><h2 id="steps-h" class="visually-hidden">The four steps</h2>{steps_html(detailed)}</div></section>
<section class="section" aria-labelledby="pr-h"><div class="wrap split">
  <div class="split__media reveal">{picture("sheep-house", "Sheep grazing in a meadow below a stone house among the trees", "(max-width: 860px) 100vw, 50vw")}</div>
  <div class="reveal"><span class="eyebrow">What guides us</span><h2 id="pr-h">The principles behind every home we manage</h2>
  <div class="stack">{"".join(f"<div><h3>{t}</h3><p class='muted'>{d}</p></div>" for t, d in principles)}</div></div>
</div></section>
<section class="section section--tint" aria-labelledby="faq-h"><div class="wrap wrap--narrow"><div class="section-head"><h2 id="faq-h">Common questions</h2></div>{faq_html(faqs)}</div></section>
{cta_band(location="how_final")}
'''
    return {"path": "/how-it-works/", "title": "How Our Holiday Let Management Works | Staycay Management",
            "description": "From appraisal to first booking: how Staycay takes on and manages holiday homes in the Peak District, Derbyshire and South Yorkshire.",
            "body": body, "schema": [breadcrumb_schema(crumbs), faq_schema(faqs)]}
