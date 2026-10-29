# Zap's own portfolio: what real client sites look like, per industry

Source: zapgroup.co.il/services/websites/#portfolio, captured 29/10/2026 by a browser agent (the cloud session is
blocked by Cloudflare; brief for the agent: `docs/PORTFOLIO-CAPTURE.md`). 363 items (Wix 291, WordPress 72);
40 live sites screenshotted on desktop and at 390 px. `benchmark/portfolio/index.csv` lists every item (name, URL,
category, package); `benchmark/portfolio/NN-<slug>.jpg` is a first screen, `-page.jpg` the top of the home page.

Use it like the templates: **structure and conventions per industry**, never a look to copy, never their photos.
39% of the first 75 portfolio links are dead sites, so verify before showing one to a client.

## Zap's packages → our `tier`

| Zap package | what Zap sells | share of the portfolio | our `tier` |
|---|---|---|---|
| BasiX (199 ₪/month) | a site from a template, 2 revision rounds, 2 updates/month | 171 (restaurants 85, local businesses 62) | `basic` |
| DeliverX (199 ₪/month) | BasiX + online delivery ordering, photographer, WhiteMenu | restaurants only | `basic` + order links in hero, `cta` and `header.mobile_bar` |
| ProX (399 ₪/month) | up to 12 pages, logo design, 2 features of choice, 3 rounds | 159 (legal 27/30, medical 32/46, e-commerce, zimmers) | `standard` |
| "אתרים עם קידום SEO" | ProX + keyword research, content growth, monthly report | quote | `premium` |

## What every industry does (the conventions a client expects)

**Everywhere (all 40 sites):** a fixed action bar on phones (call, WhatsApp, then Waze / booking / delivery) →
`header.mobile_bar`; hamburger on one side, logo centred, round phone button on the other; a short form before the
footer; Waze on the address.

| industry | home order seen | CTAs | engine recipe |
|---|---|---|---|
| **restaurants** (6–8 sections, Basix) | full-bleed food slideshow with the logo centred, H1 + 1–3 buttons → about split on a dark band → photo strip → gallery + "more" → contact band with **hours by day** and the buttons again → form | הזמנת שולחן, הזמנת משלוח, תכנון אירוע, Waze (every site), call | hero `cover` + `logo: true` + `images`; `split overlap`; `gallery strip`; `pricelist` (menu with categories; the client's own prices only); `tiles` for many short facts; `cta photo` "להזמנת שולחן"; `header.mobile_bar: ["waze", {label: "הזמנת שולחן", href: <Tabit/Ontopo>, icon: "calendar"}, {label: "משלוח", href: …, icon: "bag"}]` |
| **legal** (ProX) | top info bar → portrait / justice hero with a **lead form card** → about (portrait + bio) → practice areas as zig-zag rows or icon cards on navy → why us → articles → form | לייעוץ ראשוני, לקביעת פגישה, WhatsApp | hero `form: true`; `split frame` about; `cards` (practice areas, linked) or `tiles`; `team` for partners; `posts`; navy + gold (`editorial` / Frank Ruhl Libre for boutique) |
| **medical** (ProX) | hours bar → doctor hero + **form card** → credentials about (portrait, positions, memberships) → treatment cards → why us → testimonials → contact boxes | תיאום תור, לקביעת תורים + number | hero `form: true` + `variant: curve`; `split` about with `points` = credentials; `features`; `team` for clinics; `pricelist variant: tiles` for vets / opticians / treatments with public prices |
| **trades / local services** | photo hero with call + WhatsApp → **authorised-dealer / client logos** → about → services (photo cards or zig-zag) → why us 3×2 on dark → gallery → reviews → form on a photo | the number as the button, WhatsApp, "לתיאום" | `logos variant: band` right under the hero; `cards` overlay; `features checks`; `leadbar photo`; `route`/`steps` for the process |
| **B2B / industrial** | hero (collage, slider or video) → clients → about with counters → services → products → numbered reasons → form | דברו איתנו, הצעת מחיר, לתיאום הדגמה | `logos band`; `trust`; `cards` listing mode (`price` optional, `meta` = specs); `steps cards` |
| **zimmers / venues** (Weekend) | slideshow hero + amenity tiles → intro + **fact card** (units, rooms, guests) → photo strip → gallery → contact over a garden photo | הזמינו עכשיו + phone | hero `images`; `facts`; `carousel`; `gallery mosaic`; `contact photo` |
| **real estate** | family hero → about → **listing cards** (rent / sale: photo, title, price, rooms · floor · m²) → values → form | | `cards` with `price` + `meta`, `more` to the full list |
| **e-commerce** | promise strip → curved hero → category tiles → products grid → form | | out of scope for the engine (a shop needs WooCommerce); category tiles = `cards` overlay |

## Visual styles seen (tokens to reach for, not presets to copy)

| style | sites | palette and type | engine levers |
|---|---|---|---|
| steakhouse noir | 10, 23, 46 | #111–#191919, gold #bc9554 → #e6c88f pills, condensed display heads, script subline | `bold` / `signature`, dark grounds, accent = gold, `radius` 999 for pills |
| rustic earth | 6, 9 | brown #694f36 / #332518 bands with cream #ede6d9 | `soft`, `tone: light` off, surface = cream |
| garden bistro | 7, 12 | deep green #07642e / #3e5543 with cream #eeedd6 | `editorial`, serif wordmark, light |
| navy & gold counsel | 17, 27, 51 | navy #0c2342–#2c3a57, gold #c9a66b–#dabb8d | `editorial` or `signature`, accent gold |
| noir boutique (legal) | 49 | #0e0e11 with cream #f6f4ef, gold #d4af37, 16 px radius cards | `signature`, `radius` 16 |
| clinical soft curve | 19, 56, 63 | white + pale tint, one strong colour (green, plum, blue), curved hero bottoms | `soft` / `clean`, hero `curve` |
| olive retreat (zimmers) | 53 | cream #f5f3ed / #e8e4d9, olive #556b2f, brown #8b5a2b | `soft`, `tone: light` |
| slant trades | 3, 13, 61 | navy / red / teal bands, white rounded tiles | `industrial` / `clean` |

## Seen, not built (yet)

Branch / venue cards with several links each (chains: 26, 28), a kosher-certificate chip in the header (9, 21),
day-by-day hours block inside the contact band, vertical service tabs (13), video testimonials (61), a comparison
table (use `prose` with an HTML table), property filters, gift-card floating button. Candidates for the pool when a
client needs one: add them generically (`pool.md` → Adding to the pool).

**Avoid** (seen in the portfolio, fails Zap QA or our rules): a full-screen video hero with no H1 (26), parallax
bands that render blank, text baked into images, ratings pills ("★ 5.0 · 28 חוות דעת") on the page.
