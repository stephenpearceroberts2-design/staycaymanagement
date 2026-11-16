"""Page builders, part 2: homes, case studies, about, journal, contact, forms, legal."""
from lib import (CONFIG, e, picture, icon, img_url, abs_url, btn_appraisal, btn_call, cta_pair,
                 cta_band, breadcrumbs_html, breadcrumb_schema, faq_html, faq_schema, org_ref,
                 note_placeholder)
from pages import (booking_url, sample_flag, home_card, testimonials_section, case_feature_html,
                   article_card, local_section)
import content as C


# ===========================================================================
# OUR HOMES
# ===========================================================================
def page_homes():
    crumbs = [("Home", "/"), ("Our Homes", "/our-homes/")]
    used = {c for h in C.HOMES for c in h["categories"]}
    filters = ['<button class="filter" type="button" data-filter="all" aria-pressed="true">All homes</button>']
    filters += [f'<button class="filter" type="button" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in C.CATEGORIES if k in used]
    items = {
        "@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": abs_url(f"/our-homes/{h['slug']}/"), "name": h["name"]} for i, h in enumerate(C.HOMES)],
    }
    body = f'''
<section class="page-hero page-hero--image">
  <div class="hero__media">{picture("terrace", "A stone terrace set for dinner overlooking a valley at dusk", "100vw", eager=True)}</div>
  <div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">For guests</span><h1>Our homes</h1>
  <p class="lede">A curated collection of holiday homes across the Peak District and Derbyshire, chosen for character, comfort and setting.</p></div>
</section>
<section class="section" aria-labelledby="list-h"><div class="wrap">
  <h2 id="list-h" class="visually-hidden">All homes</h2>
  <div class="filters" data-filters role="group" aria-label="Filter homes">{"".join(filters)}</div>
  <p class="visually-hidden" aria-live="polite" data-filter-status></p>
  <div class="grid grid--3">{"".join(home_card(h) for h in C.HOMES)}</div>
  <p class="empty-note" data-empty hidden>No homes match that filter just now. <button class="text-link" type="button" data-filter="all" style="background:none;border:0;padding:0;cursor:pointer">Show all homes</button></p>
</div></section>
<section class="section section--tint" aria-labelledby="book-h"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">Booking direct</span><h2 id="book-h">Book with us directly</h2><p class="lede">Every home links straight to our booking site, where you'll find live availability, prices and secure checkout.</p></div>
  <div class="reveal"><p>Questions about a stay? <a class="text-link" href="/contact/">Get in touch</a> and the team will help.</p><p>Own a home you think belongs in this collection? <a class="text-link" href="/for-owners/">Find out about working with us</a>.</p></div>
</div></section>
'''
    # The filter "Show all" button lives outside data-filters; handled by a tiny inline hook
    body = body.replace('data-filter="all" style=', 'onclick="document.querySelector(\'[data-filters] [data-filter=all]\').click()" style=')
    return {"path": "/our-homes/", "title": "Holiday Homes in the Peak District | Staycay",
            "description": "A curated collection of holiday cottages, barns and family homes in the Peak District and Derbyshire. Book direct with Staycay.",
            "body": body, "schema": [breadcrumb_schema(crumbs), items]}


