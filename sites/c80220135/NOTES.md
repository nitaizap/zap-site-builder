# מרכז שירות יד מרדכי (80220135) — notes

Branch `site/c80220135`. Built in automatic mode from `brief/brief.md` (spec sheet
`איפיון אתר - מרכז שירות יד מרדכי - 80220135_1.docx`, dated 01/11/2026) and the 25 files in
`assets/client/` copied from `F:\SiteContent\80220135`.

## Facts table

| fact | value | source |
|---|---|---|
| business name | מרכז שירות יד מרדכי | spec, שם העסק |
| legal / client name | מוסך יד מרדכי | spec, שם הלקוח |
| client id | 80220135 | spec |
| contact person | ערן שטרנברג | spec, איש קשר |
| address | קיבוץ יד מרדכי, 7914500 | spec, כתובת העסק |
| area served | אשקלון והסביבה | spec, אזורי שירות |
| phone | 08-6720513 | spec, טלפון לאתר |
| WhatsApp | 052-6758069 | spec, וואטסאפ |
| site e-mail / leads | musach@y-m.co.il | spec, אימייל לאתר + מייל לטופס לידים |
| hours | א׳–ה׳ 07:00–16:00, ו׳ 07:00–12:30, שבת סגור | spec, שעות פעילות |
| Facebook | facebook.com/ymmazdaford | spec |
| Instagram | instagram.com/yad_mordechai_service_center | spec |
| founded | שנות ה-50 של המאה ה-20 | spec, תחומי עיסוק |
| Mazda licence | 1996, מטעם דלק מוטורס בע״מ | spec, תחומי עיסוק |
| Ford licence | 2000 | spec |
| Dongfeng + Voyah licence | 2025 | spec |
| staff | כ-13 עובדים | spec |
| ownership | בבעלות קיבוץ יד מרדכי, מנוהל בידי ערן שטרנברג | spec |
| commercial vehicles | תוכנית "המחלקה הראשונה למסחריות" של היבואן | spec |
| parts offer | עד 45% הנחה על חלקים מקוריים, רכבים מעל 3 שנים, ט.ל.ח | spec, מבצע חלקים מקוריים |
| logo | **none** ("אין לוגו לעסק") | spec, עיצוב ומותג |
| brand colours | none given, "יד חופשית למעצב — צבעים לפי החלטת המעצב" | spec |
| Zap tracking number | not given (מספר מקשר זאפ left empty) | spec → `phone_is_virtual` stays false |
| blog | not requested (אתר SEO (בלוג) and מאמרים both empty) | spec |
| package | not named anywhere | intake.json `missing` |

### Research, done after the network opened

The session's network policy denied every outbound host at first. Once it was opened, the client's existing
site was read properly with `bin/zs grab` (pages and images in `research/`), and the logo question was chased
to the end. What came back:

| source | result |
|---|---|
| ym-mazdaford.co.il | read. Confirms every fact on the new site (licence years, ownership, staff, waiting room, VIP service, parts programme). No logo image: its brand is styled text. No new photographs: its images are the same 2022 shots already in `assets/`, cropped, plus one manufacturer stock composite that was not used |
| facebook.com/ymmazdaford | read. Profile picture is a photograph of the pylon sign, not a logo |
| instagram.com/yad_mordechai_service_center | login wall, not read |
| d.co.il/80220135 | blocks automated reading, not circumvented. Its reviews do surface on the client's own site: 4.84 from 31 reviews |

Two things the old site turned up that the spec does not mention, both in OPEN-ITEMS: it displays a **Zap
tracking number, 072-3263207**, on its home page, and its **Dapei Zahav listing is populated**, which makes
the reviews block the spec asks for one verification away.

Still unread: the Maps CID and geo coordinates, and the Instagram gallery.

## Keyword map

Volume and KD are **unknown**: no Ahrefs connector and no SERP access from this session (see above).

| page | key | keyword | H1 | menu label |
|---|---|---|---|---|
| home | `` | מוסך מורשה מאזדה ופורד באשקלון | מרכז שירות יד מרדכי | דף הבית |
| about | `אודות` | מרכז שירות יד מרדכי | אודות מרכז שירות יד מרדכי | אודות |
| service | `מכונאות-רכב` | מכונאות רכב באשקלון | מכונאות רכב | מכונאות רכב |
| service | `פחחות-וצבע` | פחחות וצבע באשקלון | פחחות וצבע | פחחות וצבע |
| service | `דיאגנוסטיקה-ואבחון` | דיאגנוסטיקה לרכב באשקלון | דיאגנוסטיקה ואבחון | דיאגנוסטיקה ואבחון |
| service | `חשמל-רכב` | חשמלאי רכב באשקלון | חשמל רכב | חשמל רכב |
| service | `מערכות-מיזוג-אוויר` | תיקון מזגן לרכב באשקלון | מערכות מיזוג אוויר | מערכות מיזוג אוויר |
| service | `צמיגים` | צמיגים באשקלון | צמיגים | צמיגים |
| contact | `צרו-קשר` | מוסך יד מרדכי טלפון | צרו קשר | צרו קשר |

