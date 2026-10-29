# The template pool — mix, don't copy

Every client gets a site that fits the business, assembled from a shared pool, never a fixed
template. A site is a combination of three independent layers; vary all three:

1. **Package** (`tier` in site.json): how big and how simple.
2. **Style kit**: `preset`, `tone`, fonts, palette, radius, motion, hero layout (`references/design.md`).
3. **Section variants**: the order of the sections and the `variant` each one uses (the catalogue below).

The same variant under another preset looks like a different site, so the pool multiplies. The look still
comes from tokens and presets, and the variants only change arrangement; every variant passes `zs qa` under
every preset.

## Packages

| `tier` | pages (privacy/blog not counted) | allowed | use it for |
|---|---|---|---|
| `basic` | up to 5 | simple sections only: no `road`, `route`, `marquee`, `video`, `posts`; hero = one still photo | the "אתר בייסיק" package: one-page-feeling sites like the restaurant references |
| `standard` | up to 12 | the whole pool | most service businesses |
| `premium` | no cap | the whole pool + hero video/slider, motion `lively`, Weave video | flagship builds (the benchmark level) |

Leave `tier` out only for legacy sites. The validator stops the build when a site breaks its package.
Basic sites must still meet every other rule (QA 0 errors, real facts, Zap standards).

## Section variants (`variant` on a section)