def page_property(h):
    path = f"/our-homes/{h['slug']}/"
    crumbs = [("Home", "/"), ("Our Homes", "/our-homes/"), (h["name"], path)]
    url = booking_url(h)
    if "REPLACE-ME" in url:
        note_placeholder("Direct-booking platform URLs (BOOKING_BASE in tools/lib.py and booking_url per home)")
    gallery_parts = []
    for i, img in enumerate(h["images"][:5]):
        alt = f"{h['name']} in {h['location']}" if i == 0 else f"{h['name']}, photo {i + 1}"
        sizes = "(max-width: 760px) 100vw, 50vw" if i == 0 else "25vw"
        gallery_parts.append(f"<figure>{picture(img, alt, sizes, eager=(i == 0))}</figure>")
    gallery = "".join(gallery_parts)
    others = [x for x in C.HOMES if x["slug"] != h["slug"]][:3]
    flag = sample_flag(h, "Properties on Our Homes (names, details, photos, booking links)")
    book_btn = (f'<a class="btn btn--primary" href="{e(url)}" data-track="booking_click" data-property="{h["slug"]}" '
                f'data-track-location="property_panel" rel="noopener">Check availability &amp; book</a>')
    schema = {
        "@context": "https://schema.org", "@type": "VacationRental",
        "name": h["name"], "description": h["summary"], "url": abs_url(path),
        "image": [abs_url(img_url(i)) for i in h["images"][:5]],
        "address": {"@type": "PostalAddress", "addressLocality": h["location"], "addressRegion": h["region"], "addressCountry": "GB"},
        "containsPlace": {"@type": "Accommodation", "occupancy": {"@type": "QuantitativeValue", "maxValue": h["sleeps"]}, "numberOfBedrooms": h["bedrooms"], "numberOfBathroomsTotal": h["bathrooms"]},
        "brand": org_ref(),
    }
    body = f'''
<section class="section--tight" style="padding-top:clamp(40px,5vw,64px)"><div class="wrap">
  {breadcrumbs_html(crumbs)}
  <span class="eyebrow">{e(h["location"])}{flag}</span>
  <h1 style="font-size:clamp(44px,5.5vw,72px)">{e(h["name"])}</h1>
  <p class="lede" style="margin-bottom:36px">{e(h["summary"])}</p>
  <div class="gallery">{gallery}</div>
</div></section>
<section class="section" style="padding-top:clamp(40px,5vw,64px)"><div class="wrap property-layout">
  <div>
    <dl class="facts"><div><dt>Sleeps</dt><dd>{h["sleeps"]}</dd></div><div><dt>Bedrooms</dt><dd>{h["bedrooms"]}</dd></div><div><dt>Bathrooms</dt><dd>{h["bathrooms"]}</dd></div><div><dt>Dogs</dt><dd style="font-size:20px;padding-top:6px">{e(h["dogs"])}</dd></div></dl>
    <h2>About {e(h["name"])}</h2>
    <div class="prose">{"".join(f"<p>{e(p)}</p>" for p in h["description"])}</div>
    <h2 class="mt-l">Features</h2>
    <ul class="checklist features">{"".join(f"<li>{e(f)}</li>" for f in h["features"])}</ul>
    <h2 class="mt-l">The local area</h2>
    <p class="prose">{e(h["nearby"])}</p>
  </div>
  <aside class="book-panel" aria-labelledby="book-h">
    <span class="eyebrow">Book direct</span>
    <h2 id="book-h">Check dates and prices</h2>
    <p class="muted">Live availability, prices and secure checkout on our booking site.</p>
    {book_btn}
    <p class="small">Questions about this home? <a class="text-link" href="/contact/">Contact us</a></p>
  </aside>
</div></section>
<section class="section section--tint" aria-labelledby="more-h"><div class="wrap">
  <div class="section-head section-head--row"><div><span class="eyebrow">You might also like</span><h2 id="more-h">More homes from our collection</h2></div><a class="link-arrow" href="/our-homes/">All homes</a></div>
  <div class="grid grid--3">{"".join(home_card(x) for x in others)}</div>
</div></section>
'''
    return {"path": path, "title": f"{h['name']}, {h['location']} | Holiday Home | Staycay",
            "description": f"{h['name']} in {h['location']}: sleeps {h['sleeps']}, {h['bedrooms']} bedrooms. {h['summary']}"[:158],
            "body": body, "schema": [breadcrumb_schema(crumbs), schema], "og_image": img_url(h["images"][0])}


# ===========================================================================
# CASE STUDIES
# ===========================================================================
def page_cases():
    crumbs = [("Home", "/"), ("Case Studies", "/case-studies/")]
    cards = "".join(case_feature_html(c, "h2") for c in C.CASE_STUDIES)
    body = f'''
<section class="page-hero"><div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">Owner success</span><h1>Case studies</h1>
<p class="lede">Real homes, real owners and what changed when they started working with us.</p></div></section>
<section class="section" style="padding-top:0" aria-label="Case studies"><div class="wrap stack">{cards}</div></section>
{testimonials_section("owners")}
{cta_band(location="cases_final")}
'''
    return {"path": "/case-studies/", "title": "Holiday Let Management Case Studies | Staycay Management",
            "description": "How Staycay has helped holiday home owners in the Peak District and Derbyshire improve bookings, revenue and reviews, and get their time back.",
            "body": body, "schema": [breadcrumb_schema(crumbs)]}


