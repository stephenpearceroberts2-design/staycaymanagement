"""Shared settings, layout and components for the Staycay site build."""
import hashlib
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
IMG = SITE / "assets" / "img"

# ===========================================================================
# SETTINGS — change these, then run: python3 tools/build.py
# ===========================================================================
CONFIG = {
    "SITE_URL": "https://www.staycaymanagement.co.uk",
    # STAGING: noindex everywhere + preview bar. Set False only at launch,
    # once all placeholders are replaced and Staycay has signed off.
    "STAGING": True,
    "GA4_ID": "G-XXXXXXXXXX",                      # Staycay's own GA4 property
    "CALENDLY_URL": "https://calendly.com/REPLACE-ME/15min",
    "BOOKING_BASE": "https://REPLACE-ME.staycay.uk/properties",
    "ENQUIRY_EMAIL": "enquiries@staycay.uk",
    "BRAND": "Staycay Management",
    "TAGLINE": "Exceptional homes. Exceptionally managed.",
}

PLACEHOLDER_CONFIG = {
    "GA4_ID": "G-XXXXXXXXXX",
    "CALENDLY_URL": "REPLACE-ME",
    "BOOKING_BASE": "REPLACE-ME",
}

# Collected during the build; printed at the end and blocks a live build.
PLACEHOLDERS = set()


def note_placeholder(what):
    PLACEHOLDERS.add(what)


def e(s):
    return html.escape(str(s), quote=True)


def asset_version(rel):
    data = (SITE / rel.lstrip("/")).read_bytes()
    return hashlib.md5(data).hexdigest()[:8]


def abs_url(path):
    return CONFIG["SITE_URL"].rstrip("/") + path


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------
def _sizes_for(name):
    files = sorted(IMG.glob(f"{name}-*.webp"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
    if not files:
        raise SystemExit(f"Missing image: {name}")
    return [(int(p.stem.rsplit("-", 1)[1]), p) for p in files]


def img_url(name):
    """URL of the largest available size of an image."""
    return f"/assets/img/{name}-{_sizes_for(name)[-1][0]}.webp"


def picture(name, alt, sizes="100vw", cls="", eager=False):
    from PIL import Image
    sizes_list = _sizes_for(name)
    srcset = ", ".join(f"/assets/img/{name}-{w}.webp {w}w" for w, _ in sizes_list)
    w, p = sizes_list[-1]
    with Image.open(p) as im:
        width, height = im.size
    mid = sizes_list[min(1, len(sizes_list) - 1)][0]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{name}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{width}" height="{height}" alt="{e(alt)}" {loading}>')


# ---------------------------------------------------------------------------
# Icons (simple line icons, inherit currentColor)
# ---------------------------------------------------------------------------
ICONS = {
    "care": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M7 22 24 8l17 14"/><path d="M11 19v21h26V19"/><path d="m18 29 4.5 4.5L31 25"/></svg>',
    "performance": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M6 40h36"/><path d="m9 32 9-9 7 6 13-14"/><path d="M31 15h7v7"/></svg>',
    "representation": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><rect x="6" y="14" width="36" height="25" rx="1"/><path d="M17 14l3-5h8l3 5"/><circle cx="24" cy="26" r="7"/></svg>',
    "freedom": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M6 36c6-1 9-5 12-10s7-9 13-9c4 0 7 2 11 4"/><path d="M6 41h36"/><circle cx="35" cy="10" r="3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M4 5h16v11H9l-5 4V5Z"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="1"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
    "arrow-out": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>',
}


def icon(name, cls=""):
    svg = ICONS[name]
    return svg.replace("<svg ", f'<svg class="{cls}" ', 1) if cls else svg


# ---------------------------------------------------------------------------
# Reusable buttons
# ---------------------------------------------------------------------------
def btn_appraisal(location, style="primary", label="Request a Property Appraisal", service=None):
    href = "/property-appraisal/" + (f"?service={service}" if service else "")
    return f'<a class="btn btn--{style}" href="{href}" data-track="cta_appraisal" data-track-location="{location}">{label}</a>'


def btn_call(location, style="outline", label="Book a 15-Minute Call"):
    return (f'<a class="btn btn--{style}" href="{e(CONFIG["CALENDLY_URL"])}" data-calendly-open '
            f'data-track-location="{location}">{icon("calendar")}{label}</a>')


def cta_pair(location, dark=False, service=None):
    if dark:
        return f'<div class="btn-row">{btn_appraisal(location, "light", service=service)}{btn_call(location, "outline-light")}</div>'
    return f'<div class="btn-row">{btn_appraisal(location, service=service)}{btn_call(location)}</div>'


# ---------------------------------------------------------------------------
# Structured data helpers
# ---------------------------------------------------------------------------
def org_ref():
    return {"@type": "Organization", "name": CONFIG["BRAND"], "url": CONFIG["SITE_URL"] + "/"}


AREAS = ["Peak District", "Derbyshire", "South Yorkshire"]


def breadcrumb_schema(crumbs):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": abs_url(path)}
            for i, (name, path) in enumerate(crumbs)
        ],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }


