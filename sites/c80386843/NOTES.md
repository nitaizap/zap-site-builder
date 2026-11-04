# מסגרית Dream from Steel (80386843) — notes

Branch `site/c80386843`. Built in automatic mode from `intake.json` + `brief/`, no gate (the skill's
automatic mode: sitemap from the spec, direction chosen here, open points collected in `OPEN-ITEMS.md`).

## Facts, with a source for each

| fact | value | source |
|---|---|---|
| business | מסגרית Dream from Steel | spec sheet §2 |
| owner / contact | אופיר אלחנתי | spec sheet §2, §3 |
| years in the trade | 20 | spec sheet §2 (שנות פעילות), repeated in §5 |
| address | הרימון 89, נווה ימין | spec sheet §3 |
| service area | כפר סבא | spec sheet §3 (אזורי שירות) |
| hours | א׳–ה׳ 07:00–20:00 | spec sheet §3 |
| phone for the site | 050-9254010 | spec sheet §3 (טלפון לאתר) |
| Zap tracking number | 072-2594285 | spec sheet §3 (מספר מקשר זאפ), and the Dapei Zahav listing |
| WhatsApp | 050-9254010 | spec sheet §4 |
| e-mail (site + leads) | ofir.elc@gmail.com | spec sheet §3 |
| what the business does | metalwork and manufacture of metal products, everything custom, planning to finished product | spec sheet §5 |
| customers | private clients, architects, carpenters, drone-market and aviation-market companies | spec sheet §5 |
| existing site | none: only the Dapei Zahav listing d.co.il/80386843/33060/ | spec sheet §2, intake |
| logo | the Dream from Steel badge: slate hexagon, orange rim | the client's own Dapei Zahav listing, `img.d.co.il/Customers/80386843/…png` (found 02/11; see IMAGE-SOURCES.md) |
| brand colours | orange `#d15301` and slate `#2c3e4f`, sampled from the logo's pixels | the logo file above |
| "sites you liked" | not given | spec sheet §6 (blank) |
| photographs | none supplied; generated or stock imagery sanctioned by the sites team | spec §7 blank; `F:\SiteContent\80386843` empty (intake session); Noam 02/11 (`inbox/2026-11-02-feedback.md`) |

Nothing on the site comes from anywhere else. No founding year is stated (20 years is the spec's own
wording, not a date); no licences, no prices, no ratings, no counts.

## Design brief (the three lines)

- **Subject:** steel. Profiles, angles, plate and bar cut, welded and assembled to a drawing.
- **Audience and moment:** someone who has already failed to buy the thing off a shelf. A private client with
  an odd measurement, an architect holding a detail, a carpenter needing a metal part, a drone or aviation
  company with a spec and a tolerance. They arrive asking "can this be made at all".
- **The page's single job:** get a description of the job to Ofir (call, WhatsApp or the form).

## The direction that was built, and why

| lever | choice | why |
|---|---|---|
| `tier` | `standard` | the spec names no package, and its own sitemap is 6 pages, over basic's cap of 5. Decided 02/11: keep all six, so `standard`. No premium-only feature is used |
| `kit` | `frame` | the page sits inside a brand-orange frame with offset photo frames: `pool.md` files it under "studios, galleries, design-led trades", which is what a shop whose whole argument is one-off bespoke work is. **Changed from `sidebar` on 03/11** for uniqueness headroom, see the critique section below |
| `archetype` | `story` | chapters of the craftsman's story: origin ("אין אצלנו קטלוג", Ofir's 20 years), method, process, what you can order, material, who it is for, then the invitation. With no portfolio to show, the story is what carries the page. **Changed from `statement` on 03/11**, see the critique section below |
| `base_template` | 1 | navy-on-white, offset frames. **Deliberately not template 5** (the metal-works demo, white + red): the obvious pick for a metalworker and already used by the pilot branches |
| preset | `editorial` | serif headings, hairlines, no shadows: craft rather than heavy industry |
| palette | primary orange `#b84606`, accent steel blue `#6b8ca6`, ink slate `#1b2a36` | **sampled from the client's own logo** once it was found on their Dapei Zahav listing. The logo's orange is `#d15301`; it is deepened to `#b84606` so white text clears 4.5:1 and the chapter headings clear 4.5:1 on the surface tint, which `design.md` allows ("a darker primary only if contrast needs it"). The logo's slate `#2c3e4f` carries the text and the footer. The site was built first on petrol steel and brass, chosen as the most distant free colour; that was replaced the moment the real brand turned up |
| fonts | Heebo / Heebo | **Frank Ruhl Libre / Assistant → Alef on 03/11** (client feedback: "generally use a different font"), **→ Heebo on 04/11**: Alef turned out to have old-style figures as its only figure set, with 3, 4, 5, 7 and 9 below the baseline and no `lnum` to switch them off, which wrecked the phone number and "20 שנה". Heebo is the same kind of sturdy plain Hebrew sans, self-hosted, on the readable-body list, variable 100-900, and the heading font of no other client (the pool measure looks only at the heading). Full reasoning in the 04/11 polish pass below |
| radius | 10 | sharp (2) was the first choice, but it made the measured page frame identical to mehirut-haor's |
| hero | section variant `curve` over the workshop bay | the story archetype's opening: the photo carries the page in, the H1 sits on it, and the curved bottom edge hands over to the first chapter |
| motion | `subtle` | the brief asks for no motion |