def page_case(cs):
    path = f"/case-studies/{cs['slug']}/"
    crumbs = [("Home", "/"), ("Case Studies", "/case-studies/"), (cs["title"], path)]
    flag = sample_flag(cs, "Case studies and their figures")
    stats = "".join(f"<div><strong>{e(v)}</strong><span>{e(l)}</span></div>" for v, l in cs["stats"])
    growth = ""
    if cs.get("growth"):
        mx = max(v for _, v, _ in cs["growth"])
        bars = "".join(f'<div class="growth__bar"><b>{e(d)}</b><span style="height:{round(v / mx * 82)}%"></span></div>' for _, v, d in cs["growth"])
        labels = "".join(f"<span>{e(l)}</span>" for l, _, _ in cs["growth"])
        growth = f'<h2>Growth over time</h2><div class="growth" role="img" aria-label="{e(cs["growth_caption"])} ' + ", ".join(f"{l}: {d}" for l, _, d in cs["growth"]) + f'"><div class="growth__bars">{bars}</div><div class="growth__labels">{labels}</div></div><p class="growth__caption">{e(cs["growth_caption"])}</p>'
    t = C.TESTIMONIALS[cs["quote"]] if cs.get("quote") is not None else None
    quote = ""
    if t:
        quote = f'<figure class="quote quote--feature" style="margin:56px 0"><div class="quote__mark" aria-hidden="true">&ldquo;</div><blockquote><p class="mb-0">{e(t["quote"])}</p></blockquote><figcaption>{e(t["name"])}, {e(t["detail"])}{sample_flag(t, "Owner testimonials")}</figcaption></figure>'
    imgs = "".join(f"<div>{picture(i, '', '(max-width: 640px) 100vw, 50vw')}</div>" for i in cs["images"])
    body = f'''
<section class="page-hero page-hero--image">
  <div class="hero__media">{picture(cs["image"], "", "100vw", eager=True)}</div>
  <div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">Case study · {e(cs["service"])} · {e(cs["location"])}{flag}</span><h1 style="font-size:clamp(38px,4.8vw,64px);max-width:18em">{e(cs["title"])}</h1></div>
</section>
<section class="section section--tight section--dark dark" aria-label="Results"><div class="wrap"><div class="case-stats" style="margin:0;border-top:0;padding-top:0">{stats}</div></div></section>
<article class="section"><div class="wrap wrap--narrow prose">
  <h2 style="margin-top:0">The challenge</h2>{"".join(f"<p>{e(p)}</p>" for p in cs["challenge"])}
  <h2>Our approach</h2>{"".join(f"<p>{e(p)}</p>" for p in cs["approach"])}
  <div class="before-after"><div><h3>Before</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in cs["before"])}</ul></div><div><h3>After</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in cs["after"])}</ul></div></div>
  {growth}
  {quote}
  <div class="grid grid--2" style="margin-top:32px">{imgs}</div>
  <div class="inline-cta"><h3>Could your home do the same?</h3><p>Request a free appraisal and we'll show you what's possible.</p>{cta_pair("case_" + cs["slug"], dark=True)}</div>
</div></article>
'''
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": cs["title"], "description": cs["short"],
              "image": abs_url(img_url(cs["image"])), "author": org_ref(), "publisher": org_ref(), "mainEntityOfPage": abs_url(path)}
    return {"path": path, "title": f"{cs['title'][:60]} | Staycay"[:70], "description": cs["short"][:158], "body": body,
            "schema": [breadcrumb_schema(crumbs), schema], "og_type": "article", "og_image": img_url(cs["image"])}


