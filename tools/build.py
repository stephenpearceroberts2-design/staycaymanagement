"""Build the Staycay Management website into site/.

    python3 tools/build.py            # staging build (default)
    python3 tools/build.py --force    # live build even if placeholders remain (not recommended)

Edit content in tools/content.py and page layouts in tools/pages*.py, then rerun.
The generated HTML in site/ is what Netlify publishes. Commit both.
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import lib  # noqa: E402
from lib import CONFIG, SITE, PLACEHOLDERS, PLACEHOLDER_CONFIG, layout, note_placeholder, abs_url  # noqa: E402
import pages as P  # noqa: E402
import pages2 as P2  # noqa: E402
import content as C  # noqa: E402

FONTS = SITE / "assets" / "fonts"


def all_pages():
    pages = [
        P.page_home(), P.page_owners(), P.page_services(), P.page_full_management(), P.page_brm(),
        P.page_property_care(), P.page_performance(), P.page_how(),
        P2.page_homes(), *[P2.page_property(h) for h in C.HOMES],
        P2.page_cases(), *[P2.page_case(c) for c in C.CASE_STUDIES],
        P2.page_about(), P2.page_journal(), *[P2.page_article(a) for a in C.ARTICLES],
        P2.page_appraisal(), P2.page_contact(), P2.page_thanks(), P2.page_404(),
        P2.page_privacy(), P2.page_cookies(),
    ]
    return pages


def write_page(page):
    if page.get("file"):
        out = SITE / page["file"]
    else:
        out = SITE / page["path"].strip("/") / "index.html" if page["path"] != "/" else SITE / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(layout(page), encoding="utf-8")
    return out


def make_brand_images():
    """OG share image, favicons. Uses the self-hosted fonts."""
    # PIL can't read woff2 directly: convert the self-hosted fonts to TTF first
    ttf_candidates = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
    try:
        from fontTools.ttLib import TTFont
        tmp = Path("/tmp/cg500.ttf")
        if not tmp.exists():
            f = TTFont(str(FONTS / "cormorant-garamond-latin-500-normal.woff2"))
            f.flavor = None
            f.save(str(tmp))
        ttf_candidates.insert(0, str(tmp))
        tmp2 = Path("/tmp/jost500.ttf")
        if not tmp2.exists():
            f = TTFont(str(FONTS / "jost-latin-500-normal.woff2"))
            f.flavor = None
            f.save(str(tmp2))
        sans_path = str(tmp2)
    except Exception:
        sans_path = ttf_candidates[-1]
    serif_path = ttf_candidates[0]

    peak = (38, 59, 50)
    stone = (243, 240, 233)

    # OG image 1200x630: photo left, green panel right
    og = Image.new("RGB", (1200, 630), peak)
    photo = Image.open(lib.IMG / "hero-1200.webp").convert("RGB")
    ratio = 630 / photo.height
    photo = photo.resize((round(photo.width * ratio), 630), Image.LANCZOS)
    left = min(photo.width - 720, max(0, round(photo.width * 0.67) - 360))
    og.paste(photo.crop((left, 0, left + 720, 630)), (0, 0))
    d = ImageDraw.Draw(og)
    f_brand = ImageFont.truetype(serif_path, 52)
    f_sub = ImageFont.truetype(sans_path, 15)
    f_tag = ImageFont.truetype(serif_path, 38)

    def spaced(draw, xy, text, font, fill, spacing):
        x, y = xy
        for ch in text:
            draw.text((x, y), ch, font=font, fill=fill)
            x += draw.textlength(ch, font=font) + spacing
        return x

    def spaced_width(draw, text, font, spacing):
        return sum(draw.textlength(c, font=font) + spacing for c in text) - spacing

    cx = 720 + 240
    w = spaced_width(d, "STAYCAY", f_brand, 10)
    spaced(d, (cx - w / 2, 200), "STAYCAY", f_brand, stone, 10)
    w = spaced_width(d, "MANAGEMENT", f_sub, 7)
    spaced(d, (cx - w / 2, 270), "MANAGEMENT", f_sub, stone, 7)
    d.line((cx - 60, 320, cx + 60, 320), fill=(167, 173, 155), width=1)
    for i, line in enumerate(["Exceptional homes.", "Exceptionally managed."]):
        tw = d.textlength(line, font=f_tag)
        d.text((cx - tw / 2, 350 + i * 48), line, font=f_tag, fill=stone)
    og.save(lib.IMG / "og-image.jpg", "JPEG", quality=86, optimize=True)

    # Favicons: "S" monogram on green
    for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
        im = Image.new("RGB", (size, size), peak)
        dd = ImageDraw.Draw(im)
        f = ImageFont.truetype(serif_path, int(size * .78))
        bbox = dd.textbbox((0, 0), "S", font=f)
        dd.text(((size - (bbox[2] - bbox[0])) / 2 - bbox[0], (size - (bbox[3] - bbox[1])) / 2 - bbox[1]), "S", font=f, fill=stone)
        im.save(SITE / name)
    (SITE / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#263B32"/>'
        '<text x="32" y="47" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-size="46" fill="#F3F0E9">S</text></svg>\n')


def write_sitemap(pages):
    today = date.today().isoformat()
    urls = []
    for p in pages:
        if p.get("noindex") or p.get("sitemap") is False:
            continue
        urls.append(f"  <url><loc>{abs_url(p['path'])}</loc><lastmod>{today}</lastmod></url>")
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")


def write_robots():
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {abs_url('/sitemap.xml')}\n")


def write_llms():
    homes = "\n".join(f"- [{h['name']}, {h['location']}]({abs_url('/our-homes/' + h['slug'] + '/')}): sleeps {h['sleeps']}" for h in C.HOMES)
    txt = f"""# Staycay Management