def service_schema(name, description, path):
    return {
        "@context": "https://schema.org", "@type": "Service",
        "name": name, "serviceType": "Holiday let management", "description": description,
        "url": abs_url(path), "provider": org_ref(),
        "areaServed": [{"@type": "Place", "name": a} for a in AREAS],
    }


# ---------------------------------------------------------------------------
# Common blocks
# ---------------------------------------------------------------------------
def breadcrumbs_html(crumbs):
    items = []
    for i, (name, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li><span aria-current="page">{e(name)}</span></li>')
        else:
            items.append(f'<li><a href="{path}">{e(name)}</a></li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def faq_html(faqs):
    out = ['<div class="faq">']
    for q, a in faqs:
        out.append(f'<details><summary>{e(q)}</summary><div class="faq__a"><p>{a}</p></div></details>')
    out.append("</div>")
    return "".join(out)


def cta_band(heading="Find out what your home could achieve", text=None, location="cta_band", image="hills", service=None):
    text = text or "Request a free, no-obligation property appraisal. We'll come back to you within 48 hours."
    return f"""
<section class="cta-band dark" aria-labelledby="cta-{location}">
  <div class="cta-band__media">{picture(image, "", "100vw")}</div>
  <div class="wrap center">
    <span class="eyebrow">For owners</span>
    <h2 id="cta-{location}">{heading}</h2>
    <p class="lede">{text}</p>
    {cta_pair(location, dark=True, service=service)}
  </div>
</section>"""


NAV = [
    ("Our Homes", "/our-homes/"),
    ("For Owners", "/for-owners/"),
    ("Services", "/services/"),
    ("About", "/about/"),
    ("Journal", "/journal/"),
    ("Contact", "/contact/"),
]


def brand_html(tag="a"):
    return ('<a class="brand" href="/" aria-label="Staycay Management, home">'
            '<span class="brand__name">STAYCAY</span><span class="brand__sub">MANAGEMENT</span></a>')


def header_html(path, overlay):
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if path.startswith(href) else ""
        links.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cls = "site-header site-header--overlay" if overlay else "site-header"
    return f"""
<header class="{cls}">
  <div class="wrap site-header__inner">
    {brand_html()}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="visually-hidden">Menu</span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul class="nav__list">{"".join(links)}</ul>
      <div class="nav__cta">{btn_appraisal("mobile_nav")}{btn_call("mobile_nav")}</div>
    </nav>
    <a class="btn btn--primary btn--small header-cta" href="/property-appraisal/" data-track="cta_appraisal" data-track-location="header">Request an appraisal</a>
  </div>
</header>"""


def footer_html():
    year = date.today().year
    return f"""
<footer class="site-footer dark">
  <div class="wrap">
    <div class="footer-top">
      <div>
        {brand_html()}
        <p class="footer-tagline">{e(CONFIG["TAGLINE"])}</p>
        <p class="small">Specialist holiday home management across the Peak District, Derbyshire and South Yorkshire.</p>
        <p class="small"><a href="mailto:{CONFIG["ENQUIRY_EMAIL"]}">{CONFIG["ENQUIRY_EMAIL"]}</a></p>
      </div>
      <div>
        <h2>For owners</h2>
        <ul>
          <li><a href="/for-owners/">Why Staycay</a></li>
          <li><a href="/services/full-management/">Full Management</a></li>
          <li><a href="/services/bookings-revenue-management/">Bookings &amp; Revenue Management</a></li>
          <li><a href="/how-it-works/">How it works</a></li>
          <li><a href="/case-studies/">Owner success</a></li>
          <li><a href="/property-appraisal/">Request an appraisal</a></li>
        </ul>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="/our-homes/">Our homes</a></li>
          <li><a href="/journal/">Journal</a></li>
          <li><a href="/about/">About us</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Speak to us</h2>
        <p class="small">A quick, no-obligation conversation about your home.</p>
        {btn_call("footer", "outline-light")}
      </div>
    </div>
    <div class="footer-bottom">
      <p class="mb-0">&copy; {year} Staycay Management. All rights reserved.</p>
      <ul>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
        <li><a href="/cookie-policy/">Cookie policy</a></li>
        <li><button type="button" data-open-consent>Cookie settings</button></li>
      </ul>
    </div>
  </div>
</footer>"""


def consent_html():
    return """
<div class="consent" id="consent" role="dialog" aria-labelledby="consent-title" aria-describedby="consent-text">
  <h2 id="consent-title">Cookies</h2>
  <p id="consent-text">We'd like to use analytics cookies to understand how the site is used and improve it. They're only set if you accept. <a class="text-link" href="/cookie-policy/">Cookie policy</a></p>
  <div class="btn-row">
    <button class="btn btn--outline" type="button" data-consent="denied">Reject</button>
    <button class="btn btn--primary" type="button" data-consent="granted">Accept</button>
  </div>
</div>"""


def calendly_modal_html():
    return f"""
<div class="modal" id="call-modal" role="dialog" aria-modal="true" aria-labelledby="call-modal-title">
  <div class="modal__dialog">
    <div class="modal__head">
      <h2 id="call-modal-title">Book a 15-minute call</h2>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">&times;</button>
    </div>
    <div class="modal__body"><iframe title="Choose a time for your 15-minute call" loading="lazy"></iframe></div>
    <p class="modal__fallback">Scheduling is provided by Calendly. Trouble loading? <a class="text-link" href="{e(CONFIG["CALENDLY_URL"])}" target="_blank" rel="noopener">Open the booking page</a>.</p>
  </div>
</div>"""


def layout(page):
    """page: dict with path, title, description, body, and optional
    overlay, schema (list), noindex, og_image, body_attrs, og_type."""
    path = page["path"]
    title = page["title"]
    desc = page["description"]
    canonical = abs_url(path)
    noindex = CONFIG["STAGING"] or page.get("noindex")
    og_img = abs_url(page.get("og_image") or "/assets/img/og-image.jpg")
    css_v = asset_version("/assets/css/site.css")
    js_v = asset_version("/assets/js/site.js")
    schema = page.get("schema", [])
    schema_tags = "".join(
        f'\n<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema
    )
    preview = ""
    body_cls = []
    if CONFIG["STAGING"]:
        preview = '<div class="preview-bar"><strong>Preview site</strong><span class="preview-bar__more"> · placeholder photography and sample content, not for publication</span></div>'
        body_cls.append("has-preview")
    body_attrs = page.get("body_attrs", "")
    return f"""<!doctype html>
<html lang="en-GB" class="no-js" data-ga="{e(CONFIG["GA4_ID"])}" data-calendly="{e(CONFIG["CALENDLY_URL"])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex, nofollow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{page.get("og_type", "website")}">
<meta property="og:site_name" content="Staycay Management">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#263B32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/jost-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={css_v}">
<script src="/assets/js/site.js?v={js_v}" defer></script>{schema_tags}
</head>
<body class="{' '.join(body_cls)}"{(' ' + body_attrs) if body_attrs else ''}>
<a class="skip-link" href="#main">Skip to content</a>
{preview}
{header_html(path, page.get("overlay", False))}
<main id="main">
{page["body"]}
</main>
{footer_html()}
{consent_html()}
{calendly_modal_html()}
</body>
</html>
"""