**The one bold thing:** the H1 at full width over the workshop bay, with the whole page then running as a
single explained argument. Nothing else competes with it.

Home: `hero:curve → chapters → prose:band → split:overlap → steps:stack → cards:framed → collage →
facts → leadbar:photo → cta → faq:dark` (11 sections, resequenced into the story's beats on 03/11; no copy
was added, removed or rewritten, only reordered). Components picked for what none of the other clients use:
`chapters`, `prose:band`, `facts`, `collage`, `steps:stack`, `faq:dark` appear on no other client site.

### Critique before delivery, and what changed after it

- the `overlay` section opened with a near-square phone crop of a landscape photo, upscaled and soft
  (`pool.md`: wide photos never go into tall crops on phones) → replaced with `split:overlap`
- the home measured 43-50% like patoccina, mehirut-haor and bella-mare on the first build (brass palette,
  `frame` kit, `cards`/`features:checks`/`split:card`/`faq:outline`, the components everyone uses) →
  palette, kit and seven of the eleven components changed. Final: 38% (mehirut-haor), 35% (white-villa)
- the sidebar kit leaves the title column empty on a section without a title (the service-page `prose`).
  Kept: every section's content then starts at the same x, which is the kit's point

### Uniqueness pass, 03/11 (the readiness run)

The 02/11 build measured **38% / 34% / 39%** and was recorded as green. Re-measured on 03/11 against the
pool as it actually stood, the home was **40.4% like `c80220135`** — over the 40% ERROR line, not under it.
The two sites had drifted together while both were being built: `sidebar` gave a dark 3-column footer and
`c80220135` has one too, and the shared `facts`/`cards`/`cta` vocabulary and the matching page frame did the
rest. Four of the six measured chrome traits were identical.

`bands` and `proof` were not available to replace them: `c80220135` holds both and is one of the last three
sites, which `zs pool` refuses outright. What was changed instead:

- **kit `sidebar` → `frame`**, which moves the footer to light, puts the page inside a brand-colour frame
  (`page.edge`) and reframes every photo. The earlier build had tried `frame` and dropped it, but that was
  `frame` *with the brass palette and the components everyone uses* (`cards`, `features:checks`,
  `split:card`, `faq:outline`); with the logo's orange and this component set it measures far apart
- **archetype `statement` → `story`**, and the eleven home sections resequenced into its beats
- **hero variant `curve`**, services cards to `framed`

Measured after the change, against the live pool including the siblings building right now:

| other client | before | after |
|---|---|---|
| `c80220135` | **0.404** (ERROR) | **0.274** |
| `mehirut-haor` | 0.375 | 0.375 |
| `c2910210` | - | 0.351 |
| every other client | ≤0.32 | ≤0.32 |