# ===========================================================================
# ABOUT
# ===========================================================================
def page_about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    team = []
    for m in C.TEAM:
        sample_flag(m, "Team names, roles, biographies and photography")
        photo = picture(m["photo"], m["name"], "(max-width: 640px) 100vw, 25vw") if m.get("photo") else f'<div class="team-card__photo" aria-hidden="true">S</div>'
        team.append(f'<div class="team-card reveal">{photo}<h3>{e(m["name"])}</h3><div class="team-card__role">{e(m["role"])}</div><p>{e(m["bio"])}</p></div>')
    body = f'''
<section class="page-hero page-hero--split"><div class="wrap">
  <div>{breadcrumbs_html(crumbs)}<span class="eyebrow">About Staycay</span><h1>Local people, looking after exceptional homes</h1>
  <p class="lede">For three years we've looked after holiday homes across the Peak District, Derbyshire and South Yorkshire. Today we care for more than 75 of them, and we're choosing to focus on the very best.</p></div>
  <div class="page-hero__media">{picture("house-tight", "A stone farmhouse with climbing ivy and lit windows at dusk", "(max-width: 860px) 100vw, 45vw", eager=True)}</div>
</div></section>
<section class="section section--tint" aria-labelledby="story-h"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">Our story</span><h2 id="story-h">Why we do what we do</h2></div>
  <div class="reveal"><p class="lede">Staycay's story, in the founders' own words: how it started, what they saw missing in holiday home management, and why the Peak District.</p>
  <p>This section is ready for Staycay's finished copy. It works best at around 200 to 300 words, written personally, ending with where the business is heading: a specialist manager of high-quality homes.</p></div>
</div></section>
<section class="section" aria-labelledby="values-h"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we stand for</span><h2 id="values-h">Premium, not pretentious</h2></div>
  <div class="grid grid--3">
    <div class="reveal"><h3>Characterful and authentic</h3><p class="muted">Homes with a real sense of place, presented honestly and looked after with care.</p></div>
    <div class="reveal"><h3>Warm and welcoming</h3><p class="muted">For guests, a stay that feels effortless. For owners, a team that's easy to deal with.</p></div>
    <div class="reveal"><h3>Naturally connected to place</h3><p class="muted">We live and work here, and that local knowledge runs through everything we do.</p></div>
  </div></div></section>
<section class="section section--tint" aria-labelledby="team-h"><div class="wrap">
  <div class="section-head"><span class="eyebrow">The team</span><h2 id="team-h">The people looking after your home</h2></div>
  <div class="grid grid--4">{"".join(team)}</div>
</div></section>
{local_section()}
{testimonials_section("about", tint=False)}
{cta_band(location="about_final")}
'''
    return {"path": "/about/", "title": "About Staycay Management | Peak District Holiday Home Specialists",
            "description": "Meet Staycay: a local, specialist manager of high-quality holiday homes in the Peak District, Derbyshire and South Yorkshire, caring for 75+ homes.",
            "body": body, "schema": [breadcrumb_schema(crumbs)]}


# ===========================================================================
# JOURNAL
# ===========================================================================
def page_journal():
    crumbs = [("Home", "/"), ("Journal", "/journal/")]
    sections = []
    for key, label in C.JOURNAL_CATEGORIES.items():
        arts = [a for a in sorted(C.ARTICLES, key=lambda x: x["date"], reverse=True) if a["category"] == key]
        if not arts:
            continue
        sections.append(f'<section class="section" style="padding-top:0" id="{key}" aria-labelledby="cat-{key}"><div class="wrap"><div class="section-head"><h2 id="cat-{key}">{label}</h2></div><div class="grid grid--3">{"".join(article_card(a) for a in arts)}</div></div></section>')
    body = f'''
<section class="page-hero"><div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">Journal</span><h1>Notes for owners and guests</h1>
<p class="lede">Practical advice for holiday home owners, and ideas for making the most of the Peak District.</p>
<div class="filters" style="margin:28px 0 0">{"".join(f'<a class="filter" style="text-decoration:none" href="#{k}">{v}</a>' for k, v in C.JOURNAL_CATEGORIES.items())}</div></div></section>
{"".join(sections)}
{cta_band(location="journal_final")}
'''
    return {"path": "/journal/", "title": "Journal: Holiday Home Advice & Peak District Guides | Staycay",
            "description": "Advice for holiday let owners and guides to the Peak District, Derbyshire and South Yorkshire from the Staycay team.",
            "body": body, "schema": [breadcrumb_schema(crumbs)]}


