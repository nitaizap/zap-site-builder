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
| logo, brand colours, "sites you liked" | not given on the spec sheet; the team says a logo exists but it never reached the branch | spec sheet §6 (blank), Noam 02/11 (`inbox/2026-11-02-feedback.md`) |
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
| `tier` | `standard` | the spec names no package; its own sitemap is 6 pages, over basic's cap of 5. See OPEN-ITEMS |
| `kit` | `sidebar` | the section title sits in a side column beside long content. This client has **no portfolio to show**, so the site has to convince by explaining, and the skeleton is built for explanation. Also the only free kit with a dark footer (`bands` is on c80220135, `magazine` on lehem-erez) |
| `archetype` | `statement` | type-led: one confident line ("אין אצלנו קטלוג"), then short proof. The right shape for a site with four atmosphere photos and no work to show |
| `base_template` | 1 | navy-on-white, offset frames. **Deliberately not template 5** (the metal-works demo, white + red): the obvious pick for a metalworker and already used by the pilot branches |
| preset | `editorial` | serif headings, hairlines, no shadows: craft rather than heavy industry |
| palette | primary petrol steel `#15606b`, accent brass `#b07d22` | steel and brass, the two metals in every one of the client's photos. Measured as the most distant brand colour available: brass and amber are taken by betzel-hateena and kisos-beach-club, navy by bella-mare, blue by nick-itum, red by mehirut-haor, maroon by patoccina, olive by white-villa |
| fonts | Frank Ruhl Libre / Assistant | the business is bespoke, not mass production. A serif headline against brushed steel reads as craft |
| radius | 10 | sharp (2) was the first choice, but it made the measured page frame identical to mehirut-haor's |
| hero | `centered` + the workshop photo | statement first, photo second |
| motion | `subtle` | the brief asks for no motion |

**The one bold thing:** the H1 at full width over the workshop bay, with the whole page then running as a
single explained argument. Nothing else competes with it.

Home: `hero → chapters → prose:band → cards → split:overlap → steps:stack → facts → leadbar:photo →
collage → cta → faq:dark` (11 sections). Components picked for what none of the other clients use:
`chapters`, `prose:band`, `facts`, `collage`, `steps:stack`, `faq:dark` appear on no other client site.

### Critique before delivery, and what changed after it

- the `overlay` section opened with a near-square phone crop of a landscape photo, upscaled and soft
  (`pool.md`: wide photos never go into tall crops on phones) → replaced with `split:overlap`
- the home measured 43-50% like patoccina, mehirut-haor and bella-mare on the first build (brass palette,
  `frame` kit, `cards`/`features:checks`/`split:card`/`faq:outline`, the components everyone uses) →
  palette, kit and seven of the eleven components changed. Final: 38% (mehirut-haor), 35% (white-villa)
- the sidebar kit leaves the title column empty on a section without a title (the service-page `prose`).
  Kept: every section's content then starts at the same x, which is the kit's point

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

Known and not fixed: the `overlay` section's phone box is `56vh` while the browser picks a source by width,
so a landscape photo in it is upscaled and soft. Avoided here by not using `overlay`.
