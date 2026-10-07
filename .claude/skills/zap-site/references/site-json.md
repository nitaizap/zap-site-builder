# site.json — the whole site in one file

Complete working example: `examples/sample-plumber/site.json`. Copy it, then replace everything.
`zs build` validates first and prints `ERROR`/`WARN` lines; fix every ERROR.

## Top level

| key | what |
|---|---|
| `site` | `{ "index": false }` – leave false; packaging decides indexing from the domain. `tagline` optional |
| `business` | facts (below) |
| `standards` | `privacy_url` (Zap PDF; empty → automatic placeholder page), `accessibility_url` (default Zap central statement) |
| `design` | the active look (below) |
| `directions` | `{ "a": {...}, "b": {...}, "c": {...} }` partial `design` overrides for the gate preview; each has a `label` |
| `form` | `title`, `text`, `button`, `thanks` – the footer lead form |
| `footer` | `about` (one sentence), `links_title`, optional `ai_images_note` |
| `header` | `cta_label` (mobile menu button text) |
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
  "fonts": { "heading": "...", "body": "..." }, "radius": 14, "motion": "none|subtle|lively", "custom_css": "" }
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

Common: `title` (H2), `eyebrow` (small line above), `intro`, `bg` (`surface|dark|primary|accent`; default
alternates plain/surface automatically), `anchor` (id for in-page links).

| type | fields |
|---|---|
| `hero` | `title` (= H1), `lead`, `eyebrow`, `cta {label,href}`, `cta2`, `points` [3 short facts], `image`, `video` (key in `videos`; needs `image` as poster/mobile) |
| `trust` | `items: [{value, label}]` – 3–4 verifiable facts (never ratings) |
| `cards` | `items: [{title, text, href, image \| icon}]`, `columns` 2–4, `more {label,href}`, `item_tag`, `layout: "bento"` (photo tiles, first one large, numbered; needs images) |
| `features` | `items: [{title, text, icon}]`, `columns`, `cta` |
| `steps` | `items: [{title, text}]` – numbered process, 3–4 items |
| `split` | `title`, `text` (HTML), `points` [], `image`, `image_side` (`start`/`end`), `cta`, `cta2` |
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
| `road` | `vehicles` [icon names, default scooter/van/truck], `items` [2–4 short labels above the lane] – decorative animated lane for delivery/transport/moving clients; static under reduced motion |

Icons: check, shield, clock, phone, wrench, tools, home, building, users, user, award, truck, droplet,
bolt, leaf, heart, chat, map, calendar, search, document, lock, sparkle, ruler, money, car, scale, medical,
star-badge, thumb, target, globe, scooter, van.

## posts[]

```json
{ "slug": "hebrew-slug", "title": "H1", "category": "cat-slug", "image": "key", "date": "2026-09-20",
  "related_page": "page key of the service that solves it", "excerpt": "...",
  "seo": { "title", "description", "keyword" }, "html": "<p>…</p><h2>…</h2>…", "faq": [{q,a}]? }
```