def page_article(a):
    path = f"/journal/{a['slug']}/"
    crumbs = [("Home", "/"), ("Journal", "/journal/"), (a["title"], path)]
    flag = sample_flag(a, "Journal articles")
    related = [x for x in C.ARTICLES if x["slug"] != a["slug"]]
    related.sort(key=lambda x: x["category"] != a["category"])
    from datetime import date as d
    nice = d.fromisoformat(a["date"]).strftime("%-d %B %Y")
    if a["category"] == "owners":
        cta = f'<div class="inline-cta"><h3>Thinking about management for your home?</h3><p>Request a free, no-obligation appraisal and we\'ll come back to you within 48 hours.</p>{cta_pair("article_" + a["slug"], dark=True)}</div>'
    else:
        cta = '<div class="inline-cta"><h3>Find your place to stay</h3><p>Browse our curated collection of holiday homes across the Peak District and Derbyshire.</p><a class="btn btn--light" href="/our-homes/" data-track="guest_route" data-track-location="article">Explore our homes</a></div>'
    body = f'''
<article>
<header class="page-hero" style="padding-bottom:0"><div class="wrap wrap--narrow">
  {breadcrumbs_html(crumbs)}
  <span class="eyebrow">{C.JOURNAL_CATEGORIES[a["category"]]}{flag}</span>
  <h1 style="font-size:clamp(40px,5vw,64px)">{e(a["title"])}</h1>
  <div class="article-meta"><time datetime="{a["date"]}">{nice}</time><span>{a["read"]}</span><span>By the Staycay team</span></div>
</div>
<div class="wrap"><div class="article-hero__media">{picture(a["image"], "", "100vw", eager=True)}</div></div>
</header>
<div class="section" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap wrap--narrow prose">{a["body"]}{cta}</div></div>
</article>
<section class="section section--tint" aria-labelledby="rel-h"><div class="wrap">
  <div class="section-head section-head--row"><div><span class="eyebrow">Keep reading</span><h2 id="rel-h">Related articles</h2></div><a class="link-arrow" href="/journal/">All articles</a></div>
  <div class="grid grid--3">{"".join(article_card(x) for x in related[:3])}</div>
</div></section>
'''
    schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["description"],
              "image": abs_url(img_url(a["image"])), "datePublished": a["date"], "dateModified": a["date"],
              "author": org_ref(), "publisher": org_ref(), "mainEntityOfPage": abs_url(path)}
    return {"path": path, "title": f"{a.get('seo_title', a['title'])} | Staycay", "description": a["description"], "body": body,
            "schema": [breadcrumb_schema(crumbs), schema], "og_type": "article", "og_image": img_url(a["image"])}


# ===========================================================================
# FORMS
# ===========================================================================
HIDDEN_ATTR = "".join(f'<input type="hidden" name="{n}">' for n in ["landing_page", "referrer", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "form_page"])


def field(name, label, type_="text", required=True, autocomplete=None, hint=None, full=False, extra=""):
    req = " required" if required else ""
    opt = "" if required else ' <span class="opt">(optional)</span>'
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    hint_html = f'<p class="hint" id="{name}-hint">{hint}</p>' if hint else ""
    desc = f' aria-describedby="{name}-hint {name}-err"' if hint else f' aria-describedby="{name}-err"'
    cls = "field full" if full else "field"
    if type_ == "textarea":
        control = f'<textarea id="{name}" name="{name}"{req}{desc}{extra}></textarea>'
    else:
        control = f'<input id="{name}" name="{name}" type="{type_}"{req}{ac}{desc}{extra}>'
    err = {"email": "Please enter a valid email address.", "tel": "Please enter a telephone number.", "url": "Please enter a full link, starting https://"}.get(type_, "Please fill in this field.")
    return f'<div class="{cls}"><label for="{name}">{label}{opt}</label>{hint_html}{control}<p class="error" id="{name}-err">{err}</p></div>'


def select(name, label, options, required=True):
    opts = '<option value="">Please choose</option>' + "".join(f"<option>{o}</option>" for o in options)
    return f'<div class="field"><label for="{name}">{label}</label><select id="{name}" name="{name}" required aria-describedby="{name}-err">{opts}</select><p class="error" id="{name}-err">Please choose an option.</p></div>'


