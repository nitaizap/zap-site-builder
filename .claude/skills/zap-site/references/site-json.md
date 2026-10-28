# site.json — the whole site in one file

Complete working example: `examples/sample-plumber/site.json`. Copy it, then replace everything.
`zs build` validates first and prints `ERROR`/`WARN` lines; fix every ERROR.

## Top level

| key | what |
|---|---|
| `tier` | `basic` / `standard` / `premium`: the package; caps page count and which sections are allowed (`pool.md`) |
| `site` | `{ "index": false }` – leave false; packaging decides indexing from the domain. `tagline` optional |
| `business` | facts (below) |
| `standards` | `privacy_url` (empty → the page is built from Zap's standard privacy wording; set it only when the client has its own policy), `privacy_database` (true only when the client confirmed a database; adds the database paragraph), `privacy_purposes` (extra "השימוש במידע" items; default: answering the contact forms), `privacy_email` (default `business.email_public`), `privacy_confirmed` (the client confirmed these and `business.legal_name`; clears the launch blocker), `accessibility_url` (default Zap central statement) |
| `design` | the active look (below) |
| `directions` | `{ "a": {...}, "b": {...}, "c": {...} }` partial `design` overrides for the gate preview; each has a `label` |
| `form` | `title`, `text`, `button`, `thanks` – the footer lead form |
| `footer` | `about` (one sentence), `links_title`, optional `ai_images_note` |
| `header` | `cta_label` (mobile menu button), `topbar` (default true: dark utility bar with hours/email/phone), `topbar_text` (short line: areas + years), `mobile_call` (default true: phone icon in the mobile header; false only when the client asks) |
| `content` | `disclaimer` (YMYL; shown under posts) |
| `smtp` | normally omit (Zap relay defaults). `test_to`: internal address that receives staging test leads |
| `logo` | `assets/logo.png` (PNG/WebP, transparent; not SVG). A logo with a small tagline: use a crop without it (the header shows it at 56px). `logo_light`: optional light version for dark headers |
| `favicon` | `assets/favicon.png`: square PNG, 512px, from the logo's symbol (replaces the cloned base site's icon) |
| `og_image` | image key for social sharing; default `__logo` |
| `images` | `{ key: { "src": "assets/x.jpg", "alt": "what it shows", "ai": true?, "decorative": true? } }` |
| `videos` | `{ key: { "src": "assets/hero-loop.mp4", "ai": true? } }` – hero loops only: mp4/webm, ≤ 6 MB, 4–8 s, no audio |
| `nav` | `[{ "label", "href", "children": [...] }]` – primary menu |
| `footer_nav` | flat list – the footer services column |
| `categories` | `[{ "slug" (Hebrew), "name", "description" (150–160 chars, it is the meta description) }]`; required when there is a blog page. Archives at `/<blog>/<slug>/` |
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
`founded`, `phone_is_virtual` (true when `phone_display` is a Zap virtual number: adds "מספר מקשר" + Zap's explanation popup), `phone_regular` (the business's own number, shown in that popup), `gmb_url`, `gmb_kgmid_url`, `dpz_customer_id`, `facebook`, `instagram`, `linkedin`, `youtube`,
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

Any section can take a `variant` from the pool (`pool.md`); the validator rejects unknown ones.

Common: `title` (H2; `*word*` = accent colour, `
` = line break, a final `.` = accent dot), `eyebrow`
(tracked label with a rule), `intro` (sits beside the title; `head: "stack"` stacks them), `bg`
(`surface|dark|primary|accent`; default alternates plain/surface), `anchor` (id for in-page links).

