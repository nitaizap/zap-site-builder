# site.json — the whole site in one file

Complete working example: `examples/sample-plumber/site.json`. Copy it, then replace everything.
`zs build` validates first and prints `ERROR`/`WARN` lines; fix every ERROR.

## Top level

| key | what |
|---|---|
| `site` | `{ "index": false }` – leave false; packaging decides indexing from the domain. `tagline` optional |
| `business` | facts (below) |
| `standards` | `privacy_url` (empty → the page is built from Zap's standard privacy wording; set it only when the client has its own policy), `privacy_database` (true only when the client confirmed a database; adds the database paragraph), `privacy_purposes` (extra "השימוש במידע" items; default: answering the contact forms), `privacy_email` (default `business.email_public`), `privacy_confirmed` (the client confirmed these and `business.legal_name`; clears the launch blocker), `accessibility_url` (default Zap central statement) |
| `design` | the active look (below) |
| `directions` | `{ "a": {...}, "b": {...}, "c": {...} }` partial `design` overrides for the gate preview; each has a `label` |
| `form` | `title`, `text`, `button`, `thanks` – the footer lead form |
| `footer` | `about` (one sentence), `links_title`, optional `ai_images_note` |
| `header` | `cta_label` (mobile menu button), `topbar` (default true: dark utility bar with hours/email/phone), `topbar_text` (short line: areas + years) |
| `content` | `disclaimer` (YMYL; shown under posts) |
| `smtp` | normally omit (Zap relay defaults). `test_to`: internal address that receives staging test leads |
| `logo` | `assets/logo.png` (PNG/WebP, transparent; not SVG). `logo_light`: optional light version for dark headers |
| `og_image` | image key for social sharing; default `__logo` |
| `images` | `{ key: { "src": "assets/x.jpg", "alt": "what it shows", "ai": true?, "decorative": true? } }` |
| `videos` | `{ key: { "src": "assets/hero-loop.mp4", "ai": true? } }` – hero loops only: mp4/webm, ≤ 6 MB, 4–8 s, no audio |
| `nav` | `[{ "label", "href", "children": [...] }]` – primary menu |
| `footer_nav` | flat list – the footer services column |
| `categories` | `[{ "slug", "name", "description" (140–160 chars, it is the meta description) }]` |
| `pages` | below |
| `posts` | below |

`href` forms: `page:<key>` (`page:` = home), `post:<slug>`, `category:<slug>`, `#leave-details` (the footer
form), `tel`, `whatsapp`, or a full `https://` URL.

## business

`name`, `legal_name`, `schema_type` (LocalBusiness subtype: Plumber, Electrician, LegalService, Dentist,
MedicalClinic, HVACBusiness, RoofingContractor, GeneralContractor, AutoRepair, BeautySalon, Restaurant,
Store, ProfessionalService…), `phone_display`, `phone_e164`, `whatsapp_e164`, `whatsapp_text`,
`email_leads` (required), `email_public`, `address`, `street`, `city`, `postal_code`, `geo {lat,lng}`,
`hours` (display lines), `opening_hours` (schema format `Su-Th 08:00-19:00`), `area_served` [],
`founded`, `gmb_url`, `gmb_kgmid_url`, `dpz_customer_id`, `facebook`, `instagram`, `linkedin`, `youtube`,
`author_name`, `author_credentials`.

## design

```json
{ "preset": "signature|clean|bold|editorial|soft|industrial", "hero": "split|image|centered", "header": "light|dark",
  "colors": { "primary", "primary_ink", "accent", "accent_ink", "ink", "text", "muted", "bg", "surface", "line", "dark", "dark_ink" },
  "fonts": { "heading": "...", "body": "..." }, "radius": 14, "motion": "none|subtle|lively", "tone": "light (optional: no dark grounds anywhere — hero, bands, CTA, footer; for luxury / \"no black\" requests)", "progress": "scooter|van|truck (optional: scroll bar with a riding vehicle)", "ride": "scooter|van|truck (optional: a vehicle on every page hero; hero.ride overrides, hero.ride: null removes)", "motif": "gables (optional: the brand shape as eyebrow mark + roofline above the lead band; for roofers/builders)", "custom_css": "" }
```

Fonts available (self-hosted): Heebo, Assistant, Rubik, Noto Sans Hebrew, IBM Plex Sans Hebrew,
Frank Ruhl Libre, Noto Serif Hebrew, Secular One, Suez One, Varela Round, Fredoka. See `design.md`.

## pages[]

```json
{ "key": "שירותים/איתור-נזילות", "type": "home|hub|service|about|contact|blog|page",
  "title": "menu/admin title", "excerpt": "1 line, used on cards and in schema",
  "featured_image": "imagekey", "order": 0, "noindex": false,
  "seo": { "title", "description", "keyword" },
  "sections": [ ... ] }
```

`type: blog` has no sections: it is the posts index (uses `title` as H1 and `excerpt` as intro).
Every page with sections needs exactly one `hero` (it carries the H1).

## Sections (all optional fields can be omitted)

Common: `title` (H2; `*word*` = accent colour, `
` = line break, a final `.` = accent dot), `eyebrow`
(tracked label with a rule), `intro` (sits beside the title; `head: "stack"` stacks them), `bg`
(`surface|dark|primary|accent`; default alternates plain/surface), `anchor` (id for in-page links).

| type | fields |
|---|---|
| `hero` | `title` (= H1), `lead`, `eyebrow`, `cta {label,href}`, `cta2`, `points` [3 short facts], `image`, `images` [2–3 keys: crossfading hero slider, each slide an editable image widget; first = poster], `interval` (seconds per photo, 2–10, default 4), `video` (key in `videos`; needs `image` as poster/mobile), `ride` (scooter/van/truck: a vehicle drives along the hero bottom; with a video only on phones, where the video does not play) |
| `trust` | `items: [{value, label}]` – 3–4 verifiable facts (never ratings); `style`: `band` (default, full-width stat bar) or `card` |
| `cards` | `items: [{title, text, href, image \| icon}]`, `columns` 2–4, `more {label,href}`, `item_tag`; `layout: "bento"` (photo tiles, first one large, numbered; needs images) or, without a layout, `style`: `overlay` (automatic when every item has a photo) / `classic` |
| `features` | `items: [{title, text, icon}]`, `columns`, `cta` |
| `steps` | `items: [{title, text}]` – numbered process, 3–4 items |
| `split` | `title`, `text` (HTML), `points` [], `image`, `image_side` (`start`/`end`), `image_shape` (`arch`/`square`), `badge {title, text}` (a real number), `cta`, `cta2` |
| `prose` | `html` – long text; `<h2>/<h3>` become separate editable headings; lists, tables, links ok |
| `faq` | `items: [{q, a}]` – 3+; also emitted as FAQPage schema (counts always match) |
| `cta` | `title`, `text`, `cta` (default: השאירו פרטים → footer form), `cta2` (default: phone) |
| `gallery` | `images: [keys]`, `columns` |
| `logos` | `images: [keys]` – certifications, suppliers, media |
| `posts` | `count`, `category`, `more` – latest blog posts |
| `contact` | `title`, `text`, `map` (default true) – NAP + full form + map |
| `reviews` | renders only when `business.dpz_customer_id` exists |
| `video` | `youtube_url` |
| `quote` | `text`, `by` – a real quote from the owner only |
| `marquee` | `items` [4–8 short slogan words] – big scrolling ticker on the accent colour (decorative, aria-hidden; the words must also exist as real text). `bg` default `accent` |
| `road` | `vehicles` [scooter / van / truck — illustrated SVGs from `wp/theme/zap-base/assets/vehicles/`, other names fall back to the line icon], `items` [2–4 short labels above the scene] – decorative street scene: two lanes of traffic, spinning wheels, skyline drifting behind; for delivery/transport/moving/towing clients; parked under reduced motion |
| `layers` | `items` [3–6 × `title`, `text`, `spec` (short fact: "1.5 ק״ג למ״ר")], first item = bottom layer – a build-up drawn as a cross-section (roof, waterproofing, floor, insulation) beside an editable numbered list; bands lay down on scroll. Use the client's real spec, never invented numbers |
| `route` | `items` [3–5 × `icon`, `title`, `text`], optional `vehicle` (default scooter), `cta` – "how it works" as a route: a vehicle rides the track with the scroll, each stop lights up when reached. Steps are native containers (editable); all lit without JS / reduced motion. Steps must describe the client's real process (from the brief) |

Icons: check, shield, clock, phone, wrench, tools, home, building, users, user, award, truck, droplet,
bolt, leaf, heart, chat, map, calendar, search, document, lock, sparkle, ruler, money, car, scale, medical,
star-badge, thumb, target, globe, scooter, van.

## posts[]

```json
{ "slug": "hebrew-slug", "title": "H1", "category": "cat-slug", "image": "key", "date": "2026-09-20",
  "related_page": "page key of the service that solves it", "excerpt": "...",
  "seo": { "title", "description", "keyword" }, "html": "<p>…</p><h2>…</h2>…", "faq": [{q,a}]? }
```