> {CONFIG['TAGLINE']} Staycay Management is a specialist manager of high-quality holiday homes in the Peak District, with further homes across Derbyshire and South Yorkshire. It manages 75+ holiday homes and has operated for three years.

## For property owners
- [For Owners]({abs_url('/for-owners/')}): why owners choose Staycay
- [Full Management]({abs_url('/services/full-management/')}): flagship service; guests, housekeeping, maintenance, pricing and reporting handled
- [Bookings & Revenue Management]({abs_url('/services/bookings-revenue-management/')}): pricing, listings and bookings for owners who look after the home themselves
- [How it works]({abs_url('/how-it-works/')})
- [Request a property appraisal]({abs_url('/property-appraisal/')}): free, response within 48 hours
- Management fees are not published; they are set out in a proposal after appraisal.

## For guests
- [Our Homes]({abs_url('/our-homes/')}): curated collection, booked directly on Staycay's booking site
{homes}

## Contact
- Email: {CONFIG['ENQUIRY_EMAIL']}
- [Contact page]({abs_url('/contact/')})
"""
    (SITE / "llms.txt").write_text(txt)


def write_netlify():
    staging_header = """
# STAGING: keep search engines out until launch. Delete this block at launch
# (the build removes it automatically when STAGING = False).
[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "noindex, nofollow"
""" if CONFIG["STAGING"] else ""
    toml = f"""# Generated by tools/build.py. Edit there, not here.
[build]
  publish = "site"
  command = ""

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"
    Permissions-Policy = "camera=(), microphone=(), geolocation=(), interest-cohort=()"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains"
{staging_header}
[[headers]]
  for = "/assets/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/js/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/fonts/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/img/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"

# Redirect the bare domain to www
[[redirects]]
  from = "https://staycaymanagement.co.uk/*"
  to = "https://www.staycaymanagement.co.uk/:splat"
  status = 301
  force = true

# Short, memorable links
[[redirects]]
  from = "/appraisal"
  to = "/property-appraisal/"
  status = 301

[[redirects]]
  from = "/book-a-call"
  to = "{CONFIG['CALENDLY_URL']}"
  status = 302

# OLD WEBSITE REDIRECTS: map every indexed URL from the current site to its
# closest new page before launch (see README launch checklist), e.g.
# [[redirects]]
#   from = "/old-page-name"
#   to = "/new-page/"
#   status = 301
"""
    (lib.ROOT / "netlify.toml").write_text(toml)


def check_config():
    for key, marker in PLACEHOLDER_CONFIG.items():
        if marker in CONFIG[key]:
            note_placeholder(f"{key} in tools/lib.py")


def main():
    force = "--force" in sys.argv
    check_config()
    make_brand_images()
    pages = all_pages()
    for p in pages:
        write_page(p)
    write_sitemap(pages)
    write_robots()
    write_llms()
    write_netlify()
    print(f"Built {len(pages)} pages into site/ ({'STAGING' if CONFIG['STAGING'] else 'LIVE'})")
    if PLACEHOLDERS:
        print("\nStill using placeholders:")
        for p in sorted(PLACEHOLDERS):
            print("  -", p)
        if not CONFIG["STAGING"] and not force:
            raise SystemExit("\nLive build blocked: replace the placeholders above, or rerun with --force.")


if __name__ == "__main__":
    main()