Slug = H1 = menu label on every service page. Privacy and the accessibility statement are added by the
engine. 9 pages, inside the `standard` cap of 12.

## Design brief (the three lines)

- **Subject:** an importer-authorised service centre, not a general garage. It handles four marques only
  (Mazda, Ford, Dongfeng, Voyah), is owned by the kibbutz it sits in, and does every job on the car in one
  building: mechanics, bodywork and paint, diagnostics, auto electrics, air conditioning, tyres.
- **Audience and moment:** a Mazda or Ford owner around Ashkelon whose car is due for a service or has a
  fault, choosing between the dealer chain in the city and the local centre. What they want to know:
  are you really authorised for my model, will I get a price before the work, and do I lose my day.
- **The page's one job:** phone, or leave details, to book the car in.

## The direction (picked in automatic mode, then reworked for the uniqueness gate)

| lever | choice | why |
|---|---|---|
| `tier` | `standard` | the spec's own page list is 9 pages; `basic` caps at 5 (OPEN-ITEMS 1) |
| `kit` | `bands` | pool.md gives it to trades. Not used by the last 3 clients, nor by c80386843 (`sidebar`) |
| `archetype` | `proof` | the business sells authorisation, so the evidence comes before any claim |
| `base_template` | 5 (metal works) | workshop template. Deviations: petrol and bronze instead of white and red, a full-bleed `cover` hero of the real facade, icon service cards instead of overlay tiles |
| palette | petrol `#14525e` + bronze `#b45309` | re-set 03/11. The graphite primary (`#333b41`) and near-black footer read as the same industrial dark as c80386843's steel navy and pushed the pair to 40% (an ERROR). Petrol is the colour of the building in the client's own 2022 photos, which is what NOTES first reasoned from, so this restores the documented brand rather than inventing one. Footer `#0d3a44`, surface `#e3edef`; `muted` darkened to `#41505a` to hold 6:1 on the new tinted surface |
| `preset` | `industrial` | sharp, heavy, accent rules. No other client uses it |
| `hero` | `image` + `cover` | the 2022 facade photo is the strongest asset the client has |
| fonts | IBM Plex Sans Hebrew / Heebo | "corporate, precise", which is what an importer licence reads as |
| radius | 4 | squared, workshop |
| `header.topbar` | on | kept on 03/11, but not for the reason first written here ("no other client turns the bar on" was wrong: 4 of the 5 measured clients run one). It stays because it carries real content and because turning it off measurably *raised* the uniqueness score against c80386843, whose bar is off. Zap QA has a standing note against a top strip, so it is flagged for the team in OPEN-ITEMS 14 |

**The one bold thing:** the authorisation band under the hero, the marque logos at a uniform size, then a
facts card of the real licence years (1996 / 2000 / 2025 / 2025) and the team size.

### Palette, and why it is this one
The premises were rebuilt between the 2020 and the 2022 photos: the old building was bright blue, the current
one is graphite grey and white with a black Mazda pylon. The palette follows the building as it is now.

The palette went graphite for a while to dodge a collision (below) and came back to petrol on 03/11, which
is the colour the building actually reads as in the 2022 photos.

| token | value | measured 03/11 |
|---|---|---|
| `primary` | `#14525e` petrol | white on it 8.76:1 |
| `accent` | `#b45309` signal bronze | 5.02:1 on white |
| `dark` (footer) | `#0d3a44` deep petrol | white on it 12.31:1 |
| `surface` | `#e3edef` petrol tint | body text on it 12.86:1 |
| `muted` | `#41505a` | 8.33:1 on white, 6.99:1 on surface |

The graphite set it replaced was `primary #333b41`, `dark #1f2529`, `surface #f4f4f3`, `muted #4e575e`.