def radios(name, legend, options, cols=3):
    items = "".join(f'<label class="choice"><input type="radio" name="{name}" value="{e(v)}" data-key="{k}" required><span>{v}{f"<small>{s}</small>" if s else ""}</span></label>' for k, v, s in options)
    return f'<div class="field full" role="radiogroup" aria-labelledby="{name}-label"><span class="label" id="{name}-label">{legend}</span><div class="choices choices--{cols}">{items}</div><p class="error">Please choose an option.</p></div>'


def page_appraisal():
    crumbs = [("Home", "/"), ("Property Appraisal", "/property-appraisal/")]
    form = f'''
<form class="form-card" name="appraisal" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="bot-field" data-staycay-form>
  <input type="hidden" name="form-name" value="appraisal">
  <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  {HIDDEN_ATTR}
  <fieldset><legend>About you</legend><div class="form-grid">
    {field("name", "Full name", autocomplete="name", full=True)}
    {field("email", "Email address", "email", autocomplete="email")}
    {field("phone", "Telephone", "tel", autocomplete="tel")}
  </div></fieldset>
  <fieldset><legend>About the property</legend><div class="form-grid">
    {field("property_address", "Property address or postcode", autocomplete="street-address", full=True)}
    {select("bedrooms", "Bedrooms", ["Studio", "1", "2", "3", "4", "5", "6", "7+"])}
    {select("property_type", "Property type", ["Cottage", "Barn conversion", "Farmhouse", "Detached house", "Townhouse", "Apartment", "Lodge or cabin", "Other"])}
    {radios("let_status", "Is it currently a holiday let?", [("self", "Yes, I manage it myself", ""), ("managed", "Yes, with another manager", ""), ("not-yet", "Not yet", "")])}
    {field("listing_url", "Airbnb, Booking.com or website link", "url", required=False, hint="If the home is already listed, a link helps us prepare.", full=True, extra=' placeholder="https://"')}
  </div></fieldset>
  <fieldset><legend>How can we help?</legend><div class="form-grid">
    {radios("service_interest", "Which service interests you?", [("full-management", "Full Management", "Everything handled"), ("bookings-revenue-management", "Bookings &amp; Revenue Management", "Pricing, listings and bookings"), ("not-sure", "Not sure yet", "We'll help you decide")])}
    {field("message", "Anything else we should know?", "textarea", required=False, full=True)}
  </div></fieldset>
  <div class="form-foot"><button class="btn btn--primary" type="submit">Request my appraisal</button>
  <p>We'll respond within 48 hours. Your details are only used to respond to your enquiry. See our <a class="text-link" href="/privacy-policy/">privacy policy</a>.</p></div>
</form>'''
    body = f'''
<section class="page-hero" style="padding-bottom:clamp(32px,4vw,56px)"><div class="wrap">{breadcrumbs_html(crumbs)}</div></section>
<section class="section" style="padding-top:0"><div class="wrap form-shell">
  <div>
    <span class="eyebrow">Free, no obligation</span>
    <h1 style="font-size:clamp(42px,5vw,68px)">Request a property appraisal</h1>
    <p class="lede">Tell us a little about your home. We'll review it and come back to you within 48 hours to talk about what it could achieve.</p>
    <ul class="reassure">
      <li>{icon("clock")}<div><strong>Takes about two minutes</strong><br><span class="muted small">No financial details needed at this stage.</span></div></li>
      <li>{icon("chat")}<div><strong>A real conversation</strong><br><span class="muted small">You'll hear from a member of our team, not an automated sequence.</span></div></li>
      <li>{icon("shield")}<div><strong>No obligation</strong><br><span class="muted small">An appraisal is free, whatever you decide.</span></div></li>
    </ul>
    <p style="margin-top:28px" class="muted">Prefer to talk first?</p>
    {btn_call("appraisal_side")}
  </div>
  <div>{form}</div>
</div></section>
'''
    return {"path": "/property-appraisal/", "title": "Request a Free Property Appraisal | Staycay Management",
            "description": "Request a free, no-obligation appraisal for your holiday home in the Peak District, Derbyshire or South Yorkshire. We'll respond within 48 hours.",
            "body": body, "schema": [breadcrumb_schema(crumbs)]}