| type | fields |
|---|---|
| `hero` | `title` (= H1), `lead`, `eyebrow`, `cta {label,href}`, `cta2`, `points` [3 short facts], `image`, `images` [2–3 keys: crossfading hero slider, each slide an editable image widget; first = poster], `interval` (seconds per photo, 2–10, default 4), `video` (key in `videos`; needs `image` as poster/mobile), `ride` (scooter/van/truck: a vehicle drives along the hero bottom; with a video only on phones, where the video does not play); `variant`: `cover` (full-bleed photo, centred text; `logo: true` puts the logo above the H1) / `inset` (cover as a rounded card) / `curve` (curved bottom edge); `garland: true` (festoon bulbs in two swags across the top; twinkle and sway a few seconds, then settle — events, venues, hospitality; also on `cta`, or `design.garland` for all) |
| `trust` | `items: [{value, label}]` – 3–4 verifiable facts (never ratings); `style`: `band` (default, full-width stat bar) or `card` |
| `cards` | `items: [{title, text, href, image \| icon}]`, `columns` 2–4, `more {label,href}`, `item_tag`; `layout: "bento"` (photo tiles, first one large, numbered; needs images); `variant: "framed"` (square photos in offset frames, caption below: projects) or, without a layout, `style`: `overlay` (automatic when every item has a photo) / `classic` |
| `features` | `items: [{title, text, icon}]`, `columns`, `cta`; `variant`: `aside` (rows beside a framed photo, needs `image`) / `checks` (white check tiles on a brand gradient) / `rows` (2-col horizontal cards) |
| `steps` | `items: [{title, text}]` – numbered process, 3–4 items; `variant`: `stack` (numbered dark cards in a column) / `cards` (italic numerals on a soft gradient) |
| `split` | `title`, `text` (HTML), `points` [], `image`, `image_side` (`start`/`end`), `image_shape` (`arch`/`square`), `badge {title, text}` (a real number), `cta`, `cta2`; `variant: "frame"` (text panel in an offset frame) / `"overlap"` (dark box over the photo edge) / `"card"` (light card over the photo) / `"duo"` (+ `image2` overlapping); `image_shape` also `hex` |
| `prose` | `html` – long text; `<h2>/<h3>` become separate editable headings; lists, tables, links ok; `variant: "band"` (dark gradient band) |
| `faq` | `items: [{q, a}]` – 3+; `variant`: `outline` (centred, outlined rows) / `aside` (+ `image` beside) / `dark` (dark panel); also emitted as FAQPage schema (counts always match) |
| `cta` | `title`, `text`, `cta` (default: השאירו פרטים → footer form), `cta2` (default: phone); `variant: "photo"` + `image` (half photo, half accent panel) |
| `gallery` | `images: [keys]`, `columns`; `variant: "mosaic"` (tight 4-col square grid, 4 or 8 photos) / `"strip"` (3 tall photos + `more`) / `"stagger"` (exactly 4, raised/lowered) |
| `logos` | `images: [keys]` – certifications, suppliers, media; `variant: "band"` (+ `title`, `intro`: dark band, white logo chips) |
| `posts` | `count`, `category`, `more` – latest blog posts |
| `contact` | `title`, `text`, `map` (default true) – NAP + full form + map; `variant: "photo"` + `image` = full-height photo instead of the map |
| `tiles` | `items: [{title, text, image, cta}]` – edge-to-edge photo/colour checkerboard |
| `leadbar` | `title`, `text` – rounded brand band with a one-row lead form; once per page, away from the footer lead band; `variant: "photo"` + `image` = over a full-bleed photo |
| `reviews` | renders only when `business.dpz_customer_id` exists; `variant: "photo"` + `image` (over a darkened photo) |
| `video` | `youtube_url` |
| `quote` | `text`, `by` – a real quote from the owner only |
| `carousel` | `items`: image keys or `{image, caption}` (5–12), `interval` (s, 2–10) – full-bleed swipeable photo strip; the centred slide grows, caption as a pill, arrows + counter, autoplays only on screen (pause button, stops on hover/focus). Venues, rooms, portfolios |
| `marquee` | `items` [4–8 short slogan words] – big scrolling ticker on the accent colour (decorative, aria-hidden; the words must also exist as real text). `bg` default `accent` |
| `road` | `vehicles` [scooter / van / truck — illustrated SVGs from `wp/theme/zap-base/assets/vehicles/`, other names fall back to the line icon], `items` [2–4 short labels above the scene] – decorative street scene: two lanes of traffic, spinning wheels, skyline drifting behind; for delivery/transport/moving/towing clients; parked under reduced motion |
| `layers` | `items` [3–6 × `title`, `text`, `spec` (short fact: "1.5 ק״ג למ״ר"), `kind` (base / primer / tar / mesh / membrane / white / coat / screed / tile)], first item = bottom – a to-scale roof cross-section (slab, parapet, layers turned up, flashing) with numbered leaders beside an editable list; layers draw in on scroll, tour once, and highlight with their list item on hover/tap. Use the client's real spec, never invented numbers |
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