(`c80220135` also moved while this ran: that agent returned their site to its documented petrol palette, so
the pair is measured here against their 6b285c8. The final figures above are measured after PR #74 was
merged in, which changed the home's first H2 from the accent to white and so moved the measured `ink`.)

Worst case is now **0.375**, against `mehirut-haor`, a finished site and not one of the three joining the
pool. `atelier` (0.39, and it pulled `patoccina` and `kisos-beach-club` up to 0.36) and `magazine`
(two QA errors, and `c80220135` back to 0.342) were both measured and rejected. Nothing under
`fingerprints/` and no threshold was touched.

## Research done in the build session

The intake session reported the Dapei Zahav listing as holding only a generic category cover. Reading both
listings for this customer id directly (`/80386843/33060/`, category מתכות, and `/80386843/30120/`, category
מסגריות) turned up more:

- **the client's logo**, in Zap's own `Customers/80386843/` folder, not a category cover. It is now the
  site's logo, favicon and palette. The playbook's warning ("missing a logo that sat in a directory's
  gallery cost a round") was exactly this case.
- **the phone question, partly settled**: the only contact button on either listing is 072-2594285, and the
  page itself says Zap routes it as a virtual number. The 050 appears only inside the share-button text. The
  WhatsApp button there (972559686670) is a Zap service number, not the client's.
- **no legal name anywhere**: no company name, ח.פ., ע.מ., בע"מ or עוסק מורשה on either page, and the
  owner's name does not appear. The privacy-page blocker genuinely needs the client.
- **no reviews**: both listings say "אין עדיין חוות דעת", so no `reviews` section was added even though
  `dpz_customer_id` is set. It would render empty.
- the second listing's description drops "ייצור מוצרי מתכת" from the first sentence; the fuller wording on
  the 33060 listing is the one the spec sheet also carries, and that is what the site uses.

## Keyword map

| page | keyword | H1 | slug |
|---|---|---|---|
| home | מסגרייה בכפר סבא | מסגרית Dream from Steel | `/` |
| service | מסגרות בהתאמה אישית | מסגרות בהתאמה אישית | `/מסגרות-בהתאמה-אישית/` |
| service | ייצור מוצרי מתכת | ייצור מוצרי מתכת ייחודיים | `/ייצור-מוצרי-מתכת-ייחודיים/` |
| service | תכנון מוצרי מתכת | תכנון מוצרי מתכת | `/תכנון-מוצרי-מתכת/` |
| about | מסגרייה בנווה ימין | אודות מסגרית Dream from Steel | `/אודות/` |
| contact | צור קשר מסגרית Dream from Steel | צור קשר | `/צור-קשר/` |
| blog | מדריכים לעבודות מתכת | בלוג | `/בלוג/` |

Volume and KD: unknown (no Ahrefs in this session, and no SERP research was possible for a business with no
web presence to compare against). The terms are the spec's own page names, which is what the client and the
sites team agreed on.

Posts (3, written from the brief's own material, no invented facts): choosing raw material, what to prepare
before ordering, and the route from drawing to finished product. Each links the service that solves it.

## The 👁 rows of the SEO checklist

- **1 מספר מקשר:** 072-2594285 is shown with `phone_is_virtual`, so the "מספר מקשר" link and Zap's standard
  explanation render beside it. Confirmed by eye on `/צור-קשר/`.
- **8 FAQs:** read against this table. Every answer is the spec's own content or a process statement; the
  one about delivery time says the date is given with the quote, and promises no number.
- **9 client images:** none exist. Four AI atmosphere images, recorded in `IMAGE-SOURCES.md`.
- **+1 phone/mail/address:** site shows 072-2594285, ofir.elc@gmail.com, הרימון 89 נווה ימין. Matches the
  spec, except that the spec's "טלפון לאתר" is the 050 line (see OPEN-ITEMS).
- **+6 1280 and mobile:** looked at 1440, 1280 and 390. Mobile pass run over all 11 URLs: no horizontal
  scroll, no header overlap, no wrapped buttons.

## Engine and theme bugs found while building this site (fixed on main, by PR)

| PR | what |
|---|---|
| #54 | `zs qa` crashed for every site: `fingerprints/clients.json` (the registry index) was read as a client fingerprint |
| #57 | a light panel inside a colour band inherited the band's white text (`split:frame` 1.00, `features:rows` 1.11) |
| #61 | the H1 word-splitter reversed a multi-word Latin name in an RTL heading: "מסגרית Dream from Steel" painted as "מסגרית Steel from Dream" |
| #62 | the phone header reserved no width for the burger, so a long text brand (a client with no logo) ran under it |
| #74 | the `split:overlap` card paints its own ground with `--c-dark` but hard-coded its title to `--c-accent`: accent-coloured words on a dark ground, the pattern `qa-rules.md` records as a straight Zap QA rejection. `zs qa` measures the 4.5:1 floor and this pairing cleared it by luck (steel blue `#6b8ca6` on slate `#16222c` = **4.56:1**), so the gate never saw it. Found by eye at 1280 on 03/11: it was the only title on this site that was not white on its dark card |

Known and not fixed: the `overlay` section's phone box is `56vh` while the browser picks a source by width,
so a landscape photo in it is upscaled and soft. Avoided here by not using `overlay`.


### Design pass, 03/11 (client feedback on the live site)

- hero: the curve hero was 863px tall with 263px of text pushed to one side. Now about 480px at 1440x900; headline, lead and buttons across the start column, the three facts as a plate on the open side (desktop), tick marks made visible on the photo. Phones keep the stacked, centred layout
- three-across service row: icon, title and text centred on one axis, titles larger, hairlines between the cards, no side padding skew; the section intro stacked under its title
- ticks on the dark `split:overlap` card were dark on dark: now white
- all in `design.custom_css`; no shared theme change. Uniqueness: worst case 0.375 (mehirut-haor) before and after; c743850 0.354 to 0.346

### Polish pass, 04/11 ("cleaner, more pristine, closer to the brief")

A quality pass over the 03/11 build, not a rebuild. Four changes, all in `design.custom_css` and
`design.fonts`; nothing in `engine/`, `wp/theme/` or `wp/plugin/`.

**1. Body and heading font Alef → Heebo.** The 03/11 pass flagged Alef's digits as "slightly techy" and
left the call open. Measured rather than eyeballed (glyph ink boxes at 100px, via canvas
`actualBoundingBoxAscent/Descent`):

| | digit ink tops | digits below the baseline | cap height | x-height |
|---|---|---|---|---|
| Alef | 53-66 | **3, 4, 5, 7, 9** | 70 | 52 |
| Heebo | 71-72 | none | 71 | 54 |

Alef ships **old-style (text) figures as its only figure set**: most digits sit at x-height, 6 and 8
ascend, and five of the ten drop below the baseline. It is not a style choice that can be switched off:
`font-variant-numeric: lining-nums` and `font-feature-settings: "lnum" 1` both render identically to the
default, so the font has no lining alternative to call on.

That is not a small matter on this site. The two most important strings on it are the מספר מקשר
**072-2594285**, which is the conversion, and the brief's headline claim **20 שנה**; the step list also
runs **01 02 03 04**. In Hebrew setting it is worse than it would be in Latin, because Hebrew letters have
no ascenders or descenders and sit on one even band, so the bouncing digits are the only thing breaking the
line and read as a rendering fault rather than as a typographic style.

Heebo keeps what Alef was picked for: a sturdy, plain, slightly industrial Hebrew sans, self-hosted, on the
validator's readable-body list. Two things it adds: it is a variable face (100-900), so the 800 headings
are a real weight and not a synthesised one, and its bold Latin is a Roboto-grade grotesque, which is much
closer to the logo's own DREAM / FROM / STEEL wordmark than Alef's humanist Latin was.

Uniqueness cost: none. `engine/pool.py` puts only the **heading** font in the measured recipe, and Heebo is
the heading font of no other client (it is body on `c2910210`, `c743850`, `c80220135` and `lehem-erez`,
which the measure does not look at). Measured before and after below.

**2. The hero fix of 03/11 did not hold at 1280.** It was reported as "about 480px" and it is, at 1440 and
only at 1440. At 1280x720 the hero was still **690px (0.96vh)** with 298px of bare photo under the text,
which is the state the user rejected. Cause: `pool.css:442`, a `@media (min-width:768px) and
(max-height:760px)` rule that sets `min-height: min(100svh - 120px, 820px)` **`!important`** on the home
cover/inset/curve hero to keep the buttons above the fold on short laptops. The 03/11 custom rule had the
same specificity and no `!important`, so it lost. The rule now carries `!important` and an extra class
(`.zs-hero--img`) to win outright.

Measured with `py tools/hero-space.py`, same build, before and after:

| viewport | height | empty | biggest bare rect | first button |
|---|---|---|---|---|
| 1440x900 | 494 → **487** px | 81% → 81% | 45% → **43%** | above the fold, both |
| 1280x720 | **690 → 447** px (0.96 → 0.62vh) | 86% → **78%** | 44% → **36%** | above the fold, both |
| 390x844 | 502 → **490** px | 49% → **46%** | 18% → **14%** | above the fold, both |

**3. The FAQ questions on the dark plate were the accent on near-black.** `pool.css:210` sets
`.zs-faq.zs-v-dark .elementor-tab-title { color: var(--c-accent) }`. On this palette that is steel blue
`#6b8ca6` on `#16222c` = **4.56:1**, which clears the 4.5 floor by luck, so `zs qa` passed it with 0 errors,
exactly as it passed the `split:overlap` title that became PR #74. On screen the questions read as disabled
text, and they were the dimmest thing on a page whose section title directly above them is white.
`qa-rules.md`: "On dark grounds titles are white; the accent marks them with a rule or a chip, not by
colouring the words." The questions are now white (16.16:1) and the open one carries an orange rule instead.
This is a **generic theme defect, written up and not fixed here** (see the table below).

**4. One colour for one action.** `pool.css:71` paints the lead-bar submit with `--c-accent`, so
"שלחו לי הצעת מחיר" in the band was steel blue while the identical submit on the contact page and in the
footer form was brand orange. Both are now orange (5.36:1). Every submit on the site is now one colour.

**Looked at and deliberately left alone:**

- the `collage` section. A full-page screenshot showed a bare white panel hanging off the inset photo; it
  is an artifact of the screenshot, not the page. Playwright's `full_page` capture resizes the viewport to
  the whole document, and this theme sizes the collage in `vh` (`editorial.css:170`, `height: clamp(420px,
  64vh, 620px)`), so the layout measured in the capture is not the layout a visitor sees. Re-shot clipped
  to a real 1440x900 viewport the inset fills its white frame exactly (image 287x280 inside a 307x300 box,
  a 10px border all round). **Do not judge this theme from a full-page screenshot.**
- the `split:overlap` card's centred text. Title, body, ticks and button are all `text-align: center`; the
  ragged title only looks mixed because of where its three lines break.
- the hero's remaining bare band at 1440 (a full-width 1440x208 strip under the buttons, 43% of the hero
  box). Worth saying why, because 43% is the same number the rejected 863px hero measured and it looks at
  first like the fix did not work. It is the same number because the metric is a share **of the hero box**,
  so shrinking the hero shrinks the strip and the box together and the ratio barely moves (863px → 487px
  took it from 0.43 to 0.43). The ratio is structural to any full-bleed photo hero with a centred text
  block, and it is what the two heroes the user *approved* look like as well (yadmordechai `cover` 90%
  empty, thewhite-villa `cover` 92%) which is `hero-space.md`'s own conclusion about this site: "steel
  (`curve`) is a full-bleed photo with text over it, exactly like the approved `cover` heroes". What was
  actually wrong was the height, and that is fixed. Shrinking further would buy nothing on this metric and
  would start pushing the curve's clip into the facts plate, whose left edge sits where the ellipse already
  cuts at 94% of the box height. The photo is the message here (a workshop bay stacked with stock), which
  `hero-space.md` question 1 allows when it is said out loud, so it is said here.
- the palette, kit, archetype, section order and all copy. Nothing in the brief asked for them to move and
  the 03/11 uniqueness work depends on them.

| theme defect found, not fixed | where |
|---|---|
| `faq:dark` colours the questions `--c-accent` on `--c-dark`. Same shape as PR #74 and the same reason the gate misses it: a palette whose accent lands just over 4.5:1 passes while looking like disabled text. The variant should paint them white and spend the accent on a rule, as `split:overlap` now does | `wp/theme/zap-base/assets/pool.css:210` |
| `pool.css:442`'s short-laptop hero floor is `!important`, so a site cannot shorten its own hero at 1280x720 without matching `!important` and out-specifying it. It also fights the `curve` variant, whose clip already eats the bottom of the box | `wp/theme/zap-base/assets/pool.css:442` |
| `zs qa`'s link check opens 8 connections at once (`ThreadPoolExecutor(8)`) with a 20s timeout, against a local dev server that serialises requests. With several client sessions building on the same PC at once, pages that answer 200 in 1.4-4.4s on their own start reporting `link timed out`, and `zs qa` calls them **errors**. On 04/11 the same unchanged build scored 0 errors in a quiet window and 13 then 8 "errors" while four other agents ran `zs qa`. Nothing is wrong with the pages; the gate is reporting machine load as a site defect, which is the kind of false red that gets a gate ignored. Worth a smaller pool, a longer timeout, or treating a timeout as a WARN distinct from a real non-200 | `engine/qa.py:318-335` |
