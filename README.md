# Staycay Management website

Website for **www.staycaymanagement.co.uk**. It's a static site: Netlify publishes the `site/` folder automatically from the `main` branch of this repo, usually a minute or two after each push. There's no CMS and no build step on Netlify.

## How it's put together

```
site/                 What goes live. Plain HTML, CSS, JS and images.
  assets/css/site.css   All styles (brand colours and fonts are at the top)
  assets/js/site.js     Cookie consent, GA4, Calendly pop-up, form tracking, home filters
  assets/img/           Responsive WebP images (name-480.webp, -800, -1200, -1600)
  assets/fonts/         Self-hosted Cormorant Garamond + Jost (no Google Fonts calls)
tools/
  build.py              Generates every page in site/ plus sitemap, robots, llms.txt, netlify.toml
  lib.py                SETTINGS (GA4, Calendly, booking site, staging switch), header, footer, layout
  content.py            Homes, testimonials, case studies, team, Journal articles
  pages.py, pages2.py   Page layouts and copy
  make_images.py        Turns source photos into the responsive WebP sizes
  src/                  Source imagery (currently the mood board)
netlify.toml          Generated. Publish folder, headers, caching, redirects
```

**Every page is generated.** Don't edit the HTML in `site/` by hand: change the files in `tools/` and run:

```
python3 tools/build.py
```

Needs Python 3.10+ with `pip install pillow fonttools brotli`. Commit both `tools/` and `site/` and push.

The one exception is `site/assets/css/site.css` and `site/assets/js/site.js`, which are edited directly. The build adds a `?v=` fingerprint to them automatically, so browsers always get the latest version.

## Common jobs

| Job | Where |
|---|---|
| Add, remove, reorder or feature a home | `HOMES` in `tools/content.py`. List order is display order; `featured: True` puts it on the homepage; `categories` drive the filters |
| Change a home's photos or booking link | `images` and `booking_url` on that home |
| Add a testimonial or case study | `TESTIMONIALS` / `CASE_STUDIES` in `content.py`. `contexts` controls which pages show it |
| New Journal article | Add to `ARTICLES` in `content.py` (body is HTML) |
| Team | `TEAM` in `content.py` |
| GA4 ID, Calendly link, booking site, email | `CONFIG` in `tools/lib.py` |
| New photos | Put JPEGs in `tools/src/photos/<name>.jpg`, run `python3 tools/make_images.py`, then build |

## Forms (Netlify Forms)

Two forms, both detected by Netlify automatically: **appraisal** (Request a Property Appraisal) and **contact**. Both land on `/thank-you/`.

In Netlify: **Forms → Enable form detection**, redeploy, then **Forms → Form notifications → Email** to `enquiries@staycay.uk` for each form. Every submission is also kept in Netlify as the lead record, and can be exported as CSV or pushed to a CRM or Google Sheet with a Netlify webhook or Zapier.

Each submission includes hidden attribution fields: landing page, referrer, UTM source/medium/campaign, and the page the form was sent from.

## Analytics and tracking

GA4 only loads after a visitor accepts cookies (UK GDPR / PECR). Events sent:

| Event | When |
|---|---|
| `appraisal_form_start` | First interaction with the appraisal form |
| `appraisal_form_submit` | Appraisal form passes validation and is sent |
| `generate_lead` | Thank-you page after an appraisal (**mark as key event**) |
| `contact_submit` | Thank-you page after the contact form |
| `calendly_open` | 15-minute call pop-up opened |
| `calendly_booking` | Call actually booked in Calendly (**mark as key event**) |
| `booking_click` | Guest clicks through to the direct-booking site (with `property`) |
| `cta_appraisal`, `guest_route` | Key owner and guest CTA clicks (with `cta_location`) |
| `homes_filter` | Filter used on Our Homes |

In GA4, register `cta_location`, `property` and `form_name` as custom dimensions, and mark `generate_lead` and `calendly_booking` as key events.

## Before launch

The build lists every placeholder still in use and refuses to make a live build until they're gone.

1. **Settings** in `tools/lib.py`: real `GA4_ID`, `CALENDLY_URL` and `BOOKING_BASE`.
2. **Homes**: replace the six sample homes with Staycay's curated selection, real photos and booking URLs. Set `placeholder: False` on each.
3. **Testimonials, case studies and every figure** must be real and approved by Staycay. The only figures verified so far are 75+ properties and 3 years operating.
4. **Team**: names, roles, bios, photos. **About**: the story copy.
5. **Journal**: replace or approve the three sample articles.
6. **Legal**: privacy and cookie policy approved, with company name, number and address.
7. **Logo**: swap the text wordmark (`brand_html` in `lib.py`) and favicon for final brand files.
8. **Old site redirects**: list every URL on the current site (Search Console → Pages, or a crawl) and map each to a new page in `write_netlify()` in `build.py`.
9. **Calendly**: in Calendly, check the event allows embedding and that the confirmation page is not set to redirect (so the booking is tracked).
10. Staycay signs off the staging site.
11. Set `STAGING = False`, run the build, push. This removes the preview bar, the `noindex` tags and the `X-Robots-Tag` header.
12. Add the domain in Netlify, point DNS, submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.

## Ownership

Staycay should own the domain, DNS, the GitHub repo (or have admin on it), the Netlify site, GA4, Search Console, Calendly and the booking platform. Nothing here is proprietary: it's plain files any developer can pick up.

## Notes for editing

- Keep each `<title>` under ~60 characters and descriptions under 160. The build sets these per page in `pages*.py`.
- Structured data (Organization, Service, FAQPage, BreadcrumbList, VacationRental, BlogPosting) is generated from the same content, so FAQs and schema stay in step.
- Don't publish management fee percentages anywhere (client requirement).
- Future location pages (e.g. a page per area) should only be added with genuinely distinct content, to avoid thin or duplicate pages.