### The uniqueness gate, and what it cost
`c80386843` (מסגרית Dream from Steel), built in a parallel session, independently chose a petrol-and-bronze
palette very close to this site's first one. The two measured **58% alike**, well over the 40% limit.
(Read the dates: that was their *first* palette. `c80386843` has since moved to burnt orange `#b84606` with a
steel-blue accent, which is why petrol became available again on 03/11 and measures 36%. If that site's
palette moves back toward petrol, this one has to move again.)

Palette alone could not fix it. The measure's `button` term samples the first primary button outside the hero,
and on both sites that was the closing CTA band, which the theme paints white on every site: a near-identical
reading worth 0.15 of the score before anything else. Giving the facts card its own call to action
("לתיאום כניסת רכב", higher up the page and useful in its own right) made the sampled button a real colour.
With that, the graphite palette, the top bar and `steps` as `cards` instead of `stack`, it measured **39%**.
That did not hold: re-measured on 03/11 the pair had drifted to **40%**, an ERROR, because `c80386843` kept
building. The graphite palette was the cause and was replaced with the petrol one above; it reads **36%** now
(OPEN-ITEMS 17).

Two things were tried and reverted, both recorded so nobody repeats them: `tone: light` (collides with
patoccina and mehirut-haor, which are both light) and a `split` hero (it crops the wide facade photo into a
portrait box and loses the building, which is the one thing worth showing). A dark header was also tried and
dropped: it only moved the number, and it is not a choice worth defending to this client.

## Home composition (10 sections, archetype `proof`)

1. `hero` `cover` — facade 2022, H1 = the client's name, keyword opens the lead
2. `logos` `band` — the badge beside the text, Mazda / Ford / Dongfeng / Voyah in a 2x2, all chips one height
3. `facts` — licence years and team size, with the page's first call to action
4. `reviews` — the Dapei Zahav widget (customer id 80220135); renders only on a pushed site
5. `cards` — the six service pages, one meaningful icon each
6. `split` `frame` — "מגוון רחב של שירותים במקום אחד", workshop photo
7. `steps` `cards` — how a visit runs, taken from the brief's own description
8. `split` (`bg: plain`) — "הלקוח בראש סדר העדיפויות", waiting room photo
9. `cta` — the original-parts offer the spec asks for
10. `faq` `outline` — six questions, each answered from a spec fact

### What changed on 04/11, and why

- **`features` `checks` removed.** It listed six labels — יועץ שירות צמוד, הצעת מחיר לפני העבודה,
  חדר המתנה ממוזג, תיאום כניסה מראש, איסוף והחזרת הרכב, העברת טסט במכון רישוי — and every one of them is
  already said by the `steps` block immediately above it or by the hero bullets. Six identical check icons
  on a dark ground restating the previous section is padding, not evidence, and it was the least finished
  looking block on the page. `qa-rules.md` lists "a row of identical ticks" as a reviewer rejection in its
  own right, so this was a rule the page was already on the wrong side of, not only a taste call.
- **The waiting-room `split` moved to the plain ground.** `features`, that `split` and `cta` were all on
  brand petrol: 1,658 px of unbroken dark at the foot of the page. Removing one and lightening another
  restores an alternating rhythm, and the waiting-room photo reads better on white.

- **Prose column centred, and the contact map's empty column collapsed.** Both are worked around in this
  client's own `design.custom_css` and both are defects outside this site: the theme never centres
  `.e-con.zs-prose` (OPEN-ITEMS 18) and the plugin's map widget renders nothing (OPEN-ITEMS 20). Neither was
  fixed at source from a client session.

No two neighbours share a type or a shape. The page does not end on a `cta`, so the footer lead form is the
last action.

## Images

Seven real photographs were usable out of the 25 files. What the filenames hid:

- `Mini-Site-Image_80220135-minisite.jpg` is a generic Zap banner showing **KIA** cars. Not used.
- `חזית.jpg` / `חזית2.jpg` (2020) show the **old blue building**. Not used: the 2022 photos show the
  current grey facade, and a hero of the old building would misrepresent the place.
- `חזית.jpg` appears twice (identical bytes) and `לוגו-מחלקה-ראשונה.JPG` / `מחלקה-ראשונה-למסחריות.JPG`
  are the same file twice.
- `סטריפ_11999575_...jpg` is an old campaign graphic, not a photograph. It does corroborate the 45% parts
  offer, which is also in the spec.