def page_contact():
    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    form = f'''
<form class="form-card" name="contact" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="bot-field" data-staycay-form>
  <input type="hidden" name="form-name" value="contact">
  <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  {HIDDEN_ATTR}
  <div class="form-grid">
    {field("name", "Full name", autocomplete="name", full=True)}
    {field("email", "Email address", "email", autocomplete="email")}
    {field("phone", "Telephone", "tel", required=False, autocomplete="tel")}
    {radios("enquiry_type", "I'm a", [("owner", "Property owner", ""), ("guest", "Guest", ""), ("other", "Something else", "")])}
    {field("message", "Your message", "textarea", full=True)}
  </div>
  <div class="form-foot" style="margin-top:28px"><button class="btn btn--primary" type="submit">Send message</button>
  <p>See our <a class="text-link" href="/privacy-policy/">privacy policy</a> for how we use your details.</p></div>
</form>'''
    body = f'''
<section class="page-hero"><div class="wrap">{breadcrumbs_html(crumbs)}<span class="eyebrow">Contact</span><h1>Get in touch</h1>
<p class="lede">Whether you own a holiday home or you're planning a stay, we'd love to hear from you.</p></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="grid grid--2">
    <div class="service-card service-card--flagship"><span class="tag">Owners</span><h2 style="color:var(--stone);font-size:clamp(30px,3vw,40px)">Thinking about management?</h2><p>The quickest way to get started is a free property appraisal, or book a 15-minute call at a time that suits you.</p><div class="btn-row" style="margin-top:auto">{btn_appraisal("contact_owner", "light")}{btn_call("contact_owner", "outline-light")}</div></div>
    <div class="service-card"><span class="tag">Guests</span><h2 style="font-size:clamp(30px,3vw,40px)">Planning a stay?</h2><p>Browse our homes and book directly for live availability and prices. For questions about a booking, use the form below.</p><div class="btn-row" style="margin-top:auto"><a class="btn btn--outline" href="/our-homes/" data-track="guest_route" data-track-location="contact">Explore our homes</a></div></div>
  </div>
</div></section>
<section class="section section--tint"><div class="wrap form-shell">
  <div><span class="eyebrow">General enquiries</span><h2>Send us a message</h2><p class="lede">We'll get back to you as soon as we can.</p>
  <p>Email: <a class="text-link" href="mailto:{CONFIG["ENQUIRY_EMAIL"]}">{CONFIG["ENQUIRY_EMAIL"]}</a></p>
  <p class="muted small">We manage homes across the Peak District, Derbyshire and South Yorkshire.</p></div>
  <div>{form}</div>
</div></section>
'''
    return {"path": "/contact/", "title": "Contact Staycay Management",
            "description": "Contact Staycay Management about holiday home management or a stay in one of our Peak District homes. Request an appraisal or book a 15-minute call.",
            "body": body, "schema": [breadcrumb_schema(crumbs)]}


def page_thanks():
    body = f'''
<section class="section"><div class="wrap wrap--narrow center">
  <span class="eyebrow">Received</span><h1>Thank you</h1>
  <p class="lede" data-thanks>We've received your details and will be in touch within 48 hours.</p>
  <p class="lede" data-thanks data-thanks-appraisal hidden>We've received your appraisal request and will be in touch within 48 hours. If it would help to talk sooner, book a 15-minute call below.</p>
  <p class="lede" data-thanks data-thanks-contact hidden>Thanks for getting in touch. We'll come back to you as soon as we can.</p>
  <div class="btn-row" style="justify-content:center;margin-top:28px">{btn_call("thank_you", "primary")}<a class="link-arrow" href="/our-homes/">Explore our homes</a></div>
</div></section>'''
    return {"path": "/thank-you/", "title": "Thank you | Staycay Management", "description": "Thank you for contacting Staycay Management.",
            "body": body, "noindex": True, "body_attrs": "data-thank-you", "sitemap": False}


def page_404():
    body = f'''
<section class="section"><div class="wrap wrap--narrow center"><span class="eyebrow">Page not found</span><h1>This page has wandered off</h1>
<p class="lede">The page you're looking for may have moved. Try one of these instead.</p>
<div class="btn-row" style="justify-content:center;margin-top:24px"><a class="btn btn--primary" href="/">Home</a><a class="btn btn--outline" href="/our-homes/">Our homes</a><a class="btn btn--outline" href="/for-owners/">For owners</a></div></div></section>'''
    return {"path": "/404.html", "title": "Page not found | Staycay Management", "description": "Page not found.", "body": body,
            "noindex": True, "sitemap": False, "file": "404.html"}