| type | variant | what it looks like | source | needs |
|---|---|---|---|---|
| `split` | *(default)* | text + photo, optional badge, arch/square shape | engine | |
| `hero` | `cover` *(per section; overrides the site's hero layout)* | full-bleed photo, centred statement, `logo: true` puts the logo above the H1 (white chip without `logo_light`) | basic-site references | `image` |
| `hero` | `inset` | the cover hero as a rounded card inside the page margins | template 2 | `image` |
| `hero` | `curve` | full-bleed photo hero with a curved bottom edge, text at the start side | template 4 | `image` |
| `split` | `card` | light text card overlapping the photo (shadow, rounded) | templates 3, 5 | `image` |
| `split` | `duo` | tall photo with a second smaller photo overlapping its corner + an accent block | template 4 | `image`, `image2` |
| `split` | `image_shape: "hex"` *(shape, not a variant; combines with any split)* | hexagon-masked photo | template 6 | `image` |
| `split` | `overlap` | dark centred text box overlapping the photo's edge, accent title | basic-site references | `image` |
| `split` | `frame` | text in a panel inside a thin offset brand-colour frame, photo beside it | template 1 "קצת עלינו" | `image` |
| `cards` | *(default)* `overlay` / `classic` / `layout: bento` | photo tiles with text over the photo / boxed cards / bento | engine | |
| `cards` | `framed` | square photos each with an offset hairline frame, brand-colour caption below ("projects") | template 1 "גלריית פרויקטים" | images |
| `features` | *(default)* | icon grid | engine | |
| `features` | `aside` | 3–4 icon rows stacked beside a framed photo ("למה לבחור בנו") | template 1 | `image` |
| `features` | `checks` | white check tiles on a brand gradient ("יתרונות"), short titles only | template 1 | |
| `gallery` | *(default)* | grid, first photo large when 5+ | engine | |
| `gallery` | `strip` | one row of 3 tall photos (only the first 3 render) + `more` button to the gallery page | basic-site references | 3+ images, `more` |
| `gallery` | `stagger` | four tall photos, alternately raised and lowered | template 2 | exactly 4 images |
| `gallery` | `mosaic` | tight 4-column square grid, no gaps (2 on mobile), 8 photos | template 1 "גלריה" | 4 or 8 images |
| `faq` | *(default)* | soft cards, round +/- icon | engine | |
| `faq` | `outline` | centred title, outlined brand-colour rows | template 1 | |
| `steps` | `stack` | numbered dark cards stacked in one column, numeral behind a divider ("שלבים מרכזיים") | template 3 service page | |
| `steps` | `cards` | white cards with big italic numerals on a soft brand gradient ("תהליך") | template 4 service page | |
| `features` | `rows` | 2-column horizontal cards, check icon behind a divider ("יתרונות") | template 4 service page | |
| `prose` | `band` | a long-text block on a dark gradient band | template 3 service page | |
| `reviews` | `photo` | the Zap reviews widget over a darkened photo (renders only with `dpz_customer_id`) | template 2 | `image` |
| `faq` | `aside` | questions beside a tall photo (photo hidden on phones) | template 4 | `image` |
| `faq` | `dark` | questions on a rounded dark gradient panel, accent questions | template 6 | |
| `logos` | `band` | dark band: title on one side, white logo chips on the other | template 6 | logo images |
| `contact` | *(default)* | NAP + form + map | engine | |
| `contact` | `photo` | NAP + form beside a full-height photo, no map | template 1 | `image` |
| `cta` | `photo` | half photo, half accent panel with the action ("להזמנת שולחן") | basic-site references | `image` |
| `tiles` | *(type)* | edge-to-edge checkerboard: photo half + dark/accent half, sides alternate; `items: [{title, text, image, cta}]` | basic-site references | every item an image |
| `leadbar` | *(type)* | rounded brand band with a one-row form (name, phone, email) mid-page | template 1 | once per page, not next to the footer lead band |
| `leadbar` | `photo` | the same form centred over a full-bleed darkened photo | templates 3, 5 | `image` |
| `hero` | `form: true` *(option, any hero)* | a one-row lead-form card (name, phone, email) along the hero's foot; hidden on phones (the hero buttons + footer form stay); not on the contact page | Zap portfolio: legal / medical ProX (17, 19, 20, 37, 56, 63) | `form.email_leads` |
| `cards` | *(item fields)* `links` | several outline buttons per card (book / order / menu), stacked full width on phones | Zap portfolio: chains 26, food hall 28 | |
| `cards` | *(item fields)* `price`, `meta` | listing cards: a price line and a row of spec chips under the title (rooms · floor · m², pack size) | Zap portfolio: real estate 52, products 29 / 11 | |
| `pricelist` | *(type)* default | menu / fee list: groups of dotted-leader rows (name … price, a line under), two columns | Zap portfolio: restaurants (menus), notary fees | the client's own prices |
| `pricelist` | `tiles` | one dark tile per item, the price in a chip | Zap portfolio: vet 36, opticians | |
| `facts` | *(type)* | intro text beside a white fact card of label: value rows | Zap portfolio: zimmers 53, specs | real facts only |
| `team` | *(type)* default / `rows` | round portraits on cards; one or two people (or `rows`) = wide bio rows | Zap portfolio: law firm 20, vets 36 | the people's own photos |

Hero layouts (`split`, `image`, `centered`), `trust` styles, `marquee`, `road`, `route`, `steps` and the
presets are documented in `site-json.md` and `design.md`; they are part of the pool too.

**Adding to the pool** (engine work, own branch + PR): one entry in `VARIANTS` (`engine/sections.py`), markup
only if the arrangement truly needs it, CSS in `wp/theme/zap-base/assets/pool.css` scoped to `.zs-v-<name>`,
a row in this table, then `zs build sample && zs qa sample` with 0 errors and a look at desktop + mobile.

Sources so far: Zap's own client portfolio (`portfolio.md`: 40 live sites by industry, packages, styles), the six Zap Figma "תבניות" templates (`benchmark/zap-template-<n>-full.jpg`: 1 pergolas,
2 restaurant/events, 3 construction, 4 vet clinic, 5 metal works, 6 beauty clinic; each also has about,
contact, services/service, blog/post pages in the file) and the
basic-site references (`benchmark/basic-*.jpg`: four restaurant sites on Zap's basic package). What makes those read as "basic done well": one strong food/venue
photo per block, big centred statements, two or three colours (dark + one warm accent), very few words, a
booking/order action repeated, and a centred contact block with hours. Their full-width map is not copied
(it costs speed and adds little); `contact` keeps the map optional.
Figma copy with edit access: figma.com/design/PjcbiKwCivnwxqHPg95Nhw (pages = templates; the home frame is the
first frame on each page). New templates: extract them into variants the same way. Inner pages: page heroes take `cover`/`inset`/`curve` too and render as short
banners. Not extracted: the post sidebar (form + recent posts, share icons) and template 2's event form fields
(event type, date, guests), which would need theme/plugin work.

## Lessons from earlier builds (no reference sites)

No previous client site is kept as an example to copy (user decision, 26/10/2026): every site is composed
from the base templates, the pool and its own brief. What made the approved builds work:

- a three-line brief first (subject, audience and moment, the page's one job), then a base template + deviations
  taken from the client's world (logo colours, the client's own place or material);
- one font family, one bold element, everything else quiet;
- 8–10 home sections, no two neighbours alike, each a different variant; real photos in every slot;
- no generated-look tells; motion `subtle`;
- `zs qa` 0 errors and `zs seo` 0 FAIL before anyone sees it.

## Base templates (from the team's method)

Every site starts from **one of the six Zap templates** and names its deviations. Set `design.base_template`
(1–6); `zs pool` reads it. A direction = base template + named deviations from the client's world: the palette,
the font, and **one** bold element. Write them in NOTES.md: "from template 5: header, section order, form;
changed: palette (brand brass), hero `curve`, gallery `stagger`".

| # | demo industry | look | standout sections | fits |
|---|---|---|---|---|
| 1 | pergolas / outdoor | navy on white, offset hairline frames | framed about, overlay service cards, framed projects, check tiles on blue | home improvement, outdoor, installers |
| 2 | restaurant / events | beige surfaces, slate blue, rounded | inset hero, staggered photo row, beige event cards, reviews over a photo, event form | restaurants, venues, catering, events |
| 3 | construction | dark navy + orange, photo-heavy | light card over the photo, image-top service cards, 2×2 icon cards, form over a photo | contractors, renovation, heavy trades |
| 4 | vet clinic | white + pink, soft, rounded | curved hero, two overlapping photos, check badges on cards, FAQ beside a photo | clinics, pets, kids, wellness |
| 5 | metal works | white + red, dark overlay tiles, red gradient | overlay service tiles, white cards on a red gradient, form over a photo | industry, workshops, technicians |
| 6 | beauty clinic | teal + rose, dark navy bands | hexagon photos, logo band, rounded promo banner, dark FAQ panel | beauty, aesthetics, boutique services |

Template screenshots: `benchmark/zap-template-<n>-full.jpg`.

**The templates' shared language is the default:** header = logo, menu, phone; home order about → services →
why us → FAQ → form → footer; footer = quick links / services / contact. Deviate on purpose, not by accident.
Show what the client really has, and nothing they don't:
- the social bar shows only the networks the client really has (none → no bar);
- a WhatsApp button only if there is a WhatsApp number;
- "מספר מקשר" under the phone only if there is a Zap tracking number.

**Never use an image from the templates** (Figma or a crop of the screenshot): they are Freepik placeholders that
show where an image goes, its ratio and shape. Images come from the client, the old site, GMB or AI (`images.md`).

**What the templates don't give, we still design:** mobile (they have no mobile frames; check 390), real copy
(they are lorem), and the type scale. The templates use Light (300) body text: allow it in Hebrew only at
≥18 px with AA contrast, otherwise Regular.

**Two clients in the same industry on the same base template must differ visibly** (palette or the bold
element). `zs pool` warns when the base template and the primary colour both match another client.

**Density (the team's approved sites, measured 22/10/2026):** 9–13 sections on the home page and 13+ real images
across the directions. A home page far below that is under-designed, not "clean".

**Redesigning a site that already ranks** (check Search Console/Ahrefs at intake): keep its home page block for
block (same order, images, link targets, wording) and dress the blocks in the new style. A fresh layout with the
same words was rejected on a real client. Here that means choosing variants for the existing blocks, not a new
order, and listing "באתר הקיים ↔ בעיצוב החדש" in NOTES.md.

## Mixing rules (anti-formula)

- **Start from the business, not from the pool.** Pick sections for what this client must prove (a
  restaurant: menu, atmosphere, booking; a trade: speed, trust, area; a clinic: calm, credentials). Then pick
  the variant that best tells it.
- **No two neighbours alike**: never the same type or the same "shape" (two framed sections, two
  photo grids) back to back; one brand-colour band (`checks`, `leadbar`, `cta`, `marquee`) per screenful.
- **At most two variants from the same template on one page**, so no site reads as a copy of one template.
- **Every direction in the gate differs in at least one variant as well as preset/hero.**
- Before the gate run `bin/zs pool <slug>`: it compares the home-page recipe and design levers with every
  other client on a `site/*` branch (`git fetch` first). A "too close" warning means swap variants or a
  lever, and write the reason for each choice in NOTES.md (one line per section).