| key | file | what it shows |
|---|---|---|
| `facade` | 20220520_124727 | the current facade, centred (home hero) |
| `facade-drive` | 20220520_124705 | approach and car park (about, חשמל רכב) |
| `facade-side` | 20220520_124757 | the workshop door from the side (contact, פחחות וצבע) |
| `pylon` | 20220520_124843 | the Mazda/Ford/יד מרדכי sign (parts-offer band, צמיגים) |
| `workshop` | אולם-עבודה | cars on the lifts (מכונאות רכב, "everything in one place") |
| `waiting` | חדר-המתנה | the air-conditioned waiting room looking into the workshop |
| `reception` | משרד-קבלה | the service desk with the lit Mazda and Ford marks (דיאגנוסטיקה) |

Marque logos: `logo-mazda` from `Logo_FullColor_Horizontal.png`, `logo-ford` from
`לוגו-פורד-ללא-רקע.png`, `logo-first-dept` from `לוגו-מחלקה-ראשונה.JPG`. No AI images were generated.

## Copy

All page copy is written from the spec's own sentences. The service pages add only generic automotive
explanation ("what the service covers", "when to call"), never a client-specific claim the spec does not
make. Grep checks run before commit: no em dash, no en dash used as punctuation, no rating, review count,
superlative or placeholder anywhere in site.json.

Two spec statements disagree about age: שנות פעילות says "מעל 30 שנה" while תחומי עיסוק says the centre was
founded in the 1950s. The site uses only the 1950s statement and the dated licence years, and claims no
number of years. See OPEN-ITEMS 5.

## Build and QA result (verified)

Run on the merged tree, after the theme fixes this build found went to `main` in PR #59.

| gate | result |
|---|---|
| `bin/zs build c80220135` | builds clean |
| `bin/zs qa c80220135` | **0 errors, 0 warnings**, exit 0 (re-run 03/11) |
| `bin/zs seo c80220135` | **0 FAIL**, 39 rows: 34 pass, 5 manual (every MANUAL row looked at, below) |
| `bin/zs pool c80220135` | exit 0: **36%** against c80386843, the nearest other client (limit 40%) |
| `engine/validate.py` | 0 errors, 2 warnings (privacy confirmation, Dapei Zahav id) |

### The SEO checklist's MANUAL rows, looked at

| row | what I checked |
|---|---|
| 1 מספר מקשר | The spec leaves מספר מקשר זאפ empty, so the site shows the client's own 08-6720513 and `phone_is_virtual` is false. Nothing to pop up. If the sites team assigns a tracking number, see OPEN-ITEMS 8 |
| 8 FAQ relevant | All 15 answers (6 home, 3 per service page, 3 per post) read against the facts table above. Every one traces to a spec line: the four marques and their licence years, booking ahead and out-of-hours collection, the price quote, the commercial-vehicles programme, the hours, the 45% parts offer |
| 9 client images used | 7 of the 25 F: drive files are real usable photographs and all 7 are on the site, plus the 2 marque logos and the commercial-vehicles badge. 0 AI images. What was excluded and why is in the Images section above |
| +1 phone, email, address | Site shows 08-6720513, musach@y-m.co.il, קיבוץ יד מרדכי. Matches the spec byte for byte |
| +6 mobile and 1280 | Home read at 390 in full; service, contact, blog and post pages shot at 390; header measured and viewed at 1536, 1440, 1366, 1280, 1100 and 1025. No overlaps, no horizontal scroll, no wrapped labels |

### Theme bugs this build found (fixed generically, PR #59, merged)

1. `zs-accent-low` did not cover the footer: its contact icons and wordmark measured 2.60 on the dark footer.
2. `cta` variant `photo` puts a dark button on its accent panel, invisible when the accent is dark (2.60).
3. A business with no logo got a broken header: the name as text was shrunk into the logo's slot by Elementor's
   flex sizing and spilled out of the viewport. Also: menu labels wrapped mid-word, and the header's side grid
   tracks let a wide brand slide under the menu.
4. `pool.known()`: the branch-fingerprint loop still lacked the shape guard that #58 gave the registry loop.

Two more were found here but landed first from other sessions, so this branch dropped its own versions:
white text on a light panel inside a colour band (#57) and the `clients.json` crash in `zs qa` (#58).

### Not a bug, worth remembering

- The reveal animation leaves a `translateY(18px)` on a section's title until it scrolls into view, so a
  full-page screenshot shows the title overlapping the text under it. Scroll the element in and wait before
  judging. This is what the playbook means about scrolled screenshots.
- `wpsite.create()` runs the Hebrew language install with `check=False`. When that download fails the site
  stays `en_US` and the whole Hebrew site renders **LTR**, which invalidates every layout measurement: the
  burger lands under the accessibility button and `zs qa` dies on a click timeout instead of reporting. It
  happened in this environment to both this site and the sample. Flagged on PR #59.