# ===========================================================================
# LEGAL (drafts: Staycay supplies / approves final legal text)
# ===========================================================================
def legal_page(path, h1, title, desc, html):
    crumbs = [("Home", "/"), (h1, path)]
    note_placeholder("Privacy and cookie policy text (draft, needs Staycay's approval and company details)")
    body = f'''
<section class="page-hero" style="padding-bottom:0"><div class="wrap wrap--narrow">{breadcrumbs_html(crumbs)}<h1>{h1}</h1></div></section>
<section class="section" style="padding-top:32px"><div class="wrap wrap--narrow prose">
<p class="legal-note"><strong>Draft for approval.</strong> This text is a starting point and must be reviewed and approved by Staycay before launch. Replace the bracketed details.</p>
{html}</div></section>'''
    return {"path": path, "title": title, "description": desc, "body": body, "schema": [breadcrumb_schema(crumbs)]}


def page_privacy():
    return legal_page("/privacy-policy/", "Privacy policy", "Privacy Policy | Staycay Management", "How Staycay Management collects, uses and protects your personal data.", f'''
<p>Last updated: [date]</p>
<h2>Who we are</h2>
<p>This website is operated by [legal company name], trading as Staycay Management (company number [number], registered office [address]). We are the controller of personal data collected through this website. Contact us at <a href="mailto:{CONFIG["ENQUIRY_EMAIL"]}">{CONFIG["ENQUIRY_EMAIL"]}</a>.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Appraisal and contact forms:</strong> your name, email address, telephone number, property details and anything else you choose to tell us. We also record how you found the site (for example the page you landed on and any campaign tags in the link).</li>
<li><strong>Call bookings:</strong> if you book a call, Calendly processes your name, email and chosen time on our behalf.</li>
<li><strong>Analytics:</strong> if you accept analytics cookies, Google Analytics collects information about how you use the site. See our <a href="/cookie-policy/">cookie policy</a>.</li>
</ul>
<h2>How and why we use it</h2>
<p>We use enquiry details to respond to you and, where you're a property owner, to prepare and discuss an appraisal. Our lawful basis is our legitimate interest in responding to enquiries and taking steps at your request before entering into a contract. We use analytics data, with your consent, to understand and improve the website.</p>
<h2>Who we share it with</h2>
<p>We use trusted service providers to run the website and handle enquiries, including our website host (Netlify), our scheduling provider (Calendly) and Google (analytics, with consent). Some of these providers may process data outside the UK, with appropriate safeguards in place. We don't sell your data.</p>
<h2>How long we keep it</h2>
<p>[Retention period, e.g. enquiries that don't lead to a management agreement are deleted after 24 months.]</p>
<h2>Your rights</h2>
<p>You have the right to access, correct or delete your personal data, to object to or restrict its use, and to data portability. To exercise these rights, email us. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
''')


def page_cookies():
    return legal_page("/cookie-policy/", "Cookie policy", "Cookie Policy | Staycay Management", "How Staycay Management uses cookies and how to change your preferences.", '''
<p>Last updated: [date]</p>
<p>Cookies are small files stored on your device. We only use non-essential cookies if you agree to them, and you can change your mind at any time using <button type="button" class="text-link" data-open-consent style="background:none;border:0;padding:0;font:inherit;cursor:pointer">cookie settings</button>.</p>
<h2>Essential storage</h2>
<p>We store your cookie choice in your browser so we don't ask again on every page.</p>
<h2>Analytics cookies (only with consent)</h2>
<p>We use Google Analytics 4 to understand how visitors use the site, for example which pages are viewed and whether appraisal requests are completed. These cookies (such as <code>_ga</code> and <code>_ga_*</code>) are only set if you click Accept. With your consent, we also remember how you first arrived on the site so we know which channels bring enquiries.</p>
<h2>Third-party services</h2>
<p>If you choose to book a call, our scheduling provider Calendly loads in a window on this site and may set its own cookies. Booking a stay takes you to our direct-booking site, which has its own cookie policy.</p>
<h2>Changing your choice</h2>
<p>Use the cookie settings link in the footer of any page, or clear cookies in your browser settings.</p>
''')
